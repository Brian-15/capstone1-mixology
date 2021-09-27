

import os
from flask import Flask, request, redirect
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
import flask_debugtoolbar
from models import db, connect_db, User
from forms import LoginForm, RegisterForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()


app.config["SECRET_KEY"] = "s3cr1t059"

debug = DebugToolbarExtension(app)

# ------------------------------------------------------------- #
# User Routes
# ------------------------------------------------------------- #


@app.route("/")
def root():

    return redirect("/home")

@app.route("/home")
def home():

    return render_template("home.html",
                           title="Home")

app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

    else:
        return render_template("login.html",
                               title="Login",
                               form=form,
                               path="/login",
                               btn_name="Enter")

app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        User.register(username, password)

        return redirect("/")

    else:
        return render_template("register.html",
                               title="Register",
                               form=form,
                               path="/register",
                               btn_name="Create")

# ------------------------------------------------------------- #
# Drink Resource Routes
# ------------------------------------------------------------- #

@app.route("/drinks", methods=["GET"])
def list_drinks():

    return render_template()