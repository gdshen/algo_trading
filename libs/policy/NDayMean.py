from pprint import pprint
from datetime import timedelta

import arrow
import numpy as np

from libs.data_persist_mongodb import read_from_db
from libs.back_test import BackTest
from libs.policy.WAP import WAP


class NDayMean(WAP):
    def __init__(self, stock, date, n_days=7, n_slice=10):
        self.stock = stock
        self.date = date
        self.n_days = n_days
        self.n_slice = n_slice
        self.data = self.load_data()

    def load_data(self):
        l = list()
        i = 0
        date = arrow.get(self.date)
        while i < self.n_days:
            df = read_from_db(stock=self.stock, day=date.format('YYYY-MM-DD'))
            date = date.replace(days=-1)
            if not (df is None):
                i += 1
                l.append(df)
        return l

    def time_interval_mean(self, start_time: str, end_time: str) -> float:
        """ compute the mean order amount of the interval time in the previous n days

        :param start_time: format 'HH:mm:ss'
        :param end_time: format 'HH:MM:ss'
        :return:
        """
        time_interval_amount = list()
        for i in range(self.n_days):
            day = arrow.get(self.data[i].iloc[0, 4]).date().strftime('%Y-%m-%d')

            start = arrow.get(day + ' ' + start_time).datetime
            end = arrow.get(day + ' ' + end_time).datetime
            time_interval = self.data[i][start: end]

            time_interval_amount.append(time_interval['volume'].sum())
        return float(np.mean(time_interval_amount))



    def vwap(self, order_amount, time_intervals):
        time_list = self.time_slice(time_intervals, self.n_slice)
        l = list()
        order_number = dict()
        total_order_number = 0
        for (start, end, _) in time_list:
            order_number[(start, end)] = self.time_interval_mean(start, end)
            total_order_number += order_number[(start, end)]

        for (start, end, random_time) in time_list:
            l.append(((start, end),
                      (random_time, round(order_amount * order_number[(start, end)] / total_order_number))))
        return l

    def score(self, order_amount, time_intervals):
        policy = {
            'stock': self.stock,
            'day': self.date,
            'wap': 'vwap',
            'policy': list()
        }
        l = self.vwap(order_amount, time_intervals)
        policy['policy'] = l
        bt = BackTest(policy)
        result = bt.backtest()
        pprint(result)
        return bt.diff()


if __name__ == '__main__':
    seven_day_mean = NDayMean('600000', '2016-12-21')
    l = seven_day_mean.time_slice([('09:30:00', '10:30:00'), ('13:00:00', "13:40:00")], 8)
    l = seven_day_mean.vwap(1000, [('09:30:00', '10:30:00'), ('13:00:00', "13:40:00")])
    pprint(l)
    print(seven_day_mean.score(1000, [('09:30:00', '10:30:00'), ('13:00:00', "13:40:00")]))

