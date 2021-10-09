import os, pdb
from flask import Flask, json, request, redirect, jsonify, flash, session, g
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.datastructures import ImmutableDict, MultiDict
from werkzeug.exceptions import HTTPException
from models import Bookmark, Drink, DrinkIngredient, db, connect_db, User, Category, Ingredient
from forms import LoginForm, RegisterForm, SearchForm

USER_KEY = "curr_user"

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///mixology")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL if DATABASE_URL == "postgresql:///mixology" else DATABASE_URL.replace("://", "ql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

app.config["SECRET_KEY"] = "s3cr1t059"

debug = DebugToolbarExtension(app)


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
    """Root route. Redirect to /home"""

    return redirect("/home")

@app.route("/home")
def home():
    """Render home page"""

    if "form_data" in session:
        del session["form_data"]

    return render_template("home.html",
                           title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login route"""

    if USER_KEY in session:
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
    """User logout route"""

    if USER_KEY in session:
        del session[USER_KEY]
        flash("You are now logged out.", "success")
        return redirect("/home")
    else:
        flash("You must be logged in to do this.", "danger")
        return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration route"""

    if USER_KEY in session:
        flash("You must log out to register.", "danger")
        return redirect("/home")

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

@app.route("/user", methods=["GET"])
def get_user():
    """Renders logged in user's profile"""

    if USER_KEY not in session:
        flash("You must be logged in to view this", "danger")
        return redirect("/login")
    
    user = User.query.get_or_404(session[USER_KEY])

    return jsonify(user.serialize())

@app.route("/user", methods=["POST"])
def create_user():
    """Create new user"""

    data = request.json()

    user = User.register(data["username"], data["pwd"], data["lang_pref_id"])

    return jsonify(user.serialize())

@app.route("/user", methods=["PUT", "PATCH"])
def update_user():

    if USER_KEY not in session:
        return jsonify({"STATUS": "FAIL"})
    
    user = User.query.filter_by(id=session[USER_KEY]).update(request.json())
    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize())

@app.route("/user", methods=["DELETE"])
def delete_user():
    """Delete user account"""

    if USER_KEY not in session:
        flash("You must be logged in to do this.", "danger")
        return jsonify({"STATUS": "FAIL"})
    
    User.query.filter_by(id=session[USER_KEY]).delete()
    db.session.commit()

    del session[USER_KEY]
    flash("Account successfully deleted.", "success")

    return jsonify({"STATUS": "OK"})

# ------------------------------------------------------------- #
# ------------------ Drink Resource Routes -------------------- #
# ------------------------------------------------------------- #

def filter_drinks_by(name, category_id, ingredient_id):

    drinks = Drink.query

    if name != '':
        drinks = drinks.filter(Drink.name.ilike(f"%{name}%"))
        
    if category_id != '0':
        drinks = drinks.filter(Drink.category_id == category_id)
    
    if ingredient_id != '0':
        drink_ids = [pair.drink_id for pair in DrinkIngredient.query.filter_by(ingredient_id=ingredient_id).all()]
        drinks = drinks.filter(Drink.id.in_(drink_ids))
    
    return drinks

@app.route("/clear-search", methods=["POST"])
def clear_search():
    del session["form_data"]
    return jsonify({"STATUS": "OK"})

@app.route("/drinks", methods=["GET", "POST"])
def list_drinks():
    """Resource route for listing out drinks
    
    GET: Render drinks.html template, and display all drinks.
    POST: Return JSON data with list of drinks that underwent filters from SearchForm.
    """

    page = int(request.args.get("page"))

    if session.get("form_data", False):
        form = SearchForm(MultiDict(session["form_data"]))
        g.drinks = filter_drinks_by(form.name.data, form.category.data, form.ingredient.data)
    else:
        pdb.set_trace()
        form = SearchForm()
        g.drinks = Drink.query
        
    ingredients = [(ingr.id, ingr.name.title()) for ingr in Ingredient.query.order_by(Ingredient.name).all()]
    categories = [(cat.id, cat.name.title()) for cat in Category.query.order_by(Category.name).all()]

    form.ingredient.choices.extend(ingredients)
    form.category.choices.extend(categories)

    if form.validate_on_submit():

        session["form_data"] = request.form

        g.drinks = filter_drinks_by(form.name.data, form.category.data, form.ingredient.data)

    # if form.is_empty():
    #     g.drinks = Drink.query
    #     del session["form_data"]

    return render_template("drinks.html", title="Drinks", drinks=g.drinks.paginate(page, 10), form=form)

@app.route("/drinks/<int:id>", methods=["GET"])
def get_drink(id):
    """Get drink of id, and display page with resource instance information."""

    user = USER_KEY in session

    drink = Drink.query.get_or_404(id)

    return render_template("drink.html",
                           title=drink.name.title(),
                           drink=drink,
                           user=user)

@app.route("/drinks/<int:id>/bookmark", methods = ["POST"])
def bookmark_drink(id):
    """Bookmarks drink of id for logged in user."""

    if USER_KEY not in session:
        return jsonify({"STATUS": "NO_USER_FOUND"})
    
    bookmark = Bookmark(drink_id=id, user_id=g.user.id)
    db.session.add(bookmark)
    db.session.commit()
    return jsonify({
        "STATUS": "OK",
        "CLASS": "bi bi-bookmark-fill fs-2"
    })


@app.route("/drinks/<int:id>/bookmark", methods = ["DELETE"])
def remove_bookmark(id):
    """Removes bookmark of drink for logged in user."""

    if USER_KEY not in session:
        return jsonify({"STATUS": "NO_USER_FOUND"})

    Bookmark.query.filter_by(drink_id=id, user_id=g.user.id).delete()
    db.session.commit()
    return jsonify({
        "STATUS": "OK",
        "CLASS": "bi bi-bookmark fs-2"
    })


# ------------------------------------------------------------- #
# ----------------------- Error Route ------------------------- #
# ------------------------------------------------------------- #

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Renders error page if URL not found, or if there is a server error."""

    if isinstance(e, HTTPException):
        return render_template("error.html", error=e, title="Something went wrong.")
    else:
        return render_template("error.html", error=e, title="Something went wrong."), 500