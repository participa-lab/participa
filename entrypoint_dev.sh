#!/bin/sh


python manage.py migrate --no-input

sh makestatic.sh

python manage.py runserver
