# Causal questions: "did X cause Y?"

When to read this: whenever a request says or implies "because", "drives", "increases", "works", or compares people who chose something with people who did not. Owners make expensive decisions on correlations; this file is the brake.

## 1. The default answer

Without a randomised test, data shows what happened together, not what caused what. A randomised experiment is the clean way to learn a cause; everything else needs assumptions that must be written down and checked [S-CAU-1].

## 2. The five traps to check, in this order

| Trap | What it looks like | Quick check |
|---|---|---|
| Survivorship / immortal time | "Players who bought X stay longer" when buying requires staying long enough to buy | Compare only people who were still present when the choice could be made (landmark: everyone active on day N, bought by day N or not) [S-DQ-7, unverified] |
| Confounding | Engaged players both buy more and stay longer; the pack did not make them engaged | Name the common causes; compare within levels of them; ask what else differs between the groups [S-CAU-1] |
| Selection | Only some people are in the data (survey responders, users who updated the app) | Who could not appear? Compare the data's population with the whole |
| Reverse causation | Happy players rate the game highly, rating did not make them happy | Which came first in time? |
| Simpson's paradox | A trend in every subgroup reverses when the groups are pooled, because the mix differs | Split by the variable that drives both mix and outcome (platform, country, cohort) and compare within it [S-STA-10] |

Do not adjust for everything in sight: adjusting for a variable that is itself caused by the treatment (a mediator) or by both treatment and outcome (a collider) makes the estimate worse (good and bad controls, S-CAU-4, unverified).

## 3. Simpson's paradox: deciding which view is right

1. Show both views: the pooled rates and the rates within each subgroup.
2. Explain the mix: which group has more of the high-rate subgroup.
3. Decide by the causal story, not by the numbers: if the subgroup (platform) is not caused by the choice being evaluated (which network), compare within subgroups and combine with weights that match the population you care about [S-STA-10].
4. Check the uncertainty within each subgroup before declaring the reversed winner: subgroups are smaller, so the reversal may be noise too.

## 4. Observational methods, when no test is possible

| Method | Needs | Main risk |
|---|---|---|
| Before/after on the same users | A stable baseline, nothing else changed | Seasonality, other releases, regression to the mean |
| Difference-in-differences | A comparison group with the same trend before the change | Trends that were already diverging; staggered rollouts break the simple version [S-CAU-5] |
| Matching or adjustment | All important common causes measured | Unmeasured confounders |
| Regression discontinuity | A sharp cutoff (level, date, score) that decides treatment | Only valid near the cutoff |

Applied walk-throughs: [S-CAU-2]; a Python handbook (S-CAU-3, unverified); a four-step model, identify, estimate, refute workflow (S-CAU-6, unverified). Write the assumption each method needs in the report, and how it could fail.

## 5. What to write

- The naive comparison, reproduced, so the owner sees you took their number seriously.
- The trap, named in plain words ("buyers had to stay to buy").
- The fairer comparison you could run, with its interval, labelled as still observational.
- What would settle it: a randomised test, with a rough sample size.
- The owner's decision (price, push, budget) as an approval with your recommendation.

Statistical modelling for explanation and for prediction are different goals; a model that predicts well does not reveal causes (S-STA-9, unverified).
