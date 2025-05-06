import os
from app import db, Question, app

topics = [
    "Python", "JavaScript", "Java", "C++", "HTML & CSS",
    "SQL", "Data Science", "Machine Learning", "DevOps", "Cybersecurity"
]

# Примерные вопросы для каждой темы (по 15 на каждую)
example_questions = {
    "Python": [
        ("Что выведет `print(2 ** 3)`?", ["6", "8", "9", "12"], 1),
        ("Какой тип данных для `3.14`?", ["int", "float", "str", "bool"], 1),
        ("Как объявить функцию?", ["def", "func", "function", "lambda"], 0),
        ("Какой оператор для деления с остатком?", ["/", "//", "%", "^"], 2),
        ("Как создать список?", ["[]", "{}", "()", "<>"], 0),
        ("Как получить длину списка `a`?", ["a.length", "len(a)", "a.size()", "count(a)"], 1),
        ("Какой результат у `5 // 2`?", ["2", "2.5", "3", "1"], 0),
        ("Какой метод добавляет элемент в список?", ["add", "append", "insert", "push"], 1),
        ("Какой тип данных для `True`?", ["int", "bool", "str", "float"], 1),
        ("Какой символ для комментария?", ["#", "//", "--", "/*"], 0),
    ],
    "JavaScript": [
        ("Как объявить переменную в ES6?", ["var", "let", "const", "all"], [1, 2]),
        ("Что выведет `console.log(2 + '2')`?", ["4", "22", "NaN", "error"], 1),
        ("Какой метод добавляет элемент в конец массива?", ["push", "pop", "shift", "unshift"], 0),
        ("Как проверить тип данных?", ["typeof", "type", "getType", "instanceof"], 0),
        ("Как создать объект?", ["{}", "[]", "new Object", "all"], [0, 2, 3]),
        ("Что такое `NaN`?", ["Number", "String", "Boolean", "Object"], 0),
        ("Какой оператор для строгого равенства?", ["==", "===", "=", "!=="], 1),
        ("Как объявить функцию?", ["function", "func", "def", "fn"], 0),
        ("Что делает метод `Array.map()`?", ["Фильтрует массив", "Изменяет каждый элемент", "Создает новый массив", "Удаляет элементы"], 2),
        ("Какой результат у `Boolean('false')`?", ["true", "false", "error", "undefined"], 0),
    ],
    "Java": [
        ("Как объявить класс?", ["class", "Class", "new Class", "interface"], 0),
        ("Какой тип данных для `3.14f`?", ["double", "float", "int", "long"], 1),
        ("Как создать объект класса `MyClass`?", ["new MyClass()", "MyClass.new()", "MyClass()", "create MyClass()"], 0),
        ("Какой оператор для наследования?", ["extends", "implements", "inherits", "super"], 0),
        ("Как объявить массив?", ["int[]", "Array[int]", "int array", "[int]"], 0),
        ("Какой метод — точка входа в программу?", ["main", "start", "run", "init"], 0),
        ("Что такое JVM?", ["Java Virtual Machine", "Java Visual Manager", "Java Variable Model", "Java Version Manager"], 0),
        ("Какой тип данных для `'A'`?", ["char", "String", "int", "boolean"], 0),
        ("Как проверить длину строки `s`?", ["s.length", "s.length()", "s.size", "len(s)"], 1),
        ("Какой оператор для логического И?", ["&", "&&", "|", "||"], 1),
    ],
    "C++": [
        ("Как вывести текст в консоль?", ["print()", "cout <<", "printf()", "console.log()"], 1),
        ("Как объявить указатель?", ["int* ptr", "ptr int", "pointer int", "int ptr*"], 0),
        ("Какой оператор для динамического выделения памяти?", ["new", "malloc", "alloc", "create"], 0),
        ("Как объявить класс?", ["class", "struct", "object", "type"], 0),
        ("Какой заголовочный файл для ввода/вывода?", ["<iostream>", "<stdio.h>", "<input>", "<io.h>"], 0),
        ("Какой тип данных для `3.14`?", ["int", "float", "double", "long"], 2),
        ("Как создать ссылку на переменную?", ["int& ref = x;", "int* ref = x;", "ref int = x;", "int ref = &x;"], 0),
        ("Какой оператор для наследования?", [":", "extends", "inherits", "->"], 0),
        ("Как проверить размер типа `int`?", ["sizeof(int)", "int.size", "size(int)", "int.length"], 0),
        ("Как объявить массив из 10 элементов?", ["int arr[10];", "array[10] int;", "int[] arr = new int[10];", "arr = int[10];"], 0),
    ],
    "HTML & CSS": [
        ("Какой тег для ссылки?", ["<a>", "<link>", "<href>", "<url>"], 0),
        ("Как подключить CSS к HTML?", ["<style>", "<css>", "<link rel='stylesheet'>", "<script>"], 2),
        ("Как изменить цвет текста в CSS?", ["text-color", "font-color", "color", "text-style"], 2),
        ("Какой атрибут для уникального идентификатора?", ["id", "class", "name", "tag"], 0),
        ("Как создать кнопку?", ["<button>", "<input type='button'>", "<div class='button'>", "Все варианты верны"], 3),
        ("Как сделать жирный текст?", ["<strong>", "<bold>", "<b>", "Варианты 1 и 3"], 3),
        ("Как центрировать блок по горизонтали?", ["margin: auto;", "text-align: center;", "align: center;", "position: center;"], 0),
        ("Какой тег для заголовка первого уровня?", ["<h1>", "<header>", "<head>", "<title>"], 0),
        ("Как задать внешний отступ в CSS?", ["padding", "margin", "spacing", "border"], 1),
        ("Как вставить изображение?", ["<img src='...'>", "<image src='...'>", "<picture>", "<icon>"], 0),
    ],
    "SQL": [
        ("Как выбрать все данные из таблицы `users`?", ["SELECT * FROM users;", "GET * FROM users;", "FIND users;", "EXTRACT * FROM users;"], 0),
        ("Как добавить запись в таблицу?", ["INSERT INTO", "ADD TO", "CREATE ROW", "UPDATE"], 0),
        ("Как обновить данные в таблице?", ["MODIFY", "CHANGE", "UPDATE", "ALTER"], 2),
        ("Как удалить таблицу?", ["DELETE TABLE", "DROP TABLE", "REMOVE TABLE", "ERASE TABLE"], 1),
        ("Какой оператор для фильтрации?", ["WHERE", "FILTER", "HAVING", "CHECK"], 0),
        ("Как выбрать уникальные значения?", ["UNIQUE", "DISTINCT", "DIFFERENT", "ONLY"], 1),
        ("Как объединить таблицы?", ["MERGE", "JOIN", "LINK", "COMBINE"], 1),
        ("Как отсортировать по возрастанию?", ["ORDER BY ASC", "SORT ASC", "ORDER BY", "SORT BY"], 0),
        ("Как посчитать количество строк?", ["COUNT()", "SUM()", "TOTAL()", "AMOUNT()"], 0),
        ("Как создать базу данных?", ["CREATE DATABASE", "MAKE DATABASE", "NEW DATABASE", "BUILD DATABASE"], 0),
    ],
    "Data Science": [
        ("Какая библиотека Python для анализа данных?", ["numpy", "pandas", "matplotlib", "scipy"], 1),
        ("Как загрузить CSV-файл в pandas?", ["pd.read_csv()", "pd.load_csv()", "pd.open_csv()", "pd.import_csv()"], 0),
        ("Какой график для визуализации распределения?", ["barplot", "histogram", "pie chart", "scatter plot"], 1),
        ("Как посчитать среднее значение в pandas?", ["mean()", "avg()", "average()", "sum() / count()"], 0),
        ("Как удалить пропущенные значения?", ["dropna()", "remove_missing()", "fillna(0)", "clean()"], 0),
        ("Какой метод для обучения модели?", ["fit()", "train()", "learn()", "execute()"], 0),
        ("Как нормализовать данные?", ["MinMaxScaler", "StandardScaler", "Normalizer", "Все варианты верны"], 3),
        ("Как разделить данные на train и test?", ["train_test_split()", "split_data()", "divide()", "partition()"], 0),
        ("Как посчитать корреляцию?", ["corr()", "cov()", "relation()", "link()"], 0),
        ("Как переименовать столбец в pandas?", ["rename()", "change_column()", "set_name()", "alter()"], 0),
    ],
    "Machine Learning": [
        ("Какой алгоритм для классификации?", ["K-Means", "Linear Regression", "Logistic Regression", "DBSCAN"], 2),
        ("Что такое overfitting?", ["Модель слишком простая", "Модель слишком сложная", "Модель идеальна", "Модель не обучается"], 1),
        ("Как оценить точность модели?", ["accuracy_score()", "precision()", "score()", "check()"], 0),
        ("Какой метод для уменьшения размерности?", ["PCA", "KNN", "SVM", "Decision Tree"], 0),
        ("Что делает Random Forest?", ["Использует один дерево", "Использует ансамбль деревьев", "Только для регрессии", "Только для кластеризации"], 1),
        ("Какой loss для линейной регрессии?", ["MSE", "Cross-Entropy", "MAE", "Huber"], 0),
        ("Что такое гиперпараметры?", ["Параметры данных", "Параметры модели, заданные до обучения", "Параметры слоев нейросети", "Параметры оптимизатора"], 1),
        ("Какой метод для кластеризации?", ["K-Means", "Linear Regression", "Logistic Regression", "SVM"], 0),
        ("Что делает градиентный спуск?", ["Минимизирует функцию потерь", "Максимизирует точность", "Увеличивает сложность модели", "Удаляет шумы"], 0),
        ("Какой библиотекой создать нейросеть?", ["TensorFlow", "PyTorch", "Keras", "Все варианты верны"], 3),
    ],
    "DevOps": [
        ("Что такое CI/CD?", ["Continuous Integration / Continuous Deployment", "Code Inspection / Code Deployment", "Cloud Infrastructure / Cloud Development", "Containerization / Virtualization"], 0),
        ("Какой инструмент для контейнеризации?", ["Docker", "Kubernetes", "Ansible", "Terraform"], 0),
        ("Какой язык для инфраструктуры как кода?", ["YAML", "JSON", "HCL (Terraform)", "XML"], 2),
        ("Что делает Kubernetes?", ["Управляет контейнерами", "Создает виртуальные машины", "Развертывает серверы", "Настраивает сети"], 0),
        ("Какой инструмент для автоматизации сборки?", ["Jenkins", "GitLab CI", "GitHub Actions", "Все варианты верны"], 3),
        ("Что такое IaC?", ["Infrastructure as Code", "Internet as Cloud", "Integration as Configuration", "Instance as Container"], 0),
        ("Какой облачный провайдер от Amazon?", ["AWS", "Azure", "GCP", "IBM Cloud"], 0),
        ("Какой протокол для удаленного доступа?", ["HTTP", "SSH", "FTP", "SMTP"], 1),
        ("Что делает Ansible?", ["Оркестрация контейнеров", "Автоматизация настройки серверов", "Управление базами данных", "Мониторинг сети"], 1),
        ("Какой сервис для мониторинга?", ["Prometheus", "Grafana", "ELK Stack", "Все варианты верны"], 3),
    ],
    "Cybersecurity": [
        ("Что такое DDoS-атака?", ["Вирус", "Перегрузка сервера запросами", "Кража данных", "Фишинг"], 1),
        ("Какой метод защиты паролей?", ["Хранение в открытом виде", "Хеширование", "Отправка по email", "Запись в файл"], 1),
        ("Что такое VPN?", ["Виртуальная частная сеть", "Облачное хранилище", "Антивирус", "Файрвол"], 0),
        ("Какой тип атаки 'человек посередине'?", ["MITM", "Phishing", "SQL Injection", "Brute Force"], 0),
        ("Что такое двухфакторная аутентификация?", ["Только пароль", "Пароль + SMS-код", "Без пароля", "Только отпечаток пальца"], 1),
        ("Какой протокол для безопасного соединения?", ["HTTP", "HTTPS", "FTP", "SMTP"], 1),
        ("Что делает брандмауэр?", ["Блокирует вредоносный трафик", "Ускоряет интернет", "Шифрует данные", "Удаляет вирусы"], 0),
        ("Какой алгоритм шифрования?", ["AES", "MD5", "Base64", "JSON"], 0),
        ("Что такое SQL-инъекция?", ["Внедрение вредоносного кода в запрос", "Кража паролей", "Атака на сервер", "Фишинг"], 0),
        ("Как защититься от фишинга?", ["Не открывать подозрительные ссылки", "Использовать сложные пароли", "Обновлять ПО", "Все варианты верны"], 3),
    ],
}

# Для остальных тем просто копируем вопросы Python с заменой текста
for topic in topics:
    if topic not in example_questions:
        example_questions[topic] = [
            (f"Вопрос {i+1} по теме {topic}?", [f"Вариант {j+1}" for j in range(4)], 0) for i in range(15)
        ]

for topic, questions in example_questions.items():
    fixed_questions = []
    for qtext, opts, correct in questions:
        # Если correct_answer список, берем первый элемент
        if isinstance(correct, list):
            correct = correct[0]
        fixed_questions.append((qtext, opts, correct))
    example_questions[topic] = fixed_questions

with app.app_context():
    for topic, questions in example_questions.items():
        for qtext, opts, correct in questions:
            q = Question(topic=topic, question=qtext, correct_answer=correct)
            q.set_options(opts)
            db.session.add(q)
    db.session.commit()
print("База вопросов успешно заполнена!") 