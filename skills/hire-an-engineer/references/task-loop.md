# Task Loop — one task at a time, from plan to Done, with fixed stops

Contents: 1. Start and resume · 2. Stages · 3. The four stops · 4. Exit rule and rounds · 5. Two tasks at once · 6. Saving time and cost · 7. How to check · 8. Not a reason to skip a stop · 9. Errors · 10. Autopilot

Read when the person names a task from the board ("build #3", "agla task shuru karo", "#3 #4") or asks to resume tasks in progress. Which path applies (and its approvals) is set by the entry table in SKILL.md: Tiny work keeps its short path there; under an active Authorization, §10 governs; otherwise the four stops below. The board is `TASKS.md` (or the tool in `project-management.md` §2); the task's row is the single source of truth, so any session can resume from it.

## 1. Start and resume

| Command | Do |
|---|---|
| `#N` | Start N in the first free slot (§5). |
| `#N #M` | N and M, each in its own slot. |
| No number | Read every board row with a `stage` set and status not Done/Dropped, and resume each (below). **No such row:** say nothing is in the loop and ask which task to start. Never pick one yourself. |
| A task beyond the limit (`delivery-loop.md` §4) | Mark it `queued`, tell the person it waits for a free slot and for their go at Stop 4, start nothing, not even its plan. |

A row with no size counts as Small (`project-cases.md`: pick the smaller size).

**Resuming**
1. Check the slot's folder is on the row's `branch`.
2. Row has `needs` set → say that stop again in chat and wait.
3. Row has no `needs` → **rerun its `stage` from the start.** `stage: verify` means run every check again: what ran before a restart is not evidence now.
4. `queued` rows: mention them as waiting; start nothing.

## 2. Stages

Update the row (`stage`, `status`, `round`, `note`) when entering each stage and before any long step.

**The board** is the one in `project-management.md` §2–§3 (it owns the base fields); this loop adds technical columns to the same rows: `#` · size · stage · round · branch · slot · needs · cost (rounds used; money only where the tool shows it) · note. Status is one of `todo`, `queued` (To do), `progress` (In progress), `review`, `fixing` (In review/testing), `done`, `dropped`; blocked is `needs: help`, never a status. The board lives on the integration branch and is edited from the main folder only, never from a task folder. Diff a task branch with `git diff <base>...HEAD`.

| Stage | Do | Status |
|---|---|---|
| intake | Read the task's board entry and row. Create `task/<num>-<slug>` from the project's integration branch (`github.md`) in the slot. | progress |
| plan | Thinking pass by size (`thinking-toolkit.md` §4): Small: Pre-mortem; Medium + Second-order effects; Large + Devil's advocate and Physics or convention? (`thinking-toolkit.md` §3), and the Attacker's view when it touches login, money, files or the network. Write one line per finding; drop what finds nothing. Plan by size: **Small:** 3–5 lines (approach, files, test) in chat and in the row. **Medium:** one screen (approach, files, tests, risks). **Large:** design and plan documents (`workflow.md`). Write `howToCheck` (§7). → **Stop 1** | progress |
| build | Test-first for core logic (`engineering-discipline.md` §3); commit on the branch as tests go green (locally; pushing: §9). Run only the tests for what changed while building; never the whole suite per commit. | progress |
| review | QA runs the task's tests first; the reviewer reviews only green code. Review the branch diff in a fresh context (`engineering-discipline.md` §6), then the after-build pass: "does the real system match the plan?" and "what can I remove?". Each confirmed finding goes back to build (status fixing). A no-code task (text, docs only) shows the diff summary at Stop 2 instead. | review / fixing |
| verify | The whole suite, **once per branch, in the background** (§6), plus the project's smoke run from `AGENTS.md`. Red → back to build, `round` + 1. Exit rule met → commit → **Stop 2**. | review |
| test | Waiting on Stop 2 / Stop 3. | review |
| finish | Merge by the project's rules (`github.md`), delete the branch, update `PROJECT_STATE.md`, the board and the changelog line. → **Stop 4** | done |

## 3. The four stops

In this order: write the row (`stage`, `needs`, `needsText`), update `PROJECT_STATE.md`, commit, send the chat message, end the turn. Nothing on that task moves until the person answers. For Stop 2, run or open the build for them from the task's folder (or give one click or one command) and say what to try; never ask them to find a folder or branch.

| Stop | needs | Message | Answer that moves on |
|---|---|---|---|
| 1 Approve plan | plan | The plan and the `howToCheck` steps. | Approval → build. Changes → revise, Stop 1 again. |
| 2 Test it | test | The `howToCheck` steps, named for their real screen, device or file. | A clear pass ("works", "chal gaya") → Stop 3. A failure report → reproduce it in the task's folder. Reproduced → failing test, status fixing, `round` + 1, build. Not reproduced → keep `needs: test`, show what ran where, ask; no round. Unclear ("looks good", "ok") → ask once: "Did you try it yourself? Shall I add it in?" |
| 3 Approve merge | merge | "Tried it and happy? Shall I add it in?" | Any clear yes to adding it ("haan, add karo", "yes, merge it"). "Works, add it" in one message passes Stops 2 and 3 together. |
| 4 Next task | none (row is Done) | What was done, evidence, what you have not checked. | List the queued tasks first; the person names the next task (a queued task needs a free slot and their go). Suggest an order if useful; start nothing. |

That yes merges into the integration branch only. Merging to a branch that deploys, or any live change, is a separate approval (SKILL.md rule 2). The hard stops in `delivery-loop.md` §7 (public preview links included) apply here too.

## 4. Exit rule and rounds

