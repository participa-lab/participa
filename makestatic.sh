#!/bin/sh
npm --version
npm install cross-env

python manage.py tailwind install

python manage.py tailwind build

python manage.py collectstatic --no-input