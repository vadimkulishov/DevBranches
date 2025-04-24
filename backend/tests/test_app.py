import unittest
from backend.app import app, db
from flask import json

class TestApp(unittest.TestCase):

    def setUp(self):
        # Configure app for testing with in-memory SQLite
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        # Recreate database schema before each test
        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_register_user(self):
        response = self.client.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.get_data(as_text=True))

    def test_login_user(self):
        # Ensure user is registered first
        self.client.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.client.post('/api/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.get_data(as_text=True))

    def test_get_questions(self):
        response = self.client.get('/api/questions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
