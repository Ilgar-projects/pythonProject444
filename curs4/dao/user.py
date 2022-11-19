from dao.model.user import User

from setup_db import db


class UserDAO:
    def __init__(self, session: db):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.name = user_d.get("name")

        self.session.add(user)
        self.session.commit()

    def get_user_by_email(self, email: str):
        user = self.session.query(User).filter(User.email == email).one_or_none()
        return user
