from http import HTTPStatus


def test_root(test_app):

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