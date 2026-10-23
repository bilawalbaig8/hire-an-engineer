# Review: Creative & Art Director, Writer, UA & Growth Marketer, Product & Business Analyst

Date: 2026-10-24. Scope: the role documents and specs of four roles that are not built yet. Nothing was built. No skill, agent, eval or script was changed. Only the documents below were edited, with the smallest fix and a "Review pass" line at the bottom.

Summary: 152 claims checked, 15 fixed in the documents, 13 open findings for the owner (two are shared by two roles, two cover all four roles). All four roles are sound with fixes. The biggest open point is that the Writer and the UA & Growth Marketer both say they write ad copy, store text, posts and email text.

## Method

- **Map and territory (main test).** Every checkable claim was compared with the real file: `agents/*.md` (tools and model), `agents/orchestrator.md`, `skills/orchestrator/references/`, `skills/hire-an-engineer/references/`, `TASKS.md`, `scripts/`, `evals/`, the old part documents, `docs/agents/visual-office/event-mapping.md`, the owner's skills in `~/.claude/skills/`, and the model table in `~/.claude/CLAUDE.md`.
- **Sources.** A standard-library Python script fetched all 140 source URLs in the four specs (35 each) and read the page title or the Open Library / Crossref record. In addition, 40 pages were opened with WebFetch (10 per role), including a re-try of every source the specs list as unverified.
- **Thinking skills.** Pre-mortem and inversion on the boundaries and the eval plans. Red-team only where there is a concrete path (one finding: Writer Bash). Steel-man on the model choices and the merges. Bayesian check on "verified" labels: a matching title raises confidence that the page exists, not that every claim in it is right. Jobs-to-be-done on the boss versus Product & Business Analyst split.
- **Result labels.** ok = the claim matches the real file or page. fixed = it did not match and the document was corrected. open = the owner must decide, or it is a risk and not a factual error.

Files edited:
- `docs/superpowers/specs/2026-10-24-creative-art-director-design.md`
- `docs/agents/roles/writer.md`
- `docs/superpowers/specs/2026-10-24-writer-merge.md`
- `docs/superpowers/specs/2026-10-24-ua-growth-merge.md`
- `docs/superpowers/specs/2026-10-24-product-business-analyst-design.md`

`creative-art-director.md`, `ua-growth-marketer.md` and `product-business-analyst.md` had no factual errors and were not edited.

## 1. Creative & Art Director

