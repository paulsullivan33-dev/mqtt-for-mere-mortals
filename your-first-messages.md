# Your First Messages

**Scope:** one subscriber, one publisher, one message —
the whole protocol in miniature. Verified against
Mosquitto 2.0.21 with the broker from the previous
chapter running.

## Subscribe first

Publishing to nobody is legal in MQTT — the broker
just drops messages with no subscribers — so start
the listener first. In a fresh terminal:

```
mosquitto_sub -t first/greeting -v
```

- **`-t`** names the topic to watch:
  `first/greeting`.
- **`-v`** is verbose: print the topic in front of
  each message, so you can see *which* board each
  note came from. Without it you'd get the bare
  payload.

The command sits there, saying nothing. That's a
healthy subscriber: connected, subscribed, waiting.

## Publish

In another terminal:

```
mosquitto_pub -t first/greeting -m 'Hello from the publisher'
```

- **`-t`** names the topic to pin the note to — the
  same topic the subscriber is watching.
- **`-m`** is the message (the payload).

`mosquitto_pub` prints nothing and exits 0 when the
broker accepts the message. Meanwhile, back in the
subscriber's terminal:

```
first/greeting Hello from the publisher
```

That's the entire exchange: a note pinned to
`first/greeting`, delivered by the broker to the one
watcher. Publish a few more, different words — each
arrives as its own line. Ctrl+C stops the subscriber.

## What just happened, precisely

Three programs were involved, and it's worth being
clear about who did what:

- `mosquitto_pub` connected to the broker, handed it
  one message for `first/greeting`, and disconnected.
  It never knew a subscriber existed.
- The **broker** matched the topic against everything
  it's been asked to watch, found one subscription,
  and forwarded a copy.
- `mosquitto_sub` held a connection open and printed
  what the broker sent it.

Nothing about the publisher changes if ten more
subscribers show up, or none. That indifference is
the whole design (see What MQTT Is).

## Two everyday details

**The payload is just bytes.** `21.5`, `on`, a line of
JSON — the broker doesn't inspect or care. Any format
agreement is between the publisher and subscribers.

**Topics are case-sensitive, and spaces count.**
`first/greeting`, `First/Greeting`, and
`first /greeting` are three different boards. Pick a
style for names and keep it; the next chapter is
about how topic names are structured.
