import tkinter as tk
from tkinter import Label, Button, Radiobutton, IntVar
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import requests

# Spotify API credentials
CLIENT_ID = '66d8529b6ab94fe19c9fe63116b0df35'
CLIENT_SECRET = '7bfa110389a94919aef8d84f4f85cfde'

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Declare global variables
recommended_songs = []
like_dislike_vars = []

# Function to get user's top tracks from a playlist
def get_user_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Function to recommend songs not in the playlist
def recommend_songs(tracks, k=5, seeds=None):
    track_uris = [track['track']['uri'] for track in tracks if track['track']['uri'] is not None]
    if seeds:
        seed_uris = [track['track']['uri'] for track in tracks if track['track']['name'] in seeds]
        recommended_tracks = sp.recommendations(seed_tracks=seed_uris, limit=k)
    else:
        seed_tracks = random.sample(track_uris, min(len(track_uris), 5))
        recommended_tracks = sp.recommendations(seed_tracks=seed_tracks, limit=k)
    return [(track['name'], track['external_urls']['spotify']) for track in recommended_tracks['tracks']]

# Function to display recommendations in the GUI
def display_recommendations():
    global recommended_songs
    global like_dislike_vars
    tracks = get_user_playlist_tracks(username_entry.get(), playlist_id_entry.get())
    recommended_songs = recommend_songs(tracks, k=5)
    like_dislike_vars = [IntVar() for _ in range(len(recommended_songs))]

    for i, (song_name, song_link) in enumerate(recommended_songs):
        song_label = Label(recommendations_frame, text=song_name)
        song_label.grid(row=i, column=0, padx=10, pady=5)

        like_radio = Radiobutton(recommendations_frame, text="Like", variable=like_dislike_vars[i], value=1)
        like_radio.grid(row=i, column=1, padx=5, pady=5)

        dislike_radio = Radiobutton(recommendations_frame, text="Dislike", variable=like_dislike_vars[i], value=0)
        dislike_radio.grid(row=i, column=2, padx=5, pady=5)

# Function to submit feedback to the server
def submit_feedback_to_server(username, song_name, feedback):
    url = 'http://127.0.0.1:5000/submit_feedback'
    data = {'username': username, 'song_name': song_name, 'feedback': feedback}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Feedback submitted successfully to the server")
    else:
        print("Failed to submit feedback to the server")

# Function to generate improved recommendations based on feedback
def generate_improved_recommendations():
    global recommended_songs
    global like_dislike_vars
    global username_entry
    global playlist_id_entry

    # Retrieve the entered username and playlist ID
    username = username_entry.get()
    playlist_id = playlist_id_entry.get()

    # Get tracks from the playlist
    tracks = get_user_playlist_tracks(username, playlist_id)

    # Extract the user feedback from the radio buttons and submit to server
    for i, (song_name, _) in enumerate(recommended_songs):
        feedback = like_dislike_vars[i].get()
        submit_feedback_to_server(username, song_name, feedback)

    # Get improved recommendations based on feedback
    improved_recommendations = recommend_songs(tracks, k=5)  # You need to implement this function
    recommended_songs = improved_recommendations  # Update recommended songs with improved recommendations

    # Clear the recommendations frame
    for widget in recommendations_frame.winfo_children():
        widget.destroy()

    # Display the new recommendations
    for i, (song_name, song_link) in enumerate(recommended_songs):
        song_label = Label(recommendations_frame, text=song_name)
        song_label.grid(row=i, column=0, padx=10, pady=5)

        like_radio = Radiobutton(recommendations_frame, text="Like", variable=like_dislike_vars[i], value=1)
        like_radio.grid(row=i, column=1, padx=5, pady=5)

        dislike_radio = Radiobutton(recommendations_frame, text="Dislike", variable=like_dislike_vars[i], value=0)
        dislike_radio.grid(row=i, column=2, padx=5, pady=5)

# GUI setup
root = tk.Tk()
root.title("Song Recommendation System")
root.geometry("400x400")

username_label = Label(root, text="Enter Spotify Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

playlist_id_label = Label(root, text="Enter Playlist ID:")
playlist_id_label.pack()
playlist_id_entry = tk.Entry(root)
playlist_id_entry.pack()

recommendations_frame = tk.Frame(root)
recommendations_frame.pack()

get_recommendations_button = Button(root, text="Get Recommendations", command=display_recommendations)
get_recommendations_button.pack()

improved_recommendations_button = Button(root, text="Show Improved Recommendations", command=generate_improved_recommendations)
improved_recommendations_button.pack()

root.mainloop()