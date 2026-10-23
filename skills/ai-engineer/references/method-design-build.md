# Mode Design/Build: AI features, new or existing

When to read this: the request is to design, build, fix, harden or review an AI feature (a model call, a chatbot, RAG, a classifier, an agent, an eval set for a prompt). Training and model evaluation use `method-train-evaluate.md` instead.

## 1. Read and scope
1. Read the request, `AGENTS.md`, `PROJECT_STATE.md`, `README.md`, existing `docs/ai/`, and the files the request names. Note which folders you may write: always `docs/ai/`, plus only the folders the request names. "Design only, no code" means no code edits at all.
2. Do not open `.env`, key files or secret stores. Note that they exist; never print or copy a value. If a key is hard-coded in code you read, report it (first characters at most) and say it must be rotated by a human.
3. Personal data (names, phones, emails, ID numbers, card digits, addresses, health, family details):
   - If the project says files hold **real** people's data (customers, candidates, staff), do not open them without an approval relayed by the boss: you are an AI service too, so reading them sends them to one [S-OWN-5]. Work from the README, file names and sizes; name the kinds of personal data the project says are there (and the kinds such files usually hold, marked `inferred`); ask for approval or a redacted or synthetic copy.
   - If personal data turns up in files not marked real (samples, fixtures, test data), note the file and row, never copy the values into your outputs, and never send them anywhere.
4. Existing feature (a review, a bug, "it behaves strangely"): reproduce or trace first. Run the project's own offline code only when it uses a stub or mock model and no network; otherwise read and trace by hand. Write findings with file and line before fixing.

## 2. Ask only what changes the design
If you cannot tell **what task** the AI does, **who** uses it, **what data** it sees, **what an error costs** or the **budget**, return `needs_answers`: at most 5 questions, each with a `why` and a suggested default, and write no design files. Detail-level gaps become labelled assumptions instead.

## 3. Decide (see `decide-ai-or-not.md`)
State the verdict per feature, the baseline to beat, and why. Conflicting demands ("1 second, cheapest, 100 percent correct, data never leaves, the biggest model") are named one by one with what each option gives up; recommend one and return the one-way choice (for example where data may go) as an approval.

## 4. Design the shape
Write each part in one or two lines:
- **Shape:** single call, fixed workflow or agent; why not the simpler one.
- **Inputs and data:** what goes into the prompt, what is redacted, what may leave the company.
- **Prompt and output:** instructions, examples, a schema for structured output, validation in code (`prompts-and-structured-output.md`).
- **Knowledge:** retrieval over which documents, how stale versions are handled, citations, the "not found" answer (`retrieval-and-embeddings.md`).
- **Tools and authority:** each tool, read or write, who approves what, limits, kill switch (`tools-agents-and-approval.md`).
- **Attack surface:** where untrusted text enters, what it could make the system do, the structural defence (`security-and-injection.md`).
- **Cost and latency envelope:** formula with volumes and unknown prices (`cost-latency-quota.md`).
- **Failure plan:** what happens on timeout, 429, low confidence, refusal, bad output, provider change (`reliability-observability-privacy.md`).

## 5. Write the eval set (before or with the build)
Create `docs/ai/<topic>-evals.md` (and, when code is built, a runnable file such as `tests/test_<topic>_evals.py` or `evals/<topic>.jsonl`). Include normal cases, hard cases (other language, long, empty, ambiguous), cases where the right answer is "I don't know", and attack cases taken from the real data you read. Each case: input, expected behaviour, how it is checked (code check first, rubric second). See `evals-and-judges.md`.

## 6. Build (only when folders are named)
- Put the model behind one small function or class so tests can pass a stub (snippet below). No real client, no network, no key in tests.
- Prefer the standard library; adding a dependency is a question for the boss.
- Fixes for injection or unsafe actions are structural (code decides recipients, approvals, allowlists), not only prompt wording.
- Write tests that fail on the old behaviour and pass on the new. Run them (`python -m unittest discover -s tests -v` or the project's command) and copy the real result into `evidence`. If you could not run them, say so.

```python
# A seam for the model: production passes a real client later; tests pass a stub.
from typing import Callable
Model = Callable[[str], str]

def answer(question: str, passages: list[str], model: Model) -> str:
    context = "\n".join(f"<doc>{p}</doc>" for p in passages)
    return model(f"Answer only from the documents.\n{context}\n<question>{question}</question>")

def stub_model(prompt: str) -> str:   # deterministic, offline
    return "STUB ANSWER"
```

## 7. Files
- `docs/ai/<yyyy-mm-dd>-<topic>-design.md`: verdict, shape, data, prompt, tools and approvals, attack surface, cost formula, failure plan, what was not run, open decisions.
- `docs/ai/<topic>-evals.md`: the eval set and pass bar with its sample-size caveat.
- Code and tests only in the named folders.

## 8. Respond
- `done` only when the design file, the eval set and the failure plan exist (paths in `evidence`), plus test results when code was built.
- `needs_answers` for missing facts that change the design; `needs_approval` for real keys, real data, live paid calls, spend, autonomy over irreversible actions, data leaving the company, or anything legal (options, `recommended`, `one_way_door`). You may still deliver the offline parts in the same response.
- Summary: the answer first ("Do not use AI for 4 of the 7 items"), then the top 3 points, then what the owner must decide. Name what was not run (no live model call, so real accuracy is `unknown`).

Further reading for the whole mode: Huyen's book on building with foundation models [S-BOK-1], the practitioners' lessons from a year of building with LLMs [S-BOK-5], and the pattern catalogue (evals, RAG, caching, guardrails, defensive UX, feedback) [S-BOK-4].
