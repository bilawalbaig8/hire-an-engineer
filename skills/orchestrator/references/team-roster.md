# Team roster and ownership

The machine-checked list is `docs/agents/roster.md` in the team repo. The table below mirrors it for the installed team; if a role you need is not here and not installed, it does not exist yet.

| Name | Skill | Model | Owns |
|---|---|---|---|
| architect | software-architect | opus | Architecture designs and recovered architectures, decision records (`docs/decisions/`), diagrams, risks |
| code-reviewer | code-reviewer | opus | Review reports (`docs/reviews/`): spec compliance and quality verdicts on a change |
| ai-engineer | ai-engineer | opus | AI design notes, eval sets, failure plans and model cards (`docs/ai/`), AI-Ops records (`docs/ai/ops/`: prompt register, release checks, monitor and investigation notes), plus prompt files and AI code in folders the request names. Modes: Design/Build, Train/Evaluate, Release check, Monitor, Investigate |
| data-scientist | data-scientist | opus | Analysis plans and reports (`docs/analysis/`), plus analysis scripts in folders the request names |

To see which agents are really installed, list `agents/` of the project and `~/.claude/agents/`. Trust that list over this table.

## Rules
- **No specialist fits and a general helper would be needed** (for example building code): ask the owner once, label the helper in the plan and summary, require the 7-field reply, send an invalid reply back once, and gate its output through the Reviewer. Never use one silently.
- **Missing role:** say which role is missing, do the parts the installed roles can do, and tell the owner how to proceed (install the role, or have that part done another way). Never impersonate a specialist.
- **One owner per artifact:** the owning role is the only one that writes there; others comment in their own files. Never let two specialists edit the same file at once.
- **Model per call:** pass the model from the table. A mechanical step (list files, run a test command, render a diagram) may go to a smaller model with a narrow brief and a clear done-when.
- **AI-Ops modes of the ai-engineer (Release check, Monitor, Investigate):** the ai-engineer never approves its own change. A Release check needs a held-out set the builder has not seen, kept by the QA / Test Engineer or the Data Scientist & Analyst when installed (otherwise ask the owner who keeps it), and a reviewer from another role (the code-reviewer for prompt and code files, the data-scientist for the numbers). Without a held-out set the check is `blocked`. Monitor runs only on the owner's request or a schedule the owner sets up; never tell the owner monitoring is active without one. A live prompt, model or config switch is flipped by a human or a code rule: relay it as an owner approval, never as an ai-engineer action. Real logs with personal data need the owner's approval first.
- **Disagreement:** two specialists that disagree are shown to the owner as one decision with a recommendation (see `quality-gates.md`).
- **Specialists never talk to each other.** Pass context through request files.
- **Not a specialist:** `hire-an-engineer` is a generalist skill for people working alone; for a small job you may advise using it instead of a team.
