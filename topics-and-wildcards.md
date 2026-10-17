# Topics and Wildcards

**Scope:** topic names as a filing system, and the two
wildcards — `+` and `#` — that let one subscription
watch a whole branch of it. All runs verified against
Mosquitto 2.0.21.

## Topics are paths

A topic is a string of levels separated by slashes:

```
home/kitchen/temperature
home/kitchen/humidity
home/livingroom/temperature
```

Read it like a folder path: broad on the left, specific
on the right. The publisher picks the exact topic; the
subscriber picks what to watch. One subscriber can
watch several topics at once — repeat `-t`:

```
mosquitto_sub -t home/kitchen/temperature -t home/livingroom/temperature -v
```

Publish to each in turn, plus a ringer:

```
mosquitto_pub -t home/kitchen/temperature -m '21.5'
mosquitto_pub -t home/livingroom/temperature -m '20.0'
mosquitto_pub -t home/kitchen/humidity -m '45'
```

The subscriber receives:

```
home/kitchen/temperature 21.5
home/livingroom/temperature 20.0
```

The humidity message appears nowhere: nobody
subscribed to its topic, so the broker dropped it.
Delivery is by **exact topic match** unless the
subscription uses wildcards.

## `+`: exactly one level

A subscription topic with `+` where a level would go
matches any *one* level in that position:

```
mosquitto_sub -t 'home/+/temperature' -v
```

(Single quotes matter: the shell would otherwise
treat some of these characters as its own.) Publishing
the same four messages as before:

```
home/kitchen/temperature 21.5
home/livingroom/temperature 20.0
```

Same two deliveries — but now for a different reason
each time something *didn't* arrive:

- `home/kitchen/humidity` — the last level is
  `humidity`, not `temperature`. No match.
- `home/kitchen/fridge/temperature` (`4.0`, also
  published) — that's *two* levels between `home/` and
  `temperature`. `+` covers exactly one. No match.

## `#`: everything below

`#` must be the last thing in the filter, and matches
the level it sits on plus everything under it:

```
mosquitto_sub -t 'home/#' -v
```

```
mosquitto_pub -t home/garden/shed/temperature -m '12.0'
mosquitto_pub -t home/kitchen/humidity -m '46'
```

```
home/garden/shed/temperature 12.0
home/kitchen/humidity 46
```

Three levels deep, a different branch, a different
final level — all match. `home/#` is "everything in
the house," and on a busy broker it's a firehose:
useful for debugging, rude as a permanent subscription.

## The rules, collected

| Filter | Matches | Doesn't match |
|---|---|---|
| `home/kitchen/temperature` | that topic only | everything else |
| `home/+/temperature` | `home/kitchen/temperature`, `home/garage/temperature` | `home/kitchen/humidity`, `home/kitchen/fridge/temperature` |
| `home/#` | all of the above, any depth | `garage/temperature` (different first level) |

- Wildcards live in **subscriptions only**. Publishing
  to a topic containing `+` or `#` is an error
  (you'll meet the exact message in Troubleshooting).
- `#` goes **last**, alone in its level:
  `home/#/temperature` is invalid.
- Design topics deep and boring: place, device,
  measurement. `home/kitchen/temperature` will still
  make sense in five years; `sensor7/data` won't.

One more branch of the tree deserves a mention: topics
starting with `$` (like `$SYS/broker/uptime`) are the
broker's own noticeboard about itself — uptime,
message counts, client totals. Wildcards at the root
don't match `$` topics; you subscribe to `$SYS/#`
explicitly when you want them.
