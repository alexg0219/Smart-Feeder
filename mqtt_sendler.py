from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
import base64

import secret

broker = secret.broker
port = secret.port
topic = secret.topic
topic_to_call = secret.topic_to_call
client_id = secret.client_id
username = secret.username
password = secret.password


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    msg = 1
    result = client.publish(topic_to_call, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic_to_call}`")
    else:
        print(f"Failed to send message to topic {topic}")