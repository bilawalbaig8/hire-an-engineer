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
Append one JSON line per event to `.agents/events.jsonl` (never edit old lines). You write all of these; the hook writes `agent_start`, `agent_stop`, `file_written`; specialists write nothing.

| Type | Extra fields | Example line |
|---|---|---|
| `run_started` | `goal`, `size` | `{"ts":"2026-10-23T10:00:00Z","type":"run_started","agent":"orchestrator","run_id":"2026-10-23-login","goal":"Add an email login page","size":"project"}` |
| `handoff` | `from`, `to`, `task` | `{"ts":"2026-10-23T10:01:00Z","type":"handoff","agent":"orchestrator","run_id":"2026-10-23-login","from":"orchestrator","to":"architect","task":"Plan the login page"}` |
| `agent_result` | `status`, `summary`, `response_file` | `{"ts":"2026-10-23T10:05:00Z","type":"agent_result","agent":"architect","run_id":"2026-10-23-login","status":"needs_answers","summary":"Needs the sign-in method","response_file":".team/runs/2026-10-23-login/01-architect-response.json"}` |
| `question_asked` | `id`, `questions` | `{"ts":"2026-10-23T10:06:00Z","type":"question_asked","agent":"architect","run_id":"2026-10-23-login","id":"q-01","questions":[{"id":"q1","question":"Email and password, or a link?","why":"Changes the design"}]}` |
| `approval_requested` | `id`, `kind`, `title`, `why`, `options`, `one_way_door`, `asked_agent` | `{"ts":"2026-10-23T10:07:00Z","type":"approval_requested","agent":"orchestrator","run_id":"2026-10-23-login","id":"a1","kind":"decision","title":"Where to store accounts","options":[{"id":"o1","label":"sqlite","recommended":true},{"id":"o2","label":"postgres"}],"one_way_door":true,"asked_agent":"architect"}` |
| `approval_given` | `id`, `decision`, `option`, `answers`, `by` | `{"ts":"2026-10-23T10:08:00Z","type":"approval_given","agent":"orchestrator","run_id":"2026-10-23-login","id":"a1","decision":"approved","option":"o1","by":"terminal"}` |
| `blocked` | `reason` | `{"ts":"2026-10-23T10:09:00Z","type":"blocked","agent":"architect","run_id":"2026-10-23-login","reason":"Tests cannot run: Python missing"}` |
| `blocker_cleared` | none | `{"ts":"2026-10-23T10:10:00Z","type":"blocker_cleared","agent":"architect","run_id":"2026-10-23-login"}` |
| `run_finished` | `status` (`done`, `stopped`, `failed`), `summary` | `{"ts":"2026-10-23T10:30:00Z","type":"run_finished","agent":"orchestrator","run_id":"2026-10-23-login","status":"done","summary":"Login page planned, built and reviewed"}` |

- Every line has `ts`, `type`, `agent`, `run_id`. `run_id` is the run folder name, the same on every line of the run.
- `agent` is the specialist for `agent_result`, `question_asked`, `blocked`, `blocker_cleared`; you (`orchestrator`) for `run_started`, `run_finished`, `handoff`, `approval_*`.
- `ts` is the real current UTC time, ISO 8601 ending in Z: get it with `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) for every line; never invent or round timestamps. If the project has `scripts/agent_contract.py`, use `append_event` or run `check-event`.
- Never log a secret.

## Resuming
1. Read `plan.md`, then `decisions.md`, then the last response files.
2. Tell the owner in plain words what is done and what is next.
3. Continue at the first unfinished step with the recorded answers in its request. Never repeat finished steps or re-ask answered questions.
4. If the folder is missing or inconsistent, say so and rebuild the plan from what exists, asking the owner only what cannot be found.
