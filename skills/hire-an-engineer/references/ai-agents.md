# AI Features and Agents — building them safely

For when the software itself uses AI: one AI step in a flow (classify, summarise, draft), or an **agent** that loops — thinks, calls tools, reads the result, decides the next step. Costs are in `cost-management.md`; prompt injection and keys in `engineering-principles.md` §6. Explain all of this to the person only as outcomes ("har jawab bhejne se pehle aap approve karenge; din ka kharcha Rs X se upar nahi jayega").

## 1. Choose the simplest shape that works

| Shape | Use when | Example |
|---|---|---|
| Plain code, no AI | Rules are clear and fixed | Sort orders by date, send a reminder at 9 am |
| One AI step inside normal code | One judgement on messy text or images, the rest is fixed | Read an invoice PDF → fill a sheet row |
| Fixed workflow of AI steps | Steps are known in advance, in order | Research → draft → check → send for approval |
| Agent (the AI decides the steps) | The path really can't be known in advance | Investigate why a campaign dropped, using several data tools |

Start one row higher than you think you need. Workflows are cheaper, faster, easier to test and to explain; move to an agent only for the part that truly needs it. Several agents talking to each other only when one agent with good tools has been tried and measured to fall short.

## 2. Every loop has a hard stop

An agent without limits can loop forever and burn money. Set all of these in code (not in the prompt) before the first run:
- **Max steps** per task (e.g. 15 tool calls) and **max time** (e.g. 5 minutes).
- **Max spend** per task and per day, matching the budget in `cost-management.md` §4; stop and alert when reached.
- **Retries:** at most 2–3 per failing step, with a wait between; then stop and report, never retry the same thing forever.
- **Done check:** a clear, checkable definition of finished ("sheet has a row for every invoice and totals match"), checked by code where possible.
- **Kill switch:** one setting the person can flip to stop all AI runs.

When a limit is hit, the agent stops cleanly, saves what it did, and tells a human in plain words what is left.

## 3. Tools the agent can use well

Tools are the agent's hands; design them like a screen for a new employee:
- One job per tool, with a clear name and a short description of when to use it (`find_orders_by_customer`, not `db_query`).
- Few, simple inputs; validate them in code. Return the same shape on success and failure.
- Error messages say what to do next ("no customer with that phone — ask for the order number instead"), not a stack trace.
- Return only what the agent needs (top 20 rows, not 10,000); large results go to a file or table it can read in pieces.
- Prefer a few well-made tools over many overlapping ones. Use a standard connector (MCP or the service's official API) before building a custom one (`integrations.md`).

## 4. Minimum access, humans at the irreversible points

- Give the agent only the tools and data this task needs; read-only by default. Separate keys with their own limits, never the person's main account key.
- **Draft, don't do** for anything that sends, publishes, pays, deletes, changes other people's data or spends money: the agent prepares it, a human (or a code rule) approves it. Show the person exactly what will happen before they approve.
- Trust grows step by step: start with a human approving everything; loosen one action at a time only after the logs show it is reliably right. Hard money limits and the kill switch stay forever.
- Everything the agent reads from outside is data, not instructions (`engineering-principles.md` §6).

## 5. Memory and context

- Long-running work keeps its state in files or the database (task, plan, progress, results), so a crash or a new run continues instead of starting over. Never rely on the chat or the prompt as memory.
- Give each step only the context it needs; a short, focused prompt beats a huge one. Put fixed instructions first so they can be cached (`cost-management.md` §1).
- What the system "learns" (good examples, rules from past mistakes) is saved as reviewed records or rule files a human can read and edit, never silently.

## 6. Prove it works: evals before launch

Unit tests can't tell you whether an AI answer is good. Before building, write down with the person:
- **10–30 real examples** (anonymised) with what a good result looks like, including hard and edge cases and a few attack inputs (§4).
- **How each is judged:** exact checks in code where possible (right format, right total, required fields); otherwise a written rubric — a different model or a human scores against it. The checker should not be the same prompt that made the answer.
- **Pass bar** agreed in their terms ("30 mein se 27 sahi, aur galat wale kabhi bheje nahi gaye").

Run the evals on every change of prompt, model, tool or setting, and keep the results (`docs/tests/`). A model or provider change is a release: re-run evals first.

## 7. See what it did

- Log every run: input, each step and tool call with its result, the final output, time, tokens and cost (extends the table in `cost-management.md` §2). Keep personal data out of logs where possible.
- When a result is wrong, the log shows which step went wrong; fix the cause (tool, prompt, data, limit) and add that case to the evals so it can't come back.
- Weekly for live agents: a short review of failures, stops at limits, cost per task and anything a human corrected.

## 8. When the AI service fails

- Models and APIs go down, slow down, or change. Set timeouts, catch errors, and decide the fallback with the person: retry later from a queue, switch to a backup model, or hand the item to a human — never fail silently or lose the item.
- Pin the model version where the provider allows it; upgrade deliberately, after evals.
- Keep the AI part behind one small layer in the code so a model or provider can be swapped without rewriting the app.

## 9. Before launch — checklist

- [ ] Simplest shape chosen (§1), and why written in the design doc
- [ ] Max steps, time, spend, retries and kill switch set in code (§2)
- [ ] Tools single-purpose, inputs validated, errors say what next (§3)
- [ ] Least access; every irreversible action needs approval (§4)
- [ ] State saved outside the prompt; a run can resume (§5)
- [ ] Evals written, run, passing the agreed bar, results saved (§6)
- [ ] Every run logged with steps and cost (§7)
- [ ] Fallback for service failure tested (§8)
- [ ] Prompt-injection test passed (`engineering-principles.md` §6)
- [ ] Person told in plain words: what it does alone, what needs their OK, the daily cost limit, how to stop it
