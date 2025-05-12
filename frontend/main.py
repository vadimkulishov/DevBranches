import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
from backend.app import app as flask_app, db
from backend.fill_questions import example_questions
from frontend.controllers.main_controller import MainController
from PyQt5.QtWidgets import QApplication


def init_database():
    with flask_app.app_context():
        # Создаем все таблицы
        db.create_all()
        # Проверяем, есть ли уже вопросы в базе
        from backend.app import Question
        if Question.query.first() is None:
            # Если база пуста, заполняем её вопросами
            for topic, questions in example_questions.items():
                for qtext, opts, correct in questions:
                    q = Question(topic=topic, question=qtext, correct_answer=correct)
                    q.set_options(opts)
                    db.session.add(q)
            db.session.commit()
            print("База вопросов успешно заполнена!")


def main():
    # Инициализируем базу данных
    init_database()
    
    # Start the Flask backend in a separate thread
    flask_thread = threading.Thread(
        target=lambda: flask_app.run(
            host='127.0.0.1', port=5001, debug=False, use_reloader=False
        )
    )
    flask_thread.daemon = True
    flask_thread.start()

    app = QApplication(sys.argv)
    controller = MainController()
    controller.show_main_window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
