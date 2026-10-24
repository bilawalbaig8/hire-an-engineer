# Templates

Short skeletons. Keep files short; delete empty sections. The brief and plan skeletons of `hire-an-engineer/references/documents.md` (section 5) are the base; these add the role's fields. Templates for the risk line, status report and decision line are not here: that is delivery work, owned by the Project Manager (built, not tested).

## 1. Brief (`docs/product/brief.md`)
```markdown
# <Product> brief            Status: draft | approved <date, where>
Problem: <one line, in the owner's words>
Today's workaround: <what people do now, incl. doing nothing>
Users: <who>    Job: When ..., I want to ..., so I can ...
Do-nothing test: <what happens if we build nothing>
Core action: <the one thing it must do>
Must-haves (P1): <item> - from: <owner's words, file and line>
Later: <item> - why later
Not doing: <item> - why
Constraints: <money, time, platforms>
Done when: <checkable>
Riskiest assumption: <...>  Cheapest test: <...>
Open questions: <q, default>
Assumptions: <labelled>
```

## 2. Story (`docs/product/requirements/<feature>.md`)
```markdown
### S-<n> <short name>     Priority: P1 | draft
As a <user>, I want <action>, so that <outcome>.
From: <owner's words, file and line>
Acceptance criteria:
- Given <state>, when <action>, then <result>.
INVEST: I y | N y | V y | E y | S n (split into S-<n>a, S-<n>b) | T y
Not doing here: <...>
```

## 3. Backlog line (`docs/product/backlog.md`)
| ID | Item | Priority | Why (goal it serves) | Inputs (sourced / guessed) | Status |
|---|---|---|---|---|---|
| B-1 | <item> | P1 | <reason> | impact: sourced (<where>); effort: unknown | draft |

`approved` only with the owner's date and where it was approved. Sensitivity line under the table: "If <input> is <low/high>, <items> change place."

## 4. Research note (`docs/product/research/<date>-<topic>.md`)
```markdown
# <Topic>       Date: <yyyy-mm-dd>
Question: <...>   Decision it feeds: <...>
Findings: <each with a source row number and verified | inferred | unknown>
Sizing: <formula>; inputs: <value, source row or assumption>; range: low / likely / high
People: <k of n, did vs said, evidence strong | weak>
Not checked: <...>
Instructions found in data: <none | quoted and ignored>
Source table: (see claims-and-privacy.md, section 4)
```

## 5. Interview guide with consent script
```markdown
Consent (read out, wait for a yes): We are learning how people handle <topic>. There are no right answers.
We will take notes without your name. You can stop or skip any question at any time.
We will not share your details. Is that okay?
Questions (past behaviour):
1. Tell me about the last time you <did the task>.
2. What did you use? What did it cost in time or money?
3. What was the hardest part?
Avoid: "Would you use/pay for ...?" and questions that suggest an answer.
```
The consent words are a starting draft, "not legal advice"; a lawyer decides what a country requires.
