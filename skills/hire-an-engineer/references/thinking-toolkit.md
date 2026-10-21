# Thinking Toolkit

Thinking tools a sharp product lead and architect use *in their head* before deciding. Drawn and simplified from product-brainstorming, creative-thinking and research-brainstorming skills for this use case.

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

**Abstraction ladder.** Move up (what general pattern is this? — "booking", "tracking", "approval", "catalogue") to find proven designs; move down (what's the most concrete version for this one person?) to keep v1 small.

## 4. Stress-testing an idea

**List the assumptions.** Every plan rests on things assumed true: users will use it, the data exists, the person will maintain it, the outside service is reliable, the cost stays low. For each: how sure are we, and what would prove it wrong?

**Riskiest assumption + cheapest test.** Find the one assumption that, if wrong, kills the project. Test it before building — a mockup shown to 2 customers, a one-week spreadsheet trial, checking a service's limits.

**Pre-mortem (inversion).** "Imagine it's 3 months later and this failed. Why?" — nobody used it, data got messy, it broke and no one could fix it, costs grew. Turn each answer into a safeguard in the design or plan.

**Devil's advocate.** Argue the strongest case against your own recommendation. If it survives, recommend it with more confidence; if not, change it.

**Second-order effects.** "If we do X, what does it make easier or harder later?" (e.g. using their personal Gmail for the app makes handing it to staff harder).

**Tension hunting.** Look for goals that pull against each other — simple vs flexible, private vs shared, cheap vs reliable. Name the trade-off and pick deliberately; good designs often find a way to get most of both.

## 5. Deciding

**Impact vs effort.** For features and options, place each roughly: high impact + low effort first; low impact + high effort to "later" or never.

**Take a position.** After weighing options, recommend one clearly with the reason in their terms. Neutral menus push decisions onto someone who can't judge them.

**Opportunity tree (for growing idea lists).** Goal → needs/opportunities → possible solutions → cheapest test for each. Keeps a flood of ideas organised and makes "later" feel concrete, not dismissed.

## 6. When stuck

- Stuck or three failed fixes → `getting-unstuck.md`; then reframe (§3) before continuing.
- Two good options and no clear winner → pick the one easier to undo, and log it as a ruling.
- Person keeps changing their mind → go back to the job to be done and success criteria; decide against those.

## 7. How to show the result to the person

Never show the framework. Show:
1. The problem in one line, in their words, sharpened ("Asal masla yeh hai ke orders teen jagah se aate hain aur ek jagah jama nahi hote").
2. Two or three options in real-life terms (what they get, cost, time, effort to maintain).
3. Your recommendation and why.
4. The one risk worth knowing, and how you'll handle or test it.
