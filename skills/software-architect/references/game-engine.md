# Games and game engines

Status: `starter`. The decisions below are solid, but save systems, performance budgets and specific conference talks are thin (see "To deepen" at the end).

When to read this: the system is a game, a game engine or tool, or a live service behind a game. Unity is the owner's main engine, so it gets practical guidance; Unreal and Godot are covered more briefly.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Object model | **Simple component composition** (objects built from small behaviours, each doing one thing) for most games; it is easy to read and maintain. [S-GAME-1] | **Data-oriented or ECS layouts** only when entity counts or hard performance targets demand them (thousands of similar things, tight frame budgets on weak devices). [S-GAME-3] [S-GAME-4] | ECS gives up readability, tooling and onboarding speed for throughput; components give up raw speed at very large counts. |
| Simulation timing | **A fixed time step for the simulation** with rendering interpolated between steps, so the game behaves the same on slow and fast devices. [S-GAME-1] (the well-known article S-GAME-12 on this is unverified) | A variable step for simple, non-physical games. | A fixed step needs interpolation code and can add a frame of latency; a variable step makes physics and replays unreliable. |
| Who owns the truth | **Decide first whether server or client owns the game state.** Single-player: the client. Competitive or money-linked: the server. See `realtime-netcode-state`. [S-GAME-14] | Client-owned for co-op or casual games where cheating costs little. | Server authority gives up some responsiveness and costs servers; client authority gives up cheat resistance. |
| Shared data | **Data kept apart from behaviour**: configuration, item and level tables in data files or Unity ScriptableObjects, so designers can change values without code. (general practice; unverified source S-GAME-7 is a vendor e-book on this) | Hard-coded values only in prototypes. | Data-driven design gives up some quick-hack speed and needs validation of the data. |
| Loading assets | **Load assets by reference and release them**, so memory stays bounded and downloads stay small (in Unity this is the Addressables approach). (general practice; unverified source S-GAME-8 is the Unity manual) | Load everything at start for tiny games. | Reference loading gives up simplicity and adds async waiting and lifetime bugs if careless. |
| Frame budget | **Set budgets early** (frame time, memory, download size, battery) for the weakest device you support, and measure on that device. | "Optimise later" only for jam-sized projects. | Budgets give up some features and effects. |
| Communication between systems | **Events or messages between systems**, with a few clear owners, rather than every system reaching into every other. | Direct calls inside one system. | Events give up easy tracing of who calls whom. |
| Engine | **Unity** for most mobile and cross-platform 2D and 3D games with small teams; **Unreal** for high-end 3D and large teams; **Godot** for small, lightweight projects. (general practice; unverified sources S-GAME-9, S-GAME-10, S-GAME-11 are the vendors' documents) | A custom engine only when the game's core is the engine itself. | Each engine gives up control (and fees or licence terms differ); a custom engine gives up years of tools. |

## Unity practice (general practice unless a source is cited)

- **Scenes and prefabs:** keep scenes small and focused; build content from prefabs; nest prefabs rather than copying them; one bootstrap scene creates the long-lived services.
- **Assembly definitions:** split code into assemblies by area so compile times stay low and dependencies are explicit; keep dependencies pointing one way (game code depends on core, never the reverse).
- **ScriptableObjects:** for shared data and settings (item tables, difficulty curves); avoid using them as mutable global state.
- **Addressables:** for content that is large, optional or downloaded later; always release what you load.
- **Pooling:** reuse frequently created objects (bullets, effects, UI rows) instead of creating and destroying them.
- **Per-frame allocations:** avoid creating garbage every frame (string building, collection creation, closures in update loops); profile on the target device.
- **DOTS and ECS:** consider only for very large simulations; mixing it with ordinary objects adds complexity.
- **Event wiring:** prefer a small number of explicit events or message channels; avoid singletons that everything mutates. [S-GAME-6]
- **Build size and platforms:** decide texture compression, code stripping and the oldest device early.

## Typical shapes

- **Single-player game:** bootstrap scene, a few services (save, audio, analytics, ads), content from data, local save.
- **Live-service game:** the client plus a backend for accounts, saves, store, remote configuration and events; the client never trusts itself for anything worth money.
- **Real-time multiplayer:** a server or relay, a fixed tick, prediction and correction on the client. See `realtime-netcode-state`.
- **Game engine or tool:** layers (platform, core services, rendering, gameplay framework, editor tooling); keep tools out of the shipped runtime. [S-GAME-2]

## Failure modes

- **Frame hitches** from garbage collection, loading on the main thread, or too many objects updating every frame.
- **Memory growth** because loaded assets are never released.
- **Everything depends on everything:** singletons and scene references that make changes risky.
- **Saves that break after an update:** no version number or migration for saved data.
- **Works on the developer's phone, fails on a three-year-old one.**
- **Cheating and economy exploits** because the client was trusted.
- **Late discovery of store rules:** content, payments, data collection and age ratings.

## Questions that change the design

- Single-player, co-op or competitive multiplayer? How many players per match?
- Which platforms and which weakest device must run it well?
- Is there real-money purchase, advertising, or user data? Which regions and age groups?
- How much content, and does it update after release (live events, new levels)?
- Who changes content: programmers or designers? How often?

## Checks before you hand it back

- [ ] The object model is the simplest that fits the entity counts, and any ECS use is justified by a measurement.
- [ ] The simulation step, and who owns the game state, are decided and written.
- [ ] Budgets exist for frame time, memory, download size and battery on the weakest supported device.
- [ ] Saved data has a version number and an upgrade path.
- [ ] Content and balance values live in data, not code.
- [ ] Anything worth money is validated on a server.
- [ ] Store rules, age rating and data collection were checked before the monetisation design was fixed.

## To deepen (not yet covered well)

Save-system patterns and cloud save conflicts; concrete performance budgets by device class; verified conference talks on engine and netcode architecture; Unity-specific verified references.

## Sources
[S-GAME-1] [S-GAME-2] [S-GAME-3] [S-GAME-4] [S-GAME-6] [S-GAME-14] and, as unverified leads only, S-GAME-7, S-GAME-8, S-GAME-9, S-GAME-10, S-GAME-11, S-GAME-12
