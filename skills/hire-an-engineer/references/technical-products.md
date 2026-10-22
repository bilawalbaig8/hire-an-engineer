# Complex Technical Products — game engines, developer tools, platforms

Contents: Working inside an existing engine project · Scoping these products · Game engine runtime architecture · Editor architecture · Performance budgets · Testing engines and technical products · Developer-facing products (APIs, SDKs, engines) · Platforms (multi-tenant, real-time) · Export targets (web, playable ads, mobile) · Roadmap pattern · Roles that carry extra weight

Read when the idea is a **game engine or game framework**, an **editor/creation tool**, a **developer tool** (SDK, library, API, CLI, plugin), or a **platform** (multi-tenant SaaS, real-time collaboration, marketplace). Building the engine, editor, SDK or platform itself is Large-tier; using an existing engine for a game or tool is not (see below). Everything else in the skill still applies; this file adds what these products specifically need.

---

## Working inside an existing engine project (Unity, Godot, Unreal)

Size the task normally (`project-cases.md`); the engine does not make it Large.
- Big binaries (art, audio, builds) in Git LFS; use the engine's own `.gitignore`.
- Unity: commit the `.meta` files with their assets; never commit `Library/`, `Temp/` or `Logs/`.
- Test with the engine's own framework (Unity Test Framework, GUT/GdUnit, Unreal Automation).
- If an engine skill or MCP tool is installed, follow it for editor and engine steps.
- Cannot run the editor? Prefer steps checkable in files (e.g. `Packages/manifest.json`) over Asset Store or GUI steps. Keep core logic in plain C# (no `UnityEngine`) with an asmdef and EditMode tests; run them headless when the editor is available.

---

## 1. Scoping these products

- **Find the niche.** General-purpose engines/platforms already exist with huge teams behind them. Ask what the existing ones don't do for this person (a genre, a format like playable ads, a workflow, a price, an audience). Build for that niche only.
- **Compare honestly first** (with a quick web search for current state): e.g. engines — PlayCanvas, Babylon.js, Needle Engine, three.js editor, Godot web export; chat platforms — Mattermost, Rocket.Chat, Element. Recommend adopting or extending one when it covers the need.
- **Build on, not from scratch.** Use proven libraries for solved problems (rendering: three.js; physics: Rapier / cannon-es; audio: Web Audio / Howler; tweening; glTF loaders; UI frameworks). The value is in the integration and the niche features.
- **Dogfood from day one.** Every milestone must produce a real game/ad/app built *with* the product. If it can't, the milestone is wrong.
- **Build environment:** large multi-file codebases belong in a coding agent environment (Claude Code, Cursor, Codex, Antigravity or similar) with git and tests. Use chat for planning, design and documents.

## 2. Game engine runtime architecture

Layers (each a separate module with a clear interface):

```
Game / ad content (scenes, scripts, assets)
        │
Component / scripting API      ← what users of the engine touch
        │
Systems: input · physics · audio · animation · UI · events · tweening
        │
Core: game loop · scene model (ECS or scene graph) · time · asset manager · serializer
        │
Platform: rendering (three.js) · browser APIs · storage · network/ad SDK bridge
```

