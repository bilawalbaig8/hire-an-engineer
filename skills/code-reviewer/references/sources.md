# Sources for the Code Reviewer

Where the Reviewer's knowledge comes from. Researched and checked on 2026-10-23. Part A (review practice, testing, maintainability) and part B (security, AI-written code) were compiled and URL-checked by the controller; part C (languages, performance and data) comes from a separate research pass and is added below it when done.

How to use these sources
- Ideas only, in our own words. Never copy passages. Cite a source by its ID, for example `[S-REV-1]`.
- Cite a source as fact only when its Status is `verified`. A row marked `unverified` is a lead: say "unverified" in the same line when you mention it.
- `verified` means the page or listing was opened and showed the title and author, and the URL resolved. A year not shown on that page comes from the well-known edition. `unverified` means the page could not be opened, only a secondary page was found, or its content was not read. An unconfirmed licence alone does not change the status.
- Free does not mean copyable: summarise, never paste.

## Code review practice and research

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-REV-1 | Google Engineering Practices: How to do a code review (the reviewer guide) | Google | ongoing | https://google.github.io/eng-practices/review/reviewer/ | What to look for in a change, how to move fast, how to write comments, the standard "does it improve the code health". | Free, CC BY 3.0 per the site (licence unverified here) | verified |
| S-REV-2 | The CL author's guide to getting through code review | Google | ongoing | https://google.github.io/eng-practices/review/developer/ | How authors write reviewable changes (small, described, tested); useful for judging a change's scope. | Free; licence unverified | verified |
| S-REV-3 | Expectations, Outcomes, and Challenges of Modern Code Review | Alberto Bacchelli, Christian Bird | 2013 | https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/ | Research: reviews find fewer defects than people expect and spend much effort on understanding the change; context and clear descriptions matter. | Free to read; copyright | verified |
| S-REV-4 | Software Engineering at Google | Titus Winters, Tom Manshreck, Hyrum Wright (eds.) | 2020 | https://abseil.io/resources/swe-book | Chapter on code review, readability and testing at scale. | Free online | verified |
| S-REV-5 | Conventional Comments | Conventional Comments authors | ongoing | https://conventionalcomments.org/ | A short label scheme (praise, nitpick, suggestion, issue, question) that keeps review comments clear and low-noise. | Free; licence unverified | verified |
| S-REV-6 | Catalog of Refactorings | Martin Fowler | ongoing | https://refactoring.com/catalog/ | Names the standard code changes, so a review can say what move would fix a problem. | Free to read; copyright | verified |

## Testing

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-TST-1 | The Practical Test Pyramid | Ham Vocke | 2018 | https://martinfowler.com/articles/practical-test-pyramid.html | What belongs in unit, integration and end-to-end tests and why the mix matters. | Free to read; copyright | verified |
| S-TST-2 | Test Pyramid | Martin Fowler | 2012 | https://martinfowler.com/bliki/TestPyramid.html | Short statement of the test pyramid idea. | Free to read; copyright | verified |
| S-TST-3 | Flaky Tests at Google and How We Mitigate Them | John Micco | 2016 | https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | Why flaky tests hurt trust and what causes them; how to treat them in review. | Free to read; copyright | verified |
| S-TST-4 | xUnit Test Patterns: Refactoring Test Code | Gerard Meszaros | 2007 | http://xunitpatterns.com/ | Catalogue of test smells and patterns (fragile, obscure, erratic tests). | Book paid; the site is free | verified |
| S-TST-5 | Hypothesis documentation (property-based testing for Python) | Hypothesis project | current | https://hypothesis.readthedocs.io/en/latest/ | What property-based tests are and when they find what example tests miss. | Free, MPL-2.0 per the project (licence unverified here) | verified |
| S-TST-6 | Stryker: What is mutation testing? | Stryker Mutator | current | https://stryker-mutator.io/docs/ | Mutation testing as a way to check that tests actually fail when the code is wrong. | Free; licence unverified | verified |

