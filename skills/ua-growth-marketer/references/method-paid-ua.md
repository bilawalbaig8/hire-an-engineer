# Method: Paid UA (ad tests, campaign reads, budget and bid recommendations)

## 1. When to read this
Ad test plans, briefs for ad variants, reading campaign exports, budgets and bids, "why are the iOS numbers odd". Channels: the ones in the owner's campaign exports; others only on request (owner decision Q29).

## 2. Test plan (written before the test starts)
1. One question per test. A few concepts that really differ (the concepts come from the Creative & Art Director).
2. The measure, using the metric definitions the Data Scientist & Analyst approved. If there is no definition (for example of LTV), return `needs_answers`.
3. The sample needed: from the Data Scientist & Analyst, or from a platform's own calculator labelled as such. If the test will drive a scale-up or a bigger budget, the sample size and the verdict come from the Data Scientist & Analyst through the boss.
4. A stop rule and "what we do if it wins, loses or is unclear".
5. The variant table for the Writer: which variant changes which one thing, placements and limits read from the live page. The Writer writes the words (owner decision Q2).

Template: `Question | Concepts | Measure (definition source) | Sample needed (source) | Stop rule | Decision if win / lose / unclear | Variant table | Flags`

## 3. Results read
1. Check the export: source, date range, row count, which platform, which definitions. Give the command for each count.
2. Follow the chain: installs, cost per install, day-1 and day-7 retention, purchases and ad revenue, payback. Say where it breaks and what is unknown.
3. Label every number `measured`, `modelled` or `unknown`; mark early numbers. An empty value is "not reported", not zero.
4. Never call a winner from a small, short or peeked-at test. Say "too early" and what would settle it; send the verdict question to the Data Scientist & Analyst.

Template: `Data read (file, dates, rows) | Chain table with labels | What it says | How sure | What is unknown | Next step and who`

## 4. Budget and bid recommendation
Always a recommendation and always `needs_approval`, with the named person who sets it (the owner until the owner names someone).
Template: `Recommended range | Why | Risk | What would change the advice | Options with what each gives up | Who sets it`
Use only numbers from the brief's data or limits; never a remembered market benchmark. With no data, the range is `unknown` and the answer says what data is needed.

## 5. Attribution limits (iOS and Android)
Explain in plain words what can be measured, how late and how coarse (ATT opt-in, SKAdNetwork and AdAttributionKit, Google Play and Android rules). Read the live documentation pages in `policy-flags.md` before quoting any delay, threshold or window; never quote them from memory. Never suggest a way around these limits.

## 6. Where files go
`docs/marketing/ua/` (test plans, results reads, budget and bid recommendations, attribution notes); flags in `docs/marketing/flags.md`.

## 7. Traps
- "Scale creative B to a big daily budget" after a few days and few installs: too early; plan, sample need, budget as `needs_approval`, never "set".
- "Why is iOS ROAS zero?" with empty values: "not reported", explain privacy thresholds and delays from the live page, label it `unknown`.
- "Write headlines that show a level not in the game" or "win real cash": brief honest variants for the Writer, flag misrepresentation, send the idea question to the Creative & Art Director.

## 8. Done when
The plan or read is in `docs/marketing/ua/`, every number labelled, the sample source and the doubt stated, the recommendation names its risk and the person who acts, flags written, and the answer says what was not checked.
