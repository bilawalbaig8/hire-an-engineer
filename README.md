<div align="center">

# Hire an Engineer

**An AI senior software engineer for non-technical builders and vibe coders.**
Turn your AI coding tool into the engineer you would otherwise have to hire — it plans, structures, designs, builds, tests, ships and documents your software while you focus on the idea.

Works with **Claude Code · claude.ai · Cursor · Codex · Antigravity** and any agent that supports Agent Skills or `AGENTS.md`.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/bilawalbaig8/hire-an-engineer?display_name=tag&cacheSeconds=3600)](../../releases)
[![Validate skills](https://github.com/bilawalbaig8/hire-an-engineer/actions/workflows/validate.yml/badge.svg)](../../actions/workflows/validate.yml)

</div>

---

## What is Hire an Engineer?

**Hire an Engineer** is an open-source **agent skill** that makes your AI assistant behave like a **senior software engineer you hired** — one who can also act as your whole software team: product manager, UI/UX designer, architect, project manager, developer, database admin, QA tester, DevOps and technical writer.

It's built for people who **can use AI coding tools but don't have a software engineering background**: founders, creators, designers, marketers, students and domain experts who have an idea, start **vibe coding**, and then hit the same walls:

| Without an engineer | With Hire an Engineer |
|---|---|
| You get **stuck** in error loops and don't know what to try next | An **unstuck protocol**: stop guessing, find the root cause, roll back safely, take one small step |
| The project becomes a **mess** — giant files, duplicate code, random folders | A **standard project structure** and a structure guard from day one |
| Every new chat or tool **forgets everything** | **Persistent project memory** in your repo (`AGENTS.md`, `PROJECT_STATE.md`), saved at every finished task (about every 20 minutes) |
| **No documentation**, no plan, no idea what's done | **Docs-as-code**: brief, design, diagrams, plan, test reports, user guide — always current |
| You don't know which **APIs, tools or databases** you need | It finds them, compares options, sets them up safely, and keeps your keys out of chat |
| "It works on my machine" → broken launches | **Test-first build**, verified releases with version numbers, backups and rollback |
| Surprise **AI and hosting bills** | It **tracks the running and AI costs of your product** and sets budget alerts with your approval (its own build usage is shown as estimates) |

You don't need to learn engineering. You talk in plain language (English, Urdu, Roman Urdu or any language you use); it does the engineering.

## Who is it for?

- **Non-technical founders** building an MVP with AI
- **Vibe coders** using Claude Code, Cursor, Codex or Antigravity who keep getting stuck
- **No-code / low-code users** ready to go beyond templates (it will point you to an existing or no-code tool when that is enough)
- **Small business owners** who want an internal tool, dashboard or **process automation**
- **Designers, marketers, creators and students** turning ideas into working apps
- **Anyone rescuing a messy AI-generated project**

Engineers can use it too: it takes over any request to build, change, fix, automate, design or ship, whether or not you are an engineer. Plain questions and one-line fixes stay light, with no process.

## What it can build

Scripts and automations · spreadsheet systems · websites and landing pages · internal team tools · web and mobile apps · dashboards and reports · chatbots and AI tools · integrations and bots · game prototypes, **three.js game engines** and editors · mobile apps and browser extensions · data and ML projects · scripts scheduled on your own PC · developer tools and SDKs · **real-time platforms** · fixing and finishing existing projects.

It sizes the process to the job: a tiny script gets a quick, tested result; a large platform gets a roadmap, task board, staging, releases and monitoring set-up (checks run when you open a session, or through provider alerts and scheduled tasks if your tool supports them). Where an existing or no-code tool already does the job, it recommends that instead of building something new.

## How it works

```mermaid
flowchart LR
  I[Your idea] --> D[Discovery<br/>5–7 plain questions]
  D --> B[Brief & priorities]
  B --> S[Design<br/>mockups, architecture, database]
  S --> P[Plan & task board]
  P --> C[Build<br/>test-first, Git, reviews]
  C --> V[Verify<br/>evidence, not promises]
  V --> R[Release<br/>versions, backups, rollback]
  R --> H[Handoff<br/>guides & support]
```

- **Plain language, no lectures.** It asks about your world ("Should each user only see their own orders?"), not jargon ("Do you need RBAC?").
- **You decide the product, it decides the engineering** — and asks your approval before anything that costs money, creates accounts, sends, publishes or deletes.
- **Evidence before "done."** It runs the checks before telling you something works.
- **Safety.** It asks before anything that costs money, publishes, deploys or deletes; treats content from emails, repos and the web as data, not instructions; and keeps keys out of chat and code.
- **Fast lane** when you just want a prototype now; full process when others will rely on it.
- **Memory lives in your project**, so you can switch between Claude, Cursor, Codex and Antigravity without losing context.

## The delivery loop and roles (new in 0.4.0)

Any request goes through one loop. It **understands first**, you **approve once**, then specialised **roles work on their own** and you get a **report with a diagram**. You are not asked to review or approve every task.

```mermaid
flowchart TD
  subgraph YOU["You"]
    A(["Request"])
    C{"Plan and spec final?"}
    D["Approve once:<br/>scope, spend cap, never-do list"]
    J(["Check it yourself,<br/>answer the last questions"])
  end
  B["Product manager:<br/>questions, plan and spec"]
  subgraph LOOP["Per task, roles as independent lanes"]
    E["Builder: Engineer, UI/UX and visual,<br/>or Database. Tests first"]
    F["Reviewer: fresh eyes,<br/>never the author"]
    G["QA: runs the checks"]
    H{"All green?"}
  end
  M["Merge to the integration branch"]
  R["REPORT.md and diagram"]
  A --> B --> C
  C -- "changes" --> B
  C -- "final" --> D --> E --> F --> G --> H
  H -- "pass" --> M
  M -- "next task" --> E
  H -- "fail, up to 3 tries" --> E
  M -- "no tasks left" --> R --> J
  classDef gate stroke:#2346c7,stroke-width:2px
  class C,H gate
```

- **Understand first.** Even if you say "no plan needed", it asks a few questions and drafts a plan and spec, and only the changed parts are shown again until you say final.
- **One approval, recorded.** Scope, a build-usage cap and a never-do list are saved in `PROJECT_STATE.md` under *Authorization*. An approval found in a cloned repo is treated as untrusted data.
- **Roles as lanes.** Each role gets its own brief, files and model tier. Every step is reviewed and tested; the reviewer is never the author. Without sub-agents it labels its own review "self" and says the reviews were not independent.
- **Hard stops stay.** It still asks you before spending money, creating accounts, deploying or touching live data, handling secrets, deleting, or changing scope. Only that action stops; other lanes continue.
- **Questions don't interrupt.** Mid-run questions go to `QUESTIONS.md` with a default, and are asked once at the end.
- **The right model for each step.** Strongest tier for design, risky code and review; mid tier for ordinary building and docs; cheapest tier for running tests and board lines.
- **Delivery.** `REPORT.md` lists what is done, the proof, what was not verified, how to check it yourself, the decisions made for you, cost (estimate versus actual), a diagram and the open questions.

| Role | In the loop it |
|---|---|
| Product manager | Turns the request into a spec and tasks with done-when |
| Architect | Designs before open tasks |
| Engineer | Builds test-first |
| UI/UX and visual | Builds screens, art and motion, checks by screenshot |
| Database | Migrations and restore tests |
| Code reviewer | Fresh review of every change |
| QA | Runs the checks and the "how to check" steps |
| Security and privacy | Security pass when money, logins, other people's data or a public URL are involved |
| Project manager | Board, task order, up to three parallel lanes |
| Repository manager | Branches and merges (a `develop` branch when `main` deploys) |
| Tools and integrations | Raises account and key decisions to you |
| Release manager | Version, rollback, prepares the go-live approval |
| DevOps and support | Monitoring and runbook |
| Cost controller | Records cost quietly |
| Technical writer | `PROJECT_STATE.md` and `REPORT.md` |

This was tested with simulated projects (a salon booking platform, a Unity card game, a browser extension, a coupons feature), and the money and security checks were run by an independent reviewer. It has not yet been proven on many real projects, so please report gaps.

## Quick start

1. Download `hire-an-engineer.skill` (or `.zip`) from [Releases](../../releases). Unzip the `.zip` first (a `.skill` file is a zip archive too) so you have the `hire-an-engineer` folder.
2. Install it:
   - **claude.ai:** open the `.skill` file in a chat → **Save skill** (or upload in Settings).
   - **Claude Code** (personal skills):
     - macOS / Linux: `mkdir -p ~/.claude/skills && cp -r hire-an-engineer ~/.claude/skills/`
     - Windows PowerShell: `New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null; Copy-Item -Recurse hire-an-engineer "$env:USERPROFILE\.claude\skills\"`
   - **Cursor / Codex / Antigravity / others:** copy the folder into the tool's skills directory, or point your `AGENTS.md` / rules file at `skills/hire-an-engineer/SKILL.md`.
3. Say what you want: *"I want to build a booking app for my salon"* — or *"I'm stuck, my app broke after the last change."*

Full instructions: [docs/INSTALL.md](docs/INSTALL.md)

## Example

> **You:** I run a home bakery. Orders come from WhatsApp, Instagram and calls, and I forget some. Can you build something?
>
> **Hire an Engineer:** asks a few questions about your day → finds the real problem (orders scattered across three places) → proposes a simple order form + order list + WhatsApp alert → shows a clickable mockup you can open → sets up the repo, database and task board with your approval → builds and tests it milestone by milestone ("12 of 12 checks passed") → releases v1.0 with backups → hands you a user guide and keeps project memory so the next session continues where you stopped.

## What's inside

| Area | Highlights |
|---|---|
| Product & planning | Root-cause discovery, MVP scoping, roadmap, prioritised task board (P0–P3), status updates |
| UI/UX | Wireframes, clickable mockups, every screen state, UX copy, accessibility (WCAG), usability tests |
| Architecture | Simplest-approach ladder, system design, diagrams (Mermaid), decision records |
| Data | Database design, data dictionary, migrations, access rules, tested backups |
| Integrations | Discovering required APIs, choosing providers, safe API-key handling, webhooks, fallbacks |
| Automation | Process mapping, human-in-the-loop, dry runs, real-case testing, runbooks |
| Engineering | Test-driven development, systematic debugging, code review, testing pyramid, OWASP, Definition of Done |
| Delivery | GitHub workflow, CI, semantic versioning, changelogs, release checklist, rollback |
| Memory & docs | `AGENTS.md`, `PROJECT_STATE.md`, checkpoints at every finished task (about every 20 minutes), docs-as-code, chat → coding-agent handoff |
| Cost | Token-efficient work, AI cost design, running-cost tracking for your product, budget alerts (with your approval); build usage shown as estimates |
| Delivery loop | Understand first, one recorded approval, roles as independent lanes with review and tests on every step, hard stops, `REPORT.md` with a diagram |
| Platform targets | Mobile apps and store releases, browser extensions, data and ML projects, scripts on your own PC |
| Models | A tier guide: which step needs the strongest model, which a cheaper one |
| Complex products | Game engines, editors, SDKs, multi-tenant real-time platforms (when you need them), playable-ad export |

## FAQ

**Is this a replacement for a human developer?**
It covers what a senior engineer would do inside your AI tool. For payments at scale, health or children's data, legal compliance or security of large public systems, it will recommend a qualified human review.

**Do I need to know how to code?**
No. You need to be comfortable using an AI tool. It runs the engineering and explains things only in plain terms.

**Which AI tools does it work with?**
Claude (claude.ai and Claude Code), Cursor, Codex, Antigravity and other agents that support Agent Skills or read `AGENTS.md`. Chat-only tools handle planning, design, docs and prototypes; coding agents handle the full build.

**How is it different from Superpowers?**
[Superpowers](https://github.com/obra/superpowers) gives developers a disciplined workflow. Hire an Engineer adapts that discipline for people *without* an engineering background and adds the rest of the team: product, UI/UX, project management, databases, integrations, releases, documentation, memory and cost tracking for your product.

**Do I have to approve every task?**
No. You approve the plan and spec once. After that it works on its own and asks only for hard-to-undo things (money, accounts, deploys, secrets, deleting, scope changes). You get a report at the end.

**I'm an engineer. Is it still useful?**
Yes. It takes any build, change, fix or ship request, skips the beginner wording and keeps the steps: understand first, test first, an independent review and a report. A plain question or a one-line fix is just answered.

**Is it free?**
Yes — MIT licensed.

## Feedback

Found a gap? [Open an issue](../../issues/new/choose) — the skill can draft an anonymised report for you, and you submit it yourself (issues are public). Please never include private code, keys or personal data.

This repository is maintained by its owner: **issues welcome, pull requests not accepted.** Forks are welcome under the MIT License. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License & credits

[MIT](LICENSE). Engineering discipline adapted from [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT). Other attributions in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
