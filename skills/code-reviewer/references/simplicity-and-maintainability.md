# Simplicity and maintainability

When to read this: for every review, after correctness and security. This lens keeps the code something the next person can understand and change. It produces the most Minor findings, so keep it short and kind to the author's time.

## The standard

A change should leave the code at least as healthy as it found it. It need not be perfect and it need not match your taste. If the code is clear, correct and consistent with the project, approve it even if you would have written it differently. [S-REV-1]

## What to look for

| Smell | Question | Typical move |
|---|---|---|
| **Too complex to read** | Can someone follow this function in one pass? Deep nesting, long conditions, many branches. A reading-effort measure like cognitive complexity gives a reason beyond "feels complex". [S-MNT-7] | Split it, return early, name the pieces. |
| **Over-engineering** | Is there an abstraction, option, layer or config that nothing uses yet? Generic frameworks for one case? | Remove what is not needed now ("you will not need it"); add it when a second case arrives. |
| **Duplication** | Is the same logic copied in several places, so a fix must be made many times? (Two similar lines are fine; the same rule in three files is not.) | Extract once, but only when the copies really mean the same thing. |
| **Wrong place** | Does the code live where its responsibility belongs (a pricing rule inside a request handler; SQL inside a screen)? | Move it; keep layers honest. |
| **Coupling** | Does it reach into the internals of another module, use globals, or need many unrelated things? | Narrow the interface. |
| **Names and comments** | Do the names say what things are and do? Does a comment explain why (not repeat what)? Are there comments that lie? | Rename; delete stale comments. |
| **Dead code** | Unused functions, imports, parameters, branches, commented-out code, leftover debug prints. | Delete. |
| **Magic values** | Unexplained numbers and strings (a limit, a rate, a status text). | Name them, put them in one place. |
| **Consistency** | Different style, patterns or libraries from the rest of the project for no reason. | Follow the project's existing pattern. |
| **Change size and focus** | Does the change mix unrelated things (a fix, a refactor and a new feature)? Is it too large to review well? | Ask to split. [S-REV-2] |
| **Missing explanation** | A tricky algorithm, a workaround or an unusual choice with no word of why. | Ask for a short comment or a link to the reason. |

A "smell" is a hint to look closer, not proof of a problem. Confirm that the structure really hurts before you report it. [S-MNT-4] When you suggest a change, name the standard refactoring so the author knows the move. [S-REV-6] [S-MNT-3]

## Opinionated advice: weigh it

Books and style guides disagree (for example on how small functions should be, or on comments). Do not quote a rule as law. Prefer what the project already does; where the project has no rule, prefer the simpler option and say why. [S-MNT-2] [S-MNT-1]

## Do not

- Report formatting or naming taste when a formatter or the project's convention already decides it; at most one line, and not as a blocker.
- Ask for a rewrite when the code works and is readable.
- Pile up Minor remarks: keep the best three, mention that there are more only if they matter.
- Suggest abstractions the change does not need.

## Severity

- Maintainability problems are **Minor** by default. They become **Important** when they hide bugs (so tangled the logic cannot be verified), when they make a hot area unsafe to change (a 300-line function with no tests), or when duplication already caused inconsistent behaviour.

## Sources
[S-REV-1] [S-REV-2] [S-REV-6] [S-MNT-1] [S-MNT-2] [S-MNT-3] [S-MNT-4] [S-MNT-7]
