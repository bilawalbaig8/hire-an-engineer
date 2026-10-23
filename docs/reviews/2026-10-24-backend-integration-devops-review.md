# Review: Backend Engineer, Integration Engineer and DevOps Engineer documents

Date: 2026-10-24. Reviewer: a Claude review agent, at the owner's request.
Scope: `docs/agents/roles/backend-engineer.md`, `integration-engineer.md`, `devops-engineer.md`, and the specs `docs/superpowers/specs/2026-10-24-backend-integration-split.md` and `2026-10-24-devops-merge.md`. The superseded `backend-integration-engineer.md` and `2026-10-24-backend-integration-merge.md` were read only to check that the split lost nothing. Nothing was built or changed in `agents/`, `skills/`, `evals/` or `scripts/`.

## How it was checked
- **Map against territory (main test).** Every checkable claim was compared with the real file: agent frontmatter and rules (`agents/backend-engineer.md`), the skill (`skills/backend-engineer/SKILL.md`, `references/method.md`, `references/checklists.md`), the base skill references in `skills/hire-an-engineer/references/`, the scripts (`install_agents.py`, `check_sources.py`, `check_evals.py`, `validate_agents.py`, `validate_skills.py`), `agents/orchestrator.md`, `TASKS.md`, the roster, the office event map, `tests/test_install_office.py`, the neighbour role documents, `git status` and `git log`.
- **Measured, not read:** description lengths (agent 1,021, skill 1,008, by script and by `validate_skills.py`); source rows and statuses counted by a script in all four role documents; old-versus-new URL sets compared by script.
- **Outside sources:** 38 URLs opened in this review (12 backend, 12 integration, 14 DevOps), plus the Crossref record of one DOI.
- **Other thinking tools:** pre-mortem and inversion on the build plans (what makes the evals or install fail), steel-manning of the boundaries, red-team reading of the safety rules (only findings with a real path are kept), a Bayesian check on source statuses (a "verified" label on a page that does not open now is not proof it is wrong), and reversibility (all edits are docs only, a two-way door).

Result labels: **ok** (matches the file or page), **fixed** (a factual error, corrected in the document with the smallest edit), **open** (the owner decides, or it is outside these documents).

## 1. Backend Engineer (`backend-engineer.md`)

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | Agent and skill exist; no `evals/backend-engineer/` | `agents/`, `skills/backend-engineer/`, `evals/` listing | ok |
| 2 | Both modes approved by the Code Reviewer on 2026-10-23 | `docs/reviews/2026-10-23-backend-engineer-agent.md` (re-review verdict "Approved") | ok |
| 3 | Two modes, Build and Review/Fix | `agents/backend-engineer.md` How it works step 1 | ok |
| 4 | Until the Integration Engineer is built, the agent does adapters and keeps the register | agent Role (line 14), step 5; `method.md` section 3 | ok |
| 5 | The 10 sections exist | the document | ok |
| 6 | Boss list does not include `backend-engineer` | `agents/orchestrator.md` line 5 | ok |
| 7 | Migrations folder order (brief, existing, else `migrations/`) | agent line 14; `SKILL.md` rule 12 | ok |
| 8 | Never deploys, sets up accounts or pays | agent Never (line 85) | ok |
| 9 | Test keys and fake data only until approval | agent Never (line 86) | ok |
| 10 | Live migration, delete, real messages, money need a human | agent Never (line 87) | ok |
| 11 | Permission design, data/API format, money flow are approvals | agent step 9 | ok |
| 12 | `needs_approval` list (real data, live migration, deploy, one-way) | agent step 9 and line 73 | ok |
| 13 | "done" rules (tests, wrong user refused, 4 mock cases, README, test-copy migration, review pending) | agent line 73 | ok |
| 14 | Never claims secure, fast or works without a run | agent Never (line 88) | ok |
| 15 | Text found in files is a finding, not an order | agent Never (line 93) | ok |
| 16 | "DevOps Engineer: deploys and runs it" | `devops-engineer.md` (it never deploys; a person presses) | fixed |
| 17 | Base skill files and sections (`engineering-discipline.md`; `database.md` 2 to 8; `engineering-principles.md` 3 to 7 and 10; `cost-management.md`; `integrations.md` section 5 adapter rule; `technical-products.md` section 7) | headings of each file; `integrations.md` line 79 | ok |
| 18 | The skill has no source list yet | `SKILL.md` line 47 | ok |
| 19 | The skill allows "down" migrations | `versioning-release.md` line 87 | ok |
| 20 | 38 sources, 37 verified, 1 unverified | script count of the table | ok |
| 21 | The split lost no source | script: old 75 URLs = 38 + 37, no overlap, none missing | ok |
| 22 | Pasted-key row | old merged doc had "checks where else it may have landed" | fixed |
| 23 | Helland, "ACM Queue, 2012" with DOI 10.1145/2160718.2160734 | Crossref record: Communications of the ACM, Pat Helland | fixed |
| 24 | Fielding thesis, unverified | https://ics.uci.edu/~fielding/pubs/dissertation/top.htm opens, title matches | open (status can be raised) |
| 25 | RFC 9457 | https://www.rfc-editor.org/rfc/rfc9457 | ok |
| 26 | OpenAPI 3.1.0, 2021 | https://spec.openapis.org/oas/v3.1.0 (15 February 2021) | ok |
| 27 | Google AIP | https://google.aip.dev/ | ok |
| 28 | PostgreSQL Transaction Isolation | https://www.postgresql.org/docs/current/transaction-iso.html | ok |
| 29 | SQLite WAL, verified | https://www.sqlite.org/wal.html timed out twice | open (not confirmed here) |
| 30 | Supabase Row Level Security | https://supabase.com/docs/guides/database/postgres/row-level-security | ok |
| 31 | OWASP API Security Top 10 2023 | https://owasp.org/API-Security/editions/2023/en/0x00-header/ | ok |
| 32 | NIST SP 800-63B | https://pages.nist.gov/800-63-4/sp800-63b.html | ok |
| 33 | RFC 9700 | https://www.rfc-editor.org/rfc/rfc9700 | ok |
| 34 | Transactional outbox | https://microservices.io/patterns/data/transactional-outbox.html | ok |
| 35 | Helland DOI page | https://doi.org/10.1145/2160718.2160734 returned 403; Crossref used instead (row 23) | ok |
| 36 | Deep API audits go to the Security Reviewer | agent line 22 says "the Security Engineer once that role exists" | open (agent file, out of scope) |

