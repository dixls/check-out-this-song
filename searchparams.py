

class YTSearch:
    params = {
        "videoCategoryId":"10",
        "part":"snippet",
        "type":"video"
        }
    root_url = "https://www.googleapis.com/youtube/v3/search"


class LastFMSearch:
    params = {
        "method":"track.search",
        "format":"json"
    }
    root_url = "http://ws.audioscrobbler.com/2.0/"