# Method: Performance mode

## 1. When to read this
Stutter, slow start, memory, build or download size, or server response time must be measured against a budget; or a load test is asked for.

## 2. Steps
1. **Budget first.** Write the budget per target device before measuring: frame time, start time (cold, warm and hot measured apart), memory, size, response time. Take it from the owner's goals or the project's budget table; for budgets by platform class read `software-architect/references/game-performance-budgets.md`. Write it in `docs/qa/performance/`. No budget means "fast enough" cannot be said.
2. **Fix the conditions.** Same build, scene or journey, device, settings and warm-up each time. Default device floor: the owner's mid-range Android phone and a phone-size browser window; anything else is "not tested".
3. **Several runs.** Report the number of runs, the median, the slow end (75th, 95th or 99th percentile) and the worst frames, and frozen frames where the platform defines them. Never an average alone.
4. **Read the profiler capture** and point at where the time or memory goes. Do not change or optimise the code or the assets; the fix goes to the builder through the boss.
5. **Budget check.** Write or update a check that fails a run when a number goes over, in the folder the brief names.
6. **Before and after.** When a fix is checked, use the same conditions and enough runs; a small difference from two runs can be noise, so say it cannot show an improvement and run more.

## 3. Load tests
- Only against a separate test copy. By owner decision, no load test until a test copy exists; never on a live server. A server or URL is a test copy only when the brief names it as one (a test, preview or staging build the owner set up for testing); anything else is live, so ask the boss.
- Write the scenario and pass and fail limits before running.
- Anything near a live system, a paid load tool or a paid device is an approval relayed by the boss.

## 4. Files
The performance sheet: budget per device; measured numbers (runs, median, percentiles, worst frames), each marked measured in this session or taken from captures the owner gave (labelled so); before and after numbers; what was not measured.

## 5. Done (Performance)
The budget is written, the numbers come from runs made in this session (or labelled captures), with the device, the number of runs and the slow end shown.
