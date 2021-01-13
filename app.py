import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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
