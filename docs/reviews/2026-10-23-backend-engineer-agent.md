# Review: Backend Engineer agent (agent file, thin skill, roster row)

Range reviewed: uncommitted working tree against HEAD (`git status` / `git diff`; no commit yet)     Requirement: `docs/agents/roles/backend-engineer.md`, plus the build brief `.team/runs/2026-10-23-backend-engineer-agent/01-architect-request.json`
Date: 2026-10-23     Size: 4 new files (`agents/backend-engineer.md` 91 lines, `skills/backend-engineer/SKILL.md` 46, `references/method.md` 46, `references/checklists.md` 42) and 3 changed files (+3 / -1 lines)
Read in full: all 7 changed files, the role file, `handoff-contract.md`, `agent-template/README.md`, `agents/data-scientist.md`, `agents/code-reviewer.md` (handoff section), both run files 01-request and 01-response, `scripts/sync_team_start.py`
Sampled or skipped: `skills/hire-an-engineer/references/integrations.md` (headings only, to check that the routed files and sections exist); the validator scripts' source was not read, only their output

## Verdict
Needs fixes (one Important finding, five Minor).

The build matches the role file closely. Every item on the role file's "will not do" list is in the agent file, nothing is cited without a source list, the tools match what the file says it does, and the model matches the roster. The one Important problem: the "Model and why" section explains the choice of `sonnet` with a safety step that the rest of the agent never carries out. Auth design and data formats are said to go back as approvals, but no operating rule sends them back.

## Spec compliance
- Met:
  - Role, owned folders (`docs/backend/`, `migrations/`, the server folders the brief names, "writes nowhere else"), the two modes with one question when the mode is unclear, the 9-step method, the done / needs_answers / needs_approval / blocked definitions, and the `verified` / `inferred` / `unknown` claim labels all match the role file, sections 2 to 9.
  - Every item on the "will not do" list (role file section 4) is in the agent's Never list, `agents/backend-engineer.md:79-87`: no system design or stack choice alone, no screens, AI or analysis work, no cloud accounts, plans, domains or going live, no real secrets, live keys or customer data, no live migrations, permanent deletes, real messages or moving money, no legal certificates, no unmeasured claims, no direct calls to other specialists.
  - Brief check (2): every one of these is also an approval trigger (`agents/backend-engineer.md:52`, `method.md:46`), with money, live data, messages and deploys marked one-way doors. Questions go only to the boss (`:79`).
  - Brief check (3): the frontmatter tools (Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch) match the Tools section one to one, each with its limits (`:31-34`). This is the same set the data-scientist agent has.
  - Brief check (4): `model: sonnet` (`:4`) matches the roster row in `docs/agents/roster.md:13` and the synced copy; `check_roster.py` agrees.
  - Brief check (5): the handoff block has all 7 fields with the contract's names and shapes (`:59-69`). The status rules agree with `handoff-contract.md:37-47`.
  - Brief check (6): no source IDs anywhere in the agent or the skill (grep for `S-` and `sources.md` returned nothing). `SKILL.md:43` says plainly not to cite sources until a list exists.
  - The deferred items (sources.md, evals, CHANGELOG, THIRD_PARTY_NOTICES, install, commit) are absent, as the owner asked, and the architect's response says so.
- Missing (small, see Minor 3): role file section 7, "the Code Reviewer reads its changes before they count as done"; role file section 6, the AI Engineer's design and the Data Scientist's metric definitions as inputs; role file section 3, a README that "runs in 15 minutes"; the "no legal or privacy certificates" rule in `SKILL.md`, which matters when the skill is used without the agent file.
- Extra (not in the role file; none of it contradicts the role file):
  - The "Model and why" claim about approvals (see Important 1).
  - "Overwrite, renumber or reformat existing project records" in Never (`:90`). This is a sensible guard.
  - "Choosing a provider the owner will be tied to" as an approval trigger (`method.md:23,46`). This fits "You decide. It recommends."
  - "Rate limits on login and costly routes" (`checklists.md:24`). The role file only mentions the rate limits of outside services.
  - "not 1,000 times" (`method.md:9`), the only number added.
