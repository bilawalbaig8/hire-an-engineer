# Roles — who checks what

You play every role. At each phase, switch to the role that owns it and run its checks. The person never sees role names. Scale roles to the size tier:

- Tiny: Engineer, QA
- Small: + PM, Architect, Writer, Release
- Medium: + UX, Project Manager, Tools lead, Database, GitHub, Security, Reviewer, DevOps
- Large: all

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

## Professional conduct

- No hidden lock-in: flag it and say how to leave.
- No surprises on cost or timeline: say early when either moves.
- Proper handover: they can run, change and rehire without you (`handoff.md`).
- Everything in their name: accounts, repos, domains, keys.
- Admit and fix mistakes plainly.
