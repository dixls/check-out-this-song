from http import HTTPStatus
from flask_login import login_user, current_user
from flask import session
from pytest_mock import mocker
from unittest import mock
from app.search import LastFMSearch, YTSearch


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
    assert b"404 " in response.data


def test_user_search_no_results(client, app, persisted_user):
    response = client.get("/usersearch", query_string={"q": "fakeuser"})
    assert b"no results found" in response.data


def test_song_search(client, app):
    response = client.get("/search")
    assert b"Search for a song title" in response.data


def test_song_search_post(client, app):
    response = client.post("/search", data={"search": "song_title"})
    assert response.status_code == HTTPStatus.FOUND


def test_edit_user_get(app, test_db, persisted_user):
    """
    Given a registered user
    When that user attempts to view the edit-profile page
    Then the page should be found without a 404
    """
    with app.test_client(user=persisted_user) as test_client:
        response = test_client.get("/edit-profile")
        current_user = persisted_user

    assert response.status_code == HTTPStatus.OK
    assert current_user.id == persisted_user.id
    assert bytes(current_user.email, "utf8") in response.data
    assert b"404 " not in response.data
    assert b"503 " not in response.data


def test_user_search(client, app):
    response = client.get("/usersearch")

    assert b"Search for a user" in response.data
    assert response.status_code == HTTPStatus.OK


def test_user_search_with_query(client, app, persisted_user):
    response = client.get("/usersearch?q=test")

    assert bytes(persisted_user.username, "utf8") in response.data
    assert response.status_code == HTTPStatus.OK


def test_user_search_with_bad_query(client, app, persisted_user):
    response = client.get("/usersearch?q=jibberish")

    assert b"Sorry, no results found" in response.data
    assert response.status_code == HTTPStatus.OK


def test_song_search(app, test_db, persisted_user):
    with app.test_client(user=persisted_user) as test_client:
        response = test_client.get("/search")
        current_user = persisted_user

    assert response.status_code == HTTPStatus.OK
    assert b"Search for a song title" in response.data


def test_song_search_results(client, app, mocker):
    """Not sure if mock implemented properly?"""
    mocker.patch(
        "app.views.LastFMSearch.get_results",
        return_value={
            "result": {
                "results": {
                    "trackmatches": {
                        "track": [
                            {
                                "name": "Army of Me",
                                "artist": "björk",
                                "url": "https://www.last.fm/music/Bj%C3%B6rk/_/Army+of+Me",
                                "image": "/static/user_icon-01.png"
                            }
                        ]
                    }
                }
            }
        },
    )
    response = client.get("/search-results?q=army of me")
    
    assert response.status_code == HTTPStatus.OK
    assert b"bj\xc3\xb6rk" in response.data


def test_song_search_bad_results(client, app):
    response = client.get("/search-results?q=gnjresklfodiasseewap")

    assert response.status_code == HTTPStatus.OK
    assert b"no matches found" in response.data


def test_video_select(client, app, mocker):
    """Test works, but mock does not, test fails because expected result based on mocked YTSearch is not passed"""
    mocker.patch(
        "app.views.YTSearch.get_results",
        return_value={
            "result": {
                "items": [
                    {
                        "snippet": {
                            "title": "björk : army of me (HD)",
                            "channelTitle": "björk",
                        },
                        "id": {"videoId": "jPeheoBa2_Y"},
                    }
                ]
            }
        },
    )

    response = client.post(
        "/video-select",
        data={
            "title": "Army of Me",
            "artist": "Bj\xc3\xb6rk",
            "url": "https://www.last.fm/music/Bj%C3%B6rk/_/Army+of+Me",
        },
    )

    assert b"army of me" in response.data