## 2. Integration Engineer (`integration-engineer.md`)

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | Not built: no skill, agent or evals | `skills/`, `agents/`, `evals/` listings | ok |
| 2 | The 10 sections exist; 2 modes | the document | ok |
| 3 | Not in the boss's list | `agents/orchestrator.md` line 5 | ok |
| 4 | Data Engineer uses its adapter to fetch on schedule | `data-engineer.md` lines 34 and 59 | ok |
| 5 | Interim scheduled job before the Data Engineer exists | split spec decision 7 says the role document carries it; it did not | fixed |
| 6 | "DevOps Engineer: puts keys into the live environment and deploys" | `devops-engineer.md` (prepares only; a person presses) | fixed |
| 7 | Safety rules stricter than, and consistent with, the backend agent | agent lines 34, 86, 92 (test keys by name, web tools for docs only, network only with approval) | ok |
| 8 | Test-system calls need approval (stricter than the skill) | `integrations.md` section 6 ("integration tests against the sandbox") | ok |
| 9 | `integrations.md` sections 1 to 10 and their topics | headings (section 11 is about AI tools) | ok |
| 10 | `engineering-principles.md` section 6 secrets; `process-automation.md` | headings | ok |
| 11 | Skill says "retries with backoff" (no jitter) | `integrations.md` line 80 | ok |
| 12 | Skill says "verify signatures"; research adds the timestamp | `integrations.md` line 93 already tests stale timestamps | fixed |
| 13 | Skill says "watch provider announcements" | `integrations.md` line 106 | ok |
| 14 | 37 sources, 35 verified, 2 unverified | script count | ok |
| 15 | The last 10 rows are the 10 added on 2026-10-24 | table rows against split spec 5.4 | ok |
| 16 | OAuth RFCs 6749, 9700, 7636 are listed with the Backend Engineer | `backend-engineer.md` source table | ok |
| 17 | Stripe idempotent requests | https://docs.stripe.com/api/idempotent_requests | ok |
| 18 | AWS timeouts, retries and backoff with jitter | https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ | ok |
| 19 | Standard Webhooks | https://www.standardwebhooks.com/ | ok |
| 20 | Idempotency-Key header draft | https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ (draft -08) | ok |
| 21 | OWASP SSRF cheat sheet, unverified | https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html opens, title matches | open (status can be raised) |
| 22 | Meta Ad Library API, unverified (site blocked) | https://www.facebook.com/ads/library/api/ still 403 | ok |
| 23 | App Store Connect API | https://developer.apple.com/documentation/appstoreconnectapi | ok |
| 24 | OWASP API10:2023 | https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/ | ok |
| 25 | RateLimit header fields, draft 11 | https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/ (draft -11) | ok |
| 26 | RFC 9745 Deprecation header | https://www.rfc-editor.org/rfc/rfc9745 | ok |
| 27 | Twilio secure webhooks | https://www.twilio.com/docs/usage/webhooks/webhooks-security | ok |
| 28 | RFC 7009 token revocation | https://www.rfc-editor.org/rfc/rfc7009 | ok |
| 29 | Split lost nothing from the merged Connect and Check text | old doc sections 2 to 9 compared line by line | ok |
| 30 | Webhook checks owned by this role | `security-engineer.md` line 12 also lists "webhook signature checks" | open (boundary) |

