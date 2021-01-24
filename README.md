# Scoreboard
learning project - django, openapi, swagger, connexion, mqtt, ajax, js, nginx, gunicorn

# Intro
The project was created to have a little web application showing a scoreboard for team sports. 
Plan is to have very small wlan buttons based on ESP8266 which can send updates via mqtt to update the score. (each player will have one button)
Also updates via REST API should be possible (learning purpose)

# Technical infos
- Project is based on django 3.1.4 - https://www.djangoproject.com/
- For MQTT connections paho-mqtt-client is used - https://pypi.org/project/paho-mqtt/ 
- For REST API definitions OpenAPI-Spec 3.0.2 was taken - https://swagger.io/specification/ 
- Connexion is choosen to generate Swagger UI and also provide API Endpoints with flask - https://github.com/zalando/connexion
- Scores update via Ajax every 500ms
- Nginx is used as proxy for gunicorn WSGI server to server django (webapp) and flask (API calls)
- create default Admin user by calling python manage.py initadminuser (default PW: 123)

# Installation - docker

Please find instructions on dockerhub
https://hub.docker.com/r/emkey0/scoreboard 

# Installation - native

## webapp
- Install required packages -> see requirements.txt
- Set ENV variable: DJANGO_ALLOWED_HOSTS (comma separated)
- Run Django app
- Create Django Superuser

## mqtt score updates
- run mqtt broker
- set environment variables
    - MQTT_SERVER
    - MQTT_PORT
    - MQTT_USER
    - MQTT_PW
- run script: scoreboard_mqtt.py in subfolder
- use channels scoreboard/player1 or scoreboard/player2 and send number of point in the message (-10 to 10 possible)

## rest api
- set environment variable API_KEY
- run script: scoreboard_rest.py
- to access swagger ui: url + /v1/ui
- try out (default api key is 1234)

![Alt text](scoreboard.png?raw=true "Scoreboard-Index")

# Other features
- Create new games via dropdown menu
- Reset score with droptdown menu
- Manage avaialbe players in "Scoreboard Admin Panel" (Slightly modified Django Admin)
- Change players of active game
- Check highscore table
- updada score via "/controller" webview

# Planned features
- build custom player mangagment page based on django forms
- Add API feature to get all game results and build a second App that can manage multiple scoreboards (tournament master)
- look at websockets or other methods to update score based on server side events

Have Fun!

