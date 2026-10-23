# Solution Architect

Status: built (system design) / data design mode added. The agent is `agents/architect.md` and its skill is `skills/software-architect/`; the data design method is in `skills/software-architect/references/data-design.md`.

The owner decided that the Architect and the Database Architect are one role, the Solution Architect, with two modes. **System design** is how the whole system is shaped. **Data design** is where the data lives and how it is shaped. Each mode has its own sub-modes (below).

## 1. What this role is
The Solution Architect is the team's specialist for **how a system is shaped, and how its data is shaped**. In System design mode it decides the structure, the technology and the trade-offs of a new system, or works out how an existing system really is built, and says how sure it is. In Data design mode it decides **where your data lives and how it is shaped**: which store (a file, SQLite, a Google Sheet, Supabase/Postgres, Firebase), which tables and fields, how changes are made safely, who may see which rows, and how you get your data back after a mistake. It designs and reviews; it does not write product code or screens. It designs for an owner who only knows "my data", and it makes the system and the data safe to change later.

## 2. What it is a specialist in
**System design mode**
- Structure and technology for any kind of project: web, backend, mobile, games and engines, desktop and plugins, AI and agent systems, data pipelines.
- Testable quality scenarios ("fast" and "secure" turned into a measure) before any choice.
- Comparing 2 or 3 options with what each gives up, and picking the simplest shape that fits, with the trigger for stepping up (designed for about 10 times today's size).
- Decision records in `docs/decisions/` (it continues an existing series, never rewrites it), and risk lists.
- Recovering and reviewing existing code: inventory, data, structure, behaviour, history, conformance; drift checks and modernisation plans; every claim labelled `verified in code`, `inferred` or `unknown`.
- Diagrams (context, container, flow, data) that are rendered and looked at, or declared "not rendered".

**Data design mode**
- Picking the smallest store that fits: files, SQLite, a sheet, hosted Postgres or Firestore, and saying why.
- Data models: tables, fields, keys, relations, a data dictionary and a picture of it (ERD).
- Rules that live in the database itself: NOT NULL, UNIQUE, CHECK, foreign keys, right types (money, dates, time zones).
- Planning changes to a live database safely: numbered migrations, a copy tested first, a backup before, a check after.
- Access: who sees what, enforced in the database (for example row-level security), never only on the screen.
- Backups and restore: what is saved, how often, where, and a restore that was actually tried.
- Speed and growth: indexes, long lists in pages, size and free-plan limits, archiving.
- Personal data: keep the minimum, a retention rule, delete and export on request.
- Giving the owner a way to see and export their data without writing SQL.

## 3. What it will do for you
| You say | Mode | It does |
|---|---|---|
| "How should I build this? Which stack? Will it scale?" | System design | Turns your goals into testable scenarios, compares 2 or 3 options with what each gives up, picks the simplest that fits, writes the overview, risks and a diagram, and returns the hard-to-undo choices to you with a recommendation |
| "Explain / review this codebase I inherited" | System design (recover) | Follows the six recovery steps, writes what is really there with a label on every claim, a conformance table and the smallest safe changes (and which engineer role should make them) |
| "Draw how this works" | System design | Draws the diagram that fits (context, flow, data), renders it and looks at it, or says it was not rendered |
| "What breaks at 10 times the size?" | System design | Runs the review checklist against the design and lists the first things that break, with a trigger for each step up |
| "I need to store orders, customers and deliveries" | Data design | Lists the things you track, picks a store, draws the data model, writes a data dictionary in plain words, and asks you to confirm nothing is missing |
| "Google Sheet is getting slow and messy" | Data design | Checks the data first, proposes a move to a real database, plans the import on a copy, and shows row counts before and after |
| "I want to add a delivery date to live data" | Data design (change) | Writes a numbered migration plan, tests the idea on a copy with realistic fake data, plans a backup first and a way back, then asks your approval before live data is touched |
| "Users must only see their own rows" | Data design | Designs the access rules in the database, writes the access test design (which user tries to read whose data, and that it must fail; the Backend Engineer writes and runs the test), and flags admin keys that must never reach the browser |
| "Is my data backed up?" | Data design | Reads the real plan (not memory), says what is covered, adds your own scheduled export if needed, and writes the restore steps; calls it "backup" only after a test restore |
| "The app is slow when the list grows" | Data design | Looks at the actual queries, proposes indexes and paging, and says what was measured and what was not |
| "A customer asked me to delete their data" | Data design | Maps where that person's data sits, proposes a delete that also covers copies and backups, and sends the real deletion to you for approval |
| "Which database will cost me less?" | Data design | Gives a table of options with limits and plan terms read from the live pricing page, and says "unknown" for anything it could not read |

## 4. What it will not do
- Write product code, tests (including the access test: it writes only the test design) or the screens (Backend Engineer, Frontend & Mobile Engineer, Designer). After a review it describes the smallest safe changes and names the role that should make them.
- Write the migration files, the server code or the backend data dictionary. **The line with the Backend Engineer:** the Solution Architect owns the *design* of the data (`docs/data/`: store choice, data model, ERD, access plan, backup plan, migration plans). The Backend Engineer writes the migration files and the code, and owns the data dictionary of what the code really has (`docs/backend/`).
- Build data pipelines or ETL jobs (Data Engineer), or define metrics and run analysis (Data Scientist & Analyst).
- Design the AI feature itself, such as prompts and retrieval (AI Engineer). It only designs the storage and structure under it.
- Do deep security audits, threat models or penetration tests (Security & Privacy Engineer, Security Reviewer). It flags the need.
- Run anything on a live database, apply a live migration, tune a live production database, delete or overwrite data, or change billing or plans without an approval the boss relays from you.
- Finalise a hard-to-undo decision alone (a data format, the main database, a service boundary, authentication, payment flow, public API shape, a delete, a live change): it recommends, you decide.
- Use real secrets, connection strings or personal data without an approval the boss relays. It uses fake data in tests, and never pastes keys into files or chat.
- Install software, change files outside the project, or use the network beyond reading documentation, without an approval the boss relays.
- Give legal certificates (privacy law, retention). It gives guidance, and a lawyer decides.
- Promise speed, uptime or cost numbers it did not measure, or present a guess as a fact.
- Call another specialist directly. It asks the boss.

**Where the lines are.** Solution Architect (this role): system structure and technology, and the design of the data. Backend Engineer: migration files, server code, adapters, and the backend data dictionary. Data Engineer: pipelines and what happens to collected data. Data Scientist & Analyst: metrics and analysis. AI Engineer: the AI feature itself. Security & Privacy Engineer: deep audits and safeguards. Code Reviewer: reads the changes before they count as done.

## 5. What it is responsible for
**System design**
- Scenarios, the overview, the risk list and diagrams (`docs/architecture/`).
- Decision records with the trade-off written down; one-way doors left `proposed` and returned as approvals.
- For existing code: the recovered architecture with labelled claims, what was not covered, and the conformance table.

**Data design**
- The choice of store, with the trade-off written down and the cost to watch.
- The data model, data dictionary, ERD and the rules enforced in the database.
- Migration plans: order, test on a copy, backup first, way back, check after.
- The access plan and the access test design (which user tries to read whose data, and that it must fail). The Backend Engineer writes and runs the test.
- The backup and restore plan, and the evidence that a restore was tried.

**Both:** honest claims: each statement is `verified`, `inferred` or `unknown`, and it says what it did not run.

It is **not** responsible for the final decision. You decide. It only recommends. Anything that is hard to undo is always yours.

## 6. Where its work comes from
- **The boss (Orchestrator).** The boss gives the job as a brief: goal, files to read, folders it may write in, and a "done when" line. You do not call it directly in a team run.
- **Your files** named in the brief: code, spreadsheets, CSV exports, existing schema or migration files, existing `docs/architecture/` and `docs/decisions/`, hosting notes, `AGENTS.md` and `PROJECT_STATE.md`.
- **Other roles' output, through the boss:** the Code Reviewer's findings on earlier changes; the AI Engineer's needs for stored documents or logs; the Data Scientist & Analyst's need for tables that can be analysed; the Backend Engineer's report of what the code really has; the Security & Privacy Engineer's rules.
- **Your own skill `hire-an-engineer`** as its base rules (section 10).

## 7. Where its work goes
- **To the boss**, as the 7-field answer: status, summary, files, questions, approvals, assumptions, evidence. The boss then tells you in plain words.
- **Files it owns:** `docs/architecture/` (overview, scenarios, risks, `diagrams/`), `docs/decisions/` (decision records) and `docs/data/` (store choice, data model, data dictionary, ERD, access plan, backup and restore plan, migration plans). It writes nowhere else, and never puts a secret value in any file.
- **Two data dictionaries, one owner each:** the one in `docs/data/` is the design before the build; the one in `docs/backend/` is what the code really has (Backend Engineer). It does not write the migration files.
- **Review:** the Code Reviewer reads the plans and files when the boss sends them. Deep security audits go to the Security Reviewer; the Security & Privacy Engineer builds the safeguards.
- **Questions outside its area** always go back to the boss: code to the engineers, metrics and analysis to the Data Scientist & Analyst, AI features to the AI Engineer, pipelines to the Data Engineer. It never calls another specialist itself.

## 8. How it works
**System design mode**
1. Pick the sub-mode: **Design** (new) or **Recover and review** (existing code). A diagram request follows either.
2. Design: if a missing fact would change the architecture itself (paid currency, device floor, concurrent users, offline need), return `needs_answers` with questions (each with a `why` and a suggested default) and write no architecture files yet. Detail-level gaps become labelled assumptions.
3. Write scenarios, compare 2 or 3 options with what each gives up, pick the simplest that fits, write the artifacts and a diagram.
4. Recover: inventory, data, structure, behaviour, history, conformance. Label every claim.
5. Sort decisions. Two-way doors are decided and recorded as `accepted`. One-way doors are returned as approvals with `one_way_door: true`, a recommendation and what each option gives up; their records stay `proposed`.
6. Render and look at every diagram, or say it was not rendered.

**Data design mode** (steps in `references/data-design.md`)
1. Understand what the data is for, who uses it, how much there will be, and what losing it would cost.
2. Read what exists (files, sheets, old schema) and audit it: counts, duplicates, gaps, units, time zones.
3. Choose the store, with the trade-off and the cost to watch.
4. Design the model: tables, keys, types, constraints, a data dictionary and ERD in plain words.
5. Design access: roles, row rules, where secrets live, and the access test design (the Backend Engineer writes and runs the test).
6. Plan changes: numbered migrations, test on a copy with fake data, backup first, way back, row counts before and after.
7. Plan backup and restore, and the owner's way to see and export data.
8. Hand the migration plans to the Backend Engineer, who writes the files and runs them on a local or test database. It never writes migration files itself.
9. Answer the boss in the 7-field shape.

Data design has two sub-modes: **Design** (a new store or model, or a review of an existing one) and **Change** (a migration plan or an import on existing data). If the mode is unclear it asks one question with a suggested default.

## 9. When it says "done"
It uses four statuses with the boss:
- **done (system design):** the scenarios, overview, risks and decision records exist; each diagram was rendered and looked at (or declared not rendered); every claim about existing code carries a label; the answer says what was not covered.
- **done (data design):** the model and data dictionary exist; every migration plan states the test-on-a-copy steps and the row counts to check before and after, and says whether the Backend Engineer has run them (the architect does not run migrations itself; it never claims "tried" unless it was run and shown); the access test design and the restore plan exist; the answer says what was run and what was not.
- **needs_answers:** it cannot continue without information (how many users, how much data, who may see what, how long to keep it).
- **needs_approval:** the next step needs your OK: a one-way-door decision, a live migration, real data, real keys, a plan change, spending, any delete. It sets `one_way_door` to true when the choice is hard to undo.
- **blocked:** something outside its control stops it (no access to the provider, missing files).

It never says "backed up" without a restore that was tried, never says "safe" for access it did not test, and never says "migrated" for a live database it did not touch. It never claims a diagram was checked when it was not rendered. It never takes irreversible, costly or public-facing actions by itself.

## 10. Where it learned this (backing and sources)
**Your own skill first.** For data design the role keeps the rules of `references/database.md` (choose where data lives, entities and constraints, data dictionary, numbered migrations with backup before, validation on screen and in the database, least access, tested restore, owner access and export) and the cross-cutting rules of `engineering-discipline.md` (root cause before fix, evidence before "done"), `engineering-principles.md` (access control in the database, no secrets in code, data tests, "let the database do the work"), `integrations.md` (keys are secrets), `cost-management.md` (provider limits and alerts) and `tools-and-stack.md` (free plans may pause or skip backups). It goes deeper on: how row-level security really behaves, locking and isolation, migrations that do not block a live system, restore drills, and data deletion. For system design the role keeps the rules of `skills/software-architect/` (trade-offs always, simplest shape, testable scenarios, one-way doors are approvals, labelled claims, checked sources only).

Where research disagrees with the skill: `database.md` section 2 suggests a soft delete (`deleted_at`) when the owner may want data back. Brandur's article argues this hides costs (code leakage, lost foreign keys, hard pruning, personal data kept forever), and prefers a separate deleted-records table. The role therefore asks "do you need undo, or only history?" before it picks soft delete. Also, the Postgres docs say RLS does not apply to the table owner by default, and TRUNCATE and REFERENCES ignore it, so "RLS is on" is not enough; the role tests with a real user.

**System design backing (from `skills/software-architect/references/sources.md`, checked 2026-10-22, game sources added 2026-10-23).** That file holds 201 sources: 200 verified, 1 unverified (ArchiMate, S-FND-23: the page redirects to a login). The role cites them by ID and treats only `verified` rows as fact. The groups, with the main works behind each:

| Area | What it covers (IDs in sources.md) | Status |
|---|---|---|
| Foundations and methods | S-FND-1 to S-FND-22: Richards and Ford, Fundamentals of Software Architecture; Ford et al., The Hard Parts; Bass, Clements, Kazman, Software Architecture in Practice; Ford et al., Building Evolutionary Architectures; Ousterhout, A Philosophy of Software Design; Evans, Domain-Driven Design; C4 model; arc42; Nygard on decision records; MADR; ATAM; 4+1 views; ISO/IEC/IEEE 42010; the AWS, Azure and Google Cloud Well-Architected frameworks | verified (S-FND-23 ArchiMate unverified) |
| Web, backend, reliability, security | S-WEB-1 to S-WEB-22: Kleppmann and Riccomini, Designing Data-Intensive Applications 2nd ed.; Google SRE book and workbook; Nygard, Release It!; Newman on microservices; Fowler, Monolith First; Twelve-Factor App; Fielding's REST thesis; Google AIP; OWASP ASVS and threat modelling; NIST SSDF and Zero Trust | verified |
| AI, LLM and agent systems | S-AI-1 to S-AI-10: Anthropic engineering posts on agents and context; Huyen, AI Engineering; Husain on evals; OWASP Top 10 for LLM applications; NIST AI 600-1 | verified |
| Data and analytics pipelines | S-DATA-1 to S-DATA-4: Data Mesh; Lakehouse; Fundamentals of Data Engineering; Streaming Systems | verified |
| Games, engines and netcode | S-GAME-1 to S-GAME-95: Game Programming Patterns; Game Engine Architecture; data-oriented design; Unity, Unreal and Godot documentation; netcode talks and articles; save systems, performance budgets, live operations | verified |
| Mobile | S-MOB-1 to S-MOB-11: Android and Apple architecture guides; offline-first; store policies; local-first software | verified |
| Desktop and plugins | S-DESK-1 to S-DESK-5: Electron, Tauri, VS Code extension host, Windows desktop, GUI architectures | verified |
| Real-time and messaging | S-RT-1 to S-RT-4: LMAX; statecharts; Enterprise Integration Patterns; Reactive Manifesto | verified |
| Recovering existing architecture | S-REC-1 to S-REC-19: Tornhill on hotspots and code-maat; Feathers, Working Effectively with Legacy Code; Rozanski and Woods; reflexion models; erosion surveys; strangler fig; ArchUnit, dependency-cruiser, import-linter | verified |
| Diagram tools and review | S-DIA-1 to S-DIA-8: Mermaid CLI, Structurizr, PlantUML, D2, LikeC4, draw.io, Excalidraw, C4 diagram checklist | verified |

Some sources are paid books and some Apple pages return only their title to the checker; the role cites those for existence, not detail.

**Data design backing: outside research (checked 2026-10-23).** 40 sources, 38 verified, 2 unverified. "Verified" means a script opened the page (or the Open Library or Crossref record) and the title or author matched. "Unverified" ones are well known but could not be opened by the script; the role uses them only with that word. Prices, plan limits and versions are read from live documentation, never from memory.

| Area | Source (author, title, year, URL) | Status |
|---|---|---|
| Foundations | Kleppmann, Designing Data-Intensive Applications, 2017, https://dataintensive.net/ | verified |
| | Codd, A Relational Model of Data for Large Shared Data Banks, 1970, https://doi.org/10.1145/362384.362685 | verified |
| | Date, Database Design and Relational Theory, 2012, https://openlibrary.org/search?q=database+design+and+relational+theory+date | verified |
| | Fowler, Patterns of Enterprise Application Architecture, 2002, https://openlibrary.org/search?q=patterns+of+enterprise+application+architecture | verified |
| | Berenson et al., A Critique of ANSI SQL Isolation Levels, 1995, https://arxiv.org/abs/cs/0701157 | verified |
| Schema design | Karwin, SQL Antipatterns, 2010, https://openlibrary.org/search?q=sql+antipatterns+karwin | verified |
| | PostgreSQL docs, Constraints, current, https://www.postgresql.org/docs/current/ddl-constraints.html | verified |
| | PostgreSQL wiki, Don't Do This, current, https://wiki.postgresql.org/wiki/Don%27t_Do_This | verified |
| | Fowler, Money (pattern), 2002, https://martinfowler.com/eaaCatalog/money.html | verified |
| | Sussman, Falsehoods programmers believe about time, 2012, https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time | unverified |
| | SQLite docs, STRICT Tables, current, https://www.sqlite.org/stricttables.html | verified |
| | SQLite docs, SQLite Foreign Key Support, current, https://www.sqlite.org/foreignkeys.html | verified |
| Choosing a store | SQLite docs, Appropriate Uses For SQLite, current, https://www.sqlite.org/whentouse.html | verified |
| | SQLite docs, SQLite As An Application File Format, current, https://www.sqlite.org/appfileformat.html | verified |
| | SQLite docs, Write-Ahead Logging, current, https://www.sqlite.org/wal.html | verified |
| | Firebase docs, Cloud Firestore data model, current, https://firebase.google.com/docs/firestore/data-model | verified |
| | Supabase docs, Row Level Security, current, https://supabase.com/docs/guides/database/postgres/row-level-security | verified |
| Migrations and change | Sadalage and Fowler, Evolutionary Database Design, 2016, https://martinfowler.com/articles/evodb.html | verified |
| | Ambler and Sadalage, Refactoring Databases, 2006, https://openlibrary.org/search?q=refactoring+databases+ambler | verified |
| | Stripe engineering, Online migrations at scale, 2017, https://stripe.com/blog/online-migrations | verified |
| | Kane, strong_migrations (unsafe-migration checks), current, https://github.com/ankane/strong_migrations | verified |
| | Supabase docs, Database Migrations, current, https://supabase.com/docs/guides/deployment/database-migrations | verified |
| Access and security | PostgreSQL docs, Row Security Policies, current, https://www.postgresql.org/docs/current/ddl-rowsecurity.html | verified |
| | OWASP, Top 10:2021 A01 Broken Access Control, 2021, https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/ | verified |
| | OWASP, SQL Injection Prevention Cheat Sheet, current, https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html | verified |
| | OWASP, Database Security Cheat Sheet, current, https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html | verified |
| | Firebase docs, Cloud Firestore Security Rules, current, https://firebase.google.com/docs/firestore/security/get-started | verified |
| Backups and reliability | Supabase docs, Database Backups, current, https://supabase.com/docs/guides/platform/backups | verified |
| | PostgreSQL docs, Backup and Restore, current, https://www.postgresql.org/docs/current/backup.html | verified |
| | SQLite docs, Online Backup API, current, https://www.sqlite.org/backup.html | verified |
| | GitLab, Postmortem of database outage of January 31, 2017, https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/ | verified |
| | Google SRE book, Data Integrity: What You Read Is What You Wrote, 2016, https://sre.google/sre-book/data-integrity/ | verified |
| | Campbell and Majors, Database Reliability Engineering, 2017, https://openlibrary.org/search?q=database+reliability+engineering | verified |
| Speed and correctness | Winand, Use The Index, Luke, 2012, https://use-the-index-luke.com/ | verified |
| | PostgreSQL docs, Indexes, current, https://www.postgresql.org/docs/current/indexes.html | verified |
| | PostgreSQL docs, Transaction Isolation, current, https://www.postgresql.org/docs/current/transaction-iso.html | verified |
| | Leach (Brandur), Implementing Stripe-like Idempotency Keys in Postgres, 2017, https://brandur.org/idempotency-keys | verified |
| Personal data | Leach (Brandur), Soft deletion probably isn't worth it, 2022, https://brandur.org/soft-deletion | verified |
| | ICO, Data minimisation (UK GDPR guidance), current, https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/ | verified |
| | European Union, General Data Protection Regulation 2016/679, 2016, https://eur-lex.europa.eu/eli/reg/2016/679/oj | unverified |

40 data design sources, 38 verified, 2 unverified.

**Limit of this backing:** the checks covered that the page opened and that its title or author matched, plus a few passages read for the claims named in this section. They did not cover every claim inside each source. Provider documentation (Supabase, Firebase, Postgres, Unity, Unreal) changes quickly, so the role reads the live page when a limit, price or behaviour matters. Law and privacy rules differ by country and need a lawyer.

Review pass 2026-10-24: data design source count corrected to 40 (38 verified, 2 unverified) to match the table; "Backend & Integration Engineer" renamed "Backend Engineer" after the 2026-10-24 split (agent `backend-engineer`).
