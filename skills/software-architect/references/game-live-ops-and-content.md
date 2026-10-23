# Game live operations and content

When to read this: the game changes after release (new content, events, tuning, experiments), earns money (purchases, ads, random rewards), or ships through app stores that set rules. Part of the games set: start at `game-engine.md`. Think of two halves: what you can change **without a store release** (content, config) and what must be **checked by a server** (money and fairness).

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Content delivery | **Downloadable content bundles** (Unity Addressables, Unreal chunks and Asset Manager) hosted on a CDN, for big or frequently changed content. [S-GAME-42] [S-GAME-43] [S-GAME-47] | Everything in the app build for small, rarely updated games. | Bundles give up simplicity: you need hosting, versioning, a download UX and an offline plan. In-app content gives up update speed and a small install. |
| Tuning without release | **Remote configuration**: key-value settings the app fetches at start, with baked-in defaults. [S-GAME-23] [S-GAME-95] | Constants changed only by a new build. | Config gives up a single reviewed source of truth: a bad value goes live instantly. Needs validation, staged rollout and a kill switch. |
| Feature flags | **Short-lived release flags and permanent kill switches**, each with an owner and a removal date. [S-GAME-93] | None in tiny games. | Flags are inventory with a carrying cost; too many make the game untestable. |
| Experiments | **Server-assigned A/B groups, event data analysed with sound statistics**, when you are changing something that affects revenue or retention. [S-GAME-94] | Ship-and-watch for small changes. | Experiments give up speed and need traffic; poor design gives wrong answers that look right. |
| Money and fairness | **The server owns every balance, purchase result and random outcome** in any game with real-money spending, tradable items or rankings. [S-GAME-76] | Client-owned for fully offline single-player games with only cosmetic purchases. | Server authority costs servers, latency, support tools and engineering; client authority gives up cheat resistance and revenue protection. |
| Backend | **A hosted game-backend service** when the team is small and the needs are standard (accounts, saves, config). [S-GAME-22] [S-GAME-23] | **Your own backend** when rules are custom (gacha, economy, events) or you need portability. | Hosted services give up control and can cost more at scale (check terms); own backend gives up engineering time and on-call duty. |
| Versioning | **Separate version numbers** for app, content, config, save format and server API, with a minimum supported version and a forced-upgrade path. | One version for everything in small games. | More numbers to track; a single number hides which part is incompatible. |

## Content pipeline and asset bundles

