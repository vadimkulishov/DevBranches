from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QMessageBox, QComboBox, QHBoxLayout, QFrame, QGraphicsOpacityEffect, QProgressBar, QScrollArea, QGraphicsDropShadowEffect, QFileDialog
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QLinearGradient, QPainter, QColor, QPainterPath
import os
import requests

class GradientBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.gradient = QLinearGradient(0, 0, 0, 1)
        self.gradient.setColorAt(0, QColor("#1e3c72"))
        self.gradient.setColorAt(1, QColor("#2a5298"))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gradient)
        self.timer.start(50)
        self.offset = 0
    def update_gradient(self):
        self.offset += 0.002
        if self.offset > 1:
            self.offset = 0
        self.gradient.setColorAt(0, QColor.fromHsvF((self.offset + 0.0) % 1, 0.7, 0.4))
        self.gradient.setColorAt(1, QColor.fromHsvF((self.offset + 0.5) % 1, 0.7, 0.7))
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        self.gradient.setStart(0, 0)
        self.gradient.setFinalStop(0, rect.height())
        painter.fillRect(rect, self.gradient)

class AccountWindow(QWidget):
    def __init__(self, username, controller=None, parent=None):
        super().__init__(parent)
        self.username = username
        self.controller = controller
        self.avatar_path = "user.png"  # Путь к аватарке по умолчанию
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Личный кабинет")
        self.setFixedSize(1040, 780)
        # Градиентный фон (современный)
        self.background = GradientBackground(self)
        self.background.setGeometry(self.rect())
        self.background.lower()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: white;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # Верхняя панель
        top_panel = QHBoxLayout()
        top_panel.setContentsMargins(24, 24, 24, 0)
        # Кнопка 'Выйти'
        self.logout_btn = QPushButton("⎋ Выйти", self)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #23242a;
                color: #ff1744;
                border-radius: 12px;
                font-weight: 600;
                padding: 8px 22px;
                font-size: 15px;
                border: none;
                transition: background 0.2s;
            }
            QPushButton:hover {
                background-color: #2d2e36;
                color: #fff;
            }
        """)
        self.logout_btn.setFixedWidth(110)
        self.logout_btn.setFixedHeight(38)
        self.logout_btn.clicked.connect(self.handle_logout)
        top_panel.addStretch()
        top_panel.addWidget(self.logout_btn)
        layout.addLayout(top_panel)
        # Аватарка + кнопка смены
        avatar_row = QHBoxLayout()
        avatar_row.setContentsMargins(0, 0, 0, 0)
        avatar_row.addStretch()
        avatar_container = QVBoxLayout()
        avatar_container.setAlignment(Qt.AlignHCenter)
        self.avatar_label = QLabel(self)
        self.update_avatar()
        self.avatar_label.setFixedSize(120, 120)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet("border: none; background: #23242a;")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(36)
        shadow.setColor(QColor(30, 136, 229, 120))
        shadow.setOffset(0, 6)
        self.avatar_label.setGraphicsEffect(shadow)
        avatar_container.addWidget(self.avatar_label, alignment=Qt.AlignHCenter)
        # Кнопка смены аватарки
        change_avatar_btn = QPushButton("Сменить аватар", self)
        change_avatar_btn.setStyleSheet("""
            QPushButton {
                background: #1E88E5;
                color: #fff;
                border-radius: 10px;
                font-size: 14px;
                padding: 6px 18px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: #1565c0;
            }
        """)
        change_avatar_btn.clicked.connect(self.choose_avatar)
        avatar_container.addWidget(change_avatar_btn, alignment=Qt.AlignHCenter)
        avatar_row.addLayout(avatar_container)
        avatar_row.addStretch()
        layout.addLayout(avatar_row)
        # Приветствие
        welcome_label = QLabel(f"Добро пожаловать, {self.username}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 26px;
                font-weight: 600;
                margin: 18px 0 18px 0;
                letter-spacing: 0.5px;
            }
        """)
        layout.addWidget(welcome_label)
        # Прокручиваемый контейнер для списка тем
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #23242a;
                width: 12px;
                margin: 0;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #1E88E5;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(28)
        topics = [
            {"name": "Python", "progress": 75, "icon": "🐍"},
            {"name": "JavaScript", "progress": 50, "icon": "🟨"},
            {"name": "Java", "progress": 30, "icon": "☕"},
            {"name": "C++", "progress": 90, "icon": "💻"},
            {"name": "HTML & CSS", "progress": 60, "icon": "🌐"},
            {"name": "SQL", "progress": 40, "icon": "🗄️"},
            {"name": "Data Science", "progress": 20, "icon": "📊"},
            {"name": "Machine Learning", "progress": 10, "icon": "🤖"},
            {"name": "DevOps", "progress": 80, "icon": "⚙️"},
            {"name": "Cybersecurity", "progress": 70, "icon": "🔒"}
        ]
        user_progress = self.load_user_progress()
        print('DEBUG user_progress:', user_progress)  # Отладка
        for topic in topics:
            topic_widget = QWidget()
            topic_widget.setFixedHeight(72)
            topic_widget.setStyleSheet("""
                QWidget {
                    background-color: #20222b;
                    border-radius: 18px;
                }
                QWidget:hover {
                    background-color: #23242a;
                }
            """
            )
            card_shadow = QGraphicsDropShadowEffect(self)
            card_shadow.setBlurRadius(18)
            card_shadow.setColor(QColor(30, 136, 229, 40))
            card_shadow.setOffset(0, 4)
            topic_widget.setGraphicsEffect(card_shadow)
            topic_layout = QHBoxLayout(topic_widget)
            topic_layout.setContentsMargins(18, 0, 18, 0)
            topic_layout.setSpacing(18)
            # Левая часть: иконка + название
            left_col = QHBoxLayout()
            icon_label = QLabel(topic["icon"], self)
            icon_label.setStyleSheet("font-size: 28px; margin-right: 10px;")
            left_col.addWidget(icon_label)
            topic_name = QLabel(topic["name"], self)
            topic_name.setStyleSheet("""
                QLabel {
                    color: #E0E0E0;
                    font-size: 20px;
                    font-weight: 500;
                }
            """
            )
            left_col.addWidget(topic_name)
            left_col.setAlignment(Qt.AlignVCenter)
            left_widget = QWidget()
            left_widget.setLayout(left_col)
            topic_layout.addWidget(left_widget)
            # Центр: прогресс-бар (растягивается)
            progress_bar = QProgressBar(self)
            correct = user_progress.get(topic["name"], 0)
            total = 10  # Теперь всегда 10 вопросов
            percent = int((correct / total) * 100) if total > 0 else 0
            progress_bar.setValue(percent)
            progress_bar.setTextVisible(False)
            progress_bar.setFixedHeight(22)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    background-color: #23242a;
                    border: none;
                    border-radius: 11px;
                    font-size: 14px;
                    color: #fff;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #42a5f5, stop:1 #1E88E5);
                    border-radius: 11px;
                }
            """
            )
            topic_layout.addWidget(progress_bar, stretch=1)
            # Красивый процент
            percent_label = QLabel(f"{percent}%", self)
            percent_label.setAlignment(Qt.AlignCenter)
            percent_label.setFixedWidth(110)
            percent_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 20px;
                    font-weight: bold;
                    color: {'#43ea5e' if percent >= 70 else ('#ffb300' if percent >= 40 else '#ff1744')};
                    background: transparent;
                }}
            """)
            topic_layout.addWidget(percent_label)
            # Справа: кнопка 'Старт'
            start_btn = QPushButton("Старт", self)
            start_btn.setFixedHeight(36)
            start_btn.setFixedWidth(80)
            start_btn.setStyleSheet("""
                QPushButton {
                    background: #1E88E5;
                    color: #fff;
                    border-radius: 9px;
                    font-size: 15px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: #1565c0;
                }
            """
            )
            start_btn.clicked.connect(lambda _, t=topic['name']: self.start_test(t))
            topic_layout.addWidget(start_btn)
            topic_widget.setLayout(topic_layout)
            scroll_layout.addWidget(topic_widget)
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def update_avatar(self):
        avatar_file = f"image_accaunt/{self.avatar_path}"
        size = 120
        # Загружаем изображение или плейсхолдер
        if os.path.exists(avatar_file):
            src = QPixmap(avatar_file).scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        else:
            src = QPixmap(size, size)
            src.fill(Qt.transparent)
            painter = QPainter(src)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QColor("#23242a"))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, size, size)
            painter.setPen(QColor("#888"))
            painter.setFont(self.font())
            painter.drawText(src.rect(), Qt.AlignCenter, "👤")
            painter.end()
        # Обрезаем изображение по кругу с помощью маски
        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, src)
        painter.end()
        self.avatar_label.setPixmap(rounded)
        self.avatar_label.setFixedSize(size, size)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet("border: none; background: transparent;")

    def choose_avatar(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        if file_dialog.exec_():
            selected = file_dialog.selectedFiles()
            if selected:
                import shutil
                dest = f"image_accaunt/{self.username}_avatar.png"
                shutil.copy(selected[0], dest)
                self.avatar_path = f"{self.username}_avatar.png"
                self.update_avatar()

    def start_test(self, topic):
        if self.controller:
            self.controller.username = self.username
            self.hide()
            self.controller.start_quiz_by_topic(topic)
        else:
            QMessageBox.warning(self, "Ошибка", "Контроллер не найден!")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background.setGeometry(self.rect())

    def load_user_progress(self):
        url = f"http://localhost:5001/api/user_progress?username={self.username}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                progress_data = response.json()
                # Обновляем прогресс-бары
                for i in range(self.layout().count()):
                    item = self.layout().itemAt(i)
                    if isinstance(item, QScrollArea):
                        scroll_content = item.widget()
                        if scroll_content:
                            for j in range(scroll_content.layout().count()):
                                topic_widget = scroll_content.layout().itemAt(j).widget()
                                if topic_widget:
                                    for child in topic_widget.findChildren(QProgressBar):
                                        topic_name = child.property("topic_name")
                                        if topic_name in progress_data:
                                            correct = progress_data[topic_name]
                                            total = 10
                                            percent = int((correct / total) * 100) if total > 0 else 0
                                            child.setValue(percent)
                return progress_data
        except Exception as e:
            print("Ошибка загрузки прогресса:", e)
        return {}

    def handle_logout(self):
        if self.controller:
            self.controller.username = None  # Очищаем имя пользователя
            self.controller.account_window = None  # Очищаем ссылку на окно аккаунта
            self.hide()
            self.controller.auth_window.show()
        else:
            self.hide()

    def set_username(self, username):
        self.username = username
        # Найти welcome_label и обновить текст
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            widget = item.widget()
            if isinstance(widget, QLabel) and 'Добро пожаловать' in widget.text():
                widget.setText(f"Добро пожаловать, {self.username}!")
                break