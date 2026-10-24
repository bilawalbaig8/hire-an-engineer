# Resource limits: handles, memory, pools, timeouts and what the OS enforces

When to read this: Limits sub-mode, or any Fix where a resource (open files, memory, processes, threads, disk) is the problem. Read the limit and its source first; fix the program second; never change the OS limit yourself.

## 1. What to read first
| Resource | How to read the limit (no admin rights) | Source |
|---|---|---|
| Open files per process (Linux, macOS) | the shell's `ulimit -n`, or `getrlimit` from a small script | S-SE-28 |
| Open files per process (Windows) | the C runtime caps open file handles per process; read the runtime's documentation for the installed version | not checked here: say "inferred" |
| Memory | free memory from the OS or a small script; the process's own use from the runtime (`tracemalloc` for Python, S-SE-12) | S-SE-12 |
| Process and thread counts | `os.cpu_count()` and the pool's own setting | S-SE-31 |
| Limits on a group of processes | Windows job objects (S-SE-29); Linux cgroup v2 (S-SE-30) | read only |
Report the number, the command that read it and where it comes from. An unreadable limit is `unknown`.

## 2. Fix the program first
| Symptom | Likely cause to check | Fix |
|---|---|---|
| "too many open files" | files opened and never closed, one per item | open and close with the language's safe pattern (a `with` block in Python), reuse one handle, process files in batches |
| Memory grows over time | an unbounded cache, list or dict that only grows; a listener never removed | bound it (maximum size or expiry), clear it, or stream instead of keeping |
| Memory spike on big files | the whole file read at once | read in chunks or lines |
| Freezes the app | long work on the main thread | move it to a worker; report progress |
| Never finishes | a wait with no timeout | add a timeout and an error path |
| Zombie processes or temp files | no cleanup on error | clean up in a `finally` step; delete temp files you made |
| Disk fills | logs or generated data with no limit | rotate, cap size, delete after the run |
Each fix has a test that reproduces the problem inside the run limits (for example a generated folder with many small files) and a before and after number from the same method.

## 3. Pools and workers
Use the language's pool (S-SE-31) with a cap. Cap at half the logical cores by default. Waiting on disk or network does not need many workers. Shared counters and shared lists need a lock or a message pattern, tested with a total that must come out right. Concurrency is a named step-up to `opus`.

## 4. Never
Change an OS limit, power plan or job or cgroup setting; raise a limit "to see if it helps"; install a tool to read a limit. These are approvals, and the owner decides (the boss relays).

## 5. Cross-platform
Paths, line endings, limits and process rules differ between Windows, Linux and macOS. Test the paths you use with the OS the project targets; say which OS you ran on.
