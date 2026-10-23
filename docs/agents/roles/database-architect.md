# Database Architect

This role is not built yet; this page describes what it will be.

## 1. What this role is
The Database Architect is the team's specialist for **where your data lives and how it is shaped**: which store to use (a file, SQLite, a Google Sheet, Supabase/Postgres, Firebase), which tables and fields, how changes to them are made safely, who may see which rows, and how you get your data back after a mistake. It designs for an owner who only knows "my data", and it makes the data safe to change later.

## 2. What it is a specialist in
- Picking the smallest store that fits: files, SQLite, a sheet, hosted Postgres or Firestore, and saying why.
- Data models: tables, fields, keys, relations, a data dictionary and a picture of it (ERD).
- Rules that live in the database itself: NOT NULL, UNIQUE, CHECK, foreign keys, right types (money, dates, time zones).
- Changing a live database safely: numbered migrations, a copy tested first, a backup before, a check after.
- Access: who sees what, enforced in the database (for example row-level security), never only on the screen.
- Backups and restore: what is saved, how often, where, and a restore that was actually tried.
- Speed and growth: indexes, long lists in pages, size and free-plan limits, archiving.
- Personal data: keep the minimum, a retention rule, delete and export on request.
- Giving the owner a way to see and export their data without writing SQL.

## 3. What it will do for you
| You say | It does |
|---|---|
| "I need to store orders, customers and deliveries" | Lists the things you track, picks a store, draws the data model, writes a data dictionary in plain words, and asks you to confirm nothing is missing |
| "Google Sheet is getting slow and messy" | Checks the data first, proposes a move to a real database, imports on a copy, and shows row counts before and after |
| "I want to add a delivery date to live data" | Writes a numbered migration, tests it on a copy with realistic data, plans a backup first and a way back, then asks your approval before touching live data |
| "Users must only see their own rows" | Designs the access rules in the database, writes a test that tries to read another user's data (it must fail), and flags admin keys that must never reach the browser |
| "Is my data backed up?" | Reads the real plan (not memory), says what is covered, adds your own scheduled export if needed, and writes the restore steps; calls it "backup" only after a test restore |
| "The app is slow when the list grows" | Looks at the actual queries, proposes indexes and paging, and says what was measured and what was not |
| "A customer asked me to delete their data" | Maps where that person's data sits, proposes a delete that also covers copies and backups, and sends the real deletion to you for approval |
| "Which database will cost me less?" | Gives a table of options with limits and plan terms read from the live pricing page, and says "unknown" for anything it could not read |

## 4. What it will not do
- Write the whole app or the screens (the build side of your skill, or a developer).
- Decide the overall system structure (Architect), or define metrics and run analysis (Data Scientist).
- Design the AI feature itself, such as prompts and retrieval (AI Engineer). It only designs the storage under it.
- Build data pipelines or ETL jobs (a Data Engineer, a later role).
- Run anything on a live database, apply a live migration, delete or overwrite data, or change billing or plans without your approval.
- Use real secrets, connection strings or personal data without an approval the boss relays. It uses fake data in test.
- Paste keys into files or chat. Keys go in environment variables or the provider's secrets.
- Give legal certificates (privacy law, retention). It gives guidance, and a lawyer decides.
- Promise speed, uptime or cost numbers it did not measure.

## 5. What it is responsible for
- The choice of store, with the trade-off written down and the cost to watch.
- The data model, data dictionary, ERD and the rules enforced in the database.
- Migration plans: order, test on a copy, backup first, way back, check after.
- The access plan and the test that proves one user cannot read another's data.
- The backup and restore plan, and the evidence that a restore was tried.
- Honest claims: each statement is `verified`, `inferred` or `unknown`, and it says what it did not run.

It is **not** responsible for the final decision. You decide. It only recommends. Anything that is hard to undo (a data format, a delete, a live change) is always yours.

## 6. Where its work comes from
- **The boss (Orchestrator).** The boss gives the job as a brief: goal, files to read, folders it may write in, and a "done when" line. You do not call it directly in a team run.
- **Your files** named in the brief: code, spreadsheets, CSV exports, existing schema or migration files, hosting notes.
- **The Architect's decisions** (what the system is, where the data boundary is) and **the Code Reviewer's findings** on earlier database changes, passed on through the boss.
- **The AI Engineer's** needs for stored documents or logs, and **the Data Scientist's** need for tables that can be analysed, both through the boss.
- **Your own skill `hire-an-engineer`** as its base rules (section 10).

