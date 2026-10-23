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
`.agents/events.jsonl`, one JSON line per event, never edited. **Never write these lines by hand.** Run the script of this skill (`SCRIPT` below is `~/.claude/skills/orchestrator/scripts/team_event.py` or `.claude/skills/orchestrator/scripts/team_event.py` in the project; find it with a quick `ls`). It stamps the real UTC time, fills `agent`, checks the fields, refuses a bad event (exit 2, nothing written), creates the folder and appends exactly one line. You write all of these; the hook writes `agent_start`, `agent_stop`, `file_written`; specialists write nothing.

| Type | Extra fields | Command (all take `--run-id ID`; optional `--log PATH` or `--project DIR`) |
|---|---|---|
| `run_started` | `goal`, `size` | `python SCRIPT event run_started --run-id 2026-10-23-login --goal "Add an email login page" --size project` |
| `handoff` | `from`, `to`, `task` | `python SCRIPT event handoff --run-id ID --from orchestrator --to architect --task "Plan the login page"` |
| `agent_result` | `status`, `summary`, `response_file` | `python SCRIPT event agent_result --run-id ID --agent architect --status needs_answers --summary "Needs the sign-in method" --response-file .team/runs/ID/01-architect-response.json` |
| `question_asked` | `id`, `questions` | `python SCRIPT event question_asked --run-id ID --agent architect --id q-01 --questions-json '[{"id":"q1","question":"Email and password, or a link?","why":"Changes the design"}]'` |
| `approval_requested` | `id`, `kind`, `title`, `why`, `options`, `one_way_door`, `asked_agent` | `python SCRIPT event approval_requested --run-id ID --id a1 --kind decision --title "Where to store accounts" --why "Hard to move later" --options-json '[{"id":"o1","label":"sqlite","recommended":true},{"id":"o2","label":"postgres"}]' --one-way-door true --asked-agent architect` |
| `approval_given` | `id`, `decision`, `option`, `answers`, `by` | `python SCRIPT event approval_given --run-id ID --id a1 --decision approved --option o1 --by terminal` |
| `blocked` | `reason` | `python SCRIPT event blocked --run-id ID --agent architect --reason "Tests cannot run: Python missing"` |
| `blocker_cleared` | none | `python SCRIPT event blocker_cleared --run-id ID --agent architect` |
| `run_finished` | `status` (`done`, `stopped`, `failed`), `summary` | `python SCRIPT event run_finished --run-id ID --status done --summary "Login page planned, built and reviewed"` |

- Every line has `ts`, `type`, `agent`, `run_id`. `run_id` is the run folder name, the same on every line of the run.
- `run_started` also writes `.agents/current_run` (the run id) and `run_finished` removes it, so the hook logs the same `run_id` and adds the Claude session id as an optional `session_id` field.
- `agent` defaults to `orchestrator` for `run_started`, `run_finished`, `handoff`, `approval_*`; pass `--agent <specialist>` for `agent_result`, `question_asked`, `blocked`, `blocker_cleared`.
- `ts` is set by the script from the real clock; never pass or invent one. Answers to questions use `--decision answered` and `--answers-json`.
- If the script refuses, fix the command and run it again; do not write the line another way.
- Never log a secret.

## Checking a run
`python SCRIPT check-run .team/runs/<run>` (optional `--log PATH`) checks the folder: plan and summary exist, every request and response is valid, the log starts with `run_started`, has a handoff pair and an `agent_result` per response, ends with `run_finished` when closed, and lists approvals still `pending`. It prints OK or PROBLEMS (one per line) and exits 0 or 1. Run it before the closing summary and fix every problem.

## Resuming
1. Read `plan.md`, then `decisions.md`, then the last response files.
2. Tell the owner in plain words what is done and what is next.
3. Continue at the first unfinished step with the recorded answers in its request. Never repeat finished steps or re-ask answered questions.
4. If the folder is missing or inconsistent, say so and rebuild the plan from what exists, asking the owner only what cannot be found.
