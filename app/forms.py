from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, HiddenField
from wtforms.validators import Length, URL, InputRequired, Optional
from wtforms_validators import AlphaNumeric


class SignupForm(FlaskForm):
    """Form for a new user to sign up"""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            AlphaNumeric(message="username can only contain letters and numbers"),
        ],
    )
    email = StringField("E-mail Address", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8)])
    bio = TextAreaField("Bio")
    avatar = StringField("Profile Picture URL", validators=[URL(require_tld=True, message="Please use a valid URL"), Optional()])


class LoginForm(FlaskForm):
    """Form for existing users to login"""

    username = StringField("Username or E-mail Address", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Stay logged in?")


class SongSearchForm(FlaskForm):
    """Form to search for songs to post"""

    search = StringField("Search for a song title", validators=[InputRequired()])


class SongSelectForm(FlaskForm):
    """Form to select a song from results"""

    title = HiddenField("Title")
    artist = HiddenField("Artist")
    lastfm_entry = HiddenField("Last FM URL")


class YTSubmitForm(FlaskForm):
    """Form to add a youtube video to a song submission"""

    youtube_url = HiddenField("Youtube URL")


class PostSubmitForm(FlaskForm):
    """Form for submitting a song as a post"""

    description = TextAreaField("Why did you choose this track?")
    song_id = HiddenField("song id")
