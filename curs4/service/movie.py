from flask import current_app

from dao.movie import MovieDAO
from dao.model.movie import MovieSchema


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_by_id(self, pk):
        movie = self.dao.get_by_id(pk)

        return MovieSchema().dump(movie)

    def get_all_movies(self, data):

        movies_query = self.dao.get_movies()

        status = data.get('status')
        page = data.get('page')

        if status and status == 'new':
            movies_query = self.dao.get_new(movies_query)

        if page:
            limit = current_app.config['ITEMS_PER_PAGE']
            offset = (page - 1) * limit
            movies_query = self.dao.get_pages(movies_query, limit, offset)

        movies = self.dao.get_all(movies_query)

        return MovieSchema(many=True).dump(movies)