- **The chain:** source art and data, then an automated build, then versioned bundles, then a CDN, then the game's download and cache logic. Automate every step so a release does not depend on one person's machine.
- **Unity Addressables:** assets are loaded by address, bundles can be hosted remotely, a catalog says where each asset is, and a **content update build** ships only what changed. [S-GAME-42] [S-GAME-43] Every load needs a matching release, and memory returns only when the whole bundle can unload, so group assets that are used together. [S-GAME-41] Cost: build complexity, a catalog and a hosting setup, and async loading everywhere.
- **Unreal:** the Asset Manager, primary assets and chunking control what goes in the build and what downloads later; Game Feature plugins add gameplay modules. [S-GAME-47] [S-GAME-49] **Platform stores** also offer their own ways to deliver large assets (Apple's Background Assets, Google's asset delivery for app bundles). [S-GAME-82] (Google's asset delivery page was not verified here.)
- **Content versus code:** data and assets may change after release, but app code generally may not be downloaded and run. Store rules limit this, so read the current rules before designing a scripting or hot-patch system. [S-MOB-7] [S-MOB-8] (details not verified here)
- **Compatibility:** content bundles are built against a specific app version; keep a table of which content versions each app version can load, and do not ship content that an old app cannot read. [S-GAME-43]
- **Offline and failure:** the game must start with what is on the device, show a clear message when a download fails, resume partial downloads, and never block play for non-essential content. Test on a slow connection.
- **Size and cost:** compress, deduplicate shared assets, and set a cap on first download; CDN cost scales with downloads times size, so patch only what changed.

## Remote config and feature flags

- **Defaults baked in:** the app must work if the fetch fails; values are cached with a time limit.
- **Typed and validated:** each key has a type, a range and an owner; the server rejects out-of-range values; the client ignores values it does not recognise.
- **Target and stage:** roll out to a small percentage, then more; target by app version, platform, country and player segment; keep a **kill switch** for each risky feature. [S-GAME-23] [S-GAME-95] [S-GAME-93]
- **Flag types and lifespans:** release flags (days to weeks), experiment flags (the experiment), operational switches (permanent), permission flags (permanent). Record an owner and an expiry for each; remove dead ones. [S-GAME-93]
- **Config is not a secret store.** Anything the client downloads can be read, so do not put keys, secret odds logic or exploitable pricing rules in it. (general practice)
- **Audit and rollback:** log who changed what and when; make rollback one click.
- What it gives up: a typo can change every player's game within minutes, so treat config like code (review, staging, gradual rollout).

## Analytics events and A/B tests

- **Design events as a schema, not as logs.** Every event has a name from a controlled list, a version, a timestamp, a unique event ID (so repeats can be dropped), the app and content versions, the platform, a pseudonymous player ID, a session ID, and the experiment groups the player is in. Parameters are typed.
- **Core events:** session start and end, tutorial steps, level start and result, economy sources and sinks (every currency gained and spent, with reason), store views and purchases, ad views, errors and crashes, performance samples (frame time, memory by device model). [S-GAME-71]
- **Batch, queue offline, and sample** high-volume events; set a cap on size. Never block gameplay on analytics.
- **Privacy:** collect only what you need, follow the age and region rules, and let players opt out where the law or the stores require. Confirm with the owner's legal adviser. [S-MOB-7] [S-MOB-8]
- **A/B tests:** decide the question, the main metric, a guardrail metric (such as crash rate or retention), the sample size and the run length **before** starting; assign on the server or deterministically from the player ID; check that group sizes match what was planned; do not stop early on a good-looking number. [S-GAME-94]
- **Do not mix tests that touch the same thing**, and do not run them on small populations that cannot show an effect.
- A hosted analytics service is fine for starting; keep the event schema yours so you can move. [S-GAME-24]
- What it gives up: every event is a commitment (names, meaning, storage cost); renaming later breaks dashboards. **The event names and meanings are close to a one-way door.**

## Economy and server authority

For games with real-money purchases, random rewards or shared state, the client is untrusted. [S-GAME-76]

| Must be on the server | May stay on the client |
|---|---|
| Currency balances and every earn and spend (as a ledger with reasons) | Settings, UI state, graphics options |
| **Purchase verification** and the grant of what was bought (verify the store receipt or token on the server; a purchase token is unique, so store and reject repeats) [S-GAME-76] [S-GAME-84] | Showing the shop and prices (from server config) |
| **Random outcomes with value** (gacha rolls, loot) and the pity counters, using a server-side random source; keep a log | Visual effects of the result |
| Rewards for ads, timers that skip with paid currency, daily bonuses (use server time) | Local timers for cosmetic things |
| Inventory that can be traded, gifted or counts toward rankings | Cosmetic-only unlocked state in a single-player game |
| Leaderboards, matchmaking and match results | Predictions shown before the server confirms |
| Prices, drop tables and odds (as versioned server data) | Cached copies for display |

How:
- **Idempotent operations:** every purchase or spend carries a unique request ID; the server applies each ID once, so retries and crashes never charge or grant twice.
- **Ledger, not just a balance:** record events; a balance is the sum, which makes disputes, refunds and fraud review possible.
- **Odds disclosure:** both major stores require telling players the odds of randomised paid items before purchase. [S-MOB-7] [S-GAME-77] Keep the odds in the same versioned data the server uses to roll, so the shown and real odds cannot drift apart, and keep a history of past versions.
- **Attestation** (Play Integrity, App Attest) lets the server reject requests from modified apps or fake devices; it is a layer, not a guarantee. [S-GAME-75] [S-GAME-83] [S-GAME-86]
- **Refunds, chargebacks and bans:** design reversal of a grant from day one.
- **Offline play with a server economy:** either block the economy offline, or queue events and let the server accept or reject them later; decide per feature.
- **Cost:** a live economy needs servers, monitoring, customer support tools, and someone on call. Do not add a server economy to a game that has nothing of value to protect.
- **Regional and age rules** for random paid items and for children's data differ widely; get legal advice for the target regions. This skill does not give legal advice.

## Patching and versioning

| Thing | Changes when | Rule |
|---|---|---|
| App build | Code changes, store release | Staged rollout in the stores; keep a minimum supported version |
| Content version | New bundles | Compatible with a range of app versions; published before the code that needs it |
| Config version | Tuning | Instant; staged; validated; reversible |
| Save format version | Data shape changes | Migration chain; never break old saves (see `game-save-systems`) |
| Server API version | Protocol changes | Old apps keep working for a stated period; deprecate with notice |

- **Order of release** for a feature that needs all of them: server first (backward compatible), then content, then app, then switch on with a flag.
- **Forced upgrade:** a server-driven minimum version, shown as a friendly screen, used only when an old version is dangerous or broken.
- **Rollback plan:** you cannot roll back an app store release quickly, so keep every risky change behind a server flag and keep the old server behaviour until old apps are gone.
- **Hot fixes** go through config, flags and content, not new builds.

## Store requirements to check before fixing the monetisation design

- **Digital goods:** each store has rules about which payment system must be used for digital items and subscriptions. [S-MOB-7] [S-MOB-8]
- **Randomised paid items:** odds must be shown before purchase on both stores. [S-MOB-7] [S-GAME-77]
- **Privacy and data collection:** privacy labels, data safety forms, tracking permission, and rules for children's apps.
- **Age rating and content** rules, and rules about account creation and deletion.
- **Review time and rejection risk:** plan for a delay on the first and on risky releases.
- Rules change often: **read the current text at design time and again before launch**, and put the date you read it in the decision record.

## One-way doors (return as approvals)

- **Who owns the economy** (client or server) and how currency is represented (balance or ledger).
- **Account and identity system** (linking saves, purchases and analytics to a player).
- **The store and payment setup** (which stores, which payment path, subscription or not).
- **The analytics event schema and player ID.**
- **The content catalog and CDN layout**, and the app-to-content compatibility rule.
- The chosen backend vendor or platform (moving a live game's data is painful).

## Failure modes

- A remote config typo or bad flag breaks every player at once.
- Content published that old app versions cannot read, so they crash.
- Purchases granted twice (or never) after a crash or retry.
- Gacha odds shown in the store differ from what the server rolls.
- Client-trusted rewards exploited and the economy inflated.
- Experiments stopped early on noise; flags never removed.
- Analytics events renamed, breaking history; no privacy opt-out.
- Updates that break old saves.
- Store rejection late in the schedule because the rules were read once, long ago.

## Questions that change the design

- Does the game take real money, and does anything players earn have value to others?
- How often will content and tuning change after launch, and who makes the changes?
- Which stores, regions and age groups?
- How many players at launch and at 10 times that, and what is the monthly budget for servers and CDN?
- Who answers when the economy or a release goes wrong at night?

## Review checklist

- [ ] The split between "changes without a release" (content, config) and "checked by a server" (money, fairness) is written.
- [ ] Content bundles are built, versioned and hosted automatically, with a compatibility rule between app and content and a safe offline start.
- [ ] Remote config has baked-in defaults, validation, staged rollout, audit and a kill switch; flags have owners and expiry dates.
- [ ] The analytics event schema is defined with unique event IDs, versions and experiment groups; privacy rules are applied.
- [ ] Experiments have a question, metrics, sample size and a guardrail before they start.
- [ ] Purchases are verified on the server, are idempotent, and are recorded in a ledger; random outcomes and odds live on the server and match what players see.
- [ ] Separate version numbers exist for app, content, config, save and server API, with a minimum version and a forced-upgrade path.
- [ ] The store rules were read at design time and the date is recorded; odds disclosure, data collection and age rating are covered.
- [ ] The one-way doors are written as proposed decisions and returned for approval.

## Sources
[S-GAME-22] [S-GAME-23] [S-GAME-24] [S-GAME-41] [S-GAME-42] [S-GAME-43] [S-GAME-47] [S-GAME-49] [S-GAME-71] [S-GAME-75] [S-GAME-76] [S-GAME-77] [S-GAME-82] [S-GAME-83] [S-GAME-84] [S-GAME-86] [S-GAME-93] [S-GAME-94] [S-GAME-95] [S-MOB-7] [S-MOB-8]
