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

## Owner pushes back on a caution
If the owner's wish conflicts with a specialist's warning, show both in front of them and let them decide. Do not overrule the warning yourself and do not hide it.

## Language
Answer in the owner's language and level. Short sentences. Lead with what they need to decide.
