# Prompts and structured output

When to read this: writing or reviewing a prompt, asking a model for JSON, or turning model output into actions.

## 1. Success criteria before the prompt
Write what a good answer is, in checkable terms, before writing the prompt: format, length, required fields, what must never appear, what to do when unsure [S-LLM-4]. The prompt is then tuned against the eval set, never by impression.

## 2. Prompt checklist
- Clear task and audience in the first lines; the stable part first (it can be cached, `cost-latency-quota.md`).
- Explicit rules the eval will check (at most 2 sentences, keep the order number, reply in the ticket's language).
- A few varied examples, including an edge case; examples steer strongly, so keep them representative [S-LLM-1].
- Untrusted input placed inside clear markers (`<ticket>...</ticket>`) and described as data. This helps but is not a defence by itself (`security-and-injection.md`) [S-SEC-4].
- Permission to say "I don't know" or a fixed sentinel (`NO_TICKET`); training and grading that reward guessing produce confident wrong answers [S-BOK-6], [S-LLM-6].
- For answers from documents: answer only from the given documents and quote or cite them [S-LLM-6].
- Pin the model version where the provider allows it; a model change is a release, re-run the evals [S-OWN-1], [S-LLM-18].
- Asking the model to reason step by step can help multi-step tasks on large models; it costs tokens and is not a guarantee [S-AGT-1].

## 3. Structured output
- Ask for a schema-constrained object when the provider supports it (structured outputs, function or tool calling); plain "reply in JSON" can still break [S-LLM-12], [S-LLM-13], [S-LLM-19].
- Always validate in code anyway: parse, check types and allowed values, check required fields; on failure retry once with the error, then fall back (human queue or a safe default).
- Use enums for labels; include an `unsure` or `other` value so the model is not forced to guess.
- Never pass model output straight into SQL, a shell, a file path, an email recipient or a payment: code decides those from trusted data [S-OWN-3].

```python
import json
ALLOWED = {"billing", "bug", "how_to", "account", "other", "unsure"}
def parse_label(raw: str) -> str:
    try:
        obj = json.loads(raw)
        label = obj.get("label") if isinstance(obj, dict) else None
    except ValueError:
        label = None
    return label if label in ALLOWED else "unsure"   # unsure goes to the human queue
```

## 4. Prompt files in a project
Keep prompts as files (`prompts/<name>.txt`) with a short header: purpose, owner, model version tested, eval file, date. Changes go through the eval set like code changes go through tests.

## 5. Failure modes
- Fixing a bad case by adding one more rule to the prompt each time, until rules contradict; add the case to the eval set and look for the cause instead [S-EVL-3].
- Long prompts with the key fact in the middle: models use the start and end of a long context better [S-EVL-11].
- Testing a prompt on the five examples it was written from.
- Treating a fluent answer as a correct one.
