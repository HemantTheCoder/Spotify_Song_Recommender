const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const app = express();
const port = 5000;

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/song_feedback_db', { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;

// Define a schema for the feedback data
const feedbackSchema = new mongoose.Schema({
    username: String,
    playlist_id: String,
    feedback_data: [{
        songName: String,
        feedbackValue: String
    }]
});

// Create a model for the feedback data
const Feedback = mongoose.model('Feedback', feedbackSchema);

// Middleware to parse JSON requests
app.use(bodyParser.json());

// Route handler for submitting feedback
app.post('/submit_feedback', (req, res) => {
    const { username, playlist_id, feedback_data } = req.body;

    // Create a new Feedback document
    const feedback = new Feedback({
        username: username,
        playlist_id: playlist_id,
        feedback_data: feedback_data
    });

    // Save the feedback to the database
    feedback.save((err, savedFeedback) => {
        if (err) {
            console.error('Error saving feedback:', err);
            res.status(500).send('Error saving feedback');
        } else {
            console.log('Feedback saved successfully:', savedFeedback);
            res.status(200).send('Feedback saved successfully');
        }
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