## 3. DevOps Engineer (`devops-engineer.md`)

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | Not built: no skill, agent or evals | `skills/`, `agents/`, `evals/` listings | ok |
| 2 | The 10 sections exist; 4 modes | the document | ok |
| 3 | Neighbour named "Backend & Integration Engineer" (6 places) | owner's split; `TASKS.md` rows 6 and 6b | fixed |
| 4 | No role may press deploy today | agent Never line 85 | ok |
| 5 | Game & Technical never releases or uploads | `game-technical-engineer.md` lines 48 and 49 | ok |
| 6 | Security incidents go to the Security & Privacy Engineer | `security-engineer.md` lines 31 and 57; `TASKS.md` row 8 | ok |
| 7 | AI Engineer sends infrastructure, secrets register and release plan here | `ai-engineer.md` lines 48 and 81 | ok |
| 8 | QA owns whole-product tests; DevOps the pipeline and test environments | `qa-test-engineer.md` line 91 | ok |
| 9 | Backup plan with the Solution Architect, restore test with the Backend | `solution-architect.md` line 73 also claims "the evidence that a restore was tried" | open (boundary) |
| 10 | Skill lets the assistant deploy after approval | `versioning-release.md` section 4 step 7 | ok |
| 11 | Skill says there is no undo in a store | `platform-targets.md` line 37 | ok |
| 12 | Skill says losing signing keys can block all updates | `platform-targets.md` line 24 | ok |
| 13 | Skill suggests one release per milestone | `versioning-release.md` line 93 | ok |
| 14 | Skill marks SLOs "lite" for medium projects | `engineering-principles.md` section 7 table | ok |
| 15 | Skill says pin dependency versions | `engineering-principles.md` line 60 | ok |
| 16 | Base skill file list and sections | headings of all 10 files | ok |
| 17 | `roles.md` has Release manager and DevOps rows | `roles.md` lines 27 and 28 | ok |
| 18 | Apple phased release: 7 days, pause up to 30 days in total | Apple page (below) | ok |
| 19 | A lost upload key can be reset | Android "Sign your app" page | ok |
| 20 | 35 + 40 = 75 sources, 73 verified, 2 unverified | script count of both tables | ok |
| 21 | "Required reviewers" gate a live environment | GitHub page: on Free, Pro and Team plans required reviewers work only in public repositories | open (plan detail) |
| 22 | Pasted key: "moves it to secrets by name" | section 4: it never uses real secrets without approval | open (wording) |
| 23 | Implementing SLOs | https://sre.google/workbook/implementing-slos/ | ok |
| 24 | Etsy blameless postmortems, unverified | https://www.etsy.com/codeascraft/blameless-postmortems still 403 | ok |
| 25 | AWS hands-off deployments | https://builder.aws.com/content/3ErTKQOTKc5NIw031UePBPxTQ6I/automating-safe-hands-off-deployments | ok |
| 26 | GitHub environments | https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment | ok |
| 27 | GitHub OpenID Connect | https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect | ok |
| 28 | CISA tj-actions alert | https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction (title also names reviewdog) | ok |
| 29 | Apple phased release | https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/ | ok |
| 30 | Play App Signing | https://support.google.com/googleplay/android-developer/answer/9842756 | ok |
| 31 | Play target API level | https://developer.android.com/google/play/requirements/target-sdk (served in Korean; same page) | ok |
| 32 | Unity Build Automation | https://docs.unity.com/en-us/build-automation | ok |
| 33 | GameCI | https://game.ci/docs/ | ok |
| 34 | Android "Sign your app", unverified (redirect loop) | https://developer.android.com/studio/publish/app-signing opens, title matches | open (status can be raised) |
| 35 | Vercel Instant Rollback | https://vercel.com/docs/instant-rollback | ok |
| 36 | PagerDuty incident response | https://response.pagerduty.com/ | ok |

