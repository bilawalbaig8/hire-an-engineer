# Market and users mode

## 1. When to read this
The request asks who has the problem, what they use today, who else sells a fix, how big it could be, or what people said in interviews: competitors, market size, an interview guide, a summary of interview notes.

## 2. Before searching
1. Write the research question and the decision it feeds ("should the first version target shops or customers?"). No decision, no research: ask one question with a suggested default.
2. Read `claims-and-privacy.md` first. Every number, competitor fact and user claim follows its rules.

## 3. Competitors and alternatives
- Alternatives include what people do today without a product: a spreadsheet, WhatsApp, paper, a person they pay, doing nothing (S-PBA-28, S-PBA-27).
- For each product or alternative: what it does well, what it does badly, price if the public page shows it, the URL and the date read. A fact you could not open in this job is `unknown`.
- Do not sign up for, log in to, or buy a competitor's product. Read-only live access follows the live-access rule in `SKILL.md`.
- Write what you could not check (a page behind a login, a paid report, an app store page that did not load).

## 4. Market sizing
- A formula, never one bare number: for example `people with the problem x share who pay x price per year`. Each input has a source (URL, publisher, year, place, definition) or is labelled `assumption`.
- Give a range (low, likely, high), not one number. Top-down (from a published total) and bottom-up (from counts of buyers and prices) when both are possible; show both and why they differ.
- Two sources that disagree are both shown with their definitions and years, and why they differ (S-PBA-25 and S-PBA-26 show how different assumptions give very different sizes).
- Arithmetic: a small standard-library Python script in `docs/product/research/`, its command and output in the evidence. No sizing script ships with this skill (not built).
- Web blocked or no source found: write the formula with every input `unknown` and say what you could not reach. Never fill an input from memory.

## 5. Interview guides (the owner runs the interviews)
- Problem and market interviews only; usability tests with real people belong to the Designer.
- Ask about past behaviour, not opinions about the future: "When did this last happen? What did you do? What did it cost?" not "Would you pay for ...?" (S-PBA-18, S-PBA-19). No leading questions.
- Every guide starts with a consent script (template in `templates.md`; S-PBA-23).
- The owner or their team run the interviews. This role never contacts people, sends surveys or books calls.

## 6. Synthesis of notes the owner gives
1. Anonymise first: people become P1, P2, ...; drop names, emails, phone numbers, employers, places that identify someone (S-PBA-24). Never look anyone up.
2. Group notes into themes (affinity grouping, S-PBA-21; thematic analysis, S-PBA-22).
3. Count: "4 of 6 people". Never write "users want X" from fewer people than the count shows.
4. Keep what people **did** (past behaviour, money or time spent) apart from what they **said they would do**. Rate the evidence: strong (several people, past behaviour), weak (one voice, or future talk only).
5. A small sample finds problems; it does not size a market (S-PBA-20).
6. No personas invented from nothing. A persona comes only from real research; otherwise it is labelled an assumption.

## 7. Done when
The research file `docs/product/research/<date>-<topic>.md` exists with the question, the decision it feeds, a source table, every number as a formula and a range, every claim `verified`, `inferred` or `unknown`, counts for user claims, what was not checked, and no personal details.
