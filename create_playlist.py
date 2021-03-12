# Step 1: Log into youtube
# Step 2: Grab our liked video
# Step 3: Create a new playlist In spotify
# Step 4: Create Search for the Song 
# Step 5: Add the Song to the spotify playlist

import json
import requests
from secrets import spotify_user_id
from secrets import spotify_token

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors



class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_tokens = spotify_token

    def get_youtube_client(self):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secrets.json"

            # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

        return youtube





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
# Need the playlist ID to add specific songs to the playlist
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




if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_spotify_playlist()