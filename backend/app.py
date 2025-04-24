from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Quiz questions
questions = [
    {
        'question': 'Какой язык программирования считается самым популярным в 2024 году?',
        'options': ['Java', 'Python', 'JavaScript', 'C++'],
        'correct_answer': 2  # JavaScript
    },
    {
        'question': 'Что выведет этот код на Python?\nprint(2 + 2 * 2)',
        'options': ['6', '8', '4', 'Ошибку'],
        'correct_answer': 0  # 6
    },
    {
        'question': 'Какой алгоритм сортировки самый быстрый в среднем случае?',
        'options': ['Пузырьковая сортировка', 'Сортировка вставками', 'Быстрая сортировка (QuickSort)', 'Сортировка выбором'],
        'correct_answer': 2  # QuickSort
    },
    {
        'question': 'Как называется ошибка "бесконечного цикла"?',
        'options': ['Infinite loop', 'Stack Overflow', 'Segmentation fault', 'SyntaxError'],
        'correct_answer': 0  # Infinite loop
    },
    {
        'question': 'Какой язык программирования создал Гвидо ван Россум?',
        'options': ['Ruby', 'Python', 'Perl', 'PHP'],
        'correct_answer': 1  # Python
    },
    {
        'question': 'Какой тег в HTML используется для создания ссылки?',
        'options': ['<div>', '<a>', '<link>', '<href>'],
        'correct_answer': 1  # <a>
    },
    {
        'question': 'Что такое "рекурсия"?',
        'options': ['Цикл for', 'Функция, вызывающая саму себя', 'Условный оператор', 'Тип данных'],
        'correct_answer': 1  # Функция, вызывающая саму себя
    },
    {
        'question': 'Какой из этих языков компилируется в байт-код для JVM?',
        'options': ['Python', 'Kotlin', 'JavaScript', 'C#'],
        'correct_answer': 1  # Kotlin
    },
    {
        'question': 'Какой командой в Git создаётся новая ветка?',
        'options': ['git commit', 'git push', 'git branch', 'git clone'],
        'correct_answer': 2  # git branch
    },
    {
        'question': 'Какой принцип ООП позволяет скрывать детали реализации?',
        'options': ['Наследование', 'Полиморфизм', 'Инкапсуляция', 'Абстракция'],
        'correct_answer': 2  # Инкапсуляция
    },
    {
        'question': 'Как называется система управления базами данных от Oracle?',
        'options': ['MySQL', 'PostgreSQL', 'Oracle Database', 'SQLite'],
        'correct_answer': 2  # Oracle Database
    },
    {
        'question': 'Какой метод HTTP используется для получения данных?',
        'options': ['POST', 'PUT', 'GET', 'DELETE'],
        'correct_answer': 2  # GET
    },
    {
        'question': 'Что делает оператор === в JavaScript?',
        'options': ['Сравнивает без приведения типов', 'Сравнивает значения и типы', 'Присваивает значение', 'Проверяет на null'],
        'correct_answer': 1  # Сравнивает значения и типы
    },
    {
        'question': 'Какой фреймворк НЕ используется для фронтенда?',
        'options': ['React', 'Angular', 'Vue.js', 'Django'],
        'correct_answer': 3  # Django
    },
    {
        'question': 'Какой язык программирования называют "языком веба"?',
        'options': ['Java', 'C#', 'JavaScript', 'Swift'],
        'correct_answer': 2  # JavaScript
    }
]

# Routes


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful'}), 200


@app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
