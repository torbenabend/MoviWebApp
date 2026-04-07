"""
Flask web application for managing users and their movie collections.

This module defines routes for creating users, listing users and their
movies, adding movies via the OMDb API, updating movie titles, and
deleting movies. It uses SQLAlchemy for database interaction and a
DataManager abstraction for business logic.
"""
from flask import flash, Flask, redirect, request, url_for, render_template
import os
from data_manager import DataManager
from models import db, Movie
from data_fetcher import fetch_omdb_data


app = Flask(__name__)
app.secret_key = "secretkey"


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def list_users():
    """
    Display a list of all users.

    Returns:
        Response: Rendered template with all users.
    """
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route('/users', methods= ["POST"])
def create_user():
    """
    Create a new user.

    Retrieves the username from the submitted form and creates a new user
    via the data manager.

    Returns:
        Response: Redirect to the user list page.
    """
    new_username = request.form.get("username")
    data_manager.create_user(new_username)
    return redirect(url_for("list_users"))


@app.route("/users/<int:user_id>/movies")
def list_movies(user_id):
    """
    Display all movies for a specific user.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        Response: Rendered template with the user's movies.
    """
    users = data_manager.get_users()
    user = next(
        (user for user in users if user.user_id == user_id)
    )
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=movies, user=user)



@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    """
    Add a new movie for a specific user.

    Fetches movie details from the OMDb API based on the provided title
    and stores the movie in the database. If the movie is not found,
    an error message is flashed.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        Response: Redirect to the user's movie list.
    """
    movie_title = request.form.get("movie_title")
    try:
        title, director, year, poster_url = fetch_omdb_data(movie_title)
        new_movie = Movie(
            title=title,
            director=director,
            year=year,
            poster_url=poster_url,
            user_id=user_id
        )
        data_manager.add_movie(new_movie)
    except ValueError:
        flash("Movie not found in OMDb.", "error")

    return redirect(url_for("list_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Update the title of an existing movie.

    Args:
        user_id (int): The unique identifier of the user.
        movie_id (int): The unique identifier of the movie.

    Returns:
        Response: Redirect to the user's movie list.
    """
    new_title = request.form.get("updated_title")
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for("list_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Delete a movie from a user's collection.

    Args:
        user_id (int): The unique identifier of the user.
        movie_id (int): The unique identifier of the movie.

    Returns:
        Response: Redirect to the user's movie list.
    """
    data_manager.delete_movie(movie_id)
    return redirect(url_for("list_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found():
    """
    Handle 404 (page not found) errors.

    Returns:
        tuple: Rendered 404 template and HTTP status code 404.
    """
    return render_template("404.html"), 404


if __name__ == '__main__':
    """
    Run the Flask development server.

    Starts the application using the default Flask development server.
    Database initialization can be enabled if required.
    """
    #with app.app_context():
    #  db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)