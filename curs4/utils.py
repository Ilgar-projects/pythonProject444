import hashlib
from datetime import datetime, timedelta

import jwt
from flask import request
from flask_restx import abort

from constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT


def get_hash(password: str):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    ).decode('utf-8', 'ignore')


def get_access_token(data: dict):
    min30 = datetime.utcnow() + timedelta(days=10)
    data['exp'] = int(min30.timestamp())
    access_token = jwt.encode(data, PWD_HASH_SALT, algorithm='HS256')

    days130 = datetime.utcnow() + timedelta(days=130)
    data["exp"] = int(days130.timestamp())
    refresh_token = jwt.encode(data, PWD_HASH_SALT, algorithm='HS256')

    return {"access_token": access_token, "refresh_token": refresh_token, "EXP": data["exp"]}


def check_refresh_token(refresh_token: str):
    try:
        data = jwt.decode(jwt=refresh_token, key=PWD_HASH_SALT, algorithms='HS256')
    except Exception as e:
        return None

    tokens = get_access_token(data)

    return tokens


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, PWD_HASH_SALT, algorithms=['HS256'])
        except Exception as e:
            print(f"JWT.decode auth Exception: {e}")
            abort(401)
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        role = None
        try:
            user = jwt.decode(token, PWD_HASH_SALT, algorithms='HS256')
            role = user.get("role")
        except Exception as e:
            print("JWT Decode admin Exception", e)
            abort(401)
        if role != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper



