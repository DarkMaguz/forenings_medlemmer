#!/bin/bash
python manage.py migrate
python manage.py loaddata fixtures/templates.json
python manage.py loaddata fixtures/unions.json
python manage.py loaddata fixtures/departments.json
python manage.py runserver 0.0.0.0:8000
