from flask import request
from flask_restx import Resource, Namespace, abort

from implemented import movie_service
from utils import auth_required

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        data = {
            'status': request.args.get('status'),
            'page': request.args.get('page')
        }

        movies = movie_service.get_all_movies(data)

        return movies, 200


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    @auth_required
    def get(self, bid):
        movie = movie_service.get_by_id(bid)

        if not movie:
            abort(404, message='Movie not found')

        return movie
