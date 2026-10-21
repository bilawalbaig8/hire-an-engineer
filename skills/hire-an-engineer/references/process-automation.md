# Process Automation

The most common request from non-technical people: "Yeh kaam roz haath se karta hoon, khud ho jaye." They know the process deeply but can't describe it as steps, triggers and rules. You map it, decide what to automate, build it on the simplest reliable platform, keep a human in control where it matters, and make sure it never fails silently.

## Contents
1. Discover the process (as-is)
2. Map it
3. Decide what to automate
4. Design the automated process (to-be)
5. Choose the platform
6. Build safely
7. Test with real cases
8. Roll out
9. Run, monitor and measure
10. Documents for automation projects

---

## 1. Discover the process (as-is)

Ask them to **walk you through the last time they did it**, step by step, with real examples — not how it "should" work. Better: ask them to share or screen-record one real run, or show the files/emails/sheets involved.

Capture, in their words:
- **Trigger:** what starts it (an email arrives, a form is filled, every Monday 9am, a file lands in a folder)
- **Steps:** each action, where it happens (which app/website/file), who does it
- **Decisions:** every "agar… to…" (if the amount is over X, if the client is new, if the file is missing)
- **Inputs/outputs:** what data goes in and what comes out, with real samples
- **Exceptions:** what goes wrong and what they do then ("kabhi kabhi invoice PDF nahi hota, tab main call karta hoon")
- **Volume and time:** how often, how long each run takes, how many people do it
- **Pain:** where mistakes and delays happen
- **Access:** which accounts/apps are involved, and whether those apps can be connected (APIs, exports, connectors)

## 2. Map it

Draw the as-is process as a flowchart (swimlanes if several people are involved) and confirm it with them: "Kya aap ka kaam bilkul aise hota hai?" Fix it until they say yes. Then mark each step: manual / rule-based / needs judgement / waiting.

## 3. Decide what to automate

Score each step:

| Good to automate | Keep human (or human approves) |
|---|---|
| Repetitive, rule-based, high volume | Needs judgement, relationships, negotiation |
| Copying data between apps/files | Money movements, legal/irreversible actions |
| Formatting, renaming, sorting, reminders | Rare cases (cheaper to do by hand) |
| Reports and summaries from data | Steps where a mistake is costly and hard to undo |

- **Fix the process before automating it.** Automating a bad process just makes mistakes faster. Remove pointless steps first (thinking toolkit: remove-something option).
- **Start with the highest pain × frequency step**, not the whole process. Deliver a first automated slice within days.
- **ROI check:** time saved per month × value vs. build effort + running cost. Tell them plainly if it's not worth automating.
- AI can handle "semi-judgement" steps (classify emails, extract fields from PDFs, draft replies) — with a human reviewing until accuracy is proven.

## 4. Design the automated process (to-be)

Draw the to-be flowchart showing: trigger → steps → decisions → outputs, plus:
- **Human-in-the-loop points:** where a person approves, reviews or handles exceptions (e.g. "Draft ban jayega, aap 'Approve' dabayenge, phir email jayegi").
- **Exception path:** anything the automation can't handle goes to a clear place (a "needs attention" list, a message to the owner) — never dropped.
- **Notifications:** who is told what, when (success summaries optional; failures always).
- **Data flow** between apps, with what data each step reads and writes.
- **Rollback/undo** for steps that change data.

## 5. Choose the platform

Pick the simplest that handles the volume, logic and apps involved (check current capabilities and pricing):

| Option | Good for | Watch out |
|---|---|---|
| Built-in features of their apps (Gmail filters, Sheets formulas, calendar rules) | Very simple steps | Limited logic |
| **No-code automation** (Zapier, Make, n8n, Power Automate) | Connecting common apps, simple–medium logic, low–medium volume | Per-task pricing, complex logic gets messy, vendor limits |
| **Google Apps Script / Office Scripts** | Work inside Google Workspace / Microsoft 365 | Quotas, needs code maintenance |
| **Python script** (scheduled locally or in the cloud, e.g. GitHub Actions schedule) | Files, data processing, reports, complex logic, high volume | Needs hosting/scheduling, maintenance |
| **AI agent / AI steps** (LLM API in a flow, or an AI assistant with connectors and scheduled tasks) | Reading unstructured text/PDFs, classifying, drafting | Must be checked; cost per run; privacy |
| **Browser automation / RPA** | Only when an app has no API or export | Fragile — breaks when the website changes; check the site's terms |
| **Small custom app** | Process needs its own screens, approvals, records | Most effort — use the full workflow |

Prefer official APIs and connectors (`integrations.md`). Prefer tools the person already pays for.

## 6. Build safely

- **Work on copies first.** Never test on real customer data, live inboxes or real money.
- **Dry-run mode:** first version only logs/drafts what it *would* do; the person reviews; then turn on real actions.
- **Idempotent:** running twice must not send twice, pay twice or duplicate rows (check "already processed" markers).
- **Validate inputs:** missing or odd data goes to the exception path, not through.
- **Run log:** every run records time, items processed, results, errors (a sheet/table the person can open).
- **Failure alerts:** if a run fails or finds exceptions, the owner gets a plain message with what to do.
- **Secrets** in the platform's secure storage, never in the flow text or docs.
- **Limits:** respect app rate limits and platform quotas; batch where possible.
- Use the integration patterns in `integrations.md` (timeouts, retries, webhooks).

## 7. Test with real cases

- Collect 10–20 **real past examples**, including the awkward ones (missing attachment, duplicate, wrong format, very large).
- Run them through in dry-run; compare outputs to what the person actually did. Track accuracy, especially for AI steps.
- Test every exception path and the failure alert.
- Acceptance checks in their words: "Agar invoice email aaye to 5 minute mein sheet mein row aa jaye; agar PDF na ho to aap ko message aaye."

## 8. Roll out

- **Parallel run:** for a week (or N runs), automation runs alongside the manual process; compare results daily.
- Switch to automation for the easy cases first; humans keep handling exceptions.
- Turn on full automation only with the person's approval and acceptable accuracy.
- If others are affected (staff, customers), give them a short note on what changes for them.

## 9. Run, monitor and measure

- **Run log + weekly health glance** (silently, unless something's wrong): runs, items, failures, exceptions.
- **Alerts** for failures, repeated exceptions, or the automation not running when expected.
- **Measure value:** time saved per week, errors avoided — reported only if the person wants to see it (same record-only rule as costs).
- **Maintenance:** apps change (new form fields, API versions, website layouts); when the run log shows new errors, treat as an incident: root cause, fix, re-test with real cases.
- **Costs:** per-task/per-run platform and AI costs go in the cost register.

## 10. Documents for automation projects

Scaled to size; usually one combined document plus the run log:
- **Process map:** as-is and to-be flowcharts, with human-in-the-loop points.
- **Automation spec:** trigger, steps, rules, exceptions, data, platform, schedule.
- **Test results:** real-case comparison, accuracy.
- **Runbook / SOP** (in their words): what it does, where to see the run log, what each alert means and what to do, how to pause it, how to run the step manually if it's down, who owns the accounts.
