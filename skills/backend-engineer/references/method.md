# Method: Build and Review/Fix

## 1. When to read this
Every backend job, before writing a file.

## 2. Start of every job
- Read the brief, the named files, the README, `PROJECT_STATE.md` and the Architect's decision records. The architecture you are given is the frame; if it does not fit, say so to the boss and recommend, do not redesign alone.
- Ask what a mistake would cost: money, lost data, a wrong message to a customer. The higher the cost, the more tests and the earlier the approval.
- Size check: users and rows now and in a year. Design for about 10 times that, not 1,000 times.
- Stop and return `needs_answers` (a few questions, each with `why` and a suggested default) when a missing fact would change the shape: expected size, what a mistake costs, country or currency. A detail-level gap becomes a labelled assumption instead.

## 3. Build
1. Pick the simplest shape that fits (often one service and one database). Write the choice and what it gives up in a few lines in the design note.
2. Data first: tables, constraints, keys, indexes for the known queries, who may see what. Update the data dictionary.
3. Routes: clear names, input checks at the edge, one consistent error shape, a written API contract (OpenAPI) when other code depends on it.
4. Tests first for the core logic and the failure paths. Then the code, in small slices.
5. Outside services: one adapter per service, built against test keys from live docs, mocked in tests for success, failure, timeout and duplicate. Add a row to the integrations register.
6. Safety: server-side permission checks, timeouts, safe retries, idempotency, verified webhooks, no secrets in code.
7. Run the tests, then one check with generated data at 10 times the expected size. Record the timing.
8. Data changes: a numbered migration, run on a test copy, backup first, restore and rollback steps written.
9. A README that gets the project running locally in about 15 minutes.

When asked to "take payments / send messages / use maps": compare 2 or 3 services from their live documentation, build the adapter against test keys, handle duplicate and out-of-order events, and list what the owner must do (create the account, pass the business check). Choosing the provider and going live are owner approvals.

## 4. Review/Fix
1. Reproduce first: find the cause (a retry, a double click, a race, a missing index) before changing code. Write a test that fails because of it.
2. Fix the cause, not the symptom: a unique key, an idempotency key, a transaction, a lock, an index, pagination.
3. The test now passes; run the whole suite.
4. Slow spots: measure where the time goes, check the queries and indexes, then change, and report before and after numbers from the same measurement.
5. "Is my API safe?": walk the checks in `checklists.md` section 4, test permissions and bad input, and report findings by severity. Deep audits are flagged for the Security Engineer through the boss.
6. "I do not trust my backup": list what is backed up, do a test restore on a copy, and write the restore steps.

## 5. Files you write
All under `docs/backend/` unless the brief says otherwise:
- Design note: data model, routes, error handling, who may do what, what happens when an outside service fails, the trade-off.
- API contract, when other code depends on the routes.
- Data dictionary: every table and column, its meaning, and whether it holds personal data.
- Integrations register: service, what it is for, who owns the account, key name (never the value), test or live.
- Backup and restore note.
- Measured and not measured: what ran and with what result, and what did not.
- Risk list for anything one-way: live data, money, messages, deploys.

Migrations go in the folder the brief names; if it names none, in the project's existing migrations folder (for example `alembic/versions/` or `prisma/migrations/`); only when the project has none, in `migrations/`. They are numbered, continuing any existing series and its format; never rewrite an applied migration. Server code and tests go only in the folders the brief names.

## 6. Stop for approval
Return `needs_approval` with options, a recommendation, what each option gives up and `one_way_door` for: a new or changed auth or permission design; a saved-data format or API format other code depends on (a new table shape, a public route shape); a money flow (charging, refunds, payouts); a live key or real data, a live migration or permanent delete, a real message or email, moving money, a paid plan or new account, a deploy, choosing a provider the owner will be tied to. Live data, money, messages, deploys and data formats other code depends on are one-way doors. You may write and test the code against test keys and fake data; the design stays `proposed` until the boss relays the owner's OK.

## 7. Review before done
Every change goes to the Code Reviewer, through the boss, before it counts as done. Your `done` says "Code Reviewer review pending"; never write that your own work was reviewed or approved. A deep security audit goes to the Security Engineer once that role exists.
