from flask import Flask, request, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

app = Flask(__name__)
CORS(app)

# Spotify API credentials
CLIENT_ID = 'e060c3e4e5f743248e88088593f1d5ca'
CLIENT_SECRET = 'ab703da153db477e885cc55cef61543f'

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Function to get user's top tracks from a playlist
def get_user_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Function to recommend songs not in the playlist
def recommend_songs(tracks, k=5):
    track_uris = [track['track']['uri'] for track in tracks if track['track']['uri'] is not None]
    seed_tracks = random.sample(track_uris, min(len(track_uris), 5))
    recommended_tracks = sp.recommendations(seed_tracks=seed_tracks, limit=k)
    return [(track['name'], track['external_urls']['spotify']) for track in recommended_tracks['tracks']]

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    username = request.args.get('username')
    playlist_id = request.args.get('playlist_id')
    tracks = get_user_playlist_tracks(username, playlist_id)
    recommended_songs = recommend_songs(tracks, k=5)
    return jsonify(recommended_songs=recommended_songs)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    # Process feedback data
    # For demonstration, just return success
    return jsonify(message="Feedback submitted successfully")

if __name__ == '__main__':
    app.run(debug=True)
