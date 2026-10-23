# Sources for the Architect

Where the Architect's knowledge comes from. Researched and checked on 2026-10-22 (four passes: foundations; web, backend, security, AI and data; games, mobile, desktop and real-time; recovering existing architecture and diagram tools).

How to use these sources
- Ideas only, in our own words. Never copy passages. Cite a source by its ID, for example `[S-FND-1]`.
- Cite a source as fact only when its Status is `verified`. A row marked `unverified` is a lead: say "unverified" in the same line when you mention it.
- `verified` means its existence, author, title, year and URL were confirmed against the publisher, the author's site or consistent search records. `unverified` means one of those was not confirmed (or only a bookseller or secondary page was found). An unconfirmed licence alone does not change the status; it is written as "licence unverified".
- Publisher pages for O'Reilly returned HTTP 403 to the checker, so books from O'Reilly were confirmed through search listings and author or publisher records.
- Free does not mean copyable: summarise, never paste. Licences are noted where a page states one.

## Foundations, methods and frameworks

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-FND-1 | Fundamentals of Software Architecture, 2nd ed. | Mark Richards, Neal Ford | 2025 | https://www.oreilly.com/library/view/-/9781098175504 | Whole-field baseline: architecture characteristics, styles, governance, data, diagramming. Default reference. | Paid | verified |
| S-FND-2 | Software Architecture: The Hard Parts | Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani | 2021 | https://www.oreilly.com/library/view/software-architecture-the/9781492086888/ | Trade-off analysis for distributed systems: granularity, splitting data, sagas, contracts. | Paid | verified |
| S-FND-3 | Software Architecture in Practice, 4th ed. | Len Bass, Paul Clements, Rick Kazman | 2021 | https://www.informit.com/store/software-architecture-in-practice-9780136886099 | Quality attributes, tactics, documentation and evaluation. | Paid | verified |
| S-FND-4 | Building Evolutionary Architectures, 2nd ed. | Neal Ford, Rebecca Parsons, Patrick Kua, Pramod Sadalage | 2022 | https://oreilly.com/library/view/building-evolutionary-architectures/9781492097532 | Fitness functions and automated governance of architecture over time. | Paid | verified |
| S-FND-5 | A Philosophy of Software Design, 2nd ed. | John Ousterhout | 2021 | https://web.stanford.edu/~ouster/cgi-bin/book.php | Managing complexity: deep modules, information hiding, red flags. | Paid | verified |
| S-FND-6 | Domain-Driven Design: Tackling Complexity in the Heart of Software | Eric Evans | 2003 | https://www.informit.com/store/domain-driven-design-tackling-complexity-in-the-heart-9780321125217 | Ubiquitous language, bounded contexts, aggregates. | Paid | verified |
| S-FND-7 | Domain-Driven Design Reference: Definitions and Pattern Summaries | Eric Evans | 2015 | https://domainlanguage.com/ddd/reference/ | Free short glossary of every DDD pattern. | Free, CC BY 4.0 (summarise with attribution) | verified |
| S-FND-8 | Implementing Domain-Driven Design | Vaughn Vernon | 2013 | https://www.pearson.com/store/en-us/p/implementing-domain-driven-design/P200000009616/9780321834577 | Strategic to tactical DDD with context maps and worked examples. | Paid | verified |
| S-FND-9 | Clean Architecture: A Craftsman's Guide to Software Structure and Design | Robert C. Martin | 2017 | https://www.informit.com/store/clean-architecture-a-craftsmans-guide-to-software-structure-9780134494166 | Dependency rule, boundaries, SOLID at component scale. Opinionated; weigh against S-FND-5. | Paid | verified |
| S-FND-10 | Evaluating Software Architectures: Methods and Case Studies | Paul Clements, Rick Kazman, Mark Klein | 2001 | https://openlibrary.org/books/OL25444980M | ATAM, SAAM and ARID in practice. Title, authors and 2001 confirmed on Open Library. | Paid | verified |
| S-FND-11 | The C4 model | Simon Brown | ongoing | https://c4model.com/ | Four zoom levels (context, container, component, code), notation independent. | Free, CC BY 4.0 | verified |
| S-FND-12 | arc42 architecture documentation template | Peter Hruschka, Gernot Starke | ongoing | https://arc42.org/overview | Twelve-section skeleton for documenting an architecture. | Free, CC BY-SA 4.0 (summarise, do not copy text) | verified |
| S-FND-13 | Documenting Architecture Decisions | Michael Nygard | 2011 | https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions | The original ADR post: context, decision, consequences. | Free, CC0 1.0 | verified |
| S-FND-14 | MADR: Markdown Architectural Decision Records, v4.0.0 | ADR GitHub community | 2024 | https://adr.github.io/madr/ | Structured ADR template with options and pros and cons. | Free, MIT or CC0 | verified |
| S-FND-15 | ATAM: Method for Architecture Evaluation (CMU/SEI-2000-TR-004) | Rick Kazman, Mark Klein, Paul Clements | 2000 | https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation | Scenario-based evaluation: utility tree, sensitivity and trade-off points, risks. | Free to read; permission form linked, summarise only | verified |
| S-FND-16 | Architectural Blueprints, the 4+1 View Model of Software Architecture | Philippe Kruchten | 1995 | https://doi.org/10.1145/216591.216611 | Logical, development, process and physical views plus scenarios. Title, author and 1995 confirmed via the DOI record (Crossref). | IEEE paywalled; copy licence unverified | verified |
| S-FND-17 | ISO/IEC/IEEE 42010:2022, Software, systems and enterprise architecture description | ISO/IEC/IEEE | 2022 | https://www.iso.org/standard/74393.html | Stakeholders, concerns, viewpoints and views for architecture descriptions. | Paid, copyrighted | verified |
| S-FND-18 | Risk-storming | Simon Brown | 2016 (in Software Architecture for Developers) | https://riskstorming.com/ | A short workshop to find and rate architecture risks. Technique steps read on the site. | Free site; licence unverified | verified |
| S-FND-19 | AWS Well-Architected Framework | AWS | 2024 | https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html | Six pillars and review questions; a review is a conversation, not an audit. | Free; licence unverified, summarise only | verified |
| S-FND-20 | Azure Well-Architected Framework | Microsoft | 2026 | https://learn.microsoft.com/en-us/azure/well-architected/ | Five pillars, workload and service guides. | Free; licence unverified | verified |
| S-FND-21 | Google Cloud Well-Architected Framework | Google Cloud | current | https://docs.cloud.google.com/architecture/framework | Six pillars plus AI/ML perspective. | Free, CC BY 4.0 (code samples Apache 2.0) | verified |
| S-FND-22 | Unified Modeling Language (UML) 2.5.1 | Object Management Group | 2017 | https://www.omg.org/spec/UML/2.5.1/About-UML | Standard notation for class, sequence, component, deployment diagrams. | Free download; terms unverified | verified |
| S-FND-23 | ArchiMate (Open Group enterprise architecture modelling language) | The Open Group | unknown | https://pubs.opengroup.org/architecture/archimate3-doc/ | Enterprise-level layered modelling. Page redirected to a login; not opened. | Unverified | unverified |

