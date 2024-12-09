import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="048596e668f6462aac3d4c1e680cf083", 
        client_secret="29f72ea1157c4026831a73e1b1047905"
    )
)

followedArtists = {} #consider using SQLite


def searchArtistIdByName():
    results = sp.search(q='Imagine Dragons', limit=1)
    return results["tracks"]["items"][0]["album"]["artists"][0]["id"]

def followArtist(artist_id):
    artist_album = sp.artist_albums(artist_id, limit=50)
    followedArtists[artist_id] = len(artist_album)



results = sp.search(q='imagine dragons', limit=1)
artist_id = results["tracks"]["items"][0]["album"]["artists"][0]["id"]
artist_data = sp.artist(artist_id)
print(artist_data["name"])
artist_album = sp.artist_albums(artist_id, limit=50)
for album in artist_album["items"]:
    print(album["name"])
    print(album["release_date"])
    print(album["images"][0]["url"])
    print(album["album_type"])



'''
def searchArtistIdByName:
    results = sp.search(q='Imagine Dragons', limit=1)
    return results["items"][0]["id"]
'''