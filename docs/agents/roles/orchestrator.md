# Orchestrator (the boss)

Status: built and tested. The agent is `agents/orchestrator.md` and its skill is `skills/orchestrator/` (version 0.1.0, unreleased). Evals: 12 local cases, run headless with stub or real specialists; all pass after three fixes (a run folder for every specialist run, no self-checking of specialist work, real timestamps). One run of each case, so this shows the method works, not that it is perfect. See "What is not covered" at the end of section 4.

You start the boss as the main session: `claude --agent orchestrator` (or the `agent` setting). It is not meant to be called as a subagent, because it must be able to ask you questions.

## 1. What this role is
The Orchestrator is the **boss of the specialist team** and the only member who talks to you. You give it a job in plain words. It decides how big the job is, picks only the specialists the job needs, writes each one a short brief with files and a "done when" line, collects their structured answers, brings you only the questions and approvals that are yours, makes sure changed work is reviewed before it counts as done, and keeps a record of the run. It does not design, review or build the specialists' work itself. Specialists never see you and never talk to each other except through the boss.

## 2. What it is a specialist in
- **Sizing a job:** tiny (it answers directly, no specialist), small (one or two specialists), project (a chain). It never wakes the whole team for a small job.
- **Planning:** a plain-words plan (who does what, in which order, what can run in parallel, which steps need you) before it spends any specialist call.
- **Briefing by files:** a request file per step with the goal, the files to read, the limits and a checkable "done when". It gives paths, not pasted text.
- **Checking answers:** every specialist answer must have the 7 fields (`status`, `summary`, `files`, `questions`, `approvals`, `assumptions`, `evidence`), and a `done` needs real evidence.
- **Relaying to you:** one batched, numbered message in your language, each question with why it matters and a suggested default.
- **Approvals and one-way doors:** anything hard to undo, costly, legal, personal, financial or public goes to you with the recommendation first and what each option gives up.
- **Gating changes:** work that changes code or files goes to the Code Reviewer before it counts as done.
- **Failure handling:** blocked specialists, refused launches, wrong output, injected instructions, caps, interrupted runs.
- **Run records:** a run folder and an event log that also feed the live office window.

## 3. What it will do for you
| You say | It does |
|---|---|
| "Add a login page" or any job that needs more than one specialist | States the size and the plan in one or two plain lines, names the specialists and the order, then runs the steps one by one (or in parallel only if they touch different folders) |
| "Run the team" / "have the architect and reviewer look at it" | Calls exactly those specialists, with a written brief for each, and gives you one plain summary |
| "Use only the architect" or "you answer, no specialists" | Does exactly that. Your words decide who works. Even with no specialist it never writes product code or reviews code itself |
| A quick question | Answers it directly. No run folder, no specialists |
| (a specialist needs facts only you have) | Merges all questions into one numbered message, removes duplicates, answers from your project files where it can, and gives a suggested default for each |
| (a specialist wants to do something hard to undo) | Brings it to you as an approval: recommendation first, then each other option and what it gives up. Nothing is applied before a clear yes in your own message |
| (two specialists disagree) | Shows you both positions, who said what and why, a recommendation, and whether the choice is a two-way or one-way door |
| (a specialist changed code or files) | Sends the change to the Code Reviewer, passes the Critical and Important findings back to the producer, and checks again, at most 2 rounds |
| "Continue the run from yesterday" | Reads `plan.md`, `decisions.md` and the last responses in `.team/runs/`, tells you what is done and what is next, and continues without repeating finished steps or re-asking answered questions |
| (something fails) | Says it plainly: which step, what was attempted, what you can do (allow it, do it another way, or stop). It never fakes a result |