Documents: `docs/agents/roles/creative-art-director.md`, `docs/superpowers/specs/2026-10-24-creative-art-director-design.md`.

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | No skill, agent or evals exist | `skills/`, `agents/`, `evals/` listings | ok |
| 2 | Role 12 in `TASKS.md` | `TASKS.md` roles table | ok |
| 3 | Wave 2 "Creative lanes", Ads Factory steps 4 to 6 | `TASKS.md` (current table has no wave column; an earlier version of the file had it) | fixed (source noted) |
| 4 | "22 bigger roles" | `TASKS.md` heading "Roles (23)" after the 6 / 6b split | fixed |
| 5 | Neighbour numbers: Artist 13, Video & Sound Editor 14, Writer 16, Designer 17, UA 19, QA 9 | `TASKS.md` | ok |
| 6 | Data Scientist and AI Engineer have Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch | `agents/data-scientist.md`, `agents/ai-engineer.md` | ok |
| 7 | No agent has an image generation tool | all `agents/*.md` tool lines | ok |
| 8 | The Read tool shows PNG and JPG to the model | Read tool description in this setup | ok (it also reads PDF pages; see open finding C4) |
| 9 | `visual-quality.md` section 2: one idea, competitor swap, never invent proof | `skills/hire-an-engineer/references/visual-quality.md` | ok |
| 10 | Section 5 design record; section 6 judge screenshots, 1 s and 5 s glance, squint, severity 4 to 1 | same file | ok |
| 11 | `visual-quality.md` is written for web pages | same file (capture widths 1440/768/390 px) | ok |
| 12 | The skill has no games or ad-creative reference | `skills/hire-an-engineer/references/` listing | ok |
| 13 | 7-field handoff | `docs/agents/agent-template/handoff-contract.md` | ok |
| 14 | Eval case fields `id`, `prompt`, `kind`, `expect` (README step 4) | `docs/agents/agent-template/README.md` line 12 | ok |
| 15 | `agent.md` template and `verify-ground-truth.py` pattern exist | `docs/agents/agent-template/`, `evals/data-scientist/` | ok |
| 16 | Higgsfield and Adobe connectors exist in the owner's main session, not in specialists | this session's tool list; `agents/*.md` | ok |
| 17 | The role document has the 10 sections | `creative-art-director.md` | ok |
| 18 | 18 eval cases, 4 per mode plus 2 shared, a trap in each | spec section 8 | ok |
| 19 | Open questions each have a default | spec section 12 (6 questions) | ok |
| 20 | Model `opus` | owner's table in `~/.claude/CLAUDE.md` | open (C1) |
| 21 | Folders `docs/creative/...` | grep of all docs, specs, agents and skills | ok (no other role claims them) |
| 22 | 35 sources, 32 verified, 3 unverified; counts per area | spec section 14 rows | ok |
| 23 | S12, S13 unverified (GDC Vault maintenance) | re-tried with WebFetch and script: redirect to `gdconf.com/gdc-vault-maintenance/` | ok (still unverified; note added) |
| 24 | S23 unverified (AppLovin blog index) | re-tried: 301 to `applovin.com/en/blog` | ok (still unverified; note added) |
| 25 | S21 Meta: real gameplay, early hook, sound-off, clear call to action, refresh | WebFetch of the Meta page | ok |
| 26 | S27 and role doc: UK ASA banned Playrix ads for unrepresentative gameplay, the disclaimer did not fix it | WebFetch of the ASA ruling (30 September 2020) | ok |
| 27 | S28 Mutant Box: year "not checked", body not read | WebFetch: ruling 5 April 2017, game "Liberators", upheld | fixed (year and outcome filled in) |
| 28 | S20 Google Ads: AI labels required in some regions | WebFetch: EU, India and New York named | ok |
| 29 | S22 Unity, Emmanuel Bergman, 2025 | WebFetch: 22 October 2025 | ok |
| 30 | S32 Valve "AI Content on Steam", 2024 | WebFetch: title matches, no date shown | open (C3, minor) |
| 31 | S34 C2PA 2.2 | WebFetch: 301 to `spec.c2pa.org`, same path | ok |
| 32 | S07 Wheeler, 2003 | Open Library search: records for 2003, 2008 and 2012 | ok |
| 33 | Other 25 source titles | script title fetch | ok |
| 34 | Boundaries with Artist, Designer, UA, Art QA | role documents and specs of the neighbours | ok |
| 35 | Boundary with the Writer on hooks | `writer.md` sections 3, 4 and 8 | open (C2) |
| 36 | Legal and rights points are flags, "not legal advice" | role doc sections 2, 4, 10; spec section 14 | ok |
| 37 | Nothing claimed beyond what was measured (Read tool to be confirmed by eval R1; sizes are estimates) | spec sections 6, 9, 11 | ok |

## 2. Writer

