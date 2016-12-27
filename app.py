import json
import logging

import redis
from flask import Flask, render_template, request
from flask import jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

from config import REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB

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
# toolbar = DebugToolbarExtension(app)


# @app.route('/post', methods=['POST'])
# @login_required
# def hello():
#     if request.method == 'POST':
##         a = request.form['hello']
# a = request.get_json()
#
# return a['hello'] + 'receive'
# else:
#     return "NoData"


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        data = request.get_json()
        print(data)
        return 'success'


@app.route('/predict', methods=['GET'])
@login_required
def predict():
    return render_template('predict.html')

    # @app.route('/history', methods=['GET'])
    # def history():
    d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    # return render_template('history.html')


@app.route('/table', methods=['GET'])
@login_required
def table():
    user_id = current_user.get_id()
    # print(user_id)

    policies = read_from_redis(user_id)

    # current_user
    d = {"data": convert(policies=policies)}
    return jsonify(**d)


def read_from_redis(user_id):
    r = redis.StrictRedis(REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB)
    values = r.lrange(user_id, 0, -1)
    policies = list()
    for value in values:
        policies.append(json.loads(value.decode(encoding='UTF-8')))
    return policies


def convert(policies):
    data = list()
    for policy in policies:
        stock = policy['stock']
        operation_type = policy['order_type']
        for strategy in policy['policy']:
            data.append({'stock': stock, 'type': operation_type, 'volume': strategy[1][1], 'time': strategy[1][0]})
    return data
