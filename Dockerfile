FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py

# Установка зависимостей
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копирование кода приложения 
COPY . .

# Запуск приложения Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]