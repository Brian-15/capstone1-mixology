

import os, pdb
from flask import Flask, json, request, redirect, jsonify, flash, session, g
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import HTTPException
import flask_debugtoolbar
from models import Drink, DrinkIngredient, db, connect_db, User, Category, Ingredient
from forms import LoginForm, RegisterForm, SearchForm

USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql:///mixology")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

app.config["SECRET_KEY"] = "s3cr1t059"

debug = DebugToolbarExtension(app)

ingredients = [(ingr.id, ingr.name.title()) for ingr in Ingredient.query.order_by(Ingredient.name).all()]
categories = [(cat.id, cat.name.title()) for cat in Category.query.order_by(Category.name).all()]

# ------------------------------------------------------------- #
# ---------------------- User Routes -------------------------- #
# ------------------------------------------------------------- #

@app.before_request
def add_user_to_g():
    """Add user to flask's global g variable."""

    if USER_KEY in session:
        g.user = User.query.get(session[USER_KEY])

    else:
        g.user = None

@app.route("/")
def root():

    return redirect("/home")

@app.route("/home")
def home():

    return render_template("home.html",
                           title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():

    if g.user:
        flash("You must be logged out to view this.", "danger")
        return redirect("/home")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash("Successfully logged in.", "success")
            session[USER_KEY] = user.id
            return redirect("/home")
        else:
            flash("Invalid login credentials.", "danger")
            
    return render_template(
        "form.html",
        title="Login",
        form=form,
        path="/login",
        btn_name="Enter"
    )

@app.route("/logout", methods=["GET"])
def logout():

    if USER_KEY in session:
        del session[USER_KEY]
        flash("You are now logged out.", "success")
        return redirect("/home")
    else:
        flash("You must log in to do this.", "danger")
        return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        lang_pref = form.lang_pref.data

        User.register(username, password, lang_pref)
        flash("Successfully created account. Please log in with your credentials.", "success")

        return redirect("/login")

    else:
        return render_template(
            "form.html",
            title="Register",
            form=form,
            path="/register",
            btn_name="Create"
        )

@app.route("/users", methods=["GET"])
def list_users():
    """Return JSON data of all users"""

    users = User.query.all()

    return {jsonify(user.serialize()) for user in users}

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    """Return JSON data of user"""

    user = User.query.get_or_404(id)

    return jsonify(user.serialize())

# ------------------------------------------------------------- #
# ------------------ Drink Resource Routes -------------------- #
# ------------------------------------------------------------- #

@app.route("/drinks", methods=["GET", "POST"])
def list_drinks():

    drinks = Drink.query.all()
    form = SearchForm()
    form.ingredient.choices.extend(ingredients)
    form.category.choices.extend(categories)

    if request.method == "POST":

        form_data = {field["name"]: field["value"] for field in request.json}

        alcoholic = form_data.get("alcoholic", False)
        name = form_data["name"] if form_data["name"] != '' else False
        category_id = form_data["category"] if int(form_data["category"]) is not 0 else False
        ingredient_id = form_data["ingredient"] if int(form_data["ingredient"]) is not 0 else False

        drinks = Drink.query
        if alcoholic:
            drinks = drinks.filter(Drink.alcoholic == True)
        else:
            drinks = drinks.filter(Drink.alcoholic == False)
        
        if name:
            print("***contains name***")
            print(name)
            drinks = drinks.filter(Drink.name.ilike(f"%{name}%"))
        
        if category_id:
            print("***contains category***")
            print(category_id)
            drinks = drinks.filter(Drink.category_id == category_id)
        
        if ingredient_id:
            print("***contains ingredient***")
            print(ingredient_id)
            drink_ids = [pair.drink_id for pair in DrinkIngredient.query.filter_by(ingredient_id=ingredient_id).all()]
            drinks = drinks.filter(Drink.id.in_(drink_ids))

        drinks = drinks.all()

        return jsonify([drink.serialize() for drink in drinks])
        

    return render_template("drinks.html", title="Drinks", drinks=drinks, form=form)

@app.route("/drinks/<int:id>", methods=["GET"])
def get_drink(id):

    drink = Drink.query.get_or_404(id)

    return render_template("drink.html", title=drink.name.title(), drink=drink)

@app.errorhandler(HTTPException)
def handle_exception(e):

    if isinstance(e, HTTPException):
        return render_template("error.html", error=e, title="Something went wrong.")
    else:
        return render_template("error.html", error=e, title="Something went wrong."), 500