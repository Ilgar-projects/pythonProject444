from setup_db import db


class BaseModelId(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
