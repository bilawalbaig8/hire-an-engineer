# Security architecture

When to read this: you are designing or reviewing anything that holds user data, takes logins, handles money, runs code for other people, or is reachable from the internet. Security is designed in at the start, not added at the end.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| When to think about threats | **During design**: draw the data flows and trust boundaries, then ask four questions: what are we building, what can go wrong, what will we do about it, did we do well enough. [S-WEB-19] [S-WEB-20] | A lighter pass for a throwaway prototype, written down as such. | Threat modelling gives up a few hours at the start; skipping it gives up the cheapest time to fix things. |
| How to find what can go wrong | **A simple checklist of threat types** (spoofing, tampering, denial of service, leaking information, privilege escalation) applied to each flow and each boundary. [S-WEB-19] | Free brainstorming when the system is tiny. | A checklist can miss novel threats; brainstorming can miss the boring ones. |
| How to define "secure enough" | **Turn security wishes into testable requirements** at a chosen level (a recognised verification standard has levels for ordinary and high-risk systems). [S-WEB-18] | A short list of your own tested rules for small systems. | A standard gives up time and some flexibility; it pays back as a clear test list. |
| Trust inside your own network | **Do not trust a request because it came from inside**: authenticate and authorise every service-to-service call. [S-WEB-22] | Network separation as an extra layer, never the only one. | Zero-trust style design gives up some simplicity and speed for a smaller blast radius. |
| Identity | **A managed identity provider** or a vetted library; separate "who are you" from "what may you do" (permissions checked on the server, every time). | Your own only with expert review. | A provider gives up some control and adds cost. |
| Access | **Least privilege**: every account, key and service gets only what it needs, with expiry where possible. | Broader access for a short, written, reviewed period. | Least privilege gives up convenience. |
| Secrets | **A secret store or the platform's secret feature**; never in code, never in logs, rotated when leaked. | Environment variables on a locked-down host, with the same rules. | Secret stores add a dependency and a setup step. |
| Dependencies | **Check each new package before installing** (does it exist, who maintains it, is the name a lookalike), pin versions, and watch for known problems. [S-WEB-21] | A vendored copy for critical code. | Checking gives up speed; skipping it gives up protection against fake or hijacked packages. |
| Data protection | **Collect less, keep it shorter, encrypt in transit and at rest, and know who can read it.** | Keep more only for a stated legal or product reason. | Less data gives up some analytics and features. |
| Security and reliability together | **Design them together**: many failures that look like outages are security events, and the other way round. (unverified source S-WEB-4 discusses this) | Treat them separately only in small systems. | Together costs a joint design effort. |

## Typical shapes

- **Public web app:** browser to a gateway or app, then to the database. Boundaries: browser to server, server to database, server to third parties. Check each.
- **API with partners or mobile apps:** tokens with short lifetimes, scopes per client, rate limits.
- **Multi-tenant system:** one tenant must never see another's data; enforce it in one central place, not in every query by hand.
- **Admin tooling:** its own strong sign-in, audit log, and no shared accounts.
- **Anything with AI features:** follow `ai-systems` and treat all outside text as untrusted. [S-AI-9]

## Failure modes

- **Broken access checks:** the screen hides a button but the server still allows the action.
- **Secrets in the repository, in logs or in screenshots.**
- **Trusting input:** unvalidated data reaches the database, a shell, a file path or another user's screen.
- **Over-wide keys:** one key that can do everything, shared by every service.
- **Outdated or fake dependencies.**
- **No audit trail:** you cannot tell what happened after an incident.
- **Security as a final checkbox:** found late, fixed expensively or never.

## Questions that change the design

- What is the worst thing an attacker could do or see here? Who would want to?
- What personal, financial, health or children's data is held? Which laws or store rules apply?
- Who are the different kinds of users and administrators, and what may each do?
- Which external systems are called, and with what keys?
- Is there an existing sign-in system or compliance requirement?

## Checks before you hand it back

- [ ] A data flow and trust boundary sketch exists, and each boundary has a listed threat and mitigation.
- [ ] Permissions are checked on the server for every action, not only in the screen.
- [ ] No secrets in code or logs; rotation is possible.
- [ ] Every account and key has only the access it needs.
- [ ] New dependencies were checked, and versions are pinned.
- [ ] Personal data is minimised, and who can see it is written down.
- [ ] The top security requirements are testable, and someone owns testing them. [S-WEB-18]
- [ ] An incident plan exists, even if it is one page: who is told, what is switched off, how keys are rotated.

## Sources
[S-WEB-18] [S-WEB-19] [S-WEB-20] [S-WEB-21] [S-WEB-22] [S-AI-9] and, as an unverified lead only, S-WEB-4
