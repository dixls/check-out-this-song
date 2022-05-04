from app.search import YTSearch, LastFMSearch
import pytest


@pytest.fixture
def test_search_lfm():
    sanctuary_search = LastFMSearch("sanctuary elder")
    return sanctuary_search


@pytest.fixture
def test_search_yt():
    sanctuary_yt_search = YTSearch("sanctuary")
    return sanctuary_yt_search
