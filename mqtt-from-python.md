# MQTT from Python

**Scope:** a complete miniature system in Python —
one script that publishes sensor-style readings, one
that subscribes and reacts — run for real against the
guide's broker. Verified with paho-mqtt 2.1.0 on
Python 3.12.

## Setup

The client library is **paho-mqtt**, the Eclipse
project's Python client. Keep it in a virtual
environment so it never tangles with system packages:

```
python3 -m venv mqtt-env
source mqtt-env/bin/activate
pip install paho-mqtt
```

```
paho-mqtt version: 2.1.0
```

## The publisher

[`examples/sensor_publisher.py`](examples/sensor_publisher.py)
stands in for a sensor. It connects, then publishes
five readings, two seconds apart, to
`home/kitchen/temperature` — the same topic the
wildcard chapter played with. The readings step
upward on purpose, so the watcher below gets one hot
enough to react to; in a real setup a sensor read
would replace the list, and nothing else in the
script would change.

The shape to notice: build a client, set an
`on_connect` callback, `connect()`, `loop_start()`
(that runs the network in a background thread), then
`publish()` whenever you please.

```
python3 sensor_publisher.py
```

```
Connected to broker.
Published 21.5 to home/kitchen/temperature
Published 22.3 to home/kitchen/temperature
Published 23.1 to home/kitchen/temperature
Published 23.9 to home/kitchen/temperature
Published 24.7 to home/kitchen/temperature
Done.
```

## The watcher

[`examples/temperature_watcher.py`](examples/temperature_watcher.py)
subscribes to the same topic and prints each reading;
above 24 °C it also prints the reaction — the spot
where a real setup would open a vent, start a fan, or
send a notification. It subscribes inside
`on_connect`, which matters: if the connection ever
drops and reconnects, the subscription is re-made
automatically. `loop_forever()` then just sits in
the message stream until Ctrl+C.

Start it in its own terminal, then run the publisher:

```
python3 temperature_watcher.py
```

```
Connected. Subscribing to home/kitchen/temperature
home/kitchen/temperature: 21.5 °C
home/kitchen/temperature: 22.3 °C
home/kitchen/temperature: 23.1 °C
home/kitchen/temperature: 23.9 °C
home/kitchen/temperature: 24.7 °C
  -> Too hot (over 24 °C): this is where you'd open the vent or send an alert.
```

Two terminals, two small programs, no server code, no
polling: the sensor publishes when it has something,
the watcher is told the instant it lands. That is
the whole pattern from What MQTT Is, wearing code.

## Notes from the lab

- **Payloads arrive as bytes.** The watcher does
  `float(msg.payload.decode())` — MQTT payloads are
  untyped, so converting is the receiver's job.
- **Buffering surprise:** when the watcher's output
  was redirected to a file in the lab, its prints
  vanished when the program was stopped — Python
  buffers output that isn't going to a terminal.
  In a terminal (as above) it's line-buffered and
  fine; when scripting output to files, use
  `python3 -u` for unbuffered output.
- The paho 2.x callback signatures (with
  `CallbackAPIVersion.VERSION2`) differ from the 1.x
  examples all over the internet — if a snippet from
  a forum throws callback errors, that version drift
  is the first suspect.
