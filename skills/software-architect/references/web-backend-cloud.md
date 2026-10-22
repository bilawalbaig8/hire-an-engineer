# Web, backend and cloud

When to read this: the system is a website, web app, API or backend service, or it will run in the cloud.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| One program or many services | **One program with clean modules** (modular monolith) when the team is small, the domain is still being learned, or you have not measured a need to scale parts separately. [S-WEB-10] [S-WEB-6] | **Separate services** only for a concrete reason: independent scaling, a different release rhythm, team ownership, or fault isolation. Move one slice at a time so each step can be undone. [S-WEB-7] [S-WEB-11] | A monolith gives up independent deployment and scaling. Services give up simplicity: network calls, partial failure, harder tests, more operations. [S-WEB-9] |
| API style | **Resource-oriented REST** (nouns, standard verbs, consistent errors) for most public and mobile-facing APIs. [S-WEB-13] [S-WEB-14] [S-WEB-15] | A typed RPC or a graph query style when clients need many shapes of the same data and you can afford the extra tooling. | REST can mean more round trips; the alternatives are harder to cache and to secure by default. |
| Where state lives | **Stateless services** that keep configuration in the environment and data in a database or cache, so any instance can serve any request. [S-WEB-12] | Sticky sessions or in-memory state only for a measured reason. | Stateless needs a shared store and a little more latency; in-memory state makes scaling and restarts fragile. |
| Where to run it | **A managed platform** (app platform, managed containers, serverless functions) while the team is small: less to operate. | Your own virtual machines or a container cluster when you need control, special hardware, or the platform's limits block you. | Managed platforms give up control and can cost more at high steady load; self-managed gives up the team's time. (general practice) |
| Caching | Cache only what is read often and changes rarely, **with an expiry or an invalidation rule written down**. | Do not cache until a measurement shows a slow or overloaded path. | A cache gives up simplicity (stale data, a second place to be wrong) for speed. |
| Authentication | **A managed identity provider** or a well-known library for sign-in; never invent your own password handling. See `security-architecture`. | Build your own only with a security reviewer and a strong reason. | A managed provider gives up some control and adds a dependency and cost. |
| API changes over time | Version only when you must break clients; add fields, do not rename or remove them; return errors in one consistent shape. [S-WEB-14] [S-WEB-15] | A new version path or header when a break is unavoidable. | Versioning gives up the ability to change freely; supporting two versions costs effort. |
| Review against a framework | Walk the cloud provider's well-architected pillars as a conversation to find gaps (reliability, security, cost, operations, performance, sustainability). [S-FND-19] [S-FND-20] [S-FND-21] | Skip for tiny prototypes, and say so. | The review costs time; its value is the questions, not a score. |

## Typical shapes

- **Modular monolith + one database + one background worker.** The default for most products. Fits: one team, one product, unknown future. Grows by extracting a module into a service only when a trigger fires.
- **Server-rendered site or single-page app + API + database.** Fits content and form products. Keep rendering and API in one codebase until the team splits.
- **Queue-based pipeline.** A request is accepted fast, the slow work happens in a worker. Fits email, image or video processing, imports, reports. See `distributed-data` for retries and idempotency.
- **Serverless functions + managed services.** Fits spiky, low-volume or event-driven work. Watch cold starts, per-request cost and local testing.
- **Backend for a mobile or game client.** A thin API with a database, authentication, and push or queue services. See `mobile` and `game-engine`.

## Failure modes

- **Chatty calls:** one screen causes dozens of requests or database queries (the classic "N plus 1"). Notice early: count queries per request in tests.
- **Shared database between services:** services secretly depend on each other's tables, so you have a distributed monolith.
- **Unbounded lists:** a screen or endpoint that returns everything works with 100 rows and fails at 100,000. Page every list.
- **No timeouts:** one slow dependency holds every worker and takes the whole system down. [S-WEB-5]
- **Cache stampede:** many requests rebuild the same expired value at once.
- **Config and secrets in the repository:** keys committed or printed in logs.
- **One region, one instance, no restore test:** fine for a prototype, a risk for anything people depend on.

## Questions that change the design

- Roughly how many users and requests now, and in a year? Is traffic spiky (launch days, events)?
- Do users log in? Do you hold personal or payment data? Which countries?
- What is the one failure that hurts most? What response time must a normal action meet?
- Who builds and runs this, and how many people? Is there an existing cloud account or provider you must use?
- Are there external systems you must call, and what are their limits?

## Checks before you hand it back

- [ ] The shape is the simplest that meets the scenarios, and the trigger to split is written.
- [ ] Every list is paged and every external call has a timeout.
- [ ] Configuration and secrets come from the environment or a secret store, not the code. [S-WEB-12]
- [ ] Any cache has an expiry or invalidation rule.
- [ ] Sign-in uses a managed provider or a known library.
- [ ] You can name what runs where, and how a new version is released and rolled back.
- [ ] The first thing that breaks at 10 times load is named.

## Sources
[S-WEB-5] [S-WEB-6] [S-WEB-7] [S-WEB-9] [S-WEB-10] [S-WEB-11] [S-WEB-12] [S-WEB-13] [S-WEB-14] [S-WEB-15] [S-FND-19] [S-FND-20] [S-FND-21]
