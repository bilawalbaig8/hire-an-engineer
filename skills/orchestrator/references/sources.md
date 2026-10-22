# Sources for the Orchestrator

Where the Orchestrator's knowledge comes from. Researched and URL-checked on 2026-10-23 (each URL was fetched; the page title was read).

How to use these sources
- Ideas only, in our own words. Never copy passages. Cite a source by its ID, for example `[S-ORC-1]`.
- Cite a source as fact only when its Status is `verified`. A row marked `unverified` is a lead: say "unverified" in the same line when you mention it.
- `verified` means the page was opened and showed the title, and the URL resolved. A year or author not shown on that page comes from the well-known edition. `unverified` means the page could not be opened by automated fetch or its content was not read. An unconfirmed licence alone does not change the status.
- Free does not mean copyable: summarise, never paste.
- IDs use the `S-ORC-n` form because scripts/check_sources.py requires `S-AREA-n`.

## Multi-agent orchestration patterns

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-ORC-1 | Building effective AI agents | Erik Schluntz, Barry Zhang (Anthropic) | 2024 | https://www.anthropic.com/engineering/building-effective-agents | run-method: workflows versus agents, orchestrator-workers, keep it simple | Free to read; copyright | verified |
| S-ORC-2 | How we built our multi-agent research system | Anthropic engineering | 2025 | https://www.anthropic.com/engineering/multi-agent-research-system | briefing: lead agent briefs workers, effort scaling, lessons from failures | Free to read; copyright | verified |
| S-ORC-3 | Create custom subagents (Claude Code docs) | Anthropic | current | https://code.claude.com/docs/en/sub-agents | team-roster: how specialist agents are defined and handed work | Free to read; copyright | verified |
| S-ORC-4 | Orchestrate teams of Claude Code sessions (agent teams) | Anthropic | current | https://code.claude.com/docs/en/agent-teams | team-roster: lead and teammate sessions, shared task list | Free to read; copyright | verified |
| S-ORC-5 | Agent orchestration (OpenAI Agents SDK) | OpenAI | current | https://openai.github.io/openai-agents-python/multi_agent/ | run-method: manager pattern versus handoffs | Free to read; licence unverified | verified |
| S-ORC-6 | Handoffs (OpenAI Agents SDK) | OpenAI | current | https://openai.github.io/openai-agents-python/handoffs/ | briefing: what is passed when one agent hands over to another | Free to read; licence unverified | verified |
| S-ORC-7 | Swarm: educational multi-agent framework | OpenAI | 2024 | https://github.com/openai/swarm | run-method: minimal routines-and-handoffs idea | Free; MIT per the repo (unverified here) | verified |
| S-ORC-8 | langgraph-supervisor: supervisor multi-agent library | LangChain | current | https://github.com/langchain-ai/langgraph-supervisor-py | run-method: supervisor routes work to specialist agents | Free; MIT per the repo (unverified here) | verified |
| S-ORC-9 | LangGraph: agent orchestration framework | LangChain | current | https://www.langchain.com/langgraph | run-method: stateful graph runs with durable execution | Free to read; copyright | verified |
| S-ORC-10 | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | Qingyun Wu et al. | 2023 | https://arxiv.org/abs/2308.08155 | run-method: conversation-based multi-agent patterns | Free (arXiv) | verified |
| S-ORC-11 | Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks | Adam Fourney et al. (Microsoft Research) | 2024 | https://arxiv.org/abs/2411.04468 | run-method: orchestrator keeps a task ledger and a progress ledger | Free (arXiv) | verified |
| S-ORC-12 | CrewAI: Tasks | CrewAI | current | https://docs.crewai.com/concepts/tasks | briefing: task description, expected output, context from other tasks | Free to read; licence unverified | verified |
| S-ORC-13 | MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework | Sirui Hong et al. | 2023 | https://arxiv.org/abs/2308.00352 | team-roster: software-company roles and structured hand-off documents | Free (arXiv) | verified |
| S-ORC-14 | ChatDev: Communicative Agents for Software Development | Chen Qian et al. | 2023 | https://arxiv.org/abs/2307.07924 | team-roster: role-played phases (design, code, test) with chat between agents | Free (arXiv) | verified |
| S-ORC-15 | Why Do Multi-Agent LLM Systems Fail? | Mert Cemri et al. | 2025 | https://arxiv.org/abs/2503.13657 | failure-handling: taxonomy of multi-agent failures (spec, misalignment, verification) | Free (arXiv) | verified |
| S-ORC-16 | Magentic-One (Microsoft Research article) | Microsoft Research | 2024 | https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/ | run-method: plain-language summary; page blocked automated fetch (HTTP 403) | Free to read; copyright | unverified |

