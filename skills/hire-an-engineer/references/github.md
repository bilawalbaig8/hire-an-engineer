# GitHub — setup and management

GitHub is where the project's code, history, tasks and releases live. You run it; the person never needs to touch git. To them it's "aap ke software ki safe jagah, har version ke saath".

---

## 1. When to use GitHub

| Project | GitHub? |
|---|---|
| Any code-based project (script, web app, site, bot) | **Yes** — private repo by default |
| Spreadsheet + Apps Script | Recommended for the script (clasp), optional otherwise |
| Pure no-code tool | No; keep docs in their docs tool |

The person owns the account and the repo (create it under their account or organisation). You may be added as a collaborator via connector/tool access; never hold the only copy.

## 2. Setting up the repository

- **Private** unless the person wants it public.
- Name: short, lowercase, hyphens (`bakery-orders`).
- Files from day one: minimum files per project size are in `project-memory.md` §1. `.gitignore` always excludes secrets (`.env`), build output, OS junk.
- Default branch `main`; enable branch protection on `main` for medium/large projects (no direct pushes, checks must pass).

Folder structure follows the file map from the implementation plan; keep it flat and obvious.

## 3. Day-to-day workflow

Simple, not enterprise:
- `main` is always working and deployable.
- One short-lived branch per task or small group: `feat/order-form`, `fix/phone-validation`, `docs/user-guide`.
- Small commits with clear messages (conventional style):
  `feat: add order form`, `fix: reject letters in phone number`, `test: …`, `docs: …`, `chore: …`
- Commit after each passing test step (TDD cycle); never commit secrets or failing tests to `main`.
- Merge via pull request; delete the branch after merge.
- Tiny single-person projects may commit straight to `main` — but still small commits, tests passing, tags for versions.

## 4. Issues, labels, milestones and Projects board

`project-management.md` decides where the board lives. When it's GitHub:
- **Issues** = tasks and bugs, using the task anatomy (title, why, done-when, priority).
- **Labels:** `P0`–`P3`, `feature`, `bug`, `design`, `docs`, `test`, `chore`, `needs-owner` (waiting on the person), `blocked`.
- **Milestones** = releases/milestones with due dates (`v1.0 — Launch`).
- **Projects board** = the task board (Backlog / To do / In progress / Review / Done) with priority and milestone fields. Share the board link with the person — they can watch progress without understanding code.
- Issue templates for bug reports so the person (or their users) can report problems in plain language: what happened, what they expected, steps, screenshot, device.

## 5. Pull requests and reviews

- One PR per task/feature; description: what, why, linked issue (`Closes #14`), how it was tested, screenshots for UI changes.
- Run the Code Reviewer role on every PR (reviewer agent if available) — against the brief, design and checks in `roles.md`.
- Merge only when checks are green and review issues are fixed.

## 6. Automation (GitHub Actions)

Add as the project warrants:
- **CI on every push/PR:** install, lint, run all tests. Red = no merge.
- **Preview deploys:** hosting integration (Vercel/Netlify) gives every PR a test link — share with the person for UI approval.
- **Deploy on release:** tag `v*` → build → deploy to live. If hosting auto-deploys a branch, merging to it is a live release: release approval (SKILL.md rule 2).
- **Scheduled jobs:** nightly database backup, data exports, dependency checks.
- **Dependabot:** the person can't review these. You review and merge only after CI is green and a changelog check; major-version bumps need their OK.

Keep workflows short and commented; record them in the Handoff Guide.

## 7. Releases and tags

- Every release = git tag `vX.Y.Z` + GitHub Release with notes (from the changelog) and any built files attached.
- Use releases as the rollback points (`versioning-release.md`).

## 8. Security and access

- Secrets only in GitHub Actions secrets / hosting env vars — never in code, issues, docs or commits. If one is committed, rotate it immediately (removing it from history isn't enough).
- Enable secret scanning and Dependabot alerts.
- Least access: collaborators only as needed; remove access when people leave.
- The person enables 2-factor auth on their account (guide them; never handle their codes).
- The repo is also a backup of the code; database backups are separate (`database.md`).

## 9. How you operate it

In order of preference:
1. Use available tools directly (git in a coding agent or terminal, a GitHub connector or CLI) — create repo, branches, commits, issues, board, PRs, releases. Approvals follow SKILL.md rule 2; also ask before making the repo public (it exposes all history and docs) or adding collaborators.
2. If you can't access GitHub, prepare everything (files, issue list as CSV/markdown, workflow files) and guide the person click by click through repo creation and upload — or recommend continuing the build in a coding agent (CLI or IDE) for full automation.

Always report in plain terms: "Version 1.1 GitHub pe save ho gaya, yeh raha link."
