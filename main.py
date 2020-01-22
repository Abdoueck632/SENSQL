from flask import Flask, request
from flask_restful import Resource, Api
from Recuperation import CreateDB,GeAttributAndType
app = Flask(__name__)
api = Api(app=app)
ns_books = api.namespace('db', description = "Books operations")
ns_movies = api.namespace('movies', description = "Movies operations")
@ns_books.route("/")
class BooksList(Resource):
    def get(self):
        """
        returns a list of books
        """
        return GeAttributAndType("Teste.json","Awa")
    def post(self):
        """
        Add a new book to the list
        """
@ns_books.route("/<string:title>")
class Book(Resource):
    def put(self, title):
        """
        Edits a selected book
        """
        CreateDB(title)
        return "Creation de la base de données reussit"
    def delete(self, title):
        """
    delete a selected book
    """
@ns_movies.route("/")
class MoviesList(Resource):
    def get(self):
        """
        returns a list of movies
        """
    def post(self):
        """
        Add a new movie to the list
        """
@ns_movies.route("/<string:title>")
class Movie(Resource):
    def put(self, title):
        """
        Edits a selected movie
        """
    def delete(self, title):
        """
    delete a selected movie
    """
app.run(port= 8887, host= '127.0.0.1')
