# MQTT for Mere Mortals

One small protocol quietly carries most of the
world's sensor chatter. **MQTT** is publish and
subscribe: devices pin messages to named channels
called **topics**, a program called a **broker**
forwards them to whoever subscribed, and nobody
needs to know who else is listening. A temperature
sensor doesn't poll and isn't polled — it publishes
`21.5` to `home/kitchen/temperature` and goes back
to sleep.

This guide stands up a real broker (Mosquitto),
publishes and subscribes from the command line, and
then makes the broker do its four best tricks —
wildcards, guaranteed delivery, retained messages,
and a last will for devices that die without
saying goodbye — before writing the whole pattern
in Python and locking the door with passwords.

It assumes you use a terminal and have edited
config files before. Networking basics (what an IP
address and a port are) are assumed; everything
about brokers, topics, and sessions is explained
from zero.

## What this guide covers

- [**What MQTT is**](what-mqtt-is.md) — publish and
  subscribe, the noticeboard idea, and when it's
  the wrong tool
- [**Installing a broker**](installing-a-broker.md) —
  Mosquitto, a small honest config, and proving it's
  listening
- [**Your first messages**](your-first-messages.md) —
  `mosquitto_sub` and `mosquitto_pub`, one message,
  end to end
- [**Topics and wildcards**](topics-and-wildcards.md) —
  the topic tree, and the `+` and `#` wildcards
- [**How sure is delivery? QoS**](qos.md) — QoS 0, 1,
  and 2, with the packet handshakes read from a real
  broker log
- [**Retained messages and the last will**](retained-and-last-will.md) —
  sticky notes for late arrivals, and a message
  sent for the dead
- [**Sessions and queued messages**](sessions-and-queued-messages.md) —
  clean sessions, client IDs, and mail that waits
  for an offline subscriber
- [**Keeping it private**](keeping-it-private.md) —
  password files, the refusal messages, and why the
  broker never faces the internet
- [**MQTT from Python**](mqtt-from-python.md) — a
  publisher and a watcher in paho-mqtt, run for
  real against the lab broker
- [**Where MQTT shows up**](where-mqtt-shows-up.md) —
  Home Assistant, small hardware, and the broker's
  own `$SYS` diary
- [**Troubleshooting**](troubleshooting.md) —
  symptom → fix, with the real error messages
- [**Glossary**](glossary.md) — the terms, collected
  in one place

## What it doesn't cover

Broker clustering and bridging (brokers talking to
brokers), MQTT over websockets, commercial cloud
brokers, and building production IoT fleets. TLS
and ACLs are explained and marked (documented)
rather than run — see below.

## How to use this guide

Everything runnable was run for real (Mosquitto
2.0.21, paho-mqtt 2.1.0): a broker served the lab,
wildcards were matched and missed on purpose, QoS
handshakes were read out of the broker's own
verbose log, a retained message was set, read by a
late subscriber, and cleared, a client was killed
with `kill -9` and its last will arrived, three
messages queued for an offline session and were
delivered on reconnect, a password file refused the
anonymous and the wrong-passworded in the broker's
own words, and the Python publisher and watcher
exchanged live readings. Two boundaries, stated
plainly: the lab's clients were separate programs
on one machine, so a second physical device's
steps are marked **(documented)**, as are systemd
service management (the lab ran the broker in a
terminal) and TLS with real certificates.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Node-RED for Mere Mortals](https://paulsullivan33-dev.github.io/nodered-for-mere-mortals/)
- [Home Assistant for Mere Mortals](https://paulsullivan33-dev.github.io/home-assistant-for-mere-mortals/)
- [ESPHome for Mere Mortals](https://paulsullivan33-dev.github.io/esphome-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/mqtt-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/mqtt-for-mere-mortals/blob/main/LICENSE-CODE).
