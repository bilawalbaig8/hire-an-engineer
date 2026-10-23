# Sources for the Backend & Integration Engineer

Where this role's knowledge comes from. The outside sources were researched for the role document (`docs/agents/roles/backend-integration-engineer.md`) on 2026-10-23 and 2026-10-24: each page, or its Open Library, Crossref or arXiv record, was opened and the title or author matched. The URLs were opened again by a script on 2026-10-23 when this list was written: 77 of 80 answered; the other 3 are the 2 unverified rows below and the ACM link of S-REL-4, which blocks scripts and stays verified from its Crossref record. 75 outside sources (72 verified, 3 unverified), plus 5 files of our own base skill.

How to use these sources
- Ideas only, in our own words. Never copy passages. Cite a source by its ID, for example `[S-REL-1]`.
- Cite a source as fact only when its Status is `verified`. A row marked `unverified` is a lead: say "unverified" in the same line when you mention it.
- Pages marked `current` change over time. Provider limits, prices, versions, error codes and terms are read from the live page during the job, with the date read, never from this list or from memory.
- Vendor documentation (Stripe, Twilio, GitHub, Slack and others) shows good practice and features, not proof, and none of these vendors is chosen for the owner.
- Law and terms pages are orientation only, never legal advice; a lawyer decides.