## 4. Split spec (`2026-10-24-backend-integration-split.md`)

| # | Claim | Real file checked | Result |
|---|---|---|---|
| 1 | Backend built and reviewed 2026-10-23 | agent, skill, review file | ok |
| 2 | `model: sonnet`; 8 tools | agent frontmatter | ok |
| 3 | Agent owns the register; provider choice is an approval in step 9 | agent lines 14 and 54 | ok |
| 4 | Descriptions 1,008 and 1,021; limit 1,024 | measured; `validate_agents.py` line 33, `validate_skills.py` line 35 | ok |
| 5 | No `evals/backend-engineer/` | `evals/` | ok |
| 6 | Installed copy older than the repo copy | `~/.claude/agents/backend-engineer.md` 16:55, repo 18:28, files differ | ok |
| 7 | "Nothing is committed" | `git log`: commit `b48752e` added the agent; later changes uncommitted | fixed |
| 8 | Boss list | `agents/orchestrator.md` line 5 | ok |
| 9 | `data-engineer.md` already names an Integration Engineer | lines 34, 59, 66 | ok |
| 10 | Files that name the merged role | grep: `TASKS.md` no longer does; `evals/software-architect/evals.json` was missing | fixed |
| 11 | Office has a Backend zone, no Integration; test lists `backend-engineer` | `event-mapping.md` line 115; `test_install_office.py` line 165 | ok |
| 12 | Skill rules 5 and 7, `method.md` 3 and 5, `checklists.md` 5 hold integration work | the skill files | ok |
| 13 | Phrase "No source list is part of this skill yet" | `SKILL.md` line 47 | ok |
| 14 | Eval format like `evals/ai-engineer/evals.json`, with `setup-fixtures.py` and `GROUND-TRUTH.md` | that folder | ok |
| 15 | Planned eval kinds pass `check_evals.py` | `check_evals.py` (typical, edge, refusal) | ok |
| 16 | `sources.md` in the `check_sources.py` format | `check_sources.py`: IDs `S-AREA-n`, Status exactly `verified` or `unverified` | open (build note) |
| 17 | `install_agents.py --only backend-engineer` replaces the stale copy | script never overwrites a differing file without `--force` | fixed |
| 18 | Headless eval run with `--agent integration-engineer` before install | earlier runs install into `--dest <case>/.claude` | fixed |
| 19 | Two small items left from the 2026-10-23 review | step 9 has provider choice; roster row names the existing folder first | fixed |
| 20 | "Split row 6 in `TASKS.md`" | already rows 6 and 6b | fixed |
| 21 | Evals: at least 3 per mode, one trap each | Backend 3 Build + 3 Review/Fix + 2 out of role; Integration 6 Connect + 4 Check + 1 | ok |
| 22 | 75 sources = 38 + 37, 72 verified, 3 unverified | script count | ok |
| 23 | `opus` is an allowed model | `validate_agents.py` line 10 | ok |

## 5. DevOps spec (`2026-10-24-devops-merge.md`)

| # | Claim | Real file checked | Result |
|---|---|---|---|
| 1 | No DevOps skill, agent or evals | listings | ok |
| 2 | Agents in the repo: architect, backend-engineer, ai-engineer, data-scientist, code-reviewer, orchestrator | `agents/` | ok |
| 3 | Quote of the backend "never deploys" rule | agent line 85, exact text | ok |
| 4 | Game & Technical lines 48 and 49 | the file | ok |
| 5 | `versioning-release.md` section 4 step 7; `github.md` section 6 "Deploy on release" | the files | ok |
| 6 | Security Engineer sends a live break-in to the Incident Responder | `security-engineer.md` line 57 | ok |
| 7 | AI Engineer sends infrastructure work here | `ai-engineer.md` lines 48 and 81 | ok |
| 8 | Three documents claim parts of backup and restore | SA, backend, first DevOps doc | ok (the SA overlap stays, see open 3) |
| 9 | Boss list | `agents/orchestrator.md` | ok |
| 10 | No `check_merge` script; the AI Engineer spec names one | `scripts/`; `2026-10-24-ai-engineer-ai-ops-merge.md` line 62 | ok |
| 11 | Master plan line 54; `roles.md` 27 and 28; "You are the release manager" | the files | ok |
| 12 | "Backend & Integration Engineer" (3 places) | owner's split | fixed |
| 13 | Decision 10: "the Backend's integration register" | split spec: register moves to `docs/integrations/` | fixed |
| 14 | Tools "the same set as the other specialists" | `agents/code-reviewer.md` has 5 tools | fixed |
| 15 | 16 eval cases, 4 per mode, one trap each | the table | ok |
| 16 | Build checks use real scripts | `scripts/` and their arguments | ok |
| 17 | A PreToolUse guard blocks live commands | no agent file uses hooks; `install_agents.py` has no hook handling | open (plan risk) |
| 18 | Status "Not started" | `TASKS.md` row 7 | ok |
| 19 | Role 7 of 22 merged roles | `TASKS.md` rows 1 to 22 (plus 6b after the split) | ok |

