#!/usr/bin/env python3
"""Publish simulated kitchen temperature readings to an MQTT broker.

Stands in for a real sensor: every two seconds it sends one reading
to the topic home/kitchen/temperature. The readings step upward on
purpose so the companion watcher script gets one reading hot enough
to react to. Swap the READINGS list for a real sensor call and the
rest of the script doesn't change.

Run:  python3 sensor_publisher.py
Needs a broker on localhost:1883 (see the guide's broker chapter).
"""

import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "home/kitchen/temperature"

# Simulated readings, degrees C. The last one crosses 24 on purpose.
READINGS = [21.5, 22.3, 23.1, 23.9, 24.7]


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to broker.")
    else:
        print(f"Connection failed, reason code: {reason_code}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                     client_id="kitchen-sensor")
client.on_connect = on_connect
client.connect(BROKER, PORT)
client.loop_start()

time.sleep(1)  # let the connection settle before the first publish
for reading in READINGS:
    client.publish(TOPIC, f"{reading:.1f}", qos=1)
    print(f"Published {reading:.1f} to {TOPIC}")
    time.sleep(2)

client.loop_stop()
client.disconnect()
print("Done.")
