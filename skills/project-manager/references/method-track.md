# Track mode

## 1. When to read this
"Where do we stand?", "why does the tracker say 5 and the document 4?", "what changed since yesterday?", "what should the team do next?".

## 2. Drift check (read only)
The script `drift_check.py` is not built: do the check by hand with Read, Grep and Glob, and say "checked by hand, script not built" in the evidence.

Compare these sources, item by item (one item per role or task):
1. `TASKS.md`: the roles table, Documentation and Build columns.
2. Each role document's status line (the "Status:" line or first paragraph): built, tested, "k of n modes".
3. The tracker numbers: the local copy `docs/agents/task-tracker/index.html` (the live tracker only when the owner asks; that tool is not built).
4. The files on disk: `agents/<name>.md` exists; a row in `docs/agents/roster.md`; the name in the boss's `Agent(...)` list (owner decision X4: a role the boss cannot call is not built); `evals/<skill>/` and a results file with "k of n"; a spec in `docs/superpowers/specs/`; "Superseded by" lines on replaced documents (owner decision Q37); the `PROJECT_STATE.md` "Last updated" date against the newest change.

Output one row per mismatch: item, what each source says, what the files support, the proposed fix (file, line, new text), the owner of the file. The files win over every record; when the files cannot settle it, the row says `unknown`. A status line that cannot be read is a mismatch ("cannot parse"), never skipped. Never pick the majority of the records.

## 3. Change check (read only)
The script `change_check.py` is not built. Until it is:
- In a git repository: `git log --name-status --since=<time of the last status>` and `git status` (read only).
- Without git: compare an `ls -lR` listing (size and date) of `docs/`, `agents/`, `skills/`, `evals/`, `TASKS.md`, `PROJECT_STATE.md`, `CHANGELOG.md` and `.team/runs/` with the listing saved in `docs/project/snapshot.json`. SHA-256 fingerprints come with the script (not built). With no snapshot yet, say "first status; no change check possible".

Output: added, changed and removed files grouped by the role that owns the folder. Flag a change no recorded run explains ("changed outside a recorded run"; name the file and the folder owner, not the session). Flag a new decision that replaces an older one and the documents that still describe the old one. Do not flag every change.

## 4. Status
1. Mark a task done only with proof (rule 4 of `SKILL.md`).
2. Write `docs/project/status.md` from the template, rebuilt from evidence, never edited by hand: the owner's open decisions first, with how long each has waited; then mismatches with their fixes and owners; changes; done; blocked; top risks; what is next.
3. **What is next:** decisions that unblock the most work first; then the jobs that can start now, in dependency order, with the reason, and the Product & Business Analyst's value order beside it when they differ. The boss picks the job; this role starts nothing and calls no one.
4. A stale `PROJECT_STATE.md` is reported with its date against the newest run; the status is built from the run records.
5. Write the new `docs/project/snapshot.json` last, only after the status is written, so a failed run does not hide changes.

## 5. Done when
The drift check and the change check ran in this session (commands and output, or "checked by hand, script not built", in `evidence`); `docs/project/status.md` lists every mismatch with its fix and owner, the owner's open decisions first, and the time of the check; the snapshot was written after the status.