- Cannot verify from the change: how the agent behaves on real prompts. There are no evals in this run (the owner deferred them).

## Findings
### Critical
none

### Important
1. The reason given for `sonnet` relies on an approval step that no rule creates   [confidence: likely]
   - Where: `agents/backend-engineer.md:27`, compared with `agents/backend-engineer.md:52` (How it works, step 9) and `skills/backend-engineer/references/method.md:46` (Stop for approval).
   - What goes wrong: line 27 says hard-to-undo work ("data formats, a live migration, money flows, auth design") "is never finalised by this agent alone: it goes back as an approval". But the approval list in step 9 and in method section 6 only covers live actions (live key, real data, live migration, paid plan, real message, deploy, provider choice). Trigger: a brief such as "add login so users see only their own orders, and take payments with Stripe test keys". Following its own steps, the agent designs the auth model, the permission rules, the payment idempotency and a new table format, runs the tests, and returns `done`. No approval is raised and no `opus` check happens.
   - Why it matters: the model choice rests on this safeguard. The owner's global model table puts "risky code (data formats, concurrency, security, anything hard to undo)" on `opus`, and the Backend Engineer's core work is exactly that kind of code. The role file's real safeguard is section 7, "the Code Reviewer reads its changes before they count as done", and the agent never states it. A boss reading line 27 would believe a check exists that does not.
   - Smallest fix (agent-file author, the role that built it): choose one of these.
     - (a) Rewrite line 27 to say what is true: the boss sends every change to the Code Reviewer (`opus`) before it counts as done (role file section 7). Add "Code Reviewer review pending" to what `done` reports.
     - (b) Keep the sentence and make it true: add "a new or changed auth or permission model, a saved-data or API format other code depends on, a money flow" to the approval list in step 9 and in `method.md` section 6.
     Whether `sonnet` stays is the owner's call (see question q1).

### Minor
1. The rule "always end with the JSON block" is missing   [confidence: likely]
   - Where: `agents/backend-engineer.md:71` (Handoff), compared with `agents/data-scientist.md:67` and `agents/code-reviewer.md:65`.
   - What goes wrong: when the boss passes a plain-words request ("bas ek simple login bana do"), nothing tells the agent to still close with the 7-field JSON, or to write its own files without asking first. The brief named data-scientist.md as the pattern, and that file has both sentences. Running on `sonnet`, the agent is more likely to answer in prose only, and `agent_contract.py` would then reject the reply. This is not confirmed, because there are no evals.
   - Smallest fix: copy the data-scientist sentence, adapted to `docs/backend/`, `migrations/` and the named folders.
2. The base-skill paths in the router only work inside this repo   [confidence: likely]
   - Where: `skills/backend-engineer/SKILL.md:40-41`.
   - What goes wrong: the router points to `skills/hire-an-engineer/references/...`. In any other project, and once the skill is installed, that path does not exist. The files are at `~/.claude/skills/hire-an-engineer/references/` (checked: all 7 files are present there). The agent file names this same problem for `handoff-contract.md` (`:57`), but the skill does not.
   - Smallest fix: name both locations ("in this repo `skills/hire-an-engineer/...`; once installed `~/.claude/skills/hire-an-engineer/...`"), or name the skill and the file only.
3. Small items from the role file that were dropped   [confidence: confirmed]
   - Where: `agents/backend-engineer.md:36-40` (Reads first), `:71` (done), `skills/backend-engineer/SKILL.md:20-33`.
   - What goes wrong: four small items are missing.
     - Role file section 6: the inputs from the AI Engineer and the Data Scientist are not in Reads first.
     - Role file section 3: the "15 minutes" README target is reduced to "runs the project".
     - Role file section 7: Code Reviewer review before done is missing (see Important 1).
     - Role file section 4: "no legal or privacy certificates" is missing from `SKILL.md`, so a direct skill user (no agent file) does not get it.
   - Smallest fix: one line each, in Reads first, the done sentence and a SKILL rule.
