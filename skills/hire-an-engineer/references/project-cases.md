# Project Cases — what each kind of project needs

Identify the case and the size early (end of discovery). They decide which roles are active, which documents to produce, and how much ceremony to use. Projects can combine cases.

## Contents
1. Size tiers
2. Project types
3. Special situations

---

## 1. Size tiers

| Size | Looks like | Roles active | Documents |
|---|---|---|---|
| **Tiny** | One script, one calculator, a formula; under a day | Engineer, QA | One short combined note: what it does, how to run, checks done; checklist instead of a board; version 1.0 noted |
| **Small** | Personal/single-user tool, a few screens, no shared data | + PM, Architect, Writer, Release | One combined document; simple task board; GitHub repo if code; versions + changelog |
| **Medium** | Team tool, shared data, login, a few integrations | + UX, Project Manager, Tools lead, Database, GitHub, Security, Reviewer, DevOps | Full pack; live board with priorities; PR workflow + CI; test & live environments; migrations; backups |
| **Large** | Public users, payments, personal data at scale, many integrations, mobile app | All roles incl. Production Support | Full pack, separate documents, roadmap of versions, branch protection, staging, release + monitoring plans |

When unsure, pick the smaller size and grow — never the reverse. The size also selects the process, principles and test types in `engineering-principles.md`.

## 2. Project types

| Type | Typical approach | Key roles & extra focus | Key tests |
|---|---|---|---|
| **Process automation** (repetitive task or workflow done by hand today: emails → sheet, invoices, reports, reminders, file handling) | Mapped first; no-code, Apps Script, Python, AI steps — see `process-automation.md` | PM (process mapping), Engineer, QA; human-in-the-loop, data safety (copies, dry-run) | 10–20 real past cases incl. awkward ones, exception paths, failure alerts, parallel run |
| **Calculator / small interactive tool** | Single HTML file | UX, Engineer, QA | Wrong inputs, phone screen, edge numbers |
| **Spreadsheet-based system** (tracker, inventory, CRM-lite) | Google Sheets + Apps Script / Airtable | BA (data model), Security (sharing), Writer | Many rows, two people editing, wrong entries |
| **Website / landing page** | Static site on Vercel/Netlify | UX, Writer, DevOps (domain) | All devices, links, forms, load speed |
| **Internal team tool / web app** | Web app + hosted DB/auth | All medium roles; permissions | Roles/permissions, concurrent edits, backups |
| **Public web app / SaaS** | Full stack, separate test & live | All roles; Security, DevOps, SRE | Security, load, payments in test mode, rollback |
| **Mobile app** | Mobile-friendly web app first; native only if needed | UX, DevOps (stores), Security | Devices, offline, store requirements |
| **Dashboard / analytics / report** | Sheet charts, Looker Studio, or HTML dashboard | BA (which numbers matter), Architect (data source) | Numbers match source, date ranges, empty data |
| **Chatbot / AI tool** | Script/app calling an AI API | Architect, Cost Controller (estimate, caps, usage log), Security (keys, data sent out), QA | Odd inputs, tokens and cost per call, limits hit, wrong-answer handling |
| **Integration / bot** (WhatsApp, Slack, email, sheets syncing) | Zapier/Make or small script | Architect (flows), SRE (failures) | What if one side is down, duplicates, retries |
| **Game prototype / interactive experience** | HTML5 or engine of choice | UX, Engineer, QA (feel) | Different devices, restart, scoring edge cases |
| **Data migration / cleanup** | Script on copies | Engineer, QA, Security | Row counts match, nothing lost, backup first |
| **Game engine / editor / creation tool** | Build on three.js + proven libraries; niche-focused | Architect, Performance, QA, Writer — read `technical-products.md` | Deterministic sim, visual regression, perf benchmarks, export validation, device matrix |
| **Developer tool** (SDK, library, API, CLI, plugin) | Typed package + docs + examples | Architect (API design), Writer, Release (strict semver) | API compatibility, docs examples run, integration with sample projects |
| **Platform** (Slack-like, collaboration, marketplace, multi-tenant SaaS) | Managed real-time + DB with tenant isolation | All roles; Security, DevOps, Cost — read `technical-products.md` | Tenant isolation, real-time reconnects, load, permissions, abuse |

## 3. Special situations

**Existing software / they already have something**
- Start by understanding what exists (files, links, screenshots). Don't redesign what works.
- Follow its existing patterns. Add a test around current behaviour before changing it.
- Produce a short "current state" section in the design doc.

**A bug in something already built**
- Systematic debugging (engineering-discipline §4). Reproduce → cause → test → fix → verify → short incident note in the Handoff Guide.

**They want to change direction mid-project**
- Project Manager hat: show the impact (time, what gets thrown away), update brief and plan, bump document versions, then continue.

**They want to hire a developer later**
- Make the technical sections thorough: setup from zero, architecture, decision log, how to run tests. The pack becomes the developer's onboarding.

**Idea is not a software problem**
- Say so. If a process change, an existing app, or a spreadsheet solves it, recommend that — even if nothing gets built.

**Something would be illegal, unsafe or harmful**
- Don't build it. Offer a safe alternative where one exists.
