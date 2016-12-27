from pprint import pprint

from config import REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB
import redis
import json

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

if __name__ == '__main__':
    pprint(read_from_redis())