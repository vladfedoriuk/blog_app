#!/bin/bash

find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

python manage.py migrate
python manage.py test

if [ "$1" = "run_dev" ]; then
     python manage.py runserver 0.0.0.0:8000
fi