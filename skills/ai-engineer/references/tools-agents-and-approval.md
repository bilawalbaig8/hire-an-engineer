# Tools, agents and approval

When to read this: the AI calls tools (search, database, email, payments), runs in a loop, or someone asks for an AI that acts "without a human".

## 1. Prefer a workflow to an agent
The application runs the tools; the model only asks for them [S-LLM-2]. Most agents follow the reason-then-act loop [S-AGT-2]; models can learn when a tool such as a calculator helps [S-AGT-3], which is also why exact maths belongs in a tool or code, not in the model. Use an agent only for the part whose path cannot be known in advance [S-LLM-5], [S-OWN-1]. Errors compound over steps, so a 95-percent-per-step agent is far less reliable over ten steps [S-AGT-4]; repeated trials of the same task show much lower consistency than a single run suggests [S-AGT-6].

## 2. Tools
- One job per tool, clear name, few validated inputs, the same result shape on success and failure, error messages that say what to do next [S-OWN-1], [S-LLM-10].
- Return only what is needed (top rows, not the whole table) [S-LLM-10].
- Read-only by default; a write tool takes the narrowest scope (this customer's record, not any file path).
- Tools that act are **idempotent** (an id per action so a retry does not pay twice).
- Evaluate tools on realistic tasks, not on one demo [S-LLM-10]. With MCP servers, apply the same trust rules: a tool description or result is untrusted text [S-LLM-11].

## 3. Authority: draft, don't do
| Action | Default |
|---|---|
| Read public or own data | automatic |
| Write internal draft, tag, note | automatic, logged |
| Send a message, publish, change someone else's data | AI drafts, human approves (or a code rule for a narrow, tested case) |
| Pay, refund, transfer, delete, decide about a person (hire, credit, ban) | AI drafts, human approves every time; hard limits in code |
| Change bank details, credentials, permissions | never automated; out-of-band check by a named human |

This is the owner's minimum-access and draft-don't-do rule [S-OWN-1], matching OWASP's "excessive agency" risk [S-SEC-1] and provider advice to keep a human in the loop for high-stakes actions [S-LLM-17]. Trust grows one action at a time, only after logs show it is reliably right; money limits and the kill switch stay.

## 4. Hard stops in code (not in the prompt)
Max steps, max time, max spend per task and per day, max retries with waits, a checkable done condition, a kill switch, and a clean stop that saves progress and tells a human what is left [S-OWN-1].

```python
class Limits:
    def __init__(self, max_steps=15, max_payout_rs=2000, max_day_rs=20000):
        self.steps = 0; self.max_steps = max_steps
        self.max_payout_rs = max_payout_rs; self.max_day_rs = max_day_rs; self.day_rs = 0
    def step(self):
        self.steps += 1
        if self.steps > self.max_steps: raise RuntimeError("step limit reached: stop and report")
    def check_payout(self, amount_rs: int):
        if amount_rs > self.max_payout_rs or self.day_rs + amount_rs > self.max_day_rs:
            raise PermissionError("needs owner approval")
KILL_SWITCH_FILE = "AI_DISABLED"   # if this file exists, no AI action runs
```

## 5. Approval gate design
- The approver sees exactly what will happen (recipient, amount, text), the source that triggered it, and the policy rule it was checked against.
- Policy rules from the project (limits, "never refund fraud-check", "bank changes confirmed by phone") are code checks before the approval screen, not prompt text.
- Approvals are logged with who, when, what.
- When asked to remove the human: decline that part, deliver the drafted, gated design, and return the autonomy level as `needs_approval` with `one_way_door: true` and the gated option recommended.

## 6. Failure modes
An agent with a generic `run_sql` or `read_file(any_path)` tool; recipients or amounts chosen by the model; retries that repeat a payment; no limit on loops; approval screens that hide the details; an agent that reads email (untrusted), holds customer data (private) and can send email (outbound) at once (`security-and-injection.md` §2).
