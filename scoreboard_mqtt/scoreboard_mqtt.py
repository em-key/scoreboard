import os
import sys
import time
import django
import paho.mqtt.client as mqtt

# append path that module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

# the django setup needs access to the settings file
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "scoreboard.settings_dev")
django.setup ()

from scoreapp.models import Game

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("scoreboard/player1")
    client.subscribe("scoreboard/player2")

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

    if msg.topic=='scoreboard/player1':
        print("player1 " + str(points))
        game.score_1 = game.score_1 + points
    elif msg.topic=='scoreboard/player2':
        print("player2 " + str(points))
        game.score_2 = game.score_2 + points
    game.save()

client = mqtt.Client(client_id="Scoreboard")
client.username_pw_set("scoreboard","mqtt!")

client.on_connect = on_connect
client.on_message = on_message

CONNECTSTATUS = False
while not CONNECTSTATUS:
    print("Try to connect to MQTT Broker")
    try:
        client.connect("localhost", 1883, 60)
        CONNECTSTATUS = True
    except ConnectionRefusedError:
        print("Connection refused - reconnect in 5sec")
        time.sleep(5)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
