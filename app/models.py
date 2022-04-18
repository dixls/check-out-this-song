from enum import unique
from .extensions import db

class User(db.Model):
    """user class"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    avatar = db.Column(db.String)
    bio = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)
    email_confirm = db.Column(db.Boolean, default=False)
    account_enabled = db.Column(db.Boolean, default=True)


class Song(db.Model):
    """table to organize songs that have been submitted"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    youtube_url = db.Column(db.String)
    lastfm_entry = db.Column(db.String)