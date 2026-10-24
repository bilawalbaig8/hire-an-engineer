# Measurement rules: how a number is made and how it is reported

When to read this: before any before-and-after number, benchmark or "it is faster" sentence, in any mode. The same rules are used for a re-measure of QA's budget.

## 1. Rules
1. **Same method before and after:** same input, same warm-up, same number of runs, same tool, same machine, same other load as far as you can see it. A different method means the comparison is refused.
2. **Warm-up, then at least 5 runs** (default). One run proves nothing; setup details can change a result by more than the effect (S-SE-19), repeats and a statistical summary are needed (S-SE-20, S-SE-21), and some programs never reach a steady state (S-SE-22).
3. **Report the median and the spread** (minimum and maximum, or the interquartile range), never an average alone. Ranges that overlap mean "not shown to help": say so, do not claim a win.
4. **No "faster", "lighter" or "fixed" without numbers and the machine block.**
5. **Measured on this machine only** is repeated in every speed or resource answer. Numbers from this PC are not numbers for the owner's users.
6. **Do not tune the machine to make numbers look better.** Power plan, CPU pinning, system limits, drivers: no change (S-SE-16 is background on why runs are noisy). If the machine looks noisy, repeat the runs and say so.
7. **One change per round.**

## 2. Tools (built in only)
| Language | Time | Memory | Profile |
|---|---|---|---|
| Python | `timeit` (S-SE-15), `time.perf_counter` in a small script | `tracemalloc` (S-SE-12) | `cProfile` (S-SE-11) |
| Node.js | `performance.now`, a small script | heap snapshots by the runtime | `--cpu-prof` (S-SE-13) |
| Command line | a small script that runs the command N times and records wall time | the same script reading process memory where the OS allows | not available in the base role |
| Go, Java, .NET, C++ | not available on this PC at the time of the design; "not run" with the command the owner can run | | |
Installing hyperfine, pyperf, py-spy or a system recorder is an approval, one per tool (S-SE-17 and S-SE-14 are named only as options). There is no shared timing script yet; until one exists, write a small standard-library script in the scratch folder and keep its text in the measurement record.

## 3. The machine block
Put this in every measurement record and speed answer:
```
Machine: <CPU model>, <logical cores> logical cores, <RAM> GB, <OS and version>
Runtime: <language and version>   Power plan / other load: <value or unknown>
Measured on this machine only. Run: warm-up <n>, runs <n>, median <x> (min <a>, max <b>)
```
Read the values with commands that need no admin rights. A value that cannot be read is `unknown`, never guessed. Hybrid processors (fast and slow cores) add noise: say "inferred" if you only know it from the model number.

## 4. Run limits
Time limit per run (default 10 minutes), generated data limit (default 1 GB), scratch folder only, workers capped (default at most half the logical cores), clean up afterwards. Above that: an approval. Test data is generated with a fixed random seed and made up.

## 5. Reading a result
- Median before and after, then the change in plain words: "median 41.2 s before, 12.8 s after, ranges do not overlap".
- Overlapping ranges: "not shown to help".
- A gain on this PC is "relative change on this PC". For other machines, say what only a test on the target (the owner or QA) can show.
- Memory: the same run length before and after; "flat over N minutes" never means "flat for hours".
- Name what was not measured.
