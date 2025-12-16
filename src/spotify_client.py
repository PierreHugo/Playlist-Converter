import spotipy
from spotipy.oauth2 import SpotifyOAuth

from src.config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
)


def get_spotify_client() -> spotipy.Spotify:
    """
    Initialise et retourne un client Spotify authentifié
    pour l'utilisateur courant.
    """
    scope = (
        "playlist-read-private "
        "playlist-read-collaborative"
    )

    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope,
        cache_path=".spotify_cache"
    )

    return spotipy.Spotify(auth_manager=auth_manager)
