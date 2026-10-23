# Sources for the AI Engineer

Where the AI Engineer's knowledge comes from. Researched and checked on 2026-10-24: every URL was fetched by a script; the page title, author name and year were compared with this table, and a row is `verified` only when they matched. 98 external sources verified, 2 unverified, plus 7 own-base files.

How to use these sources
- Ideas only, in our own words. Never copy passages. Cite a source by its ID, for example `[S-EVL-1]`.
- Cite a source as fact only when its Status is `verified`. A row marked `unverified` is a lead: say "unverified" in the same line when you mention it.
- `verified` means the page or a trustworthy catalogue record (arXiv, Crossref/DOI, Open Library) was read and showed the title and author, and the URL resolved. A year not shown on that page comes from the well-known edition. Documentation pages marked `current` change over time: re-check a detail (model names, limits, prices, parameter names) in the live page before relying on it.
- Provider documentation changes quickly. Treat model names, limits and prices as `unknown` until read from the live page during the job.
- Regulatory pages are orientation only, never legal advice.
- Free does not mean copyable: summarise, never paste.

## Our own base (the owner's hire-an-engineer skill, in this repo)

The AI Engineer starts from these files and does not contradict them. The URL is the repository; the path is in the title.

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-OWN-1 | hire-an-engineer: AI Features and Agents (skills/hire-an-engineer/references/ai-agents.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Simplest shape first, hard stops for every loop, tools, minimum access and draft-don't-do, state outside the prompt, facts need sources, evals before launch (10 to 30 examples), run logs, fallbacks and pinned versions, launch checklist. | Own work (see the repository licence) | verified |
| S-OWN-2 | hire-an-engineer: Cost Management and AI Usage Audit (skills/hire-an-engineer/references/cost-management.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Product AI cost formula, smallest model that passes, caching and batching, guardrails, AI usage log table, budgets and alerts, model-to-work table. | Own work (see the repository licence) | verified |
| S-OWN-3 | hire-an-engineer: Engineering principles, section 6 Security (skills/hire-an-engineer/references/engineering-principles.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Prompt injection in AI features, privacy by design, secrets, package checks. | Own work (see the repository licence) | verified |
| S-OWN-4 | hire-an-engineer: Platform targets, section 3 Data analysis and ML projects (skills/hire-an-engineer/references/platform-targets.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Reproducibility, split before looking, leakage, baseline first, privacy, what numbers do not prove. | Own work (see the repository licence) | verified |
| S-OWN-5 | hire-an-engineer: Integrations, section 11 Real customer data sent to an AI tool (skills/hire-an-engineer/references/integrations.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Real or personal data goes to an AI tool only with informed approval; otherwise samples or anonymised copies. | Own work (see the repository licence) | verified |
| S-OWN-6 | hire-an-engineer: Roles (skills/hire-an-engineer/references/roles.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Role checklist of the one-person team; the base from which the separate specialist roles were split. | Own work (see the repository licence) | verified |
| S-OWN-7 | hire-an-engineer: Technical products, scale plan (skills/hire-an-engineer/references/technical-products.md) | Bilawal Baig (owner) | 2026 | https://github.com/bilawalbaig8/hire-an-engineer | Scale plan asks what breaks first at 10x and 100x, including AI cost. | Own work (see the repository licence) | verified |

## Model providers, prompting, tools and agents

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-LLM-1 | Prompt engineering overview (Claude docs) | Anthropic | current | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Prompt basics, success criteria first, techniques such as clear instructions, examples, XML structure, role prompts. | Free; copyright | verified |
| S-LLM-2 | Tool use with Claude (overview) | Anthropic | current | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | How tool definitions, tool calls and tool results flow; the application executes tools, not the model. | Free; copyright | verified |
| S-LLM-3 | Prompt caching (Claude docs) | Anthropic | current | https://platform.claude.com/docs/en/build-with-claude/prompt-caching | Caching a stable prompt prefix for latency and cost; what breaks a cache hit. | Free; copyright | verified |
| S-LLM-4 | Define success criteria and build evaluations (Claude docs) | Anthropic | current | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Success criteria that are specific and measurable; eval design principles and grading methods (code, human, model). | Free; copyright | verified |
| S-LLM-5 | Building effective agents | Anthropic (Erik S., Barry Zhang) | 2024 | https://www.anthropic.com/engineering/building-effective-agents | Simplest shape first: single call, workflow patterns, then agents; tools deserve as much care as prompts. | Free; copyright | verified |
| S-LLM-6 | Reduce hallucinations (Claude docs) | Anthropic | current | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | Allow I-don't-know, quote-first answers, verification passes, restricting to given documents. | Free; copyright | verified |
| S-LLM-7 | Mitigate jailbreaks and prompt injections (Claude docs) | Anthropic | current | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | Layered mitigations: input screening, harmlessness checks, prompt design; none is complete alone. | Free; copyright | verified |
| S-LLM-8 | Reduce latency (Claude docs) | Anthropic | current | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency | Latency levers: model choice, shorter prompts and outputs, streaming. | Free; copyright | verified |
| S-LLM-9 | Message Batches (Claude docs) | Anthropic | current | https://platform.claude.com/docs/en/build-with-claude/batch-processing | Asynchronous batch processing for non-urgent work at a lower price; limits and result retrieval. | Free; copyright | verified |
| S-LLM-10 | Writing effective tools for agents | Anthropic | 2025 | https://www.anthropic.com/engineering/writing-tools-for-agents | Design tools for agents, prototype, evaluate on realistic tasks, return meaningful context, token-efficient results. | Free; copyright | verified |
| S-LLM-11 | Model Context Protocol specification | Model Context Protocol project | current | https://modelcontextprotocol.io/specification/latest | An open protocol for connecting models to tools and data; its security and trust considerations for tools. | Free; open spec | verified |
| S-LLM-12 | Structured Outputs (OpenAI docs) | OpenAI | current | https://developers.openai.com/api/docs/guides/structured-outputs | Schema-constrained model output versus plain JSON mode; refusals and edge cases. | Free; copyright | verified |
| S-LLM-13 | Function calling (OpenAI docs) | OpenAI | current | https://developers.openai.com/api/docs/guides/function-calling | Defining functions, handling tool calls, strict mode; the same pattern as other providers. | Free; copyright | verified |
| S-LLM-14 | Working with evals (OpenAI docs) | OpenAI | current | https://developers.openai.com/api/docs/guides/evals | Eval workflow: datasets, graders, runs; model-based and string-check graders. | Free; copyright | verified |
| S-LLM-15 | OpenAI Cookbook | OpenAI | current | https://developers.openai.com/cookbook | Worked examples for retrieval, evals, function calling, guardrails; code recipes to adapt. | Free; MIT per repo (unverified here) | verified |
| S-LLM-16 | A practical guide to building agents | OpenAI | 2025 | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | Agent design: when to use, tools, guardrails, human intervention triggers. The PDF resolved but its text could not be read here. | Free; copyright | unverified |
| S-LLM-17 | Safety best practices (OpenAI docs) | OpenAI | current | https://developers.openai.com/api/docs/guides/safety-best-practices | Moderation, human in the loop, adversarial testing, input and output limits, user identifiers. | Free; copyright | verified |
| S-LLM-18 | Prompt engineering (OpenAI docs) | OpenAI | current | https://developers.openai.com/api/docs/guides/prompt-engineering | Prompt message roles, pinning model snapshots, evals as the guard against prompt drift. | Free; copyright | verified |
| S-LLM-19 | Structured output (Gemini API docs) | Google | current | https://ai.google.dev/gemini-api/docs/structured-output | Schema-constrained output on a third provider; shows the pattern is provider-independent. | Free; copyright | verified |
| S-LLM-20 | Rate limits (Claude API docs) | Anthropic | current | https://docs.anthropic.com/en/api/rate-limits | Quota concepts to design around: request and token limits, 429 handling, backoff. | Free; copyright | verified |

## Evaluation and judging

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-EVL-1 | Your AI Product Needs Evals | Hamel Husain | 2024 | https://hamel.dev/blog/posts/evals/ | Three levels of evals (unit tests, human and model review, A/B); look at data; remove friction from reading traces. | Free; copyright | verified |
| S-EVL-2 | Using LLM-as-a-Judge For Evaluation: A Complete Guide | Hamel Husain | 2024 | https://hamel.dev/blog/posts/llm-judge/ | Calibrating a model judge against one domain expert; critiques; pass/fail over scores. | Free; copyright | verified |
| S-EVL-3 | A Field Guide to Rapidly Improving AI Products | Hamel Husain | 2025 | https://hamel.dev/blog/posts/field-guide/ | Error analysis first, custom data viewers, binary evals, roadmap by experiments. | Free; copyright | verified |
| S-EVL-4 | Task-Specific LLM Evals that Do & Don't Work | Eugene Yan | 2024 | https://eugeneyan.com/writing/evals/ | Per-task metrics for classification, summarisation, extraction, retrieval; which ones mislead. | Free; copyright | verified |
| S-EVL-5 | Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge) | Eugene Yan | 2024 | https://eugeneyan.com/writing/llm-evaluators/ | Survey of model-as-judge use, biases and practical guidance. | Free; copyright | verified |
| S-EVL-6 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | Lianmin Zheng et al. | 2023 | https://arxiv.org/abs/2306.05685 | Position, verbosity and self-preference bias of model judges and agreement with humans. | Free; arXiv | verified |
| S-EVL-7 | Large Language Models are not Fair Evaluators | Peiyi Wang et al. | 2023 | https://arxiv.org/abs/2305.17926 | Order of candidates changes the judge's verdict; calibration and swapping as mitigations. | Free; arXiv | verified |
| S-EVL-8 | Holistic Evaluation of Language Models | Percy Liang et al. | 2022 | https://arxiv.org/abs/2211.09110 | Evaluate many scenarios and several metrics (accuracy, calibration, robustness, fairness, toxicity, efficiency), not one score. | Free; arXiv | verified |
| S-EVL-9 | Ragas: Automated Evaluation of Retrieval Augmented Generation | Shahul Es et al. | 2023 | https://arxiv.org/abs/2309.15217 | Reference-free RAG metrics (faithfulness, answer relevance, context relevance) and their caveats. | Free; arXiv | verified |
| S-EVL-10 | A Survey of Hallucination in Natural Language Generation | Ziwei Ji et al. | 2022 | https://arxiv.org/abs/2202.03629 | Taxonomy of intrinsic and extrinsic hallucination; metrics and mitigation. | Free; arXiv | verified |
| S-EVL-11 | Lost in the Middle: How Language Models Use Long Contexts | Nelson F. Liu et al. | 2023 | https://arxiv.org/abs/2307.03172 | Models use information at the start and end of a long context better than the middle; affects how many chunks to stuff. | Free; arXiv | verified |
| S-EVL-12 | Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks | Curtis G. Northcutt et al. | 2021 | https://arxiv.org/abs/2103.14749 | Labelled sets contain errors; check labels before trusting a metric. | Free; arXiv | verified |
| S-EVL-13 | Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences | Shreya Shankar et al. | 2024 | https://arxiv.org/abs/2404.12272 | People refine criteria while grading outputs (criteria drift), so judge criteria need iteration against human labels. | Free; arXiv | verified |

## Retrieval, embeddings and vector search

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-RAG-1 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Patrick Lewis et al. | 2020 | https://arxiv.org/abs/2005.11401 | The original RAG idea: a retriever plus a generator, with sources kept outside the model weights. | Free; arXiv | verified |
| S-RAG-2 | Retrieval-Augmented Generation for Large Language Models: A Survey | Yunfan Gao et al. | 2023 | https://arxiv.org/abs/2312.10997 | Naive, advanced and modular RAG; where each stage can fail. | Free; arXiv | verified |
| S-RAG-3 | Dense Passage Retrieval for Open-Domain Question Answering | Vladimir Karpukhin et al. | 2020 | https://arxiv.org/abs/2004.04906 | Embedding-based retrieval beating keyword search on some tasks; the dense versus sparse trade-off. | Free; arXiv | verified |
| S-RAG-4 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | Nandan Thakur et al. | 2021 | https://arxiv.org/abs/2104.08663 | Keyword search (BM25) is a strong baseline that embeddings do not always beat out of domain. | Free; arXiv | verified |
| S-RAG-5 | MTEB: Massive Text Embedding Benchmark | Niklas Muennighoff et al. | 2022 | https://arxiv.org/abs/2210.07316 | No single embedding model wins every task; choose and test on your own data. | Free; arXiv | verified |
| S-RAG-6 | Introducing Contextual Retrieval | Anthropic | 2024 | https://www.anthropic.com/news/contextual-retrieval | Adding chunk-level context and reranking; vendor-reported gains in failed retrievals (their figures). | Free; copyright | verified |
| S-RAG-7 | Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods | Gordon V. Cormack, Charles L. A. Clarke, Stefan Buettcher | 2009 | https://doi.org/10.1145/1571941.1572114 | A simple way to merge keyword and vector rankings. Checked through the Crossref record for the DOI (title, authors, year). | Free; copyright | verified |
| S-RAG-8 | Faiss documentation and wiki | Meta AI Research | current | https://github.com/facebookresearch/faiss/wiki | Index types, choosing an index, getting started; local similarity search with no service. | Free; MIT per repo (unverified here) | verified |
| S-RAG-9 | pgvector: open-source vector similarity search for Postgres | Andrew Kane and contributors | current | https://github.com/pgvector/pgvector | Vector columns, exact and approximate indexes (HNSW, IVFFlat) inside Postgres, with SQL filters. | Free; PostgreSQL licence per repo (unverified here) | verified |
| S-RAG-10 | SQLite FTS5 extension | SQLite project | current | https://www.sqlite.org/fts5.html | Built-in full-text search with BM25 ranking: a dependency-free keyword baseline for small corpora. | Free; public domain | verified |

## Agent and reasoning research, cost

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-AGT-1 | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | Jason Wei et al. | 2022 | https://arxiv.org/abs/2201.11903 | Intermediate reasoning steps improve multi-step tasks on large models; not a guarantee for every task. | Free; arXiv | verified |
| S-AGT-2 | ReAct: Synergizing Reasoning and Acting in Language Models | Shunyu Yao et al. | 2022 | https://arxiv.org/abs/2210.03629 | Interleaving reasoning and tool actions; the loop behind most agents. | Free; arXiv | verified |
| S-AGT-3 | Toolformer: Language Models Can Teach Themselves to Use Tools | Timo Schick et al. | 2023 | https://arxiv.org/abs/2302.04761 | Models can learn when to call tools such as a calculator or search. | Free; arXiv | verified |
| S-AGT-4 | Agents | Chip Huyen | 2025 | https://huyenchip.com/2025/01/07/agents.html | Tools, planning, reflection, failure modes; errors compound across steps. | Free; copyright | verified |
| S-AGT-5 | FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance | Lingjiao Chen, Matei Zaharia, James Zou | 2023 | https://arxiv.org/abs/2305.05176 | Cascades, caching and prompt adaptation to cut spend; the idea of trying a cheap model first. | Free; arXiv | verified |
| S-AGT-6 | tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains | Shunyu Yao et al. | 2024 | https://arxiv.org/abs/2406.12045 | Agent evals with policy rules and repeated trials; reliability across repeated runs is much lower than one-run success. | Free; arXiv | verified |

## Security and prompt injection

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-SEC-1 | OWASP Top 10 for LLM Applications (project page) | OWASP | 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | The standard risk list: prompt injection, sensitive information disclosure, excessive agency, and others. | Free; CC BY-SA per OWASP (unverified here) | verified |
| S-SEC-2 | LLM Prompt Injection Prevention Cheat Sheet | OWASP Cheat Sheet Series | current | https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html | Practical prevention steps for direct and indirect injection. | Free; CC BY-SA per OWASP (unverified here) | verified |
| S-SEC-3 | Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection | Kai Greshake et al. | 2023 | https://arxiv.org/abs/2302.12173 | Instructions hidden in retrieved data can hijack an app; the origin of the indirect-injection threat model. | Free; arXiv | verified |
| S-SEC-4 | Defending Against Indirect Prompt Injection Attacks With Spotlighting | Keegan Hines et al. | 2024 | https://arxiv.org/abs/2403.14720 | Marking untrusted text (delimiting, encoding) to help the model tell data from instructions; a mitigation, not a fix. | Free; arXiv | verified |
| S-SEC-5 | Design Patterns for Securing LLM Agents against Prompt Injections | Luca Beurer-Kellner et al. | 2025 | https://arxiv.org/abs/2506.08837 | Architectural patterns (plan-then-execute, dual model, action selector) that limit what injected text can cause. | Free; arXiv | verified |
| S-SEC-6 | The lethal trifecta for AI agents | Simon Willison | 2025 | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | Private data plus untrusted content plus an outbound channel is the dangerous combination; remove a leg. | Free; copyright | verified |
| S-SEC-7 | Extracting Training Data from Large Language Models | Nicholas Carlini et al. | 2020 | https://arxiv.org/abs/2012.07805 | Models can reveal memorised training text; a reason to keep personal data out of training and fine-tuning sets. | Free; arXiv | verified |
| S-SEC-8 | MITRE ATLAS (Adversarial Threat Landscape for AI Systems) | MITRE | current | https://atlas.mitre.org/ | Attack tactics and case studies against AI systems, in the ATT&CK style. | Free; copyright | verified |
| S-SEC-9 | Secure AI Framework (SAIF) | Google | current | https://saif.google/secure-ai-framework | Six core elements for securing AI systems; risk map. | Free; copyright | verified |
| S-SEC-10 | Defeating Prompt Injections by Design (CaMeL) | Edoardo Debenedetti et al. | 2025 | https://arxiv.org/abs/2503.18813 | A design that separates trusted control flow from untrusted data so injected text cannot steer tool calls. | Free; arXiv | verified |
| S-SEC-11 | AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents | Edoardo Debenedetti et al. | 2024 | https://arxiv.org/abs/2406.13352 | A benchmark showing agents with tools are often hijackable; useful as a test-design model. | Free; arXiv | verified |

## Governance, privacy, regulation and documentation

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-GOV-1 | Artificial Intelligence Risk Management Framework (AI RMF 1.0), NIST AI 100-1 | NIST | 2023 | https://www.nist.gov/itl/ai-risk-management-framework | Govern, map, measure, manage; a voluntary framework for AI risk. | Free (US government) | verified |
| S-GOV-2 | Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1) | NIST | 2024 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf | Twelve risks specific to generative AI and suggested actions. PDF body not read; Crossref record and URL checked. | Free (US government) | verified |
| S-GOV-3 | Model Cards for Model Reporting | Margaret Mitchell et al. | 2018 | https://arxiv.org/abs/1810.03993 | What a model card should say: intended use, data, metrics by group, limits. | Free; arXiv | verified |
| S-GOV-4 | Datasheets for Datasets | Timnit Gebru et al. | 2018 | https://arxiv.org/abs/1803.09010 | Question list for documenting how a dataset was made, what it contains and how it may be used. | Free; arXiv | verified |
| S-GOV-5 | AI Act: regulatory framework (European Commission) | European Commission | current | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai | Official summary of the risk-based EU AI Act. Orientation only, not legal advice. | Free; EU | verified |
| S-GOV-6 | EU Artificial Intelligence Act explorer and summaries | Future of Life Institute | current | https://artificialintelligenceact.eu/ | Readable article-by-article text and summaries of the Act. Orientation only, not legal advice. | Free; copyright | verified |
| S-GOV-7 | Regulation (EU) 2016/679 (GDPR) | European Union | 2016 | https://eur-lex.europa.eu/eli/reg/2016/679/oj | Primary text for personal-data rules that apply when personal data goes to an AI service. The site answered with a challenge page, so it was not read. Not legal advice. | Free; EU | unverified |
| S-GOV-8 | Guidance on AI and data protection | UK Information Commissioner's Office | current | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/ | Regulator guidance on fairness, accountability, data minimisation in AI. | Free; Open Government Licence per ICO (unverified here) | verified |
| S-GOV-9 | Microsoft Responsible AI principles and approach | Microsoft | current | https://www.microsoft.com/en-us/ai/principles-and-approach | The six principles and the Responsible AI Standard overview. | Free; copyright | verified |
| S-GOV-10 | Model Cards (Hugging Face Hub documentation) | Hugging Face | current | https://huggingface.co/docs/hub/model-cards | A practical model-card template and the sections it expects. | Free; Apache-2.0 per project (unverified here) | verified |

## Training, fine-tuning, validation and leakage

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-TRN-1 | Rules of Machine Learning: Best Practices for ML Engineering | Martin Zinkevich (Google) | 2017 | https://developers.google.com/machine-learning/guides/rules-of-ml | Ship a simple baseline first; do not use ML when rules suffice; infrastructure before fancy models. | Free; CC BY per Google (unverified here) | verified |
| S-TRN-2 | Hidden Technical Debt in Machine Learning Systems | D. Sculley et al. | 2015 | https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html | Why ML systems accumulate debt: entanglement, feedback loops, data dependencies, glue code. | Free; NeurIPS | verified |
| S-TRN-3 | The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction | Eric Breck et al. | 2017 | https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/ | Checklist of tests for data, model, infrastructure and monitoring before production. | Free; copyright | verified |
| S-TRN-4 | Cross-validation: evaluating estimator performance (scikit-learn user guide) | scikit-learn developers | current | https://scikit-learn.org/stable/modules/cross_validation.html | Train/test splits, k-fold, stratified and grouped splits, and why preprocessing must sit inside the pipeline. | Free; BSD-3 per project (unverified here) | verified |
| S-TRN-5 | Common pitfalls and recommended practices (scikit-learn) | scikit-learn developers | current | https://scikit-learn.org/stable/common_pitfalls.html | Data leakage examples, inconsistent preprocessing, randomness control. | Free; BSD-3 per project (unverified here) | verified |
| S-TRN-6 | Metrics and scoring: quantifying the quality of predictions (scikit-learn) | scikit-learn developers | current | https://scikit-learn.org/stable/modules/model_evaluation.html | Choosing metrics for classification; precision, recall, F1, confusion matrices, class imbalance. | Free; BSD-3 per project (unverified here) | verified |
| S-TRN-7 | Dummy estimators (scikit-learn) | scikit-learn developers | current | https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html | The majority-class baseline every model must beat. | Free; BSD-3 per project (unverified here) | verified |
| S-TRN-8 | Probability calibration (scikit-learn) | scikit-learn developers | current | https://scikit-learn.org/stable/modules/calibration.html | Whether predicted probabilities mean what they say; reliability curves. | Free; BSD-3 per project (unverified here) | verified |
| S-TRN-9 | Cross-validation failure: small sample sizes lead to large error bars | Gael Varoquaux | 2017 | https://arxiv.org/abs/1706.07581 | With few samples, the error bars on an accuracy estimate are wide; relevant to tiny labelled sets. | Free; arXiv | verified |
| S-TRN-10 | Leakage and the Reproducibility Crisis in ML-based Science | Sayash Kapoor, Arvind Narayanan | 2022 | https://arxiv.org/abs/2207.07048 | Survey of leakage types found in published studies; a leakage checklist idea. | Free; arXiv | verified |
| S-TRN-11 | On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation | Gavin C. Cawley, Nicola L. C. Talbot | 2010 | https://jmlr.org/papers/v11/cawley10a.html | Tuning on the same data you report on inflates results; use nested validation. | Free; JMLR | verified |
| S-TRN-12 | Underspecification Presents Challenges for Credibility in Modern Machine Learning | Alexander D'Amour et al. | 2020 | https://arxiv.org/abs/2011.03395 | Models with equal test scores can behave differently in deployment; test beyond the held-out score. | Free; arXiv | verified |
| S-TRN-13 | Shortcut Learning in Deep Neural Networks | Robert Geirhos et al. | 2020 | https://arxiv.org/abs/2004.07780 | Models learn spurious cues that work on the test set and fail in the world. | Free; arXiv | verified |
| S-TRN-14 | Transformers: fine-tune a pretrained model (Hugging Face docs) | Hugging Face | current | https://huggingface.co/docs/transformers/training | The standard fine-tuning workflow: data, tokenization, Trainer, evaluation metric. | Free; Apache-2.0 per project (unverified here) | verified |
| S-TRN-15 | PEFT (parameter-efficient fine-tuning) documentation | Hugging Face | current | https://huggingface.co/docs/peft/index | Adapters such as LoRA that train few parameters; lower cost, same evaluation duties. | Free; Apache-2.0 per project (unverified here) | verified |
| S-TRN-16 | Evaluate library documentation | Hugging Face | current | https://huggingface.co/docs/evaluate/index | Standard metric implementations and their use. | Free; Apache-2.0 per project (unverified here) | verified |
| S-TRN-17 | LoRA: Low-Rank Adaptation of Large Language Models | Edward J. Hu et al. | 2021 | https://arxiv.org/abs/2106.09685 | Freeze base weights and train small low-rank matrices; the idea behind most cheap fine-tunes. | Free; arXiv | verified |
| S-TRN-18 | Confident Learning: Estimating Uncertainty in Dataset Labels | Curtis G. Northcutt, Lu Jiang, Isaac L. Chuang | 2019 | https://arxiv.org/abs/1911.00068 | A method for finding mislabelled rows before training. | Free; arXiv | verified |

## Books and practitioner writing

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-BOK-1 | AI Engineering: Building Applications with Foundation Models | Chip Huyen | 2025 | https://www.oreilly.com/library/view/ai-engineering/9781098166298/ | Evaluation, prompting, RAG, agents, finetuning, latency and cost in one reference. Checked through an Open Library listing (title and author), not the publisher page (blocked). | Paid | verified |
| S-BOK-2 | Designing Machine Learning Systems | Chip Huyen | 2022 | https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/ | Data, features, training, deployment, monitoring and data distribution shift. Checked through an Open Library listing (title and author), not the publisher page (blocked). | Paid | verified |
| S-BOK-3 | Building A Generative AI Platform | Chip Huyen | 2024 | https://huyenchip.com/2024/07/25/genai-platform.html | Components around the model: gateway, guardrails, caching, routing, observability. | Free; copyright | verified |
| S-BOK-4 | Patterns for Building LLM-based Systems & Products | Eugene Yan | 2023 | https://eugeneyan.com/writing/llm-patterns/ | Seven patterns: evals, RAG, fine-tuning, caching, guardrails, defensive UX, collect user feedback. | Free; copyright | verified |
| S-BOK-5 | What We Learned from a Year of Building with LLMs (Part I) | Eugene Yan, Bryan Bischof, Charles Frye, Hamel Husain, Jason Liu, Shreya Shankar | 2024 | https://www.oreilly.com/radar/what-we-learned-from-a-year-of-building-with-llms-part-i/ | Tactical lessons: prompting, RAG, flow engineering, evaluation and monitoring. | Free; copyright | verified |
| S-BOK-6 | Why Language Models Hallucinate | OpenAI | 2025 | https://openai.com/index/why-language-models-hallucinate/ | Why training and grading that reward guessing produce confident wrong answers; supports rewarding abstention in evals. | Free; copyright | verified |
| S-BOK-7 | Demystifying evals for AI agents | Anthropic | 2026 | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | How to grade agent runs: tasks, trials, graders, transcripts. | Free; copyright | verified |
| S-BOK-8 | Don't Mock Machine Learning Models In Unit Tests | Eugene Yan | 2020 | https://eugeneyan.com/writing/unit-testing-ml/ | What to test in ML code without mocking the model away: shapes, ranges, behaviour on fixed inputs. | Free; copyright | verified |
| S-BOK-9 | Common pitfalls when building generative AI applications | Chip Huyen | 2025 | https://huyenchip.com/2025/01/16/ai-engineering-pitfalls.html | Using generative AI when it is not needed, too much complexity too early, not evaluating by hand, over-trusting judges. | Free; copyright | verified |

## Testing and observability tooling

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-OPS-1 | Semantic conventions for generative AI (OpenTelemetry semantic-conventions repository) | OpenTelemetry project | current | https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai | Shared names for tracing model calls (model, tokens, operation) so traces are comparable. | Free; Apache-2.0 per project (unverified here) | verified |
| S-OPS-2 | unittest.mock: mock object library | Python Software Foundation | current | https://docs.python.org/3/library/unittest.mock.html | Standard-library mocks and patching: test model-calling code without a live call. | Free; PSF licence | verified |
| S-OPS-3 | VCR.py: record and replay HTTP interactions | VCR.py contributors | current | https://vcrpy.readthedocs.io/ | Recorded fixtures for HTTP calls so tests replay instead of calling a paid API. Third-party tool. | Free; MIT per project (unverified here) | verified |

## AI-Ops backing (release check, monitor, investigate)

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-AIO-1 | Your AI Product Needs Evals | Husain | 2024 | https://hamel.dev/blog/posts/evals/ | AI-Ops backing: Evals | see publisher | verified |
| S-AIO-2 | A Field Guide to Rapidly Improving AI Products | Husain | 2025 | https://hamel.dev/blog/posts/field-guide/ | AI-Ops backing: Evals | see publisher | verified |
| S-AIO-3 | Demystifying evals for AI agents | Anthropic | 2026 | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | AI-Ops backing: Evals | see publisher | verified |
| S-AIO-4 | Define success criteria and build evaluations | Anthropic Docs | current | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | AI-Ops backing: Evals | see publisher | verified |
| S-AIO-5 | Working with evals | OpenAI Docs | current | https://developers.openai.com/api/docs/guides/evals | AI-Ops backing: Evals | see publisher | verified |
| S-AIO-6 | Beyond Accuracy: Behavioral Testing of NLP Models with CheckList | Ribeiro et al. | 2020 | https://arxiv.org/abs/2005.04118 | AI-Ops backing: Evals | see publisher | verified |
| S-AIO-7 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | Zheng et al. | 2023 | https://arxiv.org/abs/2306.05685 | AI-Ops backing: Judges | see publisher | verified |
| S-AIO-8 | Who Validates the Validators? | Shankar et al. | 2024 | https://arxiv.org/abs/2404.12272 | AI-Ops backing: Judges | see publisher | verified |
| S-AIO-9 | Evaluating the Effectiveness of LLM-Evaluators | Yan | 2024 | https://eugeneyan.com/writing/llm-evaluators/ | AI-Ops backing: Judges | see publisher | verified |
| S-AIO-10 | Get started with prompt management | Langfuse Docs | current | https://langfuse.com/docs/prompts/get-started | AI-Ops backing: Prompts as code | see publisher | verified |
| S-AIO-11 | Prompt Registry | MLflow Docs | current | https://mlflow.org/docs/latest/genai/prompt-registry/ | AI-Ops backing: Prompts as code | see publisher | verified |
| S-AIO-12 | Intro | Promptfoo Docs | current | https://www.promptfoo.dev/docs/intro/ | AI-Ops backing: Prompts as code | see publisher | verified |
| S-AIO-13 | Prompt engineering | OpenAI Docs | current | https://developers.openai.com/api/docs/guides/prompt-engineering | AI-Ops backing: Prompts as code | see publisher | verified |
| S-AIO-14 | Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design | Sclar et al. | 2023 | https://arxiv.org/abs/2310.11324 | AI-Ops backing: Prompts as code | see publisher | verified |
| S-AIO-15 | How is ChatGPT's behavior changing over time? | Chen, Zaharia, Zou | 2023 | https://arxiv.org/abs/2307.09009 | AI-Ops backing: Model change | see publisher | verified |
| S-AIO-16 | Model deprecations | Anthropic Docs | current | https://platform.claude.com/docs/en/about-claude/model-deprecations | AI-Ops backing: Model change | see publisher | verified |
| S-AIO-17 | Deprecations | OpenAI Docs | current | https://developers.openai.com/api/docs/deprecations | AI-Ops backing: Model change | see publisher | verified |
| S-AIO-18 | Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift | Rabanser, Gunnemann, Lipton | 2018 | https://arxiv.org/abs/1810.11953 | AI-Ops backing: Model change | see publisher | verified |
| S-AIO-19 | A postmortem of three recent issues | Anthropic | 2025 | https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues | AI-Ops backing: Model change | see publisher | verified |
| S-AIO-20 | Semantic conventions for generative AI | OpenTelemetry | current | https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai | AI-Ops backing: Tracing and logs | see publisher | verified |
| S-AIO-21 | Observability primer | OpenTelemetry Docs | current | https://opentelemetry.io/docs/concepts/observability-primer/ | AI-Ops backing: Tracing and logs | see publisher | verified |
| S-AIO-22 | Observability Engineering | Majors, Fong-Jones, Miranda | 2022 | https://openlibrary.org/search.json?title=Observability+Engineering&author=Charity+Majors | AI-Ops backing: Tracing and logs | see publisher | verified |
| S-AIO-23 | Monitoring Distributed Systems | Google SRE book | 2016 | https://sre.google/sre-book/monitoring-distributed-systems/ | AI-Ops backing: Operations | see publisher | verified |
| S-AIO-24 | Postmortem Culture | Google SRE book | 2016 | https://sre.google/sre-book/postmortem-culture/ | AI-Ops backing: Operations | see publisher | verified |
| S-AIO-25 | Service Level Objectives | Google SRE book | 2016 | https://sre.google/sre-book/service-level-objectives/ | AI-Ops backing: Operations | see publisher | verified |
| S-AIO-26 | Feature Toggles | Hodgson | 2017 | https://martinfowler.com/articles/feature-toggles.html | AI-Ops backing: Operations | see publisher | verified |
| S-AIO-27 | Semantic Versioning 2.0.0 | Preston-Werner | current | https://semver.org/ | AI-Ops backing: Operations | see publisher | verified |
| S-AIO-28 | Keep a Changelog 1.1.0 | Lacan | current | https://keepachangelog.com/en/1.1.0/ | AI-Ops backing: Operations | see publisher | verified |
| S-AIO-29 | Hidden Technical Debt in Machine Learning Systems | Sculley et al. | 2015 | https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html | AI-Ops backing: ML in production | see publisher | verified |
| S-AIO-30 | The ML Test Score | Breck et al. | 2017 | https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/ | AI-Ops backing: ML in production | see publisher | verified |
| S-AIO-31 | Rules of Machine Learning | Zinkevich | current | https://developers.google.com/machine-learning/guides/rules-of-ml | AI-Ops backing: ML in production | see publisher | verified |
| S-AIO-32 | AI Engineering | Huyen | 2024 | https://openlibrary.org/search.json?title=AI+Engineering&author=Chip+Huyen | AI-Ops backing: ML in production | see publisher | verified |
| S-AIO-33 | Building A Generative AI Platform | Huyen | 2024 | https://huyenchip.com/2024/07/25/genai-platform.html | AI-Ops backing: ML in production | see publisher | verified |
| S-AIO-34 | What We Learned from a Year of Building with LLMs (Part I) | Yan et al. | 2024 | https://www.oreilly.com/radar/what-we-learned-from-a-year-of-building-with-llms-part-i/ | AI-Ops backing: ML in production | see publisher | verified |
| S-AIO-35 | Usage and Cost API | Anthropic Docs | current | https://platform.claude.com/docs/en/build-with-claude/usage-cost-api | AI-Ops backing: Cost and quota | see publisher | verified |
| S-AIO-36 | Prompt caching | Anthropic Docs | current | https://platform.claude.com/docs/en/build-with-claude/prompt-caching | AI-Ops backing: Cost and quota | see publisher | verified |
| S-AIO-37 | Rate limits | Anthropic Docs | current | https://docs.anthropic.com/en/api/rate-limits | AI-Ops backing: Cost and quota | see publisher | verified |
| S-AIO-38 | FinOps Framework | FinOps Foundation | current | https://www.finops.org/framework/ | AI-Ops backing: Cost and quota | see publisher | verified |
| S-AIO-39 | unittest.mock | Python docs | current | https://docs.python.org/3/library/unittest.mock.html | AI-Ops backing: Testing | see publisher | verified |
| S-AIO-40 | Top 10 for LLM Applications | OWASP | current | https://genai.owasp.org/llm-top-10/ | AI-Ops backing: Risk | see publisher | verified |
