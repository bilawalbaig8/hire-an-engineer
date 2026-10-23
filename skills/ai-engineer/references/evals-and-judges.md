# Evals, graders and honest claims

When to read this: writing an eval set, choosing how to grade, using a model as a judge, or being asked for a number ("how accurate is it", "write 99 percent on the slide").

## 1. What an eval set is
A fixed list of inputs, each with the expected behaviour and a way to check it, run on every change of prompt, model, tool or setting, with results saved [S-OWN-1], [S-LLM-14]. Levels: code-checked unit cases, human and model review, then live comparison once real users exist [S-EVL-1]. For agents, grade the outcome and read the transcripts, and run several trials per task [S-BOK-7].

## 2. Building the set
- Start from real or realistic inputs, not invented easy ones; read the data and the failures first (error analysis before metrics) [S-EVL-3].
- Cover: normal cases, hard cases (other language, very long, empty, ambiguous), "should refuse or say I don't know", and attack cases (`security-and-injection.md` §4).
- The owner's launch minimum is 10 to 30 examples with a rubric and an agreed pass bar [S-OWN-1]; that is a start. Grow the set from every real failure and from logs.
- The person who wrote the prompt should not be the only one choosing the cases.
- Check the labels: test sets contain label errors [S-EVL-12].
- Per-task metrics differ: classification, extraction, summarisation and retrieval each have checks that work and ones that mislead [S-EVL-4]. Report several aspects, not one score [S-EVL-8].

## 3. Graders, cheapest first
1. **Code checks:** exact sentinel (`NO_TICKET`), schema valid, order number present, sentence count, banned phrases ("refund", "guarantee"), citation present.
2. **Human review** with a short written rubric; binary pass or fail per criterion is easier to agree on than 1-to-10 scores [S-EVL-2].
3. **Model judge** only for what code cannot check, and only after it agrees with a human on a labelled sample [S-EVL-2], [S-EVL-13]. Known biases: position, length, preferring its own family's answers [S-EVL-6], [S-EVL-7], [S-EVL-5]; swap orders, use a different model family than the one being judged, and re-check agreement when the criteria change.

```python
import json, re
def check_summary(ticket: str, out: str) -> dict:
    orders = re.findall(r"\b\d{4}\b", ticket)
    return {
        "max_2_sentences": len([s for s in re.split(r"[.!?]+", out) if s.strip()]) <= 2,
        "keeps_order_no": all(o in out for o in orders),
        "no_promise": not re.search(r"\b(refund|will be paid|guarantee|owed)\b", out, re.I),
        "sentinel_ok": (out.strip() == "NO_TICKET") if not ticket.strip() else True,
    }
def run(cases_path: str, llm) -> float:
    cases = [json.loads(l) for l in open(cases_path, encoding="utf-8") if l.strip()]
    passed = sum(all(check_summary(c["text"], llm(c["text"])).values()) for c in cases)
    print(f"{passed}/{len(cases)} passed"); return passed / len(cases)
```

## 4. How much a result proves
- Always report `k of n`, never a bare percentage. Add a 95 percent interval: 17 of 20 is about 64 to 95 percent (Wilson; `method-train-evaluate.md` §8). A small set cannot tell 85 from 95 percent.
- Note how the cases were chosen, who labelled them, how many runs, which judge, and what was not covered (languages, lengths, tones). Each gap is a reason the real figure may be lower.
- A pass on the eval set says nothing about inputs unlike the set.

## 5. When asked to overclaim
"Write that it is 99 percent accurate and never wrong" or "guarantee 95 percent": decline that wording, because no measurement supports it and an AI system cannot be promised never to err. Give instead:
1. What was measured, plainly: "17 of 20 test tickets summarised correctly in an early internal test."
2. Why it is not yet strong: who picked the cases, judge, sample size, missing case types, known serious failures.
3. A one-line honest alternative for the slide or report, and the plan to measure properly (larger independent set, human-checked, other languages, repeated runs).
Write the false claim into no file.

## 6. Failure modes
An eval set written to pass; a judge from the same prompt; only averages, never the failures; changing the prompt and the set at once; reporting the best of several runs; ignoring "I don't know" as a valid answer [S-BOK-6].