Documents: `docs/agents/roles/writer.md`, `docs/superpowers/specs/2026-10-24-writer-merge.md`.

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | No skill, agent or evals exist | `skills/`, `agents/`, `evals/` | ok |
| 2 | Role 16, status "Parts, not merged yet" | `TASKS.md` now says "Documented", build "Not started" | fixed |
| 3 | "22 bigger roles" | `TASKS.md` (23 rows) | fixed |
| 4 | `storyboard-scriptwriter.md` has 42 sources, 40 verified, 2 unverified | that file, line 134 and table | ok |
| 5 | Old folder `docs/storyboards/`; nothing exists there | `storyboard-scriptwriter.md` line 59; `docs/` listing | ok |
| 6 | `ux-ui-designer.md` says "Content Writer" and "long-form or marketing copy" | that file, line 36 | ok |
| 7 | `video-editor.md` says "Storyboard / Scriptwriter" | that file, lines 31 and 53 | ok |
| 8 | `performance-ua-marketer.md` says "the Ad Marketer owns ad copy" | that file, line 39 | ok |
| 9 | `creative-art-director.md` already says "Writer" | that file, section 4 | ok |
| 10 | `ui-ux.md`: users' language, right-to-left and fonts for Urdu | `ui-ux.md` line 85 | ok |
| 11 | `roles.md` rows "Technical writer" and "DevOps / support" | `roles.md` lines 28 and 30 | ok |
| 12 | `documents.md` sections 1, 2 and 5 (User guide and Handoff skeletons) and section 6 (docs in the same change as code) | `documents.md` lines 17, 61 to 63, 99 | ok |
| 13 | `versioning-release.md` section 5: changelog and plain release notes | that file, section 5 | ok |
| 14 | All specialists except the Code Reviewer have the 8 tools; the Code Reviewer has 5 | `agents/*.md` | ok |
| 15 | No agent has a helpdesk, store, social or translation connector | `agents/*.md` | ok |
| 16 | `check_sources.py` columns ID, Title, Author, Year, URL, Use, Cost/licence, Status | `scripts/check_sources.py` line 12 | ok |
| 17 | Eval folder layout | `evals/data-scientist/` | ok |
| 18 | No `check_merge` script; the AI Engineer spec names one | `scripts/`; `2026-10-24-ai-engineer-ai-ops-merge.md` line 62 | ok |
| 19 | The role document has the 10 sections | `writer.md` | ok |
| 20 | 3 or more cases per mode (16) plus 1 out-of-role (17), a trap in each | spec section 5 | ok |
| 21 | Open questions each have a default | spec section 6 | ok |
| 22 | Model `sonnet`, effort medium | owner's table: docs and ordinary work = Sonnet, medium | ok |
| 23 | Folder `docs/writing/` | grep of docs, specs, agents, skills | ok (no collision); README and CHANGELOG are shared files: open (W4) |
| 24 | Microsoft rule of thumb: about 40 percent text growth | WebFetch of Microsoft Learn "Pseudolocalization" | ok |
| 25 | English has 2 plural forms, Arabic 6 | WebFetch of CLDR "Plural Rules" (English two shown); Arabic six is from the CLDR data, not stated on that page | ok |
| 26 | UK data request answered within one month | WebFetch of ICO "A guide to subject access" | ok |
| 27 | Apple refunds go through reportaproblem.apple.com | WebFetch of Apple Support 118223 | ok |
| 28 | Google Play: "the developer usually handles them, so your policy decides" | WebFetch: the developer can refund under its policy; Google can also refund some purchases | fixed (role doc and spec row 31) |
| 29 | FTC: evidence before the ad runs | WebFetch: "The law requires that advertisers have proof before the ad runs" (edited January 2025) | ok |
| 30 | Mailchimp guide may be adapted "under a Creative Commons licence with credit" | WebFetch: CC BY-NC 4.0 (non-commercial); the repo is MIT | fixed (spec row 5 and build plan) |
| 31 | ISO 17100 unverified (403) | re-tried: WebFetch 403, script fetch 200 with matching title | fixed (verified by title only; counts now 35 of 35) |
| 32 | Source counts per area 5, 6, 14, 6, 3, 1 | spec section 8 rows | ok |
| 33 | Help Scout 2025 | WebFetch: 18 March 2025 | ok |
| 34 | Zendesk macros page | WebFetch: title matches | ok |
| 35 | Other 25 source titles | script title fetch (FTC returned 404 to the script but opened with WebFetch) | ok |
| 36 | Bash only for read-only commands "for example `--help`" | red-team of the rule | open (W3) |
| 37 | Writer writes store copy, ad copy, posts and email text | `ua-growth-marketer.md` sections 2, 4 and 7 say UA writes them | open (W1) |
| 38 | The Creative & Art Director "sets the hook"; the Writer writes "at least three hooks" | `creative-art-director.md` section 4; `writer.md` sections 3 and 8 | open (W2, same as C2) |
| 39 | Legal, medical and data-request text is a draft, "not legal advice" | role doc sections 3, 4, 9 | ok |

