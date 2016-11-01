import tushare as ts
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('foo2', 'bar2')
r.hmset(1134, {1:2, 3:4})
print(r.get('foo2'))

df = ts.get_realtime_quotes('600000')

# r.set
