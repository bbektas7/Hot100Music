from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-public"
CLIENT_ID = "844053f26cdd4eed867489e941524e42"
CLIENT_SECRET = "f26a0b46b82d4e99953131f9ec8ee195"
REDIRECT_URI = "http://example.com"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/2000-08-12/#")

soup = BeautifulSoup(response.text, "html.parser")

music_hot_100 = []
new_music_hot_100 = []
musics = soup.select("li ul li h3")

music_hot_100 = [music.getText() for music in musics]

for music in music_hot_100:
    music = music.replace("\n","")
    music = music.replace("\t","")
    new_music_hot_100.append(music)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=REDIRECT_URI, 
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in new_music_hot_100:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
