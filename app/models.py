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
    songs = db.Relationship("Song", secondary="posts", backref="users")
    liked_posts = db.Relationship("Post", secondary="likes", backref="users_liked")


class Song(db.Model):
    """table to organize songs that have been submitted"""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    youtube_url = db.Column(db.String)
    lastfm_entry = db.Column(db.String)
    other_url = db.Column(db.String)


class Post(db.Model):
    """relationship table for each post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        backref=db.backref("posts", lazy=True),
    )
    song_id = db.Column(
        db.Integer,
        db.ForeignKey("songs.id"),
        nullable=False,
        backref=db.backref("posts", lazy=True),
    )
    timestamp = db.Column(db.DateTime, nullable=False)


class Like(db.Model):
    """relationship table for likes"""

    __tablename__ = "likes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