## 3. UA & Growth Marketer

Documents: `docs/agents/roles/ua-growth-marketer.md`, `docs/superpowers/specs/2026-10-24-ua-growth-merge.md`.

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | No skill, agent or evals exist | `skills/`, `agents/`, `evals/` | ok |
| 2 | Role 19, wave 3, "Parts, not merged yet" | `TASKS.md` now: no wave column, "Documented", build "Not started" | fixed |
| 3 | "22 bigger roles" | `TASKS.md` (23 rows) | fixed |
| 4 | `performance-ua-marketer.md`: 40 sources, 36 verified, 4 unverified | that file, line 87 and table | ok |
| 5 | Meta Advertising Standards was unverified there and is now verified | old doc line 110; WebFetch: "Introduction to the Advertising Standards" | ok |
| 6 | Old folder `docs/ua-marketing/`; nothing written there | old doc line 59; `docs/` listing | ok |
| 7 | Master plan standing rule quote | `2026-10-22-agent-team-master-plan.md` line 80 | ok |
| 8 | Creative doc sends "budget, targeting and launch" and "test setup" to UA | `creative-art-director.md` says "test setup, budget, launch and reading the campaign" | fixed (quote corrected) |
| 9 | Built specialists have the 8 tools and no connectors | `agents/*.md` | ok |
| 10 | Owner's setup has Pubforce (Adjust data) and Klaviyo, Supermetrics, Ahrefs, Similarweb, Amplitude connectors | this session's tool list | ok |
| 11 | Boss rule "use the model the roster gives" | `agents/orchestrator.md` line 63 | ok |
| 12 | Skills `ads`, `ad-creative`, `aso`, `ai-seo`, `social`, `emails`, `influencer-marketing`, `public-relations` exist outside the repo | `~/.claude/skills/` listing: all 8 present | ok |
| 13 | `emails` has no consent, CAN-SPAM or sender-authentication content | grep: only unsubscribe-rate lines, no consent, CAN-SPAM, SPF, DKIM or DMARC | ok |
| 14 | One reference names the "marketingskills" collection; licence not checked | `social/references/listening.md` line 279; no licence file found | ok |
| 15 | Scripts list | `scripts/` listing | ok |
| 16 | No `check_merge` script | `scripts/` | ok |
| 17 | `cost-management.md`, `integrations.md` ("Ad network / analytics events", transactional email), `platform-targets.md`, `thinking-toolkit.md` | those files | ok |
| 18 | The role document has the 10 sections | `ua-growth-marketer.md` | ok |
| 19 | 3 cases per mode (12) plus 2 cross-mode, a trap in each | spec section 6 | ok |
| 20 | Open questions each have a default | spec section 7 | ok |
| 21 | Model `opus` | owner's table | open (U1) |
| 22 | Folder `docs/marketing/` | grep of docs, specs, agents, skills | ok (no collision) |
| 23 | Boundary with Data Scientist & Analyst Growth mode | `2026-10-24-data-scientist-analyst-merge.md` lines 78, 82, 84, 100; `data-scientist.md` lines 46, 66, 73 | open (U2) |
| 24 | Boundary with the Writer | `writer.md` | open (U3, same as W1) |
| 25 | Source counts per area 10, 3, 5, 7, 5, 4, 1 | spec section 9 rows | ok |
| 26 | Apple product page optimization: up to three treatments | WebFetch | ok |
| 27 | Apple custom product pages: up to 70 | WebFetch | ok |
| 28 | Gmail: from February 2024, SPF or DKIM, spam rate below 0.3 percent, one-click unsubscribe above 5,000 a day | WebFetch of Gmail Help 81126 | ok |
| 29 | Google Play: no incentivised ratings | WebFetch: "Don't offer rewards or incentives for ratings or reviews" | ok |
| 30 | FTC reviews rule (2024) covers fake social media indicators | WebFetch: November 2024, section 465.8 | ok |
| 31 | FTC COPPA FAQ, Rule amended 2025 | WebFetch: amended 22 April 2025 | ok |
| 32 | ASA/CAP influencers' guide, 4th edition, made with the CMA | WebFetch: 4th (2026) edition, with the CMA | ok |
| 33 | TikTok row: ad creatives and landing page policy page | script and WebFetch: redirects to the general "TikTok Advertising Policies" index | fixed (note added) |
| 34 | CRTC unverified (403) | re-tried with WebFetch and script: 403 | ok (still unverified; note added) |
| 35 | Other 25 source titles | script title fetch (FTC pages 404 to the script, opened with WebFetch) | ok |
| 36 | Status label "Not started (0 of 4 modes)" | other three roles say "Not built (0 of n modes)" | open (X1) |
| 37 | Policy, privacy and consent points are flags, "a human or lawyer decides" | role doc sections 4, 5, 8, 9 | ok |
| 38 | No spending, posting, sending or logging in | role doc section 4; proposed tools have no connectors | ok |

