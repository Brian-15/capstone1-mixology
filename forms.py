from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, RadioField
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired, EqualTo, Optional

class LoginForm(FlaskForm):

    username = StringField("Username",
                           validators = [InputRequired()])

    password = PasswordField("Password",
                             validators = [InputRequired()])

    
class RegisterForm(LoginForm):

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

    alcoholic = BooleanField(
        "Contains Alcohol?",
        default=True,
        validators=[Optional()]
    )