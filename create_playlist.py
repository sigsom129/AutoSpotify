# Step 1: Log into youtube
# Step 2: Grab our liked video
# Step 3: Create a new playlist In spotify
# Step 4: Create Search for the Song 
# Step 5: Add the Song to the spotify playlist

import os
import json
import requests
import youtube_dl

from secrets import spotify_user_id
from secrets import spotify_token
from exceptions import ResponseException

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors



class CreatePlaylist:

    def __init__(self):
        self.all_song_info = {}
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()

# Getting the YOUTUBE API to work with application

    def get_youtube_client(self):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

            # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

        return youtube



# Grabbing liked videos on youtube

    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )

        response = request.execute()

        #grabbing the information of the videos 
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["id"])

        #use youtube_dl to collect the song name and artist name
        video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)
        song_name = video["track"]
        artist = video["artist"]

        if song_name is not None and artist is not None:
            # save the information if the info given isn't none
            self.all_song_info[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artists": artist,
                # Using our function we created
                "spotify_uri": self.get_spotify_uri(song_name, artist)

            }



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
                "Authorization": "Bearer {}".format(self.spotify_token)
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
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        response_json = response.json()
        songs = response_json["tracks"]["items"]
        uri = songs[0]["uri"]

        return uri




    def add_song_to_spotify_playlist(self):
        # Add all the liked videos from youtube into the spotify playlist
        self.get_liked_videos()
        
        #collect all the uri
        uris = [info["sportiy_uri"] for song, info in self.all_song_info.items()]

        playlist_id = self.create_playlist()

        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

                # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json





if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_spotify_playlist()