# Distributed systems and data

When to read this: more than one process or machine is involved, data must stay correct across them, or you are choosing a database, a queue or a reliability target.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Consistency | **Strong consistency** where money, stock, permissions or anything legally or financially binding is involved. | **Eventual consistency** for feeds, counters, search indexes and caches. Choose it per use case, not once for everything, and say which store is the source of truth. [S-WEB-1] [S-WEB-8] | Strong consistency gives up speed and availability under failure; eventual gives up "everyone sees the same thing right now". |
| Call style | **Synchronous call** when the caller needs the answer now and can live with the callee being down for a moment. | **Asynchronous messages or events** when you want decoupling, to absorb spikes, or to retry safely. [S-WEB-1] [S-WEB-5] | Async gives up simple request and response flow and makes debugging harder; sync couples the caller to the callee's health. |
| Failure handling | **Always**: a timeout on every remote call, a limited number of retries with growing waits, and a circuit breaker or bulkhead around dependencies that fail. Failure is the normal case. [S-WEB-5] [S-WEB-2] | There is no "otherwise": decide the numbers, but never leave a call unbounded. | A little latency and complexity in exchange for not failing everywhere at once. |
| Retries | **Make operations safe to repeat** (idempotent): give each request an ID and ignore duplicates. | Do not retry operations that cannot be made safe; report the failure instead. (general practice) | Idempotency needs storage for request IDs and careful design. |
| Transactions across services | **Keep data that must change together in one service and one database.** | Use a saga (a series of local steps with undo steps) when a business process truly spans services. [S-FND-2] | A saga gives up the simplicity of one transaction and needs compensation logic and monitoring. |
| Database choice | **A relational database** by default for most products: well understood, flexible queries, strong guarantees. [S-WEB-1] [S-WEB-8] | A document, key-value, graph, time-series or search store when the access pattern clearly fits and you can name why a relational design would not. | Each specialised store gives up flexibility and adds another system to run, back up and secure. |
| Replication and partitioning | **Not yet**, until a measurement shows one machine cannot hold the data or the load. | Read replicas first, then partitioning by a key you can defend. [S-WEB-1] | Replication gives up immediate consistency on reads; partitioning gives up easy cross-partition queries and transactions. |
| Splitting a monolith's data | **Split the code first**, then the data, one table or capability at a time. [S-WEB-7] | Keep one database while services are young. | Splitting data gives up joins and easy reporting; you need new ways to combine data. |
| Reliability target | **Set the target first** (a service-level objective, such as "99.9% of requests succeed in a month") and an error budget; let it decide how much reliability work and how fast releases. [S-WEB-2] [S-WEB-3] | For prototypes, write "no target yet" and revisit at launch. | A strict target gives up release speed and costs more to run. |

## Typical shapes

- **One database, one app, a read replica for reports.** Fits most products for a long time.
- **Outbox pattern:** write the business change and an "event to publish" row in the same transaction, then publish from that row. Avoids losing or double-sending events. (general practice)
- **Command and event flow with a queue:** requests become messages, workers process them, results come back through status checks or events.
- **Saga with orchestrator:** one coordinator drives a multi-service process and triggers undo steps on failure. [S-FND-2]
- **Event log as the source of truth:** only when you need a full history and replay; it is a heavy choice. [S-WEB-1]

## Failure modes

- **Retry storms:** every client retries at once and finishes off a struggling service. Use waits that grow and add randomness.
- **Lost or duplicated messages:** assume "at least once" delivery and design for duplicates.
- **Split brain and stale reads:** two parts believe different things about who is in charge or what the latest value is.
- **Clock assumptions:** machines disagree about the time; do not use wall clocks to order important events.
- **The shared bottleneck:** one database, one queue or one third-party API with a limit that everything depends on.
- **Hidden coupling:** a change in one service silently breaks another because contracts are not written down.
- **Untested restore:** backups exist, but nobody has tried restoring them.

## Questions that change the design

- What must never be wrong or lost, and what may be a little late or approximate?
- How much data now and in a year, and how fast does it grow? What is the biggest single query?
- What happens if a part is down for 5 minutes? For an hour?
- Do operations cross more than one team or system? Who owns each piece of data?
- What availability and recovery time do users and contracts expect?

## Checks before you hand it back

- [ ] For each important piece of data, one source of truth is named.
- [ ] Consistency is chosen per use case, and strong consistency is used where money or correctness depends on it.
- [ ] Every remote call has a timeout, a retry limit and a plan for when the dependency is down.
- [ ] Operations that can be repeated are safe to repeat, or are not retried.
- [ ] Anything that spans services has a written approach (single owner, or a saga with undo steps).
- [ ] A reliability target exists, or its absence is written down with a reason.
- [ ] A restore has been tried, or is listed as a launch task.

## Sources
[S-WEB-1] [S-WEB-2] [S-WEB-3] [S-WEB-5] [S-WEB-7] [S-WEB-8] [S-FND-2]
