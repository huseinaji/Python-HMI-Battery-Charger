import paho.mqtt.client as mqtt
import time
import json

import ssl

MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "mqtt/subscribe"

def on_connect(client, userdata, flags, rc) :

    if rc==0:
        print("connected ok")
    else:
        print("not connected", rc)
 #---------------------------------------------------------------------------
def on_disconnect(client, userdata, flags, rc=0) :
    print("disconnect result code "+str(rc))
 #-------------------------------------------------------------------------
def on_message(client,userdata,msg) :

    global m_decode
    
    m_decode=str(msg.payload.decode("utf-8","ignore")) 


    client = mqtt.Client("paclido") #create new instance
    client.on_connect=on_connect
    client.on_message=on_message

    #######can't configure tls ? how i'm suppose to do ? ##########
    client.tls_set('/etc/mosquitto/certs/ca/ca.crt', tls_version=1)
    client.tls_insecure_set(True)
    ###############################################################

    print ("cnct to broker", MQTT_HOST)
    self.client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    client.subscribe([("gateway/abcdef1010101010/rx", 0)("gateway/a10b20c20d30e40f/rx", 0)])
    client.loop_forever()