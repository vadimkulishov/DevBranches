from app import app
from flask import json

# Тест регистрации пользователя
client = app.test_client()
response = client.post('/api/register', json={
    'username': 'testuser',
    'password': 'testpassword'
})
assert response.status_code == 201
assert 'User registered successfully' in response.get_data(as_text=True)

# Тест авторизации пользователя
response = client.post('/api/login', json={
    'username': 'testuser',
    'password': 'testpassword'
})
assert response.status_code == 200
assert 'Login successful' in response.get_data(as_text=True)

# Тест получения вопросов
response = client.get('/api/questions')
assert response.status_code == 200
data = json.loads(response.get_data(as_text=True))
assert isinstance(data, list)
assert len(data) > 0