## 4. Product & Business Analyst

Documents: `docs/agents/roles/product-business-analyst.md`, `docs/superpowers/specs/2026-10-24-product-business-analyst-design.md`.

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | No skill, agent, evals or roster row | `skills/`, `agents/`, `evals/`, `docs/agents/roster.md` | ok |
| 2 | Role 21, Wave 4 "not needed for Ads Factory" | `TASKS.md` (no wave column now; an earlier version had it) | fixed (source noted) |
| 3 | Boss allowlist is `Agent(architect, code-reviewer, ai-engineer, data-scientist)`; roster lists `backend-engineer` | `agents/orchestrator.md`; `docs/agents/roster.md` line 13 | ok |
| 4 | Boss writes `plan.md`, `decisions.md`, `summary.md` in `.team/runs/` and logs with `team_event.py` | `skills/orchestrator/references/run-method.md`; `skills/orchestrator/scripts/team_event.py` | ok |
| 5 | `docs/decisions/` belongs to the Solution Architect | `docs/agents/roster.md` line 9; `team-roster.md` line 7 | ok |
| 6 | Office registry lists `pm` and `ba`; UI files too | `event-mapping.md` lines 111 and 112; `visual-office/index.html` | ok |
| 7 | `ux-ui-designer.md` and `performance-ua-marketer.md` "still name Product Manager" | grep: 4 in `ux-ui-designer.md`, 0 in `performance-ua-marketer.md` (it has other old names) | fixed |
| 8 | `creative-art-director.md` already names "Product & Business Analyst" | that file, lines 58, 69, 85 | ok |
| 9 | `project-management.md` prefers the owner's board tool through a connector | that file, line 22 | ok |
| 10 | Eval layout as in `evals/data-scientist/` | that folder | ok |
| 11 | The Backend Engineer is a `sonnet` precedent | `agents/backend-engineer.md` | ok |
| 12 | `project-management.md`: P0 to P3 and Won't, about 30 percent buffer, On track / At risk / Blocked, risk register from a pre-mortem, change requests and a decision log | that file, lines 54 to 58, 72, 81, 93, 95 | ok |
| 13 | `workflow.md` Phase 1 discovery and Phase 2 brief (must-haves, later, non-goals, done-when, riskiest assumption) | that file, lines 9 to 13 | ok |
| 14 | `thinking-toolkit.md`: job to be done, do-nothing test, riskiest assumption and cheapest test, pre-mortem, second-order effects | that file | ok |
| 15 | `documents.md` brief and plan skeletons | that file, section 5 | ok |
| 16 | `plain-language.md` hidden-requirements checklist | that file, section 2 | ok |
| 17 | `templates.md` decision record format | that file | ok |
| 18 | `roles.md` quotes "each must-have traceable to their words", "board current? anything waiting on the person?" | `roles.md` lines 16 and 19 | ok |
| 19 | One owner per file, as in `team-roster.md` | `team-roster.md` line 25 | ok |
| 20 | The role document has the 10 sections | `product-business-analyst.md` | ok |
| 21 | 19 eval cases, 3 or more per mode, a trap in each | spec section 8 | ok |
| 22 | Open questions each have a default | spec section 12 | ok |
| 23 | Model `sonnet`, effort medium | owner's table | open (P1) |
| 24 | Folder `docs/product/`, continuing `docs/brief.md` and `docs/plans/roadmap.md` when named | grep; `documents.md` scaffold tree | ok (no collision) |
| 25 | "The boss reads `docs/product/backlog.md` and `delivery/plan.md` to choose the next job" | `run-method.md` and `team-roster.md` have no such step | open (P2) |
| 26 | Orange Book, 2020 | WebFetch: current edition May 2023 | fixed |
| 27 | S-PBA-9 Klement unverified | re-tried: script timeout, WebFetch failed | ok (still unverified; note added) |
| 28 | Kano et al. 1984 (J-STAGE) | WebFetch: title, four authors, 1984 | ok |
| 29 | Braun and Clarke 2006 (Crossref) | WebFetch: Qualitative Research in Psychology 3(2), 2006 | ok |
| 30 | Gurley, 11 July 2014 | WebFetch | ok |
| 31 | Cagan, The Four Big Risks, 2017 | WebFetch: 4 December 2017, value, usability, feasibility, viability | ok |
| 32 | The Mom Test page | WebFetch: title and author match; "past behaviour" is from the book, not stated on the page | ok (the spec already says paid books are cited for the idea) |
| 33 | BABOK v3 | WebFetch: v3 inferred from errata and product code | ok |
| 34 | Torres, Opportunity Solution Trees | WebFetch | ok |
| 35 | Kanban Guide 2025 | WebFetch: v2025.5, May 2025 | ok |
| 36 | Wiegers and Beatty, 3rd edition, 2013 | Open Library: 2013 record of the 3rd edition | ok |
| 37 | Other 24 source titles | script title fetch | ok |
| 38 | Privacy and legal points are flags, "not legal advice" | role doc sections 3, 4, 10 | ok |

