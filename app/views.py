from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    jsonify,
    flash
)
from app.models import User, Song, Post, db
from app import login_manager
from app.search import YTSearch, LastFMSearch
from flask import current_app as app
import app.forms

main = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@main.route("/")
def root():
    db.session.rollback()
    posts = Post.query.all()
    if "new_song" in session:
        session.pop("new_song")
    if "post_desc" in session:
        session.pop("post_desc")
    return render_template("home.html", posts=posts)


@main.route("/search", methods=["GET", "POST"])
def search():
    form = app.forms.SongSearchForm()

    if form.validate_on_submit():
        query = form.search.data
        return redirect(url_for(".search_results", q=query))
    else:
        return render_template("songsearch.html", form=form)


@main.route("/search-results")
def search_results():
    query = request.args.get("q")
    lfm = LastFMSearch(query)
    matches = lfm.matches

    form = app.forms.SongSelectForm()

    return render_template(
        "search-results.html", matches=matches, query=query, form=form
    )


@main.route("/video-select", methods=["GET", "POST"])
def video_select():
    match = dict(title="", artist="")
    form = app.forms.SongSelectForm(obj=match)

    if form.validate_on_submit():
        match["title"] = form.title.data
        match["artist"] = form.artist.data
        match["lastfm_entry"] = form.lastfm_entry.data
        yt = YTSearch(match["title"] + " " + match["artist"])
        yt_matches = yt.matches
        yt_submit = app.forms.YTSubmitForm()
        session["new_song"] = match
        return render_template(
            "video_select.html", match=match, yt_matches=yt_matches, yt_submit=yt_submit
        )
    else:
        return redirect(url_for(".search"))


@main.route("/create-post", methods=["GET", "POST"])
def create_post():
    new_song = session["new_song"]
    form = app.forms.YTSubmitForm(obj=new_song)

    if form.validate_on_submit():
        new_song["youtube_url"] = form.youtube_url.data
        session["new_song"] = new_song
        post_form = app.forms.PostSubmitForm()
        return render_template("create_post.html", song=new_song, post_form=post_form)
    else:
        return redirect(url_for(".search"))


@main.route("/confirm-post", methods=["GET", "POST"])
def confirm_post():
    post_form = app.forms.PostSubmitForm()

    if post_form.validate_on_submit():
        description = post_form.description.data
        song_id = post_form.song_id.data
        new_song = session["new_song"]
        user = User.query.get_or_404(1)
        # placeholder user, add logic to get actual user when users implemented
        session["post_desc"] = description
        return render_template("confirm_post.html", description=description, user=user, song=new_song)
    else:
        return redirect("/")


@main.route("/submit")
def submit():
    new_song = session["new_song"]
    description = session["post_desc"]
    song = Song(title=new_song['title'], artist=new_song['artist'], lastfm_entry=new_song['lastfm_entry'], youtube_url=new_song['youtube_url'])
    db.session.add(song)
    user = User.query.get_or_404(1)
    new_post = Post(song_id=song.id, description=description, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()
    flash('posted successfully')
    return redirect('/')