# How Sure Is Delivery? QoS

**Scope:** MQTT's three delivery promises — QoS 0, 1,
and 2 — what each actually guarantees, and the packet
exchanges that prove it, read from a real broker log.
Verified against Mosquitto 2.0.21.

## Three grades of promise

Every publish carries a **Quality of Service** level.
It's a contract between the sender and the broker
(and again between the broker and each subscriber):
how hard everyone tries to deliver.

- **QoS 0 — at most once.** "Fire and forget." The
  message is sent once; if it's lost on the way,
  it's gone. No acknowledgment, no retry.
- **QoS 1 — at least once.** The sender keeps the
  message until the receiver acknowledges it
  (`PUBACK`), and resends if the acknowledgment
  doesn't come. Delivery is guaranteed; *duplicates
  are possible* if the acknowledgment is what got
  lost.
- **QoS 2 — exactly once.** A four-step handshake
  (`PUBREC`, `PUBREL`, `PUBCOMP`) makes sure the
  message is delivered once and only once. The
  strongest promise, and the slowest.

The flag is `-q` to both clients. One subscriber
asking for QoS 2, three publishes at the three levels:

```
mosquitto_sub -q 2 -t qos/test -v
mosquitto_pub -q 0 -t qos/test -m 'sent at QoS 0'
mosquitto_pub -q 1 -t qos/test -m 'sent at QoS 1'
mosquitto_pub -q 2 -t qos/test -m 'sent at QoS 2'
```

All three arrive. From the subscriber's chair the
levels are indistinguishable — the difference is in
the plumbing, which the broker's log shows if you run
a broker with `log_type all` (the lab did exactly
this on a side port). Publisher side, one line per
packet:

**QoS 0** — a single packet, no reply:

```
Received PUBLISH from auto-... (d0, q0, r0, m0, 'qos/test', ... (13 bytes))
```

**QoS 1** — publish, then an acknowledgment back:

```
Received PUBLISH from auto-... (d0, q1, r0, m1, 'qos/test', ... (13 bytes))
Sending PUBACK to auto-... (m1, rc0)
```

**QoS 2** — the four-step dance:

```
Received PUBLISH from auto-... (d0, q2, r0, m1, 'qos/test', ... (13 bytes))
Sending PUBREC to auto-... (m1, rc0)
Received PUBREL from auto-... (Mid: 1)
Sending PUBCOMP to auto-... (m1)
```

(The same exchanges repeat on the delivery side,
between broker and subscriber, at the *lower* of the
publish QoS and the subscription's QoS. A QoS 2
publish delivered to a QoS 0 subscription travels
the last hop as QoS 0 — the promise only covers the
legs that ask for it.)

## Which to use

| Level | Guarantee | Typical use |
|---|---|---|
| 0 | maybe once | frequent sensor readings — the next one is seconds away and a gap doesn't matter |
| 1 | at least once (duplicates possible) | commands, alerts, notifications — things that must arrive, where hearing it twice is harmless |
| 2 | exactly once | rare: an action that must happen once and only once, when the extra chatter is worth it |

Working rules of thumb:

- Most real systems live at QoS 0 and 1. QoS 2's
  certainty costs four packets per message per hop,
  and "exactly once" rarely matters as much as
  people first think.
- Duplicates at QoS 1 are not a bug — they're the
  price of the guarantee. Subscribers that act on
  commands should tolerate hearing one twice.
- QoS is also what makes the broker hold messages
  for offline subscribers — which is the next
  chapter but one (Sessions and Queued Messages).
  A QoS 0 message for an absent subscriber is
  simply gone.
