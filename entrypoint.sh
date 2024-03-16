#!/bin/sh
npm --version
npm install cross-env

python manage.py tailwind install

python manage.py migrate --no-input

python manage.py tailwind build

python manage.py collectstatic --no-input

gunicorn --bind 0.0.0.0:8000 --workers 9 --max-requests 1000 participa.wsgi:application