Rounds count failures at verify or Stop 2, and in autopilot each review pass that returns a real bug; other review fixes do not. Exit rule (all): the task's tests green · no test from the approved list removed, skipped or loosened (the reviewer checks test changes in the diff) · no confirmed review findings · the whole suite green · the smoke run works. A no-code task needs none of the suites or the smoke: say so in the commit. Not met after round 3 → `needs: help` with the failing check and a best guess, stop. No fourth round without the person's word. In autopilot, `delivery-loop.md` §9 decides what happens to the run.

## 5. Two tasks at once

How many at once: `delivery-loop.md` §4. Each lives in its own folder (a git worktree or clone, outside the project folder or gitignored) on its own branch, so work never mixes. The task waiting for the person's test and the task being built can overlap; two builds at once only when they touch different files. A task waiting at a stop does not block the other. A task approved but waiting for a slot or for another task: `stage: build`, note `waits #N`. When tasks touch the same code, the later one rebases onto the merged one, adds a test for the combined behaviour and reruns verify before its Stop 3. Before handing a slot to a new task, check the folder is clean: if it has files you did not write, list them and ask; never stash, reset or commit them.

## 6. Saving time and cost

- **Tests while building:** the task's own tests plus the tests that import what changed. A change to a shared module runs that suite once. The whole suite runs once per branch (verify) and before merge.
- **Review by risk:** risky parts (money, login, data formats, anything hard to undo) get a review per plan task; everything else is covered by the branch review. Polish findings are listed with at most one fix round; only a real bug (wrong result, crash, data loss) loops.
- **Long jobs** (over about a minute: suites, builds, exports) run in the background with output in a file. Work on something independent or end the turn with one line ("suites running, will report once"). No polling. If the tool doesn't wake you when a background job ends, run it in the foreground.
- **Big output:** read logs and diffs through a filter (counts, first errors, last lines), never whole.
- **Models:** match the model to the work (`cost-management.md` §6): a fresh sub-agent per piece of work is the big saving; strongest tier for risky build tasks and review, mid for the rest, cheapest for running suites and tracker lines. If sub-agents are blocked, do the rest of the session inline and say so in one line.
- **Cost is recorded quietly, never an alert.** Write rounds used (and money only where the tool shows it, labelled) to the row's `cost` at each stop without mentioning it. In autopilot, the cap check before each task is in `delivery-loop.md` §5. At Stop 4, only if they chose to see costs: one line, "rounds used: N" (plus measured money, labelled). Being stuck is handled by the round rule, not by cost.

## 7. How to check

Every task, bug and reported issue says what to check and how. At plan, write 3–8 numbered steps in plain words, each "do this → you should see that", on their real screen, device or file (no code unless the step is opening a file). Cover the change itself, one thing that must still work as before, and for a bug the original failing case. Put the same steps in the plan and send them at Stop 2. A failure at a step becomes a failing test, then fixing.

## 8. Not a reason to skip a stop

Under Authorization, §10 governs.

| Thought | Rule |
|---|---|
| "It's Small / they said just do it" | Stop 1 still applies; the plan is 3 lines. "Just do it" means keep the plan short, not skip it. |
| "They said looks good / ok / great" | Not a clear yes to merge, and not proof they tried it. Ask once. |
| "The suites are green, testing is a formality" | Stop 2 always. Suites are not their screen. |
| "I resumed at verify; it passed before the restart" | Rerun verify. Only this session's output is evidence. |
| "Task done, the next one is obvious" | Stop 4. They pick. |
| "Both slots are full but I can plan a third meanwhile" | Queue it. |
| "The slot is dirty, I'll offer to stash or discard" | Their files. List them, ask; never stash, reset, checkout over them or commit them. |
| "A status like 'blocked' fits better" | Use only the values the board defines; blocked is `needs: help`. Anything else breaks their view. |

## 9. Errors

| Situation | Do |
|---|---|
| Round 3 fails the exit rule | `needs: help`, failing check and best guess, stop (autopilot: `delivery-loop.md` §9 decides). |
| The thing they must test cannot run (app closed, service down) | `needs: help`, say exactly what to open or start; continue when it answers. |
| Slot dirty at hand-over | `needs: help`, list the files, stop. |
| Merge or rebase conflict | Resolve technical conflicts and rerun the suite; ask only when the two sides differ in behaviour they would notice. |
| Board write conflict | Re-read, retry once, then report in chat. |
| Permission denied or tool missing | `needs: help` with exactly what to allow or run. |

Reply in the language of their messages. Commits happen in their repo only. **Pushing:** default is commit locally. Push a branch only when Authorization or `PROJECT_STATE.md` records `branch pushes deploy: no` (previews included) and `repo visibility: private`, or the person approved pushing; unknown counts as deploys, and a push to a public repo is publishing (SKILL.md rule 2).

## 10. Autopilot

When the person gave the one approval in `delivery-loop.md` §3 (Authorization recorded in `PROJECT_STATE.md`), Stops 1–3 are waived:
- **Stop 1:** the plan stays inside the approved plan; record that check in the row.
- **Stop 2:** QA's automated evidence replaces the person trying it: the checks, the "how to check" steps run, and for visual work a screenshot critique (`visual-quality.md`).
- **Stop 3:** merge into the integration branch (`github.md` §3) automatically when the exit rule (§4) is met; never a branch that deploys.
- **Stop 4:** take the next task from the plan.

The person's own try-out happens once, at delivery. Hard stops (`delivery-loop.md` §7) still stop the affected task. If the person says "ask me per task", or has not approved yet, the stepwise stops above apply. After delivery closes the Authorization, follow-up tasks get the fresh one-message yes offered in `delivery-loop.md` §8, not four stops each, unless the person prefers stepwise.
