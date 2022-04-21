from app.models import Song
import pytest
from app import create_app

app = create_app("config.TestingConfig")
app.app_context().push()


def test_song_model(new_song, test_db):
    """just a test test"""
    test_db.session.add(new_song)
    test_db.session.commit()

    assert new_song.id
