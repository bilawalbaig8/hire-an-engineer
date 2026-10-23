# Bug report and severity (every mode)

## 1. When to read this
Whenever a check fails, a player gets stuck, a file fails its check list, a number goes over budget or an accessibility rule is broken.

## 2. Before writing
1. Reproduce it from a clean start (fresh install, new save, cleared cache, a new test account).
2. Cut it down to the smallest steps that still show it.
3. Count how often it happens: "3 of 5 tries", never "sometimes".
4. Keep the evidence: log lines, screenshot, short video, save file, profiler capture, the exact command and its output.

## 3. The report
One file per bug in `docs/qa/` (or the mode's sub-folder), numbered, continuing any existing series:

| Field | What goes in |
|---|---|
| Title | What breaks, where, in one line ("Checkout charges twice after a double click on Pay") |
| Build / version | The exact build, commit or file version tested |
| Device and setup | Device, OS, browser or engine version, settings, test account |
| Steps | Numbered, from a clean start, each one an action |
| Expected | What should happen, and where that comes from (requirement, style guide, budget, rule) |
| Actual | What happened, with the measured value when there is one |
| How often | k of n tries |
| Evidence | Paths to logs, captures, crops, save files; the command and its output |
| Severity | 4, 3, 2 or 1 (below) |
| Proposed priority | P0 to P3 on the project's scale; the owner sets it |
| Not checked | Other devices, builds or paths not tried |

Made-up data only in the steps; never a real person's name, email or account. Never a key or secret value.

## 4. Severity (one scale for every mode)
The scale is the one in `hire-an-engineer/references/ui-ux.md` (section 8). The lines for 3, 2 and 1 below are this role's working wording, not a quoted rule.
- **4 blocks:** crash, data or progress loss, soft-lock, a journey cannot be finished, a person with a disability is locked out. These are always 4.
- **3 major:** the journey works only with a workaround, or a main feature is wrong.
- **2 minor:** wrong but easy to live with.
- **1 polish:** looks or feels off; nothing is wrong in use.

## 5. Bad and good
- Bad: "Checkout sometimes fails." No build, no steps, no count: builders close it as "cannot reproduce".
- Good: a title that names the place, steps from a clean start, expected and actual, "4 of 5 tries", a log line and a video path.

## 6. After the fix
Rerun the exact steps, then the regression set, and keep a regression test for the bug. Write "fixed" only after the rerun passes, with the command and its result.
