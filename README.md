# algo_trading
Algorithmic Trading Code Of SJTU Team

## Dependency
to run data_feed.py, we need

```
easyquotation
tushare
html5lib
pandas
pymongo
mongoengine
arrow
flask
flask-mongoengine
flask-bcrypt
flask-debugtoolbar
redis
```

and create database called `trade` in mysql server.

## Mongodb
[install mongodb on windows and start mongodb as windows services](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
[install mongodb on ubuntu](https://docs.mongodb.com/v3.2/tutorial/install-mongodb-on-ubuntu/)

After set configuration from this tutorial, just use `net start MongoDB` to start mongodb services.

## database design
### user authentication

### stocks owned by users
one user is a document, all users forms a collection. stocks owned by uses as a list.
1. user id
2. stock id
3. amount 

### users pending orders
1. user id
2. stock id
3. action
4. amount
5. time to put into market
6. status

### users order history
1. user id
2. stock id
3. action
4. amount
5. time that put into market
6. time that matched

## how to make a flask login system
1. flask_login (User class, user_load methods)
2. login view
3. forms

## Python docstring

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

# todo
separate flask application with algo engine using rpc
