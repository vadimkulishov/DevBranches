import sys
import os
from PyQt5.QtWidgets import QApplication

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    controller = MainController()
    controller.show_main_window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 