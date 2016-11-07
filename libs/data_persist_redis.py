import datetime
import json
from time import sleep

import arrow
import pandas as pd
import redis
import tushare as ts
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

r = redis.StrictRedis(host='192.168.1.150', port=6379, db=0)

stocks = ['600000']


def dataframe_convert_type(df):
    # cast type
    df[['a1_p', 'a1_v', 'a2_p', 'a2_v', 'a3_p', 'a3_v', 'a4_p', 'a4_v', 'a5_p', 'a5_v', 'amount', 'ask', 'b1_p', 'b1_v',
        'b2_p', 'b2_v', 'b3_p', 'b4_p', 'b4_v', 'b5_p', 'b5_v', 'bid', 'high', 'low', 'open', 'pre_close', 'price',
        'volume']] = df[
        ['a1_p', 'a1_v', 'a2_p', 'a2_v', 'a3_p', 'a3_v', 'a4_p', 'a4_v', 'a5_p', 'a5_v', 'amount', 'ask', 'b1_p',
         'b1_v', 'b2_p', 'b2_v', 'b3_p', 'b4_p', 'b4_v', 'b5_p', 'b5_v', 'bid', 'high', 'low', 'open', 'pre_close',
         'price', 'volume']].apply(pd.to_numeric)

    df[['date', 'time']] = df[['date', 'time']].apply(pd.to_datetime)
    return df


def persist_to_redis(stock):
    df = ts.get_realtime_quotes(stock)
    dict_data = df.to_dict(orient='records')[0]
    json_data = json.dumps(dict_data)
    r.rpush(stock, json_data)
    logging.debug("insert data {}".format(dict_data['time']))


def retrieve_from_redis(stock):
    datas = r.lrange(stock, 0, -1)
    d = []
    for data in datas:
        d.append(json.loads(data.decode(encoding='UTF-8')))
    # pprint(d)
    df = pd.DataFrame.from_dict(d)
    df = dataframe_convert_type(df)
    return df


if __name__ == '__main__':
    while True:
        now = arrow.now('Asia/Shanghai').time()
        morning_open_market_time = datetime.time(9, 30)
        morning_close_market_time = datetime.time(11, 30)

        afternoon_open_market_time = datetime.time(13, 0)
        afternoon_close_market_time = datetime.time(15, 0)

        if morning_open_market_time < now < morning_close_market_time \
                or afternoon_open_market_time < now < afternoon_close_market_time:
            for stock in stocks:
                persist_to_redis(stock)
                sleep(60 / len(stocks))
        else:
            sleep(60)

    # df = retrieve_from_redis('600000')
