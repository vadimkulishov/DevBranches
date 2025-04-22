from models.quiz_model import QuizModel
from views.main_window import MainWindow
from PyQt5.QtCore import QTimer

class MainController:
    def __init__(self):
        self.model = QuizModel()
        self.view = MainWindow()
        self.setup_connections()
        self.start_quiz()

    def setup_connections(self):
        self.model.load_questions()
        # Setup timer to check for answers
        self.timer = QTimer()
        self.timer.setInterval(100)  # Check every 100ms
        self.timer.timeout.connect(self.check_answer)
        self.timer.start()

    def show_main_window(self):
        self.view.show()

    def start_quiz(self):
        self.model.reset_quiz()
        self.show_next_question()

    def show_next_question(self):
        question = self.model.get_current_question()
        if question:
            self.view.show_question(question['question'], question['options'])
        else:
            self.view.show_final_score(self.model.get_score(), len(self.model.questions))
            self.start_quiz()

    def check_answer(self):
        selected_answer = self.view.get_selected_answer()
        if selected_answer is not None:
            current_question = self.model.get_current_question()
            
            # Останавливаем таймер проверки
            self.timer.stop()
            
            # Показываем результат на плитках
            self.view.show_answer_result(current_question['correct_answer'])
            
            # Проверяем ответ
            self.model.check_answer(selected_answer)
            
            # Ждем немного и переходим к следующему вопросу
            QTimer.singleShot(1500, self.proceed_to_next)

    def proceed_to_next(self):
        if not self.model.next_question():
            self.view.show_final_score(self.model.get_score(), len(self.model.questions))
            self.start_quiz()
        else:
            self.show_next_question()
        self.timer.start() 