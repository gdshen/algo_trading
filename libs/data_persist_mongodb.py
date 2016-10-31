# monitor python process and restart it

import json
import logging

import arrow
import tushare as ts
from pymongo import MongoClient

stocks = ['600000']

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.stocks

    presents = arrow.now()
    a_year_before = arrow.now().replace(years=-1)

    for stock in stocks:
        for r in arrow.Arrow.range('day', a_year_before, presents):
            date = r.format('YYYY-MM-DD')
            df = ts.get_tick_data(stock, date)
            if df.iloc[0, 0] != 'alert("当天没有数据");':
                # df.to_csv('../data/600000/600000_{}.csv'.format(date))
                df['date'] = date
                db[stock].insert(json.loads(df.to_json()))
                logging.debug('{} {} saved'.format(stock, date))
            else:
                logging.debug('{} {] no data'.format(stock, date))

# print(ts.get_tick_data('600000', '2016-10-31'))
# df = ts.get_tick_data('600')
