# Where MQTT Shows Up

**Scope:** where this protocol actually lives in the
wild, so you can recognize it — and a pointer at what
a second device looks like. This chapter is context,
marked (documented) where it describes systems the
lab didn't run.

## Home Assistant (documented)

The biggest mortal habitat. Home Assistant — the
home-automation platform — uses MQTT as one of its
main ways to talk to devices:

- **Devices publish state, assistants subscribe.**
  A Zigbee or Wi-Fi sensor reports through an
  MQTT bridge (Zigbee2MQTT is the common one) onto
  topics like `zigbee2mqtt/kitchen_sensor`, and Home
  Assistant watches them. If you ran Zigbee2MQTT,
  your broker is already the busiest program in
  the house.
- **Availability is the Last Will at work.** Devices
  (via their bridge) keep a retained `online` on an
  availability topic and register a will that flips
  it to `offline` — precisely the pattern from the
  Retained and Last Will chapter. When Home
  Assistant shows a device greyed out as
  "unavailable," that machinery is what it's
  reading.
- **Discovery topics** (`homeassistant/...`) let
  devices announce *themselves* — name, units, what
  they measure — so they appear in the UI without
  hand-written configuration.

If you already run Home Assistant with any MQTT
integration, you don't need a second broker story:
the guide's lab broker and an automation broker are
the same program wearing different configs.

## Small hardware (documented)

MQTT's original constituency. Microcontrollers —
ESP8266, ESP32, Arduino boards with network shields,
Raspberry Pi in sensor duty — speak it through small
client libraries (PubSubClient is the Arduino
staple). The shape never changes:

1. Connect to the broker (Wi-Fi first, then MQTT).
2. Publish readings to a topic per measurement.
3. Subscribe to a command topic if the device also
   *does* things — a relay, a valve, a light.

A garden sensor that publishes
`home/greenhouse/temperature` and a script that
subscribes and waters when it's hot is the guide's
Python chapter with the pretend sensor replaced by
a real one. Nothing else in the system notices the
swap — that's the payoff for publishing to topics
instead of to programs.

## Elsewhere you'll trip over it

- **Chat and presence systems** historically used
  MQTT (Facebook Messenger's early mobile messaging
  did) because it's gentle on batteries and bad
  networks.
- **Industrial telemetry** — its birthplace. Remote
  sensors on pipelines, farms, and factory floors
  still report this way, often via MQTT's sibling
  profile Sparkplug.
- **Your broker itself:** subscribe to `$SYS/#`
  sometime on a live broker (see Topics and
  Wildcards) and watch it report its own uptime,
  message rates, and client counts. Every Mosquitto
  keeps this diary.

## The honest boundary

This guide built everything on one machine:
publisher, subscriber, and broker as neighbors on
localhost. Real deployments differ in exactly the
ways the Keeping It Private chapter covers —
passwords on, listener widened to the LAN on
purpose, never to the internet, TLS if the traffic
must cross anything untrusted. The protocol
exchanges are identical; only the audience changes.
