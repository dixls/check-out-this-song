from flask import Blueprint, render_template, redirect, url_for, request
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


@main.route("/search", methods=["GET", "POST"])
def search():
    form = app.forms.SongSearchForm()

    if form.validate_on_submit():
        query = form.search.data
        return redirect(url_for('.create_post', q=query))
    else:
        return render_template("songsearch.html", form=form)


@main.route("/create-post", methods=["GET", "POST"])
def create_post():
    query = request.args.get('q')
    lfm = LastFMSearch(query)
    matches = lfm.matches

    return render_template("create-post.html", matches=matches, query=query)