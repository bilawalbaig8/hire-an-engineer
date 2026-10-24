# Templates

When to read this: when you write a layout note, an algorithm note, a measurement record or a rename list. Keep each to one page, in simple English. Files go in `docs/software-engineering/structure/`, `algorithms/` and `performance/`. Continue the project's existing numbering or names; never overwrite an earlier file.

## 1. Layout note (`docs/software-engineering/structure/layout-<date>.md`)
```
# Layout note: <project or part>
Plan used: docs/architecture/structure.md, tree.txt, naming.md (date of each file)
What was created: <list of folders and files, from the dry run>
Not created, returned as questions: <items and why>
Checks: placeholder test <command and result>; naming check <command, counts, violations>
Conflicts between plan and code: <none | list with file evidence>
Not covered by the naming rules: <names for the Architect>
Review: Code Reviewer review pending
```

## 2. Algorithm note (`docs/software-engineering/algorithms/<topic>.md`)
```
# Algorithm note: <topic>
Data and operations: <shape, size now and at 10 times, how often>
Simple built-in choice: <structure and its cost in words and big-O>
Chosen: <what and why; "no change needed" is allowed>
Cost before and after: <plain words and big-O; extra memory>
Tests: <behaviour test, size test at 10 times, results>
Numbers: <median and spread before and after, machine block, "Measured on this machine only">
Source and licence: <ideas in own words with source IDs; code reused: none | source, licence, credit>
Revisit when: <size or time at which the answer changes>
For another role's code: <"note only, no code changed; <role> decides">
```

## 3. Measurement record (`docs/software-engineering/performance/<topic>-<date>.md`)
This is the only name for this file. It is never called a performance sheet (QA's file) or a budget sheet (Game & Technical's file).
```
# Measurement record: <topic>
Goal or budget: <one sentence and where it comes from>
Machine: <CPU>, <logical cores>, <RAM>, <OS>   Runtime: <version>   Other load / power plan: <value | unknown>
Method: <input, warm-up, runs, tool, script path>
Baseline: median <x> (min <a>, max <b>)
Profile: <biggest cost and its share; the other costs>
Change: <one change>
After: median <y> (min <c>, max <d>)   Result: <plain words, or "not shown to help" if ranges overlap>
Measured on this machine only. What only the target machine can show: <text>
Tests: <command and result>   Not run: <list>
Pending: Code Reviewer review<, QA re-measure>
```

## 4. Rename list for approval
```
Rename list: <project>   Baseline tests: <command and result>
| # | Old name | New name | Rule broken | References (how found) | Public path? | Reference owner |
Hidden references that search cannot find: <dynamic imports, names built from strings, files outside the repo>
Plan: branch <name>; one rename or rule per commit with git mv and no content change; references in the next commit; tests after each step
Way back: revert that commit
Options: approve all / approve some / none. Recommended: <option>. One-way door: <true if any public path>
```
