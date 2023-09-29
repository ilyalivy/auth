from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
# config data from config.py
from config import Config
# migrate
from flask_migrate import Migrate
import re
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask_cors import CORS


# create the app
app = Flask(__name__)
CORS(app)

# from config file
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI']
app.config['JWT_SECRET_KEY']
# disables a feature that automatically tracks modifications to objects and emits signals 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

migrate = Migrate(app, db)

jwt = JWTManager(app)

# class represent a table in database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)  # Changed from username to email
    password = db.Column(db.String(1000), nullable=False) #hashed password, length increased from 80 to 1000
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='organization', lazy=True)

def validate_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email) is not None

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data['email']

    if not validate_email(email):
        return jsonify({"message": "Invalid email format."}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(email=email, password=hashed_password)  # Modified here

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if 'unique constraint' in str(e.orig).lower():
            return jsonify({"message": "Email already exists."}), 400
        else:
            return jsonify({"message": "An error occurred while creating the user."}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An unknown error occurred: {str(e)}"}), 500

    return jsonify({"message": "User created!"}), 201

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data['email']

    if not validate_email(email):
        return jsonify({"message": "Invalid email format."}), 400

    user = User.query.filter_by(email=email).first()  # Modified here
    # tests log
    print("Req data =>", data)
    print("DB query user", user)
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials."}), 401
    access_token = create_access_token(identity=user.email)  # Use email as identity
    return jsonify({"access_token": access_token})

@app.route('/create-org', methods=['POST'])
@jwt_required
def create_organization():
    data = request.get_json()

    if not data.get('name'):
        return jsonify({"message": "Organization name cannot be empty."}), 400
    
    new_organization = Organization(name=data['name'])
    db.session.add(new_organization)
    db.session.commit()

    try:
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        if 'unique constraint' in str(e.orig).lower():
            return jsonify({"message": "Organization name already exists."}), 400
        else:
            return jsonify({"message": "An error occurred while creating the organization."}), 500
        
    except InvalidRequestError as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the organization."}), 500
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An unknown error occurred."}), 500

    return jsonify({"message": "Organization created!"}), 201

@app.route('/add-user-to-org', methods=['POST'])
@jwt_required
def add_user_to_org():
    try:
        data = request.get_json()

        user_email_to_add = data.get('user_email')
        organization_name = data.get('name')

        if not user_email_to_add or not organization_name:
            return jsonify({"error": "User email and organization name are required."}), 400

        organization = Organization.query.filter_by(name=organization_name).first()
        if not organization:
            return jsonify({"error": "Organization not found."}), 404

        user_to_add = User.query.filter_by(email=user_email_to_add).first()

        if not user_to_add:
            return jsonify({"error": "User with the provided email not found."}), 404

        if user_to_add.organization_id == organization.id:
            return jsonify({"error": "User already added to this organization."}), 400
        else:
            user_to_add.organization_id = organization.id
            db.session.commit()
            return jsonify({"message": "Successfully added user to organization!"}), 201

    except KeyError:
        return jsonify({"message": "Invalid data provided."}), 400
    except Exception as e:
        app.logger.error(f"Error while adding user to organization: {e}")
        return jsonify({"message": "Internal server error. Please try again later."}), 500


if __name__ == '__main__':
    app.run(debug=True)