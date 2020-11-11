#!/usr/bin/env bash
./manage.py migrate

# Run Application
./manage.py runserver 0.0.0.0:8000
