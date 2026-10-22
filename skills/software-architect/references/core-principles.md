# Core principles

When to read this: before any design or review, and whenever you have to justify a decision.

## 1. What architecture is for

Architecture is the set of decisions that are costly to change later. Spend your effort where undoing a choice would hurt (data formats, service boundaries, who owns the truth, security model). Decide quickly where a choice is cheap to reverse. [S-FND-1] [S-FND-4]

No architecture is best in general. Each one favours some qualities (speed, safety, cost, ease of change) over others. Your job is to find the best one for *this* project's priorities and to say plainly what it gives up. [S-FND-1] [S-FND-2] [S-FND-3]

## 2. Write qualities as scenarios you can test

"Fast" and "secure" cannot be tested. A scenario can. Use this shape:

> When **[who or what causes it]** does **[what]** in **[what situation]**, the system **[responds how]**, measured by **[number or yes/no check]**.

Worked examples:

| Kind | Scenario |
|---|---|
| Web | When 5,000 shoppers browse at the same time on a normal evening, a product page opens in under 2 seconds for 95% of requests, measured at the server. |
| Mobile | When a player has no network for 30 minutes, every action they take still works and is saved, and all of it syncs without losing or duplicating anything when the network returns. |
| Game | When 8 players are in one match on average phones, the game holds 30 frames per second and one player's lag never stops the others. |
| AI | When the model provider is down for an hour, customers still get a clear fallback answer within 5 seconds, and no request is charged twice. |

Each scenario becomes a design constraint and later a test or a monitored number. If you cannot give a measure, the scenario is not ready. [S-FND-3] [S-FND-15]

## 3. Two kinds of decisions: one-way and two-way doors

- **Two-way door** (easy to undo: a library, a folder layout, a UI framework behind a thin layer). Decide fast, write one line why, move on.
- **One-way door** (hard to undo: the main database or data format, the public API shape, splitting into services, an authentication model, a payment flow, anything that holds users' data). Slow down: compare options, write a decision record, and return it to the boss as an **approval**, never as a finished fact.

When unsure, treat it as one-way until you can say how you would undo it and what that would cost. You can often turn a one-way door into a two-way one by adding a small boundary (an interface, an export, a feature flag) so the choice can be swapped later. [S-FND-1] [S-FND-4]

## 4. Keep it proportionate

Choose the simplest shape that meets the scenarios, and name the trigger that would make you step up.

| Start with | Step up only when | What stepping up costs |
|---|---|---|
| One program, clean modules inside it (a modular monolith) | Several independent teams, or one part needs to scale or deploy on its own, and the domain boundaries are well understood [S-WEB-10] [S-WEB-6] | Network calls instead of function calls, partial failure, harder testing and debugging, more operations work |
| One database | A part has a measured need the database cannot meet (volume, access pattern, isolation) | Keeping copies consistent, more things to back up and secure |
| One AI call with good instructions | The steps are fixed and repeatable: use a fixed workflow. The steps cannot be known in advance: only then an agent [S-AI-1] | More cost and latency, errors that compound over many steps [S-AI-7], more to test and watch |
| Plain objects and components | Entity counts or frame budgets demand data-oriented or ECS layouts [S-GAME-3] | Harder to read, fewer tools, steeper learning |
| Server decides everything | Measured input lag is unacceptable | Prediction and correction code, cheating risks [S-GAME-14] |

Design for about 10 times today's size, not 1,000 times. Name what would break first at 10 times and how you would find out early.

## 5. Hide complexity, draw boundaries on the business

- Prefer modules with a small, simple surface that hide a lot inside ("deep" modules) over many shallow ones. [S-FND-5]
- Draw boundaries along the language of the business (orders, billing, inventory), not along technical layers only. Each boundary has one owner and one clear meaning for its words. [S-FND-6] [S-FND-7]
- Let dependencies point toward the stable, valuable core (business rules) and away from changeable details (frameworks, databases, screens). This is one strong school of thought; weigh it against keeping things simple. [S-FND-9] [S-FND-5]

## 6. Make the important rules checkable

A rule that only lives in a document will be broken. Where a rule matters (no screen code imports the database layer, no cycles between modules, response time stays under a limit), turn it into an automated check that runs with the tests. This is called a fitness function. [S-FND-4] Propose them; write them only when the owner asks.

## 7. Record why, not only what

Every significant decision gets a short record that a stranger can read in two minutes: the situation, the options you considered, the choice, and what follows from it, good and bad. [S-FND-13] [S-FND-14]

Rules for decision records (ADRs):
- Location and numbering: `docs/decisions/NNNN-short-title.md`. If the folder already exists, **continue its numbering and copy its format**. Never renumber, rewrite or reformat existing records.
- Status is one of `proposed`, `accepted`, `superseded by NNNN`. A one-way-door decision stays `proposed` until the owner approves it. [S-REC-14]
- A decision is changed by writing a new record that supersedes the old one. The old one stays, with only its status line updated.
- A decision you inferred from existing code (not made by you) is written as a record with `Status: inferred` and the evidence (files, commits) that supports it.
- Each record says what the decision gives up.

## 8. Say how sure you are

Every claim about an existing system carries one label:

| Label | You may use it when |
|---|---|
| `verified in code` | You read the code or ran something, and can name the file, line, command or output. |
| `inferred` | It follows from evidence but you did not see it directly (a naming pattern, a commit message, how a framework usually behaves). Say what the inference rests on. |
| `unknown` | You could not find out. Say what you would look at next. |

Never present a guess as a fact. Never list a component you did not find evidence for. "I did not find a cache" is a valid, useful finding.

## 9. Common traps

- **Resume-driven design:** choosing a technology because it is fashionable or because you want to use it.
- **Copying a giant company's architecture** for a team of five.
- **Microservices too early:** boundaries drawn before the domain is understood are expensive to fix. [S-WEB-10] [S-WEB-9]
- **Designing for 1,000 times the load** and paying for it in complexity today.
- **Hidden assumptions:** write each one down so someone can check it.
- **Skipping the trade-off:** "X is best" without what it gives up is an opinion, not a design.
- **Diagrams without decisions:** a picture that no decision record or scenario explains.

## Sources
[S-FND-1] [S-FND-2] [S-FND-3] [S-FND-4] [S-FND-5] [S-FND-6] [S-FND-7] [S-FND-9] [S-FND-13] [S-FND-14] [S-FND-15] [S-WEB-6] [S-WEB-9] [S-WEB-10] [S-AI-1] [S-AI-7] [S-GAME-3] [S-GAME-14] [S-REC-14]