## Web, backend, distributed systems, reliability and security

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-WEB-1 | Designing Data-Intensive Applications, 2nd ed. | Martin Kleppmann, Chris Riccomini | 2026 | https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html | Replication, partitioning, transactions, consistency, batch and stream processing. | Paid | verified |
| S-WEB-2 | Site Reliability Engineering | Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (eds.) | 2017 | https://sre.google/sre-book/table-of-contents/ | SLOs, error budgets, monitoring, overload, incident handling. | Free online, CC BY-NC-ND 4.0 | verified |
| S-WEB-3 | The Site Reliability Workbook | Betsy Beyer, Niall Richard Murphy, David K. Rensin, Kent Kawahara, Stephen Thorne (eds.) | 2018 | https://sre.google/workbook/table-of-contents/ | Practical SLOs, alerting on SLOs, canarying. | Free online, CC BY-NC-ND 4.0 | verified |
| S-WEB-4 | Building Secure and Reliable Systems | Heather Adkins, Betsy Beyer, Paul Blankinship, Ana Oprea, Piotr Lewandowski, Adam Stubblefield | 2020 | https://google.github.io/building-secure-and-reliable-systems/raw/toc.html | Designing for security and reliability together. Launch date 2020-04-08 per the book repository; licence not confirmed. | Free to read online; licence unverified | verified |
| S-WEB-5 | Release It!, 2nd ed. | Michael Nygard | 2018 | https://pragprog.com/titles/mnee2/release-it-second-edition/ | Stability patterns: timeouts, circuit breaker, bulkhead. | Paid | verified |
| S-WEB-6 | Building Microservices, 2nd ed. | Sam Newman | 2021 | https://www.oreilly.com/library/view/building-microservices/9781492034018 | Modelling, integrating, testing and deploying services. | Paid | verified |
| S-WEB-7 | Monolith to Microservices | Sam Newman | 2019 | https://tenlong.com.tw/products/9781492047841 | Incremental migration patterns: strangler fig, branch by abstraction, database decomposition. | Paid | verified |
| S-WEB-8 | Database Internals | Alex Petrov | 2019 | https://www.oreilly.com/library/view/-/9781492040330/ | Storage engines, replication, consensus. | Paid | verified |
| S-WEB-9 | Microservices (a definition of this new architectural term) | James Lewis, Martin Fowler | 2014 | https://martinfowler.com/articles/microservices.html | Canonical definition and characteristics of microservices. | Free to read, copyright; summarise only | verified |
| S-WEB-10 | Monolith First | Martin Fowler | 2015 | https://martinfowler.com/bliki/MonolithFirst.html | Why to start with a monolith and extract services later. | Free to read, copyright | verified |
| S-WEB-11 | Microservices patterns catalog (microservices.io) | Chris Richardson | 2026 | https://microservices.io/patterns/index.html | Pattern language for services, data management, deployment. | Free to read, all rights reserved | verified |
| S-WEB-12 | The Twelve-Factor App | Adam Wiggins | 2017 | https://12factor.net/ | Baseline for cloud-native services: config, stateless processes, logs. | Free; licence unverified | verified |
| S-WEB-13 | Architectural Styles and the Design of Network-based Software Architectures | Roy T. Fielding | 2000 | https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm | Origin and constraints of REST. Direct fetch failed a certificate check; confirmed through search. | Free | verified |
| S-WEB-14 | API Improvement Proposals (AIP) | Google | ongoing | https://google.aip.dev/ | Resource-oriented API design rules: naming, pagination, errors. | Free, CC BY 4.0 (code Apache 2.0) | verified |
| S-WEB-15 | Microsoft REST API Guidelines | Microsoft | ongoing | https://github.com/microsoft/api-guidelines | Practical REST conventions: versioning, errors, filtering. | Free, CC BY 4.0 | verified |
| S-WEB-16 | Azure Architecture Center | Microsoft | 2026 | https://learn.microsoft.com/en-us/azure/architecture/ | Architecture styles, cloud design patterns, reference architectures. | Free; licence unverified | verified |
| S-WEB-17 | High Scalability | various | newest post 2024 | https://highscalability.com/ | Case studies of large systems; thinner than books and seems inactive. | Free | verified |
| S-WEB-18 | OWASP Application Security Verification Standard (ASVS) | OWASP | 5.0.0 | https://owasp.org/www-project-application-security-verification-standard/ | Verifiable security requirements by level. | Free, CC BY-SA 4.0 | verified |
| S-WEB-19 | OWASP Threat Modeling Cheat Sheet | OWASP | current | https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html | Four phases: model, find threats (STRIDE), mitigate, validate. | Free, CC BY-SA 4.0 | verified |
| S-WEB-20 | Threat Modeling Manifesto | Adam Shostack, Zoe Braiterman and others | undated | https://www.threatmodelingmanifesto.org/ | The four questions of threat modelling. | Free; licence unverified | verified |
| S-WEB-21 | NIST SP 800-218, Secure Software Development Framework (SSDF) v1.1 | Murugiah Souppaya, Karen Scarfone, Donna Dodson | 2022 | https://csrc.nist.gov/pubs/sp/800/218/final | Secure development practices, used in procurement. | Free (US government) | verified |
| S-WEB-22 | NIST SP 800-207, Zero Trust Architecture | Scott Rose, Oliver Borchert, Stu Mitchell, Sean Connelly | 2020 | https://csrc.nist.gov/pubs/sp/800/207/final | Zero-trust model and deployment approaches. | Free (US government) | verified |

