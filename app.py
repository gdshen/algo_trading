from flask import Flask, redirect, request, flash, render_template
from flask_login import LoginManager, login_user, logout_user, login_required

from forms import SimpleForm
from user import User
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension

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
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SimpleForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_obj = User()
        user_obj.get_by_email(email, password_acquirement=True)
        if email == user_obj.email and password == user_obj.password:
            login_user(user_obj)
            # flash("Logged in!")
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SimpleForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_obj = User()
        user_obj.email = email
        user_obj.password = password
        user_obj.save()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


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
