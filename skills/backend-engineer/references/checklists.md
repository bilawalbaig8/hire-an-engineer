# Checklists before "done"

## 1. When to read this
Before you answer the boss with `done`, and for any review. Tick only what you ran or read; mark the rest "not checked".

## 2. Tests and evidence
- [ ] The test command ran and its result line is in `evidence`.
- [ ] Core logic and failure paths have tests; a bug fix has the test that reproduced it.
- [ ] One run with generated data at about 10 times the expected size, with the timing noted.
- [ ] The README runs the project from a clean checkout in about 15 minutes.

## 3. Data
- [ ] Constraints, keys and uniqueness live in the database, not only in code.
- [ ] Indexes exist for the queries the routes run; lists are paginated.
- [ ] Each migration is numbered, small and additive, ran on a test copy, with a backup first and written restore steps.
- [ ] The data dictionary matches the schema and marks personal data.

## 4. API and permissions
- [ ] Every route that reads or changes a record checks, on the server, that the caller may touch that record (a test where user A reads user B's data fails).
- [ ] Field-level checks: a caller cannot read or set fields they should not (for example a role or price field).
- [ ] Input is checked at the edge; queries are parameterised, never built from strings.
- [ ] One consistent error shape; errors do not leak stack traces or internals.
- [ ] Login uses a proven auth provider; passwords are never stored by hand-rolled code.
- [ ] Rate limits on login and costly routes.

## 5. Outside services and jobs
- [ ] One adapter per service; mocked in tests for success, failure, timeout and duplicate.
- [ ] Every outside call has a timeout; retries use backoff with random jitter and a total limit.
- [ ] Anything that charges, creates or sends is idempotent (idempotency key or unique key).
- [ ] Webhooks are verified and handled safely when they arrive twice or out of order.
- [ ] Jobs and schedules survive a crash and a repeat run without double effects.
- [ ] The integrations register lists every service, owner of the account, key name and test or live.

## 6. Secrets and operations
- [ ] No secret values in code, config, docs, tests or answers; config comes from environment variables.
- [ ] Packages added exist and were checked; none are guessed names.
- [ ] Structured logs without personal data or secrets; a health check; error tracking named.

## 7. Honest claims
- [ ] Every claim is labelled `verified`, `inferred` or `unknown`.
- [ ] The answer says what was not run or measured.
- [ ] Anything live, paid, permanent or public-facing is an approval, not a step taken; so are auth or permission designs, data and API formats other code depends on, and money flows.
- [ ] The answer says "Code Reviewer review pending"; it does not claim its own work was reviewed.
