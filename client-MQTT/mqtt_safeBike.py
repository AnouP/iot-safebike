import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

def on_publish(client,userdata,result):             
    print("data published \n")
    pass

def on_subscribe(client,userdata,result):             
    print("subbed \n")
    pass

def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))

mqttBroker = "eu1.cloud.thethings.network"
client = mqtt.Client("safeBike-client")
client.connect(mqttBroker, port=1883)

client.loop_start()
client.subscribe('#')
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe

#TODO Publish an alarm on/off

client.loop_end()

"""
m = subscribe.simple(topics=['#'], hostname="eu1.cloud.thethings.network", port=1883, auth={'username':"mse-iot-safebike",'password':"NNSXS.WFXYSO6IXBSHDY6OVB6TFZFKF6QYVVMSF6SVFCQ.HOGSA3RY4IAAEBBO4WY2QGBK7HHM2C4KBYIH6ZDUWHE4PFIYYG4Q"}, msg_count=2)

for a in m:
    print(a.topic)
    print(a.payload)
    
publish.single("v3/mse-iot-safebike/devices/eui-70b3d5499c89cc8f/down/push", '{"downlinks":[{"f_port": 15,"frm_payload":"vu8=","priority": "NORMAL"}]}', hostname="eu1.cloud.thethings.network", port=1883, auth={'username':"mse-iot-safebike@ttn",'password':"NNSXS.WFXYSO6IXBSHDY6OVB6TFZFKF6QYVVMSF6SVFCQ.HOGSA3RY4IAAEBBO4WY2QGBK7HHM2C4KBYIH6ZDUWHE4PFIYYG4Q"})
"""
