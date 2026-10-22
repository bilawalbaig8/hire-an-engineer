# Handoff contract: boss and specialist

This is how the boss agent and a specialist agent talk. Both sides use plain JSON.
Anything that breaks this contract is rejected by `python scripts/agent_contract.py`.

## Who talks to the owner

Only the boss. A specialist never asks the owner anything directly. If a specialist
needs an answer or a decision, it puts it in its response and the boss relays it in
plain language, then sends the answer back in the next request.

## The request (boss to specialist)

| Field | Required | Meaning |
|---|---|---|
| `goal` | yes | One or two sentences: what to achieve. |
| `context_files` | yes | Files to read first (can be an empty list). |
| `constraints` | yes | Rules to respect, e.g. "no new dependencies" (can be empty). |
| `done_when` | yes | At least one check that proves the work is finished. |
| `mode` | no | A word the specialist understands, e.g. `plan` or `build`. |
| `answers` | no | Owner answers to earlier questions: `{ "id", "answer" }`. |

Example:

```json
{
  "goal": "Add an email login page to the app.",
  "context_files": ["README.md", "src/app.py"],
  "constraints": ["No new dependencies", "Keep the page plain and simple"],
  "done_when": ["Login test passes", "Page is documented in README.md"],
  "mode": "build"
}
```

## The response (specialist to boss)

| Field | Meaning |
|---|---|
| `status` | `done`, `needs_answers`, `needs_approval` or `blocked`. |
| `summary` | What happened, in plain language. |
| `files` | Files created or changed. |
| `questions` | Used with `needs_answers`: `{ "id", "question", "why" }`. |
| `approvals` | Used with `needs_approval`: `{ "id", "decision", "options", "recommended", "one_way_door" }`. |
| `assumptions` | Things the specialist assumed instead of asking. |
| `evidence` | Proof the work is real. Required (at least one) when `status` is `done`. |

All seven fields must be present; use an empty list when there is nothing to say.

### Questions and approvals

- **Question** (`needs_answers`): the specialist cannot continue without information.
  `why` explains in one line why the answer matters. The boss asks the owner, then
  sends the answers back in `answers` in a new request.
- **Approval** (`needs_approval`): a decision the owner must make, with the options and
  the specialist's `recommended` choice. Set `one_way_door` to `true` when the choice
  is hard or expensive to undo (data formats, deleting things, publishing). The boss
  always asks the owner for these, and never decides them alone.
- **Blocked** (`blocked`): something outside the specialist's control stops the work.
  Say what in `summary`.

### What counts as evidence

Something the boss (or the owner) can check without trusting the specialist's word:
a test command with its result ("pytest: 9 passed"), a command output, a file path
that now exists, or a link. "I checked and it works" is not evidence.

Example, a response asking questions:

```json
{
  "status": "needs_answers",
  "summary": "I can build the login page once I know which sign-in method to use.",
  "files": [],
  "questions": [
    {
      "id": "q1",
      "question": "Should people sign in with email and password, or with a one-time email link?",
      "why": "It changes the design and what we store about each person."
    }
  ],
  "approvals": [],
  "assumptions": [],
  "evidence": []
}
```

Example, a response asking for approval:

```json
{
  "status": "needs_approval",
  "summary": "The login page needs somewhere to keep accounts. I need a decision before I build it.",
  "files": ["docs/plan.md"],
  "questions": [],
  "approvals": [
    {
      "id": "a1",
      "decision": "Where to store user accounts",
      "options": ["A local file database (sqlite)", "A hosted database (postgres)"],
      "recommended": "A local file database (sqlite)",
      "one_way_door": true
    }
  ],
  "assumptions": ["Fewer than 1000 users"],
  "evidence": ["docs/plan.md compares both options"]
}
```

## The event log

Events are appended to `.agents/events.jsonl` (one JSON object per line, never edited
afterwards). This is the trail the owner can read to see what happened. Who writes what:

- The hook (`scripts/log_event.py`, see "Event sources") writes `agent_start`, `agent_stop`
  and `file_written`.
- The boss writes `handoff`, `approval_requested` and `approval_given`, using
  `append_event` from `scripts/agent_contract.py` (it checks the line before writing).
- A specialist writes nothing to the log.

| Field | Meaning |
|---|---|
| `ts` | Time in UTC, ISO 8601, e.g. `2026-10-22T10:00:00Z`. |
| `type` | `agent_start`, `agent_stop`, `handoff`, `file_written`, `approval_requested`, `approval_given`. |
| `agent` | Name of the agent writing the line. |
| `run_id` | One id shared by everything in the same job. |
| `path` | Only for `file_written`: the file. |
| `from`, `to` | Only for `handoff`: who passes work to whom. |

Example lines (save one per file to check them with the CLI):

```json
{"ts": "2026-10-22T10:00:00Z", "type": "handoff", "agent": "boss", "run_id": "run-1", "from": "boss", "to": "architect"}
```

```json
{"ts": "2026-10-22T10:05:00Z", "type": "file_written", "agent": "architect", "run_id": "run-1", "path": "docs/plan.md"}
```

## Checking a file

```
python scripts/agent_contract.py check-request request.json
python scripts/agent_contract.py check-response response.json
python scripts/agent_contract.py check-event event.json
```

Exit code 0 means valid. Exit code 1 prints what is wrong.

## Event sources

The event log (`.agents/events.jsonl`) is filled by a Claude Code hook that runs `scripts/log_event.py`.
Field names below were read from the official hooks reference, https://code.claude.com/docs/en/hooks (checked 2026-10-22). The hook sends one JSON object on stdin.

Common fields, all events: `session_id`, `transcript_path`, `cwd`, `hook_event_name`. Inside a subagent also `agent_id` and `agent_type`. The environment variable `CLAUDE_PROJECT_DIR` is the project root.

| Hook event | Extra fields used | Becomes event |
|---|---|---|
| `SubagentStart` | `agent_id`, `agent_type` | `agent_start`, `agent` = `agent_type` |
| `SubagentStop` | `agent_id`, `agent_type`, `agent_transcript_path`, `last_assistant_message`, `stop_hook_active` | `agent_stop`, `agent` = `agent_type` |
| `PostToolUse` with `tool_name` `Write` or `Edit` | `tool_input.file_path` (absolute path), `tool_response`; Write also `tool_input.content`, Edit also `old_string`, `new_string`, `replace_all` | `file_written`, `path` = file path relative to the project |

`run_id` is the hook's `session_id`. For `file_written`, `agent` is `agent_type` when present, otherwise `main`.
Everything else is ignored. Not confirmed in the docs: any field beyond those listed; the script uses none.
