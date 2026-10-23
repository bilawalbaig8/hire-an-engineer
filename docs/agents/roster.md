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
| qa-test-engineer | qa-test-engineer | opus | QA / Test Engineer (Test, Playtest, Art QA, Performance, Accessibility). Test plans, test cases, run reports and bug reports (`docs/qa/`, with `playtest/`, `art/`, `performance/`, `accessibility/`), the held-out AI release cases (by default, in the place the brief names that the AI Engineer is not given), plus automated tests, made-up test data, bot scripts, benchmark scenes and test configuration in folders the request names; never product code or art |
| writer | writer | sonnet | Writer (Content, Script and storyboard, Technical docs, Support; English only). Style guide and glossary (`docs/writing/`), store copy, posts, ad copy and claims lists (`docs/writing/content/`), scripts, shot lists, captions and variant plans (`docs/writing/storyboards/`), FAQ, canned replies, help articles, escalation list and ticket theme counts (`docs/writing/support/`); edits `README.md`, `docs/guides/` and release notes, `CHANGELOG.md` only when the brief names it; drafts only, never publishes or sends |
| ua-growth-marketer | ua-growth-marketer | opus | UA & Growth Marketer (Paid UA; Store and organic; Social, influencer and PR; Email / CRM). Test plans, results reads, budget and bid recommendations and attribution notes (`docs/marketing/ua/`), store listing briefs, store-test plans and SEO notes (`docs/marketing/store/`), social plans, creator briefs and press outlines (`docs/marketing/social/`), email message plans, audience rules and consent checklists (`docs/marketing/email/`), and the open policy, privacy and claim flags (`docs/marketing/flags.md`); recommends and drafts only, never spends, posts, sends, signs or applies; the Writer writes the final words |

Rules the boss follows with this table:

- One owner per artifact: the role above that owns a folder is the only one that writes there; others comment.
- The model column is the model the boss passes when it calls the specialist.
- Mechanical steps (list changed files, run a test command) may go to a smaller model with a narrow brief.
