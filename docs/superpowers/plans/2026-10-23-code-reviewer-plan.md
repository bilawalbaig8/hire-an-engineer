# Code Reviewer agent: implementation plan (Phase 3)

> For agentic workers: this plan follows the pattern proven by the Architect (`2026-10-22-agent-contract-and-architect-plan.md`, Part 2). Steps use checkboxes.

**Goal:** Build the Code Reviewer specialist (skill `code-reviewer` + `agents/code-reviewer.md`) with verified sources, evals written first, knowledge files, agent file, and passing evals. Prove the handoff contract on a second, different role.

**Spec:** `docs/superpowers/specs/2026-10-23-code-reviewer-design.md` (approved by the owner 2026-10-23).

## Global constraints
- Same rules as the Architect plan: `AGENTS.md`, own-words summaries, cite verified sources only (unverified only with the word "unverified" on the same line), skill SKILL.md lean, description at most 1024 characters, repo and installed copies identical, stage only named files, branch `feat/specialized-agents`, no release or tag, no real install without the owner's OK and never `--force`.
- The Reviewer never edits code; its model is opus; the review report goes to `docs/reviews/`; findings carry file:line evidence and a confidence level; precision matters as much as recall.
- Ledger and independent reviews as before; when a reviewer or implementer launch is refused, follow the owner's standing rules (park reviews for the final review, write natively).

## Tasks
- [ ] **R1 Sources research.** Three research passes written to files in the workspace (not only returned): (a) code review practice, correctness, testing, maintainability; (b) security review, CWE/OWASP, AI-written code defects; (c) per-language official guides (Python, TypeScript/JavaScript, C# and Unity, Java/Kotlin, Go, SQL) and performance and data review. Every item verified against the publisher or consistent records; unconfirmed items marked. Then `skills/code-reviewer/references/sources.md` in the checked table format (IDs `S-REV-n`, `S-SEC-n`, `S-LNG-n`, `S-AIC-n`, `S-PRF-n`, `S-TST-n`), `check_sources.py` exit 0, notices added to `THIRD_PARTY_NOTICES.md`, stub `SKILL.md` so validators pass.
- [ ] **R2 Evals first.** `evals/code-reviewer/` (git-ignored, local): `evals.json` with the 12 cases of spec section 8, a fixture project with planted defects and several diffs, `GROUND-TRUTH` file outside the fixtures, a setup script. `check_evals.py` exit 0.
- [ ] **R3 Knowledge files.** `review-method`, `correctness-and-edge-cases`, `security-review`, `performance-and-data`, `tests-review`, `simplicity-and-maintainability`, `ai-written-code`, `language-notes`, `report-templates`. Any command or script verified on a throwaway repo.
- [ ] **R4 SKILL.md and agent file.** From the agent template; handoff section inlined; validators green.
- [ ] **R5 Run the evals, fix, rerun.** Each case in a fresh subagent as the agent under test; grade against ground truth; count false positives; up to two fix rounds.
- [ ] **R6 Installer `--only <skill>` option.** TDD in `scripts/install_agents.py` and tests: with `--only name` only that skill folder (and the agent files naming it) are planned, nothing else is touched, `--force` unchanged. Small separate commit.
- [ ] **R7 Close-out.** CHANGELOG entry (`## code-reviewer`, 0.1.0 Unreleased), task list and progress page, installed copy after the owner's OK (with `--only`), independent reviews of anything parked, push the branch.
