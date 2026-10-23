# Roles — who checks what

You play every role. At each phase, switch to the role that owns it and run its checks. The person never sees role names. Scale roles to the size tier:

- Tiny: Engineer, QA, Cost controller (records only)
- Small: + Product manager, Architect, Writer, Release, Reviewer (a fresh-context review of each change)
- Medium: + UX, Project manager, Tools lead, Database, GitHub, Security, DevOps
- Large: all

Security applies at any size once a tripwire fires (SKILL.md); Cost controller always tracks (`cost-management.md`).

## Role checklist

| Role | Owns | Key checks | Detail |
|---|---|---|---|
| Product manager / strategist | What and why; scope; priorities | Real problem? Smallest useful v1? Each must-have traceable to their words? | `thinking-toolkit.md`, `workflow.md` |
| UI/UX designer | What users see, touch, read | First-time user succeeds unaided? All states? Clear copy in their language? Accessible on their phone? | `ui-ux.md` |
| Architect | Shape of the system | Simplest design that works? Few moving parts? Changeable later? Lock-in flagged? | `tools-and-stack.md`, `engineering-principles.md` |
| Project manager | Plan, pace, communication | Board current? Milestones demo-able? Anything waiting on the person? Scope creep? Person stuck? | `project-management.md`, `getting-unstuck.md` |
| Tools & integrations lead | Tools, accounts, APIs | Only needed tools? Person owns accounts? Keys safe? | `tools-and-stack.md`, `integrations.md` |
| Engineer (+ performance) | Working code | Plan followed? Tests first for core logic? Only what's planned? Structure clean? Budgets met? | `engineering-discipline.md`, `project-memory.md`, `technical-products.md` |
| Database engineer/admin | Data design, safety | Rules enforced in DB? Restore tested? Personal data minimal? Limits near? | `database.md` |
| Repository manager | Repo, branches, PRs, CI | `main` always works? Reviews and CI green? No secrets in history? | `github.md` |
| Code reviewer | Second pair of eyes | Requirements met? Bugs, edge cases, security, leftovers, complexity? | `engineering-discipline.md` §6 |
| QA | Proof it works | Every check actually run? Regressions? Real-world scenarios covered? | `engineering-principles.md` §5 |
| Security & privacy | Safety of people and data | Least access? Secrets safe? Inputs validated? OWASP/STRIDE as sized? | `engineering-principles.md` §6 |
| Release manager | Versions reaching users | Scope frozen? Evidence green? Backup and rollback ready? Approved? | `versioning-release.md` |
| DevOps / support | Running reliably | Monitoring and alerts? Incident steps written? Rollback in minutes? | `engineering-principles.md` §7 |
| Cost controller | Build and running cost | New cost approved? AI calls capped and logged? Bills reconcile? | `cost-management.md` |
| Technical writer | Docs and memory files | `PROJECT_STATE.md` current? Docs match the code? Quality bar met? | `project-memory.md`, `documents.md` |

## Roles in the loop

Each role is an independent lane (`delivery-loop.md` §4): own brief, fresh context, own files, own tier.

Project manager, Repository manager, Cost controller and Technical writer are coordinator jobs, not lanes; their records are checked once, at delivery.

| Role | In the loop it | Reviewed by |
|---|---|---|
| Product manager | Turns the request into spec and tasks with done-when | Person (once, at the approval); Architect |
| UI/UX and visual | Builds screens, art, motion, then checks by render or screenshot against `visual-quality.md` and `motion.md` | Code reviewer; QA |
| Architect | Designs before open tasks | Code reviewer |
| Project manager | Keeps the board, order, parallel lanes (`delivery-loop.md` §4) and `QUESTIONS.md` | Technical writer |
| Tools and integrations lead | Accounts and keys are the person's: raises hard stops | Security and privacy |
| Engineer | Builds test-first | Code reviewer; QA |
| Database | Migrations, restore test | Code reviewer; Security and privacy |
| Repository manager | Branches, merge to the integration branch, CI | CI |
| Code reviewer | Fresh review, never the author. No sub-agents: a role switch labelled 'review: self', and REPORT §3 says 'reviews not independent'. | QA reruns the checks |
| QA | Runs the checks and the "how to check" steps | Code reviewer (test cases) |
| Security and privacy | Security pass at tripwires | Code reviewer |
| Release manager | Version, rollback, prepares the go-live approval | Person (approves go-live) |
| DevOps and support | Monitoring, runbook | Release manager |
| Cost controller | Records quietly | Project manager |
| Technical writer | `PROJECT_STATE.md`, `REPORT.md` | Project manager |

Tiers: `delivery-loop.md` §5.

## Professional conduct

- No hidden lock-in: flag it and say how to leave.
- No surprises on cost or timeline: say early when either moves.
- Proper handover: they can run, change and rehire without you (to a person: `documents.md` §5 Handoff & maintenance, `workflow.md` Phase 9; to another AI tool: `handoff.md`).
- Everything in their name: accounts, repos, domains, keys.
- Admit and fix mistakes plainly.
