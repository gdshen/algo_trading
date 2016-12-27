import datetime
import json
import logging
import time
import random
from pprint import pprint

import redis

from config import REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB
from libs.data_persist_redis import retrieve_from_redis
from predict.predictAPI import getDayVolume


# class OrderMatch:
#     # def __init__(self):
#     #     self.policy = self.retrieve_policy_from_db()
#     #
#     # def retrieve_policy_from_db(self):


def read_from_redis():
    r = redis.StrictRedis(REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB)
    keys = r.keys()
    policys = {}
    for key in keys:
        values = r.lrange(key, 0, -1)
        policys[str(key, 'utf-8')] = list()
        for value in values:
            policys[str(key, 'utf-8')].append(json.loads(value.decode(encoding='UTF-8')))
    return policys


def order_match():
    users = read_from_redis()
    while True:
        for user in users:
            user_policys = users[user]
            for user_policy in user_policys:
                for user_policy_element in user_policy['policy']:
                    order_point = user_policy_element[1][0]
                    order_num = user_policy_element[1][1]
                    if datetime.datetime.now().strftime("%X") == order_point:
                        current_data = retrieve_from_redis(user_policy['stock']).iloc[-1]
                        if user_policy['wap'] == 'twap' or user_policy['wap'] == 'vwap':
                            if user_policy['order_type'] == 'buy':
                                if current_data['a1_v'] < order_num:
                                    logging.warning(str(user) + "在" + str(order_point) + "时刻要买入的关于" + user_policy[
                                        'stock'] + "股票的一单失败")
                                else:
                                    pass
                            else:
                                if current_data['b1_v'] < order_num:
                                    logging.warning(str(user) + "在" + str(order_point) + "时刻要卖出的关于" + user_policy[
                                        'stock'] + "股票的一单失败")
                        elif user_policy['wap'] == 'vwap_with_predict':
                            datetime_format = '%Y-%m-%d%H:%M:%S'
                            end_1min = datetime.datetime.strptime(user_policy['day'] + order_point, datetime_format)
                            start_1min = end_1min + datetime.timedelta(minutes=-1)
                            start_2min = start_1min + datetime.timedelta(minutes=-1)
                            start_3min = start_2min + datetime.timedelta(minutes=-1)

                            price_3min = current_data['price', 'volume'][
                                (current_data['time'] >= start_3min) & (current_data['time'] <= start_2min)]
                            price_2min = current_data['price', 'volume'][
                                (current_data['time'] >= start_2min) & (current_data['time'] <= start_1min)]
                            price_1min = current_data['price', 'volume'][
                                (current_data['time'] >= start_1min) & (current_data['time'] <= end_1min)]

                            input_list = [price_1min['price'].iloc[0], price_1min['price'].iloc[-1],
                                          min(price_1min['price']), max(price_1min['price']), sum(price_1min['volume']),
                                          int(price_1min['price'].iloc[-1] > price_1min['price'].iloc[0]),
                                          price_2min['price'].iloc[0], price_2min['price'].iloc[-1],
                                          min(price_2min['price']), max(price_2min['price']), sum(price_2min['volume']),
                                          int(price_2min['price'].iloc[-1] > price_2min['price'].iloc[0]),
                                          price_3min['price'].iloc[0], price_3min['price'].iloc[-1],
                                          min(price_3min['price']), max(price_3min['price']), sum(price_3min['volume']),
                                          int(price_3min['price'].iloc[-1] > price_3min['price'].iloc[0])]

                            next_min_trend = getDayVolume(input_list, user_policy['stock'])
                            if user_policy['order_type'] == 'buy':
                                if next_min_trend == 1:
                                    random_num = random.random()
                                    if random_num > 0.1:
                                        if current_data['a1_v'] < order_num:
                                            logging.warning(
                                                str(user) + "在" + str(order_point) + "时刻要买入的关于" + user_policy[
                                                    'stock'] + "股票的一单失败")
                                        else:
                                            pass
                                    else:
                                        user_policy_element[1][0] = (end_1min + datetime.timedelta(minutes=1)).strftime("%X")
                                        r = redis.StrictRedis(REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB)
                                        r.delete(user)
                                        for u in users[user]:
                                            r.rpush(user, json.dumps(u))
                                else:
                                    pass




                    else:
                        continue
        time.sleep(1)


if __name__ == '__main__':
    users = read_from_redis()
    for user in users:
        user_policys = users[user]
        for user_policy in user_policys:
            #pprint(user_policy['policy'])
            for i in user_policy['policy']:
                order_point = i[1][0]
                if i[1][1] == 194:
                    i[1][1] = 10970
                r = redis.StrictRedis(REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB)
                r.delete(user)
                for u in users[user]:
                    r.rpush(user, json.dumps(u))
                # b = [1,2,3,4,5]
                # a = datetime(2016,12,23,21,1,35)
                # for i in b:
                #     while 1:
                #         if a.strftime("%X") == datetime.now().strftime("%X"):
                #             print(i)
                #             break
                #         else:
                #             time.sleep(1)
                #     time.sleep(1)
