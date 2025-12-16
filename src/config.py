import os
import sys
from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"❌ Variable d'environnement manquante : {name}")
        sys.exit(1)
    return value


# Spotify
SPOTIFY_CLIENT_ID = _require("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = _require("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = _require("SPOTIFY_REDIRECT_URI")

# Deezer
DEEZER_APP_ID = _require("DEEZER_APP_ID")
DEEZER_APP_SECRET = _require("DEEZER_APP_SECRET")
DEEZER_REDIRECT_URI = _require("DEEZER_REDIRECT_URI")

# Deezer token (sera utilisé plus tard)
DEEZER_ACCESS_TOKEN = os.getenv("DEEZER_ACCESS_TOKEN")