## Maintainability, correctness and general craft

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-MNT-1 | Code Complete, 2nd ed. | Steve McConnell | 2004 | https://www.microsoftpressstore.com/store/code-complete-9780735619678 | Broad construction practice: defensive programming, error handling, complexity, checklists. | Paid | verified |
| S-MNT-2 | Clean Code: A Handbook of Agile Software Craftsmanship | Robert C. Martin | 2008 | https://www.pearson.com/en-us/subject-catalog/p/clean-code-a-handbook-of-agile-software-craftsmanship/P200000009044/9780136083238 | Naming, functions, comments and smells. Opinionated; weigh it against S-FND-5-style simplicity thinking. | Paid | verified |
| S-MNT-3 | Refactoring, 2nd ed. | Martin Fowler | 2018 | https://martinfowler.com/books/refactoring.html | Code smells and the refactorings that remove them. | Paid | verified |
| S-MNT-4 | Code Smell | Martin Fowler | 2006 | https://martinfowler.com/bliki/CodeSmell.html | Short definition: a surface sign that may point to a deeper problem, to be checked, not assumed. | Free to read; copyright | verified |
| S-MNT-5 | The Pragmatic Programmer, 20th Anniversary Edition | David Thomas, Andrew Hunt | 2019 | https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/ | Habits: DRY, orthogonality, design by contract, crash early. | Paid | verified |
| S-MNT-6 | Java Concurrency in Practice | Brian Goetz et al. | 2006 | https://jcip.net/ | Reasoning about shared state, visibility and locking; the best reference for concurrency review questions. | Paid | verified |
| S-MNT-7 | Cognitive Complexity: a new way of measuring understandability | G. Ann Campbell (SonarSource) | 2017 | https://www.sonarsource.com/resources/cognitive-complexity/ | A measure of how hard code is to read; a way to say "too complex" with a reason. | Free to read | verified |
| S-MNT-8 | Falsehoods programmers believe about time | Noah Sussman | 2012 | https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time | Time-handling traps (time zones, daylight saving, leap seconds). The page blocked the checker. | Free to read | unverified |

## Security review

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-SEC-1 | OWASP Code Review Guide | OWASP | ongoing | https://owasp.org/www-project-code-review-guide/ | How to review code for security issues: what to look at and how. | Free, CC BY-SA 4.0 (ideas summarised, text not copied) | verified |
| S-SEC-2 | OWASP Top 10 | OWASP | current | https://owasp.org/www-project-top-ten/ | The most common web application risk classes (access control, injection, cryptography, and others). | Free, CC BY-SA 4.0 | verified |
| S-SEC-3 | OWASP API Security Top 10 | OWASP | current | https://owasp.org/API-Security/ | API-specific risks: broken object-level authorisation, excessive data exposure, unrestricted resource use. | Free, CC BY-SA 4.0 | verified |
| S-SEC-4 | OWASP Cheat Sheet Series | OWASP | ongoing | https://cheatsheetseries.owasp.org/ | Short how-to sheets for injection, authentication, sessions, secrets, file upload, logging and more. | Free, CC BY-SA 4.0 | verified |
| S-SEC-5 | CWE Top 25 Most Dangerous Software Weaknesses | MITRE | current | https://cwe.mitre.org/top25/ | A ranked list of weakness types with identifiers; a way to name a finding precisely. | Free; MITRE terms | verified |
| S-SEC-6 | Microsoft Security Development Lifecycle | Microsoft | current | https://www.microsoft.com/en-us/securityengineering/sdl | Security practices across the development process, including review. | Free to read | verified |
| S-SEC-7 | The Art of Software Security Assessment | Mark Dowd, John McDonald, Justin Schuh | 2006 | https://www.informit.com/store/art-of-software-security-assessment-identifying-and-preventing-9780321444424 | Classic on finding vulnerabilities by reading code. | Paid | verified |
| S-SEC-8 | Secure by Design | Dan Bergh Johnsson, Daniel Deogun, Daniel Sawano | 2019 | https://www.manning.com/books/secure-by-design | Design habits that remove classes of security bugs (domain types, validation, immutability). | Paid | verified |
| S-SEC-9 | Threat Modeling: Designing for Security | Adam Shostack | 2014 (2nd edition listed on the site) | https://shostack.org/books/threat-modeling-book | Threat modelling method; the site now lists a second edition. | Paid | verified |
| S-SEC-10 | OpenSSF Scorecard | Open Source Security Foundation | current | https://securityscorecards.dev/ | Automated checks of a dependency's security health; useful when a change adds a package. | Free, Apache-2.0 per the project (licence unverified here) | verified |
| S-SEC-11 | SEI CERT Coding Standards | Carnegie Mellon SEI | ongoing | https://wiki.sei.cmu.edu/confluence/display/seccode | Secure coding rules for C, C++, Java and Perl. The wiki dropped the connection during the check. | Free to read | unverified |

