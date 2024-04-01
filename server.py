from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Create a list to store feedback
feedback_data = []

@app.route('/')
def home():
    return render_template('index.html', feedback=feedback_data)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback = request.json
    feedback_data.append(feedback)
    return jsonify({'message': 'Feedback submitted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application