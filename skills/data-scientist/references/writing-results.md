# Writing results, reproducibility and the handoff

When to read this: before writing the analysis file and the final answer, on every job.

## 1. Where things go

- Analysis write-up: `docs/analysis/<yyyy-mm-dd>-<topic>.md` (a new file per job; never overwrite an earlier one, add `-2` instead).
- Scripts: `docs/analysis/scripts/<yyyy-mm-dd>-<topic>.py`, or the folder the request names. Inputs are read-only; scripts never write into `data/`.
- Nothing else is written. No product code, no data files, no other roles' documents.

## 2. Reproducible by default

- One script produces every number in the write-up; running it again prints the same output [S-COM-3].
- Fixed random seeds (`random.Random(42)`), stated in the write-up.
- Record: input file names and row counts, the date of the data, Python version, libraries used (standard library or which installed ones).
- Raw data untouched; cleaning is code [S-COM-4].
- If a number was computed in a quick one-off command, move it into the script before using it.

## 3. Write-up template

```markdown
# <Topic> (<date>)

**Answer:** <one or two sentences, with the number, its range, and how sure: clear / likely / can't tell / can't be answered with this data>

**Decision for the owner:** <the action and the recommendation, or "none">

## Question
Decision, question, metric (exact definition), population, time window.

## Data checks
File, rows, grain; what was found (duplicates, units, missing, time zone) with counts and what was done.

## Method
What was computed and how (test, interval, split, baseline). Assumptions.

## Results
Small table of the key numbers with intervals. Sensitivity (the answer under the other reasonable choice).

## What this does not show
Causation, populations not covered, things not checked, data that would change the answer.

## Next step
The smallest useful next action (a test, more data, a definition to agree).

## Reproduce
`python docs/analysis/scripts/<file>.py` -> prints <the key lines>. Seed, versions.
```

Keep it short: a simple question gets a ten-line write-up.

## 4. Writing for a non-technical owner

- Lead with the answer and how sure you are, then at most three points, then what the owner must decide [S-COM-1].
- Numbers in the owner's units (users, dollars, percentage points), rounded sensibly; say "percentage points" when subtracting rates.
- Uncertainty in plain words and numbers together: "about 4,000, likely between 3,500 and 4,500" [S-COM-5].
- Charts, if any, show uncertainty and start bar axes at zero [S-COM-2]. Text charts are fine when no plotting library is installed.
- Jargon gets a one-line explanation the first time ("sample ratio mismatch: the groups are not the sizes we planned, which means something broke").

## 5. The handoff answer

Every answer ends with the 7-field JSON, even when the request was a plain question:

- `status`: `done` when the analysis is finished and nothing waits on the owner; `needs_approval` when the analysis is finished but an owner decision is pending (rollout, price, budget, sharing data, spend); `needs_answers` only when a missing fact would change the conclusion and no default is defensible; `blocked` when the data cannot be read or is missing. A request outside the role that involves spend, accounts or installs is `needs_approval`, not `blocked` (`privacy-and-safety.md` §4).
- `summary`: plain language, the owner's language (as named in the request constraints, otherwise the language of the request), answer first.
- `files`: the write-up and scripts created.
- `questions`: each with `id`, `question`, `why` (and a suggested default inside the question).
- `approvals`: each with `id`, `decision`, `options`, `recommended`, `one_way_door` (true for sharing personal data, spending, irreversible launches).
- `assumptions`: definitions and defaults you chose (time zone, refunds, significance level, MDE).
- `evidence`: the command you ran and the key output lines with row counts ("python docs/analysis/scripts/2026-10-24-revenue.py: 1,512 rows, 12 duplicates removed, net revenue for the month printed"). Also say what you did not run.

## 6. Labels

Mark claims in the write-up as `verified` (computed from the data or read in a file), `inferred` (reasoned, not checked) or `unknown`. Never present an inference as a measurement.
