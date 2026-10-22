# Correctness and edge cases

When to read this: for every review. Correctness is the first lens: does the code do the right thing, not only on the happy path?

## How to look

Do not read for "does it look fine". Trace it with concrete values:

1. Pick a normal input and follow it through, line by line, writing down the values.
2. Pick the awkward inputs from the table below and do the same.
3. Check what the change was supposed to do (the requirement, the README rules, the existing tests) against what it does with those values.
4. When a test already covers the case, read what the test really asserts; a test that passes is not proof if it asserts nothing (see `tests-review`).

A finding is real when you can state the input and the wrong result: "quantity 10 now gets no discount; the old test `test_discount_at_ten` would fail."

## Inputs to try

| Kind | Try |
|---|---|
| Numbers | zero, one, minus one, the boundary of every rule (the exact limit, one below, one above), very large, a fraction, not a number |
| Collections | empty, one item, many items, duplicates, unsorted, contains null |
| Text | empty, only spaces, very long, accents and non-Latin letters, emoji, newlines, quote characters, something that looks like code or a path |
| Dates and time | midnight, the end of a month or year, daylight-saving changes, different time zones, leap days, a date in the past or far future. [S-MNT-8 is an unverified source of time pitfalls] |
| Absent things | missing field, null or none, missing file, empty response, the object was deleted meanwhile |
| Order and repeat | the same request twice, two requests at once, steps in a different order, a retry after a failure |
| Failure | the network call fails or is slow, the disk is full, the database rejects the write, the process stops halfway |

## What goes wrong most often

- **Boundaries and comparison operators.** `>` versus `>=`, `<` versus `<=`, off by one in a loop or a slice, "within 14 days" counted as 14 or 15. Compare each comparison with the rule it implements, in the README, the requirement or the old code.
- **Wrong or missing error handling.** An error is caught and ignored (`except: pass`, an empty `catch`), the wrong error type is caught, a failure returns a value that looks like success (None, empty list, true), or the error message hides the cause. A function that returns nothing after its last attempt fails silently. Swallowed errors are an Important finding when they sit on a path that matters (payments, saving, security).
- **Half-finished changes.** Two writes that must succeed together are done separately (two commits, or a file and a database row). If the second fails, the first stays. Ask: what state is the system in if it stops here? Look for a transaction, an undo step, or a design where partial states are harmless.
- **Repeats and retries.** Doing the same operation twice (a double click, a retry, a duplicated message) should not double-charge, double-count or restore stock twice. Look for a request id, a status check ("already refunded") or a natural idempotency.
- **Shared state and concurrency.** Check-then-act on shared data (read stock, then write stock) can interleave with another request; shared collections modified from several threads or tasks; a lock held across a slow call; a lock acquired in different orders. For concurrent code ask which data is shared, who writes it, and what guarantees ordering. [S-MNT-6]
- **Money and measurements.** Money in whole minor units (cents), never floating point; check rounding rules explicitly; do not mix units (seconds and milliseconds, metres and feet, bytes and kilobytes); watch integer overflow and division that truncates.
- **Resource handling.** Files, connections and locks opened and not closed on every path (including error paths); resources created in a loop.
- **Absent values.** A value that can be missing is used as if it were present; an optional field is assumed; a lookup result is not checked before use.
- **Conditions and flow.** Inverted conditions, `and` where `or` was meant, a condition that is always true or false, unreachable branches, a missing `else`, a `return` placed inside a loop, shadowed variables, copy-pasted code where one name was not changed.
- **Contracts.** The function's callers expect a type, a unit, an order, a sorted result, or an exception that the change silently altered; a changed return shape breaks every caller (look them up).
- **Inconsistency with the rules of the project.** The code contradicts a README rule, a documented invariant or an earlier decision.

## Questions that find bugs

- What does this assume that nothing guarantees?
- What happens on the second call? On the empty case? When it fails here?
- Who else calls this, and what do they expect?
- What does the existing test suite say about the rule the change touches, and does it still pass?
- If I removed this change's key line, would any test notice?

## Reading the tests as evidence

If tests exist, run the focused ones for the touched code (read-only, no installs) and report the result. A new failure in an old test is a strong, cheap-to-confirm finding. If you cannot run them, say so and say which test you would run.

## Severity hints

- Wrong results in the core behaviour, lost or corrupted data, silent failure on money or security paths: Critical or Important.
- Boundary regressions against a stated rule: Important.
- Rare edge cases with a harmless result: Minor, or a question.

## Sources
[S-MNT-1] [S-MNT-5] [S-MNT-6] and, as an unverified lead only, S-MNT-8
