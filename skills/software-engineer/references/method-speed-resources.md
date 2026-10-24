# Speed & Resources mode: Profile, Fix and Limits

When to read this: the request is about slow code, memory that grows, a script that uses too much disk, CPU or time, threads and workers, or limits (open files, memory caps, timeouts). The mode is called "Speed & Resources" so it is never mixed up with QA's Performance mode (QA measures and gates; you fix). The base rules are in `hire-an-engineer/references/engineering-principles.md` section 11; the measuring rules are in `measurement-rules.md`.

## Lane and reason check
- Code owner (`boundaries.md`): server code and queries go to the Backend & Integration Engineer; game code to the Game & Technical Engineer; UI to nobody yet; pipelines to the Data Engineer; machine sizes and cost to DevOps. "Measure only, no fix" goes to QA.
- Reason: tune only for a failing budget (brief, project or QA) or a measured problem. Otherwise answer "no change needed" with the number.

## Sub-modes
- **Profile:** find where the time or memory goes. No change to the code.
- **Fix:** one biggest measured cost, fixed, then measured again.
- **Limits:** resource management inside the program, and reading the hardware and OS limits that apply.

## Profile
1. Goal or budget in one sentence ("the report runs in under 2 minutes on this PC").
2. Machine block (`measurement-rules.md` section 3).
3. Baseline: same input, warm-up, at least 5 runs, median and spread.
4. Profile with a tool already installed: Python `cProfile` (S-SE-11) for time, `tracemalloc` (S-SE-12) for memory snapshots, Node `--cpu-prof` (S-SE-13). Read a flame graph the right way up (S-SE-9): wide means much time. No runtime found for a language (Go, Java, .NET, C++): "not run" with the exact command the owner can run. Do not install a profiler: it is an approval (S-SE-17 and S-SE-14 are named only as options).
5. For a resource problem check each resource for use, saturation and errors (the USE method, S-SE-8): CPU, memory, disk, network, handles. Say which one is the limit.
6. Name the single biggest cost, not the guess in the request. Say what share of the time it takes.
7. Write the measurement record (`templates.md` section 3).

## Fix
1. A failing test first: a behaviour test that keeps the result the same, plus a size test where data grows.
2. Fix that one biggest cost. One change per round, so the effect can be seen.
3. Tests stay green. Measure again with exactly the same method.
4. Compare with the rules: ranges that overlap mean "not shown to help"; a different method before and after means the comparison is refused.
5. Stop when the budget is met. Do not keep tuning.
6. Measurement record: before, after, method, machine block, "Measured on this machine only". `done` says "Code Reviewer review pending", and "QA re-measure pending" where QA has a budget (re-measure with QA's written method in `qa-test-engineer/references/method-performance.md`).
7. A change to a saved or exchanged file format made for speed is a one-way door: return it as an approval; the boss may step you up to `opus`.

## More threads or processes
- State first the part that cannot run in parallel (Amdahl, S-SE-27): if half the job is serial or waiting, more cores cannot make it more than twice as fast.
- Measure whether the work waits on disk or network. If it waits on one slow stage, more workers cannot speed that stage up. Threads help CPU-bound code little in some languages, and processes cost memory.
- Cap the workers (default at most half the logical cores; S-SE-31 for pools with a worker limit).
- Shared data needs protection: test that the total is right under the workers. Concurrency problems are a named step-up to `opus` (the boss decides).
- The owner's users may have far fewer cores than this PC: say so.

## Limits (resource management inside the program)
Open files and handles (close with the language's safe pattern), thread and process pools with a cap, timeouts on waits, memory caps and bounded caches, reading big files in chunks, cleanup of temporary files and processes. Details and OS limits in `resource-limits.md`.
- Never change an OS limit (open file limit, power plan, job or cgroup limits) to get a result: it is an approval, and usually not the fix. Read the limit, report it and its source, fix the program.
- A memory growth fix is shown flat over the same run length as the baseline, and claims nothing longer. A longer run is "still open".

## Run limits (always)
Every benchmark or stress run has a time limit (default 10 minutes) and a size limit (default 1 GB of generated data), runs in a scratch folder, caps workers, and cleans up. A run that would exceed them is an approval. Never run anything near a live service or real data.

## Unknown cause
"It gets slow after an hour" or "memory grows until it crashes" with no known cause is debugging a problem not yet understood: the boss may step this mode up to `opus`. Say what is measured and what is not; do not guess a cause and fix it.

## Done when
Baseline and after numbers from the same method, the machine block, "Measured on this machine only", the biggest cost named, tests green, nothing outside the named folders changed, what was not run listed, and the pending reviews named.