## AI, LLM and agent systems

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-AI-1 | Building effective agents | Erik S., Barry Zhang (Anthropic) | 2024 | https://www.anthropic.com/engineering/building-effective-agents | Five workflow patterns; when an autonomous agent is justified. | Free, copyright | verified |
| S-AI-2 | How we built our multi-agent research system | Anthropic | 2025 | https://www.anthropic.com/engineering/multi-agent-research-system | Lead agent plus parallel subagents: good for breadth, costs many more tokens. | Free, copyright | verified |
| S-AI-3 | Effective context engineering for AI agents | Anthropic | 2025 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Context is limited: compaction, notes, subagents, just-in-time retrieval. | Free, copyright | verified |
| S-AI-4 | Writing effective tools for agents | Anthropic | 2025 | https://www.anthropic.com/engineering/writing-tools-for-agents | Design tools for agents, evaluate on realistic tasks. | Free, copyright | verified |
| S-AI-5 | Introducing Contextual Retrieval | Anthropic | 2024 | https://anthropic.com/news/contextual-retrieval | RAG chunk-context technique with reranking. Anthropic reports 49% fewer failed retrievals, 67% with reranking (their figures). | Free, copyright | verified |
| S-AI-6 | AI Engineering: Building Applications with Foundation Models | Chip Huyen | 2025 | https://www.oreilly.com/library/view/ai-engineering/9781098166298/ | Evaluation, prompting, RAG, agents, latency and cost. | Paid | verified |
| S-AI-7 | Agents | Chip Huyen | 2025 | https://huyenchip.com/2025/01/07/agents.html | Tools, planning, reflection, failure modes; errors compound across steps. | Free, copyright | verified |
| S-AI-8 | Your AI Product Needs Evals | Hamel Husain | 2024 | https://hamel.dev/blog/posts/evals/ | Three levels of evals; calibrate LLM judges against humans. | Free, copyright | verified |
| S-AI-9 | OWASP Top 10 for LLM Applications | OWASP | 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Prompt injection, insecure output handling, excessive agency. | Free; licence unverified | verified |
| S-AI-10 | NIST AI 600-1, Generative AI Profile | NIST | 2024 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf | Twelve generative-AI risks mapped to govern, map, measure, manage. Confirmed through search; PDF not opened. | Free (US government) | verified |

