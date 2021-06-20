"""Models for flaskFeedback"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """connects database to flask app"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """user"""

    __tablename__ = "users"

    # username no longer than 20 characters

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )

    # password, email 50char limit, first and last name 30char limit

    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship(
        "Feedback", backref="user", cascade="all,delete")

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """register the user and hash the password using bcrypt"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # adduser to session

        db.session.add(user)
        return user


class Feedback(db.Model):
    """feedback"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey(
        'users.username'), nullable=False,)
