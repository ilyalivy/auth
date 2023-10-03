# Auth Project

This project is a web application that enables user authentication and organization management. The backend is built using Flask and provides RESTful API endpoints for user and organization management operations. The frontend is built using React and provides a user interface for interacting with the backend services.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed on your local machine:
- Python 3.11
- Node.js
- Docker (Optional)

## Backend Setup

1. Navigate to the project's backend directory.
2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file and specify your database URL and JWT secret key. Use the `config.py` file as a reference.
5. Set the `FLASK_APP` environment variable to point to your Flask application:
    ```bash
    export FLASK_APP=app.py
    ```
6. Initialize your migrations folder with:
    ```bash
    flask db init
    ```
7. Create a migration script: 
    ```bash
    flask db migrate -m "Initial migration"
    ```
8. Run the database migrations:
    ```bash
    flask db upgrade
    ```
9. Run the backend server:
    ```bash
    flask run
    ```

## Frontend Setup

1. Navigate to the project's frontend directory.
2. Install the required Node.js packages:
    ```bash
    npm install
    ```
3. Start the frontend server:
    ```bash
    npm start
    ```

## Docker Setup (Optional)

1. Change `localhost` to `host.docker.internal` in `.env`.
2. Build the Docker image:
    ```bash
    docker build -t project-image .
    ```
3. Run the Docker container:
    ```bash
    docker run -d -p 5000:5000 project-image 
    ```
    (Perhaps the 1st port `5000` can be occupied by system tasks, in this case change it to `5001`)

## Running the Tests

To run the tests for the backend, navigate to the backend directory and run:
```bash
python -m unittest test_app.py
```

## Usage

After setting up both the backend and frontend, navigate to http://localhost:3000 in your web browser to access the application. You can now sign up, sign in, create organizations, add users to organizations, and view a list of organizations and their users.

## API Endpoints

The backend provides the following RESTful API endpoints:

- `/signup` (POST): Sign up a new user.
- `/signin` (POST): Sign in an existing user.
- `/create-org` (POST): Create a new organization.
- `/add-user-to-org` (POST): Add a user to an organization.
- `/list-users/<int:organization_id>` (GET): List all users in an organization.
- `/list-orgs` (GET): List all organizations.
- `/list-all-users` (GET): List all users.

## Built With

### Backend:
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Migrate
- Flask-Cors

### Frontend:
- React
- react-router-dom
- axios
- @mui/material
