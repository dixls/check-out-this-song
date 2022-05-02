from builtins import classmethod
import bcrypt
from . import db
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func
from flask_login import UserMixin

bcrypt = Bcrypt()


class Post(db.Model):
    """relationship table for each post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="posts", lazy=True)
    song_id = db.Column(db.Integer, db.ForeignKey("songs.id"), nullable=False)
    song = db.relationship("Song", back_populates="posts", lazy=True)
    description = db.Column(db.String)
    timestamp = db.Column(db.DateTime, server_default=func.now())

    def __repr__(self):
        return f"post {self.id} by {self.user.username}"

    def date_format(self):
        date = self.timestamp.date()
        return f"{date.strftime('%B')} {date.day}, {date.year}"


class Like(db.Model):
    """relationship table for likes"""

    __tablename__ = "likes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"), primary_key=True)
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


class User(UserMixin, db.Model):
    """user class"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    avatar = db.Column(db.String, default="/static/user_icon-01.png")
    bio = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)
    songs = db.relationship("Song", secondary="posts", viewonly=True)
    liked_posts = db.relationship("Post", secondary="likes", backref="users_liked")
    posts = db.relationship("Post", back_populates="user", lazy=True)

    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follow.user_followed == id),
        secondaryjoin=(Follow.user_following == id),
        overlaps="following, users"
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follow.user_following == id),
        secondaryjoin=(Follow.user_followed == id),
        overlaps="followers, users"
    )
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return f"User #{self.id}: {self.username}"

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

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False


class Song(db.Model):
    """table to organize songs that have been submitted"""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    youtube_url = db.Column(db.String)
    lastfm_entry = db.Column(db.String)
    other_url = db.Column(db.String)
    posts = db.relationship("Post", back_populates="song", lazy=True)
    users = db.relationship("User", secondary="posts", viewonly=True)

    def __repr__(self):
        return f"Song: {self.title} by {self.artist}"
