import paho.mqtt.client as mqtt
import json
A = 60
B = 55.1
C = "iso cuyy"

MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "mqtt/subscribe"

buff = {
    "AA" : A,
    "BB" : B,
    "CC" : C
}
brokers_out = json.dumps(buff)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
 
client = mqtt.Client()
client.reinitialise(client_id="clientidmqtt", clean_session=True, userdata=None)
client.on_connect = on_connect
# hostname, port, timeout
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
# auto reconnect

client.publish(MQTT_TOPIC, brokers_out)
client.subscribe(MQTT_TOPIC)
client.loop_forever()
