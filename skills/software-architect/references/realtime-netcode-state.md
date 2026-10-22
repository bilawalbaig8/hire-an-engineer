# Real-time systems, netcode, state machines and messaging

When to read this: the system must react quickly or continuously (multiplayer games, live collaboration, chat, trading, device control), or it has long-lived behaviour best described as states and events (screen flows, game AI, connections, workflows).

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Who owns the truth | **The server owns the state** and clients send intentions, when fairness, money or cheating matters. [S-GAME-14] [S-GAME-13] | **The client owns its own state** for co-op or casual games and tools where cheating is cheap to tolerate. | Server authority gives up some instant feel (fixed by prediction) and costs servers. Client authority gives up cheat resistance. |
| Sync model | Pick by genre and player count: **lockstep** (only inputs cross the network and everyone simulates the same game; few players, many units, exact determinism needed), **snapshots** (the server sends state many times a second; fits action games), **prediction with reconciliation** (the client guesses locally and corrects when the server disagrees; fits fast games). [S-GAME-13] [S-GAME-14] [S-GAME-15] | Turn-based or slow games can use plain request and response, but plan how turns reach the other players, how a player who dropped rejoins and catches up, and send each client only what it may see (for example hidden cards). | Lockstep gives up flexibility and needs exact determinism; snapshots give up bandwidth; prediction gives up simplicity and shows corrections. |
| Time | **A fixed tick on the server** (a steady number of simulation steps per second) and timestamps on messages; clients interpolate for display. [S-GAME-14] | A variable step only for non-critical visuals. | A fixed tick gives up some flexibility; it makes behaviour predictable and testable. |
| Transport | **Unreliable fast messages for frequently refreshed state** (positions), **reliable ordered messages for events that must arrive** (purchases, deaths, chat). | One reliable stream for everything when volume is low. | Mixed transport adds code; a single reliable stream can stall on loss (late data blocks new data). |
| Lag handling | **Design for latency**: interpolation, prediction, and (for hit detection) rewinding the server's view to what the shooter saw. [S-GAME-15] | Accept the delay in slow-paced games. | Lag compensation gives up some fairness to the player being hit; ignoring latency gives up playability. |
| Long-lived behaviour | **Model it as an explicit state machine** (states, events, allowed transitions, entry and exit actions); use nested states when it grows. [S-RT-2] | Plain if-statements for two or three states. | State machines give up a little quick-and-dirty speed for behaviour you can test and draw. |
| Module communication | **Events or messages between modules**, not shared mutable state; keep one owner for each piece of state. [S-RT-1] | Direct calls inside one module. | Events give up easy stepping through calls. |
| Very low latency core | **Consider a single-threaded core that processes events in order from a queue** when latency and predictability matter most and the state fits in memory. [S-RT-1] | Ordinary multi-threaded services when throughput matters more. | A single writer gives up parallel speed on one core; it removes a whole class of locking bugs. |
| Messaging patterns | Use well-known message patterns (channels, routers, idempotent receivers) rather than inventing ad hoc ones. (unverified source S-RT-3 is the standard catalogue; an unverified manifesto S-RT-4 gives a checklist of qualities) | Direct function calls for in-process work. | Patterns give up some directness for decoupling. |

## Typical shapes

- **Authoritative server with client prediction:** server tick, input messages from clients, state snapshots back, client-side prediction and correction.
- **Relay or lockstep room:** a small server only forwards inputs; clients run identical deterministic simulations. Needs exact determinism.
- **Peer-to-peer with host:** one player is the server; cheapest, least cheat-proof, host leaves = session ends.
- **State-machine-driven UI or AI:** a table of states, events and transitions drawn as a diagram, tested by walking every transition.
- **Event-driven collaboration:** each client sends operations, a server orders them and broadcasts, with a documented rule for conflicts.

## Failure modes

- **Teleporting and rubber-banding:** prediction and correction disagree, or corrections are too abrupt.
- **Desync:** clients diverge because of non-deterministic code (floating point differences, unordered iteration, local time).
- **Lag spikes stall everyone** because one slow client blocks a lockstep game or a reliable stream.
- **Trusting the client:** speed, damage or inventory values accepted from clients.
- **Message floods:** unbounded queues grow until the server dies; no limits per client.
- **State machines with hidden states:** flags scattered around the code that nobody can list.
- **Untested networks:** only tried on a fast local connection.

## Questions that change the design

- How many players or users interact at once, and how fast is the action (turn-based to twitch)?
- What happens if one player's connection is bad? If the server restarts mid-session?
- Does cheating or tampering cost money or fairness?
- Must behaviour be reproducible (replays, tests, audits)?
- What are the latency and update-rate targets, measured where?

## Checks before you hand it back

- [ ] Who owns each piece of state is written down.
- [ ] The sync model is named and justified for the genre and player count.
- [ ] Time is handled with a fixed tick or clear timestamps.
- [ ] Reliable and unreliable messages are chosen per message type.
- [ ] The design was reasoned through with 200 ms of latency and 5% packet loss, and the behaviour is described.
- [ ] Queues and rates have limits per client and per server.
- [ ] Every long-lived behaviour has a drawn state machine with all transitions listed.

## Sources
[S-GAME-13] [S-GAME-14] [S-GAME-15] [S-RT-1] [S-RT-2] and, as unverified leads only, S-RT-3 and S-RT-4