## AI-written code

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-AIC-1 | Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions | Hammond Pearce et al. | 2021 | https://arxiv.org/abs/2108.09293 | Study: a large share of assistant-generated code for security-relevant tasks contained vulnerabilities. | Free (arXiv) | verified |
| S-AIC-2 | Do Users Write More Insecure Code with AI Assistants? | Neil Perry et al. | 2022 | https://arxiv.org/abs/2211.03622 | Study: people using an AI assistant wrote less secure code and were more confident in it. | Free (arXiv) | verified |
| S-AIC-3 | We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs | Joseph Spracklen et al. | 2024 | https://arxiv.org/abs/2406.10279 | Study: code-generating models often name packages that do not exist, which attackers can register ("slopsquatting"). | Free (arXiv) | verified |
| S-AIC-4 | GenAI and Code Security: What You Need to Know | Veracode | 2025 | https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/ | Industry report on the security of AI-generated code. The page was reachable; its findings were not read. | Free (form may apply); copyright | unverified |
| S-AIC-5 | AI assistant code quality research (duplication, churn) | GitClear | 2025 | https://www.gitclear.com/ai_assistant_code_quality_2025_research | Industry analysis of code duplication and churn associated with AI assistants. The page blocked the checker. | Free; copyright | unverified |

## Languages, performance and data

Compiled by a research pass on 2026-10-22 (pages fetched and read; book rows rest on search listings from at least two sources). Where the Use column says a page could not be read, the row is `unverified`.

