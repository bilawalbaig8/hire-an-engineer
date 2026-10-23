# Framing the question

When to read this: at the start of every job, before opening the data. Five minutes of framing prevents the most expensive mistake in analysis: a correct answer to the wrong question.

## 1. The five things to pin down

| Item | Ask yourself | Example |
|---|---|---|
| Decision | What will someone do differently depending on the answer? | Roll out the new button, or not |
| Question | The one question whose answer drives that decision | Does the new button raise purchase conversion? |
| Metric | Exactly how it is computed: numerator, denominator, unit, window | Users who bought anything / users who saw the store page, within the 14 test days |
| Population | Who is in, who is out (test accounts, bots, staff, refunds) | All users assigned to the test, both platforms |
| Time window | Which dates, in which time zone | 2026-09-01 to 2026-09-14, UTC |

Write these five lines at the top of the report. If the request does not say, choose a sensible default, write it in `assumptions`, and state it in the summary so the boss can correct it.

## 2. When to ask and when to assume

- **Ask** (`needs_answers`) only when the answer would change the conclusion and there is no defensible default. Each question carries a `why` and a suggested default. At most three questions.
- **Assume** when a default is standard (5% significance, 80% power, UTC when the export says UTC, net revenue excluding refunds when "revenue" is unqualified) and show how the answer moves under the alternative. Often the best answer is a small table: "with a 5% lift you need X, with 10% Y, with 20% Z".
- **Never ask** what the request already says (dates, file, metric), and never ask about things you can check in the data yourself.
- A metric definition that matters for money or a public claim (what counts as "revenue", "active", "churned") is the owner's decision. Use a default, label it, and list it as an owner decision in the report.

## 3. Match the mode to the decision

| Decision type | Mode | What a useful answer looks like |
|---|---|---|
| "What happened / how much" | Analyst | A number with its definition, row counts and caveats |
| "Should we ship B instead of A?" | Experiment | An effect with an interval, a check that the test was valid, a recommendation |
| "Who will do X?" | Model | A ranked list or score, compared with a simple baseline, with honest error rates |
| "How many next month?" | Forecast | A central value with an interval and what would change it |
| "Does X cause Y?" (no test was run) | Analyst plus `causal-questions.md` | What the data can and cannot show, and the test that would settle it |

## 4. Red flags in the request itself

- **The answer is named in advance** ("prove that...", "find where it is significant"): the job becomes measuring honestly, not confirming. See `honest-inference.md` §4.
- **"Just one number"** for something uncertain: give the number and its range in one sentence; a range is what keeps the owner from planning on luck.
- **A causal verb** ("increases", "drives", "because of") applied to observational data: check `causal-questions.md` before agreeing.
- **A business action bundled with the question** ("...and roll it out", "...and send it to the agency"): answer the question; return the action as an approval.
- **Work outside the role** (pipelines, dashboards, cloud setup): see `privacy-and-safety.md` §4.

## 5. Proportionate effort

A question that a three-line script answers gets a three-line script and a short answer. Do not add models, forecasts or significance tests the decision does not need. Complexity is a cost the owner pays in time and in trust; the simplest method that answers the decision wins [S-MOD-6].

Sources: the five framing items follow common experimentation practice [S-EXP-1]; documenting where data came from and what it is for follows [S-MOD-8].
