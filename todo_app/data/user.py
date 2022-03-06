

from enum import Enum
class UserRole(Enum):
    reader = "reader"
    writer = "writer"

role_lookup = { "JackieMaw" : UserRole.reader }

from flask_login import UserMixin
class User(UserMixin):

    def __init__(self, id):
        self.id = id

    def get_role(self):
        return role_lookup[self.id]

class AnonymousUser(UserMixin):

    def __init__(self, id):
        self.id = id

    def get_role(self):
        return UserRole.writer