## Data and analytics pipelines

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-DATA-1 | Data Mesh Principles and Logical Architecture | Zhamak Dehghani | 2020 | https://martinfowler.com/articles/data-mesh-principles.html | Domain ownership, data as a product, self-serve platform. | Free, copyright | verified |
| S-DATA-2 | Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics | Michael Armbrust, Ali Ghodsi, Reynold Xin, Matei Zaharia | 2020 | https://www.databricks.com/research/lakehouse-a-new-generation-of-open-platforms-that-unify-data-warehousing-and-advanced-analytics | One open storage layer for warehouse and ML. Published at CIDR 2021. | Free | verified |
| S-DATA-3 | Fundamentals of Data Engineering | Joe Reis, Matt Housley | 2022 | https://www.oreilly.com/library/view/-/9781098108298 | Data engineering lifecycle: ingestion, orchestration, transformation, storage. | Paid | verified |
| S-DATA-4 | Streaming Systems | Tyler Akidau, Slava Chernyak, Reuven Lax | 2018 | https://oreilly.com/library/view/streaming-systems/9781491983867 | Windowing, watermarks, exactly-once, streams versus tables. | Paid | verified |

## Games, game engines and netcode

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-GAME-1 | Game Programming Patterns | Robert Nystrom | 2014 | https://gameprogrammingpatterns.com/ | Game loop, component, state, observer, object pool, data locality. | Free online; all rights reserved | verified |
| S-GAME-2 | Game Engine Architecture, 3rd ed. | Jason Gregory | 2018 | https://www.gameenginebook.com/ | Whole-engine layering. Book confirmed through listings; its site blocked the checker. | Paid | verified |
| S-GAME-3 | Data-Oriented Design | Richard Fabian | 2018 | https://www.dataorienteddesign.com/dodbook/ | Table-based, data-first design as an alternative to objects. | Free online | verified |
| S-GAME-4 | Data-Oriented Design and C++ (CppCon 2014 keynote) | Mike Acton | 2014 | https://isocpp.org/blog/2015/01/cppcon-2014-data-oriented-design-and-c-mike-acton | Why data-oriented design beats over-abstraction. | Free video | verified |
| S-GAME-5 | Unity Entities (ECS / DOTS) manual, v1.3 | Unity Technologies | current | https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/index.html | Unity's ECS model for many entities. Page fetched and title confirmed. | Free; Unity docs terms | verified |
| S-GAME-6 | Level up your code with design patterns and SOLID (Unity 6 e-book) | Unity | current | https://unity.com/resources/design-patterns-solid-ebook | Factory, pooling, observer and SOLID applied to Unity code. | Free (form-gated) | verified |
| S-GAME-7 | Create modular game architecture in Unity with ScriptableObjects | Unity | current | https://unity.com/resources/create-modular-game-architecture-with-scriptable-objects-ebook | Data and logic separation with ScriptableObjects. Price unconfirmed. | Form-gated; cost unverified | verified |
| S-GAME-8 | Unity Addressables manual, v2.3 | Unity Technologies | current | https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/index.html | Asset loading, groups, remote content, memory lifetime. Page fetched and title confirmed. | Free; Unity docs terms | verified |
| S-GAME-9 | Unreal Engine Gameplay Framework documentation | Epic Games | current | https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine | Game mode, game state, player controller, pawn. Page fetched and title confirmed. | Free; Epic docs terms | verified |
| S-GAME-10 | Unreal Engine Networking Overview | Epic Games | current | https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine | Server-authoritative replication, RPCs, relevancy. Page fetched and title confirmed. | Free; Epic docs terms | verified |
| S-GAME-11 | Godot Best practices | Godot community | current | https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html | Scene and node composition, signals, autoloads. Page fetched and title confirmed. | Free; licence unverified | verified |
| S-GAME-12 | Fix Your Timestep! | Glenn Fiedler | 2004 | https://gafferongames.com/post/fix_your_timestep/ | Fixed physics step with interpolated rendering. Page fetched and title confirmed. | Free; copyright | verified |
| S-GAME-13 | What Every Programmer Needs To Know About Game Networking | Glenn Fiedler | 2010 | https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/ | History and trade-offs of lockstep, snapshots and state sync. | Free | verified |
| S-GAME-14 | Client-Server Game Architecture (Fast-Paced Multiplayer) | Gabriel Gambetta | undated | https://www.gabrielgambetta.com/client-server-game-architecture.html | Authoritative server, prediction, reconciliation, interpolation. | Free | verified |
| S-GAME-15 | Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization | Yahn W. Bernier (Valve), GDC 2001 | 2001 | https://developer.valvesoftware.com/wiki/Latency_Compensating_Methods_in_Client/Server_In-game_Protocol_Design_and_Optimization | Prediction, interpolation and lag compensation in Source. Confirmed through search. | Free | verified |
| S-GAME-16 | Overwatch Gameplay Architecture and Netcode (GDC 2017) | Timothy Ford (Blizzard) | 2017 | https://gdcvault.com/play/1024001 | ECS plus deterministic simulation for netcode. Existence and speaker confirmed; talk content not accessed. | GDC Vault, members only | verified |
| S-GAME-17 | It IS Rocket Science! The Physics of Rocket League Detailed (GDC 2018) | Jared Cone (Psyonix) | 2018 | https://www.gamedeveloper.com/design/video-the-rocket-science-behind-i-rocket-league-s-i-physics | Networked physics with a fixed tick and prediction. Existence confirmed; technical details only secondhand. | Free video | verified |

