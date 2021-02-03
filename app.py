import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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


# Routes

# 404 error capture
@app.errorhandler(404)
def page_not_found(e):
    """page_not_found:
    * This function renders the 404.html template if a 404 error is occured.
    """
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# Home Page
@app.route("/")
def home():
    """home:
    * This functio renders the home.html 
    """
    try:
        if session["user"]:
            user = True
    except KeyError:
        user = False
    finally:
        top_recipes = list(
            mongo.db.recipes.find().sort([("votes", -1)]).limit(4))
        return render_template("home.html", top_recipes=top_recipes, user=user)


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """register:

    * This function renders register.html page ['GET'].
    * This function pushes new user information to the database ['POST'].
    * Redirects to register.html template if POST request error
    with a supporting flash message.
    """
    if request.method == "POST":
        # check if username already exists in DB
        exisiting_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if exisiting_user:
            flash("Username already exsits")
            return redirect(url_for("register"))

        register_user = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register_user)

        # put the user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("recipes", username=session["user"]))
    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    """login:

    * This function renders login.html page ['GET'].
    * This function verifies login details with the database ['POST'].
    * Redirects to login.html template if POST request error
    with a supporting flash message.
    """
    if request.method == "POST":
        # check if username already exists in DB
        exisiting_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if exisiting_user:
            # ensure hashed password matches users input
            if check_password_hash(exisiting_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
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


# Logout
@app.route("/logout")
def logout():
    """logout:
    * This function removes the user variable from the session cookies and redirects to the recipes page.
    """
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("recipes"))


@app.route("/recipes")
def recipes():
    """recipes:
    * This function renders recipes.html page with varied recipes,
    based on the arguments passed and accessed.
    """
    try:
        if session["user"]:
            user = True
    except KeyError:
        user = False
    finally:
        query = request.args.get("query")
        category = request.args.get("category")
        page = request.args.get("page")
        # Check if search query
        if query is not None:
            recipes_list = list(
                mongo.db.recipes.find(
                    {"$text": {"$search": query}}))
        # Check if category filter
        elif category is not None:
            recipes_list = list(
                mongo.db.recipes.find(
                    {"category": category.capitalize()}).sort([("_id", -1)]))
        else:
            # Find all recipes
            recipes_list = list(
                mongo.db.recipes.find().sort([("_id", -1)]))

        # Pagination
        if page is not None:
            current_page = int(page)
        else:
            current_page = 1

        # Pagination Variables
        number_per_page = 6
        number_of_pages = round(len(recipes_list) / number_per_page)
        if number_of_pages < 1:
            number_of_pages = 1

        # Paginate Recipes List
        begin = (current_page - 1) * number_per_page
        end = begin + number_per_page
        recipes_list = recipes_list[begin:end]
        return render_template(
            "recipes.html", recipes=recipes_list, user=user, category=category,
            current_page=current_page, number_of_pages=number_of_pages)


# Next Recipe Page
@app.route("/next_page/<current_page>", methods=["GET", "POST"])
def next_page(current_page):
    """next_page:
    * This function redirects to recipes the function, with an updated page argument variable
    """
    category = request.args.get("category")
    if current_page == (request.args.get("number_of_pages")):
        page = current_page
        return redirect(url_for('recipes', page=page, category=category))
    else:
        page = int(current_page) + 1
        return redirect(url_for('recipes', page=page, category=category))


# Previous Recipe Page
@app.route("/prev_page/<current_page>", methods=["GET", "POST"])
def prev_page(current_page):
    """previous_page:
    * This function redirects to the recipes function, with an updated page argument variable
    """
    category = request.args.get("category")
    if int(current_page) == 1:
        return redirect(url_for('recipes', page=None, category=category))
    else:
        page = int(current_page) - 1
        return redirect(url_for('recipes', page=page, category=category))


# Add Like to Recipe
@app.route("/add-recommendation/<recipe_id>", methods=["GET", "POST"])
def add_recommendation(recipe_id):
    """add_recommendation:
    * This function redirects to the recipe page passed into it, once it updates the recipe's vote count in the database.
    """
    if request.method == 'POST':
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        votes = recipe['votes']
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)},
            {'$set': {"votes": votes + 1}}, upsert=False)
        return redirect(url_for('get_recipe', recipe_id=recipe_id))


