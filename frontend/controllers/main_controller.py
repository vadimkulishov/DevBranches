from frontend.models.quiz_model import QuizModel
from frontend.views.main_window import MainWindow
from frontend.views.account_window import AccountWindow
from PyQt5.QtCore import QTimer
import requests


class MainController:
    def __init__(self):
        self.model = QuizModel()
        self.model.load_questions()  # Load questions at startup
        self.username = None  # Добавлено: хранение никнейма

        # Create main window but don't show it yet
        self.game_window = MainWindow(controller=self)
        self.game_window.controller = self

        # Setup timer
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.check_answer)

        # Connect auth signal and show auth window
        self.auth_window = self.game_window.auth_window
        self.game_window.auth_window.auth_successful.connect(
            self.on_auth_successful)
        self.game_window.auth_window.show()

        # Initialize account window attribute
        self.account_window = None

    def setup_connections(self):
        pass  # Moved connections setup to __init__

    def on_auth_successful(self, username):
        self.username = username  # Сохраняем никнейм
        if self.account_window is None or not self.account_window.isVisible():
            if self.account_window is None:
                self.account_window = AccountWindow(username, controller=self)
            self.auth_window.close()
            self.account_window.show()
        self.game_window.hide()

    def show_main_window(self):
        pass  # Теперь не нужно, так как окна управляются через on_auth_successful

    def start_quiz(self):
        self.model.reset_quiz()
        self.game_window.set_nickname(self.username)  # Устанавливаем никнейм
        self.show_next_question()

    def show_next_question(self):
        question = self.model.get_current_question()
        if question:
            self.game_window.show_question(
                question['question'], question['options'])
            # Обновляем прогресс вопросов при загрузке следующего вопроса
            self.game_window.update_question_progress(
                self.model.current_question_index + 1, len(self.model.questions))
        else:
            self.game_window.show_final_score(
                self.model.get_score(), len(self.model.questions))

    def update_user_progress(self, topic):
        url = "http://localhost:5001/api/update_progress"
        data = {"username": self.username, "topic": topic}
        try:
            requests.post(url, json=data)
        except Exception as e:
            print("Ошибка обновления прогресса:", e)

    def check_answer(self):
        selected_answer = self.game_window.get_selected_answer()
        if selected_answer is not None:
            current_question = self.model.get_current_question()
            if current_question is None:
                return  # Нет вопроса — ничего не делаем

            # Останавливаем таймер проверки
            self.timer.stop()

            # Показываем результат на плитках
            self.game_window.show_answer_result(
                current_question['correct_answer'])

            # Проверяем ответ
            is_correct = self.model.check_answer(selected_answer)
            if is_correct:
                self.update_user_progress(current_question['topic'])

            # Ждем немного и переходим к следующему вопросу
            QTimer.singleShot(1500, self.proceed_to_next)

    def proceed_to_next(self):
        if not self.model.next_question():
            self.game_window.show_final_score(
                self.model.get_score(), len(self.model.questions))
        else:
            self.show_next_question()
        self.timer.start()

    def start_quiz_by_topic(self, topic):
        self.model.load_questions_by_topic(topic)
        self.model.reset_quiz()
        self.game_window.set_nickname(self.username)  # Устанавливаем никнейм
        # Проверка: есть ли вопросы по теме
        if not self.model.questions:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self.game_window, "Ошибка", f"Нет вопросов по теме '{topic}'!")
            return
        self.show_next_question()
