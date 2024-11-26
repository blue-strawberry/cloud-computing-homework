from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(
    filename='application_server.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///numbers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ProcessedNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)

with app.app_context():
    db.create_all()

def is_valid_number(number):
    return isinstance(number, int) and number > 0

def is_unprocessed_number(number):
    return not ProcessedNumber.query.filter_by(number=number).first()

def save_number_to_db(number):
    new_number = ProcessedNumber(number=number)
    db.session.add(new_number)
    db.session.commit()
    logging.info(f'Number {number} saved to database.')

@app.route('/process', methods=['POST'])
def process_number():
    data = request.get_json()

    if not data or 'number' not in data:
        logging.error('No number provided in request.')
        return jsonify({'error': 'No number provided'}), 400

    number = data['number']

    if not is_valid_number(number):
        logging.error(f'Invalid number provided: {number}')
        return jsonify({'error': 'Invalid number. Must be a positive integer.'}), 400

    try:
        if not is_unprocessed_number(number):
            logging.warning(f'Number {number} has already been processed.')
            return jsonify({'error': 'Number has already been processed.'}), 400

        if not is_unprocessed_number(number - 1):
            logging.warning(f'Number {number} - 1 ({number - 1}) has already been processed.')
            return jsonify({'error': f'Number {number} - 1 ({number - 1}) has already been processed.'}), 400

        save_number_to_db(number)

        return jsonify({'incrementedNumber': number + 1})

    except Exception as e:
        logging.error(f'Database error: {str(e)}')
        return jsonify({'error': 'Internal server error.'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
