# Game performance budgets

When to read this: you are setting how fast, how big and how battery-friendly a game must be, or a game is slow, hitching, crashing from memory, or overheating. Part of the games set: start at `game-engine.md`. The numbers below are **starting points from general practice, not standards**: replace them with measurements from your weakest supported device.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Target frame rate | **30 fps** for most mobile games that are not twitch-fast, puzzle, idle, casual and strategy games; it halves the heat and battery cost. On Unity mobile, the default with no setting is a fixed 30 fps. [S-GAME-33] | **60 fps** for action, racing and rhythm games, and on desktop and console. **90 or 120 fps** only as an option on devices that hold it. | 30 fps gives up smoothness and some input feel. 60 fps gives up battery, heat, and visual detail per frame. 120 fps adds heat for little gain in many games. |
| Weakest supported device | **Name it** (a real model, with its RAM, chip and OS), buy one, and measure on it. | A range of two or three tiers (low, mid, high) with quality settings that scale. | A low floor gives up features and effects; a high floor gives up the market. **This is close to a one-way door**: art, levels and rules get built to it. |
| Where to measure | **On the real device in a development build**, with the editor profiler attached; the editor lies on mobile. [S-GAME-29] | Editor profiling only for early logic checks. | Device testing needs devices and time. |
| Memory | **A hard memory budget per scene and per game**, below the point where the OS closes the app, tested on the lowest-RAM device. (general practice; Apple's memory guidance S-GAME-79 is a pointer only, body not read) | Fewer limits for desktop games with a known high spec. | A budget gives up asset quality and loads more often. |
| Loading | **Stream and load in the background, show progress**, with one place that owns what is loaded. [S-GAME-40] [S-GAME-41] | Load everything up front in tiny games. | Streaming adds waiting states, release bugs and complexity. |
| Allocations | **Do not create garbage in the frame loop**; pool what you spawn often. [S-GAME-26] [S-GAME-27] [S-GAME-62] | Allow it in menus and one-off code. | Pooling gives up simple create and destroy, and adds reset bugs. |
| Adapting to heat | **Read the device's thermal state and lower the load before it is throttled** (resolution, effects, frame rate cap). [S-GAME-70] [S-GAME-32] | Cap at a fixed sustainable rate for the whole session. | Adaptive quality gives up consistency and takes testing; a fixed cap gives up peak quality. |

## The frame budget method

1. **Pick the target and turn it into milliseconds:** 30 fps is 33.3 ms per frame, 60 fps is 16.7 ms, 120 fps is 8.3 ms (1000 divided by fps).
2. **Keep headroom.** Spend about 70 to 80 percent of that on a cool device. A device that just fits the frame cool will miss it when hot or on battery. (general practice)
3. **Split by thread and system.** A frame has a main-thread cost, a render-thread cost and a GPU cost; the frame takes as long as the slowest. Write a budget per system and give the total headroom its own line.
4. **Example split for a 30 fps mobile action game** (illustrative; set your own): game logic 6 ms, physics 3 ms, animation 3 ms, UI 3 ms, rendering CPU 6 ms, audio and misc 2 ms (about 23 ms of 33 ms, leaving headroom); GPU about 22 ms.
5. **Put the budget in the project:** a table with each system's number, who owns it, and the scene where it is measured. Review it when a feature is added.
6. **Test the worst scene**, not the average one (the biggest fight, the most UI, the first frames after a load).
7. **Measure percentiles, not averages.** Hitches ruin feel even when the average is fine; track the slow frames (for example the 99th percentile) and the longest frame. [S-GAME-31]

## Budgets by platform class (starting points)

| Class | Frame | Memory | Other limits |
|---|---|---|---|
| Low-end mobile (2 to 3 GB RAM, older chip) | 30 fps, lowest quality tier | Small: plan well below half the device RAM (the OS and other apps take the rest) | Longest thermal stress; smallest download wins installs; avoid heavy shaders and large textures |
| Mid and high mobile | 30 to 60 fps | Moderate; still below what the OS allows | Sustained performance drops after several minutes when hot [S-GAME-69] |
| Desktop and console | 60 fps or more | Set by the lowest supported spec | Load times and install size matter for reviews |
| Web (browser) | 30 to 60 fps | Strict: the browser tab is limited | Download size is the main constraint; incremental GC is not available in Unity web builds [S-GAME-25] |

Also write a budget for: **cold start** (to first interaction), **level load time**, **install and download size** (check each store's current limits), and **battery** (percent per hour of play on the reference device). Android's own quality data tracks start time, crashes, freezes and battery, which affect store ranking. [S-MOB-9] Apple provides performance and memory guidance and reports. [S-MOB-10] [S-GAME-78]

## Memory, allocation and garbage collection

- **Memory is the common killer on phones.** The OS closes the app silently when it uses too much, which shows up as crashes that no code error explains. Measure peak memory on the lowest device across a whole session, including scene changes. (general practice) [S-GAME-30]
- **Textures and audio dominate.** Choose compressed texture formats per platform, limit texture size by quality tier, and strip unused code to cut build size. [S-GAME-34] [S-GAME-35]
- **Garbage collection:** in Unity the collector is incremental by default, spreading work across frames, but a collection still adds cost to frame time and can cause visible spikes. [S-GAME-25] The fix is to produce less garbage: avoid building strings, creating lists or capturing closures in the per-frame code, and reuse buffers. [S-GAME-26]
- **Pooling** (reuse bullets, effects, UI rows, enemies) removes both allocation and collection cost. Use Unity's built-in pool type or your own. [S-GAME-27] [S-GAME-62] What it gives up: you must reset state on reuse, and pools hold memory when idle; size them from measurements.
- **Addressables (Unity):** asynchronous load and release of assets by reference; reference counting decides when memory comes back; groups set what unloads together and what size each download is. Every load needs a matching release, and memory comes back only when the whole bundle can unload, so group assets that live and die together. [S-GAME-41]
- **Unreal and Godot:** Unreal has its own object garbage collection and a stat system to see costs; Godot frees most things through reference counting and its performance guide lists the common fixes. Use their tools in the next section. [S-GAME-45] [S-GAME-52]

## Streaming and loading

- **Load asynchronously** and never block the main thread with a big load. In Unity, `LoadSceneAsync` and Addressables load in the background. [S-GAME-40] [S-GAME-41]
- **Loading screen or seamless streaming?** A loading screen is simple and lets you free memory completely between levels (choose it by default). Seamless streaming gives a better feel but needs careful budgets for CPU time per frame and for peak memory, and is harder to test. [S-GAME-47]
- **Time-slice** any work that must happen on the main thread (spawning, parsing) into a few milliseconds per frame.
- **Download later:** big optional content goes into downloadable bundles so install size stays small. [S-GAME-42] On Apple, downloads can run in the background. [S-GAME-82] See `game-live-ops-and-content`.
- **First-session path:** make the first minutes light (small download, fast start), because that is where installs are lost.

## Mobile heat and battery

- Phones drop their speed when hot, so a game that runs at 60 fps for two minutes may run at 35 fps after ten. **Test for 20 to 30 minutes on the reference device**, not for one level. (general practice)
- **Android:** the Thermal API reports status and a headroom estimate, so the game can reduce load before the system throttles it. [S-GAME-70] The Dynamic Performance Framework adds performance hints. [S-GAME-69] The Frame Pacing library delivers frames evenly. [S-GAME-72]
- **Unity:** the Adaptive Performance package reacts to thermal and power state. [S-GAME-32] Set `Application.targetFrameRate` and the vertical-sync setting deliberately, because the mobile default is a fixed 30 fps. [S-GAME-33]
- **Battery levers:** lower frame rate on menus, lower resolution scale, fewer or cheaper effects, stop network polling when idle, no wake locks, pause the simulation in the background.
- **Cost:** adapting quality gives up a uniform look and takes testing on many devices; fixing a lower target gives up a few features and is predictable.

## Profiling method: measure before you decide

1. **Reproduce** the slow case on the device with a repeatable path (a recorded input, a test scene).
2. **Find the bottleneck type** before touching code: main-thread CPU, render thread, GPU, memory, loading or I/O. Optimising the wrong one changes nothing. Capture one frame trace and look at the longest bar.
3. **Change one thing, measure again, keep the result in a note** (before and after, device, build).
4. **Tools, per engine:**
   - Unity: Profiler on the device and Play mode, Memory Profiler snapshots, and Frame Timing for CPU and GPU time at run time (GPU values arrive several frames later). [S-GAME-28] [S-GAME-29] [S-GAME-30] [S-GAME-31]
   - Unreal: Unreal Insights traces and the stat commands. [S-GAME-44] [S-GAME-45]
   - Godot: the built-in profiler and monitors, and the performance guide. [S-GAME-52]
   - Android: GPU Inspector and Performance Tuner (frame times from real players by device). [S-GAME-73] [S-GAME-71]
   - Apple: Xcode Instruments and the Metal tools, plus MetricKit for field data. [S-GAME-80] [S-GAME-78]
5. **Field data decides the tiers.** Collect frame time percentiles, memory peaks and crash rates by device model from real players, so the low tier is set from facts. [S-GAME-71] [S-GAME-78]
6. **Before adopting a heavy technique** (a data-oriented rewrite, a custom renderer, an entity framework), show the profile that proves the current approach cannot meet the budget. [S-GAME-64] [S-GAME-48]

## One-way doors (return as approvals)

- The weakest supported device and the target frame rate.
- The render pipeline and the engine's graphics features (hard to swap after content is built).
- The texture and asset format pipeline and the content size per platform.
- Adopting an entity-component data-oriented framework for core gameplay (see `game-architecture-patterns`).

## Failure modes

- Fast on the developer's phone, unplayable on a three-year-old one.
- Hitches from garbage collection or loading on the main thread.
- Memory grows after each level because a load had no release. [S-GAME-41]
- Profiling in the editor and trusting it.
- The budget exists only as a number in a document and is never checked.
- Optimising the average and missing the worst scene.
- No thermal testing, so reviews say the game heats the phone.

## Questions that change the design

Ask before budgeting: the real reference (floor) device, the target frame rate, the typical session length, and the install and download size limits.

- Which exact devices are the floor, and what share of the target market do they hold?
- What is the genre's real need for smoothness: puzzle, action, competitive?
- How big may the install be, and how much may download later?
- How long is a typical session (battery and heat)?
- Which stores and regions (store ranking uses quality data)? [S-MOB-9]

## Review checklist

- [ ] A named weakest device and a target frame rate, with the millisecond budget per system and 20 to 30 percent headroom.
- [ ] Budgets for memory, cold start, level load, download size and battery, each with a measurement method.
- [ ] Measurements were taken on the real device in a development build, over a long session.
- [ ] No allocation in the per-frame code; frequently spawned objects are pooled; every load has a release.
- [ ] Loading is asynchronous and scenes free their memory; in Unity, Addressables groups, reference counts and releases are planned and checked for leaks.
- [ ] Heat behaviour is designed (adaptive quality or a fixed cap) and tested for 20 minutes or more.
- [ ] Field telemetry for frame time, memory and crashes by device model is planned.
- [ ] Any heavy optimisation is justified by a profile.

## Sources
[S-GAME-25] [S-GAME-26] [S-GAME-27] [S-GAME-28] [S-GAME-29] [S-GAME-30] [S-GAME-31] [S-GAME-32] [S-GAME-33] [S-GAME-34] [S-GAME-35] [S-GAME-40] [S-GAME-41] [S-GAME-42] [S-GAME-44] [S-GAME-45] [S-GAME-47] [S-GAME-48] [S-GAME-52] [S-GAME-62] [S-GAME-64] [S-GAME-69] [S-GAME-70] [S-GAME-71] [S-GAME-72] [S-GAME-73] [S-GAME-78] [S-GAME-79] [S-GAME-80] [S-GAME-82] [S-MOB-9] [S-MOB-10]