## Delegation, briefing and handoffs

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-ORC-17 | Responsibility assignment matrix (RACI) | Wikipedia contributors | ongoing | https://en.wikipedia.org/wiki/Responsibility_assignment_matrix | team-roster: who is responsible, accountable, consulted, informed | Free, CC BY-SA per Wikipedia | verified |
| S-ORC-18 | Mission command (delegated initiative) | Wikipedia contributors | ongoing | https://en.wikipedia.org/wiki/Mission_command | briefing: state the intent and limits, let the specialist choose the method | Free, CC BY-SA per Wikipedia | verified |
| S-ORC-19 | Intent (military), commander's intent | Wikipedia contributors | ongoing | https://en.wikipedia.org/wiki/Commander%27s_intent | briefing: purpose and end state so work survives surprises | Free, CC BY-SA per Wikipedia | verified |
| S-ORC-20 | SBAR (Situation, Background, Assessment, Recommendation) | Wikipedia contributors | ongoing | https://en.wikipedia.org/wiki/SBAR | questions-and-approvals: short structure for asking a human to decide | Free, CC BY-SA per Wikipedia | verified |
| S-ORC-21 | Team Topologies: key concepts | Matthew Skelton, Manuel Pais | current | https://teamtopologies.com/key-concepts | team-roster: team types, interaction modes, limiting cognitive load | Free to read; book paid; copyright | verified |
| S-ORC-22 | Effective context engineering for AI agents | Anthropic engineering | 2025 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | briefing: give each agent the smallest useful context | Free to read; copyright | verified |

## Human in the loop, approvals and one-way doors

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-ORC-23 | Jeff Bezos 2016 letter to shareholders (Type 1 and Type 2 decisions) | Jeff Bezos (Amazon) | 2016 | https://www.aboutamazon.com/news/company-news/2016-letter-to-shareholders | questions-and-approvals: slow down for one-way doors, move fast on two-way | Free to read; copyright | verified |
| S-ORC-24 | Handle approvals and user input (agent SDK docs) | Anthropic | current | https://code.claude.com/docs/en/agent-sdk/user-input | questions-and-approvals: how an agent pauses to ask or get approval | Free to read; copyright | verified |
| S-ORC-25 | Configure permissions (agent SDK docs) | Anthropic | current | https://code.claude.com/docs/en/agent-sdk/permissions | questions-and-approvals: allow, deny and ask rules for tool use | Free to read; copyright | verified |
| S-ORC-26 | Human-in-the-loop (OpenAI Agents SDK) | OpenAI | current | https://openai.github.io/openai-agents-python/human_in_the_loop/ | questions-and-approvals: pausing a run for approval and resuming | Free to read; licence unverified | verified |
| S-ORC-27 | Documenting Architecture Decisions | Michael Nygard | 2011 | https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions | run-records: short decision records with context and consequences | Free to read; copyright | verified |
| S-ORC-28 | Architecture Decision Record | Martin Fowler | 2023 | https://martinfowler.com/bliki/ArchitectureDecisionRecord.html | run-records: why decisions are written down and kept | Free to read; copyright | verified |

## Task decomposition and planning

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-ORC-29 | Plan-and-Solve Prompting | Lei Wang et al. | 2023 | https://arxiv.org/abs/2305.04091 | run-method: plan first, then execute the steps | Free (arXiv) | verified |
| S-ORC-30 | ReAct: Synergizing Reasoning and Acting in Language Models | Shunyu Yao et al. | 2022 | https://arxiv.org/abs/2210.03629 | run-method: interleave thinking and acting with observations | Free (arXiv) | verified |
| S-ORC-31 | Reflexion: Language Agents with Verbal Reinforcement Learning | Noah Shinn et al. | 2023 | https://arxiv.org/abs/2303.11366 | failure-handling: retry with a written lesson from the last attempt | Free (arXiv) | verified |
| S-ORC-32 | Work breakdown structure | Wikipedia contributors | ongoing | https://en.wikipedia.org/wiki/Work_breakdown_structure | run-method: split work into deliverable-based pieces | Free, CC BY-SA per Wikipedia | verified |
| S-ORC-33 | The Mythical Man-Month | Fred Brooks | 1975 | https://en.wikipedia.org/wiki/The_Mythical_Man-Month | run-method: adding workers to late work adds communication cost | Book paid; page free | verified |
| S-ORC-34 | Conway's Law | Martin Fowler | 2022 | https://martinfowler.com/bliki/ConwaysLaw.html | team-roster: short explanation and design consequences | Free to read; copyright | verified |

## Quality gates and review

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-ORC-35 | Definition of Done | Agile Alliance | ongoing | https://www.agilealliance.org/glossary/definition-of-done/ | quality-gates: shared checklist that says when work counts as finished | Free to read; copyright | verified |
| S-ORC-36 | Google Engineering Practices: Code review | Google | ongoing | https://google.github.io/eng-practices/review/ | quality-gates: standard for what a reviewer must confirm | Free; licence unverified here | verified |
| S-ORC-37 | DORA software delivery performance metrics | DORA (Google Cloud) | ongoing | https://dora.dev/guides/dora-metrics-four-keys/ | quality-gates: speed and stability measures that balance each other | Free to read; copyright | verified |
| S-ORC-38 | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | Carlos Jimenez et al. | 2023 | https://arxiv.org/abs/2310.06770 | quality-gates: judge agent work by tests that pass, not by claims | Free (arXiv) | verified |

