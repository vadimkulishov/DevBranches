from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QStackedWidget, QMessageBox,
                             QGraphicsDropShadowEffect, QFrame, QApplication, QMainWindow)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect, QSize, QParallelAnimationGroup, pyqtSignal
from PyQt5.QtGui import (QFont, QColor, QPalette, QLinearGradient, QPainter, 
                        QRadialGradient, QGradient, QPainterPath)
import math

class AnimatedGradientBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gradient)
        self.timer.start(50)  # Update every 50ms
        
    def update_gradient(self):
        self.angle = (self.angle + 2) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        
        # Calculate gradient points based on angle
        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = math.sqrt(center_x**2 + center_y**2)
        
        start_x = center_x + radius * math.cos(math.radians(self.angle))
        start_y = center_y + radius * math.sin(math.radians(self.angle))
        end_x = center_x + radius * math.cos(math.radians(self.angle + 180))
        end_y = center_y + radius * math.sin(math.radians(self.angle + 180))
        
        gradient.setStart(start_x, start_y)
        gradient.setFinalStop(end_x, end_y)
        
        # Add colors
        gradient.setColorAt(0, QColor(108, 92, 231))    # Purple
        gradient.setColorAt(0.5, QColor(46, 134, 222))  # Blue
        gradient.setColorAt(1, QColor(0, 206, 201))     # Cyan
        
        # Fill background
        painter.fillRect(0, 0, self.width(), self.height(), gradient)

class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                color: white;
                padding: 13px 20px;
                font-size: 18px;
                min-height: 26px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(255, 255, 255, 0.3);
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
                    background-color: #6c5ce7;
                    border: none;
                    border-radius: 20px;
                    color: white;
                    padding: 13px 26px;
                    font-size: 18px;
                    font-weight: bold;
                    min-width: 156px;
                }
                QPushButton:hover {
                    background-color: #8075e9;
                }
                QPushButton:pressed {
                    background-color: #5849e5;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    border-radius: 20px;
                    color: white;
                    padding: 13px 26px;
                    font-size: 18px;
                    min-width: 156px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.05);
                }
            """)

class LoginScreen(QWidget):
    auth_successful = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(52, 52, 52, 52)
        main_layout.setSpacing(26)

        # Add logo or title
        title_label = QLabel("Welcome Back")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 42px;
                font-weight: bold;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("Please sign in to continue")
        subtitle_label.setStyleSheet("QLabel { color: rgba(255, 255, 255, 0.7); font-size: 21px; }")
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        main_layout.addSpacing(39)

        # Create form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        # Username field
        self.username_edit = StyledLineEdit("Username")
        form_layout.addWidget(self.username_edit)

        # Password field
        self.password_edit = StyledLineEdit("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_edit)

        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)

        # Login button
        self.login_button = StyledButton("Sign In", is_primary=True)
        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button)

        # Register button
        self.register_button = StyledButton("Create Account", is_primary=False)
        self.register_button.clicked.connect(self.handle_register)
        main_layout.addWidget(self.register_button)

        main_layout.addStretch()

    def handle_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        
        if not username or not password:
            QMessageBox.warning(
                self,
                "Error",
                "Please fill in all fields",
                QMessageBox.Ok
            )
            return
            
        # Временно для тестирования пропускаем любые непустые логин/пароль
        self.auth_successful.emit(username)

    def handle_register(self):
        QMessageBox.information(
            self,
            "Registration",
            "Registration functionality will be implemented soon!",
            QMessageBox.Ok
        )

class RegisterScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Заголовок
        title = QLabel("Регистрация")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title)
        
        # Поля ввода
        self.username = StyledLineEdit("Имя пользователя")
        layout.addWidget(self.username)
        
        self.password = StyledLineEdit("Пароль")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        self.confirm_password = StyledLineEdit("Подтвердите пароль")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        register_button = StyledButton("Зарегистрироваться", True)
        register_button.clicked.connect(self.handle_register)
        buttons_layout.addWidget(register_button)
        
        login_button = StyledButton("Вернуться ко входу", False)
        login_button.clicked.connect(lambda: self.parent().switch_screen(0))
        buttons_layout.addWidget(login_button)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
    def handle_register(self):
        username = self.username.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()
        
        if not username or not password or not confirm_password:
            self.parent().show_error("Пожалуйста, заполните все поля")
            return
            
        if password != confirm_password:
            self.parent().show_error("Пароли не совпадают")
            return
            
        self.parent().show_success("Регистрация успешна! Теперь вы можете войти.")
        self.parent().switch_screen(0)

class AuthWindow(QMainWindow):
    auth_successful = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Authorization")
        self.setFixedSize(650, 780)
        
        # Set window flags to prevent resizing and remove maximize button
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.MSWindowsFixedSizeDialogHint)
        
        # Center window on screen
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        # Create central widget with animated background
        central_widget = AnimatedGradientBackground(self)
        self.setCentralWidget(central_widget)

        # Create login screen
        self.login_screen = LoginScreen(central_widget)
        self.login_screen.auth_successful.connect(self.handle_auth_successful)

        # Add login screen to central widget
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.login_screen)

    def handle_auth_successful(self):
        username = self.login_screen.username_edit.text()
        self.auth_successful.emit(username)
        self.close()

    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Ошибка")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a2e;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        msg.exec_()

    def show_success(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Успех")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a2e;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        msg.exec_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.centralWidget().resize(self.size())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept() 