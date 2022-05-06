from cgi import test
from http import HTTPStatus
from flask_login import login_user, current_user
from flask import session


def test_root(client, app, test_db):

    response = client.get("/")
    assert response.status_code == HTTPStatus.OK


def test_login_get(client, app):

    response = client.get("login")
    assert response.status_code == HTTPStatus.OK


def test_login_post(client, app, persisted_user):

    response = client.post(
        "login",
        data={"username": persisted_user.username, "password": "unhashed-pw"},
        follow_redirects=True,
    )
    assert b"Welcome back" in response.data


def test_login_post_bad_pw(client, app, persisted_user):

    response = client.post(
        "login",
        data={"username": persisted_user.username, "password": "wrong_password"},
        follow_redirects=True,
    )
    assert b"Invalid credentials" in response.data


def test_login_post_bad_username(client, app, persisted_user):

    response = client.post(
        "login",
        data={"username": "badusername", "password": "unhashed-pw"},
        follow_redirects=True,
    )
    assert b"Username not found" in response.data


def test_signup_get(app):

    with app.test_client() as test_client:
        response = test_client.get("/signup")
        assert response.status_code == HTTPStatus.OK
        assert b"Sign up for Check Out This Song!" in response.data


def test_signup_post(client, app, test_db):

    response = client.post(
        "/signup",
        data={
            "username": "testSignupUser",
            "password": "test_signup_password",
            "email": "test_email@email.com",
            "avatar": None,
            "bio": "",
        },
        follow_redirects=True,
    )
    print(response.data)
    assert b"Welcome to Check Out This Song" in response.data


def test_signup_post_illegal_username(client, app, test_db):

    response = client.post(
        "/signup",
        data={
            "username": "test_signup_user",
            "password": "test_signup_password",
            "email": "test_email@email.com",
            "avatar": None,
            "bio": "",
        },
        follow_redirects=True,
    )
    assert b'<p class="help is-danger">' in response.data


def test_user_detail_page(client, app, test_db, persisted_user):

    response = client.get(f"/users/{persisted_user.username}")
    assert b"test_user1" in response.data
    assert response.status_code == HTTPStatus.OK


def test_user_detail_page_404(client, app):

    response = client.get(f"/users/not_a_real_user")
    assert b"404" in response.data


def test_edit_user_get(app, test_db, persisted_user):
    """
    Given a registered user
    When that user attempts to view the edit-profile page
    Then the page should be found without a 404

    I cannot get this one to work at all, I've tried a number of different ways to login a user, but it's unclear if they work, and if they do, none seem to let current_user function right.
    """
    with app.test_client(user=persisted_user) as test_client:
        response = test_client.get("/edit-profile")

    assert response.status_code == HTTPStatus.OK
    assert current_user.id == persisted_user.id
    assert b"404" not in response.data
    assert b"503" not in response.data


def test_user_search(client, app):
    response = client.get("/usersearch")
    assert b"Search for a user" in response.data


def test_user_search_q(client, app, persisted_user):
    response = client.get("/usersearch", query_string={"q": "test"})
    assert b"test_user1" in response.data


def test_user_search_no_results(client, app, persisted_user):
    response = client.get("/usersearch", query_string={"q": "fakeuser"})
    assert b"no results found" in response.data


def test_song_search(client, app):
    response = client.get("/search")
    assert b"Search for a song title" in response.data


def test_song_search_post(client, app):
    response = client.post("/search", data={"search": "song_title"})
    assert response.status_code == HTTPStatus.FOUND