# Add Recipe
@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    """add_recipe:

    * This function renders add-recipe.html page if ['GET'].
    * This function posts a new recipe to the database and redirects to all recipes if ['POST'].
    * Redirects to login.html template if Key Error with a supporting flash message.
    """
    try:
        if session["user"]:
            # grab the session users username from the db
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            categories = mongo.db.categories.find()
            return render_template(
                "add-recipe.html", categories=categories, username=username)

    except KeyError:
        flash("You need to be logged in to add a recipe.")
        return redirect(url_for("login"))

    finally:
        if request.method == 'POST':
            total_time = int(request.form.get(
                "recipe_preptime")) + int(request.form.get("recipe_cooktime"))
            recipe = {
                "category": request.form.get("category_name"),
                "name": request.form.get("recipe_name"),
                "short_description": request.form.get("recipe_description"),
                "recipe_info": [request.form.get(
                    "recipe_yield"), request.form.get(
                        "recipe_preptime"), request.form.get(
                            "recipe_cooktime"), total_time],
                "ingredients": request.form.getlist("recipe_ingredient"),
                "method": request.form.getlist("recipe_step"),
                "img_url": request.form.get("recipe_img_url"),
                "votes": 0,
                "added_by": username
            }

            mongo.db.recipes.insert_one(recipe)
            return redirect(url_for("recipes"))


# Edit Recipe
@app.route("/edit-recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """edit_recipe:

    * ['GET'] This function renders edit-recipe.html page.
    * ['POST'] This function updates a recipe in the database with the functions passed recipe_id. It then redirects to all recipes.
    * Redirects to login.html template if Key Error with a supporting flash message.
    """
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    print(recipe["votes"])
    try:
        if session["user"]:
            # grab the session users username from the db
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            categories = mongo.db.categories.find()
            return render_template(
                "edit-recipe.html", categories=categories,
                username=username, recipe=recipe)

    except KeyError:
        flash("You need to be logged in to edit a recipe.")
        return redirect(url_for("login"))

    finally:
        if request.method == 'POST':
            submit = {
                "category": request.form.get("category_name"),
                "name": request.form.get("recipe_name"),
                "short_description": request.form.get("recipe_description"),
                "recipe_info": [request.form.get(
                    "recipe_yield"), request.form.get(
                    "recipe_preptime"), request.form.get("recipe_cooktime")],
                "ingredients": request.form.getlist("recipe_ingredient"),
                "method": request.form.getlist("recipe_step"),
                "img_url": request.form.get("recipe_img_url"),
                "votes": recipe["votes"],
                "added_by": username
            }

            mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
            flash("Recipe Successfully Updated")
            return redirect(url_for("recipes"))


# Delete Recipe
@app.route("/delete-recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """delete_recipe:
    * This function removes the recipe from the database with recipe_id == that passed into the function. It then redirects to all recipes.
    """
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    mongo.db.reviews.remove({"recipe_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("recipes"))


# Delete Review
@app.route("/delete-review/<review_id>")
def delete_review(review_id):
    """delete_review:
    * This function removes the comment from the reviews database with review_id == that passed into the function. It then redirects back to the relevant recipe page.
    """
    recipe_id = request.args.get("recipe_id")
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Comment Successfully Deleted")
    return redirect(url_for("get_recipe", recipe_id=recipe_id))


# Add Review
@app.route("/add-review/<recipe_id>", methods=["GET", "POST"])
def add_review(recipe_id):
    """add_review:
    * This function adds a comment and rating to the reviews database. It then redirects back to the relevant recipe page once completed.
    """
    if request.method == 'POST':
        if session["user"]:
            review = {
                "recipe_review": request.form.get("recipe_review"),
                "recipe_rating": request.form.get("recipe_rating"),
                "recipe_id": recipe_id,
                "added_by": username
            }
            mongo.db.reviews.insert_one(review)
            return redirect(url_for("get_recipe", recipe_id=recipe_id))
        else:
            flash("You need to be logged in to add a review.")
            return redirect(url_for("login"))

# Get Recipe
@app.route("/get-recipe/<recipe_id>")
def get_recipe(recipe_id):
    """get_recipe:
    * This function renders the get_recipe.html template, using the relevant recipe, by pulling data from the recipes database using the recipe_id passed into the route/function.
    """
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
            "get-recipe.html", recipe=recipe, reviews=reviews,
            user=user, username=username, recipe_id=recipe_id)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
