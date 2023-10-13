#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py add_superuser
python manage.py add_coins_to_db
python manage.py collectstatic --noinput
