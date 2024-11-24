# Spotify to YouTube Playlist Creator

This Python app duplicates your Spotify liked songs into a YouTube playlist.

## Features
- Fetches your Spotify liked songs.
- Creates a new YouTube playlist.
- Adds corresponding YouTube videos for each Spotify song.

## Prerequisites
- Python 3.8 or later installed on your system.
- A [Spotify Developer Account](https://developer.spotify.com/dashboard/) to get your API credentials.
- A [Google Cloud Project](https://console.cloud.google.com/) with the YouTube Data API v3 enabled.

## Setup

### Clone the Repository
```bash
git clone https://github.com/your-username/spotify-to-youtube-playlist.git
cd spotify-to-youtube-playlist





---

## Example Output

```bash
Fetching your Spotify liked songs...
Spotify Liked Songs:
1. Valhalla Calling by Miracle Of Sound
2. Blinding Lights by The Weeknd
3. Imagine by John Lennon

Authenticating with YouTube...
Authentication successful!

Creating YouTube playlist...
Playlist 'Spotify Favorites' created successfully with ID: PL12345abcde.

Adding songs to playlist...
Added: Valhalla Calling
Added: Blinding Lights
Added: Imagine

Done! Your YouTube playlist is ready.