4. The migrations folder is fixed at `migrations/`, which clashes with projects that keep migrations elsewhere   [confidence: needs-check, so it goes under questions and does not count toward the verdict]
   - Where: `agents/backend-engineer.md:14,33`, `method.md:43`. The role file has the same wording in section 7.
   - Trigger: a project with Alembic (`alembic/versions/`) or Prisma (`prisma/migrations/`). "Continue the existing series" and "write only in `migrations/`" cannot both be followed, unless the brief happens to name that folder. The build follows the role file faithfully here, so this is a question for the owner (q2), not a defect of this build.
5. The role file still says "not built yet"   [confidence: confirmed]
   - Where: `docs/agents/roles/backend-engineer.md:3`.
   - What goes wrong: once this is committed, the role page tells readers the role does not exist. The architect was not allowed to edit this file.
   - Smallest fix: the boss updates the line in the follow-up commit, together with the CHANGELOG.

## Strengths
- The Never list and the approval triggers cover every one-way action in the role file, and money, live data, messages and deploys are explicitly one-way doors.
- Honest scoping: no invented citations, and an explicit "do not cite sources by ID" line, as the brief asked.
- The runtime roster copy and the hard-coded test list were updated together with the roster row, so the validators and `sync_team_start --check` are green.

## What I ran
- `PYTHONUTF8=1 python scripts/validate_agents.py`: exit 0. All 6 agents pass, including `backend-engineer`.
- `PYTHONUTF8=1 python scripts/validate_skills.py`: exit 0. "backend-engineer: description 1008 chars, SKILL.md 46 lines", "All skills valid."
- `python scripts/check_roster.py`: exit 0, "ok: docs/agents/roster.md".
- `python scripts/sync_team_start.py --check` (read-only mode, source read first): exit 0. The runtime roster copy is in sync.
- `git status --short`, `git diff`, `git diff --stat`: read-only.
- The pytest suite was not run, as the brief instructed. The two roster tests the architect reported as failing were not re-run. Their causes (stale runtime copy, hard-coded name list) are fixed in the diff, and the copy is confirmed in sync by `--check`.

## Not covered
- How the agent behaves on prompts (no evals exist yet).
- The source code of the validator scripts.
- The full text of the base skill's references (only their presence and headings were checked).
- Install parity with `~/.claude` (install was deferred).

## Re-review (fix round 1, 2026-10-23)

Read in full again: `agents/backend-engineer.md` (94 lines), `skills/backend-engineer/SKILL.md` (50), `references/method.md` (50), `references/checklists.md` (44), `docs/agents/roles/backend-engineer.md`, run files 03-request and 03-response. Also read: `agents/architect.md:40-79`, the roster row `docs/agents/roster.md:13`, and grep over `agents/` and `skills/` for the one-way-door lists. The diff was not taken with git this time; the files were read as they are on disk.

### Verdict
Approved. No Critical or Important finding is left. Two new Minor notes, neither blocks.

### Old findings
| Old finding | Status | Evidence |
|---|---|---|
| Important 1 (the `sonnet` reason rested on an approval step that did not exist) | Fixed, both options (a) and (b), as the owner chose in q1 | `agents/backend-engineer.md:27` names both safeguards; `:52` step 9 now lists auth or permission design, data or API formats other code depends on, and money flows; `:71` `done` says "Code Reviewer review pending"; `:89` Never marks its own work as reviewed; `method.md:46` (section 6) and `:48-49` (new section 7); `SKILL.md:31` rule 11; `checklists.md:42-43` |
| Minor 1 (no "always end with the JSON block") | Fixed | `agents/backend-engineer.md:73`, same pattern as `agents/data-scientist.md` |
| Minor 2 (router paths only worked in the repo) | Fixed | `SKILL.md:42-45`; all 7 routed files exist under both `skills/hire-an-engineer/references/` and `~/.claude/skills/hire-an-engineer/references/` (checked with `test -f`) |
| Minor 3 (four dropped role-file items) | Fixed, all four | AI Engineer and Data Scientist inputs `agents/backend-engineer.md:39`; 15-minute README `:71`, `method.md:21`, `checklists.md:10`; Code Reviewer before done (see Important 1); legal certificates `SKILL.md:33` |
| Minor 4 (migrations folder, q2) | Answered as the owner decided in q2 | brief folder, then existing project folder, then `migrations/`: `agents/backend-engineer.md:14,33`, `SKILL.md:32`, `method.md:43` |
| Minor 5 (role file said "not built yet") | Fixed | `docs/agents/roles/backend-engineer.md:3`; the CHANGELOG entry is still deferred to the boss's commit |

