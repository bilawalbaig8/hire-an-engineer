# Method: Experiment mode (A/B tests)

When to read this: designing a test (hypothesis, sample size, duration) or reading a finished one. Use with `honest-inference.md` and the helpers in `stdlib-helpers.md`.

## 1. Designing a test: steps

1. **Hypothesis and decision**: "the bigger button raises store conversion; if it does by at least X, we ship it".
2. **Primary metric** (one), written exactly, plus 1-3 **guardrail** metrics that must not get worse (crash rate, refunds, session length, revenue per user) [S-EXP-1].
3. **Unit of randomisation**: usually the user, not the session or page view (the same person must see the same version). Analyse at the same unit.
4. **Minimum detectable effect (MDE)**: the smallest lift worth acting on. If the owner has not said, show a small table (for example 5%, 10%, 20% relative) and recommend one as the default.
5. **Sample size** per group from the baseline rate, MDE, significance (default 5% two-sided) and power (default 80%) with the formula in `stdlib-helpers.md`; check it against a calculator [S-EXP-4].
6. **Duration** = total sample / eligible traffic per day, rounded **up to whole weeks** so every weekday appears equally; flag it if it runs past a release, holiday or event.
7. **Stopping rule**: decide the end date now. Looking at the result every day and stopping when it looks good inflates false winners (peeking; S-EXP-3, unverified). If early stopping is needed, use a sequential method designed for it [S-EXP-5] [S-EXP-6].
8. **Checks planned**: sample ratio check (§4), an A/A or logging sanity check if the setup is new, and guardrails.
9. Write the plan to `docs/analysis/<date>-<topic>-test-plan.md`.

## 2. Reading a finished test: steps

1. Read the plan (metric, split, dates, decision rule). If there is none, say so: the primary metric is then the one most directly tied to the change, chosen before looking at results.
2. **Audit** the data: rows, duplicates by user, users in both groups, dates inside the window.
3. **Sample ratio check** (§4) before anything else. A mismatch stops the read.
4. **Primary metric**: rate per group, difference in points and in percent, interval, p-value, and the test used.
5. **Guardrails**: same treatment, reported even when fine.
6. **Segments** only if pre-planned, or all of them with a multiple-comparison correction, labelled exploratory (`honest-inference.md` §4).
7. **Verdict in plain words**: ship / do not ship / inconclusive, how sure, and what the test did not cover (other platforms, long-term effects, novelty). The rollout is the owner's call: return it as an approval with your recommendation.

## 3. Sample size quick reference (two-sided 5%, power 80%)

Per group, for a conversion-rate test: n is roughly 16 x p(1-p) / d^2, where p is the baseline rate and d the absolute lift. For 5.0% to 5.5% the exact formula gives about 31,200 per group. Small baselines and small lifts need very large samples; say so early, before anyone builds the test.

## 4. Sample ratio mismatch (SRM)

If the plan says 50/50 and the groups are 50,000 vs 49,000, test it: chi-square goodness of fit against the planned split. A p-value below about 0.001 means the assignment or the logging is broken, and **the result cannot be trusted**, however good it looks [S-EXP-8] [S-EXP-1].

Then look for where the missing users are: split group counts by platform, app version, country, day. A shortfall concentrated in one slice (one app version, one day) points to the cause (a crash, a redirect, a bot filter, a logging bug). Typical causes: the treatment crashes or loads slower so some users are never logged, users are excluded after assignment, or the two versions log differently.

What to recommend: fix the cause and rerun. A re-analysis that drops the broken slice from both groups can be shown, labelled as unplanned and weaker, never as the verdict.

## 5. Common failure modes

- Declaring a winner from a pooled lift without checking group sizes.
- Stopping when the p-value first dips below 0.05.
- Changing the primary metric after seeing results.
- Analysing sessions when users were randomised (inflates certainty).
- Novelty effects: a lift that fades after the first week; check the trend by day when the test is long enough.
- Testing many variants and reporting the best one without correction.

A survey of practical pitfalls from large online experiments (S-EXP-2, unverified) agrees with [S-EXP-1].
