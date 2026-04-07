"""
Database models for the movie collection application.

This module defines the SQLAlchemy ORM models for users and movies,
including their attributes and relationships. It also initializes
the shared SQLAlchemy database instance.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String

db = SQLAlchemy()


class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        user_id (int): Primary key, unique identifier for the user.
        name (str): Name of the user (max length 100 characters).
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        """
        Return a human-readable string representation of the user.

        Returns:
            str: User name and unique identifier.
        """
        return f"{self.name} (User-ID: {self.user_id})"


class Movie(db.Model):
    """
    Represents a movie associated with a user.

    Attributes:
        movie_id (int): Primary key, unique identifier for the movie.
        title (str): Title of the movie (max length 100 characters).
        director (str): Name of the movie's director.
        year (int): Release year of the movie.
        poster_url (str): URL to the movie poster image.
        user_id (int): Foreign key referencing the associated user.
    """
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    director = Column(String)
    year = Column(Integer)
    poster_url = Column(String)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    def __str__(self):
        """
        Return a human-readable string representation of the movie.

        Returns:
            str: Movie title and release year.
        """
        return f"{self.title} ({self.year})"
