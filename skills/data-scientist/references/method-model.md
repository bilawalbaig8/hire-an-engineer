# Method: Model mode (predict, classify, segment)

When to read this: building a predictive model, scoring users, segmenting, or checking a model someone else made. Code for AUC, a stdlib logistic regression and splits is in `stdlib-helpers.md`.

## 1. Steps

1. **Frame the use**: who acts on the prediction, how (a discount, an offer, a warning), and at what moment. The prediction moment decides which data is allowed: only what is known at that moment.
2. **Audit and list every column with "known when?"** Write a small table: column, meaning, known before the prediction moment (yes / no / unsure). Read any data README. Columns that are only known after the outcome are **leakage** and are dropped, with the reason in the report [S-MOD-14] [S-MOD-1].
3. **Split before fitting anything**:
   - Rows of the same user (or player, store) stay together (grouped split).
   - Data with time order is split by time: train on earlier periods, test on later ones; ordinary shuffled cross-validation is only safe for time series under narrow conditions [S-MOD-13] [S-MOD-2].
   - Scaling, filling gaps, feature selection and target encoding are fitted on training data only [S-MOD-1].
   - Keep the test part untouched until the end; tune on a validation part or with cross-validation inside training.
4. **Baseline first**: the base rate ("nobody churns" is right 80% of the time when 20% churn), a one-rule baseline (fewest sessions), or last period's behaviour. A model is worth keeping only if it clearly beats the baseline on the test part [S-MOD-6].
5. **Simple model next**: a logistic regression or a small tree with few features. Use more complex models only if installed already and clearly better; an interpretable model is preferable when people act on individual scores [S-MOD-11].
6. **Pick the metric for the decision** [S-MOD-4]:
   - Rare outcomes: precision and recall at a stated threshold, and the precision-recall view; ROC AUC can look good when positives are rare [S-MOD-12].
   - Ranking ("who to contact first"): AUC, or how many real positives are in the top 10%.
   - Probabilities used as probabilities: check calibration [S-MOD-3].
   - Never report accuracy alone.
7. **Error analysis**: where is it wrong (which segments, which periods)? Permutation importance on the test part to see what drives it, with the caveat about correlated features [S-MOD-5] [S-MOD-10].
8. **Report** as a short model card: purpose, data and period, features used and dropped, split, baseline vs model, metric with uncertainty, where it fails, what it must not be used for [S-MOD-9].
9. **Action is the owner's**: sending discounts or offers based on scores costs money; recommend a small randomised test (score high-risk users, give the offer to half) to learn whether the action works, not only whether the score ranks well.

## 2. Leakage: the usual suspects

| Pattern | Example |
|---|---|
| Filled by the outcome | an exit-survey answer exists only for people who left |
| Measured after the outcome window | "days inactive" counted on the export day, after the window being predicted |
| Totals over the whole history | total orders or last order date copied from today's customer table |
| Target hidden in an ID or a status | order status "refunded" when predicting refunds |
| Duplicates across split | the same user in train and test |
| Preprocessing on all data | scaler or imputer fitted before the split |

Signs of leakage: a score that is near perfect, one feature that does almost all the work, or a big drop when the model meets truly new data. When a model looks too good, look for leakage before celebrating.

## 3. Checking someone else's model

1. Run it as is and reproduce its number (say if it cannot run).
2. Read how it splits and which columns it uses; fill in the "known when?" table.
3. Re-evaluate with an honest split and without leaky columns; compare with a baseline.
4. Report both numbers side by side with the reason for the difference.

## 4. Segmentation

Clusters are descriptions, not truths: report the features used, the number of groups and why, how stable the groups are with another seed or sample, and give each group a plain-language profile with its size. Small groups risk identifying people (`privacy-and-safety.md`).

## 5. Common failure modes

- Tuning on the test set, or picking the best of many models by test score.
- Shuffled split on time-ordered or repeated-user data.
- A model trained on one period used when behaviour changed (season events, price changes); check the base rate per period.
- Treating a predictive feature as a cause ("support tickets cause churn"); see `causal-questions.md`.
- Fairness: a model can treat groups unequally even when no protected column is used; check error rates by group when people are affected [S-PRI-6].
- Long-term upkeep: models quietly decay and entangle with the product [S-MOD-7].

Background: model assessment and validation [S-STA-13] [S-STA-14].
