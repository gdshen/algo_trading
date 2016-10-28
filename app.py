from flask import Flask, redirect, request, flash, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from forms import SignupForm, LoginForm
from user import User
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)

db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

flask_bcrypt = Bcrypt(app)

toolbar = DebugToolbarExtension(app)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', email=current_user.email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        # flash("You have login, return to homepage!")
        return redirect('/')
    form = LoginForm(request.form)
    if request.method == 'POST':
        user_obj = User()
        email = form.email.data
        password = form.password.data
        user_obj.get_by_email(email, password_acquirement=True)
        if flask_bcrypt.check_password_hash(user_obj.password, password):
            login_user(user_obj)
            flash("Logged in!")
        else:
            logging.debug('login-- user {} has input wrong password'.format(email))
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user_obj = User()
            email = form.email.data
            password = flask_bcrypt.generate_password_hash(form.password.data)
            user_obj.email = email
            user_obj.password = password
            user_obj.save()
            logging.debug('Register-- {} registered'.format(email))
            return redirect('/login')
        else:
            logging.debug('Register-- validate check failed')
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


# todo: to find the comment style for python methods
# user_loader is required by flask_login extension
# input: unicode of user_id
# ouput: User class or None
@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        redirect('/login')
    user = User()
    user.get_by_id(user_id)
    if user.is_active:
        return user
    else:
        return None