### Requested checks
- Approval list across the four files: the three new designs (auth or permission, data or API formats other code depends on, money flows) are in all four places, with the same words: agent `:52` and `:71`, `method.md:46`, `SKILL.md:31`, `checklists.md:42`. The one-way-door set (money, live data, messages, deploys, data formats other code depends on) is the same in agent `:71` and `method.md:46`. One small gap remains, see new Minor 1.
- `done` never claims a review: confirmed in all four files (lines above). No line anywhere says the agent's work is reviewed or approved.
- Frontmatter descriptions: agent 1021 characters, skill 1008 characters (measured with `yaml.safe_load`); both at or under 1024. Agent `model` is still `sonnet`, as the owner chose in q1.
- No source citations: grep for `S-<digit>`, `[S` and `sources.md` in the agent and the skill found nothing (exit 1). `SKILL.md:47` still says not to cite by ID.
- New rules and the role file: the new approval triggers go beyond the role file's `needs_approval` list (section 9). They come from the owner's q1 decision, and they agree with the Architect skill (`skills/software-architect/SKILL.md:24`, where data formats, authentication, payment flows and public API shape are one-way doors) and the base skill (`skills/hire-an-engineer/references/thinking-toolkit.md:79`). The "proposed until the owner's OK" wording follows the Architect's pattern (`agents/architect.md:45`). Nothing new contradicts the role file.

### New findings
#### Critical
none

#### Important
none

#### Minor
1. "Choosing a provider" is an approval only in `method.md`   [confidence: confirmed]
   - Where: `skills/backend-engineer/references/method.md:23,46` list "choosing a provider the owner will be tied to" as an approval. The agent's step 9 (`agents/backend-engineer.md:52`), its `needs_approval` sentence (`:71`), `SKILL.md` rules 1 and 11 and `checklists.md:42` do not.
   - Trigger: a brief such as "add Stripe payments". If the agent follows only its own file, it could pick the provider and list only the money-flow design as an approval. In practice the router sends every job to `method.md`, so the risk is low.
   - Smallest fix: add "choosing a provider the owner will be tied to" to step 9 and to the `needs_approval` sentence in the agent file (and to SKILL rule 11, if it fits).
2. Note only, not a defect of the agent: the role file body and the roster still say `migrations/`   [confidence: confirmed]
   - Where: `docs/agents/roles/backend-engineer.md:60` (section 7) and the roster row `docs/agents/roster.md:13`. The agent and the skill now follow q2 (the existing project folder first). The fix round was not allowed to edit these files.
   - Smallest fix: the boss changes both to "the migrations folder (the existing one, else `migrations/`)" in the follow-up commit. If the roster row changes, re-run `sync_team_start.py`.

### What I ran (re-review)
- `PYTHONUTF8=1 python scripts/validate_agents.py`: exit 0; all 6 agents pass, including `backend-engineer`.
- `PYTHONUTF8=1 python scripts/validate_skills.py`: exit 0; "backend-engineer: description 1008 chars, SKILL.md 50 lines", "All skills valid."
- `python scripts/check_roster.py`: exit 0, "ok: ...docs/agents/roster.md".
- `python scripts/sync_team_start.py --check`: exit 0.
- `python -c` with `yaml.safe_load` to measure the descriptions: 1021 and 1008 characters.
- grep for source IDs (none found) and for the approval lists; `test -f` on the 7 routed base files in both locations (all present).
- Not run: pytest (as the brief said), evals (none exist), `git diff`.
