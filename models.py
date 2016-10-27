import datetime
from app import db


class User(db.Document):
    email = db.EmailField(unique=True)
    password = db.StringField(default=True)
    active = db.BooleanField(default=True)
    is_admin = db.BooleanField(default=False)
    timestamp = db.DateTimeField(default=datetime.datetime.now())