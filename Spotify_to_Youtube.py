#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Required Libraries
# Before running the script, install the following libraries:
# pip install spotipy google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 python-dotenv

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ------------------- Spotify Integration -------------------

# Spotify API credentials
SPOTIPY_CLIENT_ID = "---"  ###### Replace with your Spotify Client ID
SPOTIPY_CLIENT_SECRET = "---"  ###### Replace with your Spotify Client Secret
SPOTIPY_REDIRECT_URI = "http://localhost:8080/callback"

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-library-read"
))

# Function to get liked songs from Spotify
def get_liked_songs():
    """
    Fetch liked songs from Spotify.
    Returns:
        - A list of strings in the format "Song Name by Artist Name".
    """
    try:
        results = sp.current_user_saved_tracks()
        if not results['items']:
            print("No liked songs found on Spotify.")
            return []
        songs = []
        for item in results['items']:
            track = item['track']
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            songs.append(f"{song_name} by {artist_name}")
        return songs
    except Exception as e:
        print(f"Error fetching liked songs from Spotify: {e}")
        return []

# Now we get the liked songs
liked_songs = get_liked_songs()
print("Spotify Liked Songs:")
for song in liked_songs:
    print(song)

# ------------------- YouTube API Integration -------------------

# YouTube API credentials
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Authenticate and build the YouTube API client
def authenticate_youtube():
    """
    Authenticate and return the YouTube API client.
    """
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            r"C:\Users\client_secret.json", SCOPES  # Replace with your client_secret.json file path
        )
        credentials = flow.run_local_server(port=0)
        youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        return youtube
    except FileNotFoundError:
        print("Error: 'client_secret.json' file not found. Please ensure the file is in the specified location.")
        exit(1)
    except Exception as e:
        print(f"Error during YouTube authentication: {e}")
        exit(1)

# Create a YouTube playlist
def create_playlist(youtube, title, description):
    """
    Create a YouTube playlist.
    Args:
        - youtube: Authenticated YouTube API client.
        - title: Name of the playlist.
        - description: Description of the playlist.
    Returns:
        - Playlist ID of the created playlist.
    """
    try:
        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": ["Spotify", "Favorites"],
                    "defaultLanguage": "en"
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        )
        response = request.execute()
        print(f"Playlist '{title}' created with ID: {response['id']}")
        return response["id"]
    except HttpError as e:
        print(f"Error creating playlist: {e}")
        return None

# Search for a video on YouTube
def search_video(youtube, query):
    """
    Search for a video on YouTube.
    Args:
        - youtube: Authenticated YouTube API client.
        - query: Search term (e.g., "Song Name by Artist Name").
    Returns:
        - The video ID of the first search result, or None if no results are found.
    """
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            maxResults=1,
            type="video"
        )
        response = request.execute()
        if not response["items"]:
            print(f"No results found on YouTube for '{query}'.")
            return None
        video_id = response["items"][0]["id"]["videoId"]
        return video_id
    except HttpError as e:
        print(f"An error occurred while searching for '{query}': {e}")
        return None

# Add a video to a playlist
def add_video_to_playlist(youtube, playlist_id, video_id):
    """
    Add a video to a YouTube playlist.
    Args:
        - youtube: Authenticated YouTube API client.
        - playlist_id: The ID of the playlist.
        - video_id: The ID of the video to add.
    """
    try:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        request.execute()
        print(f"Added video ID {video_id} to playlist ID {playlist_id}")
    except HttpError as e:
        print(f"An error occurred: {e}")

# ------------------- Main Script -------------------

def main():
    print("Welcome to the Spotify to YouTube Playlist Creator!")

    # Authenticate with YouTube
    youtube = authenticate_youtube()

    # Create a new playlist
    playlist_name = "Spotify Favorites"
    playlist_description = "A playlist created by duplicating Spotify Liked Songs."
    playlist_id = create_playlist(youtube, playlist_name, playlist_description)

    if not playlist_id:
        print("Failed to create playlist. Exiting.")
        return

    # Search for each Spotify song on YouTube and add it to the playlist
    for song in liked_songs:
        video_id = search_video(youtube, song)
        if video_id:
            add_video_to_playlist(youtube, playlist_id, video_id)

    print(f"\nPlaylist '{playlist_name}' created successfully!")
    print(f"Check your YouTube account to view the playlist.")

if __name__ == "__main__":
    main()


# In[ ]:




