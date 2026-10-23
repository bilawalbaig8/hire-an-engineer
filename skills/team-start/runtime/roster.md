# Team roster

The single list of specialists the Orchestrator may call. Checked against `agents/*.md` by `python scripts/check_roster.py`.
A role that is not in this table does not exist yet; the boss must say so instead of inventing it. The boss itself
(`orchestrator`) is not listed. Add a row in the same commit that adds the agent file.

| Name | Skill | Model | Owns |
|---|---|---|---|
| architect | software-architect | opus | Solution Architect (System design + Data design). Architecture designs and recovered architectures, decision records (`docs/decisions/`), diagrams, risks; data design (`docs/data/`: store choice, data model, data dictionary and ERD as design before build, access plan, backup and restore plan, migration plans) |
| code-reviewer | code-reviewer | opus | Review reports (`docs/reviews/`): spec compliance and quality verdicts on a change |
| ai-engineer | ai-engineer | opus | AI design notes, eval sets, failure plans and model cards (`docs/ai/`), AI-Ops records (`docs/ai/ops/`: prompt register, release checks, monitor and investigation notes), plus prompt files and AI code in folders the request names |
| data-scientist | data-scientist | opus | Analysis plans and reports (`docs/analysis/`), plus analysis scripts in folders the request names |
| backend-engineer | backend-engineer | opus | Backend & Integration Engineer (Build, Review/Fix, Connect, Check). Backend design notes, API contracts, data dictionaries and backup notes (`docs/backend/`; its data dictionary is what the code really has, the one in `docs/data/` is the design), integration records (`docs/backend/integrations/`: register, service notes, change watch, check reports), migration files (the migrations folder the brief names, else the project's existing migrations folder, else `migrations/`; architect writes only the migration plans), plus server and adapter code in folders the request names |

Rules the boss follows with this table:

- One owner per artifact: the role above that owns a folder is the only one that writes there; others comment.
- The model column is the model the boss passes when it calls the specialist.
- Mechanical steps (list changed files, run a test command) may go to a smaller model with a narrow brief.
