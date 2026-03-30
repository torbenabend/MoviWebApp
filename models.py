from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return f"{self.name} (User-ID: {self.user_id})"


class Movie(db.Model):
    __tablename__ = "Movies"

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    director = Column(String)
    year = Column(Integer)
    poster_url = Column(String)
    user_id = Column(Integer, ForeignKey="Users.user_id")

    def __str__(self):
        return f"{self.title} ({self.year})"
