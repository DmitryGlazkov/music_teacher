# Используем официальный Python образ
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

RUN pip install gunicorn==20.1.0

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir -v -r requirements.txt

# Копируем все остальное содержимое проекта
COPY . .

# Экспонируем порт, на котором работает ваше приложение (например, 8000)
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "music_teacher:app"]