import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.controllers.main_controller import MainController
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    controller = MainController()
    controller.show_main_window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
