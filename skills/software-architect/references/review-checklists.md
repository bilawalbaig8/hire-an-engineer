# Review checklists

When to read this: to check a design before you hand it back, to review someone else's design, to ask "what breaks when this grows", to prepare a launch, or to check an existing project for drift.

For every item answer `yes`, `no` or `unknown`, and give the evidence (file, number, command). An item with no evidence is `unknown`. Every `no` and `unknown` that matters goes into `risks`. These lists are prompts for conversation, not an audit. [S-FND-19]

## 1. Design review

- [ ] The top 4 to 8 quality scenarios are written with a measure each.
- [ ] Every top scenario is met by the chosen shape, or the gap is named as a risk.
- [ ] Two or three genuinely different options were compared, and each says what it gives up.
- [ ] The chosen shape is the simplest that meets the scenarios, and the trigger to step up is written.
- [ ] Every one-way-door decision has a decision record with status `proposed` and was returned as an approval.
- [ ] Ownership is clear: each building block has one owner and one sentence of responsibility.
- [ ] Who owns the truth for each important piece of data is stated (one source of truth).
- [ ] Failure is designed for: every call to something outside the program has a timeout and a retry limit; what happens when each external part is down is written. [S-WEB-5]
- [ ] Security was considered at design time: assets, trust boundaries, who can do what, secrets, and the top threats with mitigations. [S-WEB-19] [S-WEB-18]
- [ ] Reliability targets exist (an availability or response target and an error budget, or a reason none is needed). [S-WEB-2]
- [ ] Data protection and privacy: what personal data is stored, why, for how long, who sees it.
- [ ] Cost: a rough monthly running cost and what drives it.
- [ ] Assumptions are written down.
- [ ] A new engineer could build from the files without asking you anything important.

## 2. What breaks at 10 times

For each row, find the first thing that breaks, the number at which it breaks (or `unknown`), and how you would notice early.

- [ ] **Data size:** biggest table or file now and at 10 times; queries that scan everything; list screens without paging; backups and restore time; storage cost.
- [ ] **Users and traffic:** requests per second now and at 10 times; the slowest shared resource (one database, one queue, one third-party API with a limit); sessions or connections held in memory; peak versus average.
- [ ] **Team size:** how long a new person needs to make a safe change; modules that two teams must edit together; test and build time; release process.
- [ ] **Cost:** which line grows fastest (compute, storage, third-party calls, AI tokens, bandwidth); is there a cap or an alert.
- [ ] **Failure:** what a single failure of the most central part does to everything else.
- [ ] **Operations:** who gets alerted, with what, and what they do first.

## 3. Pre-launch

- [ ] The main scenarios have been tested with realistic data and realistic volume, not only a small sample.
- [ ] Security: no secrets in the code or the repository; least access for every account; dependencies checked; user input validated; login and permissions tested; the top threats from the design have a mitigation. [S-WEB-18]
- [ ] AI features (if any): instructions from outside content are treated as data, not commands; the AI cannot take irreversible actions without a human step; outputs are checked before use; spending and step limits exist in code. [S-AI-9] [S-AI-1]
- [ ] Reliability: targets and alerts exist; health checks; what users see when something fails. [S-WEB-2] [S-WEB-3]
- [ ] Backups run and a restore has been tried once.
- [ ] Rollback: how to go back to the last good version, and what happens to data that was already changed.
- [ ] Observability: logs, a few key numbers, and a way to find a failing request.
- [ ] Cost cap or alert is set.
- [ ] Privacy and rules: data handling matches what users were told; store or platform rules checked (apps and games).
- [ ] A named person owns the system after launch.
- [ ] Anything hard to undo in the launch itself (data migration, DNS, payment go-live) has an explicit approval.

## 4. Drift check for an existing project

- [ ] Recent decision records exist and still match the code (list those that no longer do).
- [ ] The dependency graph still has no cycles and no lower layer importing a higher one (run the import script in `method-recover`).
- [ ] The files that change most often are known, and the biggest ones have an owner and a plan.
- [ ] Files that change together across module boundaries are known (change coupling).
- [ ] Rules that matter are automated checks, not only text. [S-FND-4]
- [ ] New external dependencies since the last review were looked at (licence, maintenance, security).
- [ ] The documented architecture overview matches the entry points you can find in the code today.
- [ ] Open risks from the last review: which are retired, which are still open, which are new.

## Writing the findings

Order findings by what would hurt most. For each: what you saw (with evidence and label), why it matters in one sentence, the smallest change that would fix or reduce it, and what the fix gives up. Be plain: a non-engineer should understand the first three findings.

## Sources
[S-FND-4] [S-FND-19] [S-WEB-2] [S-WEB-3] [S-WEB-5] [S-WEB-18] [S-WEB-19] [S-AI-1] [S-AI-9]
