#!/usr/bin/env bash
# start-server.sh

# Change to project direcotry
APP_ROOT="$(dirname "$(dirname "$(readlink -f "$0")")")"
cd $APP_ROOT

# Generate new secret key for app
python manage.py generate_secret_key --replace

# Prepare database
python manage.py makemigrations
python manage.py migrate
python manage.py initadminuser

# Run MQTT Client

if [ "$MQTT" = "yes" ]
then
    echo "Start MQTT Client - send channel updates to $MQTT_PLAYER1 or $MQTT_PLAYER2"
    python scoreboard_mqtt/scoreboard_mqtt.py &
fi

# Run RESTAPI

if [ "$API" = "yes" ]
then
    echo "Start REST API - connect to swagger UI via exposed port 8081 /v1/ui"
    gunicorn --chdir ./scoreboard_api scoreboard_rest --bind 127.0.0.1:8020 --workers 3 --daemon
fi

# Run Webapp
# python manage.py runserver 0.0.0.0:8000
gunicorn scoreboard.wsgi --user nginx --bind 127.0.0.1:8010 --workers 3 --daemon
nginx -g "daemon off;"