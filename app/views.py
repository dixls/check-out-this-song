from flask import Blueprint, render_template
import app.forms
from app.models import User, Song
from app.extensions import login_manager, db
from app.search import YTSearch, LastFMSearch

main = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@main.route("/")
def root():
    
    return render_template("home.html")

@main.route("/search")
def search():
    form = app.forms.SongSearchForm()

    if form.validate_on_submit():
        return f"{form.data}"
    else:
        return render_template("songsearch.html", form=form)