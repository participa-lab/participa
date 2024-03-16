#!/bin/sh


python manage.py migrate --no-input

gunicorn --bind 0.0.0.0:8000 --workers 9 --max-requests 1000 participa.wsgi:application
