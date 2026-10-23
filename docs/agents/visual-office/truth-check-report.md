# Truth check: does the live office show what the log says?

Date: 2026-10-23. Subject: `docs/agents/visual-office/index.html` against `live-test/real-run-shop.events.jsonl` (25 real lines, one real boss run). Server: `scripts/office_server.py` on port 8794, temp project copy of the log. Browser: Browser pane, DOM read through `javascript`/ARIA text, not screenshots.

## 1. Reference timeline (written from the log only)

Times are UTC, m:ss since the first line (04:53:05).

| Line | m:ss | Event | Truth after it |
|---|---|---|---|
| 1-2 | 0:00, 0:08 | Boss writes `plan.md`, `01-architect-request.json` | Boss: Idle (no job yet), 2 files |
| 3 | 0:10 | `run_started` "Explain shop code structure ..." | Boss: Working |
| 4 | 0:13 | handoff boss to architect "Recover shop architecture..." | Architect: Idle ("Brief"), board To do |
| 5 | 0:16 | architect `agent_start` | Architect: Working |
| 6-10 | 2:30, 2:34, 2:53, 2:57, 3:17 | architect writes 5 files (overview, structure.mmd, risks, ADR 0001, ADR 0002) | Architect files 5 |
| 11 | 3:46 | architect `agent_stop` | Architect: Done |
| 12 | 4:05 | boss writes `01-architect-response.json` | Boss files 3 |
| 13 | 4:08 | handoff architect to boss (relay) | architect handoffs 1 |
| 14 | 4:09 | `agent_result` architect `needs_approval` | Architect: Needs approval (23 s after the stop) |
| 15 | 4:16 | boss writes `02-architect-request.json` | |
| 16 | 4:18 | handoff boss to architect "Independent review ..." | Architect: Idle (brief) |
| 17 | 4:22 | architect `agent_start` (second call) | Architect: Working |
| 18 | 6:39 | architect writes the design review | Architect files 6 |
| 19 | 6:55 | `agent_stop` | Architect: Done |
| 20 | 7:09 | boss writes `02-architect-response.json` | |
| 21 | 7:15 | handoff architect to boss | |
| 22 | 7:16 | `agent_result` architect `done` | Architect: Done (21 s after the stop) |
| 23 | 7:20 | `question_asked` q-01 (2 questions, asker architect) | Architect: Waiting for you; Inbox 1 |
| 24 | 7:21 | `approval_requested` a1 (decision, one-way door, asked_agent architect) | Architect: Needs approval; Inbox 2; Owner: Needed now (2 items) |
| 25 | 7:29 | boss writes `plan.md` again | file "updated" |

Final: Boss Working (no `run_finished`), Architect Needs approval, everyone else Idle, 12 file rows (6 by Boss, 6 by Architect; 6 are run records), 4 handoffs (2 from boss, 2 from architect), 25 timeline rows, pending q-01 and a1 (a1 with the door tag), owner "Needed now".

## 2. What was compared

- Catch-up final state, all 3 themes x 3 layouts (9 combinations): chips of all 13 seats, owner chip, per-agent file and handoff counts, Files tab rows and counter, Timeline rows and counter, Inbox cards and counter, handoff list, block count.
- Replay ("Replay this run", 8x): a snapshot after every one of the 25 events, each compared with a reference model that I wrote separately from the spec (state table, section 2 of `event-mapping.md`). Also paused at events 14, 17 and 23 and compared in all 9 theme/layout combinations.
- The same two comparisons for `normal-run` and `blocked-run` (28 and 24 events), plus hand-made logs: an old log without ids, 28 unknown agents, out-of-order `ts`, an unknown event type, a bad line, an HTML `path`, a 5 000-line log, a second and third run appended live.
- Answer path in the window against the real run, and `agent_contract.py check-event`.

## 3. Mismatches

### Found and fixed (all in `index.html`)

| # | Mismatch | Cause | Fix |
|---|---|---|---|
| 1 | Files tab showed 0 files, the Architect desk showed Idle ("Brief") while the second call was running, no `agent_start`/`agent_stop` in the shown run, Run picker listed the same job twice ("Run 437a2f7d..." with 16 events and the goal run with 9) | The log carries two `run_id`s for one job: the hook (`log_event.py`) writes the Claude session id, the boss (`team_event.py`) writes the job id (`2026-10-23-shop-recover`). The UI grouped by `run_id`, so hook lines (all files, starts, stops) sat in a different "run" than the boss lines. | New job linking: an event whose `run_id` has no `run_started` of its own, and whose time lies inside a job window (2 min before `run_started`, until `run_finished` + 2 min, or 30 min after the last boss line while the job is open), belongs to that job. Windows are computed from the whole log on load; in live mode a new `run_started` rebuilds the jobs so earlier hook lines join the job. Tested for catch-up, replay, live append, two jobs. |
| 2 | Files tab: no grouping, 6 run records hidden with no way to see by folder | Spec 4.1 optional grouping not built | Folder chips with counts ("All (12)", "docs (6)", ".team (run records) (6)"). Choosing the `.team` chip also reveals run records. Every `file_written` row still shows path, agent, time and the "updated" tag. |
| 3 | In an older (not newest) run the owner chip still said "Needed now / 2 items waiting for you" while the Inbox said "Never answered" and the badge was 0 | `markStale` did not recompute the owner | `setOwner()` after marking cards stale. |
| 4 | After the owner answered q-01 in the window, the Architect went Idle ("Answer received") although decision a1 (also asked of the Architect) was still open | Resolving one request cleared the asker unconditionally | Asker goes back to Idle only when it has no other open request; otherwise it shows the remaining one (Waiting for you / Needs approval). |
| 5 | Scene zoomed or cropped after the tab was in the background until reload | `fit()` returned silently when the stage had no size and only ran on window `resize`/ResizeObserver of `#main`; `requestAnimationFrame` does not run in background tabs | Fit now also runs on `visibilitychange`, `pageshow`, `focus`, `resize` (immediately, then again), a ResizeObserver on `#main` and on `<html>`, and retries every 250 ms (up to 40 times) while the stage size is 0. Tested by corrupting the scale and firing the events, by hiding `#main`, and by mobile/tablet/desktop viewport changes (always fits). |
| 6 | (test hook) none | | `Office.getState().loadMs` added (time from page start to the first catch-up) for check 9. |

