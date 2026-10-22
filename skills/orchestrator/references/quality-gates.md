# Quality gates

## When a review is required
- Any step that changes code, configuration or project files passes the Code Reviewer before you call it done.
- Documents and designs from the Architect need a review only when the owner asks or the design will drive costly work; say so in the plan.
- Who reviews what: code and diffs go to the Code Reviewer. A design or decision record goes to a fresh call of the Architect in review mode (a call that did not write it), because that lens fits; say in the plan which one you chose and why. The author never reviews its own work.
- When more checkers exist (QA, Security) they join the gate for what they own. Today the gate is the Code Reviewer alone; say that in the summary, do not imply tests or a security audit happened.

## What done means
A step is done when: the response is valid, `done_when` is met with evidence you can check (files exist, a command result, counts), open approvals are answered, and the gate has passed or the owner accepted the open findings.

## Fix rounds
1. The Reviewer returns findings. Pass the Critical and Important ones to the producing specialist as a new request (`goal`: fix these; `context_files`: the review file and the files).
2. Ask the Reviewer to check again, scoped to the findings.
3. At most 2 rounds per step. Then stop and give the owner the open findings in plain words with a recommendation: accept the risk, change the plan, or keep going with a higher cap.
4. Minor findings never block; list them.

## Disagreements
When specialists disagree (for example the Architect accepts a shortcut and the Reviewer rejects it): state both positions, who said it and why, the recommendation, and what each option gives up. Say whether it is a two-way door. Wait for the owner when it is hard to undo; do not pick silently.

## Do not
- Mark work done because the producing specialist says so.
- Ask the Reviewer to approve without reading, or to fix code.
- Count a skipped check as a pass.
