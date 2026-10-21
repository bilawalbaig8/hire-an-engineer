# hire-an-engineer — Agent Instructions

## What this is
Open-source skills for AI agents, maintained by the owner only. Each skill lives in `skills/<name>/` (SKILL.md + references/).

## Always
- Start: read this file and PROJECT_STATE.md. End (and every ~20 min of work): update PROJECT_STATE.md and commit.
- Run `python scripts/validate_skills.py` before committing.
- Keep SKILL.md lean (router + core rules); details go in references/. Description ≤ 1024 chars.
- Every change: CHANGELOG entry; link the issue (`Fixes #n`).
- Credit adapted sources in THIRD_PARTY_NOTICES.md.

## Release
Tag `<skill-name>-v<version>` → GitHub Action validates, packages, and publishes a release.

## Folder map
- `skills/` — published skills
- `evals/` — test prompts per skill
- `templates/skill-template/` — starting point for new skills
- `scripts/` — validate, package, labels, owner setup
- `docs/` — install and owner setup
- `.github/` — issue forms, triage, validation, release workflows
