from flask_mongoengine.wtf import model_form
from flask_mongoengine.wtf.orm import validators
from wtforms import PasswordField

import models

user_form = model_form(models.User, exclude=['password'])


class SignupForm(user_form):
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class LoginForm(user_form):
    password = PasswordField('Password', validators=[validators.DataRequired()])
