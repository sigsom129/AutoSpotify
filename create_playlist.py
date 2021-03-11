# Step 1: Log into youtube
# Step 2: Grab our liked video
# Step 3: Create a new playlist In spotify
# Step 4: Create Search for the Song 
# Step 5: Add the Song to the spotify playlist

import json
import requests
from secrets import spotify_user_id
from secrets import spotify_token


class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_tokens = spotify_token

    def get_youtube_client(self):
        pass

    def get_liked_videos(self):
        pass
    #Creates a new PlayList 
    def create_playlist(self):

        request_body = json.dumps({
            "name": "Liked YouTube",
            "description": "Liked Videos on YouTube",
            "public": True
            })
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data= request_body,
            headers= {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_tokens)
            }
        )

        response_json = response.json()
# returns the playlist ID
        return response_json["id"]


# Search for a Song 
    def get_spotify_uri(self, song_name, artist):

        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        
        response = requests.get(
            query,
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_tokens)
            }
        )

        response_json = response.json()
        songs = response_json["tracks"]["items"]
        uri = songs[0]["uri"]

        return uri


    def add_song_to_spotify_playlist(self):
        pass


# THis SHOULD've BEEN DONE WEEKS AGO 


if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_spotify_playlist()