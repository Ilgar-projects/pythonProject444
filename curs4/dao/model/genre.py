from marshmallow import Schema, fields
from dao.model.basemodel import BaseModelId

from setup_db import db


class Genre(BaseModelId, db.Model):
    __tablename__ = 'genre'

    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
