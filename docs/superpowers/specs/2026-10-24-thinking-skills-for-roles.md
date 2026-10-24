# Thinking skills for roles and the boss gate: plan

Status: plan, agreed in discussion on 2026-10-24. Nothing is built yet.

## Goal

Make the team think more critically at every stage, and let the boss judge the final file with real analysis instead of trusting "done".

## Decision

- No "philosopher" or "psychologist" agent. A persona gives style, not a check.
- Use named thinking procedures (the existing `thinking-*` skills) and attach 2-4 of them to each role.
- Add a short critical check at the boss gate, sized by the job.
- Add one independent "Challenge mode" to the Code Reviewer for high-stakes gates only.
- Keep agent files thin. The knowledge stays in skills (repo rule).

## Layer 1: skills per role

Each agent file gets one short section: "Thinking skills: use these in these situations". Max 4 per role.

| Role | Skills | When |
|---|---|---|
| QA / Test Engineer | scientific-method, map-territory, inversion, red-team | find a cause; verify running code, not docs; derive test cases from "how to make it fail"; attack paths |
| Code Reviewer | red-team, debiasing, steel-manning | security findings; check own anchoring; before rejecting a design |
| Solution Architect | pre-mortem, reversibility, second-order, first-principles | before a decision record; one-way doors; side effects; "too expensive" claims |
| Product & Business Analyst | jobs-to-be-done, first-principles, steel-manning | what to build; challenge fixed constraints; opposing case |
| Project Manager | pre-mortem, theory-of-constraints, opportunity-cost | plan risks; the bottleneck; what we give up |
| Data Scientist & Analyst | bayesian, probabilistic, debiasing | read a test result; forecasts; p-hacking guard |
| Orchestrator (boss) | map-territory, pre-mortem, steel-manning, debiasing, inversion | final gate (Layer 2) |

Other roles get skills when they are built (part of every build).

## Layer 2: boss acceptance check

Added to the orchestrator skill, as one reference file. Size by job:

- Small job: one question, map-territory. "Did I check one claim myself (open the file, run the command), or only read the report?"
- Medium job: add pre-mortem. "Assume this failed in a month. What is the most likely cause?"
- Large or one-way-door job: add steel-manning (strongest case against the decision), debiasing (are we protecting an early choice against evidence?), inversion (how would we guarantee failure?).

Rules:
- The boss must verify at least one claim itself on every medium or large job (but never redo a specialist check; existing rule).
- The result is logged in the run record as one line: checks run, one finding or "none".
- The boss tells the owner the findings in plain words, in the owner's language.

## Layer 3: Code Reviewer Challenge mode

- A mode of the Code Reviewer, not a new agent (no new agent count).
- Input: only the deliverable and the stated goal. No other agent's conclusion, so it is not anchored.
- Output: the usual 7-field shape; findings are objections with evidence, ranked.
- Used only at: release, architecture decision records, data formats, anything hard to undo.
- The boss chooses it; it is not run on every job.

## Limits and risks

- Too many skills per agent make answers slow and wandering. Cap: 4 per role.
- Thinking runs at gates, not in every reply. Keep to the token-discipline rule.
- Description limit: agent descriptions are 1,024 chars max. Several roles are near the limit (Data Scientist 1,016, Backend 1,019). Put the thinking list in the agent body, not in the description.
- The existing `thinking-*` skills come from outside this repo and the install script does not copy them. Do not depend on them (see Decisions). The table above uses their method names only as names of our own methods.

## Proof (test)

A planted-mistake test: give the boss a job where a specialist report contains one false claim (for example "all tests pass" while one fails). Pass = the boss catches it at the gate and says so. Run it once on a small job and once on a large job. Also run one Challenge mode case on a design with a hidden one-way door.

## Decisions (recommended, owner rule added 2026-10-24)

1. Challenge mode is a Code Reviewer mode, not a new agent. Reason: the reviewer is already independent and never edits; a new agent adds count, cost and a new description to maintain.
2. The boss sizes the check (small, medium, large). Reason: the full set on every job wastes tokens and trains the boss to skim.
3. No external dependency. The team must work from this repo alone. So the thinking skills are not referenced from outside plugins and not copied from them. We write our own short skill, `skills/critical-thinking/`, in our own words:
   - `SKILL.md`: router plus the core rule (named procedure, not persona).
   - `references/`: one short file per method (map-territory check, pre-mortem, steel-manning, inversion, debiasing check, red-team, scientific-method, second-order, reversibility, bayesian update). Each file: when to use, 3-6 steps, one example, one stop rule.
   - `references/sources.md`: the public origin of each method (for example pre-mortem: Gary Klein, 2007 HBR; red team and inversion: public writing) with a checked link. Only ideas are used, so credit is to the idea's author; if any text is adapted from a licensed file, add it to THIRD_PARTY_NOTICES.md with its licence.
   - Roles list the method names and read the file; if the skill is missing the agent still works (the section says "if the skill folder is present").
   - The install script copies this skill like the others, so one `--only` install is enough.

## Revision after review (2026-10-24, owner approved)

The plan was checked with pre-mortem, steel-manning, inversion and map-territory. Findings and changes:

Facts checked in the repo:
- `skills/hire-an-engineer/references/thinking-toolkit.md` already exists (pre-mortem, inversion). Extend it; do not start from zero. Its header says it is drawn from an outside source, so rewrite in our own words or add a notice. It lives inside the `hire-an-engineer` skill, so specialists installed with `--only` do not get it: move or copy it into the team-level skill.
- `agents/code-reviewer.md` has no modes. Challenge mode is a new design, not a switch.
- `skills/qa-test-engineer/references/method-test.md` has no thinking method: the gap is real.
- Not verified: the description lengths near 1,024 (taken from TASKS.md). Check the real files before E3.

Main risks and the change that answers each:
1. Skills become ritual (an agent writes "pre-mortem done" and nothing changes) -> every method has an output contract: one line that shows what changed.
2. The boss gate gives false comfort (verifies the easy claim) -> verify the riskiest claim, the one "done" depends on.
3. Challenge mode loses independence (the brief carries a conclusion) -> a brief template that forbids other agents' conclusions.
4. Cost and upkeep (10 methods, 15 roles, many links to verify) -> 5 methods first.
5. Same model family has shared blind spots -> the planted-mistake test measures real misses; one-way doors still go to the owner.

Strongest case against the plan: models already do a pre-mortem when asked; the value is in the gate and the output rule, not in skill files. Accepted in part. Result: measure first.

New order: E6a baseline test of today's boss, then E5 gate, E6b rerun and compare, E4 Challenge mode, then the skill (E1b), then roles only where a miss showed (E3, E2).

## Rule for all new work
Every new skill, agent and script in this repo must run without any other repository, plugin or global skill. If an outside tool is useful (Gemini CLI, a plugin), it may help the owner write documents, but the shipped result must not call it.
