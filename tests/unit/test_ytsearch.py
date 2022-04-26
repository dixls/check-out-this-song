import pytest
from app import create_app

app = create_app("config.TestingConfig")
app.app_context().push()


def test_yt_search(test_search_yt):
    """
    Testing search functionality for lastfm
    """
    test_search_yt
    test_resp = test_search_yt.results['resp']
    search_results = test_search_yt.results['result']

    assert test_resp.ok
    assert search_results
