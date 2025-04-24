from frontend.api import QuizAPI

class QuizModel:
    def __init__(self):
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.api = QuizAPI()

    def load_questions(self):
        response, status_code = self.api.get_questions()
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
            return True
        return False

    def next_question(self):
        self.current_question_index += 1
        return self.current_question_index < len(self.questions)

    def get_score(self):
        return self.score

    def reset_quiz(self):
        self.current_question_index = 0
        self.score = 0

    def get_final_message(self):
        if self.score >= 4000:
            return "Отличный результат! Вы настоящий эксперт!"
        elif self.score >= 2000:
            return "Хороший результат! Но есть куда расти."
        else:
            return "Попробуйте еще раз! Вы можете лучше!"