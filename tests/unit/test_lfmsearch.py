from app.search import LastFMSearch
from http import HTTPStatus
import pytest
from app import create_app

app = create_app("config.TestingConfig")
app.app_context().push()


def test_lastfm_search(test_search_lfm):
    """
    Testing search functionality for lastfm
    """
    test_search_lfm
    test_resp = test_search_lfm.results['resp']
    search_results = test_search_lfm.results['result']

    assert test_resp.ok
    assert search_results
