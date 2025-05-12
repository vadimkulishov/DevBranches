import sys
import os
import unittest
import json

# Добавляем корень проекта в sys.path для корректного импорта backend.app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app import app, db, User, Question

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Добавим тестовый вопрос
            q = Question(topic='Python', question='2+2?', options=json.dumps(['3','4','5','6']), correct_answer=1)
            db.session.add(q)
            db.session.commit()

    def register(self, username, password):
        return self.client.post('/api/register', json={
            'username': username,
            'password': password
        })

    def login(self, username, password):
        return self.client.post('/api/login', json={
            'username': username,
            'password': password
        })

    def test_register_success(self):
        resp = self.register('user1', 'pass1')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('User registered successfully', resp.get_data(as_text=True))

    def test_register_missing_fields(self):
        resp = self.client.post('/api/register', json={'username': 'user2'})
        self.assertEqual(resp.status_code, 400)
        resp = self.client.post('/api/register', json={'password': 'pass2'})
        self.assertEqual(resp.status_code, 400)

    def test_register_duplicate(self):
        self.register('user3', 'pass3')
        resp = self.register('user3', 'pass3')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Username already exists', resp.get_data(as_text=True))

    def test_login_success(self):
        self.register('user4', 'pass4')
        resp = self.login('user4', 'pass4')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Login successful', resp.get_data(as_text=True))

    def test_login_wrong_password(self):
        self.register('user5', 'pass5')
        resp = self.login('user5', 'wrong')
        self.assertEqual(resp.status_code, 401)

    def test_login_no_user(self):
        resp = self.login('nouser', 'nopass')
        self.assertEqual(resp.status_code, 401)

    def test_get_questions(self):
        resp = self.client.get('/api/questions')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.get_data(as_text=True))
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_questions_by_topic(self):
        resp = self.client.get('/api/questions?topic=Python')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.get_data(as_text=True))
        self.assertTrue(all(q['topic'] == 'Python' for q in data))

    def test_update_and_get_progress(self):
        self.register('user6', 'pass6')
        # Прогресс до обновления
        resp = self.client.get('/api/user_progress?username=user6')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.get_data(as_text=True)), {})
        # Обновляем прогресс
        resp = self.client.post('/api/update_progress', json={'username': 'user6', 'topic': 'Python'})
        self.assertEqual(resp.status_code, 200)
        # Проверяем прогресс
        resp = self.client.get('/api/user_progress?username=user6')
        self.assertEqual(resp.status_code, 200)
        progress = json.loads(resp.get_data(as_text=True))
        self.assertEqual(progress.get('Python'), 1)

    def test_update_progress_no_user(self):
        resp = self.client.post('/api/update_progress', json={'username': 'nouser', 'topic': 'Python'})
        self.assertEqual(resp.status_code, 404)

    def test_get_progress_no_user(self):
        resp = self.client.get('/api/user_progress?username=nouser')
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
