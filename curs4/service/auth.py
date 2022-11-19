import hashlib
from datetime import datetime, timedelta

import jwt

from dao.user import UserDAO
from utils import get_hash

from constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT


class AuthService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def auth_user(self, email, password):
        user = self.dao.get_user_by_email(email)

        if not user:
            return None

        hash_password = get_hash(password)

        if hash_password != user.password:
            return None

        data = {
            "email": user.email,
        }

        return self.get_access_token(data)

    def get_hash(self, password: str):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode('utf-8', 'ignore')

    def get_access_token(self, data: dict):
        min30 = datetime.utcnow() + timedelta(days=10)
        data['exp'] = int(min30.timestamp())
        access_token = jwt.encode(data, PWD_HASH_SALT, algorithm='HS256')

        days130 = datetime.utcnow() + timedelta(days=130)
        data["exp"] = int(days130.timestamp())
        refresh_token = jwt.encode(data, PWD_HASH_SALT, algorithm='HS256')

        return {"access_token": access_token, "refresh_token": refresh_token, "EXP": data["exp"]}

    def check_refresh_token(self, refresh_token: str):
        try:
            data = jwt.decode(jwt=refresh_token, key=PWD_HASH_SALT, algorithms='HS256')
        except Exception as e:
            return None

        tokens = self.get_access_token(data)

        return tokens
