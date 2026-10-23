# Decide: AI or not, and which kind

When to read this: before designing any AI feature, and whenever someone wants "AI everywhere". The first answer you owe is whether AI belongs here at all.

## 1. The ladder (start low, climb only with evidence)

| Step | Use when | Typical examples | What it gives up |
|---|---|---|---|
| 0. Plain code, rules, lookups | The rule can be written down; the answer must be exact; cheap and instant matters | totals, tax, discounts, validation of emails and phones, uniqueness checks, date logic, templates and layouts | Cannot read messy free text |
| 1. Keyword rules or regex plus a human queue | A few words decide most cases | ticket routing that already works for most tickets | Brittle on new wording; needs upkeep |
| 2. Classic ML (logistic regression, gradient boosting) on your labels | Many labelled examples, a fixed set of labels, high volume | spam filter, category tags with thousands of labels | Needs labelled data and retraining |
| 3. One model call inside normal code | One judgement on messy text or images | summarise feedback, extract fields from a PDF | Per-call cost, latency, wrong-with-confidence answers |
| 4. Fixed workflow of model steps | Known steps in a known order | draft, check, send for approval | More calls, more places to fail |
| 5. Agent (the model chooses the steps) | The path cannot be known in advance | open-ended investigation with several tools | Hardest to test, errors compound across steps |

This is the owner's base rule (simplest shape first) [S-OWN-1], the same advice as Anthropic's agent guide [S-LLM-5] and Google's rules of ML (do not use ML when a rule will do; ship a simple baseline first) [S-TRN-1]. Using generative AI where it is not needed is a common, costly mistake [S-BOK-9].

## 2. Decision questions (answer each in one line in the design file)
1. **Is exactness required?** Money, accounting, legal numbers, IDs: code. A model may help read the input but code computes.
2. **Does a baseline exist?** If rules already handle 90 percent, the AI only needs to beat the human queue on the remaining 10 percent. Measure the baseline first.
3. **What does an error cost?** Low (a tag fixed later) allows automation; high (money sent, a person rejected) needs a human approval.
4. **Volume and latency:** calls per day times tokens per call is the bill; a call per page view for content that rarely changes is waste (`cost-latency-quota.md`).
5. **Data:** is it personal or confidential, and may it leave the company (`reliability-observability-privacy.md` §3)?
6. **Can we evaluate it?** If nobody can say what a good answer is, write that first (`evals-and-judges.md`).

## 3. Choosing a model size (once AI is justified)
- Start with the smallest or cheapest option that passes the eval set, then step up only when the eval says so [S-OWN-2]. A cascade (cheap model first, bigger model when unsure) is a known cost lever [S-AGT-5].
- Local or self-hosted models keep data in house but cost hardware and setup; hosted models are easier but need a data agreement. This is the owner's decision (one-way door when personal data is involved).
- Model names, prices, context sizes and limits change often: write them as `unknown` until read from the live provider page in this job.

## 4. Writing the verdict
For a list of wished-for AI features, produce a table: feature, verdict (`no AI`, `measure first`, `good fit`), why in one line, the cheaper alternative, what would change the verdict. Lead the summary with the count ("4 of 7 should be plain code"). Never write AI code for a feature you marked `no AI`.

## 5. Failure modes
- "AI-first" as a goal: AI is a tool, not a feature. Ask what outcome the owner wants.
- Replacing a working rule with a model and losing accuracy and money.
- Comparing the AI with nothing instead of with the current process.
- Choosing the biggest model "to be safe" before any eval exists.
