# monitor python process and restart it

import logging
from datetime import datetime

import arrow
import pandas as pd
import tushare as ts
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

from config import MONGODB_URL, MARKET_MORNING_OPEN, MARKET_MORNING_CLOSE, MARKET_AFTERNOON_OPEN, MARKET_AFTERNOON_CLOSE
from cons import stocks_list

logging.basicConfig(filename='database.log', format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
stocks = list(stocks_list.keys())


def is_holiday(date):
    """ The tushare.is_holiday has bug, so I rewrite it here.

    :param date: string -> format 'YYYY-MM-DD"
    :return: whether the date is holiday: bool -> True/False
    """

    df = pd.read_csv('./calAll.csv')
    holiday = df[df.isOpen == 0]['calendarDate'].values
    today = datetime.strptime(date, "%Y-%m-%d")

    if today.isoweekday() in [6, 7] or '{dt.year}/{dt.month}/{dt.day}'.format(dt=today) in holiday:
        return True
    else:
        return False


def get_and_persist_data(stock, date):
    """ get stock tick data and persist to mongodb

    :param stock: string -> a stock id, like '600000'
    :param date: string -> format 'YYYY-MM-DD'
    :return: status of execution: bool -> True/False
    """

    client = MongoClient(MONGODB_URL)
    if is_holiday(date):
        logging.debug('{} is holiday'.format(date))
        return False

    df = ts.get_tick_data(stock, date, retry_count=5)
    db = client[stock]

    # consider stock suspension
    if df.iloc[0, 0] != 'alert("当天没有数据");':
        df['time'] = date + df['time']
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d%H:%M:%S')
        df = df.sort_index(axis=0, ascending=False)
        try:
            db[date].insert_many(df.to_dict(orient='records'))
            logging.debug('{} {} saved'.format(stock, date))
            return True
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            logging.error('{} {} save error'.format(stock, date))
            return False
    else:
        logging.debug('{} {} no data, stock is in suspension.'.format(stock, date))
        return False


def read_from_db(stock, day, morning_start=None, morning_end=None, afternoon_start=None, afternoon_end=None):
    """read stock history data from database and return a pandas dataframe


    关于使用时间段的说明：
        1. 默认不传时间段参数的情况下：将获取全天的所有数据
        2. 两个时间段（四个时间点）都指定：获取对应两个时间段的数据
        3. 只使用一个时间段：需要给另外的一个时间段的两个时间点传递字符串参数”NOT_USE"
        4. 其他情况下：如果不指定某个时间参数，则该时间参数取值为对应的开市和闭式值。

    :param stock: string -> a stock id, like "600000"
    :param day: string -> which day, format 'YYYY-MM-DD", like "2016-01-03"
    :param morning_start: string -> the start of time interval of the morning, format "HH:MM", like "10:30"
    :param morning_end: string -> the end of time interval of the morning, format "HH:MM", like "11:00"
    :param afternoon_start: string -> format "HH:MM"
    :param afternoon_end: string -> format "HH:MM"
    :return: pandas.Dataframe: the data in Dataframe type, if the day is not trade day for that stock, return None
    """

    client = MongoClient(MONGODB_URL)
    db = client[stock]

    trade_days = db.collection_names()
    if not (day in trade_days):
        return None
    collection = db[day]

    # to simplify the none time interval selection
    if morning_start is None and morning_end is None and afternoon_start is None and afternoon_end is None:
        data = list(collection.find())
        return pd.DataFrame.from_dict(data)

    # below is the set time interval version

    # handle the not use case
    if morning_start == "NOT_USE" or morning_end == "NOT_USE":
        morning_start, morning_end = "00:00", "00:00"
    if afternoon_start == "NOT_USE" or morning_end == "NOT_USE":
        afternoon_start, morning_end = "23:59", "23:59"

    # parse time to proper type
    datetime_format = '%Y-%m-%d%H:%M'
    if morning_start is None:
        morning_start = datetime.strptime(day + MARKET_MORNING_OPEN, datetime_format)
    else:
        morning_start = datetime.strptime(day + morning_start, datetime_format)

    if morning_end is None:
        morning_end = datetime.strptime(day + MARKET_MORNING_CLOSE, datetime_format)
    else:
        morning_end = datetime.strptime(day + morning_end, datetime_format)

    if afternoon_start is None:
        afternoon_start = datetime.strptime(day + MARKET_AFTERNOON_OPEN, datetime_format)
    else:
        afternoon_start = datetime.strptime(day + afternoon_start, datetime_format)

    if afternoon_end is None:
        afternoon_end = datetime.strptime(day + MARKET_AFTERNOON_CLOSE, datetime_format)
    else:
        afternoon_end = datetime.strptime(day + afternoon_end, datetime_format)

    data = list(collection.find(
        {
            # "$or: [{x: {$lte: 10}}, {x: {$gte: 20, $lte: 25}}, {x: {$gte: 30}}],

            "$or": [
                {"time": {"$gte": morning_start, "$lte": morning_end}},
                {"time": {"$gte": afternoon_start, "$lte": afternoon_end}}
            ]
        }
    ))
    return pd.DataFrame.from_dict(data)


if __name__ == '__main__':
    # read_from_db('600000', '2016-12-21')

    presents = arrow.now()
    a_year_before = arrow.now().replace(years=-1)
    #
    for stock in stocks:
        for r in arrow.Arrow.range('day', a_year_before, presents):
            date = r.format('YYYY-MM-DD')
            #     read_from_db('600000', date)
            #     read_from_db('600000', date, 'NOT_USE', 'NOT_USE', '13:30', "14:30")
            get_and_persist_data(stock, date)
            # sleep(1)
            #
            # get_and_persist_data('601398', '2016-08-15')

            # get_and_persist_data('601766', '2016-03-04')
# print(ts.get_tick_data('600000', '2016-10-31'))
# df = ts.get_tick_data('600')
