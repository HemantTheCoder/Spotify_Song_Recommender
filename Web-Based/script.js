async function getRecommendations() {
    const username = document.getElementById("username").value;
    const playlistId = document.getElementById("playlist_id").value;

    try {
        const response = await fetch(`http://localhost:5000/recommendations?username=${username}&playlist_id=${playlistId}`);
        const data = await response.json();
        displayRecommendations(data.recommended_songs);
    } catch (error) {
        console.error("Error fetching recommendations:", error);
    }
}

async function submitFeedback() {
    const username = document.getElementById("username").value;
    const playlistId = document.getElementById("playlist_id").value;
    const feedbackData = [];

    document.querySelectorAll('input[name="feedback"]').forEach((input, index) => {
        feedbackData.push({
            song_name: input.dataset.songName,
            feedback: input.checked ? 1 : 0
        });
    });

    try {
        const response = await fetch('http://localhost:5000/submit_feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, playlist_id: playlistId, feedback_data: feedbackData })
        });
        if (response.ok) {
            alert("Feedback submitted successfully!");
        } else {
            alert("Failed to submit feedback!");
        }
    } catch (error) {
        console.error("Error submitting feedback:", error);
    }
}

function displayRecommendations(recommendedSongs) {
    const recommendationsDiv = document.getElementById("recommendations");
    recommendationsDiv.innerHTML = "";

    recommendedSongs.forEach((song, index) => {
        const songDiv = document.createElement("div");
        songDiv.textContent = song[0];

        const likeRadio = document.createElement("input");
        likeRadio.type = "radio";
        likeRadio.name = "feedback";
        likeRadio.dataset.songName = song[0];
        likeRadio.value = "like";
        songDiv.appendChild(likeRadio);

        const dislikeRadio = document.createElement("input");
        dislikeRadio.type = "radio";
        dislikeRadio.name = "feedback";
        dislikeRadio.dataset.songName = song[0];
        dislikeRadio.value = "dislike";
        songDiv.appendChild(dislikeRadio);

        recommendationsDiv.appendChild(songDiv);
    });
}
