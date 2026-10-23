# Team roster and ownership

The machine-checked list is `docs/agents/roster.md` in the team repo. The table below mirrors it for the installed team; if a role you need is not here and not installed, it does not exist yet.

| Name | Skill | Model | Owns |
|---|---|---|---|
| architect | software-architect | opus | Architecture designs and recovered architectures, decision records (`docs/decisions/`), diagrams, risks |
| code-reviewer | code-reviewer | opus | Review reports (`docs/reviews/`): spec compliance and quality verdicts on a change |

To see which agents are really installed, list `agents/` of the project and `~/.claude/agents/`. Trust that list over this table.

## Rules
- **No specialist fits and a general helper would be needed** (for example building code): ask the owner once, label the helper in the plan and summary, require the 7-field reply, send an invalid reply back once, and gate its output through the Reviewer. Never use one silently.
- **Missing role:** say which role is missing, do the parts the installed roles can do, and tell the owner how to proceed (install the role, or have that part done another way). Never impersonate a specialist.
- **One owner per artifact:** the owning role is the only one that writes there; others comment in their own files. Never let two specialists edit the same file at once.
- **Model per call:** pass the model from the table. A mechanical step (list files, run a test command, render a diagram) may go to a smaller model with a narrow brief and a clear done-when.
- **Disagreement:** two specialists that disagree are shown to the owner as one decision with a recommendation (see `quality-gates.md`).
- **Specialists never talk to each other.** Pass context through request files.
- **Not a specialist:** `hire-an-engineer` is a generalist skill for people working alone; for a small job you may advise using it instead of a team.
