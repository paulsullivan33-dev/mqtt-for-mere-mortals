# Installing a Broker

**Scope:** installing Mosquitto on Linux, giving it a
small explicit config, and proving it's alive. Every
step verified against Mosquitto 2.0.21 (Ubuntu 24.04).

## Install

```
sudo apt install mosquitto mosquitto-clients
```

That brings three things:

- **`mosquitto`** — the broker itself.
- **`mosquitto_pub`** — a command-line client that
  publishes one message and exits. This guide's test
  instrument, the way `curl` is for web servers.
- **`mosquitto_sub`** — a command-line client that
  subscribes and prints whatever arrives.

Check what you got:

```
mosquitto -h | head -2
```

```
mosquitto version 2.0.21
```

(Debian installs the same packages. Other distros call
them by the same names; the config below is identical.)

## A config on purpose

An installed Mosquitto ships a nearly empty
`/etc/mosquitto/mosquitto.conf`: it turns on
**persistence** (remembering some state across
restarts, in `/var/lib/mosquitto/`), logs to
`/var/log/mosquitto/mosquitto.log`, and reads extra
config from `/etc/mosquitto/conf.d/`. For learning,
explicit beats inherited — this guide runs the broker
from a small config we control. It ships as
[`examples/mosquitto.conf`](examples/mosquitto.conf):

```
listener 1883 127.0.0.1
allow_anonymous true
```

- **`listener 1883 127.0.0.1`** — accept connections
  on the standard MQTT port, 1883, but only from this
  machine. `127.0.0.1` is "this computer"; nothing on
  your network can reach this broker until you widen
  the listener on purpose.
- **`allow_anonymous true`** — clients may connect
  with no username or password. Acceptable *because*
  the listener is localhost-only. The Keeping It
  Private chapter removes this crutch.

On an installed system you'd put the same two lines in
`/etc/mosquitto/conf.d/local.conf` and let the service
run it (documented). For the lab, run the broker in a
terminal where you can watch it:

```
mosquitto -c mosquitto.conf -v
```

```
mosquitto version 2.0.21 starting
Config loaded from mosquitto.conf.
Opening ipv4 listen socket on port 1883.
mosquitto version 2.0.21 running
```

`-v` is verbose logging to that terminal — every
connect and disconnect lands there, which makes the
next chapters much easier to follow. Leave this
terminal running; the broker is up while it is.

**Check** (from a second terminal) that something is
really listening where you think it is:

```
ss -ltn | grep 1883
```

```
LISTEN 0      0          127.0.0.1:1883      0.0.0.0:*
```

`127.0.0.1:1883` in the LISTEN state is the broker,
holding the door — for this machine only.

## Running it for real

A broker you babysit in a terminal is a lab tool. On a
machine that's supposed to serve sensors all day, use
the packaged service instead (documented — the
commands are the distro's, not verified in this lab's
sandbox):

```
sudo systemctl enable --now mosquitto
systemctl status mosquitto
```

With the service, your config belongs in
`/etc/mosquitto/conf.d/local.conf`, edits take a
`sudo systemctl restart mosquitto`, and the log is at
`/var/log/mosquitto/mosquitto.log`. Everything else in
this guide — the clients, the topics, the tricks —
works identically either way, because the clients
can't tell who's babysitting the broker.
