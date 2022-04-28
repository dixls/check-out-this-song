import os
import requests
from dotenv import load_dotenv

load_dotenv()


class YTSearch:
    """
    Formatting for retrieving youtube search results for a given query
    """

    def __init__(self, query):
        self.params = {
            "videoCategoryId": "10",
            "part": "snippet",
            "type": "video",
            "q": query,
            "videoEmbeddable": True,
            "key": os.getenv("YOUTUBE_KEY"),
        }
        self.root_url = "https://www.googleapis.com/youtube/v3/search"
        self.results = self.get_results()
        self.matches = self.results['result']['items']

    def get_results(self):
        resp = requests.get(self.root_url, self.params)
        youtube_results = resp.json()

        return {"resp": resp, "result": youtube_results}


class LastFMSearch:
    """
    Formatting for retrieving last.fm search results for a given query
    """

    def __init__(self, query):
        self.params = {
            "method": "track.search",
            "format": "json",
            "track": query,
            "api_key": os.getenv("LASTFM_KEY"),
        }
        self.root_url = "http://ws.audioscrobbler.com/2.0/"
        self.results = self.get_results()
        self.matches = self.results['result']['results']['trackmatches']['track']

    def get_results(self):
        resp = requests.get(self.root_url, self.params)
        lastfm_results = resp.json()

        return {"resp": resp, "result": lastfm_results}
