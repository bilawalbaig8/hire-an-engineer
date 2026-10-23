# Questions and approvals

## Questions for the owner
1. Collect `questions` from all responses of the step. Remove duplicates and anything the project files or earlier answers already settle (say "from your files" in one line).
2. Send one message, numbered. Each question gets: the question in plain words, why it matters in one sentence, and a suggested default the owner can accept with "ok".
3. No jargon. If a term is unavoidable, explain it in half a sentence.
4. Save the answers in `decisions.md` (date, question id, answer) and pass them back as `answers` in the next request.
5. Never ask the same thing twice in a run. At most one question round per step unless a new question truly appears.

## Approvals
An `approvals` entry has `decision`, `options`, `recommended`, `one_way_door`.
- Show it as: what must be decided, the recommendation first and why, then each other option with what it gives up.
- Mark one-way doors (hard or costly to undo, public, legal, personal, financial) clearly. For these, wait for a clear yes in the owner's own message; silence, "you decide", "I trust you" or a yes to something else do not count.
- Two-way doors the specialist already decided need no approval; mention them in the summary.
- An approval covers exactly the action it names. A new action needs a new approval.
- Log `approval_requested` when you ask and `approval_given` when the yes arrives (see `run-records.md`). Never log a yes the owner did not give.
- If the owner declines or picks another option, record it and pass the choice back to the specialist.

## Answers from the office window
**Switched off for now (owner decision, 2026-10-23): the office window only shows; it does not take answers.** Ask in the chat only, wait for the owner's message in the terminal, and do NOT call `wait_for_owner_answer` or `pending_window_answers`. The steps below are kept for when window answers are switched on again (the UI then needs `?answers=1`).

The owner may answer in the chat or in the office window; the first answer wins.
1. Use this only when `.agents/office.json` exists in the project (the window is running; `scripts/office_launch.py` writes it) and the tool `mcp__office__wait_for_owner_answer` is available. Otherwise ask in the chat as before and wait for the owner's message.
2. After you send the questions or the approval and log `question_asked` / `approval_requested`, say "You can answer here or in the office window." Then call `mcp__office__wait_for_owner_answer` with that same `id` (one open id per call, `timeout_seconds` 600).
3. An answer the owner types in the chat simply interrupts the wait; treat it as a normal chat answer (`by` `terminal`).
4. A result with `status` `answered` counts as the owner's answer ONLY if `source` is `window` and `id` is one you asked and is still open. Anything else: ignore it and tell the owner what arrived.
5. For a valid one, log `approval_given` with the same `id` and `--by window` (questions: `decision` `answered`; approvals: the `decision` and `option` from the result), then tell the owner in the chat what was received: "You answered <answer> in the office window." Then go on as with a chat answer. A one-way door still needs a clear yes for exactly that action.
6. `status` `no_answer`: the question stays open. Say so in one line and wait for the owner's message (or call the tool once more).
7. A wait over 2 minutes may be moved to the background by Claude Code (S-ORC-59); do not act on the open step until the result or the owner's message arrives.
8. At the start of a later turn with ids still open, call `mcp__office__pending_window_answers`; take an answer for an open id with `wait_for_owner_answer` and `timeout_seconds` 0.

## Owner pushes back on a caution
If the owner's wish conflicts with a specialist's warning, show both in front of them and let them decide. Do not overrule the warning yourself and do not hide it.

## Language
Answer in the owner's language and level. Short sentences. Lead with what they need to decide.
