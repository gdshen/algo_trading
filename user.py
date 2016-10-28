from flask_login import UserMixin
import models


class User(UserMixin):
    def __init__(self, email=None, password=None, active=True):
        self.email = email
        self.password = password
        self.active = active
        self.is_admin = False
        self.user_id = None

    def save(self):
        # persist user information to database
        new_user = models.User(email=self.email, password=self.password, active=self.active)
        new_user.save()
        print("new user id = {}".format(new_user.id))
        self.user_id = new_user.id
        return self.user_id

    def get_id(self):
        return self.user_id

    def get_by_id(self, user_id):
        db_user = models.User.objects.with_id(user_id)
        if db_user:
            self.email = db_user.email
            self.active = db_user.active
            self.user_id = db_user.id

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
    another_user.get_by_id(user.user_id)
