# Reliability, observability and privacy

When to read this: designing the failure plan, logging and tracing, testing model code offline, or handling personal data around an AI feature.

## 1. Failure plan (every design has one)
| Failure | Plan |
|---|---|
| Timeout or provider down | timeout on every call; queue and retry later, backup model, or the human queue; never lose the item [S-OWN-1] |
| 429 or quota | backoff, cached result, smooth peaks (`cost-latency-quota.md` §3) |
| Output invalid (bad JSON, unknown label) | validate, retry once with the error, then `unsure` to a human |
| Low confidence or "I don't know" | the human queue or the honest "not found" answer |
| Refusal or unsafe output | do not show; log; human review |
| Attack text detected | do not follow; flag; continue safely |
| Model or provider change | pinned version; a change is a release: rerun evals first [S-OWN-1] |
| Spend cap hit | stop cleanly, alert, fall back to the non-AI path |

Keep the AI behind one small layer so a provider can be swapped [S-OWN-1]; around the model sit a gateway, guardrails, caches and observability [S-BOK-3]. ML systems accumulate hidden debt through entangled data and glue code; keep the AI part small and tested [S-TRN-2], [S-TRN-3].

## 2. Logs and traces
- Per call: time, feature, model and version, prompt version, tokens in and out, cost, latency, outcome (ok, retried, fallback), tool calls with results. Use the shared generative-AI tracing names so traces are comparable across tools [S-OPS-1].
- Error analysis needs reading real traces [S-EVL-3], yet the owner's rule is no sensitive content in logs [S-OWN-1]. Resolve it this way: log metadata always; log content only redacted, or a small sample kept for a short time with the owner's approval.
- Weekly review of failures, fallbacks, limit stops and human corrections; each real failure becomes an eval case.

## 3. Personal data
- Real customer or employee data goes to an AI service only with the owner's informed approval; otherwise use synthetic samples or anonymised copies [S-OWN-5]. As a specialist you need that approval relayed by the boss.
- Minimise: send only the fields the task needs; strip names, emails, phones, ID numbers, card digits, addresses before the call and before logging.
- Data leaving the company needs a provider agreement (retention, training use, region) chosen by the owner; this is a one-way door for trust. Privacy law is orientation only, not legal advice: UK regulator guidance on AI and data protection [S-GOV-8]; the GDPR text (unverified here, S-GOV-7).
- Never copy personal data into your own outputs, summaries or test fixtures; refer to "row 11" or "the email in 0002.txt" instead.

```python
import re
PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "<EMAIL>"),
    (re.compile(r"\+?\d[\d\s-]{7,}\d"), "<PHONE>"),
    (re.compile(r"\b\d{5}-\d{7}-\d\b"), "<CNIC>"),
    (re.compile(r"\b(card|ends)\D{0,12}\d{4}\b", re.I), "<CARD>"),
]
def redact(text: str) -> str:
    for rx, tag in PATTERNS:
        text = rx.sub(tag, text)
    return text   # names and addresses need a list or a reviewer; regex misses them
```

## 4. Testing model code offline
- Unit tests never call a live model: pass a stub function, or patch the client with the standard library's mocks [S-OPS-2]. Recorded HTTP fixtures are another option when a library is already in the project [S-OPS-3].
- Test your own code's behaviour around the model (parsing, validation, routing, limits, fallbacks, attack handling) with fixed outputs; quality of the model itself belongs to the eval set, not the unit tests [S-BOK-8].
- Network calls in tests: patch `urllib.request.urlopen` (or the client) and assert it was not called with a real URL.

```python
import unittest
from unittest import mock
class NoNetwork(unittest.TestCase):
    def test_uses_cache_without_calling_model(self):
        with mock.patch("urllib.request.urlopen") as net:
            # call the code under test here
            net.assert_not_called()
```
