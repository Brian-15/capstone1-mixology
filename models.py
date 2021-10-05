"""Database SQLAlchemy Models"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref


db = SQLAlchemy()
bcrypt = Bcrypt()

def submit_data(model):
    """Add and commit model to database"""

    db.session.add(model)
    db.session.commit()

def connect_db(app):
    """Connect to database"""
    
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    username = db.Column(
        db.String(30),
        unique=True,
        nullable=False)

    password = db.Column(
        db.Text,
        nullable=False
    )

    language_pref_id = db.Column(
        db.Integer,
        db.ForeignKey("languages.id"),
        nullable=False
    )

    language_pref = db.relationship("Language")

    bookmarks = db.relationship(
        "Drink",
        secondary="bookmarks"
    )

    def __repr__(self):
        """Return data representation of User class."""
        
        return f"<User {self.id}>"
    
    @classmethod
    def register(cls, username, pwd, lang_pref_id):
        """Register new user account"""

        username = username
        hashed = bcrypt.generate_password_hash(pwd, rounds=14)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(username=username, password=hashed_utf8, language_pref_id=lang_pref_id)
        submit_data(user)

        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Authenticate user.
        
        Returns user instance if password matches.
        Returns False if no user is found or if password hashes do not match"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

    @classmethod
    def check_username(cls, username) -> bool:
        """Checks whether username is present in database."""

        return cls.query.filter_by(username=username).one_or_none() if True else False
    
    def serialize(self):
        """Returns dict object of User model"""

        return {
            "id": self.id,
            "username": self.username,
            "language_pref": self.language_pref.code
        }
    
    def has_bookmark(self, drink_id):
        """Finds relevant bookmark for user object by drink id.
        Returns bookmark object if found, else None."""

        return Bookmark.query.filter_by(drink_id=drink_id, user_id=self.id).one_or_none()            

class Language(db.Model):
    """Model class for languages"""

    __tablename__ = "languages"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    
    code = db.Column(
        db.String(10),
        unique=True,
        nullable=False)
    
    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    def __repr__(self):
        """Return instance string representation"""

        return f"<Language {self.id} {self.code}>"
    
    @classmethod
    def get_id(cls, code):
        """Get id of language code based on array index."""

        return ["", "DE", "ES", "FR", "IT", "ZH-HANS", "ZH-HANT"].index(code) + 1

class Category(db.Model):
    """Model class for drink categories"""

    __tablename__ = "categories"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    
    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    def __repr__(self):
        """Return instance string representation"""

        return f"<Category {self.id} {self.name}>"

class Glass(db.Model):
    """Model class for glass types"""

    __tablename__ = "glasses"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    
    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    def __repr__(self):
        """Return instance string represenation"""

        return f"<Glass {self.id} {self.name}>"
    
class Instruction(db.Model):
    """Model class for drink recipe instructions"""

    __tablename__ = "instructions"

    drink_id = db.Column(
        db.Integer,
        db.ForeignKey("drinks.id"),
        primary_key=True
    )

    language_id = db.Column(
        db.Integer,
        db.ForeignKey("languages.id"),
        primary_key=True
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    language = db.relationship("Language")

    def __repr__(self):
        """Return instance string representation"""

        return f"<Instruction drink({self.drink_id}) lang({self.language.code})>"


class Ingredient(db.Model):
    """Model class for recipe ingredient"""

    __tablename__ = "ingredients"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    
    name = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    def __repr__(self):
        """Return instance string representation"""

        return f"<Ingredient {self.id} {self.name}>"
    
    @classmethod
    def get_ids(cls, ingredient_names):
        """Takes list of ingredient names and returns their ids"""

        ids = []

        for name in ingredient_names:
            ingredient = cls.query.filter_by(name=name).one_or_none()

            if ingredient:
                ids.append(ingredient.id)
            else:
                cls.create(name)
                ids.append(cls.query.filter_by(name=name).one().id)
                

        return ids
        # return [cls.query.filter_by(name=name).one().id for name in ingredient_names]
    
    @classmethod
    def create(cls, name):
        """Create new ingredient model and commit to database"""

        ingr = cls(name=name)
        submit_data(ingr)

class DrinkIngredient(db.Model):
    """Model class for drink recipe to ingredient associations"""

    __tablename__ = "drinks_ingredients"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    drink_id = db.Column(
        db.Integer,
        db.ForeignKey("drinks.id", ondelete="cascade"),
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey("ingredients.id", ondelete="cascade")
    )

    quantity = db.Column(
        db.Text
    )

    ingredient = db.relationship("Ingredient")

    def __repr__(self):
        """Return instance string representation"""

        return f"<DrinkIngredient drink:{self.drink_id} ingredient:{self.ingredient_id}>"
    

    
    @classmethod
    def generate_models(cls, drink_id, ingredient_ids, quantities):
        """Returns list of DrinkIngredient model instances
        which associate drink_id with ingredient_ids"""

        return [DrinkIngredient(
            drink_id=drink_id,
            ingredient_id=ingredient_ids[i],
            quantity=quantities[i]
        ) for i in range(len(ingredient_ids))]
    
class Drink(db.Model):
    """Model class for drinks"""

    __tablename__ = "drinks"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    image_url = db.Column(db.Text)

    image_attribution = db.Column(db.Text)

    video_url = db.Column(db.Text)

    alcoholic = db.Column(
        db.Boolean,
        nullable=False
    )

    optional_alc = db.Column(
        db.Boolean,
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    glass_id = db.Column(
        db.Integer,
        db.ForeignKey("glasses.id"),
        nullable=False
    )

    instructions = db.relationship(
        "Instruction",
        backref="drink"
    )

    ingredients = db.relationship(
        "DrinkIngredient",
        primaryjoin=(DrinkIngredient.drink_id == id)
    )

    category = db.relationship("Category")

    glass = db.relationship("Glass")

    def __repr__(self):
        """Returns string representation of instance"""

        return f"<Drink {self.name}>"

    def serialize(self):
        """Returns dict object containing drink data"""

        return {
            "id": self.id,
            "name": self.name.title(),
            "image_url": self.image_url,
            "image_attribution": self.image_attribution,
            "alcoholic": self.alcoholic,
            "optional_alc": self.optional_alc,
            "category": self.category.name.title(),
            "category_id": self.category_id
        }
    
    def get_video_url_id(self):
        """Returns last section of video URL.
        This is formatted for YouTube URL links, where the video id is located at the end of the URL."""

        return self.video_url.split("/")[-1]
    
    @classmethod
    def parse_drink_data(cls, data):
        """Parses JSON data from thecocktaildb API
        Returns appropriate Drink, Instruction,
        and DrinkIngredient models into an array
        """

        category_id = Category.query.filter_by(name=data["strCategory"].lower()).one().id
        glass_id = Glass.query.filter_by(name=data["strGlass"].lower()).one().id

        [instr_data, ingr_data, quant_data] = [[], [], []]

        for key, val in data.items():
            
            if "Measure" in key: quant_data.append(val)

            if val is not None and val != "":
                if "Ingredient" in key: ingr_data.append(val.lower())
                if "Instructions" in key:
                    instr_data.append((key[15:], val))

        instructions = [
            Instruction(
                drink_id=data["idDrink"],
                language_id=Language.get_id(lang_code),
                text=text
            ) for (lang_code, text) in instr_data]

        drink_ingredients = DrinkIngredient.generate_models(
            data["idDrink"],
            Ingredient.get_ids(ingr_data),
            quant_data
        )

        return [
            cls(
                id=data["idDrink"],
                alcoholic=(True if data["strAlcoholic"].lower() == "alcoholic" else False),
                optional_alc=(True if data["strAlcoholic"].lower() == "optional alcohol" else False),
                category_id=category_id,
                name=data["strDrink"].lower(),
                image_url=data["strDrinkThumb"] if data["strDrinkThumb"] else data["strImageSource"],
                image_attribution=data["strImageAttribution"],
                glass_id=glass_id,
                video_url=data["strVideo"]
            ),
            instructions,
            drink_ingredients
        ]

class Bookmark(db.Model):
    """Model class for user bookmarks"""

    __tablename__ = "bookmarks"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        primary_key=True
    )

    drink_id = db.Column(
        db.Integer,
        db.ForeignKey("drinks.id", ondelete="cascade"),
        primary_key=True
    )

    def __repr__(self):
        """Returns string representation of instance"""

        return f"<Bookmark user:{self.user_id} drink:{self.drink_id}>"