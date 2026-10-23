# Game architecture patterns

When to read this: you are choosing how the code of a game is shaped (the loop and update order, the object model, behaviour, messaging, scenes, services, data, mod and live-content hooks). Part of the games set: start at `game-engine.md`. Each pattern below says when to use it, what it gives up, and when it is overkill. Use the simplest one that meets the scenarios.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Loop and timing | **The engine's loop, with a fixed step for simulation and physics**, and rendering that follows the latest state. [S-GAME-57] [S-GAME-12] | A variable step for games with no physics, replays or networking. | Fixed step needs interpolation and can cost latency; variable step makes behaviour differ between devices. |
| Object model | **Component objects** (an entity built from small behaviours): Unity GameObjects, Godot nodes, Unreal actors and components. [S-GAME-63] | **Data-oriented ECS** when you simulate thousands of similar things and the profile shows the object model is the limit. [S-GAME-5] [S-GAME-48] [S-GAME-64] | ECS gives up readability, designer tooling and team familiarity; component objects give up raw throughput at very large counts. |
| Behaviour | **An explicit state machine** for characters, AI, game flow and screens with more than three states. [S-GAME-59] [S-RT-2] | Plain conditions for two or three states; behaviour trees or utility systems when AI has many layered choices (general practice). | State machines grow tangled without nesting; plain conditions rot as states are added. |
| Messaging | **A few typed events or a message queue** between systems, with one clear owner per event. [S-GAME-60] [S-GAME-6] | Direct calls inside one system or one prefab. | Events give up easy tracing of who reacts; a global bus that anyone can fire is a hidden dependency graph. |
| Scenes and levels | **A bootstrap scene that creates long-lived services, then content scenes loaded additively**, each self-contained. [S-GAME-40] [S-GAME-54] | One big scene for tiny games. | More scenes give up simple editing and need rules for what lives where. |
| Finding services | **Pass dependencies in (constructor, serialised reference, or an explicit context)** for the few real services. | **A service locator or engine-managed subsystem** when passing through many layers is painful. [S-GAME-61] [S-GAME-50] [S-GAME-53] Avoid singletons that anything can change. [S-GAME-67] | Passing costs typing and plumbing; a locator hides what a class depends on and makes tests harder. |
| Game data | **Data assets and tables** (ScriptableObjects, Godot Resources, Unreal data assets, JSON or spreadsheets imported at build time) for items, enemies, levels, balance. [S-GAME-36] [S-GAME-55] [S-GAME-65] | Constants in code for prototypes. | Data needs validation and a schema; hard-coded values give up designer control. |
| Mods and live hooks | **Data and script boundaries chosen early** for what outsiders may change. [S-GAME-66] [S-GAME-49] | None for closed single-player games. | Open hooks give up freedom to change internals and add a security surface. |

## Game loop and update order

- **Know the order your engine runs things.** Unity runs Awake and Start, then FixedUpdate (physics, on a fixed step), then Update, then LateUpdate, then rendering, in a documented order. [S-GAME-38] Unreal has tick groups; Godot has process and physics-process callbacks. Write down which of your systems run in which phase.
- **Rule of thumb for phases:** read input, then update gameplay, then physics, then follow-up (cameras, UI that reads the final state), then render. Anything that reads another system's result must run after it.
- **Do not rely on Unity's script execution order setting** to make things work; it is fragile and invisible. Prefer one explicit orchestrator that ticks the systems in a stated order (for example a "game session" object that calls them in sequence), or events that fire when data is ready. Unity lets you add your own phases to the engine's player loop if you need that. [S-GAME-39]
- **Each object updating itself** is simple and fine for hundreds of objects. [S-GAME-58] For thousands, a manager that updates a list in one pass is usually cheaper than thousands of separate update calls (measure first).
- **Fixed step for simulation**, variable step for presentation. Accumulate real time, run zero or more fixed steps, then draw with interpolation. [S-GAME-57] [S-GAME-12] Cap the number of steps per frame so a long pause cannot cause a spiral of catch-up.
- Overkill: a custom engine loop in a game that fits the engine's own.

## Object model: components, ECS, or something else

| Option | Use when | Gives up |
|---|---|---|
| **Inheritance trees** | Almost never beyond one or two levels | Rigid: a new combination of traits means refactoring the tree. [S-GAME-63] |
| **Component objects** (default) | Most games; designers assemble prefabs | Per-object overhead; many small update calls at huge counts |
| **Data-oriented ECS** (Unity Entities, Unreal Mass, your own) | Many thousands of similar entities (crowds, bullets, simulation) and a failed profile | Tooling, readability, onboarding speed, and mixing it with ordinary objects. [S-GAME-5] [S-GAME-48] |
| **Hybrid**: ordinary objects for the game, a data-oriented core only for the heavy simulation | A game with one hot loop | Two models to maintain and a boundary to design |

