# Troubleshooting

**Scope:** the failures you'll actually meet, symptom →
fix. Messages are verbatim from real runs (Mosquitto
2.0.21) unless marked (documented).

## "Error: Connection refused" (publish and subscribe)

```
$ mosquitto_pub -p 1899 -t home/test -m 'hello'
Error: Connection refused
```

**Symptom:** both clients fail instantly with the
same bare message.

**Fix:** nothing is listening at that address and
port. Work it in order: is the broker running
(the terminal you started it in, or
`systemctl status mosquitto`)? Is it on the port you
think (`ss -ltn | grep 1883`)? Did you aim the
client at the right host and port (`-h`, `-p`)? In
the lab this exact output came from publishing to
port 1899, where no broker exists. Note this message
also appears when a broker *refuses* a connection
for other reasons in older clients — if the broker
is provably up, read its log before assuming the
port is dead.

## "Connection Refused: not authorised."

```
$ mosquitto_pub -u alice -P wrongpass -t home/test -m 'hello?'
Connection error: Connection Refused: not authorised.
Error: The connection was refused.
```

**Symptom:** the broker is reachable — and is saying
no.

**Fix:** credentials. The user isn't in the
broker's `password_file`, the password is wrong, or
you sent no credentials to a broker with
`allow_anonymous false`. The broker deliberately
gives the same answer for "no such user" and "wrong
password." Check the user exists with a known-good
login, re-create it with `mosquitto_passwd` if in
doubt, and remember *every* client needs `-u`/`-P`
now, subscribers included.

## "Error: Invalid publish topic"

```
$ mosquitto_pub -t 'home/+/temperature' -m '21.5'
Error: Invalid publish topic 'home/+/temperature', does it contain '+' or '#'?

Use 'mosquitto_pub --help' to see usage.
```

**Symptom:** publish rejected before it leaves your
machine.

**Fix:** wildcards are for *subscribing* only. A
published message goes to one concrete topic —
replace the `+` with the actual level
(`home/kitchen/temperature`).

## "Error: Invalid subscription topic"

```
$ mosquitto_sub -t 'home/#/temperature' -C 1
Error: Invalid subscription topic 'home/#/temperature', are all '+' and '#' wildcards correct?

Use 'mosquitto_sub --help' to see usage.
```

**Symptom:** subscribe rejected immediately.

**Fix:** the filter is malformed: `#` must be the
final level and stand alone in it (`home/#`, not
`home/#/temperature`), and `+` must occupy a whole
level too (`home/+/temperature`, not
`home/kit+/temperature`).

## "Error: The connection was lost."

**Symptom:** in the lab, this came from aiming a
client at a host name that doesn't resolve
(`no-such-host.invalid`). It also appears when a
connection drops mid-flight.

**Fix:** check the `-h` value — a typo'd hostname
and a genuinely dead network path can wear the same
message. `ping` the host, and confirm you meant
that broker. The plainness of this one is a known
MQTT-client quirk: the interesting detail is in
the broker's log, not the client's.

## "I published it, but nobody received it"

**Fix:** think like the broker. Was anyone
subscribed to that *exact* topic (or a matching
filter) *at publish time*? Messages nobody is
subscribed to are dropped, silently, by design.
Check with the broker's own diary — subscribe to
`$SYS/#` or watch the broker's verbose log — and
compare the publish topic against the subscription
character by character. Case and stray spaces count
(`home/kitchen/temperature` ≠ `Home/kitchen/temperature`).
If late delivery was expected, that's what retained
messages are for (see the Retained chapter); if
delivery to an *offline* subscriber was expected,
that's sessions and QoS 1 (Sessions chapter).

## "The will never fired" / "The will fired but nothing was wrong"

**Fix:** a will publishes only on an *ungraceful*
disconnect — crash, power loss, network drop, or
the keepalive timer expiring. A client that exits
cleanly (Ctrl+C) discards its will by design; the
lab demonstrated both. Conversely, a will that seems
to fire "for no reason" usually means the client is
dying quietly (check its own logs) or its keepalive
is expiring on a lossy link — the broker gives up
after about 1.5× the keepalive interval of silence.

## "My retained message won't go away"

**Fix:** retained messages are cleared by
publishing to the same topic with the retained flag
and an *empty* payload: `mosquitto_pub -t <topic> -r -n`.
Deleting a topic from some admin panel isn't a
thing; the zero-length retained publish *is* the
delete. Also check you cleared the exact topic —
a retained message on `home/kitchen/status` is not
touched by clearing `home/kitchen/Status`.

## "Python prints nothing when I redirect it to a file"

**Fix (from the lab):** Python buffers stdout when
it isn't a terminal; prints sit in the buffer and
die with the process. Run `python3 -u`
(unbuffered), or add `flush=True` to the prints
that matter. In a terminal it's line-buffered and
you'll never see this.
