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

Part C (Python, JavaScript and TypeScript, C# and Unity, Java and Kotlin, Go, SQL and migrations, performance, API contracts, accessibility) is added from its research pass.
