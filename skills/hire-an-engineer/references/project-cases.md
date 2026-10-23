# Project Cases — what each kind of project needs

Identify the case and the size early (end of discovery). They decide which documents to produce and how much ceremony to use (roles per size: `roles.md`). Projects can combine cases.

Whatever the size: other people's personal data, money, login, public URL or any deploy → normal lane + security pass (SKILL.md).

## 1. Size tiers

| Size | Looks like | Documents |
|---|---|---|
| **Tiny** | One script, one calculator, a formula; under a day | the Tiny file list in `project-memory.md` §1; checklist instead of a board; first real launch = 1.0.0 (`versioning-release.md`) |
| **Small** | Personal/single-user tool, a few screens, no shared data | One combined document; simple task board; GitHub repo if code; versions + changelog |
| **Medium** | Team tool, shared data, login, a few integrations | Full pack; live board with priorities; PR workflow + CI; test & live environments; migrations; backups |
| **Large** | Public users, payments, personal data at scale, many integrations, mobile app | Full pack, separate documents, roadmap of versions, branch protection, staging, release + monitoring plans |

Guess the size from the first message to pick a lane; confirm or change it at the end of discovery. When unsure, pick the smaller size and grow — never the reverse. The size also selects the process, principles and test types in `engineering-principles.md`.

## 2. Project types

| Type | Typical approach | Key tests |
|---|---|---|
| **Process automation** (repetitive task or workflow done by hand today: emails → sheet, invoices, reports, reminders, file handling) | Mapped first; no-code, Apps Script, Python, AI steps — see `process-automation.md` | 10–20 real past cases incl. awkward ones, exception paths, failure alerts, parallel run |
| **Calculator / small interactive tool** | Single HTML file | Wrong inputs, phone screen, edge numbers |
| **Spreadsheet-based system** (tracker, inventory, CRM-lite) | Google Sheets + Apps Script / Airtable | Many rows, two people editing, wrong entries |
| **Website / landing page** | Static site on Vercel/Netlify | All devices, links, forms, load speed |
| **Internal team tool / web app** | Web app + hosted DB/auth | Roles/permissions, concurrent edits, backups |
| **Public web app / SaaS** | Full stack, separate test & live | Security, load, payments in test mode, rollback |
| **Mobile app** | Mobile-friendly web app first; native only if needed (`platform-targets.md` §1) | Devices, offline, store requirements |
| **Dashboard / analytics / report** | Sheet charts, Looker Studio, or HTML dashboard | Numbers match source, date ranges, empty data |
| **Chatbot / AI tool** | Script/app calling an AI API | Odd inputs, tokens and cost per call, limits hit, wrong-answer handling |
| **Integration / bot** (WhatsApp, Slack, email, sheets syncing) | Zapier/Make or small script | What if one side is down, duplicates, retries |
| **Game prototype / interactive experience** | HTML5 or engine of choice | Different devices, restart, scoring edge cases |
| **Data migration / cleanup** | Script on copies | Row counts match, nothing lost, backup first |
| **Browser extension; data analysis / ML; script on their own PC** | See `platform-targets.md` §2–4 | Real pages; no leakage; scheduled run and logs |

Game engines, editors, developer tools (SDK/library/API/CLI), platforms (multi-tenant, marketplace): `technical-products.md`.

## 3. Special situations

- **Existing software:** understand what exists first, follow its patterns, test current behaviour before changing it (`getting-unstuck.md` §4 rescue).
- **Bug in something built:** `engineering-discipline.md` §4.
- **Direction change mid-project:** show the impact, update brief and plan, then continue (`project-management.md` §7).
- **Hiring a developer later:** make the technical sections thorough (`documents.md`).
- **Not a software problem:** say so; recommend the simpler fix.
- **Illegal, unsafe or harmful:** don't build it; offer a safe alternative.
