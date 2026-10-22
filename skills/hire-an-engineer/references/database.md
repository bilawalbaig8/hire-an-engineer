# Database — design, setup and management

You are the database engineer and administrator. The person only knows "mera data". Your job: choose where it lives, design it properly, set it up, keep it correct, safe and backed up, and give them an easy way to see it.

---

## 1. Choosing where data lives

| Option | Good when | Watch out |
|---|---|---|
| None / files (CSV, JSON) | One-off scripts, single user, small data | No sharing, easy to lose |
| Browser storage | Personal single-device tools | Lost if browser cleared; not shared |
| Google Sheets / Airtable | Small team, they want to see/edit data directly, <~10k rows | Weak validation, concurrency, permissions |
| SQLite | Single-machine app/script needing real queries | Not for many simultaneous users over the web |
| **Supabase (Postgres)** | Multi-user web apps, login, relations — common pick for medium/large | Free plan limits, pausing of inactive projects and missing backups: check the current pricing page; set access rules |
| Firebase (Firestore) | Realtime/mobile-first apps, simple data shapes | Harder relational queries and reporting |
| Managed Postgres/MySQL | Large/custom systems | Needs more ops care |

Say it in their terms: "Data ek online database mein rahega, sirf aap aur staff login kar ke dekh sakenge, roz backup banega."

## 2. Designing the schema

From the brief and journeys, list the **things** the system remembers (entities) and the facts about each (fields).

Rules:
- One table per kind of thing (customers, orders, order_items, products).
- Every table: `id` (primary key), `created_at`, `updated_at`; add `created_by` when users matter.
- Relations via foreign keys (order_items.order_id → orders.id); draw an ERD.
- Normalise sensibly: don't repeat the same fact in two places (store product price on the product, copy it to the order item only as "price at time of order").
- Right types: numbers as numbers, money as integer minor units or decimal, dates as dates/timestamps with timezone, fixed choices as enums/check constraints (status: new/baking/ready/delivered/cancelled).
- Constraints do the guarding: NOT NULL for required fields, UNIQUE where duplicates are wrong (email, order number), CHECK for ranges (quantity > 0).
- Soft delete (`deleted_at`) when the person may want things back; hard delete for personal data on request.
- Naming: lowercase snake_case, plural tables, clear names (`delivery_date`, not `dd`).
- Keep only data the brief needs — especially personal data.

Show the person the data model in plain words with the ERD ("Har order mein customer ka naam, cheezein, quantity aur delivery date hogi") and confirm nothing they track is missing.

## 3. Data dictionary

A document (in the System Design Doc or `docs/design/data-dictionary.md`) listing every table and field:

| Table | Field | Type | Required | Meaning (plain) | Example | Rules |
|---|---|---|---|---|---|---|
| orders | delivery_date | date | yes | Kis din deliver karna hai | 2026-11-20 | Not in the past |

Keep it updated with every schema change.

## 4. Setting it up

- Create the database/project (via connector or guided), separate **test** and **live** for medium/large projects.
- Create schema with a migration script (never by clicking around in live), seed test data that looks realistic, and fake data only in test.
- Store connection strings/keys as secrets in hosting/GitHub — never in code or docs.
- Record in the Tools & Setup Guide: provider, project names, region, plan/cost, who owns the account, where backups go.
- SQLite: set `busy_timeout` and turn a lock timeout into a clear domain error. Test competing writes with two connections or threads, not only one connection.

## 5. Changing the schema (migrations)

- Every change is a numbered migration file in the repo (`migrations/003_add_delivery_date.sql`) — up and, where possible, down.
- Test on a copy/test database with realistic data first.
- Backup live before applying; no live migration without a tested restore or down migration (`versioning-release.md` §6). Apply during a quiet time. Verify after (row counts, app still works).
- Prefer additive, backward-compatible changes (add column → backfill → switch code → remove old later).
- Update the data dictionary, ERD and changelog.

## 6. Data quality and validation

- Validate on the screen (helpful messages) **and** in the database (constraints) — the screen can be bypassed, the database can't.
- Guard against duplicates (unique keys, "already exists" checks).
- For imports (CSV, old spreadsheets): clean on a copy, report what was fixed/skipped, compare row counts before and after.
- Add automated tests for the data rules.

## 7. Access and security

- Principle of least access: each user role sees/changes only what it needs; enforce in the database (e.g. Supabase row-level security policies), not only in the UI.
- Never expose admin/service keys to the browser.
- Personal data: collect the minimum, protect it, decide retention ("orders 2 saal tak rakhein, phir delete?"), support delete/export requests.
- Log important changes (who changed what, when) if the person needs history.
- Security checks go into the Test Plan (try reading another user's data — must fail).

## 8. Backups and restore

- Automatic backups on **if the plan includes them** (check; free plans often don't) **plus** your own scheduled export (e.g. nightly GitHub Action → CSV/SQL dump to their Drive or storage) for anything important.
- Backup before every release and every migration.
- **Test a restore** once before launch and after major changes — an untested backup isn't a backup.
- Write in the Handoff Guide: where backups are, how often, how to restore (step by step), who to contact.

## 9. Performance and growth

- Indexes on fields used to search, filter or sort often (delivery_date, customer_id, status).
- Paginate long lists; don't load everything at once.
- Watch size and free-tier limits; tell the person before costs change ("10,000 orders ke baad mahana kharcha aayega, takreeban …").
- Archive old data if it grows large.

## 10. Giving the person access to their data

Non-technical owners need to see and fix their data without SQL:
- An **admin screen** in the app (list, search, edit, export) for medium/large projects, or
- A read-only/editable view through the provider's table editor with a short guide, or
- A synced Google Sheet / scheduled export for reporting.
Always include **export to Excel/CSV** — it's their data.

## 11. Ongoing management

In the Handoff & Maintenance Guide, include a database section: provider and plan, ERD, data dictionary link, backup/restore steps, how to add a user/role, how to export, size and cost to watch, and the migration process for future developers. When the person comes back with "data galat dikh raha hai", treat it as an incident: root cause first, fix data on a copy, then apply with a backup.