## Mobile

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-MOB-1 | Guide to app architecture | Android Developers (Google) | current | https://developer.android.com/topic/architecture | UI, data and optional domain layers, unidirectional data flow. | Free; Google docs terms | verified |
| S-MOB-2 | Build an offline-first app | Android Developers (Google) | current | https://developer.android.com/topic/architecture/data-layer/offline-first | Local database as source of truth, sync strategies. | Free; Google docs terms | verified |
| S-MOB-3 | Managing model data in your app (SwiftUI) | Apple | current | https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app | State, observation and data ownership in SwiftUI. Page fetched and title confirmed. | Free; Apple docs terms | verified |
| S-MOB-4 | Architecting Flutter apps | Flutter team | current | https://docs.flutter.dev/app-architecture | UI and data layers, MVVM, repositories, services. | Free; licence unverified | verified |
| S-MOB-5 | React Native Architecture overview (New Architecture) | Meta / React Native | current | https://reactnative.dev/architecture/landing-page | JSI, Fabric, TurboModules. Page fetched and title confirmed. | Free; licence unverified | verified |
| S-MOB-6 | .NET MAUI MVVM architecture guidance | Microsoft Learn | current | https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm | MVVM with data binding for cross-platform .NET. Page fetched and title confirmed. | Free; Microsoft terms | verified |
| S-MOB-7 | App Store Review Guidelines | Apple | current | https://developer.apple.com/app-store/review/guidelines/ | Rules on payments, content, privacy that constrain design. Page fetched and title confirmed. | Free; Apple terms | verified |
| S-MOB-8 | Google Play Developer Program Policies | Google | current | https://developer.android.com/distribute/play-policies | Android store rules. Page fetched and title confirmed. | Free; Google terms | verified |
| S-MOB-9 | Android vitals | Google | current | https://developer.android.com/topic/performance/vitals | ANR, crash, startup and battery thresholds that affect ranking. Page fetched and title confirmed. | Free | verified |
| S-MOB-10 | Improving your app's performance (Xcode) | Apple | current | https://developer.apple.com/documentation/xcode/improving-your-app-s-performance | Launch time, hangs, memory, energy on iOS. Page fetched and title confirmed. | Free; Apple terms | verified |
| S-MOB-11 | Local-first software: you own your data, in spite of the cloud | Martin Kleppmann, Adam Wiggins, Peter van Hardenberg, Mark McGranaghan | 2019 | https://www.inkandswitch.com/essay/local-first/ | Seven ideals for offline-capable apps with sync (CRDTs). Page fetched and title confirmed. | Free; licence unverified | verified |

