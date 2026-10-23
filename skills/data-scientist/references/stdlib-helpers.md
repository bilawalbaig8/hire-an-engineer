# Standard-library helpers (copy, save, run)

When to read this: you need an interval, a test, a sample size, an AUC, a small model or a forecast backtest, and pandas, scipy or scikit-learn are not installed (check with `python -c "import scipy"`). Everything below uses only the Python standard library [S-TOOL-5] [S-TOOL-6]. If scipy or statsmodels are installed you may use them instead [S-TOOL-3] [S-TOOL-4]; never install them.

Save the block as `docs/analysis/scripts/ds_helpers.py` (or the folder the request names), import it from your analysis script, and run `python docs/analysis/scripts/ds_helpers.py` once: the self-test prints `self-test ok`. The methods and their assumptions are explained in `honest-inference.md`, `method-experiment.md`, `method-model.md` and `method-forecast.md`.

```python
"""Small statistics helpers, standard library only. Run this file to self-test."""
import csv
import math
import random
import statistics

NORM = statistics.NormalDist()


def read_csv(path):
    """Rows as dicts (strings). Read-only."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def wilson(x, n, conf=0.95):
    """Wilson interval for one proportion x/n."""
    if n == 0:
        return (float("nan"), float("nan"))
    z = NORM.inv_cdf(0.5 + conf / 2)
    p = x / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (mid - half, mid + half)


def two_prop(x1, n1, x2, n2, conf=0.95):
    """Difference p2 - p1, two-sided p-value (pooled z test), Wald interval for the difference."""
    p1, p2 = x1 / n1, x2 / n2
    pool = (x1 + x2) / (n1 + n2)
    se0 = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
    pval = 2 * (1 - NORM.cdf(abs(p2 - p1) / se0)) if se0 > 0 else 1.0
    z = NORM.inv_cdf(0.5 + conf / 2)
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return p2 - p1, pval, (p2 - p1 - z * se, p2 - p1 + z * se)


def fisher_exact(a, b, c, d):
    """Two-sided Fisher exact p for [[a, b], [c, d]] (rows = groups, columns = success, failure)."""
    n1, n2, k = a + b, c + d, a + c
    total = math.comb(n1 + n2, k)

    def prob(x):
        return math.comb(n1, x) * math.comb(n2, k - x) / total

    p0 = prob(a)
    return min(1.0, sum(prob(x) for x in range(max(0, k - n2), min(k, n1) + 1) if prob(x) <= p0 * (1 + 1e-9)))


def _gammainc_upper_reg(s, x):
    """Regularised upper incomplete gamma Q(s, x), for the chi-square tail."""
    if x <= 0:
        return 1.0
    if x < s + 1:  # series for P, then Q = 1 - P
        term = total = 1.0 / s
        k = s
        for _ in range(10000):
            k += 1
            term *= x / k
            total += term
            if term < total * 1e-15:
                break
        return 1.0 - total * math.exp(-x + s * math.log(x) - math.lgamma(s))
    b, c, d = x + 1 - s, 1e300, 1 / (x + 1 - s)  # continued fraction (Lentz)
    h = d
    for i in range(1, 10000):
        an = -i * (i - s)
        b += 2
        d = an * d + b
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = b + an / c
        c = c if abs(c) > 1e-300 else 1e-300
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return math.exp(-x + s * math.log(x) - math.lgamma(s)) * h


def chi2_sf(x, df):
    """P(chi-square with df degrees of freedom >= x)."""
    return _gammainc_upper_reg(df / 2, x / 2)


def srm_check(counts, planned_shares):
    """Sample ratio check: chi-square goodness of fit of group counts against the planned split."""
    total = sum(counts)
    stat = sum((o - total * s) ** 2 / (total * s) for o, s in zip(counts, planned_shares))
    return stat, chi2_sf(stat, len(counts) - 1)


def sample_size_two_prop(p1, p2, alpha=0.05, power=0.8):
    """Users per group to detect p1 -> p2 with a two-sided test."""
    za, zb = NORM.inv_cdf(1 - alpha / 2), NORM.inv_cdf(power)
    pb = (p1 + p2) / 2
    n = (za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2
    return math.ceil(n)


def bootstrap_diff(a, b, stat=statistics.fmean, reps=2000, seed=42, conf=0.95):
    """Percentile bootstrap interval for stat(b) - stat(a). Resample units (users), not events."""
    rng = random.Random(seed)
    diffs = sorted(stat(rng.choices(b, k=len(b))) - stat(rng.choices(a, k=len(a))) for _ in range(reps))
    lo = diffs[int((1 - conf) / 2 * reps)]
    hi = diffs[int((1 + conf) / 2 * reps) - 1]
    return stat(b) - stat(a), (lo, hi)


def permutation_p(a, b, stat=statistics.fmean, reps=5000, seed=42):
    """Two-sided permutation test p-value for a difference in stat."""
    rng = random.Random(seed)
    obs = abs(stat(b) - stat(a))
    pooled = list(a) + list(b)
    hits = 0
    for _ in range(reps):
        rng.shuffle(pooled)
        if abs(stat(pooled[len(a):]) - stat(pooled[:len(a)])) >= obs - 1e-12:
            hits += 1
    return (hits + 1) / (reps + 1)


def bh_adjust(pvals):
    """Benjamini-Hochberg adjusted p-values, same order as the input."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj, prev = [0.0] * m, 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        prev = min(prev, pvals[i] * m / rank)
        adj[i] = prev
    return adj


def auc(scores, labels):
    """ROC AUC by ranks (ties get average rank). labels are 0/1."""
    pairs = sorted(zip(scores, labels))
    ranks, i = [0.0] * len(pairs), 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            j += 1
        for k in range(i, j):
            ranks[k] = (i + j + 1) / 2
        i = j
    pos = sum(lab for _, lab in pairs)
    neg = len(pairs) - pos
    rsum = sum(r for r, (_, lab) in zip(ranks, pairs) if lab == 1)
    return (rsum - pos * (pos + 1) / 2) / (pos * neg)


def precision_recall_at(scores, labels, threshold):
    tp = sum(1 for s, y in zip(scores, labels) if s >= threshold and y == 1)
    fp = sum(1 for s, y in zip(scores, labels) if s >= threshold and y == 0)
    fn = sum(1 for s, y in zip(scores, labels) if s < threshold and y == 1)
    return (tp / (tp + fp) if tp + fp else float("nan")), (tp / (tp + fn) if tp + fn else float("nan"))


def fit_scaler(X):
    """Means and SDs from TRAINING rows only; apply the same to test rows."""
    cols = list(zip(*X))
    return [statistics.fmean(c) for c in cols], [statistics.pstdev(c) or 1.0 for c in cols]


def scale(X, scaler):
    mu, sd = scaler
    return [[(v - m) / s for v, m, s in zip(row, mu, sd)] for row in X]


def logistic_fit(X, y, l2=0.01, lr=0.1, epochs=300):
    """Plain gradient-descent logistic regression on scaled features. Returns weights (bias first)."""
    w = [0.0] * (len(X[0]) + 1)
    n = len(X)
    for _ in range(epochs):
        grad = [0.0] * len(w)
        for row, t in zip(X, y):
            z = w[0] + sum(wi * xi for wi, xi in zip(w[1:], row))
            p = 1 / (1 + math.exp(-max(-30.0, min(30.0, z))))
            err = p - t
            grad[0] += err
            for j, xi in enumerate(row, start=1):
                grad[j] += err * xi
        w = [w[0] - lr * grad[0] / n] + [wj - lr * (g / n + l2 * wj) for wj, g in zip(w[1:], grad[1:])]
    return w


def logistic_predict(w, X):
    return [1 / (1 + math.exp(-max(-30.0, min(30.0, w[0] + sum(a * b for a, b in zip(w[1:], row)))))) for row in X]


def backtest(series, horizon, method):
    """Hold out the last `horizon` points; method(history, h) -> list of h forecasts. Returns MAE and errors."""
    hist, actual = series[:-horizon], series[-horizon:]
    fc = method(hist, horizon)
    errors = [a - f for a, f in zip(actual, fc)]
    return statistics.fmean(abs(e) for e in errors), errors


def naive(hist, h):
    return [hist[-1]] * h


def mean_last(k):
    return lambda hist, h: [statistics.fmean(hist[-k:])] * h


def drift(hist, h):
    slope = (hist[-1] - hist[0]) / (len(hist) - 1)
    return [hist[-1] + slope * (i + 1) for i in range(h)]


def random_walk_interval(point, step_sd, steps_ahead, conf=0.80):
    """Interval that widens with sqrt(steps); step_sd = SD of period-to-period changes."""
    z = NORM.inv_cdf(0.5 + conf / 2)
    half = z * step_sd * math.sqrt(steps_ahead)
    return point - half, point + half


if __name__ == "__main__":
    assert abs(fisher_exact(3, 1, 1, 3) - 0.4857) < 1e-3
    assert sample_size_two_prop(0.05, 0.055) == 31234
    stat, p = srm_check([50000, 49000], [0.5, 0.5])
    assert abs(stat - 10.10) < 0.01 and 0.001 < p < 0.002
    assert abs(chi2_sf(3.841, 1) - 0.05) < 1e-3 and abs(chi2_sf(11.07, 5) - 0.05) < 1e-3
    lo, hi = wilson(5, 10)
    assert abs(lo - 0.2366) < 1e-3 and abs(hi - 0.7634) < 1e-3
    assert auc([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1]) == 0.75
    assert [round(x, 3) for x in bh_adjust([0.01, 0.04, 0.03, 0.2])] == [0.04, 0.053, 0.053, 0.2]
    rng = random.Random(0)
    X = [[rng.gauss(0, 1)] for _ in range(400)]
    y = [int(rng.random() < 1 / (1 + math.exp(-2 * x[0]))) for x in X]
    w = logistic_fit(X, y)
    assert w[1] > 1.0 and auc(logistic_predict(w, X), y) > 0.8
    print("self-test ok")
```

Notes
- `two_prop` uses the pooled z test for the p-value and an unpooled interval; with fewer than about 10 successes or failures in a group, use `fisher_exact` and `wilson` instead.
- `bootstrap_diff` and `permutation_p` take per-user values (revenue per user, sessions per user), never per-event rows.
- Fit `fit_scaler` on training rows only, then `scale` both parts with it; that is the leakage rule from `method-model.md`.
- Seeds are fixed so every run prints the same numbers; state them in the write-up.