### Python

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-LNG-1 | Programming FAQ (Python docs) | Python Software Foundation | Docs 3.15 | https://docs.python.org/3/faq/programming.html | Core-language traps (scoping, mutable defaults, copy vs reference, performance). Use for any Python diff with surprising semantics. Note: no single official page titled "Common gotchas"; this FAQ is the closest. | Free; licence not checked | verified |
| S-LNG-2 | PEP 8 and PEP 20 (Style Guide for Python Code; The Zen of Python) | PEP 8: van Rossum, Warsaw, Coghlan (2001). PEP 20: Tim Peters (2004) | Living docs | https://peps.python.org/pep-0008/ , https://peps.python.org/pep-0020/ | Naming/layout baseline and design philosophy as context; reviewer cites for style disputes only, not for bugs. | Free; licence not checked | verified |
| S-LNG-3 | Common Gotchas, The Hitchhiker's Guide to Python | Kenneth Reitz and contributors | Undated | https://docs.python-guide.org/writing/gotchas/ | Three gotchas: mutable default arguments, late-binding closures, stray .pyc files. Use on default args and lambdas in loops. | Free; licence not checked | verified |
| S-LNG-4 | Developing with asyncio | Python Software Foundation | Docs 3.x | https://docs.python.org/3/library/asyncio-dev.html | Debug mode, blocking calls in the loop, never-awaited coroutines, lost exceptions, async-generator cleanup. Use on any async def diff. | Free; licence not checked | verified |
| S-LNG-5 | Static Typing with Python (typing docs hub) | Python Typing Team | Living site | https://typing.python.org/en/latest/ | Official home of typing guides, reference and the type-system spec. Use to settle annotation questions. | Free; licence not checked | verified |
| S-LNG-6 | Effective Python: 125 Specific Ways to Write Better Python, 3rd ed. | Brett Slatkin, Addison-Wesley | Listed Nov 2024 (O'Reilly) / 2025 copyright (InformIT); Python 3.13; 672 pp | https://www.informit.com/store/effective-python-125-specific-ways-to-write-better-9780138172213 | Item-style advice on idioms, concurrency, robustness, performance. Reviewer uses for "is there a more Pythonic, safer form". | Paid | verified |

### JavaScript, TypeScript and React

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-LNG-7 | Strict mode (MDN) | MDN contributors | Living | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode | Silent errors that strict mode turns into throws (undeclared globals, `this` coercion). Note: MDN has no single "common pitfalls" page; this and JS-02 are the best fits. | Free; licence not checked | verified |
| S-LNG-8 | Using promises (MDN) | MDN contributors | Living | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises | Floating promises, missing `return` in `.then`, chaining and error propagation. | Free; licence not checked | verified |
| S-LNG-9 | TSConfig Reference: `strict` | Microsoft / TypeScript team | Living | https://www.typescriptlang.org/tsconfig/#strict | What the strict family turns on (noImplicitAny, strictNullChecks, etc.). Reviewer flags diffs that loosen it or add `any`. | Free; licence not checked | verified |
| S-LNG-10 | Effective TypeScript: 83 Specific Ways to Improve Your TypeScript, 2nd ed. | Dan Vanderkam, O'Reilly | April 2024 (O'Reilly) / paperback 10 May 2024; ISBN 9781098155063 | https://www.oreilly.com/library/view/effective-typescript-2nd/9781098155056/ | Type design, `any`/`unknown`, narrowing, type-level programming. Use for typing-quality review. | Paid | verified |
| S-LNG-11 | Node.js Security Best Practices | OpenJS Foundation / Node.js | Living | https://nodejs.org/en/learn/getting-started/security-best-practices | Request DoS, timing attacks, prototype pollution, supply chain, permission model. Use on Node server or dependency diffs. | Free; licence not checked | verified |
| S-LNG-12 | Don't Block the Event Loop (or the Worker Pool) | OpenJS Foundation / Node.js | Living | https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop | Sync APIs, ReDoS, big JSON, long CPU work on the loop. Use on hot request paths. | Free; licence not checked | verified |
| S-LNG-13 | You Might Not Need an Effect (React) | Meta / React team | Living | https://react.dev/learn/you-might-not-need-an-effect | Derived state in Effects, event logic placed in Effects, fetch race conditions and cleanup. | Free; licence not checked | verified |
| S-LNG-14 | Rendering Lists (React) | Meta / React team | Living | https://react.dev/learn/rendering-lists | Key rules: stable, unique, not index when list changes, not random. | Free; licence not checked | verified |

