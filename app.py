import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, jsonify)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    try:
        if session["user"]:
            user = True
    except KeyError:
            user = False
    finally:
        top_recipes = list(mongo.db.recipes.find().sort([("votes", -1)]).limit(4))
        return render_template("home.html", top_recipes=top_recipes, user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in DB
        exisiting_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if exisiting_user:
            flash("Username already exsits")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("recipes", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username already exists in DB
        exisiting_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if exisiting_user:
            # ensure hashed password matches users input
            if check_password_hash(
                exisiting_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "recipes", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("recipes"))


@app.route("/recipes")
def recipes():
    try:
        if session["user"]:
            user = True
    except KeyError:
            user = False
    finally:
        query = request.args.get("query")
        category = request.args.get("category")
        if query is not None:
            recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
        elif category is not None:
            recipes = list(mongo.db.recipes.find({"category": category.capitalize()}))
        else:
            recipes = list(mongo.db.recipes.find())
        return render_template("recipes.html", recipes=recipes, user=user, category=category)


@app.route("/add_recommendation/<recipe_id>", methods=["GET", "POST"])
def add_recommendation(recipe_id):
    if request.method == 'POST':
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        print(recipe)
        votes = recipe['votes']
        print(votes)
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)}, {'$set': {"votes": votes + 1}}, upsert=False)
        return redirect(url_for('get_recipe', recipe_id=recipe_id))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    try:
        if session["user"]:
            # grab the session users username from the db
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            categories = mongo.db.categories.find()
            return render_template("add_recipe.html", categories=categories, username=username)

    except KeyError:
        flash("You need to be logged in to add a recipe.")
        return redirect(url_for("login"))

    finally:
        if request.method == 'POST':
            total_time = int(request.form.get("recipe_preptime")) + int(request.form.get("recipe_cooktime"))
            recipe = {
                "category": request.form.get("category_name"),
                "name": request.form.get("recipe_name"),
                "short_description": request.form.get("recipe_description"),
                "recipe_info": [request.form.get("recipe_yield"), request.form.get("recipe_preptime"), request.form.get("recipe_cooktime"), total_time],
                "ingredients": request.form.getlist("recipe_ingredient"),
                "method": request.form.getlist("recipe_step"),
                "img_url": request.form.get("recipe_img_url"),
                "votes": 0,
                "added_by": username
            }

            mongo.db.recipes.insert_one(recipe)
            return redirect(url_for("recipes"))


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    try:
        if session["user"]:
            # grab the session users username from the db
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            categories = mongo.db.categories.find()
            recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
            return render_template(
                "edit_recipe.html", categories=categories, username=username, recipe=recipe)

    except KeyError:
        flash("You need to be logged in to edit a recipe.")
        return redirect(url_for("login"))

    finally:
        if request.method == 'POST':
            submit = {
                "category": request.form.get("category_name"),
                "name": request.form.get("recipe_name"),
                "short_description": request.form.get("recipe_description"),
                "recipe_info": [request.form.get("recipe_yield"), request.form.get("recipe_preptime"), request.form.get("recipe_cooktime")],
                "ingredients": request.form.getlist("recipe_ingredient"),
                "method": request.form.getlist("recipe_step"),
                "img_url": request.form.get("recipe_img_url"),
                "votes": 0,
                "added_by": username
            }

            mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
            flash("Recipe Successfully Updated")
            return redirect(url_for("recipes"))


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    mongo.db.reviews.remove({"recipe_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("recipes"))


@app.route("/delete_review/<review_id><recipe_id>")
def delete_review(review_id, recipe_id):
    print(f"recipeID: -{recipe_id}")
    print(f"reviewID: -{review_id}")
    #mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Comment Successfully Deleted")
    return redirect(url_for("get_recipe", recipe_id=recipe_id))


@app.route("/add_review/<recipe_id>", methods=["GET", "POST"])
def add_review(recipe_id):
    try:
        if session["user"]:
            # grab the session users username from the db
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
            return render_template(
                "add_review.html", username=username, recipe=recipe)

    except KeyError:
        flash("You need to be logged in to add a review.")
        return redirect(url_for("login"))

    finally:
        if request.method == 'POST':
            review = {
                "recipe_review": request.form.get("recipe_review"),
                "recipe_rating": request.form.get("recipe_rating"),
                "recipe_id": recipe_id,
                "added_by": username
            }

            mongo.db.reviews.insert_one(review)
            return redirect(url_for("get_recipe", recipe_id=recipe_id))


@app.route("/get_recipe/<recipe_id>")
def get_recipe(recipe_id):
    try:
        if session["user"]:
            user = True
            # grab the session users username from the db
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
    except KeyError:
            user = False
            username = False
    finally:
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        reviews = list(mongo.db.reviews.find({"recipe_id": recipe_id}))
        return render_template(
            "get_recipe.html", recipe=recipe, reviews=reviews, user=user, username=username, recipe_id=recipe_id)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