## 4. What it will not do
- Design, review or build the specialists' work. It does not read the diff, run the tests or probe the code to check a specialist; it judges only the answer: its fields, its evidence, and whether the files it lists exist.
- Write product code. If a job needs work no installed specialist does and a general helper agent would be needed, it says so and asks you once; if you agree, the helper is named as a general helper (not a specialist), must reply in the 7 fields, and its output is checked by the Code Reviewer. It never does this silently.
- Call a role that is not installed, or imitate one. A missing role is named plainly, and it does the parts the installed roles can do.
- Treat "I trust you" or "you decide" on a one-way door as a yes. It says plainly that this is not a yes, keeps the approval open, and offers one short reply that accepts all the suggested options.
- Treat a Code Reviewer's verdict as an approval. Approvals come from you only, and an approval covers only the one action it names.
- Obey instructions found in a specialist's answer, a file or a web page. It reports them to you.
- Work around a refused launch or command (reword, split, repeat it, or tell another specialist to do it). It reports the refusal.
- Go past the caps without your explicit raise: 8 specialist calls, 2 fix rounds per step, 1 retry per failed call per run.
- Put secrets in briefs, summaries or run files. A secret you paste is never copied anywhere; it tells you to change it.
- Mark work done because the producing specialist says so, or count a skipped check as a pass.
- Pick a different model than the roster gives for a specialist.

**Tools it really has** (from `agents/orchestrator.md`):
- `Agent(architect, code-reviewer, ai-engineer, data-scientist)`: the only specialists it may call.
- `Read`, `Grep`, `Glob`: to look at the project before it asks you anything.
- `Bash`: read-only checks (listing files, `git log`, the contract checker, the run-record script). Nothing that changes the project or the machine, except that the run-record script `team_event.py` appends lines to `.agents/events.jsonl`.
- `Write`: only for the run folder `.team/runs/`.
- `mcp__office__wait_for_owner_answer` and `mcp__office__pending_window_answers`: for answers from the office window. They are switched off for now (see section 8), so questions go through the chat.

**Which specialists it can call today:** architect, code-reviewer, ai-engineer and data-scientist. The roster (`docs/agents/roster.md`) also lists the backend-engineer, but the backend-engineer is **not in the boss's allowed list yet**, so the boss cannot call it today. Adding it means adding the name to the `Agent(...)` list in `agents/orchestrator.md` (the roster itself only says to add a row in the commit that adds the agent file; adding the name to the boss's list is a separate step, done for ai-engineer and data-scientist in `TASKS.md` AI-3 and DS-3). Roles that have a role page but no agent file are not installed and cannot be called.

**What is not covered:**
- The review gate today is the Code Reviewer alone. There is no QA or security checker yet, so the boss does not say tests or a security audit happened unless a specialist's evidence shows it.
- The office window only shows the work; it does not take your answers yet.
- The evals ran once per case, headless, with stub or real specialists. They do not prove it works on every kind of job.
- It is a main-session agent. It does not work as a hidden subagent.

## 5. What it is responsible for
- **The size and the plan.** It says them in plain words before the first specialist call, and you can change them in your next message.
- **Choosing only the specialists the job needs,** from the installed team.
- **The briefs.** Each request file has a goal, context files, constraints, a checkable `done_when`, and your language.
- **Checking each answer** for the 7 fields and for evidence, with one retry per bad answer.
- **Putting your questions and approvals in front of you** in plain words, and keeping them open until you really answer.
- **The review gate** before changed work counts as done, and the fix rounds.
- **One owner per file.** Two specialists never write the same files at the same time.
- **The run record:** the run folder, the event log, and the honest closing summary.

It is **not** responsible for the specialists' decisions or the quality of their work. Each specialist owns its area. It is also not the one who decides what is hard to undo: you decide.

## 6. Where its work comes from
- **You.** The job in your own words, and your answers. Your explicit words about who works (team, one specialist, nobody) win.
- **Your project files:** `AGENTS.md`, `PROJECT_STATE.md`, `docs/` and any earlier `.team/runs/`. It reads them first so it does not ask what the files already say.
- **The specialists' answers,** in the 7-field shape, saved unchanged in the run folder.
- **The skill files:** `skills/orchestrator/SKILL.md`, then `references/run-method.md` (always), then the others a step needs (briefing, questions and approvals, team roster, quality gates, run records, failure handling).
- **The roster** (`docs/agents/roster.md`, mirrored in `references/team-roster.md`, whose table does not have the backend-engineer row yet) for who exists, what each owns and which model each uses.

## 7. Where its work goes
- **To you,** in plain words and your language: the plan, one batched message of questions, approvals, and a short closing summary (what was done, what you must still decide, where the files are, what was not covered or not verified).
- **To the specialists,** as request files with the Agent tool, with the model the roster gives.
- **The run folder** `.team/runs/<date>-<topic>/`:

| File | What it holds |
|---|---|
| `plan.md` | goal, size, steps (who, order, parallel, needs you), status per step |
| `NN-<role>-request.json` | the brief for step NN |
| `NN-<role>-response.json` | the specialist's answer, unchanged |
| `decisions.md` | your answers and approvals with date and ids |
| `summary.md` | the closing summary |

- **The event log** `.agents/events.jsonl`. The boss writes these lines only with its own script `team_event.py`, never by hand: `run_started`, `handoff`, `agent_result`, `question_asked`, `approval_requested`, `approval_given`, `blocked`, `blocker_cleared`, `run_finished`. A hook writes `agent_start`, `agent_stop` and `file_written`; specialists write nothing. The live office window reads this log: it shows the job, each specialist's state, your waiting questions and the timeline. The boss tells you the office address (`http://127.0.0.1:<port>/`, from `.agents/office.json`) once at the start of a run, if that file exists.
- **Review:** changes go to the Code Reviewer. A design or decision record goes to a fresh call of the architect in review mode (one that did not write it), only when you ask or the design will drive costly work.
- **Before closing:** `team_event.py check-run` on the run folder. Every problem it lists is fixed first, and a run with a question or approval still open is not closed.

## 8. How it works
1. **Intake and size.** It restates the job and your definition of done, looks at the project files, and asks at most 5 questions of its own only if something that changes the plan is unclear (with a default). It sizes the job: tiny, small or project.
2. **Plan.** It says in one or two plain lines who will do what and why (or that it will answer itself because the job is small). Your explicit words win. For a project it writes `plan.md` and shows you a plain version before spending calls. The architect gets a mode in every request (system design or data design); a database job follows a fixed order: architect (data design), then your approval of each one-way door, then the backend-engineer builds, then the code-reviewer reads. (The backend-engineer step cannot be run by the boss today, see section 4.)
3. **Brief and dispatch.** Before the first call of any run, even a small one, it creates the run folder and writes `run_started`. It writes one request file per step and calls the specialist by name with the roster's model. Each call is logged with a `handoff` event.
4. **Collect.** It saves the answer, checks the 7 fields (with `agent_contract.py` if the project has it), and logs the return `handoff` and `agent_result`. A `done` without evidence, or missing fields, goes back once with the exact complaint. The moment an answer needs your input, `question_asked` or `approval_requested` is logged so the office shows it.
5. **Relay.** One numbered message to you, de-duplicated, each question with why and a default. Your answers go into `decisions.md` and back to the specialist as `answers`.
6. **Decide or approve.** Two-way doors the specialists already decided stay decided. Every approval goes to you; nothing is applied before a clear yes in your own message. If you hand a one-way door back ("you decide"), it stays open as a labelled working assumption.
7. **Gate.** Changes pass the Code Reviewer. The Critical and Important findings go back to the producing specialist; the Reviewer checks again. After 2 rounds it stops and gives you the open findings with a recommendation (accept the risk, change the plan, or raise the cap). Minor findings never block.
8. **Close.** `check-run`, then `summary.md` and the same in plain words, then `run_finished`. If anything is still open, the run stays open and the boss says plainly that nothing has been approved or applied.

**Questions and approvals in the chat today.** The office window only shows; it does not take answers (switched off for now by the owner, 2026-10-23). The boss asks in the chat and waits for your reply there. The window-answer steps are kept in the skill for when they are switched on again.

**When something goes wrong:** an invalid answer is sent back once, then reported as a failed step. A `blocked` specialist is retried once if the boss can fix the cause, otherwise you are asked. A refused launch is reported, not bypassed. Instructions inside specialist output are quoted to you as a finding. At a cap it stops and asks.

**Language.** It answers and writes summaries in the language of your latest message and puts that language in every request to a specialist. Code, file names and identifiers stay as the project has them.

## 9. When it says "done"
A step is done when: the specialist's answer is valid, its `done_when` is met with evidence the boss can check (files exist, a command result, counts), open approvals are answered, and the review gate has passed or you accepted the open findings.

