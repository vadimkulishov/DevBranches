from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

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
    progress = db.Column(db.Text, default='{}')  # Новое поле для прогресса

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_progress(self):
        try:
            return json.loads(self.progress)
        except Exception:
            return {}

    def set_progress(self, progress_dict):
        self.progress = json.dumps(progress_dict)


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
    topic = request.args.get('topic')
    if topic:
        questions = Question.query.filter_by(topic=topic).all()
    else:
        questions = Question.query.all()
    result = []
    for q in questions:
        result.append({
            'id': q.id,
            'topic': q.topic,
            'question': q.question,
            'options': q.get_options(),
            'correct_answer': q.correct_answer
        })
    return jsonify(result)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(80), nullable=False)
    question = db.Column(db.String(512), nullable=False)
    options = db.Column(db.Text, nullable=False)  # Храним как JSON-строку
    correct_answer = db.Column(db.Integer, nullable=False)

    def set_options(self, options_list):
        self.options = json.dumps(options_list)

    def get_options(self):
        return json.loads(self.options)


@app.route('/api/update_progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    username = data.get('username')
    topic = data.get('topic')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    progress = user.get_progress()
    progress[topic] = progress.get(topic, 0) + 1
    user.set_progress(progress)
    db.session.commit()
    return jsonify({'message': 'Progress updated'}), 200


@app.route('/api/user_progress', methods=['GET'])
def user_progress():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.get_progress()), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Проверяем, есть ли поле progress в таблице user, если нет — добавляем
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('user')]
        if 'progress' not in columns:
            try:
                db.session.execute(text("ALTER TABLE user ADD COLUMN progress TEXT DEFAULT '{}'"))
                db.session.commit()
                print("Поле progress успешно добавлено в таблицу user.")
            except Exception as e:
                print("Ошибка при добавлении поля progress:", e)
    app.run(debug=True, port=5001)
