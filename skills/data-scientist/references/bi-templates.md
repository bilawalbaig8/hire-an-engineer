# BI / Analytics templates and helpers

When to read this: in BI / Analytics mode only (`method-bi-analytics.md`), when writing a dictionary line, KPI tree, tracking plan, report spec or growth read, or when the table script needs a reconcile bridge, cohort table, ROAS or a projection. Standard library only; save helpers inside the table script and run it.

## 1. Metric dictionary (`docs/analytics/metrics.md`)

```markdown
| Metric | Meaning | Formula | Grain | Time zone | Filters | Source | Owner | Status | Approved by / date | Review date |
|---|---|---|---|---|---|---|---|---|---|---|
| dau | Players who played that day | distinct user_id with >= 1 session in the day | day | UTC | test accounts and bots out | sessions table | <role or name> | draft | - | <date + 3 months> |
```
Status is `draft` or `approved`. Only an owner approval relayed by the boss changes `draft` to `approved`; add the name and date. Under the table, list known differences with vendor dashboards ("SDK dashboard counts devices in local time").

## 2. KPI tree (`docs/analytics/kpi-tree.md`)

```markdown
North Star: <metric> = <formula>        (why it reflects value for players)
- Input: <metric> = <formula>           team that can move it: <team>
  - Input: <metric> = <formula>
- Input: <metric> = <formula>
Guardrails: crash-free users, refund rate, uninstalls (must not get worse)
Note: the tree is arithmetic; a causal link between an input and the top needs a test.
```

## 3. Tracking plan (`docs/analytics/tracking-plan.md`)

```markdown
| Event | Fires when | Property | Type | Allowed values | Feeds metric | Owner | Personal data? |
|---|---|---|---|---|---|---|---|
| level_complete | the level-end screen opens | level_id | integer | 1-200 | level funnel | game engineer | no |
| level_complete | | player_id | string | internal pseudonymous id | all | game engineer | pseudonymous |
```
Names only, no values from real players. Flagged fields (name, e-mail, phone, advertising or device id, IP, precise location, free text) are left out unless the owner approved them; record the approval date in the row.

## 4. Report or dashboard spec (`docs/analytics/reports/<name>.md`)

```markdown
# <Report name>
Decision it serves: <the decision>          Audience: <who, how often>
Primary number: <metric>                   Date range rule: <e.g. last 8 full weeks, UTC>
Owner: <name or role>   Refresh: <schedule, data delay>   Review: <date>   Retire if unused by: <date>
Built by: <owner or engineer role> in <tool>, from this spec and the table script (this role does not build it)

| # | Tile | Question it answers | Metric (dictionary, status) | Chart | Comparison | Filters | Data-quality note |
|---|---|---|---|---|---|---|---|
| 1 | ... | ... | dau (draft) | line, weekly | previous 8 weeks | platform | last partial day excluded |

Left out on purpose: <columns and why>.  Exploratory page (labelled): <optional>.
Data-quality checks (from the script): freshness, partial days, unfinished cohorts, duplicates, test accounts.
Reproduce: python docs/analytics/scripts/<file>.py -> prints the tile tables and row counts.
```

## 5. Growth read (`docs/analytics/growth/<yyyy-mm-dd>-<topic>.md`)

Use the write-up in `writing-results.md`, plus a table where each number has a label:

```markdown
| Network | Platform | Installs | CPI | D1 ret | D7 ret | D7 ROAS | D30 ROAS | Payback |
|---|---|---|---|---|---|---|---|---|
| A | android | 16,755 | 0.45 measured | 21% measured | 7% measured | 6.1% measured | 9.9% predicted (9.4-10.3) | not reached by day 21 (measured) |
```

## 6. Helpers (standard library)

```python
import math, random, statistics
from collections import defaultdict
from datetime import date

# 1. Distinct count per day under one definition (for reconcile and for DAU-style metrics).
def distinct_per_day(rows, day_of, key_of, keep=lambda r: True):
    out = defaultdict(set)
    for r in rows:
        if keep(r):
            out[day_of(r)].add(key_of(r))
    return {d: len(s) for d, s in out.items()}

# 2. Bridge from report A to report B: steps = [(label, {day: value}), ...], one difference per step.
def bridge(steps, days):
    prev = None
    for label, per_day in steps:
        avg = statistics.mean(per_day.get(d, 0) for d in days)
        print(f"{label:<40} avg {avg:10.1f}" + ("" if prev is None else f"   change {avg - prev:+.1f}"))
        prev = avg

# 3. Cohort curves with unfinished days left out; revenue None = unknown (for example iOS after the SKAN window).
def cohort_curves(rows, last_full_day, n_max):
    out = defaultdict(dict)
    for r in rows:
        c, d = r["install_date"], int(r["days_since_install"])
        if d <= min((last_full_day - date.fromisoformat(c)).days, n_max):
            rev = None if r["revenue_usd"] == "" else float(r["revenue_usd"])
            out[c][d] = (int(r["active_users"]), rev)
    return out

def roas_at(curves, spend, n):
    """MEASURED cumulative ROAS at day n over cohorts at least n days old; None if any revenue is unknown."""
    cs = [c for c, days in curves.items() if n in days]
    rev = [v[1] for c in cs for d, v in curves[c].items() if d <= n]
    if not cs or any(x is None for x in rev):
        return None, len(cs)
    return sum(rev) / sum(spend[c] for c in cs), len(cs)

# 4. PREDICTED ROAS at a later day: fit retention r(d) = a * d**-b on days 1..k, keep revenue per active day
#    at its day 0..k level, bootstrap over cohorts. The range covers cohort noise only, not the curve assumption.
def project_roas(curves, spend, installs, k, horizon, n_boot=500, seed=7):
    cs = sorted(c for c, days in curves.items() if k in days)
    rng = random.Random(seed)

    def one(sample):
        inst = sum(installs[c] for c in sample)
        pts = [(math.log(d), math.log(sum(curves[c][d][0] for c in sample) / inst))
               for d in range(1, k + 1) if sum(curves[c][d][0] for c in sample) > 0]
        mx, my = statistics.mean(x for x, _ in pts), statistics.mean(y for _, y in pts)
        b = -sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
        a = math.exp(my + b * mx)
        active_days = lambda n: 1 + sum(a * d ** -b for d in range(1, n + 1))
        rev_k = sum(v[1] for c in sample for d, v in curves[c].items() if d <= k)
        return rev_k * active_days(horizon) / active_days(k) / sum(spend[c] for c in sample)

    boots = sorted(one([rng.choice(cs) for _ in cs]) for _ in range(n_boot))
    return one(cs), boots[int(0.025 * n_boot)], boots[int(0.975 * n_boot) - 1]
```

Checks for helper 4: needs at least about 10 cohorts with k observed days; compare the fitted curve with the observed days and say if it bends away; never project further than a few times the observed window without saying the range is weak.
