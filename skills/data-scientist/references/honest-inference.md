# Honest inference: how sure are we?

When to read this: whenever a number will be compared, generalised or used for a decision. Code for every method here is in `stdlib-helpers.md`.

## 1. Report effects, not verdicts

- Lead with the **size** of the difference in the unit the owner cares about (percentage points, users, dollars) and an **interval** around it. "Conversion rose 0.4 points (95% interval -0.1 to +1.0)" says more than "not significant" [S-STA-7] [S-STA-2].
- A p-value is the chance of data at least this extreme if there were no real difference. It is not the chance the result is true, it does not measure the size of the effect, and a threshold like 0.05 is not a law of nature [S-STA-1].
- "No significant difference" is not "no difference". Say what the interval rules out: "any effect larger than +2 points is unlikely".
- Relative and absolute lifts both get stated: "+10% relative (4.0% to 4.4%)".

## 2. Choosing a method (small menu, stdlib-friendly)

| Data | Question | Method |
|---|---|---|
| Two proportions, large groups (at least ~10 successes and failures per group) | Is B's rate different from A's? | Two-proportion z-test; Wald or Newcombe interval for the difference |
| Two proportions, small groups | Same | Fisher's exact test; Wilson interval per group |
| One proportion | Rate with uncertainty | Wilson interval (better than the textbook one near 0% or 100%) |
| Means, roughly symmetric | Difference of averages | Welch t-interval (normal approximation for large n) |
| Skewed money (revenue per user, LTV) | Difference of averages | Bootstrap interval (resample users, fixed seed); report the median too |
| Counts in categories vs a plan | Do group sizes match the planned split? | Chi-square goodness of fit (sample ratio check) |
| Many comparisons | Which of these are real? | Benjamini-Hochberg false discovery rate [S-STA-6] |

When in doubt, simulate: a permutation test (shuffle the labels many times with a fixed seed) needs no formula and explains itself [S-STA-16]. The NIST handbook is the reference for assumptions of each test [S-STA-18].

## 3. Small samples

- Compute the interval first. If it runs from "clearly worse" to "much better", the honest answer is "too little data to tell", followed by how much data would be needed (sample size formula in `stdlib-helpers.md`).
- Small studies that do find a "significant" effect tend to overstate it; a striking result from a few dozen users needs replication before it drives a decision [S-STA-3].
- A decision can still be made without proof when it is cheap to undo; say so explicitly ("the data cannot tell; switching is cheap to reverse, so it is a judgement call for the owner").

## 4. Multiple comparisons and result-hunting

- Every extra metric, segment, date range, outlier rule or stopping point is another chance to find a fluke. With 20 independent looks at pure noise, about one will cross p < 0.05 [S-STA-4].
- Hidden choices count too: deciding the analysis after seeing the data is the same problem even without deliberate fishing (the "garden of forking paths", S-STA-5, unverified).
- Rules: fix the primary metric and analysis before looking (or use what the test plan says). Report the primary result first, whatever it is. If you explore segments, report all of them, adjust with Benjamini-Hochberg, and label them exploratory: they generate the next hypothesis, they do not prove this one.
- A request to "find a segment where it is significant and show only that" is refused in those words, politely, with the honest alternative (`privacy-and-safety.md` §3). A common catalogue of these mistakes is [S-STA-17].

## 5. Effect sizes, power and practical value

- Power is the chance a test detects an effect of a given size if it is real. Underpowered tests mostly produce noise and inflated winners. Conventions for small, medium and large effects exist [S-EXP-7], but the effect that matters is the smallest one worth acting on for this business.
- Practical value beats statistical significance: a real +0.1 point lift may not pay for the engineering; a non-significant +2 points may still deserve a bigger test.

## 6. Saying how sure you are

Use plain confidence words tied to evidence, the same way each time [S-COM-5]:

| Say | When |
|---|---|
| "Clear" | Large effect, tight interval, valid design, checks passed |
| "Likely" | Interval mostly on one side, or design caveats remain |
| "Can't tell" | Interval spans meaningful effects in both directions |
| "Can't be answered with this data" | Wrong design (no comparison group, survivorship, leakage) |

Further reading: plain-language inference [S-STA-15]; regression done honestly [S-STA-12]; resampling and model assessment [S-STA-13].
