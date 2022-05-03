from app.models import Song, User
from app.search import YTSearch, LastFMSearch
from app import create_app
import pytest
from app import db


@pytest.fixture
def test_app():
    app = create_app("config.TestingConfig")
    app.config.from_object("config.TestingConfig")
    return app


@pytest.fixture
def test_db(test_app):
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
    user = User.signup(username="test_user1", email="user@text.com", password="unhashed-pw")
    return user


@pytest.fixture
def persisted_user(new_user, test_db):
    test_db.session.add(new_user)
    test_db.session.commit()
    return new_user


@pytest.fixture
def test_search_lfm():
    sanctuary_search = LastFMSearch("sanctuary elder")
    return sanctuary_search


@pytest.fixture
def test_search_yt():
    sanctuary_yt_search = YTSearch("sanctuary")
    return sanctuary_yt_search
