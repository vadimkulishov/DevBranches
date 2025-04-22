from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QRadioButton, QButtonGroup,
                             QMessageBox, QGridLayout, QFrame, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QSize, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor

class AnswerTile(QFrame):
    def __init__(self, text="", color="#3498db", parent=None):
        super().__init__(parent)
        self.text = text
        self.base_color = color
        self.is_selected = False
        self.is_animating = False
        
        # Создаем эффект прозрачности
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        
        layout = QVBoxLayout(self)
        
        # Основной текст ответа
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        
        # Метка для показа очков
        self.score_label = QLabel("")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.hide()
        layout.addWidget(self.score_label)
        
        self.update_style()
        
        # Анимации
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
            AnswerTile {{
                background-color: {color};
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
                padding: 20px;
            }
        """)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(20)
        
        # Create answer tiles
        self.answer_tiles = []
        colors = ["#3498db", "#16a085", "#f39c12", "#e74c3c"]
        for i in range(4):
            tile = AnswerTile(color=colors[i], parent=self)
            self.answer_tiles.append(tile)
            row = i // 2
            col = i % 2
            self.layout.addWidget(tile, row, col)

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
            
        # Задержка перед следующим вопросом
        QTimer.singleShot(1500, self.reset_tiles)
            
    def reset_tiles(self):
        for tile in self.answer_tiles:
            tile.reset()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Quiz')
        self.setMinimumSize(800, 600)
        self.selected_answer = None
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
                min-height: 200px;
            }
        """)
        question_layout = QVBoxLayout(question_container)
        
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                margin: 20px;
            }
        """)
        question_layout.addWidget(self.question_label)
        main_layout.addWidget(question_container)

        # Answers container
        self.answers_container = AnswersContainer(self)
        main_layout.addWidget(self.answers_container)

    def show_question(self, question, options):
        self.question_label.setText(question)
        self.selected_answer = None
        for tile, option in zip(self.answers_container.answer_tiles, options):
            tile.label.setText(option)
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
        msg = QMessageBox()
        msg.setWindowTitle('Game Over')
        msg.setText(f'Your score: {score} out of {total}')
        msg.setIcon(QMessageBox.Information)
        msg.exec_() 