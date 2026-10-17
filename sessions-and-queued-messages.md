# Sessions and Queued Messages

**Scope:** what a "session" is, what *clean session*
throws away, and the broker holding mail for a
subscriber that's temporarily gone. Demonstrated
against Mosquitto 2.0.21.

## The problem

A subscriber that disconnects — laptop lid closed,
Wi-Fi dropout, program restarted — misses everything
published while it was away. Sometimes that's fine
(the next sensor reading is seconds away). Sometimes
it isn't (the missed message was "the package
arrived"). Sessions are how a subscriber tells the
broker: *don't forget me while I'm gone.*

Two ingredients are required:

- **A stable client ID** (`-i`). With no `-i`, the
  clients invent a random ID per run, so the broker
  can't know you're the same client returning.
- **Clean session off** (`-c` to `mosquitto_sub`).
  By default, connecting *cleans* the slate: the
  broker discards whatever it remembered about your
  ID. With clean session off, the **session** —
  your subscriptions, and messages queued for you —
  survives disconnects.

And one rule: only **QoS 1 and 2** messages are
queued for an absent subscriber. QoS 0 is
fire-and-forget even here — the broker won't store
what the publisher didn't ask it to guarantee.

## The demonstration

First connect — this creates the session and goes
away having received nothing:

```
timeout 2 mosquitto_sub -i hallway-display -c -q 1 -t home/notifications -v
```

Now the client is *offline*. Three messages are
published at QoS 1:

```
mosquitto_pub -q 1 -t home/notifications -m 'Package delivered'
mosquitto_pub -q 1 -t home/notifications -m 'Water the plants'
mosquitto_pub -q 1 -t home/notifications -m 'Bin night tonight'
```

Reconnect — same ID, clean session still off:

```
mosquitto_sub -i hallway-display -c -q 1 -t home/notifications -v
```

```
home/notifications Package delivered
home/notifications Water the plants
home/notifications Bin night tonight
```

All three, in order, the moment the session resumed.
The broker was the only thing holding them; no
publisher knew or cared.

## What to remember

- Session state belongs to the **client ID**. Two
  programs using the same ID kick each other off and
  inherit each other's mail — give every real client
  its own ID.
- `-q 1` on the *subscription* matters too: the
  queued delivery is capped at the subscription's
  QoS, so subscribe at the level you want stored.
- Sessions are not forever. Brokers cap how much
  they'll queue for an absent client (Mosquitto's
  defaults are finite; a client that never returns
  leaks until the broker reclaims it). Treat queued
  messages as a safety net for minutes-to-days
  absences, not as an archive — an archive is a
  database with an MQTT subscriber in front of it.
- If you *want* a clean slate every time (a
  debugging subscriber, say), the defaults already
  do that: no fixed ID + clean session on means
  nothing survives, nothing queues.
