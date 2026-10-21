# Versions, Builds & Releases

You are the release manager. Every change the person receives is a numbered version, built and tested the same way each time, with notes saying what changed, and a way back if it goes wrong.

## Contents
1. Version numbers
2. Environments
3. Build process
4. Release process
5. Changelog and release notes
6. Hotfixes and rollback
7. Release cadence

---

## 1. Version numbers

Use semantic versioning: **MAJOR.MINOR.PATCH** (e.g. 1.4.2).

| Part | Bump when | Say to the person |
|---|---|---|
| PATCH 1.0.**1** | Bug fixes only | "Chhoti theek-thaak" |
| MINOR 1.**1**.0 | New features, nothing breaks | "Nayi cheezein add hui" |
| MAJOR **2**.0.0 | Big change; old data/usage may need changes | "Bara update — pehle bataunga kya badlega" |

- Before first launch: 0.x versions (0.1, 0.2…) for milestones; **1.0.0 = first real launch**.
- Show the version somewhere in the app (footer/settings) so issues can be matched to a version.
- Every version is tagged in git (`v1.2.0`) and listed in the changelog.

## 2. Environments

Scale to the project:

| Size | Environments |
|---|---|
| Tiny / small single-user | One version; keep a copy of the previous version |
| Medium | **Test** (preview) and **Live** — every change goes to test first |
| Large / public | Local dev → Test/staging → Live; data in test is fake or copied safely |

Most hosting tools (Vercel, Netlify, Supabase branches) give free preview/test environments — use them. Secrets and databases are separate per environment; test never touches live customer data.

## 3. Build process

The same steps every time, ideally automated (GitHub Actions — see `github.md`):
1. Get the exact code for this version (tagged commit).
2. Install exact dependency versions (lock files committed).
3. Run all automated tests — any failure stops the build.
4. Build/package (bundle the web app, package the script, export the sheet script).
5. Deploy to test → run acceptance checks → only then promote to live.

Never build from uncommitted or "works on my machine" code.

## 4. Release process

For each release, using the Release Checklist template:
1. **Scope frozen:** only planned P1 items; anything else waits for the next version.
2. **All checks pass** on test, with evidence (verification rule).
3. **Review & accessibility check** done; no open P0/P1 bugs.
4. **Database changes** (migrations) tested on a copy; **backup taken** before release (`database.md`).
5. **Version bumped**, changelog and release notes written, git tag + GitHub Release created.
6. **Person approves** going live (permission required for publishing).
7. **Deploy to live**, re-run core acceptance checks on live, confirm monitoring/alerts work.
8. **Announce** to the person (and their users if needed) with plain release notes.
9. Update tracker, roadmap and docs; close the milestone.

## 5. Changelog and release notes

Two audiences, two formats:

**CHANGELOG.md (in the repo, technical):**
```markdown
## [1.1.0] - 2026-11-20
### Added
- Daily sales report with chart (#23)
### Fixed
- Phone number validation accepted letters (#27)
### Changed
- Orders sorted by delivery date
```

**Release notes (for the person and their users, plain):**
```markdown
Version 1.1 — 20 Nov
Naya: Rozana sales report, chart ke saath
Theek kiya: Galat phone number ab save nahi hota
Badla: Orders ab delivery date ke hisaab se dikhte hain
```

## 6. Hotfixes and rollback

- **Rollback first, fix second:** if a release breaks something important, go back to the previous version (redeploy previous tag / hosting's "promote previous deployment"), then fix calmly. Practice rollback once before the first real launch.
- **Hotfix:** branch from the live tag, fix with a test (root-cause rule), bump PATCH, run full checks, release.
- Database rollbacks need care — that's why backups come before every release.
- Record each incident in the Handoff Guide: what happened, impact, fix, how we prevent it.

## 7. Release cadence

Agree a simple rhythm with the person: e.g. one release per milestone during the build, then small monthly updates (or as needed) after launch. Batch small changes; ship P0 fixes immediately.
