import json
from datetime import timedelta
from pprint import pprint

import arrow
import numpy as np
import redis

from config import REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB
from libs.back_test import BackTest


class WAP:
    def __init__(self, stock, date, n_days=7, n_slice=10):
        self.stock = stock
        self.date = date
        self.n_days = n_days
        self.n_slice = n_slice
        self.strategy = None

    def load_data(self):
        pass

    @staticmethod
    def time_slice(time_intervals, n=10):
        """ slice the time_intervals to n slice

        :param time_intervals: [(start_time, end_time), (start_time, end_time), ...]
        :param n:
        :return:
        """
        time_format = 'HH:mm:ss'
        total_time = timedelta(0)
        for (start_time, end_time) in time_intervals:
            start = arrow.get(start_time, time_format)
            end = arrow.get(end_time, time_format)
            total_time += end - start
        delta_t = total_time / n

        l = list()
        for (start_time, end_time) in time_intervals:
            start = arrow.get(start_time, time_format)
            end = arrow.get(end_time, time_format)
            t = start
            while t < end:
                if t + delta_t <= end:
                    l.append((t.format(time_format), (t + delta_t).format(time_format),
                              (t + delta_t * np.random.random()).format(time_format)))
                else:
                    l.append((t.format(time_format), end.format(time_format),
                              (t + (end - t) * np.random.random()).format(time_format)))
                t += delta_t
        return l

    def wap(self, order_amount, time_intervals):
        pass

    def score(self, order_amount, time_intervals):
        policy = {
            'stock': self.stock,
            'day': self.date,
            'wap': self.strategy,
            'policy': list()
        }
        l = self.wap(order_amount, time_intervals)
        policy['policy'] = l
        bt = BackTest(policy)
        result = bt.backtest()
        pprint(result)
        return bt.diff()

    def save(self, user_id, order_type, order_amount, time_intervals):
        policy = {
            'order_type': order_type,
            'stock': self.stock,
            'day': self.date,
            'wap': self.strategy,
            'policy': list()
        }
        l = self.wap(order_amount, time_intervals)
        policy['policy'] = l

        r = redis.StrictRedis(host=REDIS_SERVER_HOST, port=REDIS_SERVER_PORT, db=REDIS_SERVER_DB)
        r.rpush(user_id, json.dumps(policy))
