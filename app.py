from flask import Flask, redirect, request, url_for
import os
from data_manager import DataManager
from models import db, Movie


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
    return str(users)  # Temporarily returning users as a string


@app.route('/users', methods= ["POST"])
def add_user():
    new_username = request.form.get("username")
    data_manager.create_user(new_username)
    return redirect(url_for("list_users"))


@app.route("/users/<int:user_id>/movies")
def list_movies():
    pass


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    pass


if __name__ == '__main__':
  #with app.app_context():
  #  db.create_all()

  app.run()