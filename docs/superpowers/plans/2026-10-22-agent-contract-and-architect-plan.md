# Agent contract and Architect agent: implementation plan (Phases 1 and 2)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the handoff contract, agent template, tooling (validator, packager, installer, event log) and the first specialist, the Architect (skill `software-architect` + agent `agents/architect.md`), with evals.

**Architecture:** Specialists are skill-shaped knowledge folders (`skills/<name>/`) with a thin Claude Code agent file (`agents/<role>.md`) on top. The boss and specialists talk through a JSON handoff contract (request, response, event line); small Python scripts in `scripts/` validate it, package it, install it and log events. Knowledge is own-words summaries of verified, credited sources.

**Tech Stack:** Python 3.12 (stdlib + pyyaml, pytest for tests), Markdown, JSON, GitHub Actions. Windows + POSIX paths.

**Spec:** `docs/superpowers/specs/2026-10-22-architect-agent-design.md` and `docs/superpowers/specs/2026-10-22-agent-team-master-plan.md` (both approved by the owner 2026-10-22).

## Global Constraints

- Follow `AGENTS.md`: CHANGELOG entry, credit sources in `THIRD_PARTY_NOTICES.md`, `PYTHONUTF8=1 python scripts/validate_skills.py` before every commit, SKILL.md lean (router + core rules), details in `references/`, description at most 1024 chars, SKILL.md under 500 lines (validator limit; aim for under 150).
- New skill name `software-architect`; agent file `agents/architect.md`; starts at 0.1.0 `Unreleased`; tag `software-architect-v0.1.0` only when the owner says release.
- Architect model is `opus`; mechanical steps may use a smaller model.
- Decision records go to `docs/decisions/NNNN-*.md` (same series as `hire-an-engineer`, continue existing numbering). Overview, diagrams, risks, scenarios go to `docs/architecture/`.
- Diagram default is Mermaid. Ask the owner before installing anything. If a diagram cannot be rendered, give the source and say it was not rendered.
- Every claim about existing code is labelled `verified in code`, `inferred` or `unknown`.
- Knowledge is written in our own words; no copied passages. Only sources with status `verified` are cited as fact.
- One-way-door decisions are returned to the boss as approvals; the agent never finalises them alone.
- The repo copy and the installed copy under `~/.claude` stay identical (`diff -rq`).
- Work on branch `feat/specialized-agents`. Another session may use the same folder for other work: stage only the files named in each task, never `git add -A`.

## Review Focus

1. A project already has `docs/decisions/` with other numbering or format: Recover/Design must continue it, not overwrite. (Task 9 eval, Task 7 template text.)
2. A repo has no git history or is huge: Recover mode must skip hotspot analysis, say so, and still label claims. (Task 9 eval.)
3. No tool to render diagrams: output says "not rendered" and gives source; never claims a check. (Task 9 eval.)
4. Owner asks for microservices for a tiny app, or to skip trade-offs: agent pushes back proportionately and returns the one-way-door decision as an approval. (Task 9 eval.)
5. Installer run twice, or destination holds a modified copy: no silent overwrite. (Task 4 test.)
6. A source marked `unverified` gets cited as fact in a knowledge file. (Task 6 check.)

---

## Part 1: Contract and tooling (Phase 1)

### Task 1: Handoff contract and validator

**Files:**
- Create: `scripts/agent_contract.py`, `tests/test_agent_contract.py`, `docs/agents/agent-template/handoff-contract.md`

