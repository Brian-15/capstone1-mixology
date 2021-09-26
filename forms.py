from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Optional, EqualTo

class LoginForm(FlaskForm):

    username = StringField("Username",
                           validators = [InputRequired()])

    password = PasswordField("Password",
                             validators = [InputRequired()])

    
class RegisterForm(LoginForm):

    confirm_password = PasswordField("Confirm Password",
                                     validators = [
                                         InputRequired(),
                                         EqualTo("password")
                                     ])