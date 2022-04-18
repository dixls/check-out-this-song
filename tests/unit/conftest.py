from app.models import Song
import pytest


@pytest.fixture(scope="module")
def new_song():
    song = Song(title="", artist="", youtube_url="", lastfm_entry="")
    return song