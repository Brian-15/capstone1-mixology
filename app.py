

import os
from flask import Flask, request, redirect, jsonify, flash, session, g
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
import flask_debugtoolbar
from models import Drink, db, connect_db, User
from forms import LoginForm, RegisterForm

USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql:///mixology")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

app.config["SECRET_KEY"] = "s3cr1t059"

debug = DebugToolbarExtension(app)


# ------------------------------------------------------------- #
# User Routes
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

    return {jsonify_model(user) for user in users}

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    """Return JSON data of user"""

    user = User.query.get_or_404(id)

    return jsonify_model(user)

# ------------------------------------------------------------- #
# Drink Resource Routes
# ------------------------------------------------------------- #

@app.route("/drinks", methods=["GET"])
def list_drinks():

    drinks = Drink.query.all()

    return {jsonify(drink.serialize()) for drink in drinks}

@app.route("/drinks/<int:id>", methods=["GET"])
def get_drink(id):

    drink = Drink.query.get_or_404(id)

    print(jsonify(drink.serialize()))

    return {jsonify(drink.serialize())}
