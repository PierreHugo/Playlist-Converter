from typing import List, Dict

import spotipy


def get_all_playlists(sp: spotipy.Spotify) -> List[Dict]:
    """
    Récupère toutes les playlists de l'utilisateur courant.
    """
    playlists = []
    results = sp.current_user_playlists(limit=50)

    while results:
        playlists.extend(results["items"])
        results = sp.next(results) if results["next"] else None

    return playlists


def get_playlist_tracks(
    sp: spotipy.Spotify,
    playlist_id: str
) -> List[Dict]:
    """
    Récupère tous les morceaux d'une playlist Spotify.
    """
    tracks = []
    results = sp.playlist_items(
        playlist_id,
        additional_types=["track"],
        limit=100
    )

    while results:
        for item in results["items"]:
            track = item.get("track")
            if not track:
                continue

            tracks.append({
                "name": track["name"],
                "artists": [a["name"] for a in track["artists"]],
                "duration_ms": track["duration_ms"],
                "isrc": track["external_ids"].get("isrc"),
            })

        results = sp.next(results) if results["next"] else None

    return tracks
