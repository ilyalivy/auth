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

        with app.app_context():
            org1 = Organization(name='Org 1')
            org2 = Organization(name='Org 2')
            db.session.add(org1)
            db.session.add(org2)
            db.session.commit()

            user1 = User(email='user1@example.com', password=generate_password_hash('password123', method='sha256'), organization_id=org1.id)
            user2 = User(email='user2@example.com', password=generate_password_hash('password123', method='sha256'), organization_id=org2.id)
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

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
            user = User(email='user@example.com', password=generate_password_hash('password123', method='sha256'))
            org = Organization(name='TechCorp')
            db.session.add(user)
            db.session.add(org)
            db.session.commit()

            token = create_access_token('test@example.com')
            response = self.app.post('/add-user-to-org', json={'user_email': 'user@example.com', 'name': 'TechCorp'}, headers={'Authorization': f'Bearer {token}'})
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Successfully added user to organization!', response.data)

    def test_list_organizations(self):
        with app.app_context():
            token = create_access_token('test@example.com')
            response = self.app.get('/list-orgs', headers={'Authorization': f'Bearer {token}'})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIsInstance(data, dict)
            self.assertIn('organizations', data)
            organizations = data['organizations']
            self.assertIsInstance(organizations, list)
            self.assertGreaterEqual(len(organizations), 2)

    def test_list_users_all(self):
        with app.app_context():
            token = create_access_token('test@example.com')
            response = self.app.get('/list-all-users', headers={'Authorization': f'Bearer {token}'})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIsInstance(data, dict)
            self.assertIn('users', data)
            users = data['users']
            self.assertIsInstance(users, list)
            self.assertGreaterEqual(len(users), 2)

if __name__ == '__main__':
    unittest.main()
