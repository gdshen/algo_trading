import time
from pprint import pprint
from mongoengine import *

'''
a sample for user information
{ '_id': 'a long code for user id',
  'username': 'username',
  'password': 'password',
  'register_time': data_object,
  'user_level", number,
  'email', 'email address',
  'tel_number', 'telephone number'
}
'''

user_information = {
    'username': 'gdshen',
    'password': '123456',  # todo to user sha256 hash algorithm to replace a plain password
    'register_time': time.localtime(),
    'user_level': 1,
    'email': 'gdshen95@gmail.com',
    'tel_number': '18221488201'
}

pprint(user_information)

connect('trade')


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


ross = User(email='ross@example.com', first_name = 'Ross', last_name='lawley').save()
