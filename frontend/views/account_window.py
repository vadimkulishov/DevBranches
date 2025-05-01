from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class AccountWindow(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Личный кабинет")
        self.setFixedSize(1040, 780)

        layout = QVBoxLayout(self)

        # Welcome message
        welcome_label = QLabel(f"Добро пожаловать, {self.username}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(welcome_label)

        # Directions grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        directions = [
            "Python", "JavaScript", "Java", "C++", "HTML & CSS",
            "SQL", "Data Science", "Machine Learning", "DevOps", "Cybersecurity",
            "Mobile Development", "Game Development", "Cloud Computing", "AI",
            "Blockchain", "Networking", "UI/UX Design", "Testing", "Big Data", "IoT"
        ]

        for i, direction in enumerate(directions):
            button = QPushButton(direction)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2c001e;
                    border: none;
                    border-radius: 15px;
                    color: white;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3a0026;
                }
                QPushButton:pressed {
                    background-color: #1a0012;
                }
            """)
            button.clicked.connect(lambda _, d=direction: self.start_test(d))
            row, col = divmod(i, 4)
            grid_layout.addWidget(button, row, col)

        layout.addLayout(grid_layout)

    def start_test(self, direction):
        QMessageBox.information(self, "Тестирование", f"Вы выбрали направление: {direction}")