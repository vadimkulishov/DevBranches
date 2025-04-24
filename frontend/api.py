import requests


class QuizAPI:
    def __init__(self, base_url='http://localhost:5001'):
        self.base_url = base_url

    def register(self, username, password):
        response = requests.post(
            f'{self.base_url}/api/register',
            json={'username': username, 'password': password}
        )
        return response.json(), response.status_code

    def login(self, username, password):
        response = requests.post(
            f'{self.base_url}/api/login',
            json={'username': username, 'password': password}
        )
        return response.json(), response.status_code

    def get_questions(self):
        response = requests.get(f'{self.base_url}/api/questions')
        return response.json(), response.status_code
