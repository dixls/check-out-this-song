import email
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash,
    abort,
)
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Song, Post, db, Follow, Like
from app import login_manager
from flask_login import login_required, login_user, logout_user, current_user
from app.search import YTSearch, LastFMSearch
from flask import current_app as app
from sqlalchemy import exc, or_, select
from .pagination import pagination
import app.forms
from app.helpers import get_user

main = Blueprint("main", __name__)

login_manager.login_view = "main.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except exc.SQLAlchemyError:
        return None


@main.route("/login", methods=["GET", "POST"])
def login():
    form = app.forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        if User.query.filter_by(username=username).first():
            user = User.authenticate(form.username.data, form.password.data)
            if user:
                if form.remember.data:
                    login_user(user, remember=True)
                else:
                    login_user(user)
                flash(f"Welcome back {username}", "success")

                next = request.args.get("next")
                # need to implement is_safe_url function for safe redirects
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
            if form.avatar.data == "":
                avatar = None
            else:
                avatar = form.avatar.data
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
                flash(
                    "An account already exists for that email address please login",
                    "warning",
                )

            return render_template("signup.html", form=form)

        login_user(new_user)
        return redirect(url_for(".root"))

    else:
        return render_template("signup.html", form=form)


@main.route("/")
def root():
    if request.args:
        page = int(request.args.get("p"))
        pages = pagination(page)
    else:
        page = 0
        pages = pagination(page)
    if current_user.is_authenticated:
        following_ids_query = db.session.execute(
            select([Follow.user_followed]).where(
                Follow.user_following == current_user.id
            )
        )
        following_ids = [id[0] for id in following_ids_query]
        posts = (
            Post.query.filter(
                or_(Post.user_id.in_(following_ids), Post.user_id == current_user.id)
            )
            .order_by(Post.timestamp.desc())
            .slice(pages["first_post_index"], (pages["last_post_index"] + 1))
        )
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).slice(
            pages["first_post_index"], (pages["last_post_index"] + 1)
        )

    num_posts = posts.count()
    return render_template(
        "home.html",
        posts=posts,
        page=page,
        items_per_page=pages["items_per_page"],
        num_posts=num_posts,
    )


@main.route("/users/<username>")
def user_details(username):
    try:
        (match, user) = get_user(username, current_user)
    except:
        abort(404)
    posts = (
        Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).limit(1)
    )
    follow_count = Follow.query.filter_by(user_followed=user.id).count()
    following_count = Follow.query.filter_by(user_following=user.id).count()
    liked_count = Like.query.filter_by(user_id=user.id).count()
    return render_template(
        "user_details.html",
        user=user,
        match=match,
        posts=posts,
        follow_count=follow_count,
        following_count=following_count,
        liked_count=liked_count
    )


@main.route("/users/<username>/followers")
def user_followers(username):
    try:
        (match, user) = get_user(username, current_user)
    except:
        abort(404)
    followers = user.followers
    follow_count = Follow.query.filter_by(user_followed=user.id).count()
    following_count = Follow.query.filter_by(user_following=user.id).count()
    liked_count = Like.query.filter_by(user_id=user.id).count()
    return render_template(
        "user_followers.html",
        user=user,
        match=match,
        followers=followers,
        follow_count=follow_count,
        following_count=following_count,
        liked_count=liked_count
    )


@main.route("/users/<username>/following")
def user_following(username):
    try:
        (match, user) = get_user(username, current_user)
    except:
        abort(404)
    following = user.following
    follow_count = Follow.query.filter_by(user_followed=user.id).count()
    following_count = Follow.query.filter_by(user_following=user.id).count()
    liked_count = Like.query.filter_by(user_id=user.id).count()
    return render_template(
        "user_following.html",
        user=user,
        match=match,
        following=following,
        follow_count=follow_count,
        following_count=following_count,
        liked_count=liked_count
    )


@main.route("/users/<username>/likes")
def user_likes(username):
    try:
        (match, user) = get_user(username, current_user)
    except:
        abort(404)
    likes = user.liked_posts
    follow_count = Follow.query.filter_by(user_followed=user.id).count()
    following_count = Follow.query.filter_by(user_following=user.id).count()
    liked_count = Like.query.filter_by(user_id=user.id).count()
    return render_template(
        "likes.html",
        user=user,
        match=match,
        likes=likes,
        follow_count=follow_count,
        following_count=following_count,
        liked_count=liked_count
    )


@main.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_user():
    form = app.forms.SignupForm(obj=current_user)
    if form.validate_on_submit():
        user = User.authenticate(current_user.username, form.password.data)
        if user:
            form.populate_obj(user)
            db.session.commit()
            flash("Profile saved successfully", "success")
            return redirect(url_for(".user_details", username=user.username))
        flash("Incorrect password", "danger")
    return render_template("edit_user.html", form=form, user=current_user)


@main.route("/usersearch")
def user_search():
    if request.args:
        query = request.args.get("q")
        results = User.query.filter(User.username.like("%" + query + "%")).slice(0, 15)
    else:
        query = None
        results = None
    return render_template("user_search.html", query=query, results=results)


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
    flash("new song posted successfully!", "success")
    return redirect("/")


@main.route("/follow", methods=["POST"])
@login_required
def follow():
    try:
        user_to_follow = User.query.get(int(request.json["follow_user_id"]))
        user_following = User.query.get(current_user.id)
        user_following.following.append(user_to_follow)
        db.session.commit()
        return {"response": True}
    except exc.SQLAlchemyError:
        return {"response": False}


@main.route("/unfollow", methods=["POST"])
@login_required
def unfollow():
    try:
        user_to_unfollow = User.query.get(int(request.json["follow_user_id"]))
        user_unfollowing = User.query.get(current_user.id)
        user_unfollowing.following.remove(user_to_unfollow)
        db.session.commit()
        return {"response": True}
    except exc.SQLAlchemyError:
        return {"response": False}


@main.route("/posts/like", methods=["POST"])
def like_post():
    try:
        user_liking = User.query.get(current_user.id)
        req = request.json
        post_to_like = Post.query.get(int(req["post_id"]))
        user_liking.liked_posts.append(post_to_like)
        db.session.commit()
        return {"response": True}
    except exc.SQLAlchemyError:
        return {"response": False}


@main.route("/posts/unlike", methods=["POST"])
def unlike_post():
    try:
        user_unliking = User.query.get(current_user.id)
        req = request.json
        post_to_unlike = Post.query.get(int(req["post_id"]))
        user_unliking.liked_posts.remove(post_to_unlike)
        db.session.commit()
        return {"response": True}
    except exc.SQLAlchemyError:
        return {"response": False}


@main.route("/posts/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    try:
        user = User.query.get(current_user.id)
        post_to_delete = Post.query.get(int(post_id))
    except exc.SQLAlchemyError:
        return {"response": False}
    if user == post_to_delete.user or user.admin:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            return {"response": True}
        except exc.SQLAlchemyError:
            return {"response": False}
    abort(503)


@main.route("/about")
def about():
    return render_template("about.html")


@main.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@main.errorhandler(503)
def not_found(e):
    return render_template("503.html")
