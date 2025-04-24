#!/bin/bash

# 1. Активируем виртуальное окружение
echo "Активируем виртуальное окружение..."
python -m venv venv
source venv/bin/activate

# 2. Устанавливаем зависимости для бэкенда
echo "Устанавливаем зависимости для бэкенда..."
pip install -r backend/requirements.txt

# 3. Запускаем сервер (бэкенд)
echo "Запускаем сервер (бэкенд)..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# 4. Устанавливаем зависимости для фронтенда
echo "Устанавливаем зависимости для фронтенда..."
pip install -r frontend/requirements.txt

# 5. Запускаем клиент (фронтенд)
echo "Запускаем клиент (фронтенд)..."
cd frontend
python main.py &
FRONTEND_PID=$!
cd ..

# 6. Ожидаем завершения
echo "Проект запущен. Для остановки нажмите Ctrl+C."
wait $BACKEND_PID $FRONTEND_PID