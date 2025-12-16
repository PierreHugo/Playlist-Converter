# Playlist-Converter

Outil personnel pour transférer des playlists de **Spotify vers Deezer** en utilisant
uniquement les APIs officielles.

Aucun service tiers, aucun abonnement, tout se fait en local.

---

## Prérequis

- Python **3.9+**
- Un compte Spotify
- Un compte Deezer

---

## Installation (première fois, sur n’importe quel ordinateur)

### 1. Cloner le dépôt

```bash
git clone https://github.com/pierrehugo/Playlist-Converter.git
cd Playlist-Converter
```

---

### 2. Créer et activer l’environnement Python

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

### 4. Créer le fichier `.env`

```bash
cp env.example .env
```

Puis éditer `.env` et remplir les valeurs :

#### Spotify
1. Aller sur https://developer.spotify.com/dashboard
2. Créer une application
3. Récupérer :
   - Client ID
   - Client Secret
4. Ajouter la Redirect URI suivante :
   ```
   http://127.0.0.1:8888/callback
   ```

#### Deezer
1. Aller sur https://developers.deezer.com/myapps
2. Créer une application
3. Récupérer :
   - App ID
   - App Secret
4. Ajouter la même Redirect URI :
   ```
   http://127.0.0.1:8888/callback
   ```

---

## Lancer le projet

Depuis la racine du repo :

```bash
python -m src.main
```

Lors du premier lancement :
- le navigateur s’ouvre
- Spotify demande l’autorisation
- un fichier `.spotify_cache` est créé automatiquement

---

## Sécurité

- Le fichier `.env` **n’est jamais versionné**
- Les tokens OAuth sont stockés localement
- Aucun secret n’est présent dans le code

Si un secret fuit par erreur :
- régénérer le secret depuis Spotify / Deezer
- mettre à jour `.env`