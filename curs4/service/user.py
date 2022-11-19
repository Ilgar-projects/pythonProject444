import calendar
from datetime import datetime, timedelta

import jwt as jwt

from dao.user import UserDAO
from utils import get_hash, get_access_token


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        users = self.dao.get_all()
        return users

    def create(self, user_d):
        user_d['password'] = get_hash(user_d['password'])
        return self.dao.create(user_d)

    def delete(self, uid):
        self.dao.delete(uid)

    def patch(self, data):
        user = self.get_one(data['id'])

        if data.get('name'):
            user.name = data['name']
        if data.get('surname'):
            user.name = data['surname']

    def update_password(self, data):
        pass


