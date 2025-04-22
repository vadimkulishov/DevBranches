class QuizModel:
    def __init__(self):
        self.questions = []
        self.current_question_index = 0
        self.score = 0

    def load_questions(self):
        self.questions = [
            {
                'question': 'Какой язык программирования считается самым популярным в 2024 году?',
                'options': ['Java', 'Python', 'JavaScript', 'C++'],
                'correct_answer': 2  # JavaScript
            },
            {
                'question': 'Что выведет этот код на Python?\nprint(2 + 2 * 2)',
                'options': ['6', '8', '4', 'Ошибку'],
                'correct_answer': 0  # 6
            },
            {
                'question': 'Какой алгоритм сортировки самый быстрый в среднем случае?',
                'options': ['Пузырьковая сортировка', 'Сортировка вставками', 'Быстрая сортировка (QuickSort)', 'Сортировка выбором'],
                'correct_answer': 2  # QuickSort
            },
            {
                'question': 'Как называется ошибка "бесконечного цикла"?',
                'options': ['Infinite loop', 'Stack Overflow', 'Segmentation fault', 'SyntaxError'],
                'correct_answer': 0  # Infinite loop
            },
            {
                'question': 'Какой язык программирования создал Гвидо ван Россум?',
                'options': ['Ruby', 'Python', 'Perl', 'PHP'],
                'correct_answer': 1  # Python
            },
            {
                'question': 'Какой тег в HTML используется для создания ссылки?',
                'options': ['<div>', '<a>', '<link>', '<href>'],
                'correct_answer': 1  # <a>
            },
            {
                'question': 'Что такое "рекурсия"?',
                'options': ['Цикл for', 'Функция, вызывающая саму себя', 'Условный оператор', 'Тип данных'],
                'correct_answer': 1  # Функция, вызывающая саму себя
            },
            {
                'question': 'Какой из этих языков компилируется в байт-код для JVM?',
                'options': ['Python', 'Kotlin', 'JavaScript', 'C#'],
                'correct_answer': 1  # Kotlin
            },
            {
                'question': 'Какой командой в Git создаётся новая ветка?',
                'options': ['git commit', 'git push', 'git branch', 'git clone'],
                'correct_answer': 2  # git branch
            },
            {
                'question': 'Какой принцип ООП позволяет скрывать детали реализации?',
                'options': ['Наследование', 'Полиморфизм', 'Инкапсуляция', 'Абстракция'],
                'correct_answer': 2  # Инкапсуляция
            },
            {
                'question': 'Как называется система управления базами данных от Oracle?',
                'options': ['MySQL', 'PostgreSQL', 'Oracle Database', 'SQLite'],
                'correct_answer': 2  # Oracle Database
            },
            {
                'question': 'Какой метод HTTP используется для получения данных?',
                'options': ['POST', 'PUT', 'GET', 'DELETE'],
                'correct_answer': 2  # GET
            },
            {
                'question': 'Что делает оператор === в JavaScript?',
                'options': ['Сравнивает без приведения типов', 'Сравнивает значения и типы', 'Присваивает значение', 'Проверяет на null'],
                'correct_answer': 1  # Сравнивает значения и типы
            },
            {
                'question': 'Какой фреймворк НЕ используется для фронтенда?',
                'options': ['React', 'Angular', 'Vue.js', 'Django'],
                'correct_answer': 3  # Django
            },
            {
                'question': 'Какой язык программирования называют "языком веба"?',
                'options': ['Java', 'C#', 'JavaScript', 'Swift'],
                'correct_answer': 2  # JavaScript
            }
        ]

    def get_current_question(self):
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, answer_index):
        current_question = self.get_current_question()
        if current_question and answer_index == current_question['correct_answer']:
            self.score += 1
            return True
        return False

    def next_question(self):
        self.current_question_index += 1
        return self.current_question_index < len(self.questions)

    def get_score(self):
        return self.score

    def reset_quiz(self):
        self.current_question_index = 0
        self.score = 0 