## Desktop, plugins and editors

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-DESK-1 | Electron Process Model | Electron | current | https://www.electronjs.org/docs/latest/tutorial/process-model | Main versus renderer process, preload, context isolation. Page fetched and title confirmed. | Free; licence unverified | verified |
| S-DESK-2 | Tauri Architecture | Tauri | current | https://tauri.app/concept/architecture/ | Rust core plus system webview, IPC and permissions. Page fetched and title confirmed. | Free; licence unverified | verified |
| S-DESK-3 | VS Code Extension Host | Microsoft | current | https://code.visualstudio.com/api/advanced-topics/extension-host | Out-of-process extensions, isolation, activation. Page fetched and title confirmed. | Free; Microsoft terms | verified |
| S-DESK-4 | Windows desktop app development | Microsoft Learn | current | https://learn.microsoft.com/en-us/windows/apps/desktop/ | Choosing between WinUI, WPF, WinForms and packaging. Page fetched and title confirmed. | Free; Microsoft terms | verified |
| S-DESK-5 | GUI Architectures | Martin Fowler | undated | https://www.martinfowler.com/eaaDev/uiArchs.html | MVC, MVP, Presentation Model, Passive View. Page fetched and title confirmed. | Free; copyright | verified |

## Real-time, state machines and messaging

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-RT-1 | The LMAX Architecture | Martin Fowler | 2011 | https://martinfowler.com/articles/lmax.html | Single-threaded event-sourced core with a ring buffer for low latency. | Free | verified |
| S-RT-2 | Statecharts | statecharts.dev community (after David Harel, 1987) | ongoing | https://statecharts.dev/ | Hierarchical state machines, parallel states, history. | Free | verified |
| S-RT-3 | Enterprise Integration Patterns | Gregor Hohpe, Bobby Woolf | 2003 | https://www.enterpriseintegrationpatterns.com/ | Messaging vocabulary: channels, routers, idempotent receiver. Page fetched and title confirmed. | Catalogue free; book paid | verified |
| S-RT-4 | The Reactive Manifesto | Reactive Manifesto authors | undated | https://www.reactivemanifesto.org/ | Responsive, resilient, elastic, message-driven principles. Page fetched and title confirmed. | Free | verified |

