# Thinking Toolkit

Thinking tools a sharp product lead and architect use *in their head* before deciding. Drawn and simplified from product-brainstorming, creative-thinking, research-brainstorming and the cc-thinking-skills mental models for this use case.

The person never sees framework names. They see the result: a clearer problem, two or three real options, and your recommendation with a reason. Use a tool when it moves the project forward; never run every tool on every project.

---

## 1. When to reach for which tool

| Moment | Tools |
|---|---|
| Phase 1 — the idea is vague or sounds like a solution, not a problem | Five whys, Job to be done, Do-nothing test, Problem reframing |
| Phase 2 — deciding what goes in v1 | Riskiest assumption, Remove-something, Impact vs effort |
| Phase 3 — choosing the approach | Option spread, Analogy, Constraint removal, Second-order effects |
| Phase 4 — design feels complicated | Problem reframing, Abstraction ladder, Inversion |
| Before build — big investment ahead | Pre-mortem, Cheapest test first |
| Any decision — how long to spend on it | One-way or two-way door |
| "Too expensive" / "impossible" / "always done this way" | Physics or convention? |
| A bug with more than one possible cause | Competing hypotheses, Simplest first, Check the real thing |
| Before launch of anything with logins, data or money | Attacker's view |
| Need a number: users, storage, cost, time | Look it up first, then rough estimate, Buffer sized to the cost of being wrong |
| Something is slow or work piles up | Find the bottleneck |
| Debugging fails 3 times / project stuck | Reframing, Tension hunting, Step back a level |
| Person adds lots of new ideas | Opportunity tree, Impact vs effort |

## 2. Understanding the problem

**Symptom vs root cause (five whys).** People describe symptoms ("orders get lost"). Keep asking why, gently and in their words, until you hit something structural ("orders come through 3 channels and nobody combines them"). Build for the root cause.

**Job to be done.** Internally frame the need as: *When [situation], they want to [motivation], so they can [outcome].* Include the emotional side ("feel in control of the day's baking"). The job stays stable even if the solution changes — design for the job, not the feature list they asked for.

**Do-nothing test.** "Agar yeh na banayein to kya hoga? Kis ko kitna nuqsan?" If the answer is "not much", the project is smaller than it sounds — or not worth building.

**Awareness, ability or motivation?** Is the problem that people don't know, can't do it, or don't want to? Software mostly fixes *ability*. If it's awareness or motivation, a reminder, a process change or a simpler tool may solve it.

**Who else is involved?** Map everyone the problem touches: the person, their customers, staff, a boss who wants reports. Each may need something different.

## 3. Generating options

**Option spread.** Before settling, think of at least 4–5 genuinely different ways to solve it, varying along:
- size: tiny tweak ↔ full system
- kind: software ↔ process change ↔ existing product
- time: quick win now ↔ bigger build later
Always include one option that **removes** something instead of adding, and one that does **the opposite** of the obvious.

**Problem reframing.** Question the problem as stated:
- Change the goal: "make the report faster" → "make the report unnecessary".
- Change who does the work: staff types orders → customers fill a form.
- Change the timing: real-time → once a day is enough.
- Change the form: an app → a shared sheet + WhatsApp message.

**Analogy.** "Kis aur business ne yeh masla hal kiya hai?" How do restaurants, clinics, delivery apps, schools handle the same pattern? Borrow the structure, not the surface.

**Constraint removal.** Imagine no budget, no technical limits, no time limit — what would the ideal be? Then work back to the version that fits reality. Reveals what really matters.

