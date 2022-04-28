import bcrypt
from .extensions import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

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
    songs = db.relationship("Song", secondary="posts", backref="users")
    liked_posts = db.relationship("Post", secondary="likes", backref="users_liked")
    posts = db.relationship("Post", backref="user", lazy=True)

    is_authenticated = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    is_anonymous = db.Column(db.Boolean)

    @classmethod
    def get_id(self):
        return f"{self.id}"

    @classmethod
    def signup(cls, username, email, password, avatar=None, bio=None, admin=False):
        """sign up a new user with hashed password"""

        hashed_pass = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            email=email,
            password=hashed_pass,
            avatar=avatar,
            bio=bio,
            admin=admin,
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """
        checks credentials and returns user if successful, returns False if not

        hopefully successfully checks against both username and password
        """


class Song(db.Model):
    """table to organize songs that have been submitted"""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    youtube_url = db.Column(db.String)
    lastfm_entry = db.Column(db.String)
    other_url = db.Column(db.String)
    posts = db.relationship("Post", backref="song", lazy=True)

    def __repr__(self):
        return f"Song: {self.title} by {self.artist}"


class Post(db.Model):
    """relationship table for each post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("songs.id"), nullable=False)
    description = db.Column(db.String)
    timestamp = db.Column(db.DateTime, nullable=False)


class Like(db.Model):
    """relationship table for likes"""

    __tablename__ = "likes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)


class Follow(db.Model):
    """relationship table for follows"""

    __tablename__ = "follows"

    user_following = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        primary_key=True,
    )
    user_followed = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        primary_key=True,
    )
