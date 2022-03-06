

from enum import Enum
class UserRole(Enum):
    reader = "reader"
    writer = "writer"

role_lookup = { "JackieMaw" : UserRole.writer }

from flask_login import UserMixin
class User(UserMixin):

    def __init__(self, id):
        self.id = id

    def get_role(self):
        if self.id in role_lookup:
            return role_lookup[self.id]
        else:
            return UserRole.reader

class AnonymousUser(UserMixin):

    def __init__(self):
        self.id = "Anonymous"

    def get_role(self):
        return UserRole.writer
