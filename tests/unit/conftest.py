from app.models import Song
from app import create_app
import pytest
from app.extensions import db


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
    song = Song(title="Army of Me", artist="Bjork", youtube_url="https://www.youtube.com/watch?v=VaLfiKq_Kvw", lastfm_entry="https://www.last.fm/music/Bj%C3%B6rk/_/Army+of+Me")
    return song