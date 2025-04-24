from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QStackedWidget, QMessageBox,
                             QGraphicsDropShadowEffect, QFrame, QApplication, QMainWindow)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect, QSize, QParallelAnimationGroup, pyqtSignal
from PyQt5.QtGui import (QFont, QColor, QPalette, QLinearGradient, QPainter,
                         QRadialGradient, QGradient, QPainterPath, QPixmap)
import math
from frontend.api import QuizAPI


class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(255, 255, 255, 0.4);
                background-color: rgba(255, 255, 255, 0.15);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
        """)


class StyledButton(QPushButton):
    def __init__(self, text, is_primary=True, parent=None):
        super().__init__(text, parent)
        self.is_primary = is_primary
        self.setup_ui()

    def setup_ui(self):
        if self.is_primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2c001e;
                    border: none;
                    border-radius: 15px;
                    color: white;
                    padding: 12px 25px;
                    font-size: 16px;
                    font-weight: bold;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #3a0026;
                }
                QPushButton:pressed {
                    background-color: #1a0012;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    color: white;
                    padding: 12px 25px;
                    font-size: 16px;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.05);
                }
            """)


class GradientBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.gradient = QLinearGradient(0, 0, 0, self.height())
        self.gradient.setColorAt(0, QColor("#2c001e"))
        self.gradient.setColorAt(1, QColor("#1a0012"))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gradient)
        self.timer.start(50)  # Обновление каждые 50 мс

        self.offset = 0

    def update_gradient(self):
        self.offset += 0.01
        if self.offset > 1:
            self.offset = 0

        self.gradient.setColorAt(0, QColor.fromHsvF(
            (self.offset + 0.0) % 1, 1, 0.5))
        self.gradient.setColorAt(1, QColor.fromHsvF(
            (self.offset + 0.5) % 1, 1, 0.5))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self.gradient)


class AuthWindow(QWidget):
    auth_successful = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = QuizAPI()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Авторизация')
        self.setFixedSize(1040, 780)
        self.setWindowFlags(Qt.Window)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #333333;
                color: white;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 5px;
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
        """)

        # Основной блок слева
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(50, 50, 50, 50)
        left_layout.setSpacing(30)

        # Title
        title = QLabel('Викторина')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        left_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel('Войдите в свой аккаунт')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 18px;
                margin-bottom: 40px;
            }
        """)
        left_layout.addWidget(subtitle)

        # Username field
        self.username_input = StyledLineEdit("Логин")
        left_layout.addWidget(self.username_input)

        # Password field
        self.password_input = StyledLineEdit("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        left_layout.addWidget(self.password_input)

        # Buttons container
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(15)

        # Login button
        self.login_button = StyledButton("Войти", True)
        self.login_button.clicked.connect(self.handle_login)
        buttons_layout.addWidget(self.login_button)

        # Register button
        self.register_button = StyledButton("Регистрация", False)
        self.register_button.clicked.connect(self.handle_register)
        buttons_layout.addWidget(self.register_button)

        left_layout.addWidget(buttons_container)
        left_layout.addStretch()

        # Анимация справа
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        animation_label = QLabel()
        animation_label.setAlignment(Qt.AlignCenter)
        animation_label.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: none;
            }
        """)
        animation_label.setPixmap(
            QPixmap("/path/to/your/animation.gif"))  # Укажите путь к анимации
        right_layout.addWidget(animation_label)

        # Основной макет
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(left_container, 1)
        main_layout.addWidget(right_container, 1)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.show_message(
                'Ошибка', 'Пожалуйста, введите логин и пароль', QMessageBox.Warning)
            return

        response, status_code = self.api.login(username, password)
        if status_code == 200:
            self.auth_successful.emit(username)
        else:
            self.show_message('Ошибка', response.get(
                'error', 'Неверный логин или пароль'), QMessageBox.Warning)

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.show_message(
                'Ошибка', 'Пожалуйста, введите логин и пароль', QMessageBox.Warning)
            return

        response, status_code = self.api.register(username, password)
        if status_code == 201:
            self.show_message(
                'Успех', 'Регистрация успешна! Теперь вы можете войти.', QMessageBox.Information)
        else:
            self.show_message('Ошибка', response.get(
                'error', 'Ошибка при регистрации'), QMessageBox.Warning)

    def show_message(self, title, message, icon):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c001e;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        msg.exec_()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
