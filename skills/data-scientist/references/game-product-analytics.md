# Game and product analytics

When to read this: retention, cohorts, funnels, DAU and engagement, monetisation (ARPDAU, payer rate, LTV), game economies, user acquisition by channel. Method steps are in `method-analyst.md`; this file gives definitions and traps.

## 1. Definitions to write down (the owner decides the official one)

| Metric | Common definition | Choices that change the number |
|---|---|---|
| DAU / MAU | distinct users with at least one session that day / 30 days | Time zone of "day"; bots, test accounts; reinstalls counted as new users |
| Dn retention | share of an install cohort active on day n after install (classic) | "On day n" versus "on day n or later" (rolling); day 0 = install day; calendar day versus 24-hour windows |
| Churn | no activity for X days, or a cancelled subscription | X; whether returning players "un-churn" |
| Payer rate / conversion | payers / active users in a period | Who counts as active; refunds |
| ARPDAU | revenue / DAU for a day | Gross or net of store fees and refunds; ads revenue in or out |
| LTV | expected revenue per user over a horizon | Horizon (D90, D365); discounting; how it is projected beyond observed data |

Analytics vendors define these slightly differently; when comparing with a dashboard, read its definition first [S-GAM-3] [S-GAM-4]. A broader reference on game telemetry and player metrics is S-GAM-1 (unverified).

## 2. Cohorts and retention

- Always group players by install date (cohort) and compare like with like: D7 of the June cohort with D7 of the July cohort.
- Recent cohorts are not finished: a cohort installed 10 days ago has no D30 yet. Exclude or mark it (right-censoring), never count it as churned.
- Retention curves flatten; small differences early can matter more than a late tail.
- **Survivorship**: comparing players who did something (bought, joined a clan, reached level 20) with those who did not is biased whenever doing it requires staying. Use a landmark comparison: among players still active on day N, compare those who did it by day N with those who did not, then follow both from day N (`causal-questions.md` §2).

## 3. Funnels

- Define each step as an event and the window (same session, same day, within 7 days).
- Count users, not events, at each step; each step is a subset of the previous one.
- Report step-to-step conversion and the biggest absolute drop; check by platform and app version, because a broken step on one version looks like a funnel problem.

## 4. LTV and monetisation

- Revenue per user is very skewed (a few big spenders): report the median and the share of revenue from the top 1% and 10%, and use bootstrap intervals for means (`honest-inference.md` §2).
- Projected LTV beyond the observed window rests on a model of how players drop out and spend; state the model and its assumptions, and show what the observed window alone gives. Probability models for repeat buying exist (S-GAM-2, unverified) but are assumptions, not data.
- LTV versus acquisition cost compares a projection with a fact; give the projection a range.

## 5. User acquisition and channels

- Compare channels within platform and country (mix differs: Simpson's paradox, `causal-questions.md` §3).
- A channel decision needs cost (per install, per payer) as well as quality; without cost, say the decision cannot be made from quality alone.
- Early cohort data from a channel is small; give intervals.

## 6. Game economy

- Track sources (where currency comes from) and sinks (where it goes) per day and per player segment; a growing balance per active player signals inflation.
- Price changes and offers change who buys and when; a before/after comparison mixes this with seasonality. Prefer a randomised price or offer test.

## 7. Churn prediction in games

How churn is labelled (days of inactivity, horizon) drives everything downstream; free-to-play churn work defines the label carefully before modelling (S-GAM-5, unverified). Use `method-model.md` for splits and leakage.
