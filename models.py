import datetime

from mongoengine import Document, EmailField, StringField, BooleanField, DateTimeField, IntField
from mongoengine import connect


class User(Document):
    email = EmailField(unique=True)
    password = StringField(default='')
    active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Order(Document):
    user_id = StringField(default='')
    stock = StringField(default=True)
    volume = IntField(default=0)
    action = IntField(default=0)  # 0 present buy, 1 present sell
    time = DateTimeField(default=datetime.datetime.now())


if __name__ == '__main__':
    connect('trade', host='192.168.1.150', port=27017)
    order = Order(user_id='1234', stock='600000', volume=10000, action=0, time=datetime.datetime.now())
    order.save()
