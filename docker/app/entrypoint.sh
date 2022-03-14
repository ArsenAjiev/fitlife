#!/bin/bash

/wait-for-it.sh db:5432 -t 10

python manage.py migrate
python manage.py collectstatic --no-input -c -v 0

gunicorn app.wsgi:application -w 4 -b :8000 --log-level debug