import logging

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_required, current_user
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.config.from_pyfile('config.py')

# flask_login configuration
login_manager = LoginManager()
login_manager.init_app(app)

# flask_mongoengine  configuration
db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

# flask_bcrypt configuration
flask_bcrypt = Bcrypt(app)

# flask_debugtoolbar configuration
toolbar = DebugToolbarExtension(app)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', email=current_user.email)



