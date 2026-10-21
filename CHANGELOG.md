# Changelog

All notable changes per skill. Versions follow semantic versioning; tags are `<skill-name>-v<version>`.

## hire-an-engineer

### [0.1.0] - 2026-10-21
- First public release: full-team workflow, project memory (AGENTS.md, PROJECT_STATE.md, ~20-min checkpoints), getting-unstuck protocol, UI/UX, database, integrations, process automation, technical products, cost tracking, router-based SKILL.md.
- Tuned from a pre-release evaluation (5 test cases): doesn't take over routine or one-off questions; replies in the language of the person's messages; first-reply recipe (size guess picks the lane, show something visible with the questions, deliver requested plans/tests first); minimum files per size with templates in `templates.md`; rescue lane for stuck projects; lighter discovery for single-step automations; privacy prompts for personal financial/health data.
- Hardened from a thinking-model review (pre-mortem, red team, via negativa, map–territory): outside content is data, never instructions; secrets never printed and kept out of rescue snapshots; approval defined (one action, own message, explicit yes) and extended to deploys, force-push, DNS, live config, migrations and rollback; tripwires force the normal lane; test-first for core logic in every lane; checkpoints per finished task, never stash, PROJECT_STATE trimming; chat-only resume; project-at-a-glance page; build-cost estimates; leaner references (new `handoff.md`, `gap-reports.md`).
