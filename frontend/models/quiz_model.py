from frontend.api import QuizAPI


class QuizModel:
    def __init__(self):
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.correct_count = 0
        self.api = QuizAPI()

    def load_questions(self):
        response, status_code = self.api.get_questions()
        if status_code == 200:
            self.questions = response
        else:
            self.questions = []

    def load_questions_by_topic(self, topic):
        response, status_code = self.api.get_questions_by_topic(topic)
        if status_code == 200:
            self.questions = response
        else:
            self.questions = []

    def get_current_question(self):
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, answer_index):
        current_question = self.get_current_question()
        if current_question and answer_index == current_question['correct_answer']:
            self.score += 1
            self.correct_count += 1
            return True
        return False

    def next_question(self):
        self.current_question_index += 1
        return self.current_question_index < len(self.questions)

    def is_finished(self):
        return self.current_question_index >= len(self.questions)

    def get_score(self):
        return self.correct_count

    def get_total_questions(self):
        return len(self.questions)

    def reset_quiz(self):
        self.current_question_index = 0
        self.score = 0
        self.correct_count = 0

    def get_final_message(self):
        total = self.get_total_questions()
        if total == 0:
            return "Нет вопросов для оценки."
        percent = (self.correct_count / total) * 100
        if percent >= 90:
            return "Отлично! Вы настоящий эксперт!"
        elif percent >= 70:
            return "Хороший результат! Но есть куда расти."
        elif percent >= 40:
            return "Неплохо, но стоит повторить материал."
        else:
            return "Попробуйте еще раз! Вы можете лучше!"
