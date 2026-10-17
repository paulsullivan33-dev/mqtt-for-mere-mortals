# Retained Messages and the Last Will

**Scope:** two broker kindnesses for a world where
things aren't always on — a message that waits for
late arrivals, and a message sent on behalf of the
dead. Both demonstrated live against Mosquitto
2.0.21.

## Retained: the sticky note

Normally a broker forwards a message and forgets it.
A **retained** message is kept — one per topic — and
handed immediately to every *new* subscriber. Think
of the difference between a shout and a sticky note
on the noticeboard: the sticky note is still there
when you arrive late.

Publish one (note the `-r`):

```
mosquitto_pub -t home/kitchen/status -r -m 'online'
```

Nothing subscribes yet, and this time that doesn't
matter. Now subscribe, *after* the fact:

```
mosquitto_sub -t home/kitchen/status -v -C 1
```

```
home/kitchen/status online
```

Delivered at once, even though the publisher is long
gone. (`-C 1` tells `mosquitto_sub` to exit after one
message.) This is how dashboards learn the current
state of everything the moment they connect, without
every sensor re-announcing itself.

Two properties worth burning in:

- **One retained message per topic.** A second
  retained publish replaces the first.
- **Clearing it is a publish too** — a retained
  message with an empty payload. `mosquitto_pub`'s
  `-n` sends exactly that:

```
mosquitto_pub -t home/kitchen/status -r -n
```

After that, a new subscriber to
`home/kitchen/status` hears nothing at all — the lab
confirmed it by subscribing for three seconds and
receiving zero bytes.

The classic retained topic is *state*: `.../status`,
`.../state`, the current temperature. The classic
mistake is retaining *events* — a retained "doorbell
rang" re-rings, misleadingly, for every late
subscriber forever.

## The Last Will: a note in case of death

When a client connects, it may register a **Last
Will and Testament**: a topic and a message that the
broker will publish *for* it if the client ever
vanishes without saying goodbye — power cut, network
dropped, program crashed. A clean disconnect throws
the will away, unpublished.

The lab set a watcher on an alerts topic:

```
mosquitto_sub -t home/alerts -v
```

…and connected a pretend sensor whose will is
registered with `--will-topic` / `--will-payload`:

```
mosquitto_sub -i greenhouse-sensor -t home/greenhouse/heartbeat \
    --will-topic home/alerts \
    --will-payload 'greenhouse-sensor disconnected unexpectedly' \
    --will-qos 1
```

Then the sensor's process was killed with `kill -9`
— the rudest death there is, no cleanup, no goodbye.
The watcher's terminal:

```
home/alerts greenhouse-sensor disconnected unexpectedly
```

The will arrived verbatim. And the contrast the lab
also ran: reconnect the same client and stop it
politely (Ctrl+C / SIGINT). The watcher received
*nothing* — a clean exit discards the will, exactly
as designed.

This is the standard "is it alive?" machinery of
MQTT: devices publish a retained `online` to their
status topic and register a will that publishes
`offline` to the same topic. Subscribers then always
know — current state from the retained message, and
an automatic update the moment a device drops dead.
Home Assistant device availability works this way,
among many others.

Caveats, plainly: the broker detects a rude death
when the connection breaks or the keepalive timer
runs out, so a will can lag a genuinely silent
failure by up to the keepalive interval (60 seconds
by default in these clients). And a will is a normal
message — it follows the usual rules, including
being retainable if you ask (`--will-retain`).
