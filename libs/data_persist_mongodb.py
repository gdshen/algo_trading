# monitor python process and restart it

import json
import logging

import arrow
import tushare as ts
import pandas as pd
from pymongo import MongoClient

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
stocks = ['600000']


def get_and_persist_data(stock, date):
    """ get stock tick data and persist to mongodb

    :param stock: string -> a stock id, like '600000'
    :param date: string -> format 'YYYY-MM-DD'
    :return: no return value
    """
    df = ts.get_tick_data(stock, date, retry_count=5)
    if df.iloc[0, 0] != 'alert("当天没有数据");':
        # df.to_csv('../data/600000/600000_{}.csv'.format(date))
        df['time'] = date + df['time']
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d%H:%M:%S')
        db[stock].insert_many(df.to_dict(orient='records'))
        logging.debug('{} {} saved'.format(stock, date))
    else:
        logging.debug('{} {} no data'.format(stock, date))


if __name__ == '__main__':
    client = MongoClient('192.168.1.150', 27017)
    db = client.stocks

    presents = arrow.now()
    a_year_before = arrow.now().replace(years=-1)

    for stock in stocks:
        for r in arrow.Arrow.range('day', a_year_before, presents):
            date = r.format('YYYY-MM-DD')
            get_and_persist_data(stock, date)

# print(ts.get_tick_data('600000', '2016-10-31'))
# df = ts.get_tick_data('600')
