# Security review

When to read this: when the change touches input, users, permissions, data storage, files, network calls, secrets, dependencies, or anything exposed to the internet. Skim it for every review: the Critical findings usually live here.

This is a review lens, not a full security audit. If the change needs threat modelling, a penetration test or a compliance check, say so and recommend a Security Engineer.

## How to look

1. **Find the entry points the change adds or touches:** new routes, functions that take outside input, file or message handlers.
2. **Follow each outside value from where it comes in to where it is used:** a query, a command, a file path, a template, a response, a log line. Ask whether it is checked on the way and how it is used at the end.
3. **For every action, ask who may do it, and where the check is.** The check must be on the server, in the code that does the action, not only in the screen.
4. **Look for secrets and personal data:** where they are stored, passed, logged.
5. Use the OWASP review and checklist material to cover classes you did not think of, and name findings with the weakness class so they can be tracked. [S-SEC-1] [S-SEC-2] [S-SEC-4] [S-SEC-5]

## Checks (each one a question you can answer from the diff)

| Class | What to look for |
|---|---|
| **Injection** | User input joined into SQL, shell commands, file paths, templates, LDAP or regular expressions by string concatenation or formatting. The fix is a parameter, a safe API, or an allow-list for identifiers (table and column names, `ORDER BY` direction), never hand-sanitising values. Name the triggering input (a quote character, `../`, a semicolon). |
| **Broken access control** | A new action with no permission check; a check that trusts the client (a hidden button, a role in the request); an object looked up by id without checking it belongs to the caller; an admin function reachable by any user. Compare with the stated rules (README, requirement). [S-SEC-2] [S-SEC-3] |
| **Authentication and sessions** | Home-made password handling, passwords or tokens stored in plain text, or secrets compared with `==` (timing leak: use a constant-time compare or the library's verify function), tokens that never expire, tokens in URLs or logs, missing rate limits on sign-in. |
| **Secrets** | Keys, passwords, tokens or connection strings in the code, tests, examples or config files in the repository. Treat a committed live secret as compromised: say it must be removed from the code and rotated, not only deleted from the latest version. |
| **Input validation and output** | Missing length, type or range checks at the boundary; output written into HTML, URLs or logs without escaping; error messages that reveal internals. |
| **Files and paths** | Uploads without type and size checks, user-controlled file names, path traversal, files written to a shared folder, temp files with predictable names. |
| **Outgoing requests** | A server that fetches a URL from user input (server-side request forgery); disabled certificate checks; no timeout. |
| **Deserialisation and dynamic code** | Loading untrusted data with formats that can run code; `eval`/`exec` or reflection on outside strings. |
| **Cryptography** | Home-made schemes; outdated algorithms; fixed or reused IVs and salts; random numbers from a non-secure generator for tokens. Recommend a standard library or service. |
| **Data exposure** | Responses returning more fields than needed; personal data in logs or analytics; debug endpoints left on. [S-LOG-2] [S-LOG-3] |
| **Dependencies** | A new package: does it exist, who maintains it, is the name a lookalike, is it needed at all, does it have an install script? A version pinned? Use local evidence only (lockfile, installed or vendored package metadata); otherwise raise a needs-check question. [S-SEC-10] |
| **Denial of service** | Unbounded input size, expensive work per request, regular expressions with catastrophic backtracking, unbounded loops on user-controlled counts. |
| **Configuration** | Debug mode, permissive cross-origin rules, default credentials, open ports, publicly readable storage. |
| **Logging** | No audit trail for sensitive actions, or secrets and personal data written to logs. |
| **APIs** | Broken object-level authorisation, excessive data exposure, missing rate limits, mass assignment of fields the caller should not set. [S-SEC-3] |
| **AI features** | Outside text treated as instructions (prompt injection), an AI that can take irreversible actions without a human step, secrets or private data sent to a model provider. |

## Severity

- **Critical:** exploitable by an outsider or an ordinary user with serious impact (injection that reaches data, missing authorisation on a destructive action, a live secret committed, remote code execution).
- **Important:** a real weakness with limited reach or a precondition (missing rate limit on sign-in, over-broad responses, weak validation with a safe sink).
- **Minor:** hardening (extra headers, logging detail).
State the attacker, the input and the impact in one sentence each.

## How to word a finding
"`shop/search.py` builds the query by joining the `term` text into SQL. An input like `' OR 1=1 --` returns every order. Use a query parameter."

## Do not
- Write or run exploit code against anything; read and reason only.
- Call something secure because it uses a framework; check how the framework is used.
- Report a theoretical weakness with no path to it as Critical; label it `needs-check`, put it under questions (it does not count toward the verdict) and explain what would make it real.
- Paste secrets into the report: describe where they are, never print their values.

## When to hand over
Escalate to a Security Engineer for: threat modelling a new feature, cryptographic design, authentication design, compliance, anything touching payments or health or children's data at scale, or a suspected breach. [S-SEC-6] [S-SEC-9]

## Sources
[S-SEC-1] [S-SEC-2] [S-SEC-3] [S-SEC-4] [S-SEC-5] [S-SEC-6] [S-SEC-7] [S-SEC-8] [S-SEC-9] [S-SEC-10] [S-LOG-2] [S-LOG-3]
