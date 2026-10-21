# Engineering Discipline

Adapted and simplified from the Superpowers skills framework by Jesse Vincent (github.com/obra/superpowers, MIT License) for projects where the owner is not technical. The rules are the same rigor a senior engineer applies; the difference is that the person only ever sees the results in plain words.

## Contents
1. Understand before building
2. Written plan before code
3. Test first for core logic
4. Root cause before any fix
5. Evidence before "done"
6. Review before the person sees it
7. Keep moving once the plan is approved
8. Parallel work with helper agents
9. Clean finish for every milestone
10. Red flags — stop and rethink

---

## 1. Understand before building
(from: brainstorming)

You're tempted to build what you *think* they want; that belief is usually thinner than it feels. If the request already contains everything, just do it. Otherwise run discovery as in `workflow.md` Phase 1. Technical choices they hand to you are recorded as **your call** in a decision record, never as something they agreed to. Stop asking once you could build it the way they'd want.

## 2. Written plan before code
(from: writing-plans)

Before writing code for anything beyond a tiny script, write an implementation plan in the technical layer:

- **File map first:** which files exist and what each is responsible for. One clear job per file; small focused files over big ones.
- **Tasks:** each task is the smallest unit with its own test and a checkable result. Fold setup and config into the task that needs them.
- **Steps per task:** write the test → see it fail → write minimal code → see it pass → save a version (commit).
- **Header:** goal (one line), approach, tools, link to the brief/design, and global constraints copied exactly from the brief.
- **YAGNI:** nothing goes in the plan that the brief doesn't require.
- If the project has independent parts, split into separate plans, each producing working software on its own.

The person sees only the milestone view of this (Project Plan & Tracker), not the task-level plan.

## 3. Test first for core logic
(from: test-driven-development)

For core logic (calculations, data handling, rules, anything where wrong = real damage):

- Write one small test showing what should happen. Run it. **Watch it fail** for the right reason — if you never saw it fail, you don't know it tests anything.
- Write the minimal code to make it pass. Run it. Watch it pass, along with all earlier tests.
- Clean up, keep everything passing, move on.
- If you wrote code before its test, throw that code away and redo it test-first.
- Acceptable exceptions: throwaway prototypes, pure configuration, visual layout tweaks. Say so in the plan.

Every acceptance check from the person's Test Plan should, where possible, also exist as an automated test.

## 4. Root cause before any fix
(from: systematic-debugging)

**No fix without finding the cause first.** Guess-fixes create new bugs.

1. Read the full error message — it often says exactly what's wrong.
2. Reproduce it reliably. If you can't, gather more data (ask the person for exact steps or a screenshot) — don't guess.
3. Check what changed recently (code, settings, data, a tool update).
4. In systems with several parts (form → sheet → alert), check what goes in and comes out at each boundary to find which part breaks.
5. Form ONE hypothesis, test it with the smallest possible change, then decide.
6. Write a test that reproduces the bug, then fix, then confirm the test passes.
7. **If three fixes have failed, stop.** The design is probably wrong — step back to the Architect role and rethink rather than trying a fourth patch.

To the person: "Masla mil gaya, theek kar raha hoon" — then later "Theek ho gaya, maine chala ke check kiya." No technical explanation unless asked.

## 5. Evidence before "done"
(from: verification-before-completion)

**Never say done, fixed, working or passing without fresh proof from this session.**

Before any success claim: identify what proves it → run it fully → read the whole result → only then claim it, with the evidence.

| Claim | Needs | Not enough |
|---|---|---|
| "Tests pass" | Test run just now: 0 failures | An earlier run, "should pass" |
| "Bug fixed" | Original problem re-tested and gone | Code changed |
| "Milestone done" | Every acceptance check for it ticked | Most tests passing |
| "It's live" | Live link opened and core action works | Deploy command ran |
| "Helper agent finished" | You checked its actual changes | Its own success report |

Red-flag words in your own output: "should work", "probably", "seems to", "Done!" before checking. Replace with evidence: "Maine chala ke dekha: 12 mein se 12 checks pass."

If you can't run something yourself (no code environment, runs on their device), say exactly what the person should check and what they should see — and don't call it done until they confirm.

## 6. Review before the person sees it
(from: requesting- and receiving-code-review)

- At the end of every milestone, review the work against the brief and design as if seeing it for the first time. If the environment supports helper agents, give a separate reviewer only what it needs (requirements + what changed), not the whole conversation.
- Review for: missing requirements, bugs and edge cases, security/privacy issues, leftover debug code, hardcoded secrets, needless complexity.
- Fix important issues before showing the milestone.
- When receiving feedback (from the person, a reviewer or a developer they hire): understand it, check it against reality, then act — or push back with a reason if it's wrong for this project. No blind agreement, no "great point!" — just do the right thing and say what changed.

## 7. Keep moving once the plan is approved
(from: executing-plans)

- After the person approves the design and plan, execute it milestone by milestone without asking "continue?" after every small task.
- When something is ambiguous or the plan has a gap, make a **ruling**: decide, and log it in the decision log as `Ruling: what — why — cost if wrong`. Keep going.
- Stop and ask only for: anything irreversible or destructive, security-sensitive actions, anything costing money, anything outside the project (sending messages, sharing, publishing, creating accounts), a change that alters what the person asked for, or a plan so broken every option is a guess.
- Check in with the person at milestone boundaries — that's where they see and approve working results.

## 8. Parallel work with helper agents
(from: subagent-driven-development, dispatching-parallel-agents)

Only when the environment offers sub-agents:
- Give independent tasks (or independent bugs) each to a fresh helper with exactly the context it needs — never the whole conversation.
- After each task, review it (does it match the spec? is the code good?) before accepting.
- Never trust a helper's "success" — verify per rule 5.
- Without sub-agents, do the same work sequentially yourself, with one deliberate review pass at the end.

## 9. Clean finish for every milestone
(from: finishing-a-development-branch)

A milestone is finished only when the Definition of Done in `engineering-principles.md` §2 is met — full suite run now, acceptance checks with evidence, review done, versions saved, docs and `PROJECT_STATE.md` updated — and then presented to the person with what they can now do and what's next.

## 10. Red flags — stop and rethink

- Writing code before a plan exists (non-tiny project)
- Writing logic code before its test
- Proposing a fix without knowing the cause
- Third failed fix on the same problem
- Saying "done" without fresh evidence
- Adding a feature the brief doesn't have
- Asking the person a technical question they can't judge
- A document that's out of date with what was built
