# Adding a new specialist agent

A specialist is two things: a knowledge folder (`skills/<skill-name>/`) and a thin agent file (`agents/<role-name>.md`). The boss (Orchestrator) talks to the owner; the specialist only answers the boss in the shape of [handoff-contract.md](handoff-contract.md).

**Before step 1 (the role's own file):** write the role's own file first: `docs/agents/roles/<role-name>.md`, one file per role (never one shared file): what it is, which problems it solves, what it does not do, modes, outputs, method, safety rules, tools and model, the knowledge plan, the research material (source counts, verified or not, the main sources), the eval plan, the place in the team, the calls made without the owner, and what is left. Start from the matching parts of the owner's own skill `skills/hire-an-engineer/` (its references and roles table): say in the file what was taken as it is, what was deepened and what was changed, and never contradict it silently. Give it to the owner in their language and wait for the approval before building further (look at `docs/agents/roles/data-scientist.md`).

Follow these ten steps. They match the Definition of Done in `docs/superpowers/specs/2026-10-22-agent-team-master-plan.md` (section 6).

1. Copy this folder: `skill/` to `skills/<skill-name>/`, `agent.md` to `agents/<role-name>.md`. Fill the names; keep `name` equal to the file name and `skill` equal to the skill folder.
2. Write the spec (what the role owns, what it never does, which model and why) and get the owner's approval before building.
3. Research the sources, check each one, and write `skills/<skill-name>/references/sources.md` with `verified` or `unverified` for every row. Credit them in `THIRD_PARTY_NOTICES.md`.
4. Write the evals BEFORE the knowledge and the agent file: at least a typical case, an edge case and a refusal case in `evals/<skill-name>/evals.json`. Every case needs `id`, `prompt`, `kind` (`typical`, `edge` or `refusal`) and `expect` (a non-empty list of text lines). They must pass after the build (step 7).
5. Write the knowledge files in your own words, citing sources by ID. No copied passages.
6. Fill in the agent file: role, when to use, model and why, tools, reads first, how it works, handoff, never.
7. Run the checks and the evals: `PYTHONUTF8=1 python scripts/validate_skills.py`, `python scripts/validate_agents.py`, `python scripts/check_sources.py skills/<skill-name>`, `python scripts/check_evals.py evals/<skill-name>/evals.json`, `python -m pytest -q`. All must pass, and the evals must pass against the finished agent.
8. Add a CHANGELOG entry for the skill.
9. Make the repo copy and the installed copy identical: `python scripts/install_agents.py --dry-run` shows what would change; install only after the owner agrees; then check with `diff -rq skills/<skill-name> ~/.claude/skills/<skill-name>` and `diff -q agents/<role-name>.md ~/.claude/agents/<role-name>.md`. The installer never removes stale files, so delete files you removed from the repo by hand.
10. Commit. Release (tag `<skill-name>-v<version>`) only when the owner says so.

## Also part of every build (owner decision 2026-10-24)

These are not separate tasks. A role is not done until each line below is done in the same build. Add them to the commit and to the checks in step 7.

- **Boss can call it.** Add the agent to the `Agent(...)` list in `agents/orchestrator.md`, to the routing in `skills/orchestrator/references/team-roster.md`, and to `docs/agents/roster.md` (model and effort columns). `python scripts/check_roster.py` must pass. A role the boss cannot call is not built.
- **Model and effort** follow the owner's table in `~/.claude/CLAUDE.md` and the spec; the boss may step a `sonnet` role up to `opus` after two failed runs and says so.
- **Description limit.** The agent and skill descriptions stay at 1,024 characters or less, with room for the modes the spec plans. Count them before writing.
- **Guards.** A role that holds keys, deploys or makes network calls gets the PreToolUse guard from the spec (DevOps and the Backend & Integration Engineer; decision Q9) and a test that the guard blocks a live command.
- **Live access.** Where the spec allows live read access (decision Q15), add the browser or connector tool as read-only, and test that the role cannot edit or save in the source.
- **Lessons.** Add `docs/lessons/<role>.md` to the role's reading list (it reads it before every job); the boss writes a lesson when the owner reports an issue (decision X2).
- **Evals.** Write results as "k of n runs on N cases". A partial case is rerun after its fix. Held-out cases for another role's check are kept by the QA / Test Engineer outside the project folder (decision Q1).
- **Office window.** Add the seat id and aliases for the agent name, and set its tag in the `TAGS` map in `docs/agents/visual-office/index.html` (Built, then Tested), then run `python scripts/sync_team_start.py`.
- **Tracking.** Update the row in `TASKS.md` and in the tracker artifact (Documentation and Build columns), and the role document's status line.
- **Install and push.** Install with `python scripts/install_agents.py --only <skill-name>`, run `check_installed.py`, commit, and push only when the owner says.

Who writes the event log (`.agents/events.jsonl`): the hook (`scripts/log_event.py`) writes `agent_start`, `agent_stop` and `file_written`; the boss writes `handoff`, `approval_requested` and `approval_given` with `append_event`; a specialist writes nothing. See the contract.

`hooks-snippet.json` only works where `scripts/log_event.py` and `scripts/agent_contract.py` exist (this repo, or a project that copied them) until the visual-office phase packages them.
