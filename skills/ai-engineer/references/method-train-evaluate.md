# Mode Train/Evaluate: models that are trained, fine-tuned or judged

When to read this: someone wants to train or fine-tune a model, or asks whether a trained model is good enough ("is 97 percent fine?", "write the model card"). Builds on the owner's data rules: split before looking, leakage, baseline first, privacy, say what numbers do not prove [S-OWN-4].

## 1. Data readiness (always first)
Run a stdlib script over the data and report the counts in `evidence`:
- Size and class balance (counts per label). Rare classes decide what you can claim.
- Exact and near duplicates inside a set, and **overlap between train and test** (same text in both inflates the score).
- The same input with different labels (label conflicts); label errors are common even in well-known test sets [S-EVL-12], and there are methods to find them [S-TRN-18].
- Ordering: data sorted by label or time breaks a "first 80 percent / last 20 percent" split.
- Columns that give the answer away (a star rating next to a sentiment label, an ID that encodes the class): leakage if unavailable at prediction time, a free baseline if available. Leakage types and a checklist idea: [S-TRN-10], [S-TRN-5].
- Personal data: keep it out of training sets; models can reveal memorised text [S-SEC-7].

```python
import csv, collections, sys
def profile(train_path, test_path=None, text="text", label="label"):
    tr = list(csv.DictReader(open(train_path, encoding="utf-8")))
    print("rows", len(tr), collections.Counter(r[label] for r in tr))
    seen = collections.defaultdict(set)
    for r in tr: seen[r[text].strip().lower()].add(r[label])
    print("duplicate texts", sum(1 for r in tr) - len(seen))
    print("label conflicts", [t for t, ls in seen.items() if len(ls) > 1][:10])
    if test_path:
        te = list(csv.DictReader(open(test_path, encoding="utf-8")))
        print("test rows also in train", sum(r[text].strip().lower() in seen for r in te))
```

## 2. Baseline first
Every result is compared with the simplest predictor: the majority class, a keyword or rule baseline, or the current process [S-TRN-7], [S-TRN-1]. "97 percent accuracy" against a 95 percent always-majority baseline is a weak model, not a strong one.

## 3. Metric chosen for the decision
- Imbalanced classes: per-class precision and recall and the confusion matrix, not accuracy alone [S-TRN-6].
- Name the costly error (a missed spam versus a lost real email) and report the metric for it.
- When a score gates an action, check calibration (do 0.8 scores come true about 80 percent of the time) [S-TRN-8].

## 4. Validation that fits the data
- Split before looking at results; keep a test set untouched for the final number.
- Stratify by label; group by customer, user or document when rows share a source; split by time when the model will predict the future [S-TRN-4].
- Do not tune on the set you report on; nested validation when tuning [S-TRN-11].
- Small data: repeated stratified cross-validation and an interval. With tens of samples the error bars are wide [S-TRN-9]; say so in words the owner understands ("between about 60 and 95 percent").
- Equal test scores can hide different behaviour in use; test the cases that matter, not only the held-out score [S-TRN-12], [S-TRN-13].

## 5. Training or fine-tuning (only if it can and should be run)
- Before fine-tuning a language model, try a prompt with a few examples measured on the eval set; fine-tuning is for when that fails and enough clean labels exist.
- Parameter-efficient methods (LoRA, adapters) reduce compute, not the duty to evaluate [S-TRN-17], [S-TRN-15]; the standard workflow is data, tokenisation, training, an evaluation metric [S-TRN-14].
- If training cannot run here (no library, no GPU, no internet, no model file), say so, give the plan and the acceptance bar, and report no number. Never write a result you did not run.

## 6. Error analysis
Read the wrong predictions, group them by cause (label noise, missing context, language, length), and fix the biggest group first [S-EVL-3].

## 7. Model card and data sheet
Write `docs/ai/<model>-model-card.md` (template in `governance-and-documentation.md` §2): intended use and out-of-scope use, data and its known problems, metrics per class with sample sizes and intervals, baseline, limits, what was not run, and the go/no-go recommendation as a decision for the owner [S-GOV-3], [S-GOV-10]. For a new dataset add data-sheet notes [S-GOV-4].

## 8. Small-sample helpers (stdlib)
```python
from math import sqrt
def wilson(k, n, z=1.96):
    """95 percent interval for k successes out of n."""
    if n == 0: return (0.0, 1.0)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d; h = z*sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (max(0.0, c-h), min(1.0, c+h))
# wilson(17, 20) -> about (0.64, 0.95); wilson(4, 10) -> about (0.17, 0.69)
```

Standard metric implementations exist when a library is allowed [S-TRN-16]. Data, deployment and distribution shift across the lifecycle: [S-BOK-2].

## 9. Respond
`done` with the profile counts, the metrics you computed and the model card path in `evidence`; claims labelled `verified` (computed here) or `inferred`. A request for a guaranteed number is answered with what can be shown and what it would take; the go/no-go for shipping is the owner's decision.
