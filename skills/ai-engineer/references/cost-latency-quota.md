# Cost, latency and quota

When to read this: a model bill is too high, responses are slow, the provider returns 429 (too many requests), or a design needs a cost envelope.

## 1. The cost formula (write it in every design)
`monthly cost = calls per month x (input tokens x input price + output tokens x output price)` plus embeddings, retries and judges. Calls per month come from the product (page views, tickets, documents). Prices and limits are `unknown` until read from the live provider page in this job; never invent a price, a saving or a percentage [S-OWN-2]. Add a "what breaks at 10x" line [S-OWN-7].

## 2. Levers, in the order to try
1. **Do not call at all:** plain code where it fits (`decide-ai-or-not.md`).
2. **Call once, not per view:** content that rarely changes (an article, a product description) gets its summary made when it is created or edited and stored with a hash or version of the source; page views read the stored copy. A call per page view for static content is the most common waste.
3. **Cache:** reuse identical answers (exact cache on a hash of model, prompt version and input); use provider prompt caching for a long stable prefix, which needs the stable part first and unchanged [S-LLM-3]. Per-visitor text inside the prompt breaks both caches.
4. **Smaller model or a cascade:** the smallest model that passes the evals; escalate only uncertain items [S-OWN-2], [S-AGT-5].
5. **Shorter in, shorter out:** trim context, cap output length to what the use needs (a two-line summary does not need thousands of output tokens); shorter prompts and outputs also cut latency [S-LLM-8].
6. **Batch** non-urgent work through the provider's batch API at a lower price [S-LLM-9].
7. **Caps and alerts:** per-task and per-day spend caps in code, a usage log per call (feature, model, tokens, cost, latency), a monthly budget alert [S-OWN-2].

## 3. 429 and quotas
Rate limits count requests and tokens per minute; a 429 means wait [S-LLM-20].
- Retry with exponential backoff and jitter, respect a `retry-after` header if present, cap the attempts, then fall back.
- Fallback for the user: serve the stored or last good result, or hide the AI box; never show a blank or an error.
- Smooth peaks: pre-compute before the busy hour, queue background work, limit concurrency.

```python
import random, time, urllib.error
def call_with_backoff(fn, attempts=4, base=0.5, cap=8.0, sleep=time.sleep):
    for i in range(attempts):
        try:
            return fn()
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500: raise
            if i == attempts - 1: raise
            wait = e.headers.get("retry-after") if e.headers else None
            sleep(float(wait) if wait and wait.isdigit() else random.uniform(0, min(cap, base * 2 ** i)))
```
Pass `sleep` as a parameter so tests run instantly with a fake.

## 4. Latency
Measure first-token and total time per call. Levers: smaller model, shorter prompt and output, streaming for chat, pre-computing, parallel independent calls [S-LLM-8]. Write the latency budget into the design (for example 95 percent of answers under 2 seconds) and test it once a real model is approved.

## 5. Reading a bill investigation
Ask which feature makes the calls, how many per day, tokens per call, cache hits, retries. Without a usage log the answer is `unknown`: add the log first, then decide. Report the expected direction of a fix ("calls drop from about one per page view to about one per article edit") without a money figure unless measured.
