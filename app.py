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
@app.route("/site_landing")
def site_landing():
    top_recipes = list(mongo.db.recipes.find().sort([("votes", -1)]).limit(4))
    return render_template("site_landing.html", top_recipes=top_recipes)


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
        return redirect(url_for("get_recipes", username=session["user"]))
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
                        "get_recipes", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("get_recipes.html", recipes=recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == 'POST':
        total_time = int(request.form.get("recipe_preptime")) * int(request.form.get("recipe_cooktime"))
        recipe = {
            "category": request.form.get("category_name"),
            "name": request.form.get("recipe_name"),
            "short_description": request.form.get("recipe_description"),
            "recipe_info": [request.form.get("recipe_yield"), request.form.get("recipe_preptime"), request.form.get("recipe_cooktime"), total_time],
            "ingredients": request.form.getlist("recipe_ingredient"),
            "img_url": request.form.get("recipe_img_url"),
            "votes": 0
        }

        mongo.db.recipes.insert_one(recipe)
        return redirect(url_for("get_recipes"))

    categories = mongo.db.categories.find()
    return render_template("add_recipe.html", categories=categories)


@app.route("/get_recipes_filtered/<category>")
def get_recipes_filtered(category):
    print(category)
    recipes = list(mongo.db.recipes.find({"category": category}))
    return render_template("get_recipes_filtered.html", recipes=recipes, category=category)


@app.route("/get_recipe/<recipe_id>")
def get_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("get_recipe.html", recipe=recipe)


@app.route("/search_recipes", methods=["GET", "POST"])
def search_recipes():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("get_recipes.html", recipes=recipes)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
