def test_yt_search(app, test_search_yt):
    """
    Testing search functionality for lastfm
    """
    test_resp = test_search_yt.results['resp']
    matches = test_search_yt.matches

    assert test_resp.ok
    assert matches
