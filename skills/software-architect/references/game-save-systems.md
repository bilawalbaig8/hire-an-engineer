# Game save systems

When to read this: the game keeps anything between sessions (progress, settings, purchases, an idle game's offline earnings), or the player can move between devices. Unity gets the most detail because it is the owner's main engine; Unreal and Godot get short pointers. Part of the games set: start at `game-engine.md`.

## Decisions that matter most

**First, ask: does the game have a paid currency or purchases?** If yes, balances and purchases are verified server-side (receipt validation, a server ledger); local anti-tamper is only for non-monetised data. If unknown, it is an architecture-changing question: return `needs_answers` before writing files (`method-design.md`, step 1).

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| What to store | **State only**: the facts you cannot recompute (what the player owns, chose, finished, and when). Derive everything else on load. | Cache derived values only when recomputing is measured to be slow, and mark them as rebuildable. | Storing less gives up a little load time; storing derived data makes saves bigger and lets two copies of a fact disagree. |
| Save format | **Plain structured text (JSON)** for most mobile and indie games: easy to read, diff and migrate by hand. [S-GAME-20] [S-GAME-51] | **Compact binary with a schema** (a protobuf-style format) when saves are large, sent over the network often, or must stay compatible for years. [S-GAME-88] [S-GAME-68] **A single SQLite file** when saves hold many records that change independently (inventories, a world map). [S-GAME-87] | JSON gives up size and speed. Binary gives up easy hand-editing and needs tooling. SQLite gives up a simple file you can open in a text editor and adds a library to ship. |
| Never use | **A general object-graph serializer from the language** (in .NET, BinaryFormatter) for saves. It is insecure, and recent .NET versions removed it. [S-GAME-92] | A schema you control. | Nothing worth keeping. |
| Version and migration | **A format version number in every save**, plus a chain of small upgrade steps (v1 to v2, v2 to v3), tested against real old saves. | Version-tolerant formats alone (add fields, never reuse or retype them) when the format is schema-based. [S-GAME-88] | A migration chain gives up some code and test effort per release; skipping it gives up every player's progress the first time the format changes. |
| Write safety | **Write to a temporary file, flush it to storage, then replace the real file**, keeping the previous good copy as a backup. [S-GAME-90] [S-GAME-91] | A database file with transactions does this for you. [S-GAME-87] | Extra code and one extra copy on disk; plain overwrite gives up the whole save when power fails mid-write. [S-GAME-89] |
| Where saves live | **Local file is the working copy, cloud is a synced backup** for games that must work offline. [S-MOB-2] | **Server owns the profile** when the game has paid currency, trading or competition. | Local-first gives up instant cross-device freshness and needs a conflict rule. Server-owned gives up offline play and costs servers. |
| Cloud provider | **The platform's own service** (Google Play Games saved games, Apple Game Center/iCloud, Steam Cloud) for a single-platform or per-store game that needs no account system. [S-GAME-74] [S-GAME-81] [S-GAME-85] | **Your own backend or a hosted service** (for example Unity Cloud Save) when players move between platforms, you run a live economy, or you need support tools. [S-GAME-22] | Platform services give up cross-platform progress and control; your own backend gives up money, work and privacy duties. |
| Anti-tamper | **Match the defence to what a cheat damages** (see the levels below). | Nothing for single-player offline games. | Each level adds cost; the top level adds server cost and latency. |

## What to store: state versus derived

- **Store:** unlocks, owned items (by stable ID), counters that only the player's actions change, currency as a list of earn and spend events or a balance with a version, timestamps (last saved, last seen), settings, tutorial flags, and the seed for anything random that must repeat.
- **Derive on load:** stats computed from items plus a data table, UI layout, anything the data tables can regenerate, the current screen.
- **Never store:** engine object references, scene paths or object instance numbers, display text (store IDs; text comes from localisation), secrets.
- **Idle and offline-earning games:** store the rate inputs and the last-saved timestamp, then compute offline gains on load from the elapsed time, with a cap. The device clock is easy to change, so for anything that matters use server time or accept that cheating the clock only hurts the cheater.
- **IDs are forever.** Item, quest and currency IDs written to saves must never be renamed or reused. Keep a table of retired IDs and what they map to. This is the most common cause of broken old saves.
- **Keep the settings apart from the progress.** Different lifetimes: settings may reset or sync differently; progress is precious.

## Versioning and migration

1. Put `formatVersion` (a whole number) and `savedByAppVersion` at the top of every save.
2. Write each upgrade as a pure function from one version to the next. Run old to new in order. Never edit a historical step after release.
3. Keep **real saves from every released version** as test files and run the full chain over them in automated tests.
4. **A newer save opened by an older app:** refuse to load it and never overwrite it. Tell the player to update. This happens with cloud saves between a phone on the new version and a tablet on the old one.
5. Unknown fields: keep them if your format allows (so an older app does not erase a newer app's data), or refuse as in step 4.
6. After a migration, write the upgraded file to a new slot and keep the old file until the next successful save, so a bug in the migration is recoverable.
7. For a schema format, add fields freely, never reuse a number or change a type, and reserve the numbers of deleted fields. [S-GAME-88]

## Corruption and atomic writes

- Simple overwrites lose data when the app is killed or power drops partway through. [S-GAME-89]
- The safe pattern: write the new data to a temporary file in the same folder, flush it to stable storage, then rename or replace it over the real file; keep the last good file as a backup. [S-GAME-90] The .NET `File.Replace` call does the replace and backup in one step where the platform supports it. [S-GAME-91]
- Put a checksum (a CRC or hash over the contents) in the file. On load, if the main file fails the check or fails to parse, fall back to the backup, then to the cloud copy, and tell the player what happened.
- **Save at the right moments:** on pause or background (mobile systems may close the app with no further warning), after meaningful events (a purchase, a level finished), and on a slow timer. Not every frame, and not on the main thread if the file is large: take a snapshot of the state in memory, then write it on another thread.
- **Purchases and rewards are saved before they are shown as given**, and the grant is idempotent (applying it twice does nothing), so a crash between payment and save does not lose or duplicate it.

## Cloud saves and conflicts

A conflict happens when two devices changed the same save while apart. Decide the rule before building sync. [S-MOB-2]

| Conflict rule | Choose when | What it gives up |
|---|---|---|
| **Whole save, pick one** by progress score (not timestamp alone), with a clear "which do you want?" screen showing playtime and progress | Single-player story or level games | Throws away the other device's work; the screen is needed because devices have clocks that disagree |
| **Merge by field**: take the larger of monotonic counters, the union of unlocks, the newer of settings | Games where progress mostly only goes up | More code and tests; a wrong rule duplicates or loses items |
| **Merge events**: save a ledger of earn and spend events with unique IDs, apply each once | Anything with currency | The ledger grows (compact it with a signed snapshot) and needs careful design |
| **Server wins** | A server-owned profile (live economy) | Local offline changes can be lost unless they are sent as events |

Platform limits: Google Play Games saved games allow up to 3 MB of data per save, work offline and sync later, and carry metadata and conflict handling. [S-GAME-74] Steam Cloud has per-user size and file-count quotas that you set, syncs before and after each session, and the player can turn it off, so do not assume it ran. [S-GAME-85] Check the current limits of any platform service before you choose it.

Also decide: which account links the cloud save (a platform account, your own, or anonymous), what happens when the player reinstalls with no account, and how a player deletes their cloud data (a privacy duty in many regions; confirm with the owner's legal adviser).

## Anti-tamper levels

| Level | What it does | Choose when | What it gives up |
|---|---|---|---|
| 0. None | Plain file; the player can edit it | Single-player offline games with no rewards outside the device | A player can cheat; only they are affected |
| 1. Make casual edits hard | Checksum and light obfuscation | You want to stop accidental or trivial edits; it is also your corruption check | Anyone with a few hours defeats it. Never rely on it |
| 2. Sign or encrypt on the device | A key held in the app | Almost never worth it. The key is in the app, so determined users extract it. [S-GAME-86] | Cost and false confidence |
| 3. Server-validated state | The server holds or checks anything of value; the device holds a copy | Paid currency, items players can trade or gift, rankings, shared events | Needs servers, latency, a rules engine and support tools |
| 3+. Attestation | The server asks whether the request came from a genuine app on a genuine device. [S-GAME-75] [S-GAME-83] | A game with real money or high-value rewards under active attack | Adds a dependency on platform services and rejects some legitimate users (rooted or older devices) |

The rule: **protect what damages other players or the money, not what only damages the cheater.** In Unity, PlayerPrefs is stored unencrypted, so it is not a place for anything sensitive. [S-GAME-18] No client-side defence is a guarantee; treat it as delay. [S-GAME-86]

## Unity specifics

- **PlayerPrefs:** for small settings only (volume, language). It lives in a platform-specific place (the registry on Windows, a plist on macOS, browser storage with a 1 MB cap on web), is not encrypted, and is awkward to back up or migrate. [S-GAME-18] Do not put progress in it.
- **File location:** `Application.persistentDataPath` for save files. Files there are kept across app updates as long as the bundle identifier does not change, and only the player can erase them. [S-GAME-19] Changing the bundle identifier or company name changes the location, so lock them early. What happens to those files on uninstall and reinstall differs by platform (not checked here), so test the reinstall path on each platform you ship.
- **Serialisation:** Unity's `JsonUtility` is fast and built in but has limits on what it can serialise (check the rules for your types). [S-GAME-20] [S-GAME-21] If you need dictionaries or polymorphism, use a JSON library or convert to plain data classes first. Plain data classes that hold only IDs and numbers, separate from MonoBehaviours, are the best save types: they migrate cleanly.
- **ScriptableObjects are for read-only data**: in a built player you can read saved ScriptableObject assets but changes are not kept. Do not use them as save files. [S-GAME-36]
- **Never serialise engine object references.** Save stable IDs and look the object up on load.
- **Threading:** build the save snapshot on the main thread, write the bytes on another.
- Do not use BinaryFormatter. [S-GAME-92]

Unreal: SaveGame objects written to named slots; same versioning and corruption rules apply, so add your own version field. [S-GAME-46] Godot: your own serialisation of persistent nodes to JSON or binary, with the documented limits of each. [S-GAME-51]

## One-way doors (return as approvals)

Once players have saves, these are hard or impossible to change:
- The save format family (text, schema binary, database) and the **ID scheme** for items and currencies.
- **Currency as a balance or as a ledger.**
- **Which account identifies the player** and which cloud service holds the saves.
- The cloud **conflict rule**.
- Any signing or encryption key arrangement.

Write each as a `proposed` decision record with options, what each gives up, and your recommendation.

## Failure modes

- A release renames an item ID and players lose items.
- A migration bug erases progress because the old file was overwritten.
- The save is written on pause, but the app was killed first, and the player loses the last hour.
- A cloud conflict silently picks the wrong device.
- A newer save loaded by an older app and overwritten.
- Offline rewards exploited by changing the device clock.
- The save file grows without limit (event logs, history).
- Tests only ever run against a fresh save.

## Questions that change the design

- Is there anything in the save that costs money or affects other players?
- Do players use more than one device, or more than one platform?
- How long must an old save keep working (a year, five years)?
- Is progress allowed to be lost in rare cases, or never?
- Are there regions or ages that require data deletion on request?

## Review checklist

- [ ] The save holds state only; derived values are recomputed on load.
- [ ] Every save has a format version and the app version that wrote it.
- [ ] There is an upgrade chain with tests using real saves from every released version.
- [ ] A newer save is never overwritten by an older app.
- [ ] Writes are atomic (temp file, flush, replace) with a backup and a checksum, and loading falls back to the backup.
- [ ] Saves happen on pause or background and after key events, off the main thread when large.
- [ ] Item and currency IDs are stable and retired IDs are tracked.
- [ ] The cloud conflict rule is written and tested with two devices.
- [ ] Anything of monetary value is validated on a server; PlayerPrefs holds only settings.
- [ ] No BinaryFormatter or engine object references in saves.
- [ ] The one-way doors are written as proposed decisions and returned for approval.

## Sources
[S-GAME-18] [S-GAME-19] [S-GAME-20] [S-GAME-21] [S-GAME-22] [S-GAME-36] [S-GAME-46] [S-GAME-51] [S-GAME-68] [S-GAME-74] [S-GAME-75] [S-GAME-81] [S-GAME-83] [S-GAME-85] [S-GAME-86] [S-GAME-87] [S-GAME-88] [S-GAME-89] [S-GAME-90] [S-GAME-91] [S-GAME-92] [S-MOB-2]
