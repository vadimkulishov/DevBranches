from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QRadioButton, QButtonGroup,
                             QMessageBox, QGridLayout, QFrame, QGraphicsOpacityEffect, QProgressBar)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QSize, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
from frontend.views.auth_window import AuthWindow

class AnswerTile(QFrame):
    def __init__(self, text="", color="#3498db", parent=None):
        super().__init__(parent)
        self.text = text
        self.base_color = color
        self.is_selected = False
        self.is_animating = False

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self.opacity_effect)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Main answer text
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                min-height: 50px; /* Устанавливаем минимальную высоту для выравнивания текста */
            }
        """)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)  # Центрируем текст

        # Score label
        self.score_label = QLabel("")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
            }
        """)
        self.score_label.hide()
        layout.addWidget(self.score_label, alignment=Qt.AlignCenter)

        self.update_style()

        # Animations
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(300)
        self.scale_animation.setEasingCurve(QEasingCurve.OutBack)

        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(300)

    def update_style(self, is_correct=None):
        color = self.base_color
        if is_correct is not None:
            color = "#2ecc71" if is_correct else "#e74c3c"
            
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 15px;
                min-height: 195px;
                margin: 13px;
                border: none;
            }}
        """)
        
    def show_result(self, is_correct, points=None):
        self.update_style(is_correct)
        if is_correct and points is not None:
            self.score_label.setText(f"+{points} очков!")
            self.score_label.show()
            # Анимация появления очков
            score_opacity = QGraphicsOpacityEffect(self.score_label)
            self.score_label.setGraphicsEffect(score_opacity)
            score_anim = QPropertyAnimation(score_opacity, b"opacity")
            score_anim.setDuration(500)
            score_anim.setStartValue(0)
            score_anim.setEndValue(1)
            score_anim.start()
        
    def reset(self):
        self.update_style()
        self.score_label.hide()
        self.is_selected = False
        
    def play_pop_animation(self):
        if self.is_animating:
            return
            
        self.is_animating = True
        current_geometry = self.geometry()
        
        # Анимация масштабирования
        self.scale_animation.setStartValue(current_geometry)
        
        # Создаем немного больший прямоугольник для эффекта "надувания"
        expanded = current_geometry.adjusted(-10, -10, 10, 10)
        self.scale_animation.setKeyValueAt(0.5, expanded)
        self.scale_animation.setEndValue(current_geometry)
        
        # Анимация прозрачности
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setKeyValueAt(0.5, 0.7)
        self.opacity_animation.setEndValue(1.0)
        
        # Запускаем анимации
        self.scale_animation.start()
        self.opacity_animation.start()
        
        # Сброс флага анимации после завершения
        self.scale_animation.finished.connect(self.reset_animation)
        
    def reset_animation(self):
        self.is_animating = False
        
    def mousePressEvent(self, event):
        if isinstance(self.parent(), AnswersContainer):
            self.play_pop_animation()
            self.parent().tile_clicked(self)

class AnswersContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)
        
        # Create answer tiles
        self.answer_tiles = []
        colors = ["#3498db", "#16a085", "#f39c12", "#e74c3c"]
        for i in range(4):
            tile = AnswerTile(color=colors[i], parent=self)
            self.answer_tiles.append(tile)
            row = i // 2
            col = i % 2
            grid_layout.addWidget(tile, row, col)
        
        main_layout.addLayout(grid_layout)

    def tile_clicked(self, tile):
        # Deselect all tiles
        for t in self.answer_tiles:
            if t != tile:
                t.is_selected = False
        
        # Select clicked tile
        tile.is_selected = True
        if self.main_window:
            self.main_window.selected_answer = self.answer_tiles.index(tile)

    def show_result(self, selected_index, correct_index):
        is_correct = selected_index == correct_index
        points = 10 if is_correct else 0
        
        # Показываем результат на выбранной плитке
        self.answer_tiles[selected_index].show_result(is_correct, points if is_correct else None)
        
        # Если ответ неверный, показываем правильный ответ
        if not is_correct:
            self.answer_tiles[correct_index].show_result(True)
            
        # Делаем все остальные ответы серыми
        for i, tile in enumerate(self.answer_tiles):
            if i != selected_index and i != correct_index:
                tile.update_style(None)  # Сбрасываем стиль
                tile.setStyleSheet(f"""
                    AnswerTile {{
                        background-color: #95a5a6;
                        border-radius: 10px;
                        min-height: 150px;
                        margin: 10px;
                    }}
                    QLabel {{
                        color: white;
                        font-size: 18px;
                        font-weight: bold;
                    }}
                """)
            
        # Задержка перед следующим вопросом
        QTimer.singleShot(1500, self.reset_tiles)
            
    def reset_tiles(self):
        for tile in self.answer_tiles:
            tile.reset()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Quiz')
        self.setFixedSize(1040, 780)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.selected_answer = None
        self.current_user = None
        
        # Apply global dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QProgressBar {
                background-color: #333333;
                border: none;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
            }
            QLineEdit {
                background-color: #333333;
                color: white;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Create auth window
        self.auth_window = AuthWindow(self)
        self.auth_window.auth_successful.connect(self.handle_successful_auth)
        
        # Setup UI but don't show any windows
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Question banner
        question_container = QWidget()
        question_container.setStyleSheet("""
            QWidget {
                background-color: #2c001e;
            }
        """)
        question_container.setMinimumHeight(260)
        question_layout = QVBoxLayout(question_container)
        
        self.nickname_label = QLabel()
        self.nickname_label.setAlignment(Qt.AlignCenter)
        self.nickname_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 5px 15px;
            }
        """)
        question_layout.insertWidget(0, self.nickname_label)

        # Add a progress bar for remaining questions
        self.question_progress = QProgressBar()
        self.question_progress.setTextVisible(False)
        self.question_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444444;
                border-radius: 5px;
                background: #333333;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
                border-radius: 5px;
            }
        """)
        question_layout.insertWidget(0, self.question_progress)

        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 31px;
                padding: 26px;
            }
        """)
        question_layout.addWidget(self.question_label)
        main_layout.addWidget(question_container)

        # Add timer progress bar
        self.timer_progress = QProgressBar()
        self.timer_progress.setMaximum(20)  # 20 seconds
        self.timer_progress.setTextVisible(False)
        self.timer_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444444;
                border-radius: 5px;
                background: #333333;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #ff0000;
                border-radius: 5px;
            }
        """)
        question_layout.addWidget(self.timer_progress)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Answers container
        self.answers_container = AnswersContainer(self)
        main_layout.addWidget(self.answers_container)

    def start_timer(self):
        self.timer_progress.setValue(20)
        self.timer.start(1000)  # 1 second interval

    def update_timer(self):
        value = self.timer_progress.value()
        if value > 0:
            self.timer_progress.setValue(value - 1)
            # Dynamically update the gradient based on remaining time
            progress = value / self.timer_progress.maximum()
            self.timer_progress.setStyleSheet(f"""
                QProgressBar {{
                    border: 2px solid #2c001e;
                    border-radius: 5px;
                    background: #1a0012;
                }}
                QProgressBar::chunk {{
                    background: qlineargradient(
                        spread: pad, x1: 0, y1: 0.5, x2: 1, y2: 0.5,
                        stop: 0 green, stop: {progress} yellow, stop: 1 red
                    );
                }}
            """)
        else:
            self.timer.stop()
            self.handle_time_up()

    def handle_time_up(self):
        QMessageBox.warning(self, "Время вышло", "Вы не успели ответить на вопрос!")
        if hasattr(self, 'controller'):
            self.controller.next_question()

    def show_auth_window(self):
        self.hide()
        self.auth_window.show()

    def handle_successful_auth(self, username):
        self.current_user = username
        self.set_nickname(username)
        self.auth_window.hide()
        # Don't show main window here - let the controller handle it
        if hasattr(self, 'controller'):
            self.controller.start_quiz()

    def show_question(self, question, options):
        self.question_label.setText(question)
        self.selected_answer = None
        for tile, option in zip(self.answers_container.answer_tiles, options):
            # Escape HTML tags by replacing < and > with &lt; and &gt;
            escaped_option = option.replace('<', '&lt;').replace('>', '&gt;')
            tile.label.setText(escaped_option)
            tile.reset()

    def get_selected_answer(self):
        return self.selected_answer

    def show_answer_result(self, correct_answer):
        self.answers_container.show_result(self.selected_answer, correct_answer)

    def show_score(self, score):
        pass  # We'll show score in the final message only

    def show_result(self, is_correct):
        pass  # We'll skip the immediate feedback for this design

    def show_final_score(self, score, total):
        final_message = self.controller.model.get_final_message()
        self.result_window = QWidget()
        self.result_window.setStyleSheet("""
            QWidget {
                background-color: #2c001e;
            }
        """)
        self.result_window.setFixedSize(self.size())

        layout = QVBoxLayout(self.result_window)
        layout.setAlignment(Qt.AlignCenter)

        nickname_label = QLabel(f"Ваш никнейм: {self.current_user}")
        nickname_label.setAlignment(Qt.AlignCenter)
        nickname_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(nickname_label)

        score_label = QLabel(f"Ваш результат: {score} из {total}")
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(score_label)

        recommendation_label = QLabel("Рекомендации: Попробуйте улучшить свои знания в области, где вы допустили ошибки.")
        recommendation_label.setAlignment(Qt.AlignCenter)
        recommendation_label.setWordWrap(True)
        recommendation_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(recommendation_label)

        restart_button = QPushButton("Начать заново")
        restart_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        restart_button.clicked.connect(self.restart_game)
        layout.addWidget(restart_button)

        self.setCentralWidget(self.result_window)

    def restart_game(self):
        # Удаляем текущий центральный виджет
        current_widget = self.centralWidget()
        if current_widget:
            current_widget.deleteLater()

        # Пересоздаём интерфейс
        self.setup_ui()

        # Восстанавливаем никнейм после пересоздания интерфейса
        self.set_nickname(self.current_user)

        # Перезапускаем игру через контроллер
        self.controller.start_quiz()

    def set_nickname(self, nickname):
        self.nickname_label.setText(nickname)

    def update_question_progress(self, current, total):
        self.question_progress.setMaximum(total)
        self.question_progress.setValue(current)

    def handle_answer(self, answer_index):
        correct = self.quiz_model.check_answer(answer_index)

        if correct:
            self.answer_buttons[answer_index].setStyleSheet("background-color: green;")
        else:
            self.answer_buttons[answer_index].setStyleSheet("background-color: red;")

        if self.quiz_model.is_finished():
            QMessageBox.information(self, "Игра окончена", "Вы завершили викторину.")
            self.close()
        else:
            self.load_next_question()