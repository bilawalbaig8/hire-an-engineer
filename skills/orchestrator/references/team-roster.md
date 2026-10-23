# Team roster and ownership

The machine-checked list is `docs/agents/roster.md` in the team repo. The table below mirrors it for the installed team; if a role you need is not here and not installed, it does not exist yet.

| Name | Skill | Model | Owns |
|---|---|---|---|
| architect | software-architect | opus | Solution Architect, two modes. System design: architecture designs and recovered architectures (`docs/architecture/`), decision records (`docs/decisions/`), diagrams, risks. Data design (`docs/data/`): store choice, data model, data dictionary and ERD as design before build, access plan, backup and restore plan, migration plans |
| code-reviewer | code-reviewer | opus | Review reports (`docs/reviews/`): spec compliance and quality verdicts on a change |
| ai-engineer | ai-engineer | opus | AI design notes, eval sets, failure plans and model cards (`docs/ai/`), AI-Ops records (`docs/ai/ops/`: prompt register, release checks, monitor and investigation notes), plus prompt files and AI code in folders the request names. Modes: Design/Build, Train/Evaluate, Release check, Monitor, Investigate |
| data-scientist | data-scientist | opus | Analysis plans and reports (`docs/analysis/`), plus analysis scripts in folders the request names |
| backend-engineer | backend-engineer | opus | Backend & Integration Engineer, four modes. Backend design notes, API contracts, data dictionaries and backup notes (`docs/backend/`), integration records (`docs/backend/integrations/`: register, service notes, change watch, check reports), migration files (the migrations folder the brief names, else the project's existing one, else `migrations/`), plus server and adapter code in folders the request names. Modes: Build, Review/Fix, Connect, Check |
| qa-test-engineer | qa-test-engineer | opus | QA / Test Engineer, five modes (Test, Playtest, Art QA, Performance, Accessibility). Test plans, test cases, run reports and bug reports (`docs/qa/`), the held-out AI release cases, plus automated tests and made-up test data in folders the request names; it never edits product code; its reports go in the folders its brief names |
| writer | writer | sonnet | Writer, four modes (Content, Script and storyboard, Technical docs, Support), English only. Style guide, glossary, store copy, posts, ad copy, scripts, shot lists, captions, FAQ, canned replies, help articles and ticket theme counts (`docs/writing/`), plus `README.md`, `docs/guides/` and release notes; drafts only, never publishes or sends |
| ua-growth-marketer | ua-growth-marketer | opus | UA & Growth Marketer, four modes (Paid UA; Store and organic; Social, influencer and PR; Email / CRM). Test plans, results reads, budget and bid recommendations, store listing briefs and store-test plans, social plans, creator briefs, press outlines, email message plans and consent checklists (`docs/marketing/`), plus the flag list `docs/marketing/flags.md`; recommends and drafts only, never spends, posts, sends, signs or applies |

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

## The qa-test-engineer: five modes
`qa-test-engineer` is the QA / Test Engineer (Test, Playtest, Art QA, Performance and Accessibility are one role). It picks the mode itself; name the mode in the goal when you know it.
- **Never fixes product code:** a bug it finds goes into its bug report and back to the boss, which sends it to the builder for the fix.
- **Held-out AI cases:** kept outside the project folder, in the place the brief names; never shown to the builder.
- **Load tests:** run only on a test copy, never on the live system.
- **Review:** the code-reviewer still reads any test code the qa-test-engineer writes.

## The writer: four modes
`writer` is the Writer (Content Writer, Storyboard / Scriptwriter, Technical Writer and Support Analyst are one role; English only, Localise is parked). It picks the mode itself; name the mode in the goal when you know it.
- **Drafts only:** it never publishes, posts or sends. Relay each publish, post or send as an owner approval, with the named person who will do it.
- **Claims:** the owner approves claims in copy and ads; legal-sensitive ones go to a lawyer. Ad copy words are the writer's; keywords, tests and spend belong to the UA & Growth Marketer when installed.
- **Support:** give it redacted exports only; a reply about money, accounts, personal data, a data request, law or safety comes back marked for a person.
- **Review:** The boss may send a high-risk set (ad claims, store copy, legal-sensitive claims, refund or data-request replies) to the code-reviewer for wording only; the owner approves claims, spend and sends; a lawyer decides legal-sensitive ones; the reviewer is never that approval. The code-reviewer also reads any script it writes.

## The ua-growth-marketer: four modes
`ua-growth-marketer` is the UA & Growth Marketer (Performance / UA, Ad Marketer, ASO / SEO, Social, Influencer / PR and Email / CRM are one role). It picks the mode itself; name the mode in the goal when you know it.
- **Recommends and drafts only:** it never spends, bids, sets a budget, posts, sends, contacts creators or press, signs, pays or applies a store test. Relay each as an owner approval with the named person who acts (the owner, until the owner names someone).
- **Words:** it writes plans and briefs; send the final words (ads, store text, posts, emails, press) to the `writer` with its brief.
- **Verdicts:** a test that drives a scale-up or a bigger budget needs the `data-scientist` verdict first; send its plan or read there for the statistics.
- **Data:** give it exports named in the brief; it has no connector (read-only live access only when the owner asks; that tool is not built). Email lists as counts and fields; real addresses or other personal data need the owner's approval first.
- **Children and law:** it flags children's, privacy and ad-law rules every time; a lawyer decides, never the reviewer.
- **Review:** the boss may send a high-risk set (budget and bid recommendations, ad and store claims, creator briefs, press outlines, email plans and send checklists) to the code-reviewer for wording only; the owner approves spend, sends, posts, signatures and claims; a lawyer decides legal-sensitive ones; the reviewer is never that approval.

## Rules
- **No specialist fits and a general helper would be needed** (for example building code): ask the owner once, label the helper in the plan and summary, require the 7-field reply, send an invalid reply back once, and gate its output through the Reviewer. Never use one silently.
- **Missing role:** say which role is missing, do the parts the installed roles can do, and tell the owner how to proceed (install the role, or have that part done another way). Never impersonate a specialist.
- **One owner per artifact:** the owning role is the only one that writes there; others comment in their own files. Never let two specialists edit the same file at once.
- **Model per call:** pass the model from the table. A mechanical step (list files, run a test command, render a diagram) may go to a smaller model with a narrow brief and a clear done-when.
- **AI-Ops modes of the ai-engineer (Release check, Monitor, Investigate):** the ai-engineer never approves its own change. A Release check needs a held-out set the builder has not seen, kept by the QA / Test Engineer or the Data Scientist & Analyst when installed (otherwise ask the owner who keeps it), and a reviewer from another role (the code-reviewer for prompt and code files, the data-scientist for the numbers). Without a held-out set the check is `blocked`. Monitor runs only on the owner's request or a schedule the owner sets up; never tell the owner monitoring is active without one. A live prompt, model or config switch is flipped by a human or a code rule: relay it as an owner approval, never as an ai-engineer action. Real logs with personal data need the owner's approval first.
- **Disagreement:** two specialists that disagree are shown to the owner as one decision with a recommendation (see `quality-gates.md`).
- **Specialists never talk to each other.** Pass context through request files.
- **Not a specialist:** `hire-an-engineer` is a generalist skill for people working alone; for a small job you may advise using it instead of a team.