### C# and Unity

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-LNG-15 | .NET Coding Conventions (C#) | Microsoft (dotnet/docs team) | Page dated 2025-01-15, updated 2026-03 | https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions | Style plus language guidance (catch only what you can handle, `using`, StringBuilder in loops, async deadlock care). Page itself says it is not authoritative for library design. | Free; licence not checked | verified |
| S-LNG-16 | Framework Design Guidelines (online excerpt) and the book, 3rd ed. | Cwalina, Barton, Abrams. Addison-Wesley | Online excerpt is from the 2nd ed. (2008), flagged by Microsoft as possibly out of date; 3rd ed. June 2020, 625 pp | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/ ; book: https://www.pearson.com/en-us/subject-catalog/p/framework-design-guidelines-conventions-idioms-and-patterns-for-reusable-net-libraries/P200000000204/9780135896327 | Do/Consider/Avoid rules for public API design (naming, exceptions, extensibility). Use for public API and library diffs. | Excerpt free (licence not checked); book paid | verified |
| S-UNI-1 | Optimizing your code for managed memory (Unity Manual) | Unity Technologies | Living | http://docs.unity3d.com/Manual/performance-optimizing-code-managed-memory.html | Reference-type management, pooling and reuse, arrays; GC pressure. The old garbage-collection URL 301-redirects here. Page is a thin index of subtopics. | Free; licence not checked | verified |
| S-UNI-2 | Optimize your game performance for mobile, XR, and the web in Unity (Unity 6 edition) | Unity Technologies | Oct 2024 | https://unity.com/en/resources/mobile-xr-web-game-performance-optimization-unity-6 | Guide covering pooling, caching components, per-frame cost. Use for Update loops and allocation review. | Free e-book (sign-up form may apply); copyright Unity, licence not checked | unverified |
| S-UNI-3 | Serialization rules (Unity Manual) | Unity Technologies | Living (Unity 6.6 manual) | https://docs.unity3d.com/Manual/script-serialization-rules.html | Fields not properties, `[Serializable]`, no polymorphism without `[SerializeReference]`, unsupported nested collections, silent data loss. | Free; licence not checked | verified |
| S-UNI-4 | Object.operator == (Unity Scripting API) | Unity Technologies | Living | https://docs.unity3d.com/ScriptReference/Object-operator_eq.html | Unity's `== null` also checks the native object, so destroyed objects compare equal to null; `?.`, `??` and `is null` bypass this. (The bypass point is common knowledge; the fetched page only confirms the native-pointer check.) | Free; licence not checked | verified |
| S-UNI-5 | Unity Profiler and ObjectPool<T> | Unity Technologies | Living | https://docs.unity3d.com/Manual/Profiler.html ; https://docs.unity3d.com/ScriptReference/Pool.ObjectPool_1.html | Profiler landing page (measure before optimising); built-in stack-based pool, not thread-safe. Use when reviewing spawn/destroy churn. | Free; licence not checked | verified |

### Java and Kotlin

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-LNG-17 | Effective Java, 3rd ed. | Joshua Bloch, Addison-Wesley | 2018 (Java 9); ISBN 978-0134685991; 416 pp | https://www.informit.com/store/effective-java-9780134685991 | Item-based API, equals/hashCode, immutability, generics, lambdas/streams, concurrency. Use on any Java class design. | Paid | verified |
| S-LNG-18 | Java Concurrency in Practice | Brian Goetz with Peierls, Bloch, Bowbeer, Holmes, Lea. Addison-Wesley | 2006; ISBN 978-0321349606 | https://www.abebooks.com/Java-Concurrency-Practice-Goetz-Brian-Peierls/32130981886/bd (listing) | Thread safety, visibility, publication, deadlocks, executors. Use on shared mutable state. Predates modern Java features. | Paid | verified |
| S-LNG-19 | Kotlin Coding Conventions | JetBrains | Living | https://kotlinlang.org/docs/coding-conventions.html | Naming, `val`, read-only collections, expression forms, platform types, library API explicitness. | Free; licence not checked | verified |
| S-LNG-20 | Kotlin Coroutines guide | JetBrains | Living | https://kotlinlang.org/docs/coroutines-guide.html | Cancellation, structured concurrency, dispatchers, exception handling, shared mutable state. Landing page lists topics. | Free; licence not checked | verified |

### Go

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-LNG-21 | Effective Go | Go team | Written for 2009 release; page says it is no longer updated and omits generics and modules | https://go.dev/doc/effective_go | Idioms: defer, error returns, zero values, embedding, goroutines. Use with care on modern code. | Free; licence not checked | verified |
| S-LNG-22 | Go Code Review Comments | Go team (Go wiki) | Living | https://go.dev/wiki/CodeReviewComments | Reviewer-oriented checklist: contexts, goroutine lifetimes, handle errors, don't panic, pass values, receiver type, interfaces. Best single Go source for a reviewer. | Free; licence not checked | verified |
| S-LNG-23 | 100 Go Mistakes and How to Avoid Them, with free site | Teiva Harsanyi, Manning | 2022; ISBN 9781617299599 | https://100go.co/ ; book: https://www.oreilly.com/library/view/100-go-mistakes/9781617299599/ | Catalogue of bugs and inefficiencies: slices, concurrency, errors, testing, optimisation. Site gives free summaries, first chapter and 8 full sections. | Book paid; site free summaries, licence not checked | verified |

### SQL, databases and migrations

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-DBS-1 | SQL Antipatterns: Avoiding the Pitfalls of Database Programming | Bill Karwin, Pragmatic Bookshelf | 1st ed. 2010 (ISBN 978-1934356555); a later "Volume 1" edition (ISBN 9781680508987) adds mini-antipatterns | https://bookshare.org/browse/book/1964529 (listing) | Schema and query antipatterns (e.g. EAV, comma-separated lists, naive trees). Use on schema and query diffs. | Paid | verified |
| S-DBS-2 | Use The Index, Luke | Markus Winand | Copyright 2010-2026 | https://use-the-index-luke.com/ | Index design, execution plans, query tuning. Free web edition of the book SQL Performance Explained (sold separately). | Free to read; all rights reserved | verified |
| S-DBS-3 | PostgreSQL: Transaction Isolation (ch. 13.2) | PostgreSQL Global Development Group | Docs v18 | https://www.postgresql.org/docs/current/transaction-iso.html | Read Committed vs Repeatable Read vs Serializable, retry on serialization failure. Use on multi-statement transactions and read-then-write logic. | Free; licence not checked | verified |
| S-DBS-4 | PostgreSQL: Explicit Locking, incl. Deadlocks (13.3.4) | PostgreSQL Global Development Group | Docs v18 | https://www.postgresql.org/docs/current/explicit-locking.html | Consistent lock order, short transactions, retry on deadlock. | Free; licence not checked | verified |
| S-DBS-5 | strong_migrations | Andrew Kane (ankane) | Repo, living (author name from general knowledge; not shown in fetch) | https://github.com/ankane/strong_migrations | Catalogue of unsafe migrations (non-concurrent index, column removal/rename, NOT NULL, backfills). Use on any migration diff in any stack. | Free; MIT | unverified |
| S-DBS-6 | Migration Style Guide | GitLab | Living | https://docs.gitlab.com/development/migration_style_guide/ | Downtime avoidance, reversibility, large tables, lock retries, index handling. | Free; licence not checked | verified |
| S-DBS-7 | Database access optimization (Django) | Django Software Foundation | Living | https://docs.djangoproject.com/en/stable/topics/db/optimization/ | The N+1 pattern (queries in a loop) and fixes with `select_related`/`prefetch_related`; profile first. Page does not use the term "N+1". | Free; licence not checked | verified |

### Performance review

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-PRF-1 | Systems Performance, 2nd ed. | Brendan Gregg, Addison-Wesley | Dec 2020 / 2021 copyright; 928 pp; ISBN 978-0136820154 | https://www.pearson.com/store/en-us/p/systems-performance/P200000000297/9780136820154 | Method-first performance analysis, profiling and tracing. Use for deep dives, not routine diffs. | Paid | verified |
| S-PRF-2 | The USE Method | Brendan Gregg | Undated | https://www.brendangregg.com/usemethod.html | For each resource check utilization, saturation, errors. Quick bottleneck checklist. | Free; licence not checked | verified |
| S-PRF-3 | Latency Numbers Every Programmer Should Know (gist) | Maintained by Jonas Bonér; numbers credited to Jeff Dean and Peter Norvig | Table labelled ~2012, with later community additions | https://gist.github.com/jboner/2841832 | Order-of-magnitude costs (cache, memory, disk, network) for back-of-envelope checks. Comments dispute some figures, e.g. SSD speed; treat as rough. | Free; licence not checked | verified |
| S-PRF-4 | Performance Hints | Jeff Dean and Sanjay Ghemawat (Google) | Undated | https://abseil.io/fast/hints.html | Estimate cost, measure with profilers, cut allocations and needless work. Mostly C++ examples. | Free; licence not checked | verified |
| S-PRF-5 | Web Vitals (Core Web Vitals) | Google (web.dev) | Living | https://web.dev/articles/vitals | LCP at 2.5 s or less, INP at 200 ms or less, CLS at 0.1 or less, at the 75th percentile. Use on front-end diffs touching loading, input handlers or layout. | Free; licence not checked | verified |
| S-PRF-6 | Analyze runtime performance (Chrome DevTools) | Google Chrome team | Living | https://developer.chrome.com/docs/devtools/performance | Flame chart reading, long tasks, forced synchronous layout, compositor-only animation. | Free; licence not checked | verified |

### API design and contract review

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-API-1 | API Improvement Proposals (AIP), General AIPs | Google | Living | https://google.aip.dev/general | Resource design, standard methods, pagination, filtering, versioning. Use on API surface changes. | Free; CC BY 4.0, code samples Apache 2.0 | verified |
| S-API-2 | Microsoft REST API Guidelines (repo, incl. Azure and Graph variants) | Microsoft | Living; Azure vNext doc fetched | https://github.com/microsoft/api-guidelines | Status codes, errors, date-based `api-version`, no breaking change within a version, paging, idempotent retries. | Free; CC BY 4.0 | verified |
| S-API-3 | Semantic Versioning 2.0.0 | Tom Preston-Werner | 2.0.0 | https://semver.org/ | Meaning of major/minor/patch; use to judge whether a change is breaking. | Free; CC BY 3.0 | verified |
| S-API-4 | RFC 9413: Maintaining Robust Protocols | Martin Thomson and David Schinazi (IAB) | June 2023, Informational | https://www.rfc-editor.org/rfc/rfc9413.html | Modern critique of Postel's law: silently accepting bad input erodes interoperability. Use when a diff adds lenient parsing. Earlier Thomson draft "The Harmful Consequences of the Robustness Principle" was NOT checked (UNVERIFIED). | Free; IETF Trust terms, not checked | verified |

### Error handling and logging

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-LOG-1 | The Twelve-Factor App, XI. Logs | Adam Wiggins | Updated 2017 | https://12factor.net/logs | Treat logs as an event stream to stdout; the environment routes them. Use on log-to-file or custom log-shipping code. | Free; licence not shown | verified |
| S-LOG-2 | Logging Cheat Sheet (OWASP) | OWASP Cheat Sheet Series team | Living | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | What to log, what to exclude, log injection, protection of logs. | Free; CC BY-SA 4.0 | verified |
| S-LOG-3 | Error Handling Cheat Sheet (OWASP) | OWASP Cheat Sheet Series team | Living | https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html | Generic client messages, full detail in server logs, RFC 9457 problem details, 4xx vs 5xx. | Free; licence not checked | verified |
| S-LOG-4 | OpenTelemetry Logs Data Model | OpenTelemetry project | Living spec | https://opentelemetry.io/docs/specs/otel/logs/data-model/ | Structured log record: severity, attributes, trace context, structured body. Use when reviewing log schema. | Free; licence not checked | verified |

### Accessibility

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-ACC-1 | How to Meet WCAG (Quick Reference) | W3C WAI | Shows WCAG 2.2 (2.1 and 2.0 views offered) | https://www.w3.org/WAI/WCAG22/quickref/ | Filterable success criteria and techniques. Use on UI diffs: labels, contrast, keyboard, focus, names/roles. | Free; licence not checked | verified |
| S-ACC-2 | Understanding the Web Content Accessibility Guidelines (WCAG) (MDN) | MDN contributors | Living | https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Understanding_WCAG | Plain-language WCAG companion. Only the title was confirmed. | Free; licence not checked | verified |
