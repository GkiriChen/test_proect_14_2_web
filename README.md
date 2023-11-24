# Проект "PhotoShare"
<p align="center">
   <img src="https://img.shields.io/badge/Language-Python-9cf">
   <img src="https://img.shields.io/badge/FastAPI-0.95.1-brightgreen">
   <img src="https://img.shields.io/badge/SQLAlchemy-2.0-orange">
   <img src="https://img.shields.io/badge/Pytest-7.3.0-informational">
   <img src="https://img.shields.io/badge/License-MIT-yellow">
</p>

## Розгорнут
- [Live PhotoShare](https://photoshare-team6.fly.dev/docs)

## Установка 💻

1. Для розгортання додатку локально на комп'ютері потрібно створити базу даних ```Postges```
2. Встановити пакет віртуального оточення ```poetry```
3. Створити ```".env"``` файл на основі ```"example.env"```
5. Встановити ```Docker(desktop)```
6. Запустити середовище розробки
7. Встановіть необхідні пакети, запустивши ```pip install -r requirements.txt```
8. В терміналі виконати команду ```alembic upgrade heads```
9. В терміналі виконати команду ```docker-compose up```
10. Також в терміналі запустити серевер командою ```uvicorn main:app --reload``` або ```uvicorn main:app --host localhost --port 8000 --reload```
11. Відкрити сторінку в браузері за посиланням з термінала.
 
