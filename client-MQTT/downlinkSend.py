import paho.mqtt.publish as publish

#!/usr/bin/python3
# Connect to TTS MQTT Server and receive uplink messages using the Paho MQTT Python client library
#
# Original source:
# https://github.com/descartes/TheThingsStack-Integration-Starters/blob/main/MQTT-to-Tab-Python3/TTS.MQTT.Tab.py
#

#
import sys
import logging
import paho.mqtt.client as mqtt
import random
from base64 import b64encode

USER = "mse-iot-safebike@ttn"
PASSWORD = "NNSXS.H4GHYJKJTFPJQLSIVVRW3MFCSBRHV2P7ARJNL6A.ZRNRCZ6ITSAG333TLXFF2QD3YIEGLIL7HBNJCBQ73WX3U2XFBZOA"
PUBLIC_TLS_ADDRESS = "eu1.cloud.thethings.network"
PUBLIC_TLS_ADDRESS_PORT = 8883
DEVICE_ID = "eui-70b3d5499c89cc8f"
ALL_DEVICES = True
QOS = 0

def stop(client):
    client.disconnect()
    print("\nExit")
    sys.exit(0)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\nConnected successfully to MQTT broker")
    else:
        print("\nFailed to connect, return code = " + str(rc))


# mid = message ID
def on_subscribe(client, userdata, mid, granted_qos):
    print("\nSubscribed with message id (mid) = " + str(mid) + " and QoS = " + str(granted_qos))


def on_disconnect(client, userdata, rc):
    print("\nDisconnected with result code = " + str(rc))


def on_log(client, userdata, level, buf):
    print("\nLog: " + buf)
    logging_level = client.LOGGING_LEVEL[level]
    logging.log(logging_level, buf)


# Generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

print("Create new mqtt client instance")
mqttc = mqtt.Client(client_id)

print("Assign callback functions")
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
# mqttc.on_log = on_log  # Logging for debugging OK, waste

# Setup authentication from settings above
mqttc.username_pw_set(USER, PASSWORD)

# IMPORTANT - this enables the encryption of messages
mqttc.tls_set()  # default certification authority of the system

print("Connecting to broker: " + PUBLIC_TLS_ADDRESS + ":" + str(PUBLIC_TLS_ADDRESS_PORT))
mqttc.connect(PUBLIC_TLS_ADDRESS, PUBLIC_TLS_ADDRESS_PORT, 60)

if len(DEVICE_ID) != 0:
    topic = "v3/" + USER + "/devices/" + DEVICE_ID + "/down/push"

    print("Subscribe to topic " + topic + " with QoS = " + str(QOS))
    mqttc.subscribe(topic, QOS)

    print("Publishing message to topic " + topic + " with QoS = " + str(QOS))

    # 00 = alarm OFF
    # 03 = alarm ON
    hexadecimal_payload = '00'
    fport = 3

    # Convert hexadecimal payload to base64
    b64 = b64encode(bytes.fromhex(hexadecimal_payload)).decode()
    print('Convert hexadecimal_payload: ' + hexadecimal_payload + ' to base64: ' + b64)

    msg = '{"downlinks":[{"f_port":' + str(fport) + ',"frm_payload":"' + b64 + '","priority": "NORMAL"}]}'
    result = mqttc.publish(topic, msg, QOS)

    # result: [0, 2]
    status = result[0]
    if status == 0:
        print("Send " + msg + " to topic " + topic)
    else:
        print("Failed to send message to topic " + topic)

else:
    print("Can not subscribe or publish to topic")
    stop(mqttc)