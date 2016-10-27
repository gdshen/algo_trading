import models
from flask_mongoengine.wtf import model_form
from wtforms.fields import *
from flask_mongoengine.wtf.orm import validators

user_form = model_form(models.User, exclude=['password'])


# Signup Form created from user_form
class SignupForm(user_form):
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class LoginForm(user_form):
        password = PasswordField('Password', validators = [validators.DataRequired()])
