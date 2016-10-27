from flask import Flask, redirect
from flask_login import LoginManager
from user import User
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_bcrypt import Bcrypt

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'this_is_a_secret_key'
app.debug = True


db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

flask_bcrypt = Bcrypt(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hello, world'


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass
    # user = User()
    # user.email = 'gdshen95@gmail.com'


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
