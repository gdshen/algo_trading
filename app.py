import os
from flask import Flask, render_template, request, redirect
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
from flask_bcrypt import Bcrypt  # for password hashing

# create and named flask app
app = Flask('trade_demo')

# app.config['MONGODB_SETTINGS'] = {'HOST': os.environ.get('MONGOLAB_URI'), 'DB':'FlaskLogin'}
app.config['SECRET_KEY'] = 'this_is_a_secret_key'  # os.environ.get('SECRET_KEY')
app.debug = True  # os.environ.get('DEBUG', False)

db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)  # modify flask default session system (werkzeug

# flask bcrypt will be used to salt the user password
flask_bcrypt = Bcrypt(app)

# associate flask-login manager with current app
login_manager = LoginManager()
login_manager.init_app(app)


