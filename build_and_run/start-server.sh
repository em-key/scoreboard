#!/usr/bin/env bash
# start-server.sh

# Change to project direcotry
APP_ROOT="$(dirname "$(dirname "$(readlink -f "$0")")")"
cd $APP_ROOT

# Generate new secret key for app
python manage.py generate_secret_key --replace

# run gunicorn server in background process
# gunicorn scoreboard.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3 &
# nginx -g "daemon off;"

python manage.py makemigrations
python manage.py migrate
python manage.py initadminuser
python manage.py runserver 0.0.0.0:8000
