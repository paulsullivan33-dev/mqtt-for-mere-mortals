# Keeping It Private

**Scope:** passwords on the broker (verified live),
and the security posture that's actually appropriate
for a home MQTT setup — including the one rule that
matters most. Password runs verified against
Mosquitto 2.0.21.

## The one rule first

**Do not expose an MQTT broker to the internet.**
Port 1883 sends everything — passwords included — as
plain text, and scanners sweep for open brokers
constantly. A broker on your home network, reachable
from your network, is a reasonable tool. A broker
port-forwarded to the world is a public noticeboard
that anyone can read and pin to — including the
topics that open your garage. If you ever need MQTT
from away, reach home some safer way (a VPN such as
Tailscale or WireGuard) and keep the broker private.
This chapter's passwords are a lock on an inside door:
worth having, not a substitute for the house lock.

## Passwords with mosquitto_passwd

The lab's broker so far lets anyone in
(`allow_anonymous true`). Give it accounts instead.
`mosquitto_passwd` maintains the password file; `-c`
creates it (and wipes any existing file!):

```
mosquitto_passwd -c /etc/mosquitto/passwd alice
mosquitto_passwd /etc/mosquitto/passwd bob
```

Each asks for the password interactively. (Scripts
can use `-b` with the password on the command line —
convenient, and visible in your shell history;
choose consciously.) The file it writes never holds
plain text:

```
alice:$7$101$JoBZ9+Dh8gXFmuSz$33mQIBMQOQMgIqxg5/jvB8O36zqhes...
```

That's a salted hash: the broker can check a password
against it, but the file itself doesn't reveal the
password. Treat it as sensitive anyway — hashes can
be attacked offline.

Now point the broker at it and close the anonymous
door. The full config ships as
[`examples/mosquitto-secure.conf`](examples/mosquitto-secure.conf);
the load-bearing lines:

```
listener 1883 127.0.0.1
allow_anonymous false
password_file /etc/mosquitto/passwd
```

Restart the broker (or service). What changes, as
seen from the clients — first, no credentials at all:

```
$ mosquitto_pub -p 1884 -t home/test -m 'can anyone hear me?'
Connection error: Connection Refused: not authorised.
Error: The connection was refused.
```

(That run used a side port, 1884, so both brokers
could live at once.) A *wrong* password gets exactly
the same refusal — the broker deliberately doesn't
say which part failed:

```
$ mosquitto_pub -u alice -P wrongpass -t home/test -m 'hello?'
Connection error: Connection Refused: not authorised.
Error: The connection was refused.
```

And the right one passes silently, as `mosquitto_pub`
does, while the message lands with a subscribed
second user (note *both* clients authenticate now,
publisher and subscriber alike):

```
home/test authenticated hello
```

Clients present credentials with `-u` and `-P`.

## Finer control, and encryption (documented)

Two next steps exist beyond this chapter's lab, and
are described rather than run here — flagged
honestly:

- **ACLs** (documented): a password says who may
  connect; an access-control list says what each
  user may publish or subscribe to — the sensor that
  may write `home/sensors/#` but never actuate
  `home/locks/#`. Mosquitto does this with an
  `acl_file`; the shape is one `user` section per
  account with `topic readwrite ...` lines.
- **TLS** (documented): on port 8883 (the standard
  MQTT-over-TLS port), the broker presents a
  certificate and the whole conversation — passwords
  included — is encrypted. Clients connect with
  `--cafile` (or the system store) and `-p 8883`.
  This is *the* requirement if a broker must ever
  cross an untrusted network, and it pairs with
  passwords: TLS protects the wire, passwords decide
  who's welcome. Getting a certificate (an internal
  CA or a public one) is a procedure of its own —
  see the SSH and Caddy guides' treatment of keys
  and certificates for the underlying ideas.

Within one trusted LAN, passwords plus a
non-internet-facing broker is a sane, mortal setup.
Know that every password crosses that LAN in the
clear on 1883, and decide whether your network
earns that trust.
