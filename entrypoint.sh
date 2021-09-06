#!/bin/bash

find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

python manage.py migrate
python manage.py test
python manage.py runserver 0.0.0.0:8000