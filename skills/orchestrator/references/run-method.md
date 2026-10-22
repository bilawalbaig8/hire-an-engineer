# Run method

The eight steps of every run. Skip steps a tiny or small job does not need, but never skip step 6 or 7 when they apply.

## 1. Intake
- Restate the job in one or two plain sentences and the owner's definition of done.
- Look at the project first (its `AGENTS.md`, `PROJECT_STATE.md`, existing `docs/`) so you do not ask what the files already say.
- If something that changes the plan is unclear, ask at most 5 questions in one message. These are your own questions, before any specialist is called. If a reasonable default exists, state it and go on.

## 2. Size and plan
- Tiny: answer directly. No run folder. Small: one or two specialists. Project: a chain.
- Choose the specialists from `team-roster.md`. If a needed role is not installed, say which and proceed with the rest.
- For a project write `plan.md` in the run folder: the steps, who does each, order, what can run in parallel, which steps need the owner. Show the owner a plain-words version before spending calls.
- Say the team size qualitatively (one, a few, several specialists) and call it an estimate. No cost nagging otherwise.

## 3. Brief and dispatch
- Write one request file per step (see `briefing.md`) and call the specialist by name through the Agent tool with the model from the roster. Pass the file path, not pasted content.
- Parallel steps only when they touch different folders. Otherwise run one after the other.
- Append a `handoff` event (boss to specialist) to the event log.

## 4. Collect
- Save the response as `NN-<role>-response.json`. Check the 7 fields (`status`, `summary`, `files`, `questions`, `approvals`, `assumptions`, `evidence`). If the project has `scripts/agent_contract.py`, run `check-response`; otherwise check by reading.
- A `done` with no evidence, or a response missing fields, goes back once with the exact complaint (that is the one retry).
- Append the return `handoff` event.

## 5. Relay
- Merge the `questions` of the step, drop duplicates, answer from files or earlier answers when possible. The rest go to the owner in one message (see `questions-and-approvals.md`).
- Save the answers in `decisions.md` and pass them back in a new request file (`answers`), resuming the same specialist when possible.

## 6. Decide or approve
- Decisions the specialists made that are two-way doors stay made.
- Every `approvals` entry goes to the owner. Nothing is applied before a clear yes in the owner's own message. Record `approval_requested` when asked and `approval_given` when the yes arrives.
- If two specialists disagree, give the owner both positions with a recommendation (see `quality-gates.md`).

## 7. Gate
- Anything that changes code or files passes the Reviewer first (see `quality-gates.md`). Findings go back to the producing specialist as a new request. After 2 fix rounds, report the open findings instead of looping.

## 8. Close
- Write `summary.md` and give the owner the same in plain words: what was done, what they must decide or do, where the files are, what was not covered or not verified. Keep it short.
- Mention anything refused, blocked, or capped.

## Small helpers you may do yourself
Listing files, copying a path into a request, formatting a summary. Never design, review or write product logic.