## Open findings the owner must decide

**Across the four roles**
- **W1 = U3. Who writes short marketing copy?** `writer.md` says the Writer writes store pages, ad copy, social posts and email text (Content mode). `ua-growth-marketer.md` says the UA & Growth Marketer writes "short marketing copy (ads, store text, posts, emails, press drafts)" and leaves only long-form and localisation to the Writer. Both cannot be true. Suggested default: the UA & Growth Marketer owns copy that is part of a test or campaign (ad headlines, store test variants, email drafts); the Writer owns the style guide, the glossary, store descriptions, release notes and all translation. Then fix both role documents in one pass.
- **C2 = W2. Who writes the hook?** The Creative & Art Director "sets the idea, the hook and the tone"; the Writer writes "at least three hooks" for each script. Suggested default: the Director names the hook type per concept; the Writer writes the words of the hook variants.
- **X1. Status labels differ.** Creative and Writer say "Not built (0 of n modes)", UA says "Not started (0 of 4 modes)", PBA says "Tested (k of 4 modes)" once built; `TASKS.md` uses "Not started". Suggested default: one label set as in `TASKS.md` ("Not started", "Built, not tested", "Tested (k of n modes)").
- **X2. Source tables are not yet in the `check_sources.py` format.** The Creative, Writer and UA tables have no `Use` and `Cost/licence` columns, so these values were never collected. The PBA table already has the right header. Suggested default: fill the two columns at build time, before `check_sources` is run.

