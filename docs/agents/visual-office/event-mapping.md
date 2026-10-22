# Visual office: event mapping (mock v2 to the live office)

Status: draft spec, 2026-10-23. Mock v2 (`mock-v2.html`) is the approved design. This file says how its demo engine becomes a reader of the real log. Anything marked **assumption** is not confirmed in the repo or docs.

Sources read: `mock-v2.html` (script block), `agent-template/handoff-contract.md`, `scripts/log_event.py`, `scripts/agent_contract.py`, `roster.md`, master plan (Phase 7 and additions), `skills/orchestrator/references/run-records.md`.

Rule that stays: the office only reads `.agents/events.jsonl` (plus run files named below). It never computes state from anything else. The window is a view and an optional second input.

---

## 1. Demo event format versus the real log

### 1.1 Real line (today, `validate_event`)

Required on every line: `ts` (UTC ISO 8601 ending Z), `type`, `agent`, `run_id`. Extra: `path` (file_written), `from` + `to` (handoff). Nothing else is checked, so extra fields are allowed by the validator today (**assumption**: `append_event` keeps unknown fields, yes it dumps the whole dict; `validate_event` ignores them).

### 1.2 Field by field

| Mock field (demo) | Real field | Rule |
|---|---|---|
| `t` (seconds from demo start) | `ts` | `t = (ts - T0)` in seconds, where `T0` = `ts` of the first event of the run being shown. Live: `t` = wall clock since `T0`. Never stored. |
| `type` | `type` | Same six names. New types in section 2.4. |
| `agent` (id like `architect`) | `agent` (name like `architect`, `code-reviewer`, `orchestrator`, `main`) | Looked up through the role registry (section 3). Boss names (`orchestrator`, `boss`, `main` when the session runs the orchestrator) map to `conductor`. |
| `from`, `to` (ids, `conductor`) | `from`, `to` | Same lookup. |
| `path` | `path` | Relative posix path, as written by the hook. |
| `task` (agent_start, handoff) | none today | Demo shows a sentence. Live: `agent_start` shows "Starting" until a following `handoff` to that agent supplies text. New optional field `task` on `handoff` and `agent_start` (section 2.4). Fallback text: "Working". |
| `result` (agent_stop: done / needs_answers / needs_approval / blocked) | none today | `agent_stop` carries no status. New optional field `status` on `agent_stop` is not possible for the hook (it sees no response). Boss writes `agent_result` instead (section 2.4). Until then `agent_stop` means `done`. |
| `note` (agent_stop) | none today | From `agent_result.summary`, first 120 chars. Else "Finished". |
| `id` (approval_requested / given) | none today | New required-for-pairing field `id` on both (section 2.4). Fallback if missing: pair by order, per `agent`, first open request with the same `agent`. |
| `kind` (`questions` / `decision`) | none | New field `kind` on `approval_requested`. Fallback: `decision`. |
| `title`, `why`, `options[]` (id, label, note, rec), `oneWay`, `questions[]` (q, hint, def), `askReply` | response fields `questions` ({id, question, why}), `approvals` ({id, decision, options, recommended, one_way_door}) | Boss copies them into `approval_requested` as `payload` (section 2.4). Mapping: `question` to `q`, `why` to `hint`, `decision` to `title`, `options` strings to `{id,label}`, `recommended` marks `rec`, `one_way_door` to `oneWay`. `def` (suggested answer) and `askReply` have no source: dropped (button "Use suggested answers" hidden unless boss supplies `suggested`). |
| `decision` on approval_given (`answered` / `approved` / `rejected`) | none | New field `decision` on `approval_given` (section 2.4). |
| `option`, `answers[]` | none | New fields on `approval_given`. |
| `by` (`owner` / `demo`) | none | New field `by`: `window`, `terminal`. Mock `demo` disappears. |
| `auto` | none | Dropped. No auto answers live. |
| `_i` (tie order) | line number | Line order in the file breaks ties. |
| (none) | `run_id` | Mock has one run. Live groups by `run_id`; the window shows the newest run, with a run picker (section 4). |