## Counts
- Claims checked: 144 (Backend 36, Integration 30, DevOps 36, split spec 23, DevOps spec 19), including 38 outside URLs opened.
- Fixed: 16 (Backend 3, Integration 3, DevOps 1 covering 6 places, split spec 6, DevOps spec 3).
- Open: 11 table rows (Backend 3, Integration 2, DevOps 4, split spec 1, DevOps spec 1), grouped with the pending neighbour renames into the 10 owner findings below.
- Every edited document ends with a "Review pass 2026-10-24" line.

## Open findings for the owner
Each has a suggested default.
1. **Raise three source statuses?** The Fielding thesis, the OWASP SSRF cheat sheet and the Android "Sign your app" page now open with matching titles. Default: raise them to `verified` when each skill's `sources.md` is written, and update the counts then (no count was changed in this pass).
2. **SQLite WAL page** could not be opened here (timeout). Default: keep `verified` from the earlier check; recheck when `sources.md` is written.
3. **Who keeps "the evidence that a restore was tried"?** `solution-architect.md` line 73 says the Architect; the Backend, DevOps and DevOps spec say the Backend Engineer runs the restore test and DevOps checks the evidence. Default: Architect designs the plan, Backend runs the test, DevOps checks it at release; edit `solution-architect.md` line 73 in the rename step.
4. **Neighbour renames still pending** (outside this review's files): `game-technical-engineer.md`, `qa-test-engineer.md`, `solution-architect.md`, `security-reviewer.md`, `ai-engineer.md`, `ua-growth-marketer.md`, `team-roster.md`, `data-design.md`. Store receipt validation in `game-technical-engineer.md` line 45 needs a choice. Default: the Backend Engineer owns the entitlement record and route; the Integration Engineer owns the call to the store API.
5. **Webhook signature checks** appear in both `security-engineer.md` (line 12) and the Integration Engineer. Default: Integration builds them; the Security & Privacy Engineer sets the rule; the Security Reviewer reads the code.
6. **Agent wording:** `agents/backend-engineer.md` line 22 sends deep audits to "the Security Engineer"; the role document says the Security Reviewer. Default: fix in the backend trim step of the split plan.
7. **GitHub required reviewers** work on private repositories only on Enterprise plans. Default: the DevOps plan uses a manual step (`workflow_dispatch`) when the repo is private and not on Enterprise.
8. **Pasted key in DevOps:** "moves it to secrets by name" could read as handling the value. Default: reword to "tells you to put the new key in the secret store and records it by name".
9. **`check_sources.py` status rule:** statuses like "verified (Crossref)" must become plain `verified` with the note moved to the Use column. Default: do this when writing each `sources.md`.
10. **PreToolUse guard has no precedent in the repo.** Default: build and test it as its own step with an eval that tries `terraform apply` and `vercel --prod`; until then the rule is prompt-only, as both specs already say.

## Verdicts
- **Backend Engineer: sound with fixes.** The document matches the built agent and skill; the status label is honest (built, 0 evals). Fixes: the DevOps line, one source venue, one dropped line from the merge.
- **Integration Engineer: sound with fixes.** The boundaries with the Backend and Data Engineer hold, the safety rules are stricter than and consistent with the backend agent, and the eval plan plants a trap in every case. Fixes: the DevOps line, one research note, the interim scheduled job.
- **DevOps Engineer: sound with fixes.** The "it prepares, a person presses" rule is consistent with every neighbour; the store and SLO claims match the live pages. Fix: the retired neighbour name in 6 places. The restore-evidence line with the Solution Architect is still open.
