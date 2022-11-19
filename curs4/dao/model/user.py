from setup_db import db
from marshmallow import Schema, fields
from dao.model.basemodel import BaseModelId


class User(BaseModelId, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    favorite_genre = db.Column(db.String(150))


class UserSchema(Schema):
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    surname = fields.Str()