The speed of data-oriented design comes from how data sits in memory and how the cache is used, not from the word "ECS". [S-GAME-64] [S-GAME-3] [S-GAME-4] A flat array of structs processed in a tight loop can give much of the gain without a framework.

**Unity:** DOTS (Entities, Burst, Jobs) only when a measured profile shows ordinary objects cannot hit the budget, the team is ready to pay the learning cost, and the features you need are supported on your target platforms. [S-GAME-5] Otherwise stay with GameObjects and components. A common mistake is choosing DOTS for a game that has 200 objects.

## State machines

- Use for: character states, enemy AI, game flow (boot, menu, loading, playing, paused, results), UI screen flow, tutorial steps, network connection state.
- **Make states and transitions visible**: a table or diagram that lists every state, the events it accepts, and what it does on entry and exit. Test by walking every transition. [S-GAME-59] [S-RT-2]
- Nest states (for example "in combat" containing "attacking") before the number of states explodes; a stack of states helps for "go back to what you were doing" (pause menus).
- Gives up: a state machine does not scale to AI with many layered choices; move to a behaviour tree or utility scoring then (general practice). Overkill for a one-way flow of two steps.

## Events and message buses

- **Direct reference**: simplest; use inside one prefab or one system.
- **Typed event on the producer** (the publisher exposes an event; interested systems subscribe): clear owner, easy to find. Remember to unsubscribe when objects are destroyed (a common leak and null-reference source).
- **A queue of messages** handled later: decouples timing as well as identity (audio requests, analytics, damage events processed at a defined point in the frame). [S-GAME-60]
- **A global bus** anyone can publish to: convenient, but it hides who depends on whom, and debugging becomes a search for subscribers. Allow it only for a small, named set of cross-cutting events (game paused, player died, level complete) and log them in development builds.
- ScriptableObject-based event channels (a shared asset that raises and listens for events) give designers wiring in the editor, at the cost of invisible links through assets; use for a limited number of channels. [S-GAME-36] [S-GAME-6]
- Gives up: ordering guarantees must be stated; events firing in the middle of an update can cause re-entrancy bugs, so queue and handle at the end of the phase when in doubt.

## Scene and level management

- **Unity structure that scales:** one **bootstrap scene** (loaded first, creates long-lived services, never unloaded), **content scenes** per level or area loaded additively, and **prefabs** for everything reused. Keep scenes small so teams do not collide in version control. [S-GAME-40]
- Rules: scenes do not reference each other directly; they talk through services or events; a scene can be loaded alone for testing with a stub of the bootstrap.
- Unload and release what you load (see `game-performance-budgets`). [S-GAME-41]
- **Godot:** scenes are reusable trees; keep them loosely coupled, with a parent wiring children rather than children reaching up. [S-GAME-54] **Unreal:** a persistent level with streamed sub-levels, and the gameplay framework (game mode, game state, controller, pawn) to place rules and state. [S-GAME-9]
- Overkill: additive scene composition for a game with three screens.

## Services and dependencies in games

- A game needs a few long-lived services: audio, save, analytics, input, ads, in-app purchase, remote config, time, localisation.
- **Order of preference:** pass the dependency in explicitly; else use one **composition root** (the bootstrap) that creates the services and hands them out; else a service locator, with an interface so tests can swap in a fake. [S-GAME-61] **Avoid singletons holding mutable global state**: they make order of creation matter and make tests hard. [S-GAME-67]
- Engines offer their own scopes: Unreal subsystems (with the lifetime of the engine, game instance, world or player) and Godot autoloads (global nodes). [S-GAME-50] [S-GAME-53] Use them for the small set of real services and keep them thin.
- A dependency-injection library for Unity can help in very large projects; it gives up simplicity and designer friendliness, and is overkill for a small team. (general practice)
- Gives up (locators): hidden dependencies; (explicit passing): plumbing code.

## Data-driven design

- **Put the numbers and content in data, not code:** item stats, enemy lists, levels, wave tables, drop rates, UI text keys, prices (unless prices must be server side). Designers can change them without a programmer and without risk to the code. [S-GAME-36] [S-GAME-65]
- **Unity:** ScriptableObjects as shared data containers; they avoid per-instance copies, but in a built player their saved data is read-only, so use them for authoring, not for save state. [S-GAME-36] **Godot:** Resources do the same job. [S-GAME-55] **Unreal:** data assets and data tables.
- **The type-object idea:** define kinds of things (an enemy type) as data and create instances from the type, rather than a class per kind. [S-GAME-65]
- **Validate data at build time** (missing references, duplicate IDs, out-of-range values) and fail the build; bad data is the most common live bug in data-driven games.
- Give every record a **stable ID** (never the file name or the display name): saves and servers refer to them. See `game-save-systems`.
- Gives up: indirection (you cannot read the behaviour in the code alone), the need for an import and validation step, and editor tooling work. Overkill: a data pipeline for a jam game.

