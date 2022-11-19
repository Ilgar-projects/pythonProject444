from marshmallow import Schema, fields
from dao.model.basemodel import BaseModelId

from setup_db import db


class Director(BaseModelId, db.Model):
    __tablename__ = 'director'

    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