**Creative & Art Director**
- **C1. Model and effort.** `opus` fits the owner's table for work that is hard to undo (a wrong direction, a misleading ad), but briefs and style guides are ordinary writing work, and no effort level is given. Suggested default: `opus`, effort high, as the table says for Opus; consider `sonnet` if eval R1 shows image review is not possible.
- **C3. S32 year.** The Steam page shows no date; "2024" is not confirmed. Minor.
- **C4. PDF.** The Read tool also reads PDF pages. Brand guides often come as PDF. Suggested default: add "PDF pages" to "what it can see" when the skill is written, and test it in eval R1.

**Writer**
- **W3. Bash "`--help`" is not always read-only (red-team).** Path: a project script with no argument parsing (for example `deploy.py`) runs its main code when started with `--help`; a Writer checking a README step would run it. Suggested default: in Technical docs mode the Writer only lists and reads files and runs its own `check_strings.py`; any project command is marked `not run` or run by an engineer or QA. This also means few steps can honestly be marked `tested` by the Writer.
- **W4. Shared files.** The Writer edits `README.md` and `CHANGELOG.md`, which engineers and the boss also edit; `team-roster.md` says one owner per artifact. Suggested default: the Writer edits them only when the brief names them (already the rule for `CHANGELOG.md`; extend it to `README.md`).

**UA & Growth Marketer**
- **U1. Model and effort.** Open question 4 already asks; no effort level is given. Steel-man for `sonnet`: the role only advises and drafts, every money step is an approval, and the Data Scientist & Analyst checks any scale-up read.
- **U2. Overlap with Data Scientist & Analyst Growth mode.** The DS merge spec lets Growth mode return a bid recommendation ("set the bid for tomorrow" leads to a recommendation as an approval) and puts growth reads in `docs/analytics/growth/`; UA puts results reads and bid recommendations in `docs/marketing/ua/`. Two roles could write two bid recommendations and two reads of one campaign. The DS documents also still say "Performance / UA Marketer". Suggested default: bid and budget recommendations only from UA; DS gives the numbers and the verdict; one results file per test, owned by UA, linking the DS read.

**Product & Business Analyst**
- **P1. Model.** The owner's table gives "plans and specs for large work" to Opus and "search, read, summaries" to Sonnet. Requirements and priorities are planning work. The spec chose `sonnet` with a step-up rule after two failed evals. Suggested default: keep `sonnet` with the step-up rule, as open question 4 says.
- **P2. The boss reading the product backlog is a change to the boss.** The spec says the boss reads `docs/product/backlog.md` and `delivery/plan.md` to pick the next job, but `run-method.md` and `team-roster.md` have no such step, and build step 5 lists only the allowlist and routing lines. Suggested default: add "read the product backlog when it exists" to the boss's run method in the same wiring step, with the owner's OK.

## Verdicts

| Role | Verdict | Why |
|---|---|---|
| Creative & Art Director | sound with fixes | Claims match the files; three small source fixes made. The open points are the model level and the hook line with the Writer. |
| Writer | sound with fixes | Five fixes, one of them a licence point (Mailchimp is non-commercial). The copy overlap with UA and the `--help` rule must be decided before build. |
| UA & Growth Marketer | sound with fixes | Strong facts and rules; four fixes. The copy overlap with the Writer and the bid overlap with the Data Scientist & Analyst must be decided before build. |
| Product & Business Analyst | sound with fixes | The line with the boss is clear and matches `agents/orchestrator.md`; three fixes. The boss-side change for reading the backlog is missing from the build plan. |

Limit of this review: source checks covered page titles, records and the specific facts named above, not every claim inside each source. Script title checks show a page exists today; pages and rules change.