### 1.3 Internal model after the mapping

The window keeps the mock's `S` object unchanged in shape (`agents`, `files`, `log`, `inbox`, `handoffs`, `blocks`, `clock`). Only the source of events changes: a normaliser turns each real line into the mock's event shape, then calls the existing `fire(e)`.

---

## 2. What each event does

### 2.1 Existing events

| Event | Monkey | Prop / motion | Drawer | Badge / state |
|---|---|---|---|---|
| `agent_start` | `agent` wakes, starts working animation (instrument / typing, rising notes or bits) | none | Timeline line "X starts" | chip `Working`, task text, `since = t`; kanban to Doing; counts update |
| `agent_stop` (no `agent_result` seen) | `agent` stops working, bow/star | none | Timeline "X stops" | chip `Done`, kanban Done |
| `handoff` from to | `from` hands over; `to` turns, `recv` pulse | flying sticky note / sheet / note (theme verb) from `from` desk to `to` desk (via meeting room in layout B) | Timeline "X hands off to Y: task"; Rehearsal list (last 3) | `from.hand++`; if `to` not working, `to` = `idle` with text "Brief: task" (kanban To do) |
| `file_written` | `agent` | file name pops above monkey for 2.5 s | Files tab: new top row `path`, "by X at m:ss", counter; Timeline line | `agent.files++` |
| `approval_requested` | `agent` (the asker) switches to `Waiting for you` (kind questions, hand up) or `Needs approval` (kind decision, card held up); owner seat glows | none | Inbox: new card (pulse the Panels button or Inbox tab if drawer closed or another tab open); `one_way_door` shows the door tag | owner chip `Needed now` ("N items waiting for you"); Panels badge = pending count |
| `approval_given` | asker returns to `idle` ("Answer received", "Rework requested" if rejected) until the boss hands off again | none | Inbox card resolves (read-only, verdict + answers); Timeline "You approved X" (`by`: window or terminal) | owner back to `Watching` when pending = 0 |

Unknown `type`: ignored by the scene, shown in Timeline as a grey line with the raw type (nothing is silently dropped).

### 2.2 Role states (state machine)