Key decisions (record each in the decision log):
- **Game loop:** fixed timestep for simulation/physics (e.g. 60 Hz with accumulator), variable-rate rendering with interpolation; pause/resume on tab hide.
- **Scene model:** three.js scene graph + components attached to objects (simplest, Unity-like) vs. **ECS** (entities, components as data, systems as logic — scales better for many objects). Default: component-on-object for editor-centric engines; ECS when thousands of similar objects or heavy simulation.
- **Component API:** lifecycle hooks (`awake`, `start`, `update(dt)`, `destroy`), typed properties with schemas (the editor's inspector reads these), event bus for decoupling.
- **Asset pipeline:** glTF/GLB for models, compressed textures (KTX2/Basis), Draco/meshopt geometry compression, audio in compressed formats; asset manifest with IDs, preloading and progress.
- **Serialization:** versioned JSON scene format; every save includes a format version; migrations for old scenes; round-trip tested.
- **Determinism** where needed (replays, tests): seeded random, fixed timestep, no reliance on frame rate.
- **Plugin/extension points** only after the core is stable.

## 3. Editor architecture

- **Editor and runtime separated:** the editor uses the runtime but ships separately; exported games contain no editor code.
- **Command pattern for every edit** → reliable undo/redo, autosave and change history.
- **Panels:** hierarchy (scene tree), inspector (auto-generated from component schemas), viewport (gizmos: move/rotate/scale, camera controls), asset browser, console.
- **Play mode:** snapshot scene state, run, restore exactly on stop.
- **Project format:** a folder/zip with scenes, assets and settings; human-readable where possible (diff-friendly in git).
- **Autosave and crash recovery** from the first editor milestone.
- The editor is a UI product: apply `ui-ux.md` fully — the person and their users judge the engine mostly through the editor.

## 4. Performance budgets

Set budgets in Phase 4, per target device (usually a mid-range Android phone — measure there, not only on a laptop):

| Budget | Typical target (adjust to project) |
|---|---|
| Frame rate | 60 fps (frame ≤ 16.6 ms); 30 fps floor on low-end |
| Draw calls | low hundreds or fewer on mobile |
| Triangles / scene | set per genre; measured |
| Texture memory | set per device class |
| JS heap & GC | no per-frame allocations in hot loops |
| Load time | first interactive in a few seconds on 4G |
| Bundle / output size | hard limit from export target (e.g. ad network caps) |

Techniques: instancing and batching, texture atlases and compression, LOD, frustum culling, object pooling, avoiding garbage in `update`, lazy loading, tree-shaking.
Tools: stats/FPS overlay, browser performance profiler, WebGL inspectors (e.g. Spector.js), memory snapshots, bundle analyzers.
Budgets are **tests**: CI fails when a benchmark scene exceeds them.

## 5. Testing engines and technical products

Beyond the standard pyramid (`engineering-principles.md` §5):
- **Unit:** math (vectors, transforms), systems logic, serializer.
- **Deterministic simulation tests:** run N fixed steps with a seed, assert positions/states.
- **Visual regression:** render reference scenes headlessly, compare screenshots to approved baselines with a tolerance.
- **Performance benchmarks in CI:** standard scenes; record fps/frame time/memory/size; fail on regression beyond threshold.
- **Serialization round-trip:** save → load → save produces the same output; old-version scenes still load.
- **Example projects as integration tests:** every template/sample game must build, export and run.
- **Device/browser matrix:** Chrome, Safari (iOS!), Firefox, Android WebView; low-end and high-end devices.
- **Export validation:** each output checked against the target's rules (size, single file, required hooks).
- **API compatibility tests** for developer-facing products: public API surface snapshot; unintended changes fail CI.

## 6. Developer-facing products (APIs, SDKs, engines)

The "users" are developers or designers, so their experience is the product:
- **API design:** small surface, consistent naming, sensible defaults, progressive disclosure (simple things simple, advanced possible), clear errors that say how to fix, typed (TypeScript types shipped).
- **Docs as a feature:** getting-started guide that works in under 10 minutes, generated API reference, recipes, example projects/templates, troubleshooting. Docs are tested (examples run in CI).
- **Strict semantic versioning** with a deprecation policy (warn for at least one minor version before removing), migration guides for majors, detailed changelog.
- **Packaging:** npm package (ESM, tree-shakeable), CDN build, starter template.
- **License:** ask the person (proprietary vs open source — MIT/Apache); record the decision.
- **Feedback loop:** issue templates, a way for users to report bugs with reproduction projects.

## 7. Platforms (multi-tenant, real-time)

For Slack-like tools, collaboration apps, marketplaces:
- **Tenancy:** every row tagged with its workspace/tenant; isolation enforced in the database (row-level security) and tested.
- **Real-time:** managed real-time services (e.g. Supabase Realtime, WebSocket services) before custom servers; handle reconnects, ordering, offline queues, presence.
- **Roles and permissions** per workspace (owner, admin, member, guest).
- **Scale plan:** what breaks first at 10×/100× users (connections, DB writes, storage, AI cost) and the planned fix.
- **Abuse and moderation:** rate limits, reporting, blocking, spam controls.
- **Billing** (if selling): proven provider, plans and limits enforced server-side, test mode first.
- **Admin console** for the person: users, workspaces, usage, costs, support actions.

## 8. Export targets (web, playable ads, mobile)

- **Web:** static hosting, caching headers, progressive loading.
- **Playable ads:** usually a single self-contained HTML file with all assets inlined, strict size limits, no external requests, network-specific hooks (e.g. MRAID / network SDK calls for the store/CTA redirect and lifecycle events), orientation handling, mute by default, quick first frame. **Requirements differ per ad network and change — look up each target network's current specs** and encode them as export validation rules and per-network export presets. Include event tracking hooks for analytics.
- **Mobile apps:** web wrapper (e.g. Capacitor) before native; check store requirements. Accounts, signing keys, review and rollout: `platform-targets.md` §1.

## 9. Roadmap pattern

| Version | Delivers | Dogfood proof |
|---|---|---|
| v0.1 | Runtime core: loop, scene, input, assets, one mechanic | One small game/ad built with code |
| v0.2 | Export pipeline + validation for first target | That game exported and passing target checks |
| v0.3 | Editor MVP: hierarchy, inspector, viewport, save/load, undo | Same game rebuilt in the editor |
| v0.4 | Templates + docs + examples | A second game made from a template quickly |
| v1.0 | Stable API, performance budgets met, more export targets | Real production use |
| later | Plugins, collaboration, asset store, analytics | — |

## 10. Roles that carry extra weight

- **Architect:** module boundaries, scene model, API surface — mistakes here are expensive later; write ADRs for each.
- **Performance engineer** (part of the Engineer role): owns budgets, profiling and benchmark CI.
- **Technical writer / developer advocate:** docs, examples, templates, migration guides.
- **QA:** device matrix, visual regression, export validation.
- **Release manager:** strict semver and deprecation policy, because other people's projects depend on each release.
