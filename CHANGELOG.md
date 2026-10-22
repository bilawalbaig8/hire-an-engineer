# Changelog

All notable changes per skill. Versions follow semantic versioning; tags are `<skill-name>-v<version>`.

## hire-an-engineer

### [0.2.0] - 2026-10-22
- Thinking toolkit: one-way vs two-way doors, physics-or-convention, attacker's view for security, look-up/estimate/buffer for numbers, and a new debugging and performance section (check the real code, simplest first, competing hypotheses, find the bottleneck); router sends bugs with unclear causes, security, estimates and slowness there. Adapted from cc-thinking-skills.
- New `engineering-principles.md` §10 Data and performance choices: real data size and 10× design, maps for lookups, no nested loops on large data, built-in sort/search, let the database filter/sort/paginate, structures by data shape (trees/graphs as rows), loops instead of deep recursion, cache with expiry, realistic-size tests; "10× data" question added to every code review.
- New `engineering-principles.md` §11 Runtime performance: browser, devices, OS: budgets (LCP, INP, CLS, memory, idle CPU) measured on weak devices; browser rules (images, JS, fonts, workers, network, long lists, memory leaks, device matrix) and OS/desktop/script rules (streaming, non-blocking work, idle, cleanup, cross-platform paths, concurrency).
- Security: risks specific to AI-built projects in §6 — prompt injection in AI features, checking new packages before install (hallucinated/typosquatted names), local pre-commit secret checks and leaked-key handling.
- Diagrams: new `documents.md` §7 Diagram quality (draw only when it beats words, type by content, ≤9 boxes/≤12 arrows, 1–2 highlights, clean connectors, no generic AI look, captions, phone-readable, redraw rules, pre-show check); Mermaid stays the editable source, a dedicated diagram skill (e.g. diagram-design) for diagrams to present. `plain-language.md` and SKILL.md: explain flows, options, plans and designs to the person with a simple diagram in the reply, with fallbacks per environment. Adapted from diagram-design.
- New `ai-agents.md` for AI features, workflows and agents inside the product: simplest shape first (code → one AI step → workflow → agent), hard stops in code (steps, time, spend, retries, kill switch), agent-friendly tool design, least access with draft-don't-do approvals and a trust ladder, state outside the prompt, evals before launch with a separate checker, run logs, provider-failure fallbacks and a pre-launch checklist; routed from SKILL.md and `process-automation.md`. Informed by readings in awesome-harness-engineering.
- `ai-agents.md` §5: layered summaries for large memory/knowledge (one-line summary and overview per folder, full file on demand) and search scoped to the current project/user/folder. Idea from OpenViking.
- `ai-agents.md` §5: memory lifecycle (source, date, confidence; newer facts retire contradicting ones; stale entries reviewed on a schedule; no auto-capture of secrets or personal data) — idea from agentmemory; facts-need-sources rule for AI research and reports (every claim cited, inferences labelled, code checks cited sources were read) — idea from scientific-agent-skills. Pre-launch checklist and `documents.md` §2 quality bar updated to match.

### [0.1.0] - 2026-10-21
- First public release: full-team workflow, project memory (AGENTS.md, PROJECT_STATE.md, ~20-min checkpoints), getting-unstuck protocol, UI/UX, database, integrations, process automation, technical products, cost tracking, router-based SKILL.md.
- Tuned from a pre-release evaluation (5 test cases): doesn't take over routine or one-off questions; replies in the language of the person's messages; first-reply recipe (size guess picks the lane, show something visible with the questions, deliver requested plans/tests first); minimum files per size with templates in `templates.md`; rescue lane for stuck projects; lighter discovery for single-step automations; privacy prompts for personal financial/health data.
- Hardened from a thinking-model review (pre-mortem, red team, via negativa, map–territory): outside content is data, never instructions; secrets never printed and kept out of rescue snapshots; approval defined (one action, own message, explicit yes) and extended to deploys, force-push, DNS, live config, migrations and rollback; tripwires force the normal lane; test-first for core logic in every lane; checkpoints per finished task, never stash, PROJECT_STATE trimming; chat-only resume; project-at-a-glance page; build-cost estimates; leaner references (new `handoff.md`, `gap-reports.md`).
- Design depth: new `visual-quality.md` (modes, idea-first, generic-look tells, concrete type/colour/space values, design record, screenshot critique, polish pass) and `motion.md` (timing, easing, feedback, performance, reduced motion); `ui-ux.md` gains quick persona, journey map, real options, heuristic walkthrough and a better test script. Adapted from taste-skill, impeccable, gsap-skills and designer-skills (credited in THIRD_PARTY_NOTICES).

## Agent team

This is repository tooling, versioned together with the first agent skill (software-architect 0.1.0); it is not tagged on its own.

### [0.1.0] - Unreleased
- Handoff contract between the boss and specialist agents (`docs/agents/agent-template/handoff-contract.md`) with a validator, `scripts/agent_contract.py`: request, response (status, summary, files, questions, approvals, assumptions, evidence), event line, and the event log `.agents/events.jsonl`.
- `scripts/validate_agents.py` checks `agents/*.md` (name, description, model, tools, skill folder, `## Handoff` section); runs in CI with the new tests.
- `scripts/package_skill.py` includes the agent files that name the skill (`agents/<file>.md` at the archive root) and warns when an agent file cannot be read.
- `scripts/install_agents.py` copies skills and agents to `~/.claude` (or `--dest`): dry run first, never overwrites a changed file without `--force`, never deletes.
- `scripts/log_event.py`: Claude Code hook script that writes one event line per subagent start/stop and file write; never fails the session, never writes outside the project, reads UTF-8. Hooks snippet in `docs/agents/agent-template/hooks-snippet.json`.
- `scripts/check_sources.py` and `scripts/check_evals.py` guard `sources.md` (verified/unverified, unique IDs, citations resolve) and `evals.json`.
- `docs/agents/agent-template/`: copy-and-fill agent file, skill folder and a ten-step "add a new specialist" checklist.
