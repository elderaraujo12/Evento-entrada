@echo off

call .env\Scripts\activate
start "Meu Projeto Django" http://127.0.0.1:8000/



python manage.py runserver