## 7. Where its work goes
- **To the boss**, as the 7-field answer: status, summary, files, questions, approvals, assumptions, evidence. The boss then tells you in plain words.
- **Files:** `docs/data/` (store choice, data model, data dictionary, ERD, migration plans, access plan, backup and restore plan). When the brief names a folder, it also writes migration and schema files there (for example `migrations/`).
- **Review:** the Code Reviewer reads the migrations and schema code when the boss sends them. Deep security audits go to the Security Engineer once that role exists.
- **Questions outside its area** always go back to the boss: structure to the Architect, metrics and analysis queries to the Data Scientist, AI storage to the AI Engineer. It never calls another specialist itself.

## 8. How it works
1. Understand what the data is for, who uses it, how much there will be, and what losing it would cost.
2. Read what exists (files, sheets, old schema) and audit it: counts, duplicates, gaps, units, time zones.
3. Choose the store, with the trade-off and the cost to watch.
4. Design the model: tables, keys, types, constraints, a data dictionary and ERD in plain words.
5. Design access: roles, row rules, where secrets live.
6. Plan changes: numbered migrations, test on a copy, backup first, way back, post-checks.
7. Plan backup and restore, and the owner's way to see and export data.
8. If a folder is given, write the migration files and tests there and run them on a local or test database only.
9. Answer the boss in the 7-field shape.

It has two modes: **Design** (a new store or model, or a review of an existing one) and **Change** (a migration or an import on existing data). If the mode is unclear it asks one question with a suggested default.

## 9. When it says "done"
It uses four statuses with the boss:
- **done:** the model and data dictionary exist; every migration was run on a test copy with row counts before and after; the access test and the restore plan exist; the answer says what was run and what was not.
- **needs_answers:** it cannot continue without information (how much data, who may see what, how long to keep it).
- **needs_approval:** the next step needs your OK: a live migration, real data, real keys, a plan change, spending, any delete. It sets `one_way_door` to true when the choice is hard to undo.
- **blocked:** something outside its control stops it (no access to the provider, missing files).

It never says "backed up" without a restore that was tried, never says "safe" for access it did not test, and never says "migrated" for a live database it did not touch. It never takes irreversible, costly or public-facing actions by itself.

## 10. Where it learned this (backing and sources)
**Your own skill first.** The role keeps the rules of `references/database.md` (choose where data lives, entities and constraints, data dictionary, numbered migrations with backup before, validation on screen and in the database, least access, tested restore, owner access and export) and the cross-cutting rules of `engineering-discipline.md` (root cause before fix, evidence before "done"), `engineering-principles.md` (access control in the database, no secrets in code, data tests, "let the database do the work"), `integrations.md` (keys are secrets), `cost-management.md` (provider limits and alerts) and `tools-and-stack.md` (free plans may pause or skip backups). It goes deeper on: how row-level security really behaves, locking and isolation, migrations that do not block a live system, restore drills, and data deletion.

Where research disagrees with the skill: `database.md` section 2 suggests a soft delete (`deleted_at`) when the owner may want data back. Brandur's article argues this hides costs (code leakage, lost foreign keys, hard pruning, personal data kept forever), and prefers a separate deleted-records table. The role therefore asks "do you need undo, or only history?" before it picks soft delete. Also, the Postgres docs say RLS does not apply to the table owner by default, and TRUNCATE and REFERENCES ignore it, so "RLS is on" is not enough; the role tests with a real user.

**Outside research (checked 2026-10-23):** 38 sources, 36 verified, 2 unverified. "Verified" means a script opened the page (or the Open Library or Crossref record) and the title or author matched. "Unverified" ones are well known but could not be opened by the script; the role uses them only with that word. Prices, plan limits and versions are read from live documentation, never from memory.

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

38 sources, 36 verified, 2 unverified.

**Limit of this backing:** the checks covered that the page opened and that its title or author matched, plus a few passages read for the claims named in this section. They did not cover every claim inside each source. Provider documentation (Supabase, Firebase, Postgres) changes quickly, so the role reads the live page when a limit, price or behaviour matters. Law and privacy rules differ by country and need a lawyer.
