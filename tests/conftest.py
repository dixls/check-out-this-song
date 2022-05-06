from app.models import Song, User
from app import create_app, login_manager
from flask_login import FlaskLoginClient
import pytest
from app import db


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")
    app.config.from_object("config.TestingConfig")
    app.test_client_class = FlaskLoginClient
    return app


@pytest.fixture
def test_db(app):
    db.create_all()
    yield db
    db.session.close()
    db.drop_all()


@pytest.fixture
def new_song():
    song = Song(
        title="Army of Me",
        artist="Bjork",
        youtube_url="https://www.youtube.com/watch?v=VaLfiKq_Kvw",
        lastfm_entry="https://www.last.fm/music/Bj%C3%B6rk/_/Army+of+Me",
    )
    return song


@pytest.fixture
def persisted_song(test_db, new_song):
    test_db.session.add(new_song)
    test_db.session.commit()
    return new_song


@pytest.fixture
def new_user():
    user = User.signup(
        username="test_user1", email="user@text.com", password="unhashed-pw"
    )
    return user


@pytest.fixture
def persisted_user(new_user, test_db):
    test_db.session.add(new_user)
    test_db.session.commit()
    return new_user


@pytest.fixture
def test_with_authenticated_user(test_app, persisted_user):
    with test_app.test_request_context():
        yield flask_login.login_user(persisted_user)

