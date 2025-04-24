import unittest
from ..app import app, db, User
from flask import json

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.app.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.get_data(as_text=True))

    def test_register_existing_user(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        response = self.app.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already exists', response.get_data(as_text=True))

    def test_login_user(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        response = self.app.post('/api/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.get_data(as_text=True))

    def test_login_invalid_user(self):
        response = self.app.post('/api/login', json={
            'username': 'invaliduser',
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid username or password', response.get_data(as_text=True))

    def test_get_questions(self):
        response = self.app.get('/api/questions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