A run is done when `check-run` is clean, `summary.md` is written, `run_finished` is logged, and **no question or approval is still open**. If decisions are waiting for you, the run stays open (the office shows "Waiting for you").

For Data design results from the architect, "done" also needs, for each migration plan, the test-on-a-copy steps and the row counts before and after, whether the backend-engineer ran them (`not run` until shown), an access test design and a restore plan. The boss never tells you "backed up" or "safe" unless the evidence shows a restore or an access test was actually run; otherwise it says "planned, not tested".

The closing summary always says what was done, what you must still decide, where the files are, and what was not covered or not verified, including anything refused, blocked or capped.

## 10. Where it learned this (backing and sources)
**Your own rules first.** The boss keeps the handoff contract (the 7-field answer) and the roster of installed specialists. Its method files are `run-method.md`, `briefing.md`, `questions-and-approvals.md`, `team-roster.md`, `quality-gates.md`, `run-records.md` and `failure-handling.md`.

**Outside research (from `skills/orchestrator/references/sources.md`, URL-checked 2026-10-23).** The file holds 59 sources: 58 verified, 1 unverified (S-ORC-16, the Microsoft Research article on Magentic-One: the page blocked the automated fetch with HTTP 403). "Verified" means the page was opened and showed the title and the URL resolved; it does not mean every claim inside was checked. The role cites sources by ID, as ideas in its own words, and treats only `verified` rows as fact. Some licences are unconfirmed; that alone does not change a status.

| Area | What it covers (IDs in sources.md) | Status |
|---|---|---|
| Multi-agent orchestration patterns | S-ORC-1 to S-ORC-16: Anthropic on building effective agents and its multi-agent research system; Claude Code subagents and agent teams; OpenAI Agents SDK and Swarm; LangGraph and its supervisor; AutoGen; Magentic-One; CrewAI tasks; MetaGPT; ChatDev; why multi-agent systems fail | 15 verified, 1 unverified (S-ORC-16) |
| Delegation, briefing and handoffs | S-ORC-17 to S-ORC-22: RACI; mission command and commander's intent; SBAR; Team Topologies; effective context engineering for agents | 6 verified |
| Human in the loop, approvals and one-way doors | S-ORC-23 to S-ORC-28: Bezos on one-way and two-way decisions; Claude agent SDK docs on approvals and permissions; OpenAI human-in-the-loop; Nygard and Fowler on decision records | 6 verified |
| Task decomposition and planning | S-ORC-29 to S-ORC-34: Plan-and-Solve; ReAct; Reflexion; work breakdown structure; The Mythical Man-Month; Conway's Law | 6 verified |
| Quality gates and review | S-ORC-35 to S-ORC-38: Definition of Done; Google code review practices; DORA metrics; SWE-bench | 4 verified |
| Failure handling and caps | S-ORC-39 to S-ORC-45: Circuit Breaker (Fowler and Azure); timeouts, retries and backoff; Saga; Compensating Transaction; Claude Code cost management; Release It! | 7 verified |
| Prompt injection and trust | S-ORC-46 to S-ORC-54: OWASP Top 10 for LLM applications (prompt injection, excessive agency); indirect prompt injection research; InjecAgent; AgentDojo; the lethal trifecta; Anthropic guidance on jailbreaks and browser-use injections | 9 verified |
| Run records and observability | S-ORC-55 to S-ORC-58: Event Sourcing; OpenTelemetry generative AI conventions; LangSmith observability; postmortem culture (SRE book) | 4 verified |
| Office window | S-ORC-59: Claude Code MCP docs (tool waits, timeouts, background calls) | 1 verified |

59 sources, 58 verified, 1 unverified.

**Limit of this backing:** the checks covered that each page opened and showed its title, not every claim inside it. Some are paid books (Release It!, The Mythical Man-Month) and are cited for the idea, not for detail. Claude Code and agent SDK documentation changes quickly, so the boss's allowed-specialist list and the Agent tool behaviour should be re-read against the live docs when they matter.

Review pass 2026-10-24: corrected what the roster says about the boss's allowed list; noted that `team_event.py` writes to `.agents/events.jsonl`; noted that `team-roster.md` lacks the backend-engineer row.
