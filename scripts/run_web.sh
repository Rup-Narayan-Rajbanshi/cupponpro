#!/usr/bin/env bash
./manage.py migrate
./manage.py load_master_data
# Run Application
./manage.py runserver 0.0.0.0:8000
