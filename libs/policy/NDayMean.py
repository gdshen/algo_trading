from pprint import pprint
from datetime import timedelta

import arrow
import numpy as np

from libs.data_persist_mongodb import read_from_db
from libs.back_test import BackTest


class NDayMean:
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
        bt.plot()


if __name__ == '__main__':
    seven_day_mean = NDayMean('600000', '2016-12-21', 1000, 7)
    # l = seven_day_mean.time_interval_mean('09:30', '09:31')
    # print(l)
    # l = seven_day_mean.time_slice('09:30', '09:40', 10)
    # pprint(l)
    # l = seven_day_mean.vwap('09:30', '10:30')
    # pprint(l)
    # seven_day_mean.score('09:30', '11:30')
    l = seven_day_mean.time_slice([('09:30:00', '10:30:00'), ('13:00:00', "13:40:00")], 8)
    # pprint(l)
    l = seven_day_mean.vwap([('09:30:00', '10:30:00'), ('13:00:00', "13:40:00")])
    pprint(l)
    l = seven_day_mean.score([('09:30:00', '10:30:00'), ('13:00:00', "13:40:00")])

    # df = seven_day_mean.score('09:30', '10:30')
    # pprint(df)

    # df = read_from_db('600000', '2016-12-22')
    # print(df['2016-12-22 09:30:00' : '2016-12-22 09:40:00'])