**Physics or convention?** When something is called "too expensive", "impossible" or "the way it's always done", ask whether that is a real limit (law, cost, a service's hard limit — verify it) or just habit. Accept real limits; rebuild around habits. Skip this for settled, working patterns — don't reinvent a login system or a payment flow.

**Abstraction ladder.** Move up (what general pattern is this? — "booking", "tracking", "approval", "catalogue") to find proven designs; move down (what's the most concrete version for this one person?) to keep v1 small.

## 4. Stress-testing an idea

**List the assumptions.** Every plan rests on things assumed true: users will use it, the data exists, the person will maintain it, the outside service is reliable, the cost stays low. For each: how sure are we, and what would prove it wrong?

**Riskiest assumption + cheapest test.** Find the one assumption that, if wrong, kills the project. Test it before building — a mockup shown to 2 customers, a one-week spreadsheet trial, checking a service's limits.

**Pre-mortem (inversion).** "Imagine it's 3 months later and this failed. Why?" — nobody used it, data got messy, it broke and no one could fix it, costs grew. Turn each answer into a safeguard in the design or plan.

**Devil's advocate.** Argue the strongest case against your own recommendation. If it survives, recommend it with more confidence; if not, change it.

**Second-order effects.** "If we do X, what does it make easier or harder later?" (e.g. using their personal Gmail for the app makes handing it to staff harder).

**Tension hunting.** Look for goals that pull against each other — simple vs flexible, private vs shared, cheap vs reliable. Name the trade-off and pick deliberately; good designs often find a way to get most of both.

**Attacker's view (security).** Before launching anything with logins, personal data, payments or an admin area: who would attack it (an outsider, a logged-in user, a staff member) and what would each try — reach another user's data, skip payment, become admin, read secrets? Report only a weakness you can show step by step against *this* project (entry point → steps → damage). "Best practice says…" without a real path is not a finding. Fix each real one, add a test for it, and run any scanner you can (`engineering-principles.md` §6).

## 5. Deciding

**One-way or two-way door.** Ask first: how costly is this to undo? Two-way doors (a library, a screen layout, a tool you can swap) — decide fast; delay costs more than a wrong choice. One-way doors (data format and where data lives, deleting data, a paid contract, publishing, a public URL people depend on) — slow down, and first look for a way to make it undoable: a backup, a small trial, a switch to turn it off, keeping the old version. Unsure? Treat it as one-way.

**Numbers: look up, estimate, then add a buffer.** If the real number can be found (a pricing page, counting rows, timing a run), get it — never estimate what you can measure. If not, break it into pieces you can guess (users × actions per day × cost per action) and give a range ("~Rs 3,000–10,000 a month"), never false precision. Then size the buffer to the cost of being wrong: a budget, a deadline or a storage limit that would break something gets real slack; a setting you can change in a minute needs none. If the decision is the same across the whole range, skip the estimate and act.

**Impact vs effort.** For features and options, place each roughly: high impact + low effort first; low impact + high effort to "later" or never.

**Take a position.** After weighing options, recommend one clearly with the reason in their terms. Neutral menus push decisions onto someone who can't judge them.

**Opportunity tree (for growing idea lists).** Goal → needs/opportunities → possible solutions → cheapest test for each. Keeps a flood of ideas organised and makes "later" feel concrete, not dismissed.

## 6. Debugging and performance

These sharpen root-cause debugging (`engineering-discipline.md` §4); they don't replace it.

**Check the real thing, not the description.** When behaviour doesn't match the docs, a comment, a test name, a function's name or your memory of the code, stop reasoning from the description. Read the code that actually runs, add a log, look at the real data, reproduce it, check what changed recently. Theorise only after looking.

**Simplest first.** If the simplest explanation (typo, wrong file, missing setting, stale cache, wrong version) can be checked in one step, check it before anything else. Don't simplify where the problem is truly complex (two things happening at once, security).

**Competing hypotheses.** If a symptom could come from several places, write down 3–5 specific causes (name the file, setting or input), then make the cheapest check that rules the most out — read the named function, compare a working and a broken log line, look at the last change. If you can think of only one cause, you are guessing. Then go back to one hypothesis, one small change, one test.

**Find the bottleneck.** When something is slow or work piles up, measure where the time goes first. Only the slowest step matters; speeding up anything else changes nothing. Fix that step, measure again — the bottleneck may move. If no single step dominates, the problem is how the parts interact; look at that instead.

## 7. When stuck

- Stuck or three failed fixes → `getting-unstuck.md`; then reframe (§3) before continuing.
- Two good options and no clear winner → pick the one easier to undo, and log it as a ruling.
- Person keeps changing their mind → go back to the job to be done and success criteria; decide against those.

## 8. How to show the result to the person

Never show the framework. Show:
1. The problem in one line, in their words, sharpened ("Asal masla yeh hai ke orders teen jagah se aate hain aur ek jagah jama nahi hote").
2. Two or three options in real-life terms (what they get, cost, time, effort to maintain).
3. Your recommendation and why.
4. The one risk worth knowing, and how you'll handle or test it.

Where the options differ in how things flow or connect, show each as a small diagram side by side ("aaj aise hota hai" vs "is tareeqe se aise hoga") — `plain-language.md` §0, Show it as a picture.
