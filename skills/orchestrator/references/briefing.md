# Briefing a specialist

A specialist knows only what you put in the request. It never sees the owner or the earlier conversation.

## The request file
Save as `.team/runs/<run>/NN-<role>-request.json`:

```json
{
  "goal": "one or two sentences: what the owner needs from this specialist",
  "context_files": ["paths the specialist should read first"],
  "constraints": ["limits: budget, platform, deadline, things not to touch"],
  "done_when": ["checkable conditions that mean this step is finished"],
  "mode": "the specialist's mode if it has one (for example design or recover)",
  "answers": [{"id": "q1", "answer": "the owner's answer to an earlier question"}]
}
```
`goal`, `context_files`, `constraints` and `done_when` are required (lists may be empty except `done_when`); `mode` and `answers` are optional. If the project has `scripts/agent_contract.py`, run `check-request` on the file.

## What good context looks like
- Paths, not pasted text. Name the files, folders, commit range or branch.
- The owner's words for the goal, plus your plain restatement, so nothing is lost.
- Earlier decisions and approvals that bind this step, with where they are recorded.
- What the specialist owns and what it must not touch (see `team-roster.md`).
- A `done_when` the specialist and you can both check, for example "an ADR exists for the database choice" rather than "design it well".

## The call
- Call the specialist by name with the Agent tool and the model the roster gives. The prompt is one short line plus the request file path and the reply rule: answer as one JSON object with the 7 fields.
- Resume the same specialist (same agent) for follow-ups with `answers`, instead of starting over.
- Name the owner's language in `constraints` (for example `Write the summary and any document for the owner in Roman Urdu`); the language of the owner's latest message wins. Code and identifiers stay in the project's own language.
- Never include secrets in a request or in the call.

## Do not
- Brief two specialists to write the same file.
- Ask a specialist to do what the harness refused you.
- Forward the owner's message unchanged: restate it and add what the specialist needs.
