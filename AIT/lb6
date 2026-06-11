# Отчет по лабораторной работе
## Docker: Развертывание Ping-Pong веб-приложения на Flask

---

## 📋 Оглавление

1. [Цель работы](#1-цель-работы)
2. [Выбор языка и архитектура проекта](#2-выбор-языка-и-архитектура-проекта)
3. [Содержимое файлов](#3-содержимое-файлов)
4. [Сборка Docker-образа](#4-сборка-docker-образа)
5. [Тестирование работы](#7-тестирование-работы)
6. [Заключение](#10-заключение)

---

## 1. Цель работы

Разработать веб-приложение в стиле "Ping-Pong" (запрос-ответ), которое читает порт и текст ответа из переменных окружения, и запустить 3 экземпляра этого приложения с помощью Docker, каждый на своем порту и с собственным ответом.

---

## 2. Выбор языка и архитектура проекта

**Выбранный язык:** Python 3.11  
**Веб-фреймворк:** Flask

**Почему Flask?**
- Легкий и простой веб-фреймворк
- Минимальное количество зависимостей
- Идеально подходит для небольших API

**Архитектура проекта:**
~/flask-ping-pong/
├── app.py # Основное веб-приложение
├── Dockerfile # Инструкция для сборки Docker-образа
└── requirements.txt # Зависимости Python

---

## 3. Содержимое файлов

### 3.1 app.py

```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Читаем переменные окружения
PONG_MESSAGE = os.getenv('PONG_MESSAGE', 'pong')
PORT = int(os.getenv('PORT', 5000))
INSTANCE_NAME = os.getenv('INSTANCE_NAME', 'unknown')

@app.route('/ping')
def ping():
    return jsonify({
        'message': PONG_MESSAGE,
        'instance': INSTANCE_NAME,
        'status': 'alive'
    })

@app.route('/')
def root():
    return jsonify({
        'service': 'Flask Ping Pong API',
        'endpoints': ['/ping', '/health'],
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)


### 3.2 requirements.txt
Flask==2.3.3

### 3.3 Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "app.py"]

## 4. Сборка Docker-образа

$ cd ~/flask-ping-pong
$ docker build -t flask-ping-pong .

## 5.Тестирование работы
$ curl http://localhost:8083/ping
$ curl http://localhost:8084/ping
$ curl http://localhost:8085/ping

## 6. Заключение
С помощью Docker были запущены 3 независимых экземпляра приложения на портах 8083, 8084 и 8085, каждый с собственным уникальным ответом. Все экземпляры успешно прошли тестирование через curl и браузер.