**Interfaces:**
- Produces: `RESPONSE_STATUSES = ("done", "needs_answers", "needs_approval", "blocked")`; `EVENT_TYPES = ("agent_start", "agent_stop", "handoff", "file_written", "approval_requested", "approval_given")`; `validate_request(obj: dict) -> list[str]`; `validate_response(obj: dict) -> list[str]`; `validate_event(obj: dict) -> list[str]`; `append_event(path: Path, event: dict) -> None` (raises `ValueError` listing errors, creates parent folders, appends one JSON line). Each validate function returns a list of error strings, empty when valid.
- Request fields: `goal: str`, `context_files: list[str]`, `constraints: list[str]`, `done_when: list[str]`, optional `mode: str`, optional `answers: list[{id, answer}]`.
- Response fields: `status`, `summary: str`, `files: list[str]`, `questions: list[{id, question, why}]`, `approvals: list[{id, decision, options: list[str], recommended: str, one_way_door: bool}]`, `assumptions: list[str]`, `evidence: list[str]`.
- Event fields: `ts` (ISO 8601 UTC), `type`, `agent`, `run_id`; `file_written` also needs `path`; `handoff` needs `from`, `to`.

- [ ] **Step 1: Write failing tests** in `tests/test_agent_contract.py`: `test_valid_response_done_has_no_errors`; `test_done_without_evidence_is_error`; `test_needs_answers_requires_questions`; `test_needs_approval_requires_approvals`; `test_unknown_status_is_error`; `test_request_requires_goal_and_done_when`; `test_event_file_written_requires_path`; `test_handoff_requires_from_and_to`; `test_append_event_writes_one_line_and_rejects_invalid` (invalid event leaves the file unchanged).
- [ ] **Step 2: Run** `pytest tests/test_agent_contract.py -q`. Expected: FAIL (module missing).
- [ ] **Step 3: Implement** `scripts/agent_contract.py` with the signatures above plus a CLI `python scripts/agent_contract.py check-request|check-response|check-event FILE` (exit 1 and print errors if invalid). Hand-written checks, no new dependency.
- [ ] **Step 4: Write `docs/agents/agent-template/handoff-contract.md`**: plain-language contract: who talks to the owner (boss only), request, response, how questions and approvals flow, what counts as `evidence`, the event log line and its path `.agents/events.jsonl`, one worked example each (valid request, `needs_answers` response, `needs_approval` response, event lines). Examples must pass the CLI.
- [ ] **Step 5: Run** `pytest tests/test_agent_contract.py -q` (PASS) and the CLI on the three examples saved to a temp folder (exit 0).
- [ ] **Step 6: Commit** `git add scripts/agent_contract.py tests/test_agent_contract.py docs/agents/agent-template/handoff-contract.md` then `git commit -m "feat: handoff contract and validator"`.

### Task 2: Agent file validator

**Files:**
- Create: `scripts/validate_agents.py`, `tests/test_validate_agents.py`, `tests/fixtures/agents/good/agents/demo.md`, `tests/fixtures/agents/good/skills/demo/SKILL.md`, `tests/fixtures/agents/bad/agents/*.md` (one bad file per rule)
- Modify: `.github/workflows/validate.yml` (read it first; add `pip install pytest`, run `python scripts/validate_agents.py` and `pytest -q`)

**Interfaces:**
- Produces: `validate_agent_file(path: Path, skills_dir: Path) -> list[str]`; CLI `python scripts/validate_agents.py` validates every `agents/*.md` against `skills/` and exits 1 on any error.
- Rules: frontmatter has `name` (equals file stem), `description` (non-empty, at most 1024 chars), `model` in `opus|sonnet|haiku|inherit`, `tools` (list of strings), `skill` (folder exists under `skills/`); body contains a `## Handoff` heading that mentions `handoff-contract.md`.

- [ ] **Step 1: Write failing tests**: `test_good_agent_passes`; one test per rule: `test_name_must_match_filename`, `test_description_too_long`, `test_bad_model`, `test_missing_skill_folder`, `test_missing_handoff_section`, `test_missing_frontmatter`.
- [ ] **Step 2: Run** `pytest tests/test_validate_agents.py -q`. Expected: FAIL.
- [ ] **Step 3: Implement** `validate_agent_file` and `main()`, reusing the frontmatter regex style of `scripts/validate_skills.py`.
- [ ] **Step 4: Run** the tests (PASS) and `PYTHONUTF8=1 python scripts/validate_agents.py` (prints "No agents found" and exits 0 when `agents/` does not exist yet).
- [ ] **Step 5: Commit** the files named above with message `feat: validate agent files in CI`.

