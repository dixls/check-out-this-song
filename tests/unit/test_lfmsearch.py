def test_lastfm_search(app, test_search_lfm):
    """
    Testing search functionality for lastfm
    """
    test_resp = test_search_lfm.results['resp']
    matches = test_search_lfm.matches

    assert test_resp.ok
    assert matches
