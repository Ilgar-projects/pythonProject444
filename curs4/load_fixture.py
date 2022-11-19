from sqlalchemy.exc import IntegrityError

from dao.model.genre import Genre
from dao.model.director import Director
from dao.model.movie import Movie
from setup_db import db
from config import Config

import json

from app import create_app


def read_json(filename, encoding="utf-8"):
    with open(filename, encoding=encoding) as f:
        return json.load(f)

app = create_app(Config)

data = read_json("fixtures.json")

with app.app_context():
    for genre in data["genres"]:
        db.session.add(Genre(id=genre["pk"], name=genre["name"]))

    for director in data["directors"]:
        db.session.add(Director(id=director["pk"], name=director["name"]))

    for movie in data["movies"]:
        db.session.add(
            Movie(id=movie["pk"], title=movie["title"], description=movie["description"], trailer=movie["trailer"],
                  year=movie["year"], rating=movie["rating"], genre_id=movie["genre_id"],
                  director_id=movie["director_id"]))

    try:
        db.session.commit()
    except IntegrityError:
        print("Fixtures already loaded")
