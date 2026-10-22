# Live office test files

Sample logs and a feeder for trying `docs/agents/visual-office/index.html` (the live office) against the real server. Test helpers only; nothing here ships with the product.

| File | What it is |
|---|---|
| `normal-run.events.jsonl` | A normal run: one set of questions, one one-way-door approval, a code review, a built-in helper (`general-purpose`, shown as a generic monkey), a run record file, `run_finished`. |
| `blocked-run.events.jsonl` | A run where Security reports `blocked`, Backend fixes it, QA is blocked by a boss `blocked` event and later `blocker_cleared`. |
| `feed.py` | Appends a sample to a project's `.agents/events.jsonl` one line at a time with the current time, so the window follows it live. |

Lines that start with `#wait-answer ID` are only for `feed.py`: it waits until the window has written an answer for `ID` to `.team/inbox.jsonl`, then logs the matching `approval_given` with `by: window`, the way the Boss would. After `--answer-timeout` it logs the sample's own answer with `by: terminal`. The server and the window ignore these lines (not JSON).

## Commands

Run from the repo root. Use any empty folder as the test project.

```
mkdir C:\tmp\office-test
python scripts/office_server.py --project C:\tmp\office-test --port 8791 --no-open
```

Open http://127.0.0.1:8791/ in a browser, then in a second terminal:

```
python docs/agents/visual-office/live-test/feed.py docs/agents/visual-office/live-test/normal-run.events.jsonl C:\tmp\office-test --delay 1.5
```

What to check:

- The architect asks 3 questions; open Panels, answer and press "Send answers". `C:\tmp\office-test\.team\inbox.jsonl` gets one line, the card shows "Sent", `feed.py` logs the `approval_given` and the card resolves.
- The database decision shows the one-way door tag; Approve asks for a second click. "Ask a question" gets a canned `boss_reply`.
- Run `blocked-run.events.jsonl` the same way for the Blocked chips (open the file to see `agent_result` and `blocked` lines).
- Finished runs show a Summary button and "Replay this run" (gaps over 4 s are shortened; speeds 1x to 8x).

Static load (replay catch-up, no feeder): copy a sample over the log, then reload the page.

```
copy docs\agents\visual-office\live-test\normal-run.events.jsonl C:\tmp\office-test\.agents\events.jsonl
```

If you empty or replace `events.jsonl` while the page is open, reload the page (the server restarts its tail but the window cannot tell the file was replaced).

Design review without a server: open `index.html` through the server with `?demo=1`, or press "Demo" in the header (the scripted run from the mock; "Back to live" returns).
