# Run method

The eight steps of every run. Every event line below is written with `scripts/team_event.py` of this skill (commands in `run-records.md`), never by hand. Skip steps a tiny or small job does not need, but never skip step 6 or 7 when they apply.

## 1. Intake
- Restate the job in one or two plain sentences and the owner's definition of done.
- Look at the project first (its `AGENTS.md`, `PROJECT_STATE.md`, existing `docs/`) so you do not ask what the files already say.
- If something that changes the plan is unclear, ask at most 5 questions in one message. These are your own questions, before any specialist is called. If a reasonable default exists, state it and go on.

## 2. Size and plan
- Tiny: answer directly. No run folder. Small: one or two specialists. Project: a chain.
- **Who does the work is the owner's choice.** If the owner said how ("team se karo", "sirf architect", "akele tum jawab do"), do exactly that. If not, after the intake say in one or two plain lines what you will do and why: which specialists and in which order, or that you will answer yourself because the job is small; the owner can change it in their next message. If a big job is unclear on this, ask once with your suggestion. Never start a long chain of specialist calls without having said the plan first.
- Choose the specialists from `team-roster.md`. If a needed role is not installed, say which and proceed with the rest. Give the `architect` its mode (system design or data design); a database job follows the order in `team-roster.md`.
- For a project write `plan.md` in the run folder: the steps, who does each, order, what can run in parallel, which steps need the owner. Show the owner a plain-words version before spending calls.
- Say the team size qualitatively (one, a few, several specialists) and call it an estimate. No cost nagging otherwise.

## 3. Brief and dispatch
- Before the first call of any run, create the run folder (see `run-records.md`), even for a small job, and append `run_started` (`goal`, `size`) as the first event line.
- Write one request file per step (see `briefing.md`) and call the specialist by name through the Agent tool with the model from the roster. Pass the file path, not pasted content.
- Parallel steps only when they touch different folders. Otherwise run one after the other.
- Append a `handoff` event (boss to specialist, with a short `task`) to the event log.

- At the start of a run, if `.agents/office.json` exists, tell the owner the office window address (`http://127.0.0.1:<port>/`, port from that file) in your first message, once per run.

## 4. Collect
- Save the response as `NN-<role>-response.json`. Check the 7 fields (`status`, `summary`, `files`, `questions`, `approvals`, `assumptions`, `evidence`). If the project has `scripts/agent_contract.py`, run `check-response`; otherwise check by reading.
- A `done` with no evidence, or a response missing fields, goes back once with the exact complaint (that is the one retry).
- Append the return `handoff` event, then `agent_result` (`agent` = the specialist, its `status`, a short `summary`, `response_file` = the saved response path).
- If something outside the specialist stops the work (missing tool, failed check, owner unreachable), append `blocked` (`reason`); when it is resolved without re-calling that specialist, append `blocker_cleared`.

- **Show pending decisions at once:** the moment a response has `needs_answers` or `needs_approval`, append `question_asked` / `approval_requested` for it (so the office Inbox shows it), even if you keep running other independent steps (for example a code review) before you ask the owner in the chat. Approvals always go to the owner, never to a reviewer: a reviewer's verdict is a quality verdict, not permission.

## 5. Relay
- Merge the `questions` of the step, drop duplicates, answer from files or earlier answers when possible. The rest go to the owner in one message (see `questions-and-approvals.md`).
- When you send the questions to the owner, append `question_asked` (`id` such as `q-01`, `agent` = the asker, `questions`). When the answers arrive, append `approval_given` with the same `id`, `decision` `answered`, `by` `terminal`.
- If the office window is running (`.agents/office.json` exists) and `mcp__office__wait_for_owner_answer` is available, call it with that `id` after asking; a chat answer interrupts it. A window answer is logged with `by` `window` (rules in `questions-and-approvals.md`, "Answers from the office window"). Same for approvals in step 6.
- Save the answers in `decisions.md` and pass them back in a new request file (`answers`), resuming the same specialist when possible.

## 6. Decide or approve
- Decisions the specialists made that are two-way doors stay made.
- Every `approvals` entry goes to the owner. Nothing is applied before a clear yes in the owner's own message. Append `approval_requested` when asked (`id`, `kind` `decision`, `title`, `options`, `one_way_door`, `asked_agent`) and `approval_given` with the same `id` (`decision` `approved` or `rejected`, `option`, `by` `terminal`, or `window` for an office window answer) when the answer arrives.
- If two specialists disagree, give the owner both positions with a recommendation (see `quality-gates.md`).

## 7. Gate
- Anything that changes code or files passes the Reviewer first (see `quality-gates.md`). Findings go back to the producing specialist as a new request. After 2 fix rounds, report the open findings instead of looping.

## 8. Close
- Run `team_event.py check-run` on the run folder and fix every problem it lists (missing handoff or `agent_result` events, a bad response file) before the summary. Approvals it lists as pending must still be open on purpose.
- Write `summary.md` and give the owner the same in plain words: what was done, what they must decide or do, where the files are, what was not covered or not verified. Keep it short.
- Mention anything refused, blocked, or capped.
- If any question or approval is still open, do NOT append `run_finished`: the run stays open and the office shows 'Waiting for you'. Say plainly that nothing has been approved or applied. Close the run later, after the answers.
- Last, append `run_finished` (`status` `done`, `stopped` or `failed`, short `summary`). A run without it is open.

## Small helpers you may do yourself
Listing files, copying a path into a request, formatting a summary. Never design, review or write product logic.
