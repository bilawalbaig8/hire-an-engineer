# Performance and data

When to read this: when the change touches loops, queries, migrations, caches, network calls, files, large collections, per-frame or per-request code, or anything that runs often or on a lot of data.

## How to look

Performance findings need numbers or at least orders of magnitude. Ask:

1. **How often does this run?** (per request, per frame, per row, once at startup)
2. **How much data does it touch now, and at 10 times?**
3. **What does each step cost?** (a database or network call is thousands of times slower than a memory access. [S-PRF-3])
4. **What is the real bottleneck?** Do not guess; where it matters ask for a measurement (profile, query plan, timing). A structured way to look at a system's resources is to check utilization, saturation and errors (USE) for each. [S-PRF-2] [S-PRF-1]
5. **Is it on a hot path?** A slow startup step is Minor; the same code inside a request handler or a frame loop is Important. Keep the severity tied to how often and how much.

## Common problems

| Problem | What to look for | Typical fix |
|---|---|---|
| **N plus 1 queries** | A query (or an API call) inside a loop over rows. [S-DBS-7] [S-DBS-1] | One query with a join or an `IN` list; fetch related data in bulk. |
| **Unbounded work** | A list or query with no limit or paging; reading a whole file or table into memory; a loop whose count comes from user input. | Page, stream, cap, set a maximum. |
| **Missing or wrong index** | A new query that filters or sorts on a column with no index; a function on the column that defeats the index. [S-DBS-2] | Add the right index (and say what it costs on write). |
| **Work in the wrong place** | Slow or blocking work in a request handler, in the main thread, in an event loop or a UI thread. [S-LNG-12] | Move to a background job or an async call; cache the result. |
| **Repeated work** | The same expensive calculation or lookup done again and again; re-reading config or files each time. | Compute once, cache with an expiry. |
| **Caching problems** | A cache with no expiry or invalidation rule; a cache key that mixes users' data; caching something that must be fresh. | Define expiry and keys; check the owner of the data. |
| **Memory growth** | Collections that only grow, listeners never removed, large objects kept alive, loading everything to filter in memory. | Bound it, release it, filter in the database. |
| **Retry storms** | Retries with no wait, no limit, or all clients retrying at once. | Limits, growing waits with randomness. |
| **Per-frame cost (games and UIs)** | Allocation every frame (new lists, string building, closures), searching the whole scene each frame, `GetComponent` in a hot loop, creating and destroying objects without reuse. [S-UNI-1] [S-UNI-5] | Cache references, reuse buffers, pool objects, change on events not every frame. |
| **Web page cost** | Large unoptimised images, blocking scripts, layout shifts, long tasks. [S-PRF-5] [S-PRF-6] | Use the standard page-experience measures to judge it. |

## Data changes: transactions, migrations, schema

These are the places where a mistake loses data, so review them slowly.

- **Atomicity:** changes that must succeed together are in one transaction. Two separate commits are a finding. Know what isolation the database gives and what it does not; concurrent updates on the same rows can still conflict or deadlock. [S-DBS-3] [S-DBS-4]
- **Migrations:**
  - Destructive steps (dropping or renaming a column or table, changing a type, while the code still uses the old shape are Critical: the code and the schema must never disagree. Adding NOT NULL without a default is not destructive, but it fails on tables that have rows or breaks old code that omits the column. The safe path is usually in steps: add the new, copy data, switch the code, then remove the old later.
  - Long locks on large tables, backfilling millions of rows in one transaction, adding an index that blocks writes: ask how it will run in production.
  - Can it be undone? If not, say so. A migration that breaks running code is a defect; an intentional, correct data drop is an approval; when both exist, follow the migration rule in `review-method`.
  - There are catalogues of unsafe migration patterns (one is an unverified source, S-DBS-5); the project's own migration style guide, if any, applies. [S-DBS-6]
- **Schema design:** missing keys or constraints that the code relies on; storing money as floating point; storing lists in text columns; no unique constraint where the code assumes one.
- **Data quality and privacy:** new fields with personal data, retention, who can read them.

## Severity

- Data loss, a migration that breaks the running code, a query that will take the system down at expected size: **Critical**.
- Hot-path N plus 1, unbounded work, missing atomicity, no index on a frequent filter: **Important**.
- Cold-path inefficiency, small avoidable allocations: **Minor** (unless in a frame loop on weak devices).
Never call something slow without saying how often it runs and on how much data.

## Sources
[S-PRF-1] [S-PRF-2] [S-PRF-3] [S-PRF-5] [S-PRF-6] [S-DBS-1] [S-DBS-2] [S-DBS-3] [S-DBS-4] [S-DBS-6] [S-DBS-7] [S-LNG-12] [S-UNI-1] [S-UNI-5] and, as an unverified lead only, S-DBS-5
