#!/bin/sh


python manage.py migrate --no-input

#sh makestatic.sh

python manage.py runserver 0.0.0.0:8000
