# Glossary

**ACL (access control list)** — per-user rules about
which topics a client may publish or subscribe to.
Passwords decide who connects; ACLs decide what
they may touch.

**Broker** — the server in the middle. Accepts
published messages and forwards them to subscribers.
This guide's broker is Mosquitto.

**Clean session** — connecting with a clean slate:
the broker forgets your subscriptions and anything
queued. Turn it off (`-c` to `mosquitto_sub`) and
your session survives disconnects.

**Client** — anything that connects to a broker:
a program, a sensor, a phone app. Clients publish,
subscribe, or both.

**Client ID** — a client's name tag with the
broker. Sessions are keyed to it; two clients
sharing one ID kick each other off.

**Keepalive** — a timer on the connection. If a
client is silent too long (about 1.5× the
interval), the broker declares it gone — and
publishes its will.

**Last Will and Testament (LWT)** — a message a
client registers at connect time, which the broker
publishes on its behalf only if the client
disconnects ungracefully.

**mosquitto** — the broker. Also the name of the
whole project, which includes the command-line
clients.

**mosquitto_pub / mosquitto_sub** — the project's
command-line clients: publish one message, or
subscribe and print. This guide's test instruments.

**mosquitto_passwd** — the tool that creates and
edits the broker's password file (salted hashes,
never plain text).

**paho-mqtt** — the Eclipse Paho client library for
Python; the guide's code chapters use it.

**Payload** — the body of a message. Untyped bytes
as far as the broker is concerned: `21.5`, `on`, or
a line of JSON are all the same to it.

**Publish** — sending a message to a topic.

**QoS (Quality of Service)** — the delivery promise
on a message: 0 = at most once, 1 = at least once
(duplicates possible), 2 = exactly once, paid for
with a four-packet handshake.

**Retained message** — a message the broker keeps
(one per topic) and hands to every new subscriber
immediately. Cleared by a retained publish with an
empty payload.

**Session** — what the broker remembers about a
client ID across disconnects: its subscriptions
and (for QoS 1/2) messages queued while it was away.

**Subscribe** — registering interest in a topic (or
a wildcard filter); the broker forwards matching
messages for as long as the session lasts.

**$SYS** — the broker's own topics
(`$SYS/broker/uptime` and friends): its diary of
itself, subscribable like any other tree but never
matched by root wildcards.

**Topic** — the channel a message is published to:
slash-separated levels, broad to specific
(`home/kitchen/temperature`). Matching is exact and
case-sensitive unless the subscription uses
wildcards.

**Wildcard** — subscription-only pattern matching:
`+` stands for exactly one topic level, `#` (final
level only) for everything below.