## Modding and live-ops hooks

- Decide early **what outsiders or the live team may change without a store release**: numbers (remote config), content (downloadable bundles), rules (data-defined behaviour or a small scripting layer). [S-GAME-66] See `game-live-ops-and-content`.
- **Small, sandboxed scripting** (a bytecode or restricted-script layer) lets designers or modders define behaviour while the host stays safe; its price is a language to design, document and secure. [S-GAME-66]
- Unreal's Game Feature plugins add and remove gameplay modules at run time. [S-GAME-49]
- Build **extension points on purpose**: well-named events, data hooks, and content IDs; do not publish internals as the modding API (you will be unable to change them).
- Overkill for a closed single-player game: an open mod API.

## Unity-specific recommendations

- **Assembly definitions** by area (core, gameplay, UI, tools, tests) so compile times stay low and dependencies are explicit and checked by the compiler. Dependencies point one way: game code depends on core, never the reverse; editor code stays in editor-only assemblies. [S-GAME-37]
- **Scene structure:** bootstrap scene plus additive content scenes; prefabs and prefab variants for reuse. [S-GAME-40]
- **MonoBehaviours as thin adapters** over plain C# classes that hold the rules: the plain classes can be unit-tested without the engine.
- **ScriptableObjects** for shared config and authoring data, not for runtime mutable state, and not for saves. [S-GAME-36]
- **Addressables** for content that is large, optional or downloaded. [S-GAME-41]
- **Pool** frequently spawned objects. [S-GAME-27]
- **DOTS** only under the conditions above. [S-GAME-5]
- Official e-books on patterns and ScriptableObject architecture exist (vendor material; use for ideas, apply with judgement). [S-GAME-6] [S-GAME-7]

## When each pattern is overkill (summary)

| Pattern | Overkill when |
|---|---|
| ECS or DOTS | Under a few thousand similar entities, or no failed profile |
| Global event bus | A single scene or small team where direct references work |
| Dependency-injection library | Small team, few services |
| Behaviour trees | An enemy with three behaviours |
| Data pipeline with importers | Prototypes and jams |
| Additive scene composition | Fewer than five scenes |
| Open mod API | Closed single-player game |
| Custom engine loop | The engine's loop fits |

## One-way doors (return as approvals)

- **The object model for the core simulation** (ECS or not) once content and tools are built on it.
- **The stable ID scheme for data** referenced by saves and servers.
- **The modding API surface**, once players depend on it.
- The engine itself.

## Failure modes

- Everything depends on everything through singletons and scene references.
- Update-order bugs that appear and vanish (things reading data before it is ready).
- A global event bus with unknown listeners, and listeners never unsubscribed.
- DOTS adopted early and used for the whole game, slowing every feature.
- Game data without validation: a typo in a table crashes a live game.
- Scenes that cannot run alone, so every test needs the full game.

## Questions that change the design

- How many entities of one kind must run at once on the weakest device?
- Who changes gameplay values and content: programmers or designers? How often, and after release?
- Will players or partners add content?
- Which parts must be tested without the engine?
- How big is the team, and how many people touch the same scene?

## Review checklist

- [ ] The loop and update order are written down (which system runs in which phase), with a fixed step for simulation if physics or networking is used.
- [ ] The object model is the simplest that fits the entity counts, and any ECS is justified by a measurement.
- [ ] Every long-lived behaviour has an explicit state machine with transitions listed.
- [ ] Events have owners; the global bus (if any) has a short list of named events and unsubscribing is handled.
- [ ] There is a bootstrap scene; content scenes can run alone; assets loaded are released.
- [ ] Services are passed in or created at a composition root; no singleton holds mutable shared state.
- [ ] Content and balance are in validated data with stable IDs.
- [ ] Mod and live-content boundaries are decided (or explicitly "none").
- [ ] Assembly definitions separate areas with dependencies pointing one way (Unity).

## Sources
[S-GAME-3] [S-GAME-4] [S-GAME-5] [S-GAME-6] [S-GAME-7] [S-GAME-9] [S-GAME-12] [S-GAME-27] [S-GAME-36] [S-GAME-37] [S-GAME-38] [S-GAME-39] [S-GAME-40] [S-GAME-41] [S-GAME-48] [S-GAME-49] [S-GAME-50] [S-GAME-53] [S-GAME-54] [S-GAME-55] [S-GAME-57] [S-GAME-58] [S-GAME-59] [S-GAME-60] [S-GAME-61] [S-GAME-63] [S-GAME-64] [S-GAME-65] [S-GAME-66] [S-GAME-67] [S-RT-2]
