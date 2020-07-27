#!/bin/bash
# entry.sh
# python3 manage.py migrate
python manage.py makemigrations
python manage.py migrate
# gunicorn project.wsgi:application --bind 0.0.0.0:1001
python manage.py runserver 0.0.0.0:8000
