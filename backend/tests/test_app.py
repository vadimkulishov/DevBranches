from backend.app import app, db, User
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))


class BackendTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        response = self.app.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully',
                      response.get_data(as_text=True))

    def test_login_user(self):
        with app.app_context():
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

    def test_get_questions(self):
        response = self.app.get('/api/questions')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)


if __name__ == '__main__':
    unittest.main()
