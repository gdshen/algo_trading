from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email=None, password=None, active=True, user_id=None):
        self.email = email
        self.password = password
        self.active = active
        self.is_admin = False
        self.id = user_id

    def get_by_id(self, user_id):
        pass
