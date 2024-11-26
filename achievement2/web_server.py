import requests
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

APPLICATION_SERVER_URL = "http://127.0.0.1:5001/process"

@app.route('/process', methods=['POST'])
def process_request():
    data = request.get_json()

    if not data or 'number' not in data:
        return jsonify({'error': 'No number provided'}), 400
    
    if not isinstance(data['number'], int) and data['number'] > 0:
        return jsonify({'error': 'Invalid number. Must be a positive integer.'}), 400

    try:
        response = requests.post(APPLICATION_SERVER_URL, json=data)
        return jsonify(response.json()), response.status_code

    except requests.ConnectionError:
        return jsonify({'error': 'Unable to connect to the application server.'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