## Recovering and reviewing existing architecture

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-REC-1 | Your Code as a Crime Scene, 2nd ed. | Adam Tornhill | 2024 | https://www.oreilly.com/library/view/your-code-as/9798888650837/ | Hotspots (change frequency times complexity), change coupling, knowledge maps from git history. | Paid | verified |
| S-REC-2 | Software Design X-Rays: Fix Technical Debt with Behavioral Code Analysis | Adam Tornhill | 2018 | https://openlibrary.org/books/OL26833447M | Prioritise tech debt from version-control data. Title, author and 2018 confirmed on Open Library. | Paid | verified |
| S-REC-3 | code-maat | Adam Tornhill | 2013 onward | https://github.com/adamtornhill/code-maat | CLI that mines git logs for coupling, revisions, ownership. | Free, GPL-3.0 | verified |
| S-REC-4 | Working Effectively with Legacy Code | Michael Feathers | 2004 | https://openlibrary.org/books/OL26223631M | Seams, characterization tests, breaking dependencies. Title, author and 2004 confirmed on Open Library. | Paid | verified |
| S-REC-5 | Software Systems Architecture, 2nd ed. | Nick Rozanski, Eoin Woods | 2011 | https://www.oreilly.com/library/view/software-systems-architecture/9780132906135 | Seven viewpoints as a checklist for a recovered architecture description. | Paid | verified |
| S-REC-6 | Software Architecture Reconstruction: A Process-Oriented Taxonomy | Stephane Ducasse, Damien Pollet | 2009 | https://hal.archives-ouvertes.fr/hal-00849009 | Survey of recovery approaches: top-down, bottom-up, hybrid. | Free HAL preprint | verified |
| S-REC-7 | Software Reflexion Models: Bridging the Gap Between Source and High-Level Models | Gail Murphy, David Notkin, Kevin Sullivan | 1995 | https://www.cs.ubc.ca/~murphy/papers/rm/fse95.html | Hypothesise a model, map it to source, compute agreement and divergence. FSE 1995 paper; the later journal version (2001) was not checked. | Free (author site, FSE 1995 version) | verified |
| S-REC-8 | A comparative analysis of software architecture recovery techniques | Joshua Garcia, Igor Ivkovic, Nenad Medvidovic | 2013 | https://doi.org/10.1109/ase.2013.6693106 | Compares architecture recovery techniques (ASE 2013). Treat automatic clustering as a hint (our caution; paper findings not read). Authors, title and year confirmed via the DOI record. Free copy not located. | Paper; free copy not located | verified |
| S-REC-9 | Controlling software architecture erosion: A survey | Lakshitha de Silva, Dharini Balasubramaniam | 2012 | https://research-portal.st-andrews.ac.uk/en/publications/controlling-software-architecture-erosion-a-survey/ | Erosion strategies: minimise, prevent, repair. | Abstract free; full text may be paywalled | verified |
| S-REC-10 | Understanding Software Architecture Erosion: A Systematic Mapping Study | Ruiyin Li, Peng Liang, Mohamed Soliman, Paris Avgeriou | 2021 | https://arxiv.org/abs/2112.10934 | Causes, symptoms and detection of erosion. Authors and date read from the arXiv page. | Free | verified |
| S-REC-11 | Using Dependency Models to Manage Complex Software Architecture | Neeraj Sangal, Ev Jordan, Vineet Sinha, Daniel Jackson | 2005 | https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf | Dependency Structure Matrix analysis and design rules. | Free PDF | verified |
| S-REC-12 | Strangler Fig Application | Martin Fowler | 2024 | https://martinfowler.com/bliki/StranglerFigApplication.html | Replace a legacy system gradually behind one entry point. | Free, copyright | verified |
| S-REC-13 | Strangler Fig pattern (Azure Architecture Center) | Microsoft | current | https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig | Facade or proxy routing between old and new; lists when not to use it. | Free; licence unverified | verified |
| S-REC-14 | Architecture Decision Record | Martin Fowler | current | https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html | ADRs are superseded, never rewritten. | Free, copyright | verified |
| S-REC-15 | Code Reading: The Open Source Perspective | Diomidis Spinellis | 2003 | https://www.spinellis.gr/codereading/ | Techniques for reading large unfamiliar code. May be out of print. | Paid | verified |
| S-REC-16 | git log documentation (log -S, --follow) | Git project | current | https://git-scm.com/docs/git-log | Dating when a boundary, library or table appeared, and why. Page fetched; blame is a separate command. | Free | verified |
| S-REC-17 | ArchUnit | TNG | current | https://github.com/TNG/ArchUnit | Java layer, slice and cycle rules written as unit tests. | Free, Apache-2.0 | verified |
| S-REC-18 | dependency-cruiser | Sander Verweij | current | https://github.com/sverweij/dependency-cruiser | JS and TS dependency rules; outputs dot, mermaid, json, html. | Free, MIT | verified |
| S-REC-19 | import-linter | David Seddon | current | https://github.com/seddonym/import-linter | Python import contracts. Contract types: forbidden, protected, layers, independence, acyclic siblings. | Free, BSD-2-Clause | verified |