### Task 3: Packager includes agent files

**Files:**
- Modify: `scripts/package_skill.py`
- Create: `tests/test_package_skill.py`

**Interfaces:**
- Consumes: `agents/*.md` frontmatter key `skill` (Task 2).
- Produces: `agent_files_for_skill(skill_name: str, agents_dir: Path) -> list[Path]`; the `.skill` and `.zip` archives additionally contain `agents/<file>.md` for every agent whose `skill` equals the skill name. Skills without agents package exactly as before.

- [ ] **Step 1: Write failing tests**: `test_agent_files_for_skill_matches_frontmatter`; `test_package_contains_agent_file` (builds a temp repo layout, runs the packager, opens the zip); `test_package_without_agent_unchanged` (archive listing equals the old behaviour).
- [ ] **Step 2: Run** `pytest tests/test_package_skill.py -q`. Expected: FAIL.
- [ ] **Step 3: Implement** `agent_files_for_skill` and call it when writing each archive; keep the existing dot-file exclusion. Resolve the `agents/` folder relative to the repo root (parent of `skills/`).
- [ ] **Step 4: Run** the tests (PASS) and `python scripts/package_skill.py skills/hire-an-engineer dist` then confirm the archive list is unchanged against `git stash`-free comparison of the earlier listing (names only).
- [ ] **Step 5: Commit** `scripts/package_skill.py tests/test_package_skill.py` with `feat: package agent files with their skill`.

### Task 4: Installer

**Files:**
- Create: `scripts/install_agents.py`, `tests/test_install_agents.py`
- Modify: `docs/INSTALL.md` (new section "Agents (Claude Code)")

**Interfaces:**
- Produces: `plan_install(src_root: Path, dest: Path) -> list[Action]` with `Action(kind: Literal["new","same","differs"], src: Path, dst: Path)`; `install(src_root: Path, dest: Path, force: bool = False, dry_run: bool = False) -> int` returns the number of files written and raises `FileExistsError` listing every `differs` path when `force` is false. Copies `skills/*` to `dest/skills/` and `agents/*.md` to `dest/agents/`. CLI: `python scripts/install_agents.py [--dest PATH] [--dry-run] [--force]`, default dest `~/.claude`.

- [ ] **Step 1: Write failing tests** with temp dirs: `test_new_files_are_copied`; `test_identical_files_are_skipped`; `test_modified_destination_raises_without_force`; `test_force_overwrites`; `test_dry_run_writes_nothing`; `test_second_run_writes_zero` (the Review Focus 5 case).
- [ ] **Step 2: Run** `pytest tests/test_install_agents.py -q`. Expected: FAIL.
- [ ] **Step 3: Implement** with `filecmp`/hash compare and `shutil.copy2`; print a one-line summary per action.
- [ ] **Step 4: Run** the tests (PASS); run `python scripts/install_agents.py --dry-run --dest <temp>` on the real repo and check it lists `skills/hire-an-engineer` files as `new`.
- [ ] **Step 5: Document** the command, `--dry-run`, the no-overwrite rule and `--force` in `docs/INSTALL.md`.
- [ ] **Step 6: Commit** the three files with `feat: installer for skills and agents`.

### Task 5: Event log hook

**Files:**
- Create: `scripts/log_event.py`, `tests/test_log_event.py`, `docs/agents/agent-template/hooks-snippet.json`

**Interfaces:**
- Consumes: `append_event`, `validate_event` (Task 1).
- Produces: `event_from_hook(payload: dict) -> dict | None` maps a Claude Code hook payload to one event (`SubagentStart` to `agent_start`, `SubagentStop` to `agent_stop`, `PostToolUse` of Write/Edit to `file_written`); returns `None` for everything else. CLI reads the hook JSON from stdin and appends to `.agents/events.jsonl` in the project folder; never fails the host (exit 0 always, errors to stderr).

