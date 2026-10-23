# Mode Release check: is this AI change safe to switch on?

When to read this: a prompt, model, retrieval setting, tool or parameter is about to change in a live AI feature ("we changed the prompt", "move to the new model", "the old model is being retired"). Only for AI-Ops modes; design work uses `method-design-build.md`.

## 1. What you may and may not do
- You compare recorded outputs offline. You never call a model yourself: no keys, no network. If the change needs a live run, return `needs_approval` with the harness and the budget, or say the check ran offline on recorded outputs only.
- You never approve your own change. A change you built is reviewed by another role (QA / Test Engineer or Data Scientist & Analyst) against the held-out set.
- You prepare the switch and the rollback; a human or a code rule flips it.

## 2. Steps
1. **Name the change** in one line and write one row in the prompt register `docs/ai/ops/prompt-register.md` (template below): version, date, what changed, why, model name `unknown` until read live, eval-set version, result, rollback target.
2. **Collect two sets of recorded outputs**: the current version and the candidate, run on the same inputs. No recorded outputs for the candidate means no result: say "ran nothing" and list what is needed.
3. **Two eval sets, never mixed.**
   - Open set: the cases the builder knows and may tune on (`docs/ai/eval-set.*`).
   - Held-out set: cases the builder has not seen, kept by QA / Test Engineer or the Data Scientist & Analyst. If it does not exist, the release check is `blocked` on that point; do not substitute the open set [S-AIO-1], [S-AIO-2].
4. **Compare case by case** with `scripts/eval_compare.py` (offline, standard library): it prints `k of n` for before and after on each set and lists cases that flipped from pass to fail (regressions) and fail to pass.
5. **Read the flips, not only the totals.** A gain on the open set with a loss on the held-out set is overfitting to the open set: report it as the main finding [S-AIO-14]. A new regression in a refusal or attack case is a blocker whatever the totals say [S-AIO-6].
6. **Model change.** Provider models change and get retired: read the provider's deprecation page live before you name dates [S-AIO-16], [S-AIO-17]; behaviour can drift even with the same name [S-AIO-15]. A model upgrade is a release check with its own recorded outputs, never a name swap.
7. **Cost and latency of the candidate** from recorded token counts with the formula in `cost-latency-quota.md`; a candidate that doubles the bill is a finding even if quality is equal.
8. **Rollback note**: the exact previous version, where it is, who flips it back, and the signal that triggers it. Feature-flag style switch by a human or code rule [S-AIO-26]; keep versions numbered [S-AIO-27] and changes listed [S-AIO-28].
9. **Verdict** in plain words: `ready` (both sets pass the agreed bar, no new refusal or attack regression), `not ready` (with the cases), or `blocked` (missing held-out set or missing outputs). The verdict stays a recommendation; the owner or reviewer decides.

## 3. Judges
If a model grades the outputs, check the judge against human labels on a sample first and report agreement [S-AIO-7], [S-AIO-8], [S-AIO-9]; details in `evals-and-judges.md`. Without that check the grade is `inferred`.

## 4. Prompt register template (`docs/ai/ops/prompt-register.md`)
| Version | Date | Change and why | Model (read live) | Eval set version | Open set | Held-out set | Reviewer | Rollback to |
|---|---|---|---|---|---|---|---|---|
| v1 | YYYY-MM-DD | first version | unknown | e1 | k of n | k of n | name or role | none |

Tools such as prompt registries exist [S-AIO-10], [S-AIO-11], [S-AIO-12]; a table in the repo is enough for a small studio.

## 5. Output
Files: the register row, `docs/ai/ops/release-check-<date>.md` (change, sets, `k of n` before and after, flips, cost, verdict, rollback note). Handoff `evidence`: the runner command and its printed lines, and the list of what was not run.
