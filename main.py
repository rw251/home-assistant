import paho.mqtt.client as mqtt
import json
from math import exp,log
from datetime import datetime
from pathlib import Path 
from os import path
from time import sleep

data_file = Path(path.dirname(__file__)) / 'data.txt'
config_file = Path(path.dirname(__file__)) / 'config.json'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("zigbee2mqtt/humidtemp/#")  

    else:
        print(f"Failed to connect, result code {rc}")


def on_message(client, userdata, msg):
    if len(msg.payload) > 5:
        data = msg.payload.decode()
        try:
            items = json.loads(data)
            config = json.loads(config_file.read_text())
            humidity = items["humidity"]
            temperature = items["temperature"]
            dew_point = (1/((1/273) - log((0.611 * exp(5423 * ((1/273) - (1/(273+temperature)))))*humidity/61.1)/5423)) - 273;  
            isoTimeString = datetime.now().isoformat()[0:19] 
            device = msg.topic.split('/')[-1]
            location = device
            if device in config["mapping"]:
                location = config["mapping"][device]
            with open(data_file, 'a') as f:
                f.write(f"""{isoTimeString}\t{location}\t{device}\t{temperature}\t{humidity}\t{dew_point}\n""")
        except Exception as e:
            print(e)

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
while True:
    try:
        print('Attempting to connect to MQTT broker on port 1883...') 
        mqttc.connect("127.0.0.1", 1883, 60)
        break
    except :
        print("Inital connection failed ... retrying in 5s...")
        sleep(5)
        pass

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()
