import email
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    jsonify,
    flash,
    abort,
)
from app.models import User, Song, Post, db
from app import login_manager
from flask_login import login_required, login_user, logout_user, current_user
from app.search import YTSearch, LastFMSearch
from flask import current_app as app
from sqlalchemy import exc
import app.forms

main = Blueprint("main", __name__)

login_manager.login_view = "main.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


@main.route("/login", methods=["GET", "POST"])
def login():
    form = app.forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        if User.query.filter_by(username=username).first():
            user = User.authenticate(form.username.data, form.password.data)
            if user:
                login_user(user)
                flash(f"Welcome back {username}", "success")

                next = request.args.get("next")
                # if not is_safe_url(next):
                #     return abort(400)
                # need to implement is_safe_url function for redirects
                return redirect(next or url_for(".root"))
            flash("Invalid credentials", "danger")
        else:
            flash("Username not found", "danger")
    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for(".root"))


@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = app.forms.SignupForm()

    if form.validate_on_submit():
        try:
            if form.avatar.data == '':
                avatar=None
            else:
                avatar=form.avatar.data
            new_user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                avatar=avatar,
                bio=form.bio.data,
            )
            db.session.commit()
            flash("Welcome to Check Out This Song!", "success")

        except exc.IntegrityError as error:
            if "username" in str(error.orig):
                flash("That username is already taken!", "danger")
            if "email" in str(error.orig):
                flash("An account already exists for that email address please login", "warning")

            return render_template("signup.html", form=form)

        login_user(new_user)
        return redirect(url_for(".root"))

    else:
        return render_template("signup.html", form=form)


@main.route("/")
def root():
    db.session.rollback()
    default = 5
    if request.args:
        page = int(request.args.get("p"))
        a = page * default
        b = a+default
    else:
        a = 0
        b = default
        page = None
    posts = Post.query.order_by(Post.timestamp.desc()).slice(a,b)
    num_posts = posts.count()
    if "new_song" in session:
        session.pop("new_song")
    if "post_desc" in session:
        session.pop("post_desc")
    return render_template("home.html", posts=posts, page=page, default=default, num_posts=num_posts)


@main.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = app.forms.SongSearchForm()

    if form.validate_on_submit():
        query = form.search.data
        return redirect(url_for(".search_results", q=query))
    else:
        return render_template("songsearch.html", form=form)


@main.route("/search-results")
@login_required
def search_results():
    query = request.args.get("q")
    lfm = LastFMSearch(query)
    matches = lfm.matches

    form = app.forms.SongSelectForm()

    return render_template(
        "search-results.html", matches=matches, query=query, form=form
    )


@main.route("/video-select", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
def confirm_post():
    post_form = app.forms.PostSubmitForm()

    if post_form.validate_on_submit():
        description = post_form.description.data
        new_song = session["new_song"]
        user = User.query.get_or_404(current_user.id)
        session["post_desc"] = description
        return render_template(
            "confirm_post.html", description=description, user=user, song=new_song
        )
    else:
        return redirect("/")


@main.route("/submit")
def submit():
    new_song = session["new_song"]
    description = session["post_desc"]
    song = Song(
        title=new_song["title"],
        artist=new_song["artist"],
        lastfm_entry=new_song["lastfm_entry"],
        youtube_url=new_song["youtube_url"],
    )
    db.session.add(song)
    user = User.query.get_or_404(current_user.id)
    new_post = Post(song_id=song.id, description=description, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()
    flash("posted successfully")
    return redirect("/")