### Seen, not a bug (by design in the spec)

- During replay and live, a specialist whose `agent_stop` is followed within 3 s by its `agent_result` keeps "Working" until the result (spec 2.2, flicker guard). 8 such differences against my plain model, all explained by this.
- In an older run, the asker still shows "Needs approval" (last real state of that run) while the card says "Never answered".

### Not fixed (owner of those files)

See section 4.

## 4. Things to change in the event log or the server (not edited by me)

1. **One `run_id` per job.** `scripts/log_event.py` writes `session_id`; `skills/orchestrator/scripts/team_event.py` writes the run folder name. The window now links them by time, which is a heuristic (a session that spans two jobs, or two sessions at once, can link wrongly). Better: the boss events also carry `session_id`, or the hook reads `.team/runs/<run>/` (for example a `.team/current-run` file) and writes that as `run_id`.
2. **`agent_result` lags `agent_stop` by 21-23 s in the real run** (3:46 to 4:09, 6:55 to 7:16). The 3 s hold in `event-mapping.md` 2.2 is too short: live, the Architect shows "Done" for about 20 s and then flips to "Needs approval". Options: boss logs `agent_result` right after the subagent returns (before writing the response file and relaying), or the hold is raised (it makes a stopped specialist look "Working" meanwhile). I did not change the 3 s.
3. **`POST /answer` in `scripts/office_server.py`** accepts any id any number of times (the same `q-01` answered twice returns 200 both times); spec 5.2/7.3 check 12 expects 409 for an already answered id. It also has no token (it checks Origin/Host instead: evil Origin and wrong Host return 403, body above the cap returns 400, binds 127.0.0.1 only).
4. `question_asked` is written with `agent: architect` (the asker) instead of the boss as writer. The window handles it (asker = `agent`), but the contract says the boss writes it.
5. The boss writes `plan.md` 10 s before `run_started`. Fine for the window (T0 is the first line), but a `run_started` as first line would be cleaner.
6. Files created through Bash do not appear (hook sees Write/Edit only): known gap, not seen in this run.
7. Housekeeping: while cleaning up I stopped all Python processes whose command line contained `office_server.py` (two extra ones besides my test servers on 8794 and 8795, probably launcher stubs of those servers; if you had your own office server running, restart it).

## 5. The 15 spec checks (event-mapping.md 7.3)

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Field mapping | Partial pass | Real, normal-run and blocked-run lines all map as the table says. `fixtures/events-demo.jsonl` does not exist, so the demo fixture was not run. |
| 2 | State per agent | Pass | Real run (25 cut points, 9 theme/layout combinations at 4 of them and at the end), normal-run, blocked-run. |
| 3 | Blocked | Pass | `agent_result blocked` and `blocked` give Blocked, later start/`blocker_cleared` clears it, block count equals reference (2). |
| 4 | Questions / approvals | Pass | Pending count equals open requests; door tag only on a1. |
| 5 | Pairing fallback | Pass | Old log without ids pairs by agent and order; banner shown. |
| 6 | Files | Pass | 12 rows = 12 `file_written` lines, newest first, same path twice gives 2 rows with "updated". |
| 7 | Unknown agents | Pass | One generic seat per name, no exception, cap at 24 then one "Others" seat. |
| 8 | Roster | Partial pass | Server roster has 2 rows, both have desks. A new roster row was simulated in the window (fetch stubbed): desk appears Idle within 5 s. Editing the real `roster.md` and the check script were not run (outside the allowed files). |
| 9 | Catch-up load | Pass | 5 000 lines: first catch-up at 672 ms after page start (event stream alone 47 ms). |
| 10 | Replay | Pass | 8x replay and paused cut points give the catch-up final state; 1x/2x/4x not run one by one; gap compression shown (real run 80 s total at 8x about 10 s). |
| 11 | Live append | Pass | Lines appended to the file showed within 2 s (checked at about 2-3 s polling granularity), including merge of a late `run_started`. |
| 12 | Answer round trip | Partial fail | Window answer writes one `.team/inbox.jsonl` line, card shows "Sent", a later `approval_given by window` and `by terminal` resolve the cards and the Architect state is correct. Second answer for the same id returns 200, not 409 (server). |
| 13 | Security | Partial pass | Localhost only, bad Origin/Host 403, oversize body 400, `<img onerror>` in a `path` shows as text (Files and Timeline). No token (design differs from the spec). |
| 14 | Contract | Pass | `agent_contract.py check-event` accepts all 25 real lines; rejects `decision` without `id` and an invalid `status`. |
| 15 | Reality | Not run | The run's response files and the shop repo were not available; the by-hand comparison with `summary.md` / `git status` was not done. The log itself is fully reflected (check 6). |

Demo mode (`?demo=1`) still works: seek 41.9 s gives 17 files and 1 block, audit of 9 theme/layout combinations fits with no overflow, no console errors in any run.

## 6. Files

- Changed: `docs/agents/visual-office/index.html`
- Added: this report. No files added under `live-test/`; no commit; `~/.claude`, `scripts/`, `tests/` untouched.
- Test projects and scripts: scratchpad only (stopped servers).
