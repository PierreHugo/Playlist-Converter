from src.spotify_client import get_spotify_client
from src.spotify_playlists import get_all_playlists, get_playlist_tracks
from src.deezer_client import DeezerClient

# ⚠️ Mets ici le nom EXACT de la playlist Spotify ET Deezer à tester
TEST_PLAYLIST_NAME = "miam"
DEEZER_TARGET_PLAYLIST_ID = 14709835061

def build_search_query(track: dict) -> str:
    """
    Construit une requête Deezer simple et efficace.
    """
    artists = " ".join(track["artists"])
    return f'{track["name"]} artist:"{track["artists"][0]}"'


def find_deezer_track_id(dz: DeezerClient, track: dict) -> int | None:
    results = dz.public_search_track(
        track["name"],
        track["artists"][0]
    )

    data = results.get("data", [])
    if not data:
        return None

    return data[0]["id"]

def transfer_playlist(sp, dz: DeezerClient, playlist: dict):
    print(f"\n🎵 Playlist : {playlist['name']}")

    tracks = get_playlist_tracks(sp, playlist["id"])
    print(f"  → {len(tracks)} morceaux à transférer")

    # 🔑 Playlist Deezer EXISTANTE
    playlist_dz_id = DEEZER_TARGET_PLAYLIST_ID
    print("  → Playlist Deezer ciblée par ID")

    success = 0
    failed = []

    for track in tracks:
        deezer_id = find_deezer_track_id(dz, track)

        if not deezer_id:
            failed.append(track)
            print(f"  ❌ {track['name']}")
            continue

        res = dz.add_tracks(playlist_dz_id, [deezer_id])

        if res is False or res == {}:
            failed.append(track)
            print(f"  ❌ {track['name']} (refus Deezer)")
            continue

        success += 1
        print(f"  ✅ {track['name']}")


    print(f"\n  ✔ {success} transférés")
    print(f"  ✖ {len(failed)} échecs")

    return failed


def main():
    print("🚀 Démarrage transfert Spotify → Deezer\n")

    sp = get_spotify_client()
    dz = DeezerClient()

    playlists = get_all_playlists(sp)

    # 🔎 Filtre pour test
    if TEST_PLAYLIST_NAME:
        playlists = [
            p for p in playlists
            if TEST_PLAYLIST_NAME.lower() in p["name"].lower()
        ]

    print(f"{len(playlists)} playlist(s) sélectionnée(s)\n")

    all_failed = {}

    for playlist in playlists:
        failed = transfer_playlist(sp, dz, playlist)
        if failed:
            all_failed[playlist["name"]] = failed

    if all_failed:
        print("\n⚠️ Morceaux non transférés :")
        for playlist, tracks in all_failed.items():
            print(f"\nPlaylist : {playlist}")
            for t in tracks:
                print(f"  - {t['name']} ({', '.join(t['artists'])})")

    print("\n🎉 Transfert terminé")


if __name__ == "__main__":
    main()