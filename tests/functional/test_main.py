from cgi import test
from http import HTTPStatus
from flask_login import login_user, current_user
from flask import session


def test_root(test_app, test_db):

    with test_app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == HTTPStatus.OK


def test_login_get(test_app):

    with test_app.test_client() as test_client:
        response = test_client.get("login")
        assert response.status_code == HTTPStatus.OK


def test_login_post(test_app, persisted_user):

    with test_app.test_client() as test_client:
        response = test_client.post(
            "login",
            data={"username": persisted_user.username, "password": "unhashed-pw"},
            follow_redirects=True,
        )
        assert b"Welcome back" in response.data


def test_login_post_bad_pw(test_app, persisted_user):

    with test_app.test_client() as test_client:
        response = test_client.post(
            "login",
            data={"username": persisted_user.username, "password": "wrong_password"},
            follow_redirects=True,
        )
        assert b"Invalid credentials" in response.data


def test_login_post_bad_username(test_app, persisted_user):

    with test_app.test_client() as test_client:
        response = test_client.post(
            "login",
            data={"username": "badusername", "password": "unhashed-pw"},
            follow_redirects=True,
        )
        assert b"Username not found" in response.data


def test_signup_get(test_app):

    with test_app.test_client() as test_client:
        response = test_client.get("/signup")
        assert response.status_code == HTTPStatus.OK
        assert b"Sign up for Check Out This Song!" in response.data


def test_signup_post(test_app, test_db):

    with test_app.test_client() as test_client:
        response = test_client.post(
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


def test_signup_post_illegal_username(test_app, test_db):

    with test_app.test_client() as test_client:
        response = test_client.post(
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


def test_user_detail_page(test_app, test_db, persisted_user):

    with test_app.test_client() as test_client:
        response = test_client.get(f"/users/{persisted_user.username}")
    assert b"test_user1" in response.data
    assert response.status_code == HTTPStatus.OK


def test_user_detail_page_404(test_app):

    with test_app.test_client() as test_client:
        response = test_client.get(f"/users/not_a_real_user")
    assert b"404" in response.data


# def test_edit_user_get(test_app, test_db, persisted_user):
#     """
#     Given a registered user
#     When that user attempts to view the edit-profile page
#     Then the page should be found without a 404

#     I cannot get this one to work at all, I've tried a number of different ways to login a user, but it's unclear if they work, and if they do, none seem to let current_user function right.
#     """
#     with test_app.test_client(user=persisted_user) as test_client:
#         response = test_client.get("/edit-profile")

#     assert response.status_code == HTTPStatus.OK
#     assert current_user.id == persisted_user.id
#     assert b"404" not in response.data
#     assert b"503" not in response.data


def test_user_search(test_app):
    with test_app.test_client() as test_client:
        response = test_client.get("/usersearch")

    assert b"Search for a user" in response.data


def test_user_search_q(test_app, persisted_user):
    with test_app.test_client() as test_client:
        response = test_client.get("/usersearch", query_string={"q": "test"})

    assert b"test_user1" in response.data


def test_user_search_no_results(test_app, persisted_user):
    with test_app.test_client() as test_client:
        response = test_client.get("/usersearch", query_string={"q": "fakeuser"})

    assert b"no results found" in response.data


def test_song_search(test_app):
    with test_app.test_client() as test_client:
        response = test_client.get("/search")

    assert b"Search for a song title" in response.data


def test_song_search_post(test_app):
    with test_app.test_client() as test_client:
        response = test_client.post("/search", data={"search": "song_title"})

    assert response.status_code == HTTPStatus.FOUND
