from flask import Flask, redirect
from flask_login import LoginManager, login_user, logout_user
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
def index():
    return 'hello, world'


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass
    # user = User()
    # user.email = 'gdshen95@gmail.com'


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
    if user.is_active():
        return user
    else:
        return None
