# Run records

Every project-size run (and any run that calls a specialist) leaves a record, so it can be resumed, audited and shown in the visual office.

## The run folder
`.team/runs/<YYYY-MM-DD>-<topic>/` in the project (the owner decides whether it is tracked in git; ask once if unclear, default: ignored).

| File | Content |
|---|---|
| `plan.md` | goal, size, steps (who, order, parallel, needs owner), status per step |
| `NN-<role>-request.json` | the request for step NN (see `briefing.md`) |
| `NN-<role>-response.json` | the specialist's answer, unchanged |
| `decisions.md` | the owner's answers and approvals with date and ids; two-way decisions made by specialists |
| `summary.md` | the closing summary, written when the run closes |

NN is two digits in call order (01, 02, ...). A re-call of the same role gets the next number.

## Event log
Append one JSON line per event to `.agents/events.jsonl` (never edit old lines):
```json
{"ts":"2026-10-23T10:00:00Z","type":"handoff","agent":"orchestrator","run_id":"<session or run id>","from":"orchestrator","to":"architect"}
```
- You write `handoff` (boss to specialist, and back), `approval_requested`, `approval_given`.
- The hook writes `agent_start`, `agent_stop`, `file_written`. Specialists write nothing.
- `ts` is UTC ISO 8601 ending in Z. If the project has `scripts/agent_contract.py`, use `append_event` or run `check-event`.
- Never log a secret.

## Resuming
1. Read `plan.md`, then `decisions.md`, then the last response files.
2. Tell the owner in plain words what is done and what is next.
3. Continue at the first unfinished step with the recorded answers in its request. Never repeat finished steps or re-ask answered questions.
4. If the folder is missing or inconsistent, say so and rebuild the plan from what exists, asking the owner only what cannot be found.
