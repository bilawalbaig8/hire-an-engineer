# Team roster and ownership

The machine-checked list is `docs/agents/roster.md` in the team repo. The table below mirrors it for the installed team; if a role you need is not here and not installed, it does not exist yet.

| Name | Skill | Model | Owns |
|---|---|---|---|
| architect | software-architect | opus | Solution Architect, two modes. System design: architecture designs and recovered architectures (`docs/architecture/`), decision records (`docs/decisions/`), diagrams, risks. Data design (`docs/data/`): store choice, data model, data dictionary and ERD as design before build, access plan, backup and restore plan, migration plans |
| code-reviewer | code-reviewer | opus | Review reports (`docs/reviews/`): spec compliance and quality verdicts on a change |
| ai-engineer | ai-engineer | opus | AI design notes, eval sets, failure plans and model cards (`docs/ai/`), AI-Ops records (`docs/ai/ops/`: prompt register, release checks, monitor and investigation notes), plus prompt files and AI code in folders the request names. Modes: Design/Build, Train/Evaluate, Release check, Monitor, Investigate |
| data-scientist | data-scientist | opus | Analysis plans and reports (`docs/analysis/`), plus analysis scripts in folders the request names |
| backend-engineer | backend-engineer | opus | Backend & Integration Engineer, four modes. Backend design notes, API contracts, data dictionaries and backup notes (`docs/backend/`), integration records (`docs/backend/integrations/`: register, service notes, change watch, check reports), migration files (the migrations folder the brief names, else the project's existing one, else `migrations/`), plus server and adapter code in folders the request names. Modes: Build, Review/Fix, Connect, Check |

To see which agents are really installed, list `agents/` of the project and `~/.claude/agents/`. Trust that list over this table.

## The architect: two modes
`architect` is the Solution Architect (the Architect and the Database Architect are one role). Put the mode in every request to it: `mode: "system design"` or `mode: "data design"`.
- **System design:** structure, technology, trade-offs, scale, recover and review existing code, diagrams.
- **Data design:** store choice, data model, data dictionary, ERD, access plan, backup and restore plan, migration plans, deletion plans, review of an existing database.
- **Data design brief:** name the input files in `context_files` (sheets, schema, CSV exports) and the folders it may write in `constraints`: `docs/data/`, `docs/architecture/`, `docs/decisions/`.
- **Not the architect's:** migration files, access tests and server code go to the `backend-engineer` (Backend & Integration Engineer), never to the architect; pipelines to the Data Engineer; metrics and analysis to `data-scientist`; the AI feature to `ai-engineer`. A role not installed or not in your Agent list follows the Missing role rule below.
- **Database job order:** 1. `architect` (data design) writes `docs/data/`. 2. The owner approves each one-way door. 3. `backend-engineer` builds the migrations and access tests from `docs/data/`. 4. `code-reviewer` reads them.

## The backend-engineer: four modes
`backend-engineer` is the Backend & Integration Engineer (the Backend Engineer and the Integration Engineer are one role). It picks the mode itself; name it in the goal when you know it.
- **Build / Review/Fix:** your own server: APIs, database, login and permissions, jobs, migrations, slow spots, duplicates, backups, a first API safety pass.
- **Connect:** a new or changed connection to an outside service (payments, messaging, maps, ad libraries, store APIs, webhooks), including the provider comparison.
- **Check:** looks at existing connections and reports (keys, limits, failures, provider changes). It never fixes; relay the next step as a Connect or Review/Fix job.
- **Brief:** name the folders it may write in `constraints` (`docs/backend/`, the migrations folder, the server or adapter folders). Never paste a real key into a brief; if the owner pastes one, tell the owner it is leaked and must be revoked.
- **Owner approvals it returns:** the choice of a provider (for example which payment service), accepting a provider's terms, a sandbox call with a test key, a live key or call, a bulk collection, a live migration, money, real messages, a deploy, an auth or permission design, data or API formats other code depends on. Relay each one; never approve for the owner.
- **Check never wakes itself:** it runs on the owner's request or a schedule the owner sets up. Never tell the owner connections are watched without one.
- **Review:** every change goes to the `code-reviewer` before it counts as done.

## Rules
- **No specialist fits and a general helper would be needed** (for example building code): ask the owner once, label the helper in the plan and summary, require the 7-field reply, send an invalid reply back once, and gate its output through the Reviewer. Never use one silently.
- **Missing role:** say which role is missing, do the parts the installed roles can do, and tell the owner how to proceed (install the role, or have that part done another way). Never impersonate a specialist.
- **One owner per artifact:** the owning role is the only one that writes there; others comment in their own files. Never let two specialists edit the same file at once.
- **Model per call:** pass the model from the table. A mechanical step (list files, run a test command, render a diagram) may go to a smaller model with a narrow brief and a clear done-when.
- **AI-Ops modes of the ai-engineer (Release check, Monitor, Investigate):** the ai-engineer never approves its own change. A Release check needs a held-out set the builder has not seen, kept by the QA / Test Engineer or the Data Scientist & Analyst when installed (otherwise ask the owner who keeps it), and a reviewer from another role (the code-reviewer for prompt and code files, the data-scientist for the numbers). Without a held-out set the check is `blocked`. Monitor runs only on the owner's request or a schedule the owner sets up; never tell the owner monitoring is active without one. A live prompt, model or config switch is flipped by a human or a code rule: relay it as an owner approval, never as an ai-engineer action. Real logs with personal data need the owner's approval first.
- **Disagreement:** two specialists that disagree are shown to the owner as one decision with a recommendation (see `quality-gates.md`).
- **Specialists never talk to each other.** Pass context through request files.
- **Not a specialist:** `hire-an-engineer` is a generalist skill for people working alone; for a small job you may advise using it instead of a team.