- [ ] **Step 1: Check the real hook payload first.** Use a `claude-code-guide` lookup (or the Claude Code hooks documentation) for the exact field names of `SubagentStart`, `SubagentStop` and `PostToolUse` payloads; record them in `docs/agents/agent-template/handoff-contract.md` under "Event sources". Do not guess field names.
- [ ] **Step 2: Write failing tests** using payload dicts built from Step 1: `test_subagent_start_maps_to_agent_start`; `test_subagent_stop_maps_to_agent_stop`; `test_write_tool_maps_to_file_written_with_relative_path`; `test_other_events_return_none`; `test_cli_never_raises_on_garbage_stdin`.
- [ ] **Step 3: Run** `pytest tests/test_log_event.py -q`. Expected: FAIL.
- [ ] **Step 4: Implement** `scripts/log_event.py`; `run_id` is the hook's session id.
- [ ] **Step 5: Write** `docs/agents/agent-template/hooks-snippet.json` (the `hooks` block to merge into a project's `.claude/settings.json` that calls the script), and verify by a manual run: pipe one sample payload into the script and confirm one valid line appears (check with `agent_contract.py check-event`).
- [ ] **Step 6: Run** tests (PASS). **Commit** with `feat: event log hook for the visual office`.

### Task 6: Sources checker and eval checker

**Files:**
- Create: `scripts/check_sources.py`, `scripts/check_evals.py`, `tests/test_check_sources.py`, `tests/test_check_evals.py`

**Interfaces:**
- Produces: `check_sources(path: Path) -> list[str]` (a `sources.md` must hold one Markdown table with columns `ID | Title | Author | Year | URL | Use | Cost/licence | Status`; `ID` unique and shaped `S-<AREA>-<n>`; `Status` is `verified` or `unverified`; `URL` starts `http`); `check_refs(skill_dir: Path) -> list[str]` (every `[S-...]` in `references/*.md` exists in `sources.md`, and none refers to an `unverified` source unless the sentence contains the word `unverified`); `check_evals(path: Path) -> list[str]` (JSON list of cases; each has `id`, `kind` in `typical|edge|refusal`, `prompt`, `expect` as non-empty list of strings, optional `fixture`).
- Before writing `check_evals`, read `evals/hire-an-engineer/evals.json` and keep its field names where they overlap; add only `kind`.

- [ ] **Step 1: Write failing tests** for each rule (`test_duplicate_id`, `test_bad_status`, `test_missing_url`, `test_ref_to_unknown_id`, `test_unverified_cited_as_fact`, `test_eval_missing_expect`, `test_eval_bad_kind`) plus one passing fixture each.
- [ ] **Step 2: Run** `pytest tests/test_check_sources.py tests/test_check_evals.py -q`. Expected: FAIL.
- [ ] **Step 3: Implement** both scripts with CLIs (`python scripts/check_sources.py skills/<name>`, `python scripts/check_evals.py evals/<name>/evals.json`).
- [ ] **Step 4: Run** the tests (PASS). Wire both CLIs into `.github/workflows/validate.yml` to run only when the target exists.
- [ ] **Step 5: Commit** with `feat: sources and evals checkers`.

### Task 7: Agent template and doc pass for Part 1

**Files:**
- Create: `docs/agents/agent-template/agent.md`, `docs/agents/agent-template/skill/SKILL.md`, `docs/agents/agent-template/skill/references/example.md`, `docs/agents/agent-template/README.md`
- Modify: `CHANGELOG.md`, `TASKS.md`, `AGENTS.md` (add "Agents" lines: folder map entry for `agents/`, the contract path)

**Interfaces:**
- Consumes: Tasks 1-6.
- Produces: a copy-and-fill template whose `agent.md` passes `validate_agent_file` once `name` and `skill` are filled, with sections: role, when to use, model and why, tools, what it reads first, how it works, `## Handoff` (points at `handoff-contract.md`), what it never does.

- [ ] **Step 1: Write failing check**: `tests/test_template.py::test_template_agent_passes_validator_after_fill` fills the placeholders in a temp copy and runs `validate_agent_file`.
- [ ] **Step 2: Run** it. Expected: FAIL.
- [ ] **Step 3: Write the template files**; the `README.md` is a 10-step "add a new role" checklist that mirrors the Definition of Done in the master plan (section 6).
- [ ] **Step 4: Run** `pytest -q` (all PASS) and `PYTHONUTF8=1 python scripts/validate_skills.py`.
- [ ] **Step 5: Update** `CHANGELOG.md` with a `## Agent team` section, `### [0.1.0] - Unreleased` (contract, validator, packager, installer, event log), update `TASKS.md` (tasks 0.4, 0.6, 1.1-1.6 done) and the progress page; commit with `feat: agent template and docs`.

---

## Part 2: Architect (Phase 2)

### Task 8: Architect evals first (written before the knowledge)

**Files:**
- Create: `evals/software-architect/evals.json`, `evals/software-architect/fixtures/shop-api/` (small Python API, about 12 files, with one planted layering violation and one planted circular dependency), `evals/software-architect/fixtures/shop-api-GROUND-TRUTH.md` (kept outside the fixture folder so the agent never sees it)

**Interfaces:**
- Consumes: `check_evals` (Task 6).
- Produces: cases, each with `expect` lines that a reviewer can grade pass/fail:
  - typical (design): `web-app`, `mobile-offline`, `multiplayer-game`, `ai-agent-product`, `data-pipeline`: asks the few questions that change the design; states quality-attribute scenarios; offers 2-3 options with trade-offs; picks the simplest that fits; writes `docs/architecture/overview.md`, `scenarios.md`, `risks.md`, at least one ADR; a diagram with at most 9 elements and labelled arrows.
  - typical (recover): `recover-shop-api`: finds the real entry points and data model; reports the planted violation and cycle; every claim labelled; invents no component listed as absent in GROUND-TRUTH.
  - edge: `recover-no-git` (copy of the fixture without `.git`: skips hotspots and says so), `existing-adr-series` (project already has `docs/decisions/0001-*.md`: new ADR is `0002`, old files untouched), `no-renderer` (says "not rendered" and gives Mermaid source).
  - refusal: `microservices-for-todo-app` (pushes back, recommends a simple shape, returns the choice as an approval), `skip-tradeoffs` (refuses to skip, explains briefly), `approve-one-way-door` (returns `needs_approval`, does not finalise).

- [ ] **Step 1: Write** the fixture and GROUND-TRUTH, then `evals.json` with the cases above (prompts in the owner's likely style: short, non-technical).
- [ ] **Step 2: Run** `python scripts/check_evals.py evals/software-architect/evals.json` (exit 0).
- [ ] **Step 3: Commit** with `test: architect evals`.

### Task 9: Sources file from the verified research

**Files:**
- Create: `skills/software-architect/references/sources.md`, `docs/superpowers/research/architect-sources-2026-10-22.md` (raw digest of the four research passes, kept for traceability)
- Modify: `THIRD_PARTY_NOTICES.md`

**Interfaces:**
- Produces: stable source IDs used by every later reference file: `S-FND-n` (foundations, methods, well-architected), `S-WEB-n` (web, backend, distributed, security), `S-AI-n`, `S-DATA-n`, `S-GAME-n`, `S-MOB-n`, `S-DESK-n`, `S-RT-n` (real-time, state, messaging), `S-REC-n` (recovery and conformance), `S-DIA-n` (diagram tools).

- [ ] **Step 1: Write** the digest file from the four research reports (about 125 items; carry over each item's status and its caveat). The raw reports are the agents' hand-backs from this session; if they are no longer available, rerun the four research prompts from `docs/superpowers/specs/2026-10-22-architect-agent-design.md` section 7.
- [ ] **Step 2: Write** `sources.md` as one table per area in the column format from Task 6, `Status` = `verified` only where the report said V; `V*`, R and anything unconfirmed become `unverified`. Add a short "How to use these sources" paragraph: ideas only, in our own words, always cite the ID.
- [ ] **Step 3: Run** `python scripts/check_sources.py skills/software-architect` (exit 0).
- [ ] **Step 4: Add** credits to `THIRD_PARTY_NOTICES.md` (one line per source family: title, author, URL, how used, licence where known; CC BY-SA items noted as "ideas summarised, text not copied").
- [ ] **Step 5: Commit** with `docs: architect sources`.

### Task 10: Core method files

**Files:**
- Create: `skills/software-architect/references/core-principles.md`, `method-design.md`, `method-recover.md`, `review-checklists.md`

**Interfaces:**
- Consumes: source IDs from Task 9. Produces file names that SKILL.md (Task 13) routes to.
- `core-principles.md`: trade-offs and quality attributes as testable scenarios, reversibility (one-way vs two-way doors), proportional design (monolith first, single AI call before agent), ADR format (MADR style, status values, superseded not rewritten, continue an existing series), labels `verified in code | inferred | unknown`.
- `method-design.md`: the five Design-mode steps of the spec, the question list that changes designs, how options are compared, what goes into each artifact, when to return `needs_answers` or `needs_approval`.
- `method-recover.md`: the six Recover steps of the spec, per-step commands for git, dependency graphs and conformance tools (every command verified by running it once on `evals/software-architect/fixtures/shop-api`), the no-git and huge-repo fallbacks, how inferred decisions are written as ADRs marked `inferred`.
- `review-checklists.md`: design review, "what breaks at 10x", pre-launch, drift check.

- [ ] **Step 1: Write** each file in our own words, citing source IDs inline.
- [ ] **Step 2: Run** `python scripts/check_sources.py skills/software-architect` (refs resolve) and a manual run of every command in `method-recover.md` against the fixture (outputs match GROUND-TRUTH).
- [ ] **Step 3: Commit** with `feat: architect core method`.

### Task 11: Field references (four small commits)

**Files:**
- Create under `skills/software-architect/references/`: (a) `web-backend-cloud.md`, `distributed-data.md`, `security-architecture.md`; (b) `mobile.md`, `desktop-plugins.md`; (c) `game-engine.md`, `realtime-netcode-state.md`; (d) `ai-systems.md`, `data-pipelines.md`

**Interfaces:**
- Each file has the same sections: when to read it; decisions that matter most (each as "choose X when ..., otherwise Y", with what is given up); typical shapes; failure modes; pre-launch checks; sources (IDs only).
- The decision rules already distilled in the master research (monolith first, timeouts and circuit breakers, per-use-case consistency, SLOs first, threat-model in design, simplest AI pattern, server-or-client owns truth, fixed timestep, local database as truth on mobile, out-of-process plugins, explicit state machines) must each appear in the file that owns them.
- Fields the research found thin (specific GDC talks, save systems, game performance budgets) are marked `starter` at the top of the file and listed in `CHANGELOG.md` as "to deepen".

- [ ] **Step 1 (per group): Write** the files in own words with source IDs.
- [ ] **Step 2: Run** `python scripts/check_sources.py skills/software-architect` (exit 0, no unverified source cited as fact).
- [ ] **Step 3: Commit** each group separately: `feat: architect references (web, distributed, security)`, `(mobile, desktop)`, `(game, real-time)`, `(AI, data)`.

### Task 12: Diagrams reference and checked toolchain

**Files:**
- Create: `skills/software-architect/references/diagrams.md`

**Interfaces:**
- Consumes: `hire-an-engineer` `references/documents.md` section 7 (link to it, do not duplicate).
- Produces: C4 levels and when each is used, Mermaid as default with templates for context, container, sequence, ER and a dependency-graph diagram; readability rules (one question per diagram, at most about 9 elements, labelled directional arrows, legend, boundaries, inferred links dashed); render-and-look procedure; fallback when nothing renders; optional tools (LikeC4, Structurizr, D2, PlantUML) with the exact commands from the research, each marked `not run here` until run.

- [ ] **Step 1: Check** whether Node and a Mermaid renderer exist: `node --version`, `npx --no-install mmdc --version`. If missing, **ask the owner before installing**; if not approved, record "render command not run here" in the file.
- [ ] **Step 2: Write** the file; for every template, render it (if a renderer is available) and look at the image; fix overlaps.
- [ ] **Step 3: Run** `python scripts/check_sources.py skills/software-architect` and commit with `feat: architect diagrams reference`.

### Task 13: SKILL.md and agent file

**Files:**
- Create: `skills/software-architect/SKILL.md`, `agents/architect.md`

**Interfaces:**
- Consumes: Tasks 9-12 (reference file names), Task 7 template, Task 1 contract.
- `SKILL.md`: frontmatter `name: software-architect`, description (at most 1024 chars, says what it does and when to use it, including Recover/Review), router table (task -> reference file), the two modes in brief, the always-rules from Global Constraints, an "ask vs decide" rule; under 150 lines.
- `agents/architect.md`: from the template; `model: opus`; `tools` limited to Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch (no network/installs without the boss relaying approval); `skill: software-architect`; handoff section: first turn returns `needs_answers` with only the questions that change the design; after answers, writes artifacts and returns `done` with evidence, or `needs_approval` for one-way doors.

- [ ] **Step 1: Write** both files.
- [ ] **Step 2: Run** `PYTHONUTF8=1 python scripts/validate_skills.py`, `python scripts/validate_agents.py`, `pytest -q` (all exit 0).
- [ ] **Step 3: Commit** with `feat: software-architect skill and agent`.

### Task 14: Run the evals, fix, rerun

**Files:**
- Create: `evals/software-architect/results-2026-10-DD.md` (date of the run)
- Modify: files under `skills/software-architect/` and `agents/architect.md` as the failures require

**Interfaces:**
- Method: each case runs in a fresh subagent on `opus` (Architect's model) with the skill and agent text loaded, in an empty scratch folder (fixtures copied in); the boss role is played by the runner, which supplies answers to `needs_answers`. A separate fresh reviewer grades each `expect` line pass/fail with quoted evidence. Record tokens as estimates unless measured.

- [ ] **Step 1: Run** all cases, write the results table (case, verdict, failing expectations, tokens).
- [ ] **Step 2: Fix** the root cause of each failure in the skill or agent file (not the eval), rerun only the failed cases; maximum two fix rounds, then report what still fails.
- [ ] **Step 3: Validate** (`validate_skills.py`, `validate_agents.py`, `check_sources.py`, `check_evals.py`, `pytest -q`) and commit with `test: architect eval results and fixes`.

### Task 15: Release prep (no tag)

**Files:**
- Modify: `CHANGELOG.md` (`## software-architect`, `### [0.1.0] - Unreleased`), `THIRD_PARTY_NOTICES.md`, `README.md` (one line listing the new skill and agent), `TASKS.md`

- [ ] **Step 1: Install** into the owner's folders: `python scripts/install_agents.py --dry-run` first, show the owner the list, then run for real after their OK; confirm `diff -rq skills/software-architect ~/.claude/skills/software-architect` and `diff -q agents/architect.md ~/.claude/agents/architect.md` are clean.
- [ ] **Step 2: Update** `TASKS.md` (tasks 2.1-2.8 done) and the progress page (regenerate `tasks.json`, upload, update the dataset `url`).
- [ ] **Step 3: Commit** with `docs: software-architect 0.1.0 release notes`. Do not tag; ask the owner whether to release.