## Failure handling and caps

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-ORC-39 | Circuit Breaker | Martin Fowler | 2014 | https://martinfowler.com/bliki/CircuitBreaker.html | failure-handling: stop calling something that keeps failing | Free to read; copyright | verified |
| S-ORC-40 | Circuit Breaker pattern (Azure Architecture Center) | Microsoft | current | https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker | failure-handling: closed, open and half-open states | Free to read; copyright | verified |
| S-ORC-41 | Timeouts, retries and backoff with jitter | Marc Brooker (Amazon Builders' Library) | ongoing | https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ | failure-handling: caps on retries, backoff, avoid retry storms | Free to read; copyright | verified |
| S-ORC-42 | Saga pattern | Chris Richardson | ongoing | https://microservices.io/patterns/data/saga.html | failure-handling: multi-step work with undo steps | Free to read; copyright | verified |
| S-ORC-43 | Compensating Transaction pattern (Azure Architecture Center) | Microsoft | current | https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction | failure-handling: undoing finished steps when a later step fails | Free to read; copyright | verified |
| S-ORC-44 | Manage costs effectively (Claude Code docs) | Anthropic | current | https://code.claude.com/docs/en/costs | failure-handling: budget and turn limits for agent runs | Free to read; copyright | verified |
| S-ORC-45 | Release It!, 2nd edition | Michael Nygard | 2018 | https://pragprog.com/titles/mnee2/release-it-second-edition/ | failure-handling: stability patterns such as timeouts and bulkheads | Paid | verified |

## Prompt injection and trust

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-ORC-46 | OWASP Top 10 for LLM Applications | OWASP GenAI Security Project | 2025 | https://genai.owasp.org/llm-top-10/ | briefing: risk list the orchestrator must respect when relaying content | Free; licence unverified here | verified |
| S-ORC-47 | LLM01:2025 Prompt Injection | OWASP GenAI Security Project | 2025 | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | briefing: treat agent and tool output as data, not instructions | Free; licence unverified here | verified |
| S-ORC-48 | LLM06:2025 Excessive Agency | OWASP GenAI Security Project | 2025 | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | questions-and-approvals: limit what an agent may do without approval | Free; licence unverified here | verified |
| S-ORC-49 | Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection | Kai Greshake et al. | 2023 | https://arxiv.org/abs/2302.12173 | briefing: indirect injection through content an agent reads | Free (arXiv) | verified |
| S-ORC-50 | InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents | Qiusi Zhan et al. | 2024 | https://arxiv.org/abs/2403.02691 | failure-handling: how often tool-using agents are hijacked | Free (arXiv) | verified |
| S-ORC-51 | AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses | Edoardo Debenedetti et al. | 2024 | https://arxiv.org/abs/2406.13352 | failure-handling: tests for injection defences in agent tasks | Free (arXiv) | verified |
| S-ORC-52 | The lethal trifecta for AI agents | Simon Willison | 2025 | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | questions-and-approvals: private data plus untrusted content plus outbound action needs a human gate | Free to read; copyright | verified |
| S-ORC-53 | Mitigate jailbreaks and prompt injections | Anthropic | current | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | briefing: vendor guidance on screening inputs and limiting damage | Free to read; copyright | verified |
| S-ORC-54 | Mitigating prompt injections in browser use | Anthropic | 2025 | https://www.anthropic.com/research/prompt-injection-defenses | questions-and-approvals: confirmations and layered defences for agent actions | Free to read; copyright | verified |

## Run records and observability

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-ORC-55 | Event Sourcing | Martin Fowler | 2005 | https://martinfowler.com/eaaDev/EventSourcing.html | run-records: append-only log of what happened, rebuild state from it | Free to read; copyright | verified |
| S-ORC-56 | Semantic conventions for generative AI (OpenTelemetry) | OpenTelemetry project | current | https://opentelemetry.io/docs/specs/semconv/gen-ai/ | run-records: standard names for agent and model spans (page now says moved) | Free; licence unverified here | verified |
| S-ORC-57 | LangSmith observability | LangChain | current | https://docs.langchain.com/langsmith/observability | run-records: traces, runs and feedback for agent apps | Free to read; product paid | verified |
| S-ORC-58 | Postmortem culture: learning from failure (SRE book) | Google SRE | 2016 | https://sre.google/sre-book/postmortem-culture/ | run-records: blameless write-up after a failed run | Free to read online; copyright | verified |
