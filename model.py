"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id,
                                               self.email)

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)


# Put your Movie and Rating model classes here.

class Movie(db.Model):
    """Movie on ratings website."""

    __tablename__ = "movies"

    def __repr__(self):
        """Provide helpful representation when printed."""

        the_m_rep = "<Movie movie_id=%s title=%s>"
        return the_m_rep % (self.movie_id, self.title)

    movie_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)

    title = db.Column(db.String,
                      nullable=False)

    released_at = db.Column(db.DateTime,
                            nullable=True)

    imdb_url = db.Column(db.String,
                         nullable=True)


class Rating(db.Model):
    """Movie scores on ratings website."""

    __tablename__ = "ratings"

    def __repr__(self):
        """Provide helpful representation when printed."""

        the_r_rep = "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>"
        return the_r_rep % (self.rating_id, self.movie_id, self.user_id,
                            self.score)

    rating_id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False)

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey("movies.movie_id"),
        nullable=False)

    score = db.Column(
        db.Integer,
        nullable=False)

    # user movie relationship

    movie = db.relationship('Movie',
                            backref=db.backref('ratings',
                                               order_by=rating_id))

    user = db.relationship('User',
                           backref=db.backref('ratings',
                                              order_by=rating_id))

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
