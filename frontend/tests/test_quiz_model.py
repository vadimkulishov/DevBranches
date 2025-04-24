from frontend.models.quiz_model import QuizModel

# Тест получения текущего вопроса
model = QuizModel()
model.questions = [
    {"question": "Question 1", "options": ["A", "B", "C", "D"], "correct_answer": 0},
    {"question": "Question 2", "options": ["A", "B", "C", "D"], "correct_answer": 1}
]

question = model.get_current_question()
assert question["question"] == "Question 1"

# Тест проверки правильного ответа
result = model.check_answer(0)
assert result is True
assert model.get_score() == 500

# Тест проверки неправильного ответа
result = model.check_answer(1)
assert result is False
assert model.score == 0

# Тест перехода к следующему вопросу
model.next_question()
question = model.get_current_question()
assert question["question"] == "Question 2"

# Тест завершения викторины
model.next_question()
assert model.is_finished() is True
