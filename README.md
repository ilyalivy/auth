Auth Project

This project is a web application that enables user authentication and organization management. The backend is built using Flask and provides RESTful API endpoints for user and organization management operations. The frontend is built using React and provides a user interface for interacting with the backend services.

Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites

Ensure you have the following installed on your local machine:
Python 3.11
Node.js
Docker (Optional)

Backend Setup

Navigate to the project's backend directory.
Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required Python packages:
pip install -r requirements.txt
Create a .env file and specify your database URL and JWT secret key. Use the config.py file as a reference.
Set the FLASK_APP environment variable to point to your Flask application:
export FLASK_APP=app.py
Initialize your migrations folder with:
flask db init
Create a migration script: 
flask db migrate -m "Initial migration»
Run the database migrations:
flask db upgrade
Run the backend server:
flask run

Frontend Setup

Navigate to the project's frontend directory.
Install the required Node.js packages:
npm install
Start the frontend server:
npm start

Docker Setup (Optional)

Change localhost to host.docker.internal in .env
Build the Docker image:
docker build -t project-image .
Run the Docker container:
docker run -d -p 5000:5000 project-image 
(Perhaps the 1st port 5000 can be occupied by system tasks, in this case change it to 5001)

Running the Tests

To run the tests for the backend, navigate to the backend directory and run:
python -m unittest test_app.py

Usage

After setting up both the backend and frontend, navigate to http://localhost:3000 in your web browser to access the application. You can now sign up, sign in, create organizations, add users to organizations, and view a list of organizations and their users.

API Endpoints

The backend provides the following RESTful API endpoints:
/signup (POST): Sign up a new user.
/signin (POST): Sign in an existing user.
/create-org (POST): Create a new organization.
/add-user-to-org (POST): Add a user to an organization.
/list-users/<int:organization_id> (GET): List all users in an organization.
/list-orgs (GET): List all organizations.
/list-all-users (GET): List all users.

Built With

Backend:
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-Migrate
Flask-Cors
Frontend:
React
react-router-dom
axios
@mui/material
