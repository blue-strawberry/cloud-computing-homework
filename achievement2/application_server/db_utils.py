import psycopg2
import logging
import os

logging.basicConfig(
    filename='application_server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# DB_CONFIG = {
#     "dbname": "numbers_db",
#     "user": "student20",
#     "password": "student20",
#     "host": "localhost",
#     "port": 5432
# }
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "numbers_db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logging.info("Database connection established.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise

def initialize_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_numbers (
                id SERIAL PRIMARY KEY,
                number INTEGER UNIQUE NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing the database: {e}")
        raise

def save_number_to_db(number):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO processed_numbers (number) VALUES (%s);", (number,))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Number {number} saved to the database.")
    except psycopg2.IntegrityError:
        logging.warning(f"Number {number} is already in the database.")
    except Exception as e:
        logging.error(f"Error saving number {number}: {e}")
        raise

def is_unprocessed_number(number):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM processed_numbers WHERE number = %s;", (number,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is None
    except Exception as e:
        logging.error(f"Error checking if number {number} is unprocessed: {e}")
        raise
