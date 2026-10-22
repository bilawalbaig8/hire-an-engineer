# Mobile apps

When to read this: the system is a phone or tablet app (iOS, Android, or both), or a backend whose main client is one.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Where the truth lives | **The phone's local database is the source of truth**, and the network is background sync, whenever the app must work on a bad connection (games, field work, notes, trackers). [S-MOB-2] | **The server is the source of truth** and the app is a window onto it, when data must always be current (banking, live availability, chat). | Local-first gives up simple "always fresh" and needs sync and conflict rules. Server-first gives up working offline. |
| Native or cross-platform | **Native** (Swift, Kotlin) when you need the newest platform features on day one, heavy graphics or sensors, or the best polish, and have the people. | **Cross-platform** (Flutter, React Native, a game engine) when one team must ship both platforms and the app is mostly screens and data. Decide by the features you need on day one and the team's skills. [S-MOB-4] | Native gives up code sharing (two codebases). Cross-platform gives up some platform-specific features, and you depend on the framework's updates. |
| App structure | **Layers with one-way data flow**: a screen layer shows state, a data layer owns storage and network, an optional domain layer holds rules shared by several screens. [S-MOB-1] [S-MOB-4] | Fewer layers for a tiny app; more layers only when logic is shared or complex. | More layers give up simplicity and speed of change for testability. |
| Sync and conflicts | **Decide the conflict rule before building sync**: last write wins, server wins, merge by field, or merge with a conflict-free data type. | Avoid sync: make the phone read-only, or make one device the only writer. | Rules give up some user edits in conflicts; avoiding sync gives up features. |
| Pushing work to the background | **Keep background work small and restartable**; the system may stop your app at any time. | Do heavy work only while the app is open and visible. | Background tasks are limited by the platforms and by battery. |
| Login | **A managed identity provider** with tokens stored in the platform's secure storage. See `security-architecture`. | A device-only account for apps with no server. | Device-only accounts give up recovery and cross-device use. |
| Money | **The platform's own payment system for digital goods**; check store rules before choosing a business model. | External payments only where the store rules allow it. | Store payments give up a share of revenue and some flexibility. |
| Updates | **Plan for old versions in the field**: the server must keep working with older app versions, and you need a way to force an upgrade when something breaks. | A single supported version for closed, managed fleets. | Supporting old versions gives up the freedom to change the server API quickly. |

Store and platform rules can invalidate a design (payments, privacy labels, content, background use). Read the current rules for each store before you commit to a business model. Official guidance: unverified sources S-MOB-7 and S-MOB-8 (the pages were reachable but not read in full by us).

## Typical shapes

- **Offline-first app:** local database, a sync queue that records changes, a sync worker, and a server that accepts changes with request IDs so repeats are safe.
- **Thin client:** screens call a backend API; a small cache keeps the last good screen for brief outages.
- **Hybrid with a game or web view:** a native shell around an engine or a web view; define clearly what the shell owns (sign-in, payments, notifications) and what the inner part owns.
- **Push-driven app:** the server pushes updates; the app still pulls on open, because pushes can be lost.

## Failure modes

- **Works on the office network only:** slow, flaky and offline connections were never tested.
- **Sync that loses or duplicates data:** no conflict rule, no request IDs.
- **Battery and data drain** from chatty polling or constant location use.
- **Old app versions break** when the server changes.
- **Memory pressure and crashes on older phones** the team never tested.
- **Store rejection** late in the project because a rule was missed.
- **Secrets inside the app package:** anything shipped in the app can be extracted.

## Questions that change the design

- Must the app work offline, and for how long? What can the user do offline?
- Which platforms, and which oldest phones and OS versions must be supported?
- Does money move? Is it digital goods (store rules) or physical goods and services?
- Is there personal, health or children's data? Which regions?
- How often will the server change, and how fast do users update?

## Checks before you hand it back

- [ ] The source of truth is named (phone or server) and the conflict rule is written down.
- [ ] The oldest supported device and OS are named and tested.
- [ ] The app was tried on a slow and an offline connection.
- [ ] The server works with at least the previous app version, and a forced-upgrade path exists.
- [ ] Store rules for payments, privacy and content were checked against the current published rules.
- [ ] No secrets are shipped inside the app.
- [ ] Battery, memory and startup time have budgets and a way to measure them.

## Sources
[S-MOB-1] [S-MOB-2] [S-MOB-4] and, as unverified leads only, S-MOB-7 and S-MOB-8
