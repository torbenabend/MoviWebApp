"""
Provides an abstraction layer for database operations.

This class encapsulates common CRUD operations for users and movies,
serving as an intermediary between the application logic and the
database models.
"""
from models import db, User, Movie

class DataManager():
    def create_user(self, name: str):
        """
        Create and persist a new user.

        Args:
            name (str): The name of the user.

        Returns:
            None
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()


    def get_users(self):
        """
        Retrieve all users.

        Returns:
            sqlalchemy.orm.query.Query: Query object for all users.
        """
        return db.session.query(User)


    def get_movies(self, user_id: int):
        """
        Retrieve all movies for a specific user.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            sqlalchemy.orm.query.Query: Query object for the user's movies.
        """
        return db.session.query(Movie) \
            .filter(Movie.user_id == user_id)


    def add_movie(self, movie: Movie):
        """
        Add and persist a new movie.

        Args:
            movie (Movie): The movie instance to add.

        Returns:
            None
        """
        db.session.add(movie)
        db.session.commit()


    def update_movie(self, movie_id: int, new_title: str):
        """
        Update the title of an existing movie.

        Args:
            movie_id (int): The unique identifier of the movie.
            new_title (str): The new title for the movie.

        Returns:
            None
        """
        movie = Movie.query.get(movie_id)
        movie.title = new_title
        db.session.commit()


    def delete_movie(self, movie_id: int):
        """
        Delete a movie by its ID.

        Args:
            movie_id (int): The unique identifier of the movie.

        Returns:
            None
        """
        db.session.query(Movie) \
        .filter(Movie.movie_id == movie_id) \
        .delete()
        db.session.commit()
