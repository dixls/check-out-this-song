from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, URL
from wtforms_validators import AlphaNumeric


class SignupForm(FlaskForm):
    """Form for a new user to sign up"""

    username = StringField("Username", validators=[DataRequired(), AlphaNumeric(message="username can only contain letters and numbers")])
    email = StringField("E-mail Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    bio = TextAreaField("Bio")
    avatar = StringField("Profile Picture URL", validators=[URL()])


class LoginForm(FlaskForm):
    """Form for existing users to login"""

    username = StringField("Username or E-mail Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Stay logged in?")


class SongSearchForm(FlaskForm):
    """Form to search for songs to post"""

    search = StringField("Search for a song title", validators=[DataRequired()])


class SongSelectForm(FlaskForm):
    """Form to select a song from results"""

    title = HiddenField("Title")
    artist = HiddenField("Artist")
    lastfm_entry = HiddenField("Last FM URL")


class YTSubmitForm(FlaskForm):
    """Form to add a youtube video to a song submission"""

    youtube_url = HiddenField("Youtube URL")