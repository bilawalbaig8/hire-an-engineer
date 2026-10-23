# Games and game engines

Status: `ready`. This file is the short router for games; the four deep files below hold the detail.

When to read this: the system is a game, a game engine or tool, or a live service behind a game. Unity is the owner's main engine, so it gets practical guidance; Unreal and Godot are covered more briefly.

## Read next, by topic

| Topic | File |
|---|---|
| Saving progress, versions and migration, cloud saves, corruption, tamper levels | `game-save-systems.md` |
| Frame, memory, load, battery and heat budgets; garbage and pooling; profiling | `game-performance-budgets.md` |
| Game loop, object model (components or ECS), state machines, events, scenes, services, data-driven design, Unity structure | `game-architecture-patterns.md` |
| Content delivery, remote config, flags, analytics and A/B, server-side economy, patching, store rules | `game-live-ops-and-content.md` |
| Multiplayer, latency, sync models | `realtime-netcode-state.md` |
| Phone-specific concerns (offline, background, stores) | `mobile.md` |

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Object model | **Simple component composition** for most games. [S-GAME-1] | **Data-oriented or ECS layouts** only when counts or budgets demand it and a profile proves it. [S-GAME-3] [S-GAME-4] [S-GAME-5] | ECS gives up readability, tooling and onboarding speed; components give up raw speed at very large counts. |
| Simulation timing | **A fixed step for the simulation**, with rendering following it. [S-GAME-1] [S-GAME-12] | A variable step for simple, non-physical games. | A fixed step needs interpolation and can add a frame of latency; a variable step makes physics and replays unreliable. |
| Who owns the truth | **Decide first whether the server or the client owns the game state.** Single-player: the client. Competitive or money-linked: the server. [S-GAME-14] | Client-owned for co-op or casual games where cheating costs little. | Server authority gives up some responsiveness and costs servers; client authority gives up cheat resistance. |
| Shared data | **Data kept apart from behaviour** (tables, data assets, ScriptableObjects). [S-GAME-7] [S-GAME-36] | Hard-coded values only in prototypes. | Needs validation and a data pipeline. |
| Loading assets | **Load by reference and release**, so memory stays bounded and downloads small (Unity Addressables). [S-GAME-8] [S-GAME-41] | Load everything at start for tiny games. | Adds async waiting and lifetime bugs if careless. |
| Budgets | **Set frame, memory, download and battery budgets early** for the weakest supported device and measure there. | "Optimise later" only for jam-sized projects. | Budgets give up features and effects. |
| Communication | **A few typed events or messages with clear owners.** [S-GAME-6] [S-GAME-60] | Direct calls inside one system. | Events give up easy tracing. |
| Engine | **Unity** for most mobile and cross-platform 2D and 3D games with small teams; **Unreal** for high-end 3D and large teams; **Godot** for small, lightweight projects. [S-GAME-9] [S-GAME-10] [S-GAME-11] (judgement; the vendor pages describe each engine, they do not rank them) | A custom engine only when the core of the game is the engine itself. | Each engine gives up control (licence terms differ); a custom engine gives up years of tools. This is a one-way door: return it as an approval. |

## Typical shapes

- **Single-player game:** bootstrap scene, a few services (save, audio, analytics, ads), content from data, local save.
- **Live-service game:** the client plus a backend for accounts, saves, store, remote configuration and events; the client never trusts itself for anything worth money.
- **Real-time multiplayer:** a server or relay, a fixed tick, prediction and correction on the client. See `realtime-netcode-state`.
- **Game engine or tool:** layers (platform, core services, rendering, gameplay framework, editor tooling); keep tools out of the shipped runtime. [S-GAME-2]

## Questions that change the design

- Single-player, co-op or competitive multiplayer? How many players per match?
- Which platforms and which weakest device must run it well?
- Is there real-money purchase, advertising, or user data? Which regions and age groups?
- How much content, and does it update after release?
- Who changes content: programmers or designers? How often?
- Does anything players own have value to other players?

## Failure modes

Frame hitches from garbage or loading; memory growth from unreleased assets; everything depending on everything; saves that break after an update; works on the developer's phone but not a three-year-old one; cheating and economy exploits from a trusted client; store rules found late. Details are in the four files above.

## Checks before you hand it back

- [ ] The object model is the simplest that fits the counts, and any ECS use is justified by a measurement.
- [ ] The simulation step and who owns the game state are decided and written.
- [ ] Budgets exist for frame time, memory, download size and battery on the weakest supported device (`game-performance-budgets`).
- [ ] Saved data has a version number, a migration path and safe writes (`game-save-systems`).
- [ ] Content and balance values live in validated data with stable IDs (`game-architecture-patterns`).
- [ ] Anything worth money is validated on a server (`game-live-ops-and-content`).
- [ ] Store rules, age rating and data collection were checked before the monetisation design was fixed.
- [ ] One-way doors (engine, save format and IDs, economy ownership, account system) are returned as approvals, not finalised.

## Sources
[S-GAME-1] [S-GAME-2] [S-GAME-3] [S-GAME-4] [S-GAME-5] [S-GAME-6] [S-GAME-7] [S-GAME-8] [S-GAME-9] [S-GAME-10] [S-GAME-11] [S-GAME-12] [S-GAME-14] [S-GAME-36] [S-GAME-41] [S-GAME-60]. The new files carry their own source lists.
