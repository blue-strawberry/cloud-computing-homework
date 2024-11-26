# Number Processing Service

This project is a simple web-based number processing system, logically divided into a **web server** and an **application server**. The system processes natural numbers with specific validation rules and logs all activities.

---

## Features

1. **Web Server**:
   - Accepts HTTP POST requests from clients.
   - Forwards requests to the application server.
   - Returns processed responses to the client.

2. **Application Server**:
   - Validates numbers based on specific rules:
     - Numbers must be positive integers.
     - Numbers must not have been processed before.
     - Numbers `N-1` must not already exist in the database.
   - Interacts with an SQLite database to store and verify processed numbers.

3. **Database**:
   - Uses SQLite to store processed numbers locally.

4. **Logging**:
   - Logs application server activities (successes and errors) into `application_server.log`.

---

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Requests (for the web server)

---

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd number-processing-service
   ```

2. Install dependencies:
   ```
   pip install flask flask-sqlalchemy requests
   ```

---

## Usage

1. Start the Web Server:
   ```
    python web_server.py
   ```
*Runs on http://127.0.0.1:5000

2. Start the Application Server:
   ```
    python application_server.py
   ```
*Runs on http://127.0.0.1:5001

3. Send a number:
   ```
    curl -X POST -H "Content-Type: application/json" -d '{"number": 5}' http://127.0.0.1:5000/process
   ```
 