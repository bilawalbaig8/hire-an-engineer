# Reviewing tests

When to read this: whenever the change adds or changes tests, or changes behaviour without changing any test. Tests are code too, and a test that proves nothing is worse than no test because it gives false comfort.

## The one question

**Would this test fail if the code were wrong?** For each important test, imagine breaking the code under test in a plausible way (flip a comparison, remove a line, return a wrong value). If the test would still pass, it does not protect anything. This is the idea behind mutation testing, which automates the question. [S-TST-6]

## What to check

| Check | Bad sign |
|---|---|
| **It asserts something** | A test that calls the function and checks nothing; `assertTrue(True)`; an assertion on a value the test itself just set; a test with only "no exception thrown" for behaviour that has results. |
| **It asserts the right thing** | Checks that something is not `None` when it should check the value; compares a result to itself; asserts on a mock that the test configured. |
| **It covers the change** | The new branch, the new rule, the boundary values and the failure path have no test. List the missing cases specifically. |
| **It covers the real risk** | Tests only the easy path while the dangerous case (negative total, empty input, duplicate request, missing permission) is untested. |
| **It tests behaviour, not wiring** | Heavy use of mocks so the test only verifies that the code calls the things it was written to call; tests that break on every harmless refactor. [S-TST-4] |
| **It is independent and repeatable** | Depends on test order, shared global state, the real clock, the network, random numbers, or leftover files; sleeps instead of waiting for a condition. These become flaky tests that people learn to ignore. [S-TST-3] |
| **It is readable** | A name that says what is expected; the arrange, act, assert steps are visible; one reason to fail. |
| **It sits at the right level** | A broad end-to-end test used where a fast unit test would do, or only unit tests with nothing checking that the parts fit together. [S-TST-1] [S-TST-2] |
| **It was not changed to pass** | A previously failing test was weakened, deleted or skipped in the same change; an assertion loosened; an expected value edited to match new behaviour without a reason. |
| **Regression test for a fix** | A bug fix without a test that fails before the fix and passes after. |

## Gaps no test catches

Coverage numbers do not prove quality; a line can be run without being checked. Look for risk, not percentages. Where a rule has many inputs, a property-based test (describe what must always be true and let a tool try many inputs) finds cases examples miss. [S-TST-5]

## If the change has no tests

Say so, and say which behaviours most need one. A change to money, permissions, data migrations or parsing without tests is an Important finding; a cosmetic change without tests is fine.

## Running tests

If the project has a test command and it is safe (no installs, no network, no writes outside temp files), run the tests for the touched code and report the real result. A new failure in an existing test is a strong finding (a regression); name the test. If you did not run tests, say that and do not say they pass.

## Severity

- Tests that assert nothing for a core behaviour; a weakened or deleted test hiding a regression: **Important**.
- Missing test for a risky edge case: **Important** if the code path is risky, otherwise **Minor**.
- Naming, structure, small duplication in tests: **Minor**.

## Sources
[S-TST-1] [S-TST-2] [S-TST-3] [S-TST-4] [S-TST-5] [S-TST-6]
