from flask_login import UserMixin
import logging
import models


class User(UserMixin):
    def __init__(self, email=None, password=None, active=True):
        self.email = email
        self.password = password
        self.active = active
        self.is_admin = False
        self.id = None

    def save(self):
        # persist user information to database
        new_user = models.User(email=self.email, password=self.password, active=self.active)
        new_user.save()
        logging.debug("register - - new user id = {}".format(new_user.id))
        self.id = new_user.id
        return self.id

    def get_id(self):
        return self.id

    def get_by_email(self, email, password_acquirement=False):
        db_user = models.User.objects.get(email=email)
        if db_user:
            self.email = db_user.email
            self.active = db_user.active
            self.id = db_user.id
            if password_acquirement:
                self.password = db_user.password
            return self
        else:
            return None

    def get_by_id(self, user_id):
        db_user = models.User.objects.with_id(user_id)
        if db_user:
            self.email = db_user.email
            self.active = db_user.active
            self.id = db_user.id

            return self
        else:
            return None


if __name__ == '__main__':
    from mongoengine import connect

    # save a new user
    connect('trade')
    user = User()
    user.email = 'gdshen95@gmail.com'
    user.password = '123456'
    user.save()

    # get a user information from database
    another_user = User()
    another_user.get_by_id(user.id)
