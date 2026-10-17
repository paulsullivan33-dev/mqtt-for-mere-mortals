# What MQTT Is

**Scope:** the one idea underneath the whole protocol —
publish and subscribe — and an honest look at when it's
the wrong tool.

## Messages without addresses

Most network talk is addressed: your browser asks a
specific server a question and waits for its answer.
MQTT throws the addressing away. A device with something
to say **publishes** a message to a named channel called
a **topic** — say, `home/kitchen/temperature`. It doesn't
know or care who is listening. Any device that has
**subscribed** to that topic receives a copy. The
publisher and the subscribers never meet; they may not
even be switched on at the same time of day.

The program in the middle that accepts messages and
forwards them to subscribers is the **broker**. It's a
small, boring, single-purpose server — the guide's lab
uses Mosquitto, the most common one — and everything in
MQTT goes through it.

Picture a community noticeboard hall:

- Each **topic** is one board, with a name on it.
- **Publishing** is pinning a note to a board.
- **Subscribing** is standing watch over a board — or
  several — and reading every new note pinned there.
- The **broker** is the hall: it holds the boards,
  remembers who's watching which, and makes sure new
  notes reach the watchers.

Nobody writes a note *to* anybody. A temperature sensor
doesn't need to know that a dashboard, a logger, and a
heating controller all care about its readings — it
pins the number to its board and gets on with its life.
Adding a fourth listener changes nothing for the sensor.

## Why this shape exists

MQTT was designed in 1999 for oil-pipeline sensors on
expensive, flaky satellite links, and it shows in the
best way:

- **Tiny messages.** A reading can be a few bytes —
  `21.5` — with very little wrapping. Nothing like a
  web page changes hands.
- **The chatty side sleeps.** A sensor can wake, pin
  one note, and power down. It never waits around
  answering questions.
- **The broker remembers.** Notes can be kept for late
  arrivals (retained messages), delivered reliably
  even across dropouts (QoS and sessions), and a
  device that vanishes can leave a pre-written "I
  died" note behind (the Last Will). Later chapters
  demonstrate each of these, for real.

The vocabulary, collected: **publish**, **subscribe**,
**broker**, **topic**, and **client** — anything that
connects to a broker, whether it publishes, subscribes,
or both. One machine usually runs several clients.

## When MQTT isn't the answer

Honesty section, per house rules:

- **Asking a question and needing *the* answer.** "Is
  the door locked *right now*?" is a request with a
  reply, which is what web APIs do well. MQTT can fake
  it (publish a question topic, subscribe to an answer
  topic), but it's swimming upstream.
- **Moving files or big payloads.** MQTT messages are
  meant to be small. A photo, a log archive, a backup —
  that's `rsync`, a web server, or a share (see *Samba
  and NFS for Mere Mortals*).
- **A permanent record.** A broker is a postman, not a
  filing cabinet. If every reading must be kept
  forever, something must subscribe and write it to a
  database — MQTT itself is the delivery, not the
  archive.

What it's *for*: many small things reporting in, being
controlled, or reacting to each other — sensors,
switches, dashboards, home automation, and the whole
Internet of Things menagerie. The rest of this guide
builds one on your own machine and makes it do tricks.
