# Adding a new specialist agent

A specialist is two things: a knowledge folder (`skills/<skill-name>/`) and a thin agent file (`agents/<role-name>.md`). The boss (Orchestrator) talks to the owner; the specialist only answers the boss in the shape of [handoff-contract.md](handoff-contract.md).

Follow these ten steps. They match the Definition of Done in `docs/superpowers/specs/2026-10-22-agent-team-master-plan.md` (section 6).

1. Copy this folder: `skill/` to `skills/<skill-name>/`, `agent.md` to `agents/<role-name>.md`. Fill the names; keep `name` equal to the file name and `skill` equal to the skill folder.
2. Write the spec (what the role owns, what it never does, which model and why) and get the owner's approval before building.
3. Research the sources, check each one, and write `skills/<skill-name>/references/sources.md` with `verified` or `unverified` for every row. Credit them in `THIRD_PARTY_NOTICES.md`.
4. Write the knowledge files in your own words, citing sources by ID. No copied passages.
5. Fill in the agent file: role, when to use, model and why, tools, reads first, how it works, handoff, never.
6. Write the evals first (a typical case, an edge case and a refusal case at least) in `evals/<skill-name>/evals.json`, then run them after the build.
7. Run the checks: `PYTHONUTF8=1 python scripts/validate_skills.py`, `python scripts/validate_agents.py`, `python scripts/check_sources.py skills/<skill-name>`, `python -m pytest -q`. All must pass.
8. Add a CHANGELOG entry for the skill.
9. Make the repo copy and the installed copy identical: `python scripts/install_agents.py --dry-run` shows what would change; copy only after the owner agrees.
10. Commit. Release (tag `<skill-name>-v<version>`) only when the owner says so.

Related: the event log (`.agents/events.jsonl`) is written by the hook in `scripts/log_event.py` (see "Event sources" in the contract), so a specialist never writes it by hand.
