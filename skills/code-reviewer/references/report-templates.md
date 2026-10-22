# Report templates

When to read this: when you write the review file and the handoff response. Keep the report short enough to read in five minutes and precise enough for an engineer to fix from.

## 1. The review file

Path: `docs/reviews/YYYY-MM-DD-<topic>.md` in the reviewed project (create the folder if needed; never overwrite an earlier review: a same-day, same-topic name gets a numeric suffix, `-2`, `-3`). The file lands in the working tree and may be committed with the change; say so. If the project folder is not writable or the boss said not to write files, put the same content in the reply and say no file was written.

```
# Review: <topic>

Range reviewed: <branch or commit range>     Requirement: <path or "none given; intent inferred from the commit message, listed in assumptions">
Date: YYYY-MM-DD     Size: N files, +A / -D lines     Read in full: <list>     Sampled or skipped: <list and why>

## Verdict
Approved | Needs fixes | Blocked | Needs approval      (one line, then two or three plain sentences)

## Spec compliance
- Met: ...
- Missing: ...
- Extra (not requested): ...
- Cannot verify from the change: ...

## Findings
### Critical
1. <short title>   [confidence: confirmed | likely | needs-check]
   - Where: file:line
   - What goes wrong: ... (the input or sequence that triggers it)
   - Why it matters: ...
   - Smallest fix: ... (in words; who should do it)

### Important
...
### Minor
...

## Strengths
- <specific, brief>

## What I ran
- `<command>`: <result in one line>      (or: "Nothing was run; tests were not available" )

## Not covered
- <what you did not read or could not check>
```

Rules:
- One finding per heading; order by severity, then by risk within it.
- Every finding has `Where` with a file and line (or the closest you can name), a trigger, and a smallest fix.
- If a section is empty, write "none" so the reader knows you looked.
- "What I ran" lists real commands with their real results. If a command failed, say so.
- Keep strengths to two or three lines.

## 2. The handoff response (when you run under a boss)

All seven fields every time, as one JSON object:

```json
{
  "status": "done | needs_answers | needs_approval | blocked",
  "summary": "verdict first, then the top findings in plain words",
  "files": ["docs/reviews/2026-10-23-order-search.md"],
  "questions": [{"id": "q1", "question": "...", "why": "..."}],
  "approvals": [{"id": "a1", "decision": "...", "options": ["..."], "recommended": "...", "one_way_door": true}],
  "assumptions": ["intent inferred from the commit message", "..."],
  "evidence": ["git diff main...review/x read: 3 files, +41 lines", "python -m unittest: 3 tests, 1 failure (test_discount_at_ten)", "findings: 2 Critical, 1 Important, 0 Minor"]
}
```

How to fill it:
- `status`: `done` when the review is finished (even if the verdict is "needs fixes": the review is done); `needs_answers` when you need the range, the requirement or another fact; `needs_approval` when a hard-to-undo concern needs the owner; `blocked` when you cannot get the change.
- `summary`: plain language for a non-engineer. First sentence is the verdict. Then at most three bullets of the top findings, then what must be decided. No jargon without a one-line explanation.
- `files`: the review file, nothing else (you change no code).
- Questions and `needs-check` items go under `questions`; they never count toward the verdict. A migration that breaks running code plus an intentional data drop: verdict needs fixes, `status` `needs_approval`.
- `approvals`: only for hard-to-undo concerns. Put your recommendation first in `recommended` and keep every option's cost in the option text.
- `assumptions`: everything you assumed instead of asking.
- `evidence`: something the boss can check without trusting you: the range and files you read, commands and their results, counts of findings by severity. "I reviewed it carefully" is not evidence. A `done` response must have evidence.

## 3. Alone, in a normal conversation

Write the same content in plain language in the reply: the verdict, the top findings with file references, what you did not cover, and the smallest next steps (and which engineer role should do them). Offer to save it as a review file. Do not offer to change the code yourself.

## 4. Short forms

- Clean change: "Approved. Nothing important left. I read <files> and ran <command> (<result>). One minor note: ..." plus the file or the handoff JSON.
- Cosmetic change: "Approved. Formatting and a rename only; I compared the logic line by line and the behaviour is unchanged."
- Cannot review: "Blocked. I could not find <range>. Branches that exist: <list>. Which one do you mean?"

## Sources
[S-REV-1] [S-REV-5]
