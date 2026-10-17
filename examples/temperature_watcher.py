#!/usr/bin/env python3
"""Watch the kitchen temperature topic and react when it gets hot.

Subscribes to home/kitchen/temperature (where sensor_publisher.py
publishes) and prints every reading. Above 24 degrees it also prints
the reaction a real setup might trigger — opening a vent, starting a
fan, sending a notification. Here it just prints; the print is where
your own action code would go.

Run:  python3 temperature_watcher.py   (Ctrl+C to stop)
"""

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "home/kitchen/temperature"
TOO_HOT = 24.0


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected. Subscribing to {TOPIC}")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed, reason code: {reason_code}")


def on_message(client, userdata, msg):
    reading = float(msg.payload.decode())
    print(f"{msg.topic}: {reading:.1f} °C")
    if reading > TOO_HOT:
        print(f"  -> Too hot (over {TOO_HOT:.0f} °C): "
              "this is where you'd open the vent or send an alert.")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                     client_id="kitchen-watcher")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nStopped.")
