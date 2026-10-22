# Adding a new specialist agent

A specialist is two things: a knowledge folder (`skills/<skill-name>/`) and a thin agent file (`agents/<role-name>.md`). The boss (Orchestrator) talks to the owner; the specialist only answers the boss in the shape of [handoff-contract.md](handoff-contract.md).

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

Who writes the event log (`.agents/events.jsonl`): the hook (`scripts/log_event.py`) writes `agent_start`, `agent_stop` and `file_written`; the boss writes `handoff`, `approval_requested` and `approval_given` with `append_event`; a specialist writes nothing. See the contract.

`hooks-snippet.json` only works where `scripts/log_event.py` and `scripts/agent_contract.py` exist (this repo, or a project that copied them) until the visual-office phase packages them.
