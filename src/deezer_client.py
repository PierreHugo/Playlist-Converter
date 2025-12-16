import requests
import random
from src.config import DEEZER_ARL

BASE_URL = "https://www.deezer.com/ajax/gw-light.php"


class DeezerClient:
    def __init__(self):
        self.session = requests.Session()

        # Cookies Deezer
        self.session.cookies.set("arl", DEEZER_ARL, domain=".deezer.com", path="/")
        self.session.cookies.set("arl", DEEZER_ARL, domain="www.deezer.com", path="/")

        # Headers navigateur
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.deezer.com/",
            "Origin": "https://www.deezer.com",
        })

        self.cid = random.randint(10**7, 10**8)
        self.api_token = None

        self._bootstrap()

    def _url(self, api_token: str | None = None) -> str:
        return (
            f"{BASE_URL}"
            f"?api_version=1.0"
            f"&api_token={api_token or ''}"
            f"&input=3"
            f"&cid={self.cid}"
        )

    def _post(self, url: str, payload: dict):
        r = self.session.post(url, json=payload)
        r.raise_for_status()
        return r.json().get("results", {})

    def _bootstrap(self):
        payload = {
            "method": "deezer.getUserData",
            "params": {}
        }

        data = self._post(self._url(), payload)

        self.api_token = data.get("checkForm")
        if not self.api_token:
            raise RuntimeError(
                "Échec récupération api_token Deezer."
            )

        user = data.get("USER", {})
        self.user_id = user.get("USER_ID")

        if not self.user_id:
            raise RuntimeError("Impossible de récupérer USER_ID Deezer")


    def _call(self, method: str, params: dict):
        payload = {
            "method": method,
            "params": params
        }
        return self._post(self._url(self.api_token), payload)

    # =====================
    # API UTILISABLES
    # =====================

    def get_user(self):
        data = self._call("deezer.getUserData", {})
        return data.get("USER", {})
    
    def search_track(self, title: str, artist: str):
        return self._call("search.music", {
            "query": {
                "query": title,
                "filters": {
                    "artist": [artist]
                }
            },
            "start": 0,
            "nb": 5
        })

    def create_playlist(self, title: str):
        return self._call("playlist.create", {
            "title": title,
            "description": "",
            "status": 0,
            "type": 0,
            "parent_user_id": self.user_id
        })


    def add_tracks(self, playlist_id: int, track_ids: list[int]):
        songs = ",".join(str(tid) for tid in track_ids)
        return self._call("playlist.addSongs", {
        "playlist_id": playlist_id,
        "songs": songs,
        "offset": 0,
        "checkForm": self.api_token
    })



    
    def get_user_playlists(self, limit=100):
        return self._call("playlist.getUserPlaylists", {
            "user_id": self.user_id,
            "limit": limit
        })


    def public_search_track(self, title: str, artist: str):
        query = f"{title} {artist}"
        r = requests.get(
            "https://api.deezer.com/search",
            params={"q": query},
            timeout=10
        )
        r.raise_for_status()
        return r.json()
