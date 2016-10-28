# algo_trading
Algorithmic Trading Code Of SJTU Team

## team members

## Dependency
to run data_feed.py, we need

```bash
tushare
pandas
pymongo
PyMySQL
sqlalchemy
Flask-PyMongo
mongoengine
flask-mongoengine
flask-bcrypt
flask-debugtoolbar
```

and create database called `trade` in mysql server.

## Mongodb
[install mongodb on windows and start mongodb as windows services](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)

After set configuration from this tutorial, just use `net start MongoDB` to start mongodb services.

## Todo

- [x] Learn how to use mongoengine & flask-mongoengine to connect to mongodb in flask app
- [x] Learn how tu use flask-login to code for user login module
- [ ] Optimize user login flow
- [ ] Add password hash
 
## how to make a flask login system
1. flask_login (User class, user_load methods)
2. login view
3. forms

