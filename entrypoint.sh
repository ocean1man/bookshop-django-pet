#!/bin/sh

python manage.py migrate

python manage.py import_data

python manage.py runserver 0.0.0.0:8000