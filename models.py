import datetime
from mongoengine import Document, EmailField, StringField, BooleanField, DateTimeField


class User(Document):
    email = EmailField(unique=True)
    password = StringField(default=True)
    active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    timestamp = DateTimeField(default=datetime.datetime.now())
