from flask import Flask, request, jsonify
import logging
from db_utils import initialize_database, save_number_to_db, is_unprocessed_number

logging.basicConfig(
    filename='application_server.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)




initialize_database()

def is_valid_number(number):
    """Check if the number is a valid positive integer."""
    return isinstance(number, int) and number > 0

@app.route('/process', methods=['POST'])
def process_number():
    """Process a number and save it to the database."""
    data = request.get_json()

    if not data or 'number' not in data:
        logging.error("No number provided in request.")
        return jsonify({'error': 'No number provided'}), 400

    number = data['number']

    if not is_valid_number(number):
        logging.error(f"Invalid number provided: {number}")
        return jsonify({'error': 'Invalid number. Must be a positive integer.'}), 400

    try:
        if not is_unprocessed_number(number):
            logging.warning(f"Number {number} has already been processed.")
            return jsonify({'error': 'Number has already been processed.'}), 400

        if not is_unprocessed_number(number + 1):
            logging.warning(f"Number {number} + 1 ({number + 1}) has already been processed.")
            return jsonify({'error': f'Number {number} + 1 ({number + 1}) has already been processed.'}), 400

        save_number_to_db(number)

        return jsonify({'incrementedNumber': number + 1})

    except Exception as e:
        logging.error(f"Error processing number: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