| State | Chip | Enter on | Leave on |
|---|---|---|---|
| idle | Idle | start of run; `approval_given` for this agent; `handoff` to it while not working ("Brief: ...") | `agent_start` |
| working | Working | `agent_start`; `run_started` for the boss | `agent_stop`, `agent_result`, `approval_requested` from it |
| waiting (for the boss's relay to the owner) | Waiting for you | `agent_result` status `needs_answers`, or `approval_requested kind=questions` | `approval_given` with same `id` |
| needs owner (approval) | Needs approval | `agent_result` status `needs_approval`, or `approval_requested kind=decision` | `approval_given` with same `id` |
| done | Done | `agent_stop` with no later `agent_result` problem, or `agent_result` status `done` | next `agent_start` or `handoff` to it |
| blocked | Blocked | `agent_result` status `blocked`, or boss event `blocked` | next `agent_start` for that agent (a fix handoff) or `blocker_cleared` |
| watching (owner only) | Watching / Needed now | always; pending count decides | n/a |

Precedence when several apply to one agent: blocked > approval > waiting > working > done > idle, but a newer event always replaces the older state (the machine is event driven, the table is for tie handling inside the same second). Hook order caveat: `agent_stop` is written by the hook when the subagent ends, `agent_result` by the boss after it reads the response, so the pair arrives in that order, usually seconds apart. The office briefly shows `Done`, then corrects to the real status. To avoid the flicker: when `agent_stop` arrives, hold the state for up to 3 s (live mode only) waiting for `agent_result` from the same agent; if none, apply `done`. Replay needs no hold (the whole log is known). (**assumption**: 3 s is enough for the boss to log; tune in testing.)

### 2.3 How blocked / needs_answers / needs_approval show up today

Today they do not exist in the log. `agent_stop` has no status; the response JSON (with `status`) goes only to `.team/runs/<run>/NN-<role>-response.json` and the boss's chat. So a live office reading only the log would show a blocked or waiting specialist as `Done`. That is wrong, and is the main gap. Two sources can fix it:

1. Preferred: the boss logs it (section 2.4, `agent_result`). One line, written right after it saves the response file.
2. Fallback for old logs: `approval_requested` from agent X, with no `agent_result`, sets X to waiting or approval; blocked cannot be seen. Mark the office with a small banner "Log has no result events; blocked states may be missing" when an `agent_stop` run exists with zero `agent_result` lines (**assumption**: banner wording).

### 2.4 Proposed new events and fields (minimal)

All additive. Old readers ignore them. `EVENT_TYPES` in `scripts/agent_contract.py` gets the new types; `validate_event` gets the checks in the last column. Contract document updated in the same change.

| New event / field | Written by | Fields | Meaning | Validation |
|---|---|---|---|---|
| `run_started` | boss (orchestrator) | `agent`=boss, `run_id`, `goal` (short text), `size` (optional) | A job begins. Office sets boss `working`, title board "Today's job: goal", picks run. | `goal` required text |
| `run_finished` | boss | `run_id`, `status` (`done`, `stopped`, `failed`), `summary` (short) | Job closes. Boss `done`, summary card shown (mock `showSummary`). The mock ends on boss `agent_stop`; live ends on this. | `status` in set |
| `agent_result` | boss, after saving the response file | `agent` (specialist), `run_id`, `status` (`done`, `needs_answers`, `needs_approval`, `blocked`), `summary`, `response_file` (relative path, optional) | Carries the contract `status` the hook cannot see. Drives the chip, the note and the blocked count. | `status` in the four contract values |
| `question_asked` | boss, when it relays a `needs_answers` response | `id` (the group id, e.g. `q-<NN>`), `agent` (asker), `questions` ([{id, question, why}]), `run_id` | The owner is asked. Creates the Inbox card, kind questions. | `questions` non-empty |
| `approval_requested` (extended) | boss | adds `id`, `kind`=`decision`, `title`, `why`, `options` ([{id, label, note, recommended}]), `one_way_door` (bool), `asked_agent` (who needs it) | Same event type, richer payload. `agent` stays the boss (it is the writer), `asked_agent` is the specialist the monkey changes state for. | `id` required when `kind` present |
| `approval_given` (extended) | boss (after it gets the answer from the terminal) or office server (when the answer came from the window, section 5) | adds `id`, `decision` (`answered`, `approved`, `rejected`), `option`, `answers` ([{id, answer}]), `by` (`terminal`, `window`) | Resolves the card with the same `id`. | `id` required when `decision` present |
| `blocked` | boss | `agent` (blocked specialist), `reason` (short), `run_id` | Boss-owned blocker that is not a specialist response (missing tool, failed test, owner unreachable). Same visual as `agent_result` blocked. | `reason` required |
| `blocker_cleared` | boss | `agent`, `run_id` | The block is resolved without re-calling that specialist. | none extra |
| `handoff` (extended) | boss | adds optional `task` (short sentence, no secrets) | Text for the speech line and "Brief: task". | optional |

Who writes what stays consistent with the contract: hook = `agent_start`, `agent_stop`, `file_written`; boss = everything else; specialists write nothing. The office server writes only `approval_given` with `by: window` (and only after the boss has confirmed, see section 5.3), plus `.team/inbox.jsonl`. **Assumption**: the boss may also write `approval_given` for terminal answers; run-records.md already says the boss writes `approval_requested` and `approval_given`.

One-way door rule: `one_way_door: true` shows the door tag on the card, the chip uses a diamond, the default selected option is the recommended one, and "Approve" asks one extra confirm click in the window (**assumption**: extra confirm is wanted).

---

## 3. Role registry

### 3.1 Core 12 (monkeys that exist in mock v2)

| Mock id | Display name | Desk zone (layout B) | Matches log `agent` name (aliases) | In `roster.md` today |
|---|---|---|---|---|
| conductor | Boss (theme Orchestra: Conductor) | glass office | `orchestrator`, `boss`, `main` when the boss runs the session | boss is not listed by design |
| architect | Solution Architect | Engineering | `architect` | yes |
| dbarch | Database Architect | Engineering | `database-architect`, `data-architect` (**assumption**: final names unknown) | no |
| pm | Product Manager | Product | `product-manager` | no |
| ba | Business Analyst | Product | `business-analyst` | no |
| ux | UX/UI Designer | Design | `ux-designer`, `ux-ui-designer` | no |
| fe | Frontend Engineer | Engineering | `frontend`, `frontend-engineer` | no |
| be | Backend Engineer | Engineering | `backend`, `backend-engineer`, `backend-api` | no |
| qa | QA / Test Engineer | Quality and Security | `qa`, `qa-test` | no |
| reviewer | Code Reviewer | Quality and Security | `code-reviewer` | yes |
| security | Security Engineer | Quality and Security | `security`, `security-engineer` | no |
| devops | DevOps Engineer | Ops | `devops`, `devops-platform` | no |
| owner | You, the owner | Visitor seat / box seat | never in the log as `agent`; stands for the human | n/a |

Rule: the agent file name in `agents/*.md` (equal to the `agent_type` the hook logs) is the key. Aliases above are only a seed; the source of truth is a registry file (3.2).

### 3.2 Registry file

A single file `docs/agents/visual-office/roles.json`, shipped with the office (**assumption**: location and name), one entry per known role:

`name` (log key), `id` (monkey id), `display`, `short`, `role` (one plain sentence), `zone`, `color`, `props` (office, orchestra), `aliases`.

It replaces the hard-coded `AGENTS`, `PROPS`, `DESK` and the zone lists in `buildHall` / `buildOffice`. A check script (extension of `scripts/check_roster.py`, **assumption**) fails when a row in `roster.md` has no `roles.json` entry (so a new built role cannot ship without a place in the office), and the other way round only warns.

### 3.3 How roles appear automatically

1. On start the server reads `docs/agents/roster.md` (table `Name`) and `agents/*.md` of the project (or installed agents folder), and `roles.json`.
2. Every roster row gets a desk at once, state `idle`, even before it has done anything (the whole team is visible; matches the Phase 7 rule that every built role is added).
3. Roster rows with a `roles.json` entry use their own monkey; rows without one use a generic monkey (3.4).
4. The roster is reloaded when `roster.md` changes (file watch or every 5 s), so a role added mid-session gets a desk with a small "joins the team" pulse (**assumption**).
5. Desks are placed by `zone` from `roles.json`; a zone with more seats than space grows its row; layout engine (`fit`) already scales the scene so everything stays visible.

### 3.4 Unknown agent names

An `agent` (or `from` / `to`) not in the registry or roster, for example a built-in `general-purpose`, `Explore`, or a future role:

| Case | Behaviour |
|---|---|
| Name not known | Generic monkey (plain brown fur, no instrument, grey tag), display name = name with dashes to spaces and capitalised; desk added to a "Visitors" zone (layout A: end of the back row; B: next to the kitchen; C: last card). State machine identical. |
| Name is `main` and a boss exists in the run | Treated as the boss (the main session, file writes by the boss land on its desk). |
| Name is `main` and no `run_started` or `orchestrator` events | Shown as the Boss too (single-agent mode: the whole job is the main session) (**assumption**). |
| Name like `general-purpose` / `Explore` / `Plan` | Generic monkey, labelled "Helper". |
| `from` / `to` unknown in a handoff | Same rule, created on first sight. |
| Roster row but never seen in the log | Idle desk, counted in "Idle". |

Generic desks are kept for the rest of the run so the timeline entries never point to a missing seat. Cap: 24 generic desks, then new unknown names share one "Others" seat (**assumption**).

---

## 4. Files, replay and speed

### 4.1 Files tab and timeline

| Item | Rule |
|---|---|
| Files row | One row per `file_written` line, newest first: `path`, "by <display> at m:ss". Same path written again: new row, tagged "updated", no dedupe (log is append only). Counter = rows. |
| Grouping | Optional filter chips by top folder (`docs`, `src`, `tests`, ...) (**assumption**, not in mock). Click row copies the path. The window never opens or reads file content (local path only shown). |
| File outside the project | The hook already drops it; nothing to show. |
| Run records | Files under `.team/runs/<run>/` appear tagged "run record" and are hidden by default behind a toggle (noise). |
| Timeline row | One row per event, newest first, text per type as in the mock (`logLi`) plus the new types: `run_started` "Job started: goal", `agent_result` "X reports: status, summary", `question_asked` "Boss asks you: ...", `blocked` / `blocker_cleared`, `run_finished`. Tag shows the type. Unknown types shown grey. |
| Timestamps | m:ss since `T0` (mock behaviour). Hover shows the real local time from `ts`. |
| Secrets | Event text is shown as is; the boss must not log secrets (run-records.md rule). The window never shows `ts`-less or non-JSON lines; a bad line is counted ("1 line skipped") (**assumption**). |

### 4.2 First load of an existing log (replay)

1. Server serves the whole file; the window parses line by line, skipping invalid lines, and groups by `run_id`.
2. Default shown run: the newest `run_id` (latest `ts`). A run picker in the drawer footer lists others ("older runs"). **Assumption**: one `run_id` = one session id from the hook, so a long session with several jobs is one run until the boss logs `run_started`; with `run_started` / `run_finished` present, jobs inside a run are split by those lines (a job id = `run_started` line number; **assumption**).
3. Load mode is catch-up, not playback: use the mock's `seek` approach (quiet mode: no flying notes, no pops, no pulses, no animation delays) and apply all events instantly, so the office opens in the correct current state. Kanban, counts, timeline, files and inbox are filled; pending questions are open.
4. If the run is finished (`run_finished` or last event older than 30 min with no open agent, **assumption**), show the end state plus the summary card button, and a "Replay this run" button.
5. "Replay" = the mock's play engine: clock from 0, speed control 1x / 2x / 0.5x (existing control), plus 4x and 8x (**assumption**), with real gaps compressed: any gap between two events above 4 s (scaled by speed) is shortened to 4 s so an hours-long log replays in minutes. The clock shown is real elapsed time since `T0`; a small "(compressed)" tag shows while compression is on.
6. Live mode: events appended after load are applied as they arrive (server pushes new lines, section 6), in real time, with animations, speed fixed to 1x. Pause is for replay only.
7. Large log: above 50 000 lines, load only the last run (**assumption**).
8. Pending items from the past: an `approval_requested` with no `approval_given` is still open if its run is the live run. In an old finished run it shows as "Never answered" (grey), and the owner's chip does not say "Needed now" (**assumption**).

---

## 5. Owner's answers

### 5.1 Channels (from master plan additions)

Answer in the terminal or the window, first answer wins, both places show the result. Window to session channel is not verified yet (plan: check Claude Code docs for pushing external events, run a small test; fallback = read-only window). This spec defines the window side so it works in both cases.

### 5.2 What the window sends

`POST /answer` to `scripts/office_server.py` (localhost only, bound to 127.0.0.1, random token in the URL the hook opens, rejected otherwise; **assumption**: token scheme). Body JSON:

| Field | Meaning |
|---|---|
| `id` | the `id` of the `approval_requested` / `question_asked` |
| `run_id` | the run |
| `kind` | `questions` or `decision` |
| `decision` | `answered`, `approved`, `rejected`, or `asked` (owner asks a follow-up instead) |
| `option` | chosen option id (decision) |
| `answers` | `[{id, answer}]` (questions; empty text allowed, means "use your best judgement" as in the mock) |
| `text` | free text: the follow-up question for `asked`, or a note |
| `sent_at` | ISO time from the window |

Server steps: validate token, check `id` exists and is still open (no later `approval_given` with that `id`), append one line to `.team/inbox.jsonl` (one JSON per line: the body plus `ts`, `seq`), return `200 {status: "queued"}`; if already answered return `409 {status: "already_answered", by: ...}` and the window refreshes the card. The server never edits `events.jsonl` itself for the question (the boss does, section 2.4); **assumption**: it may write `approval_given by window` only after the boss confirms receipt by reading `.team/inbox.jsonl` (the boss appends `approval_given` with `by: window`, so the contract "boss writes it" stays true and one writer owns the line).

Delivery to the session is the unverified part: the boss reads `.team/inbox.jsonl` when the channel exists (push event) or when the owner types "check window" in the terminal; if neither works the card says "Answer saved; tell the Boss in the terminal to read it" (fallback, **assumption**).

### 5.3 First answer wins

Terminal answer: boss logs `approval_given by terminal` -> the window (reading the log) resolves the card ("You answered in the terminal"). Window answer: card shows "Sent to the Boss, waiting for confirmation" until the boss writes `approval_given by window`; then it resolves. If a terminal answer lands first, the window answer is dropped by the boss (it checks the `id` was open) and the card shows the terminal answer.

### 5.4 Inbox tab presentation

| Item | Behaviour (as in the mock card) |
|---|---|
| Order | Newest first. Pending on top, resolved below, greyed and read-only. |
| Questions card | Title "N questions from <role>", "From <role>, relayed by the Boss", one text field per question with `why` as hint, buttons "Send answers" and (only if the boss gave `suggested`) "Use suggested answers". Unanswered fields are sent empty. |
| Decision card | Title = decision, `why`, options as radio with note, recommended pre-selected and tagged "Recommended". Buttons Approve, Ask a question, Reject. |
| One-way door | Dark tag with a door icon "One-way door: hard to undo" at the top of the card, above `why`; the owner chip and Panels badge go "hot"; Approve needs one extra confirm; cards with a door sort above other pending cards. |
| Ask a question | Sends `decision: asked` with `text`; card shows "Question sent. The Boss is checking with <role>."; the boss answers by writing a new `question_asked`-style reply in `.team/inbox.jsonl` thread (**assumption**: reply event name `boss_reply`, with `id`, `text`); until the reply arrives the decision stays pending. The mock's canned `askReply` is replaced by this. |
| Engaged protection | Keep the mock's rule: a card being typed in or open for asking is never auto-resolved from under the owner; a resolve from the terminal shows a notice and locks it after the owner leaves the field (**assumption**). |
| Empty / count | "Nothing waiting for you." Count in Panels badge and the Inbox tab; badge hidden at 0. |
| Notification | Panels button pulse if drawer closed, tab pulse if another tab is open; optional browser notification only if the owner allows it (**assumption**). |
| Reject | Sets asker to `idle` ("Rework requested"); boss then hands off again. |

Other drawer tabs: Timeline and Files as in section 4. Legend: shows the six states and a seventh "needs you" glyph row exactly as the mock (`buildLegend`); no change except the text for `blocked` mentions both sources.

---

## 6. What changes in mock-v2.html

No code here, only places.

| Area in `mock-v2.html` | Change |
|---|---|
| `AGENTS`, `OWNER`, `PROPS`, `BY`, `DESK`, and the zone lists inside `buildHall` / `buildOffice` / `buildChart` | Load from the registry (`roles.json` + roster) at start; build desks for any number of roles; add the generic monkey, Visitors zone and "Others" seat. `monkeySVG(id)` and `PXD` need a fallback skin for unknown ids. |
| `EVENTS` array, `TOTAL`, `S.queue`, the demo clock in `tick()` and `setInterval(tick,100)` | Remove the scripted data. Replace with an event source: initial `GET /events` (whole log), then a live stream (Server-Sent Events or polling every 1 s on `GET /events?after=<n>`, **assumption**: SSE). Normaliser from section 1 turns lines into mock events; a `T0`-based clock replaces the demo clock. |
| `fire(e)` | Add cases for `run_started`, `run_finished`, `agent_result`, `question_asked`, `blocked`, `blocker_cleared`; apply the 3 s hold for `agent_stop`; fall back to pairing by order when `id` is missing; end-of-run now triggers on `run_finished`, not on boss `agent_stop`. |
| `RESSTATE`, `LABEL` | Source = `agent_result.status` (same four values). |
| `resetSim`, `OfficeMock.seek` | Seek becomes the catch-up loader for a log (quiet mode); reset clears only view state, not the log. |
| Play controls (`#play`, `#reset`, speed `SPEEDS`, `paintPlay`) | Become Live / Replay controls: Live badge, Replay button for a chosen run, speeds add 4x and 8x, gap compression, run picker. "Play demo run" text goes. |
| `userResolve`, `addCard`, `resolveCard`, `engaged`, `givenText` | `userResolve` calls `POST /answer` and waits for the boss's `approval_given` (section 5.3); `addCard` built from the new payload fields (suggested answers optional, `askReply` removed); `resolveCard` shows `by: terminal / window`; remove the `by: demo` wording. |
| `addLog`, `logLi` | New row texts for the new types; unknown-type row; hover real time. |
| `popFile`, Files list (`#flist`) | Add "updated" tag, folder filter, run-record toggle; keep pop animation. |
| `showSummary`, `#summaryCard` | Stats computed from the log (monkeys that took part, files, handoffs, requests to the owner, blocks), not hard-coded text ("PostgreSQL", "Security found"). |
| Board text ("Today's job: A booking website...") in `buildOffice` | From `run_started.goal`; before that "No job yet". |
| `renderKanban`, `renderSummary`, `paintCounts` | Work on any number of roles; kanban "To do" = handoff received, not started. |
| Themes (`setTheme`, `bossName`, `passVerb`) | Keep Office, Orchestra, Pixel (plan: Pixel redone or dropped before final build; **open**). Boss name follows theme as today. |
| Legend (`buildLegend`) | Unchanged, text tweak for blocked. |
| Header / controls | Add connection indicator (Live, Reconnecting, Read-only), run picker, "Answers are read-only" note in fallback mode. |
| Hash (`hashSync`) | Keep theme and layout; add `run=` only if needed (**assumption**: not needed). |
| `window.OfficeMock` | Keep a test hook (`seekTo`, `getState`) for the test plan; rename for live (`Office`). |

Outside the HTML: `scripts/office_server.py` (serve files, `/events`, stream, `/answer`, token, roster read, localhost only), `scripts/agent_contract.py` (new types and fields), `scripts/log_event.py` (no change needed), orchestrator skill `run-records.md` and agent file (boss writes the new events), `handoff-contract.md` (event table), `check_roster.py` (registry check).

---

## 7. Test plan

Goal (plan Phase 7 step 7): prove the office shows what really happened.

### 7.1 Fixtures

| Fixture | Content |
|---|---|
| `fixtures/events-demo.jsonl` | The mock's 48 s script converted to real lines (one-to-one, all event types, one question group, one one-way door, one block, a fix handoff). Source of truth for expected states. |
| `fixtures/events-real-run.jsonl` | A real recorded `.agents/events.jsonl` from a real job (plan step 6: a real problem given to the boss and specialists), copied unchanged. |
| `fixtures/events-old.jsonl` | Only the six old event types, no ids (fallback behaviour, banner). |
| `fixtures/events-unknown.jsonl` | Unknown agents, bad lines, `main`, repeated paths, out-of-order `ts`. |
| `.team/runs/<run>/` of the real run | The response files: independent ground truth for `status`. |

### 7.2 Method: replay and compare

1. Write `office_model` = the pure part of the window (normaliser + `fire` + state table) in a testable form (no DOM; **assumption**: split out of the HTML as `office-core.js`, run with Node).
2. Compute expected state independently from the raw log with a small separate script (`expected_state.py`): per agent last event wins; counts of files, handoffs, blocks; open inbox ids; per-run list of files. For the real run also derive status from the `NN-<role>-response.json` files.
3. Feed the log into the core, take the state at the end and at 5 cut points (after each `approval_requested`, each `agent_stop`, each `blocked`), compare with the expected values.
4. Compare in the browser too: load the fixture, call `Office.getState()`, and compare to the same expected JSON; take a screenshot per theme and layout at the cut points and check chips, badge count, inbox count, timeline length, files count against the DOM text (extends the mock's `audit`).
5. Reality check (human, once per real run): list from the office "who did what" (summary card) and compare by hand with `summary.md` and `git status` / `git log` of the run: every file in the Files tab exists, every file changed by the specialists in the run appears (the hook only sees Write and Edit, so files created by Bash are expected misses: list them in the report as a known gap).

### 7.3 Checks (pass / fail)

| # | Check | Pass when |
|---|---|---|
| 1 | Field mapping | Every real line of the demo fixture normalises to a mock event with the table values |
| 2 | State per agent | Final chip equals expected for all roles (idle, working, waiting, approval, done, blocked) |
| 3 | Blocked | `agent_result blocked` and `blocked` event both give the blocked chip; later `agent_start` clears it; count in summary equals the number of blocked events |
| 4 | Questions / approvals | Pending count = requests without a matching `approval_given`; one-way door tag only where `one_way_door` is true |
| 5 | Pairing fallback | Old fixture without ids pairs by order and agent, shows the banner |
| 6 | Files | Rows = `file_written` lines; order newest first; same path twice shows two rows |
| 7 | Unknown agents | Generic monkey appears once per name; no exception; cap rule works |
| 8 | Roster | Add a row to a copy of `roster.md`: a desk appears idle within 5 s; a roster row without registry entry gets a generic monkey and the check script warns |
| 9 | Catch-up load | 5 000-line log loads in under 2 s (**assumption**: target) with no animation, final state correct |
| 10 | Replay | Speeds 1x to 8x give the same final state as catch-up; gaps compressed; replay can be paused and resumed |
| 11 | Live append | Appending a line to the file shows in the window within 2 s (**assumption**: target) with animation |
| 12 | Answer round trip | `POST /answer` writes one `.team/inbox.jsonl` line; second answer for the same `id` returns 409; boss `approval_given` resolves the card; terminal-first case resolves the card with "terminal" |
| 13 | Security | Server binds 127.0.0.1 only; wrong or missing token rejected; request body above a size cap rejected; `<script>` in an event `summary` or `path` renders as text (escape check, the mock's `esc`) |
| 14 | Contract | `agent_contract.py check-event` accepts each new event, rejects bad ones (missing `id` with `decision`, bad `status`) |
| 15 | Reality | For the real run, the by-hand comparison in 7.2 step 5 has no unexplained difference |

### 7.4 Order of work

(1) contract change and fixtures, (2) core + tests green, (3) server, (4) UI wiring, (5) answer channel (with the docs check and small test the plan requires), (6) real run recorded and compared, (7) package.

---

## 8. Assumptions and open points (summary)

Assumptions marked above: extra event fields allowed by the validator; alias names for non-built roles; `roles.json` location and the check script; 3 s hold for `agent_stop`; banner for logs without results; run splitting by `run_started`; compression gap of 4 s and the 4x / 8x speeds; 50 000-line limit; localhost token scheme; boss writes `approval_given` for window answers; `boss_reply` event for follow-up questions; extra confirm for one-way doors; unknown-agent cap of 24; `office-core.js` split; performance targets; SSE for live push.

Open (needs the owner or a test): window-to-session channel (docs check and small test, per plan); whether Pixel is redone or dropped; whether the boss may log `task` text (plain language, no secrets).