## Diagram tools and diagram review

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-DIA-1 | Mermaid CLI (mermaid-cli) | mermaid-js | current | https://github.com/mermaid-js/mermaid-cli | Diagrams in Markdown and PRs; render with `npx -p @mermaid-js/mermaid-cli mmdc -i in.mmd -o out.svg` (needs headless Chromium). Command not run here. | Free, MIT | verified |
| S-DIA-2 | Structurizr DSL (C4 modelling language) | Simon Brown / Structurizr | current | https://docs.structurizr.com/dsl | One model, many C4 views; exports to Mermaid, PlantUML, SVG, PNG. The old CLI is deprecated; exact new binary invocation unconfirmed. | Most commands free; licence unverified | verified |
| S-DIA-3 | PlantUML command line | Arnaud Roques and community | current | https://plantuml.com/command-line | Mature UML diagrams; `java -jar plantuml.jar --svg diagram.puml`. | Free (GPL, LGPL, Apache, EPL or MIT) | verified |
| S-DIA-4 | D2 | Terrastruct | current | https://github.com/terrastruct/d2 | Clean modern output with nesting; `d2 in.d2 out.svg`. | Free, MPL-2.0 | verified |
| S-DIA-5 | LikeC4 | LikeC4 community | current | https://github.com/likec4/likec4 | C4-style architecture as code, CLI validate and export, MCP server for agents. | Free, MIT | verified |
| S-DIA-6 | draw.io desktop (diagrams.net) | JGraph | current | https://github.com/jgraph/drawio-desktop | Desktop diagram editor, Electron build of draw.io; diagrams are files you can edit. CLI flags not confirmed. | Free, GPL-3.0 | verified |
| S-DIA-7 | Excalidraw | Excalidraw | current | https://github.com/excalidraw/excalidraw | Whiteboard-style sketches in JSON; no official CLI export found. | Free, MIT | verified |
| S-DIA-8 | C4 diagram review checklist | Simon Brown | current | https://c4model.com/diagrams/checklist | Checklist for title, key, labelled arrows, element types. | Free, CC BY 4.0 | verified |
