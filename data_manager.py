from models import db, User, Movie

class DataManager():
    def create_user(self, name: str):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()


    def get_users(self):
        return db.session.query(User)


    def get_movies(self, user_id: int):
        return db.session.query(Movie) \
    .filter(Movie.user_id == user_id)


    def add_movie(self, movie: Movie):
        db.session.add(movie)
        db.session.commit()


    def update_movie(self, movie_id: int, new_title: str):
        movie = Movie.query.get(movie_id)
        movie.title = new_title
        db.session.commit()


    def delete_movie(self, movie_id: int):
        db.session.query(Movie) \
        .filter(Movie.movie_id == movie_id) \
        .delete()
        db.session.commit()
