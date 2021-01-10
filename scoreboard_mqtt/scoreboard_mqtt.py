import os
import sys
import time
import logging
import django
import paho.mqtt.client as mqtt

# append path that module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

# the django setup needs access to the settings file
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "scoreboard.settings_dev")
django.setup ()

from scoreapp.models import Game


#init logging
logging.basicConfig(filename='/var/log/mqtt/mqtt.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(os.environ.get("MQTT_PLAYER1"))
    client.subscribe(os.environ.get("MQTT_PLAYER2"))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        points = int(msg.payload.decode("utf-8"))
        game = Game.objects.latest('id')
    except:
        print("error - could not resovle game or invalid input")
        return

    if points>10 or points<-10:
        print("error - invalid points value")
        return

    if msg.topic==os.environ.get("MQTT_PLAYER1"):
        print("player1 " + str(points))
        game.score_1 = game.score_1 + points
    elif msg.topic==os.environ.get("MQTT_PLAYER2"):
        print("player2 " + str(points))
        game.score_2 = game.score_2 + points
    game.save()

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logging.warning("MQTT got disconnect with error code: " + str(rc))

client = mqtt.Client(client_id="Scoreboard")
client.username_pw_set(os.environ.get("MQTT_USER"),os.environ.get("MQTT_PW"))

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

CONNECTSTATUS = False
while not CONNECTSTATUS:
    try:
        client.connect(os.environ.get("MQTT_SERVER"), int(os.environ.get("MQTT_PORT")), 60)
        CONNECTSTATUS = True
        logging.info("MQTT Server reached")
    except:
        print("MQTT client setup failed - retry in 5sec")
        logging.warning("MQTT Server could not be reached - retry in 5sec\n")
        time.sleep(5)

client.loop_forever()
