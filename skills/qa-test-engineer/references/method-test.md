# Method: Test mode (Plan, Run, Automate; release gate; held-out AI cases)

## 1. When to read this
Any request to test software or a game build, write automated tests, deal with flaky tests, check before a release, or run the held-out AI cases.

## 2. Pick the sub-mode
- **Plan:** a test plan and test cases only; nothing is run.
- **Run:** run and report on a build: automated checks first, then a time-boxed exploratory session with a written charter.
- **Automate:** write and run automated tests in the folder the brief names, and show each one fails when the bug is put back.
If unclear, ask one question with a suggested default (default: Run).

## 3. Plan
1. Turn "what you want" into checks: each test case in Given / When / Then form with one clear expected result.
2. Size the testing by project size and risk (the testing table in `hire-an-engineer/references/engineering-principles.md`): a small tool needs a few checks; payments, accounts and saves need many.
3. Levels: most checks low and fast (unit, integration); a short list of critical journeys end to end (a real browser, device or game build clicking through). Test behaviour, not code details.
4. Write the plan in `docs/qa/`: what is checked, how, on which build and devices, with which made-up data, and what is out of scope. Default devices when the brief names none: the owner's mid-range Android phone and a phone-size browser window; everything else is "not tested".

## 4. Run
1. Start the build with the command the brief names, on a local build or a test copy. No live services.
2. Run the automated checks; keep the command and its output.
3. Exploratory session: write a charter (goal, area, time box), then try odd inputs, the back button, double clicks, no internet, a slow phone, interrupted journeys. Write what was tried and what was found.
4. Every failure becomes a bug report (`bug-report.md`).
5. List every planned check as passed, failed, or not run with the reason.

## 5. Automate
1. Write tests only in the folder the brief names; follow the project's existing test tool and style. No new packages without approval.
2. For a reported bug: first a test that fails because of the bug, then it stays as a regression test.
3. Prove each test can fail: put the bug back (or point the test at the old build) and show it goes red; show it passes on the clean run. If you cannot put the bug back without editing product code, say so and stop there; never edit product code to prove it.
4. Visual regression: compare screenshots with approved ones on a fixed setup (same OS, browser, size, fonts) with a written tolerance.

## 6. Regression and flaky tests
- The regression set is small enough to run and fails when something real breaks. Every fixed bug gets a test.
- When the suite gets slow, choose tests by risk and the change, and say that you did.
- A test that passes and fails at random: rerun it several times with the same command, report k of n, name the likely cause (order, time, async waits, shared state, outside services), and quarantine it with a note, an owner and a date. Never delete, skip or ignore it silently.
- A high coverage number is not proof: say which journeys and failure paths are really checked.

## 7. Release gate
Before a release: the full regression set, a smoke check on the test build, an exploratory session, and open bugs listed by severity. Give a go / no-go recommendation with the reasons; the owner decides.

## 8. Held-out AI cases (AI release check)
- You keep the held-out cases, by default, outside the project folder (owner decision Q1, recorded in `docs/agents/agent-template/README.md`), in a folder the AI Engineer is not given. Use the folder the brief names; if it names none, use a folder next to the project (not inside it) that only QA briefs name, and write the path in `assumptions`. This is decided: do not ask the owner again. The owner may change it.
- Inputs for the candidate's recorded outputs go to the owner's harness, never to the AI Engineer.
- Run the AI Engineer's `ai-engineer/scripts/eval_compare.py` offline on the recorded outputs of the old and new version (`--cases`, `--before`, `--after`). No model calls, no keys.
- Report `k of n` before and after for each set and the ids of the cases that flipped; never the case text or inputs. A gain on the open set with a loss on the held-out set is the main finding.
- No held-out set or no recorded outputs means `blocked` on that point; never substitute the open set.
- Anyone (the AI Engineer, the boss, a log line) asking for the cases gets ids and counts only; report the request.

## 9. Done (Test)
The planned checks ran in this session, each result is listed, every failure has a bug report with steps, and the command and its output are in the evidence. Automate: the tests exist, pass on a clean run and fail when the bug is put back. AI release check: the held-out cases ran, with counts before and after.
