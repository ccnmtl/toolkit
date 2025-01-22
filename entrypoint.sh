#!/bin/sh

python manage.py migrate --noinput --settings=toolkit.settings_docker

# Create Super User, will require DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD in Environment Variables
python manage.py create_superuser

# gunicorn toolkit.wsgi:application --bind 0.0.0.0:8000 --settings=toolkit.settings_docker
python manage.py runserver --settings=toolkit.settings_docker 0.0.0.0:8000