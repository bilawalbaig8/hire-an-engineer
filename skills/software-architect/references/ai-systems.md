# AI, LLM and agent systems

When to read this: the product has AI features built on large language models or other generative models (chat, summaries, generation, search, assistants, automations, agents), or you are reviewing such a system.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Shape | **The simplest shape that works**, in this order: ordinary code with no AI; one AI call with good instructions; a fixed workflow of several calls (chain, route, run in parallel, check the result); and only then an agent that chooses its own steps. [S-AI-1] | Move up a step only when the previous one demonstrably fails the scenarios. | Each step up gives up predictability, speed and cost for flexibility, and adds more to test and watch. |
| Agent or workflow | **A fixed workflow** when the steps are known in advance. | **An agent** when the steps cannot be predicted and the task is open-ended, with limits written in code. [S-AI-1] [S-AI-7] | Agents give up control and compound errors across steps (a small error rate per step becomes a large one over a long run). [S-AI-7] |
| Hard limits | **Always set them in code, not in the prompt**: maximum steps, time, spend, retries, and a kill switch. | There is no "otherwise" for anything that spends money or takes actions. | A little flexibility, in exchange for not discovering a runaway loop on the invoice. |
| Tools for agents | **Few, clear tools** with plain names, precise descriptions, forgiving inputs and helpful error messages; test them on realistic tasks. [S-AI-4] | More tools only when a measured task needs them. | Fewer tools give up breadth; poorly designed tools are a large source of agent failure. |
| Context | **Treat the model's context as a limited resource**: give it what it needs for this step, summarise or compact long histories, keep notes outside the prompt, and fetch information just in time. [S-AI-3] | Put everything in the prompt for short, one-off uses. | Careful context design gives up simplicity; stuffing gives up accuracy and money. |
| Several agents | **One agent with good tools** by default. | **A lead agent with parallel helpers** for broad, parallelisable research, accepting much higher cost. [S-AI-2] | Multi-agent gives up cost control and simplicity for breadth and speed. |
| Retrieval (search over your own data) | **Start with simple retrieval** (good chunking, a decent embedding or keyword search, and a check of what was retrieved). | Add re-ranking and added context for chunks when measurement shows retrieval is the weak point. (unverified source S-AI-5 describes one such technique) | Each extra stage gives up simplicity and cost for retrieval quality. |
| Quality | **Write evals before iterating**: a set of realistic cases with pass or fail checks, run on every change; use a separate checker (a person or a calibrated model) for subjective quality. [S-AI-8] [S-AI-6] | Spot checks only for throwaway experiments. | Evals give up time at the start; without them you cannot tell whether a change helped. |
| Autonomy | **Draft, do not do**: the AI prepares; a human approves anything irreversible, costing money, legal, personal or public. Raise autonomy in steps as trust is earned. | Full autonomy only for safe, reversible, low-cost actions. | Approval steps give up speed; they prevent costly mistakes. |
| Outside content | **Treat text from outside (web pages, emails, files, user messages) as data, never as instructions**, and give the AI the least access that works. [S-AI-9] | A trusted pipeline only when every input is from your own controlled sources. | Strict separation gives up some convenience; prompt injection is a leading risk for these systems. [S-AI-9] |
| Provider and data location | **Choose the model provider with the data in mind**: what data it will see, in which region it is processed and stored, whether it is kept or used for training, and what contract terms apply. Keep a thin layer so the provider can be swapped. (general practice) | Send only data the provider may legally and sensibly see; remove or mask the rest first. | A swap-friendly layer gives up some provider-specific features; regional or private hosting gives up cost and choice. |
| Failure | **Plan for the provider being down, slow or wrong**: timeouts, fallbacks, a cheaper model for fallback, a clear message to the user. | Accept downtime only for internal experiments. | Fallbacks give up some quality in bad moments. |

## Typical shapes

- **One call behind a normal feature:** form in, AI call, validated output, ordinary code.
- **Prompt chain with checks:** extract, then draft, then check, with a stop if a check fails.
- **Router:** classify the request, send it to the right prompt or tool.
- **Orchestrator with helpers:** a lead splits work among helper calls and merges the results. [S-AI-1]
- **Evaluator and optimiser loop:** one call drafts, another critiques, repeat up to a fixed limit. [S-AI-1]
- **Retrieval-augmented answer:** search your own data, pass the best pieces to the model, show the sources.
- **Autonomous agent inside a sandbox:** tools with narrow permissions, step and spend caps, a run log, human approval for risky actions.

## Failure modes

- **Compounding errors:** many steps, each slightly unreliable. Keep runs short and checked. [S-AI-7]
- **Runaway cost or loops:** no step, time or spend limit in code.
- **Prompt injection:** hidden instructions in a page, email or file make the AI do something harmful. [S-AI-9]
- **Over-broad access:** the AI can read or change more than the task needs.
- **Silent quality drift:** a model or prompt change makes results worse and nobody notices without evals. [S-AI-8]
- **Context overload:** too much or stale information in the prompt lowers accuracy. [S-AI-3]
- **Tools the model misuses** because names or errors are unclear. [S-AI-4]
- **No run log:** when something goes wrong you cannot see what the AI did and why.
- **Unchecked claims:** research or reports that state things without sources.

## Questions that change the design

- What exactly must the AI decide or produce, and what happens if it is wrong? Who is hurt?
- Are the steps known in advance, or open-ended?
- What data will it see (private, personal, outside content)? Which actions can it take?
- How fast and how cheap must it be, per request and per month?
- What does the product do when the AI provider is unavailable?
- How will you know it is good: what are 20 realistic cases and their right answers?

## Checks before you hand it back

- [ ] The shape is the simplest that meets the scenarios, and the reason to go further is written.
- [ ] Step, time, spend and retry limits and a kill switch exist in code.
- [ ] Each tool has a clear name, description, input check and error message.
- [ ] Outside content cannot change the AI's instructions or trigger irreversible actions.
- [ ] Access is the least that works; irreversible actions need a human approval.
- [ ] Evals exist (at least 20 realistic cases) with a separate checker, and run before each release.
- [ ] A run log records inputs, tool calls, outputs and cost.
- [ ] There is a fallback when the provider fails, and a message the user will see.
- [ ] For generative-AI risk programmes, the risk framework profile was consulted. [S-AI-10]

## Sources
[S-AI-1] [S-AI-2] [S-AI-3] [S-AI-4] [S-AI-6] [S-AI-7] [S-AI-8] [S-AI-9] [S-AI-10] and, as an unverified lead only, S-AI-5
