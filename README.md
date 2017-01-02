# Algorithmic Trading
## Project description

This project is for *Financial Computing Service* course which is hosted by **Shanghai Jiao Tong University** with **Morgan Stanley**. 

## What is algorithmic trading?

From [wikipedia](https://en.wikipedia.org/wiki/Algorithmic_traing)

> Algorithmic trading is a method of executing a large order(too large to fill all at once) using automated  pro-programmed trading instructions accounting for variables such as time, price, and volume to send small slices of the order (child orders) out to the market overtime.



## Dependency

You need all these third-party python library to run the whole program. (Note that we just test the project under python 3.5.2, but it should work with any python version that support all these library)

```bash
aiohttp
requests
pandas
tushare
html5lib
pymongo
mongoengine
arrow
flask
flask-mongoengine
flask-bcrypt
flask-debugtoolbar
flask-login
redis
```

## Project structure

`libs.policy` holds policy of slicing orders.(including a trival twap, vwap by n days mean volume and vwap with prediction)

`libs.back_test.py` for backtest the performance of one of the three policy.

`libs.data_persist_mongodb.py` persists historical tick data to mongodb.

`libs.data_persisit_redis.py` persists realtime quotes into redis server.

`libs.OrderMatch` does order match inside our system with the real market.

`predict` contains machine learning algorithm of predicting the trend and volume of a security

`static` hosts the static resources needed by flask web framework.

`template` hosts html files need by flask web framework.

`app.py auth.py forms.py models.py user.py` are all python files for run flask web framework.

`presentation` keynotes for presentation our project.



### Python docstring format we use

```python
def function_name(param1, param2):
    '''describe what this functino does in one line
    
    multipline to describle what this function does
    
    :param param1: first arg
    :type param1: first arg type
    :param param2: second arg
    :type param2: second arg type
    :return return_value
    :rtype: return type of the return value
    '''
```
