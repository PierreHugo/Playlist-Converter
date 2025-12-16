from src.spotify_client import get_spotify_client


def main():
    sp = get_spotify_client()
    user = sp.current_user()

    print("✅ Spotify OAuth OK")
    print("Utilisateur :", user["display_name"])
    print("User ID     :", user["id"])


if __name__ == "__main__":
    main()
