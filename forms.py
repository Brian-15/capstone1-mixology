from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, RadioField
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired, EqualTo, Optional

class LoginForm(FlaskForm):
    """User login form."""

    username = StringField("Username",
                           validators = [InputRequired()])

    password = PasswordField("Password",
                             validators = [InputRequired()])

    
class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField("Username",
                           validators = [InputRequired()])

    password = PasswordField("Password",
                             validators = [InputRequired()])

    confirm_password = PasswordField(
        "Confirm Password",
        validators = [
            InputRequired(),
            EqualTo("password")
        ]
    )
    
    lang_pref = SelectField(
        "Language Preference",
        choices=[
            (1, "English"),
            (2, "German"),
            (3, "Spanish"),
            (4, "French"),
            (5, "Italian"),
            (6, "Mandarin, Simplified"),
            (7, "Mandarin, Traditional")
        ],
        validators = [InputRequired()]
    )

class SearchForm(FlaskForm):
    """Search form that queries database for drinks with any or several of the below filters"""

    name = StringField(
        "Search By Name",
        validators=[Optional()]
    )

    category = SelectField(
        "Filter By Category",
        choices=[(0, "-")],
        validators=[InputRequired()]
    )

    ingredient = SelectField(
        "Filter By Ingredient",
        choices=[(0, "-")],
        validators=[InputRequired()]
    )

    def is_empty(self):
        """Returns True if fields are empty"""

        if self.name.data is not None:
            return False
        
        if self.category.data is not None:
            return False
        
        if self.ingredient.data is not None:
            return False
        
        return True