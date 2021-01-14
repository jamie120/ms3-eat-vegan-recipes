import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, jsonify)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
    top_recipes = list(mongo.db.recipes.find().sort([("votes", 1)]).limit(4))
    return render_template("site_landing.html", top_recipes=top_recipes)


@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("get_recipes.html", recipes=recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == 'POST':
        ingredients_string = str(request.json)
        print(ingredients_string)
        print(type(ingredients_string))
        ingredient_list = json.loads(ingredients_string)
        print(ingredient_list)
        print(type(ingredient_list))
        total_time = int(request.form.get("recipe_preptime")) * int(request.form.get("recipe_cooktime"))
        recipe = {
            "category": request.form.get("category_name"),
            "name": request.form.get("recipe_name"),
            "short_description": request.form.get("recipe_description"),
            "recipe_info": [request.form.get("recipe_yield"), request.form.get("recipe_preptime"), request.form.get("recipe_cooktime"), total_time],
            #"ingredients": ingredient_list['ingredient_list']
        }
        mongo.db.recipes.insert_one(recipe)
        return redirect(url_for("get_recipes"))

    categories = mongo.db.categories.find()
    ingredients = []
    return render_template("add_recipe.html", categories=categories, ingredients=ingredients)


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
