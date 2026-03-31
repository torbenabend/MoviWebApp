from flask import Flask, redirect, request, url_for, render_template
import os
from data_manager import DataManager
from models import db, Movie
from data_fetcher import fetch_omdb_data


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def list_users():
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route('/users', methods= ["POST"])
def create_user():
    new_username = request.form.get("username")
    data_manager.create_user(new_username)
    return redirect(url_for("list_users"))


@app.route("/users/<int:user_id>/movies")
def list_movies(user_id):
    users = data_manager.get_users()
    user = next(
        (user for user in users if user.user_id == user_id)
    )
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=movies, user=user)



@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    movie_title = request.form.get("movie_title")
    title, director, year, poster_url = fetch_omdb_data(movie_title)
    new_movie = Movie(
        title=title,
        director=director,
        year=year,
        poster_url=poster_url,
        user_id=user_id
    )
    data_manager.add_movie(new_movie)
    return redirect(url_for("list_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get("updated_title")
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for("list_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    pass


if __name__ == '__main__':
  #with app.app_context():
  #  db.create_all()

  app.run()