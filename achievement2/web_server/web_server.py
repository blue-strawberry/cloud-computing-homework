import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

APPLICATION_SERVER_URL = os.getenv("APPLICATION_SERVER_URL", "http://application_server:5001/process")
# APPLICATION_SERVER_URL = "http://127.0.0.1:5001/process"

@app.route('/process', methods=['POST'])
def process_request():
    data = request.get_json()

    if not data or 'number' not in data:
        return jsonify({'error': 'No number provided'}), 400

    try:
        number = int(data['number'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid number. Must be a positive integer.'}), 400

    if number <= 0:
        return jsonify({'error': 'Invalid number. Must be a positive integer.'}), 400

    try:
        response = requests.post(APPLICATION_SERVER_URL, json={'number': number})
        return jsonify(response.json()), response.status_code
    except requests.ConnectionError:
        return jsonify({'error': 'Unable to connect to the application server.'}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
