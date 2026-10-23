# Method: Analyst mode ("what happened")

When to read this: counts, totals, trends, comparisons between groups, cohorts, retention, funnels, revenue. Use with `framing.md`, `data-audit.md` and `writing-results.md`.

## 1. Steps

1. **Frame** the five items (decision, question, metric, population, window). Write them at the top of the report. If the question names dates or a file, use them; do not ask again.
2. **Check the tools**: `python --version`, then `python -c "import pandas"` (and numpy, scipy) to see what is installed. Use the standard library when they are missing; never install.
3. **Audit** with a script (`data-audit.md` §1): rows, grain, duplicates, missing, units, time zone, window, changes over time, who is missing. Print counts.
4. **Clean in code**, never in the raw file: deduplicate by key, convert units, filter the window, exclude test rows. Count rows removed or changed at each step.
5. **Compute** the answer with the same script. Print the intermediate numbers (per group, per week) so a reader can follow.
6. **Size the uncertainty** when the number is used to compare or generalise: an interval for the difference between groups (`honest-inference.md`). A plain total of complete data ("September revenue") needs no interval, but it needs its definition and its caveats.
7. **Check the story**: if the result implies a cause, run the traps in `causal-questions.md` §2 before writing it.
8. **Sensitivity**: when a cleaning choice moves the answer (refunds in or out, time zone, an outlier), show both.
9. **Report** (`writing-results.md`): answer first, how sure, data checks, method, caveats, owner decisions, next step.

## 2. Script skeleton

Save it as `docs/analysis/scripts/<yyyy-mm-dd>-<topic>.py` (or the folder the request names) and run it; paste the key output lines into the report.

```python
import csv
from collections import Counter

PATH = "data/orders.csv"          # read-only input
with open(PATH, encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
print("rows", len(rows), "columns", list(rows[0]))

ids = Counter(r["order_id"] for r in rows)
dups = sum(c - 1 for c in ids.values() if c > 1)
print("duplicate rows", dups)

seen, clean = set(), []
for r in rows:                           # keep the first copy of each id
    if r["order_id"] in seen:
        continue
    seen.add(r["order_id"])
    clean.append(r)
print("after dedup", len(clean))
```

## 3. Proportionate answers

- A clean, small question ("average DAU last week vs the week before") gets: the two numbers, the change in units and percent, the row count checked, one line on anything unusual. No model, no test, no forecast.
- Keep weekday structure in mind: compare whole weeks with whole weeks; a Monday-to-Sunday average is not comparable with a Wednesday-to-Tuesday one if weekends differ.

## 4. Common failure modes

- Summing a column before checking units or duplicates.
- Using local dates when the export is UTC (or the reverse) and shifting a month boundary.
- Averaging per-group averages instead of recomputing from rows (weights lost).
- Comparing a partial period (this month so far) with a full one.
- Reporting a pooled rate when the groups have very different mixes (Simpson; `causal-questions.md` §3).
- Calling a before/after change an effect without asking what else changed.

For retention, cohorts, funnels, LTV and game economies, also read `game-product-analytics.md`.
