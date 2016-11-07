from flask_mongoengine.wtf import model_form
from flask_mongoengine.wtf.orm import validators
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import RadioField
from wtforms import StringField

import models

user_form = model_form(models.User, exclude=['password'])


class SignupForm(user_form):
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class LoginForm(user_form):
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember = BooleanField("Remember Me")


class OperationForm(FlaskForm):
    security = StringField("security")
    shares = StringField("shares")
    operation = RadioField("operation", choices=[('value', 'buy'), ('value', 'sell')])
    methods = RadioField("methods", choices=[('value', 'twap'), ('value_two', 'vwap')])
