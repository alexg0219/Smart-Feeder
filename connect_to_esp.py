import paho.mqtt.client as mqtt_client
import base64
import time
import telegram_services
import secret

broker = secret.broker
port = secret.port
topic = secret.topic
topic_to_call = secret.topic_to_call
client_id = secret.client_id
username = secret.username
password = secret.password


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        # For paho-mqtt 2.0.0, you need to add the properties parameter.
        # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Set Connecting Client ID
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)

    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    # client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, msg):
    result = client.publish(topic_to_call, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic_to_call}`")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe_image(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        decoded_img_data = base64.b64decode(msg.payload.decode())
        with open('output.jpeg', 'wb') as img_file:
            img_file.write(decoded_img_data)

    client.subscribe(topic)
    client.on_message = on_message


def subscribe_image_sensor(client, context):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        decoded_img_data = base64.b64decode(msg.payload.decode())
        with open('output.jpeg', 'wb') as img_file:
            img_file.write(decoded_img_data)
            telegram_services.send_in_chat_image(context, 'output.jpeg')

    client.subscribe(topic)
    client.on_message = on_message


def get_image():
    client = connect_mqtt()
    publish(client, '1')
    subscribe_image(client)
    client.loop_start()
    time.sleep(10)
    client.disconnect()


def move():
    client = connect_mqtt()
    publish(client, '10')
    client.disconnect()


def off_sensor():
    client = connect_mqtt()
    publish(client, '10')
    client.disconnect()


def on_sensor():
    client = connect_mqtt()
    publish(client, '100')
    client.disconnect()

def get_pir_image(context):
    client = connect_mqtt()
    subscribe_image_sensor(client, context)
    client.loop_start()
