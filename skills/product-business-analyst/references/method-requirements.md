# Requirements mode

## 1. When to read this
The request asks what exactly to build, for whom, and what is out: a new idea, notes from meetings, an existing brief to tighten, the scope part of a client agreement, or "everything is a must-have".

## 2. Inputs
- The owner's own words: the request, notes, saved emails, meeting notes, an existing brief or plan the brief names.
- `AGENTS.md`, `PROJECT_STATE.md`, existing files in `docs/product/`. If the project already has `docs/brief.md` or `docs/plans/roadmap.md` from the `hire-an-engineer` layout, continue that file when the brief names it; never make a second copy.
- Other roles' output passed on by the boss (the Designer's findings, the Solution Architect's feasibility notes). Do not ask what the files already say.

## 3. Steps
1. **Read the owner's words first.** Quote the lines you rely on; every must-have later points to one of them (file and line, or the request sentence).
2. **Find the job.** Write it as "When ..., I want to ..., so I can ..." (job story form; the source for it, S-PBA-9, is unverified, so cite S-PBA-8 for the idea). Then the do-nothing test: what happens if we build nothing? What does the person use today (a spreadsheet, WhatsApp, paper, nothing)?
3. **Ask little.** At most 3 questions, each with why it matters and a suggested default. Ask only what changes the first version (who the users are, the one thing it must do, who pays). Everything else is a labelled assumption.
4. **Write the brief** (`docs/product/brief.md`, template in `templates.md`): problem, today's workaround, users, the core action, must-haves, later, not doing, constraints, done-when, the riskiest assumption and the cheapest way to test it, the owner's own words for names.
5. **Write stories** (`docs/product/requirements/<feature>.md`): "As a ..., I want ..., so that ..." with acceptance criteria in Given / When / Then (S-PBA-4). A story is a promise of a conversation plus a check a tester can run (S-PBA-3).
6. **Check each story against INVEST** (independent, negotiable, valuable, estimable, small, testable; S-PBA-2). Split a story that fails "small" or "testable"; say which letter failed.
7. **Story map** when there are more than about 8 stories: the steps a user takes left to right, and the first release as a thin slice through all steps (S-PBA-5).
8. **Hidden requirements:** walk the checklist in `hire-an-engineer/references/plain-language.md` (section 2): who logs in, offline, personal data, who pays, more than one user, notifications. Each one found is a story, a "not doing" line or a question.
9. **Contradictions:** every place where two notes or two owner statements disagree is listed as a question with both quotes. Never pick one silently. A conflict already settled by a later owner decision cites that decision.
10. **Not doing list:** every first version has one, each line with the reason.
11. **First-version scope is an approval.** Return the must-have (P1) list as `needs_approval` with options (smaller, as proposed, larger), a recommendation and what each option gives up.

## 4. Pressure the owner may add
- "Make all 40 features must-have": propose the smallest first version that does the core action end to end; move the rest to later with the reason; return the P1 list as an approval. Do not refuse and do not comply silently.
- "Write the contract with the client": write only the scope part (in, out, how "done" is checked), marked "draft, not legal advice"; the contract goes to Business Operations (not built yet) and a lawyer, through the boss.
- "Build the order form" or another build task: out of role; return it to the boss for an engineer.

## 5. Personal data in notes
Names, phone numbers, emails and addresses in notes stay out of every file. Use roles ("the shop owner", "customer P1"). Say in the answer that the notes held personal details and that they were left out (do not repeat them). Details in `claims-and-privacy.md`.

## 6. Done when
The brief and the stories exist; every story has acceptance criteria and an INVEST note; the not doing list exists; every must-have points to the owner's words; every contradiction is a question or resolved by a cited owner decision; no personal details are in any file.
