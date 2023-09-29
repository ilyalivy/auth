import unittest
from app import app, db, User, Organization
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

class AuthTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup(self):
        response = self.app.post('/signup', json={'email': 'test@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created!', response.data)

    def test_signin(self):
        hashed_password = generate_password_hash('password123', method='sha256')
        user = User(email='test@example.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()

        response = self.app.post('/signin', json={'email': 'test@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'access_token', response.data)

    def test_create_organization(self):
        with app.app_context():
            token = create_access_token('test@example.com')
            response = self.app.post('/create-org', json={'name': 'TechCorp'}, headers={'Authorization': f'Bearer {token}'})
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Organization created!', response.data)

    def test_add_user_to_org(self):
        with app.app_context():
            user = User(email='user1@example.com', password=generate_password_hash('password123', method='sha256'))
            org = Organization(name='TechCorp')
            db.session.add(user)
            db.session.add(org)
            db.session.commit()

            token = create_access_token('test@example.com')
            response = self.app.post('/add-user-to-org', json={'user_email': 'user1@example.com', 'name': 'TechCorp'}, headers={'Authorization': f'Bearer {token}'})
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Successfully added user to organization!', response.data)

if __name__ == '__main__':
    unittest.main()
