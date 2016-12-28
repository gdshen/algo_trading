import json
import logging

import redis
from flask import Flask, render_template, request
from flask import jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

from libs.policy.NDayMean import NDayMean
from libs.policy.TWAP import TWAP
from libs.policy.VWAP import VWAP
from datetime import date

from config import REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB

# logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

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


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        data = request.get_json()
        print(data)

        wap = None
        if data['method'] == 'twap':
            wap = TWAP(data['security'], data['day'])
        elif data['method'] == 'vwap':
            wap = NDayMean(data['security'], data['day'])
        elif data['method'] == 'vwap_with_predict':
            wap = VWAP(data['security'], data['day'])

        user_id = current_user.get_id()
        wap.save(user_id, data['operation'], data['shares'], convert_time(data['timeIntervals']))
        return 'success'


@app.route('/predict', methods=['GET'])
@login_required
def predict():
    return render_template('predict.html')


@app.route('/table', methods=['GET'])
@login_required
def table():
    user_id = current_user.get_id()
    policies = read_from_redis(user_id)

    d = {"data": convert(policies=policies)}
    return jsonify(**d)


@app.route('/trend', methods=['GET'])
@login_required
def trend():
    return render_template('trend.html')


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
        wap = policy['wap']
        for strategy in policy['policy']:
            data.append({'stock': stock, 'type': operation_type, 'wap': wap, 'volume': strategy[1][1],
                         'time': policy['day'] + ' ' + strategy[1][0]})
    return data


def convert_time(time_intervals):
    l = list()
    for time_interval in time_intervals:
        start = time_interval['start_time']
        start_time = start['HH'] + ':' + start['mm'] + ':00'
        end = time_interval['end_time']
        end_time = end['HH'] + ':' + end['mm'] + ':00'
        l.append((start_time, end_time))
    return l