## Our own base (the owner's hire-an-engineer skill, in this repo)

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-OWN-1 | hire-an-engineer: Integrations (skills/hire-an-engineer/references/integrations.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Sections 1 to 10: find the APIs, research before choosing, accounts and keys, adapter design, testing, register, health, payments, messaging. The base of Connect and Check. | Own work (see the repository licence) | verified |
| S-OWN-2 | hire-an-engineer: Engineering Discipline (skills/hire-an-engineer/references/engineering-discipline.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Test first for core logic, evidence before "done". | Own work (see the repository licence) | verified |
| S-OWN-3 | hire-an-engineer: Database (skills/hire-an-engineer/references/database.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Schema rules, migrations with a backup, constraints in the database, tested restore. | Own work (see the repository licence) | verified |
| S-OWN-4 | hire-an-engineer: Engineering Principles (skills/hire-an-engineer/references/engineering-principles.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | OWASP checklist, least privilege, secrets, package checks, the "10 times bigger" check, size tiers. | Own work (see the repository licence) | verified |
| S-OWN-5 | hire-an-engineer: Cost Management (skills/hire-an-engineer/references/cost-management.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Cost register and budgets for paid services. | Own work (see the repository licence) | verified |

## Data and systems

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-SYS-1 | Designing Data-Intensive Applications | Martin Kleppmann | 2017 | https://dataintensive.net/ | Transactions, replication, consistency and the cost of distributed state. | Paid book | verified |
| S-SYS-2 | Patterns of Enterprise Application Architecture | Martin Fowler | 2002 | https://martinfowler.com/books/eaa.html | Service layer, data mapper, unit of work. | Paid book | verified |
| S-SYS-3 | Release It! 2nd ed. | Michael Nygard | 2018 | https://pragprog.com/titles/mnee2/release-it-second-edition/ | Stability patterns: timeouts, circuit breakers, bulkheads. | Paid book | verified |
| S-SYS-4 | Monolith First | Martin Fowler | 2015 | https://martinfowler.com/bliki/MonolithFirst.html | Simplest shape first: one service and one database. | Free to read | verified |
| S-SYS-5 | The Twelve-Factor App | Adam Wiggins | 2011 | https://12factor.net/ | Config in environment variables, backing services as attached resources. | Free to read | verified |

## APIs and HTTP

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-API-1 | Architectural Styles and the Design of Network-based Software Architectures (PhD thesis) | Roy Fielding | 2000 | https://ics.uci.edu/~fielding/pubs/dissertation/top.htm | REST constraints. | Free to read | unverified |
| S-API-2 | RFC 9110 HTTP Semantics | IETF (Fielding, Nottingham, Reschke) | 2022 | https://www.rfc-editor.org/rfc/rfc9110 | Methods, status codes, safe and idempotent methods. | Free (IETF Trust) | verified |
| S-API-3 | RFC 9457 Problem Details for HTTP APIs | IETF (Nottingham, Wilde, Dalal) | 2023 | https://www.rfc-editor.org/rfc/rfc9457 | One consistent error shape. | Free (IETF Trust) | verified |
| S-API-4 | OpenAPI Specification 3.1.0 | OpenAPI Initiative | 2021 | https://spec.openapis.org/oas/v3.1.0 | Written API contract. | Free (Apache 2.0) | verified |
| S-API-5 | API Improvement Proposals (AIP) | Google | current | https://google.aip.dev/ | Resource naming, paging, errors. | Free to read | verified |
| S-API-6 | RFC 6585 Additional HTTP Status Codes (429 Too Many Requests) | IETF (Nottingham, Fielding) | 2012 | https://www.rfc-editor.org/rfc/rfc6585 | 429 and Retry-After for rate limits. | Free (IETF Trust) | verified |
| S-API-7 | RFC 8288 Web Linking | IETF (Nottingham) | 2017 | https://www.rfc-editor.org/rfc/rfc8288 | The Link header used for paging. | Free (IETF Trust) | verified |
| S-API-8 | Google Cloud API Design Guide | Google | current | https://cloud.google.com/apis/design | Resource-oriented design, errors, versioning. | Free to read | verified |
| S-API-9 | Microsoft REST API Guidelines | Microsoft | current | https://github.com/microsoft/api-guidelines | Errors, paging, long-running operations. | Free (MIT / CC BY) | verified |
| S-API-10 | RFC 9309 Robots Exclusion Protocol | IETF (Koster et al.) | 2022 | https://www.rfc-editor.org/rfc/rfc9309 | robots.txt rules a collector must respect. | Free (IETF Trust) | verified |

## Databases

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-DB-1 | Transaction Isolation (PostgreSQL docs) | PostgreSQL Global Development Group | current | https://www.postgresql.org/docs/current/transaction-iso.html | Isolation levels and races. | Free (PostgreSQL licence) | verified |
| S-DB-2 | Indexes (PostgreSQL docs) | PostgreSQL Global Development Group | current | https://www.postgresql.org/docs/current/indexes.html | Indexes for the queries the routes run. | Free (PostgreSQL licence) | verified |
| S-DB-3 | Write-Ahead Logging (SQLite docs) | SQLite | current | https://www.sqlite.org/wal.html | SQLite concurrency for small projects. | Free (public domain) | verified |
| S-DB-4 | Use The Index, Luke | Markus Winand | current | https://use-the-index-luke.com/ | Measuring and fixing slow queries. | Free to read | verified |
| S-DB-5 | Evolutionary Database Design | Pramod Sadalage, Martin Fowler | 2016 | https://martinfowler.com/articles/evodb.html | Small additive migrations: expand, backfill, switch, remove. | Free to read | verified |
| S-DB-6 | Row Level Security (Supabase docs) | Supabase | current | https://supabase.com/docs/guides/database/postgres/row-level-security | Access rules in the database. | Free to read | verified |

## Security, login and keys

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-SEC-1 | API Security Top 10 | OWASP | 2023 | https://owasp.org/API-Security/editions/2023/en/0x00-header/ | Object-level and property-level authorization, resource limits. | Free (CC BY-SA 4.0) | verified |
| S-SEC-2 | OWASP Top 10 | OWASP | 2021 | https://owasp.org/Top10/ | Web risks baseline. | Free (CC BY-SA 4.0) | verified |
| S-SEC-3 | Application Security Verification Standard | OWASP | current | https://owasp.org/www-project-application-security-verification-standard/ | Checklist depth for a first API safety pass. | Free (CC BY-SA 4.0) | verified |
| S-SEC-4 | SQL Injection Prevention Cheat Sheet | OWASP | current | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html | Parameterised queries. | Free (CC BY-SA 4.0) | verified |
| S-SEC-5 | Password Storage Cheat Sheet | OWASP | current | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html | Never hand-rolled password storage. | Free (CC BY-SA 4.0) | verified |
| S-SEC-6 | SP 800-63B Digital Identity Guidelines (authentication) | NIST | current | https://pages.nist.gov/800-63-4/sp800-63b.html | Authentication strength. | Free (US government work) | verified |
| S-SEC-7 | RFC 6749 The OAuth 2.0 Authorization Framework | IETF (Hardt) | 2012 | https://www.rfc-editor.org/rfc/rfc6749 | OAuth flows. | Free (IETF Trust) | verified |
| S-SEC-8 | RFC 9700 Best Current Practice for OAuth 2.0 Security | IETF (Lodderstedt et al.) | 2025 | https://www.rfc-editor.org/rfc/rfc9700 | Current OAuth safety rules. | Free (IETF Trust) | verified |
| S-SEC-9 | RFC 8725 JSON Web Token Best Current Practices | IETF (Sheffer, Hardt, Jones) | 2020 | https://www.rfc-editor.org/rfc/rfc8725 | Token checks. | Free (IETF Trust) | verified |
| S-SEC-10 | We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs | Joseph Spracklen et al. | 2024 | https://arxiv.org/abs/2406.10279 | Check that a package exists before adding it. | Free (arXiv) | verified |
| S-SEC-11 | GDPR Article 25 (data protection by design) | European Union | 2016 | https://gdpr-info.eu/art-25-gdpr/ | Privacy by design as orientation; a lawyer decides. | Free to read | verified |
| S-SEC-12 | RFC 7636 Proof Key for Code Exchange (PKCE) | IETF (Sakimura et al.) | 2015 | https://www.rfc-editor.org/rfc/rfc7636 | OAuth for public clients. | Free (IETF Trust) | verified |
| S-SEC-13 | OAuth 2.0 Simplified | Aaron Parecki | current | https://www.oauth.com/ | Plain explanation of OAuth flows with providers. | Free to read | verified |
| S-SEC-14 | Secrets Management Cheat Sheet | OWASP | current | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | Keys out of code, rotation, a pasted key is leaked. | Free (CC BY-SA 4.0) | verified |
| S-SEC-15 | Server-Side Request Forgery Prevention Cheat Sheet | OWASP | current | https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html | No blind redirects or URLs from outside answers. | Free (CC BY-SA 4.0) | unverified |
| S-SEC-16 | API10:2023 Unsafe Consumption of APIs | OWASP | 2023 | https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/ | Data from a provider is checked like user input. | Free (CC BY-SA 4.0) | verified |
| S-SEC-17 | RFC 7009 OAuth 2.0 Token Revocation | IETF (Lodderstedt et al.) | 2013 | https://www.rfc-editor.org/rfc/rfc7009 | Revoking a leaked or unused token. | Free (IETF Trust) | verified |

## Reliability, idempotency and webhooks

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-REL-1 | Idempotent requests (Stripe docs) | Stripe | current | https://docs.stripe.com/api/idempotent_requests | Idempotency keys on calls that create or charge. | Free to read | verified |
| S-REL-2 | Receive events in your webhook endpoint (Stripe docs) | Stripe | current | https://docs.stripe.com/webhooks | Signature check, fast answer, duplicate and out-of-order events. | Free to read | verified |
| S-REL-3 | Timeouts, retries, and backoff with jitter | Marc Brooker (Amazon) | 2019 | https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ | Timeouts, retries with jitter and a retry budget. | Free to read | verified |
| S-REL-4 | Idempotence Is Not a Medical Condition | Pat Helland | 2012 | https://doi.org/10.1145/2160718.2160734 | Why messages arrive more than once. | Paid (ACM) | verified |
| S-REL-5 | Pattern: Transactional outbox | Chris Richardson | current | https://microservices.io/patterns/data/transactional-outbox.html | Save and send in one step. | Free to read | verified |
| S-REL-6 | Exponential Backoff And Jitter | Marc Brooker (AWS) | 2015 | https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/ | Why plain backoff is not enough. | Free to read | verified |
| S-REL-7 | Circuit Breaker | Martin Fowler | 2014 | https://martinfowler.com/bliki/CircuitBreaker.html | Stop calling a failing service for a while. | Free to read | verified |
| S-REL-8 | Addressing Cascading Failures (SRE book) | Google SRE | 2016 | https://sre.google/sre-book/addressing-cascading-failures/ | Retry storms and load shedding. | Free to read | verified |
| S-REL-9 | Designing robust and predictable APIs with idempotency | Brandur Leach (Stripe) | 2017 | https://stripe.com/blog/idempotency | A written idempotency design. | Free to read | verified |
| S-REL-10 | The Idempotency-Key HTTP Header Field (draft) | IETF HTTPAPI working group | draft | https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ | Header name and rules for idempotency keys. | Free (IETF Trust) | verified |
| S-REL-11 | Standard Webhooks specification | Standard Webhooks | current | https://www.standardwebhooks.com/ | Signature, id and timestamp for webhooks. | Free (Apache 2.0) | verified |
| S-REL-12 | Best practices for using webhooks | GitHub | current | https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks | Answer fast, work in the background, handle redeliveries. | Free to read | verified |
| S-REL-13 | Validating webhook deliveries | GitHub | current | https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries | Constant-time signature check. | Free to read | verified |
| S-REL-14 | Secure webhooks | Twilio | current | https://www.twilio.com/docs/usage/webhooks/webhooks-security | Signature checks for messaging webhooks. | Free to read | verified |

## Integration patterns and rate limits

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-INT-1 | Enterprise Integration Patterns | Gregor Hohpe, Bobby Woolf | 2003 | https://www.enterpriseintegrationpatterns.com/ | Adapters, queues, idempotent receiver. | Paid book (site free to read) | verified |
| S-INT-2 | Rate limits for the REST API | GitHub | current | https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api | Reading limit headers and waiting for the reset. | Free to read | verified |
| S-INT-3 | API reference: Pagination | Stripe | current | https://docs.stripe.com/api/pagination | Cursor paging. | Free to read | verified |
| S-INT-4 | Rate limits (Web API) | Slack | current | https://api.slack.com/docs/rate-limits | Tiered limits and Retry-After. | Free to read | verified |
| S-INT-5 | RateLimit header fields for HTTP (draft 11) | IETF HTTPAPI working group (Polli et al.) | draft | https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/ | Standard limit headers; many providers use their own names. | Free (IETF Trust) | verified |
| S-INT-6 | Test card numbers (testing docs) | Stripe | current | https://docs.stripe.com/testing | Test mode and test data before live. | Free to read | verified |

## Testing integrations

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-TST-1 | Consumer-Driven Contracts: A Service Evolution Pattern | Ian Robinson (on martinfowler.com) | 2006 | https://martinfowler.com/articles/consumerDrivenContracts.html | Contract tests between a consumer and a provider. | Free to read | verified |
| S-TST-2 | Pact documentation | Pact Foundation | current | https://docs.pact.io/ | Consumer-driven contract testing tool. | Free (MIT) | verified |
| S-TST-3 | WireMock documentation | WireMock | current | https://wiremock.org/docs/ | API mocking. | Free (Apache 2.0) | verified |
| S-TST-4 | VCR.py documentation | Kevin McCarthy et al. | current | https://vcrpy.readthedocs.io/ | Record and replay HTTP, with filters for secrets. | Free (MIT) | verified |
| S-TST-5 | Test Pyramid | Martin Fowler | 2012 | https://martinfowler.com/bliki/TestPyramid.html | Many fast unit tests, few slow end-to-end tests. | Free to read | verified |
| S-TST-6 | Tolerant Reader | Martin Fowler | 2011 | https://martinfowler.com/bliki/TolerantReader.html | Read only the fields you need, so small provider changes do not break you. | Free to read | verified |

## Change and drift

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-DRF-1 | RFC 8594 The Sunset HTTP Header Field | IETF (Wilde) | 2019 | https://www.rfc-editor.org/rfc/rfc8594 | The date after which a resource stops working. | Free (IETF Trust) | verified |
| S-DRF-2 | RFC 9745 The Deprecation HTTP Response Header Field | IETF (Dalal, Wilde) | 2025 | https://www.rfc-editor.org/rfc/rfc9745 | A provider's own signal that a resource is deprecated. | Free (IETF Trust) | verified |
| S-DRF-3 | AIP-180 Backwards compatibility | Google | 2019 | https://google.aip.dev/180 | What counts as a breaking change. | Free to read | verified |
| S-DRF-4 | Upgrade your integration (API versions and webhook endpoints) | Stripe | current | https://docs.stripe.com/upgrades | Pinned API versions and planned upgrades. | Free to read | verified |

## Operations

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-OPS-1 | Site Reliability Engineering | Betsy Beyer et al. | 2016 | https://sre.google/sre-book/table-of-contents/ | Monitoring, error budgets, health checks. | Free to read online | verified |
| S-OPS-2 | The Site Reliability Workbook | Betsy Beyer et al. | 2018 | https://sre.google/workbook/table-of-contents/ | Practical alerting and on-call. | Free to read online | verified |
| S-OPS-3 | Observability primer | OpenTelemetry | current | https://opentelemetry.io/docs/concepts/observability-primer/ | Logs, metrics and traces. | Free (CC BY 4.0) | verified |
| S-OPS-4 | Software Engineering at Google | Titus Winters, Tom Manshreck, Hyrum Wright | 2020 | https://abseil.io/resources/swe-book | Testing at scale, code review. | Free to read online | verified |

## Owner's data sources

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-SRC-1 | Meta Ad Library API | Meta | current | https://www.facebook.com/ads/library/api/ | Ad-library collection; read the live terms and limits before building. | Free to read (terms apply) | unverified |
| S-SRC-2 | App Store Connect API | Apple | current | https://developer.apple.com/documentation/appstoreconnectapi | Store data and keys. | Free to read (terms apply) | verified |
| S-SRC-3 | Google Play Developer API | Google | current | https://developers.google.com/android-publisher | Store data and keys. | Free to read (terms apply) | verified |

## Limits of this list

Three entries are unverified: the Fielding thesis (certificate error from the script), the OWASP SSRF cheat sheet (page opened, key phrase not found) and the Meta Ad Library API page (the site blocks scripts). The checks covered that each page opens and that the title, author or record matches, not every claim inside each source. There is little here on game-specific services (for example in-app purchase servers) beyond the app-store APIs, and nothing on market-data vendors. Nothing here replaces a security audit, a load test or a lawyer.
