#!/usr/bin/python3
import presence_detector
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
import time
import json
from sense_hat import SenseHat

from cryptography.fernet import Fernet

def encrypt_payload(payload):
    #HAVING A HARD CODED KEY IS INSECURE  - SHOULD BE ENV/EXTERNAL VARIABLE
    cypher_key=b'xqi9zRusHkcv3Om050HwX82eMTO-LbeW4YlqVVEzpw8=' 
    cypher=Fernet(cypher_key)
    encrypted_payload=cypher.encrypt(payload.encode('utf-8'))
    return(encrypted_payload.decode())

sense = SenseHat()
sense.clear()

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    print("Message ID: " + str(mid))

mqttc = mqtt.Client()
mqttc.tls_set("./broker.emqx.io-ca.crt")

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# parse mqtt url for connection details
url_str = sys.argv[1]
print(url_str)
url = urlparse(url_str)
base_topic = url.path[1:]

# Connect
if (url.username):
    mqttc.username_pw_set(url.username, url.password)

    mqttc.connect(url.hostname, url.port)
    mqttc.loop_start()

# Publish a message to temp every 15 seconds
while True:
    temp=round(sense.get_temperature(),2)
    temp_json=json.dumps({"temperature":temp, "timestamp":time.time()})
    pressure=round(sense.get_pressure(),2)
    pres_json=json.dumps({"pressure":pressure, "timestamp":time.time()})
    mqttc.publish(base_topic+"/temperature","/pressure", encrypt_payload(temp_json))
    time.sleep(15)
    devices_found_json=json.dumps(presence_detector.find_devices())
    mqttc.publish(base_topic+"/devices", encrypt_payload(devices_found_json),1)

