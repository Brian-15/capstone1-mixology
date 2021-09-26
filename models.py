import re
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt


db = SQLAlchemy()

def submit_data(model):
    """add and commit model to database"""

    db.session.add(model)
    db.session.commit()

def connect_db(app):
    """Connect to database"""
    
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.String(30),
                         primary_key=True,
                         unique=True)
    password = db.Column(db.String())


    def __repr__(self):
        """Return data representation of User class."""
        
        return f"<User {self.id}>"
    
    @classmethod
    def register(cls, username, pwd):
        """Register new user account"""

        username = username
        hashed = bcrypt.generate_password_hash(pwd, rounds=14)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(username=username, password=hashed_utf8)
        submit_data(user)

        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Log user in"""

        