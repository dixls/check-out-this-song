from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
import app.forms
from app.models import User, Song, Post
from app.extensions import login_manager, db
from app.search import YTSearch, LastFMSearch

main = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@main.route("/")
def root():
    db.session.rollback()
    return render_template("home.html")


@main.route("/search", methods=["GET", "POST"])
def search():
    form = app.forms.SongSearchForm()

    if form.validate_on_submit():
        query = form.search.data
        return redirect(url_for('.search_results', q=query))
    else:
        return render_template("songsearch.html", form=form)


@main.route("/search-results")
def search_results():
    query = request.args.get('q')
    lfm = LastFMSearch(query)
    matches = lfm.matches

    form = app.forms.SongSelectForm()

    return render_template("search-results.html", matches=matches, query=query, form=form)


@main.route("/video-select", methods=["GET", "POST"])
def video_select():
    match = Song(title="",artist="",)
    form = app.forms.SongSelectForm(obj=match)

    if form.validate_on_submit():
        form.populate_obj(match)
        db.session.add(match)
        db.session.commit()
        yt = YTSearch(match.title + ' ' + match.artist)
        yt_matches = yt.matches
        yt_submit = app.forms.YTSubmitForm()
        session['new_post_id'] = match.id
        return render_template('video_select.html', match=match, yt_matches=yt_matches, yt_submit=yt_submit)
    else:
        return redirect(url_for('.search'))


@main.route("/create-post", methods=["GET", "POST"])
def create_post():
    new_post_id = session['new_post_id']
    song = Song.query.get_or_404(new_post_id)
    form = app.forms.YTSubmitForm(obj=song)

    if form.validate_on_submit():
        form.populate_obj(song)
        db.session.add(song)
        raise
        db.session.flush()
        post_form = app.forms.PostSubmitForm()
        return render_template('create_post.html', song=song, post_form=post_form)
    else:
        return redirect(url_for('.search'))


@main.route("/confirm-post", methods=["GET", "POST"])
def confirm_post():
    post_form = app.forms.PostSubmitForm()

    if post_form.validate_on_submit():
        description = post_form.description.data
        song_id = post_form.song_id.data
        song = Song.query.get_or_404(song_id)
        user = User.query.get_or_404(1)
        #placeholder user, add logic to get actual user when users implemented
        new_post = Post(song_id=song_id, description=description, user_id=user.id)
        db.session.add(new_post)
        return render_template('confirm_post.html', post=new_post, user=user, song=song)
    else:
        return redirect('/')