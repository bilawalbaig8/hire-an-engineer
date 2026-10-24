# Data structures and algorithms at design level

When to read this: Project structure mode, when a choice of data structure or algorithm matters for the design (a size, a frame or response budget, or a persisted format). Not for writing the code: the Software Engineer (role not built yet) writes it, measures it and reports back through the boss.

## 1. What the Architect does and does not do here
- **Does:** states the need, the size now and at 10 times, the operations and how often; names the simplest default and, if needed, the family or class that fits; says what it gives up; names what must be measured and the trigger to revisit. Writes this as a decision record.
- **Does not:** write the code, measure, tune (threads, memory pools, caches, I/O), or promise speed. A design can pick a cost class and state sizes; real speed is known only after someone measures on the target device. You cannot tell in advance where a program spends its time, so measure before tuning; fancy algorithms lose when n is small, and n is usually small [S-STR-26]. (Knuth's "premature optimization" warning, S-STR-25, is unverified: cite Pike instead.)

## 2. One data model per project
- **Stored data** stays in `docs/data/data-model.md` (Data design mode, `data-design.md`). This mode links to it and never writes a second one. If the project has stored data and no data design yet, do the Data design step in the same job.
- **Data that lives only in memory** (game state, a tool's pipeline, caches, queues of jobs) gets a short "core data" section in `docs/architecture/structure.md`: the main types, which folder owns them, how many there are (now and at 10 times).

## 3. When to write a record
Write a decision record only when the choice matters:
- the size is large or grows fast (thousands per frame, millions stored in memory),
- a budget is at stake (a frame budget from `game-performance-budgets.md`, a response-time scenario from `docs/architecture/scenarios.md`),
- or the data is persisted or crosses a boundary (save file, network message, file format, public API).
Otherwise the simple default is used without a record. Records multiply fast; keep them few.

## 4. The record: extra fields on top of the ADR template
Use the project's ADR format (`method-design.md`, or the project's own series) and add these fields:

| Field | What to write | Example |
|---|---|---|
| Need | The job in one sentence | Find enemies near the player every frame |
| Size | n now and at 10 times; memory per item, estimated | 500 now, 5,000 at 10 times; about 64 bytes each (estimate) |
| Operations | Which operations and how often | One query per enemy per frame; inserts on spawn |
| Simple default | The plainest structure that could work | Scan a list |
| Chosen family or class | Only if the default does not fit | Uniform grid (spatial hash) |
| Cost class | How cost grows with n, in words and notation | About O(k) per query (k = items in nearby cells) instead of O(n) |
| What it gives up | Memory, complexity, a parameter to tune | Memory for the grid; a cell size to tune |
| Measure (Software Engineer) | What to measure, where, and the number that would change the choice | Profiler on the owner's target phone; frame time of the query step |
| Revisit when | The trigger | n over 5,000, or the frame budget missed |

**Status rule.** An in-memory choice is a two-way door: record it as `accepted`. A persisted or public format (save file, network message, file format, public API) is a **one-way door**: the record stays `proposed`, goes back as an approval with `one_way_door: true`, and the format carries a version field (see `game-save-systems.md` for saves).

Every record says "not measured" until the Software Engineer reports a measurement through the boss; then the record gets the number and the date.

## 5. Families by need (start at the left)
The simple default is first in each row. Step right only when the size, the operations or a measurement says so. Families and their costs follow standard textbooks [S-STR-27].

| Need | Simple default | Step up to | Notes |
|---|---|---|---|
| Look up by key | hash map (the language's dict or map) | a sorted structure only if order is also needed | |
| Keep order, walk all items | list or array | | arrays of plain data when the profiler shows per-frame cost |
| Next by priority (timers, jobs, path search) | a sorted list for small n | binary heap (priority queue) | |
| Ranges over sorted keys | sort once, binary search | balanced tree, or the database index when inserts are many | for stored data, the index belongs to Data design |
| Membership | set | Bloom filter only after measurement, and only if false positives are acceptable | |
| First in, first out | queue | ring buffer for a fixed size | |
| Relations (maps, dependencies, social links) | graph as adjacency lists | breadth-first, depth-first, topological order, shortest path (Dijkstra, A*) | pick the search by the question asked |
| Space (nearest, in range, collisions) | brute force for small n | uniform grid, then a tree (quadtree, BVH), or the engine's physics queries | the engine's own queries first in a game |
| Many entities updated each frame | plain objects | arrays of plain data (data-oriented layout, ECS) only when the profiler shows the need [S-GAME-3] | harder to read; fewer tools |
| Text search over many documents | scan for small n | an index (the database's full-text search, or a search service) | stored data: Data design |

## 6. Algorithm classes (in this order)
1. **The library's sort and search.** Never hand-write a sort.
2. **Graph search** when the data is relations.
3. **Greedy** when a local best choice is provably good enough (say why).
4. **Dynamic programming** when sub-problems repeat.
5. **Incremental and streaming** when data arrives over time or does not fit in memory.
6. **Approximation** when an exact answer is too costly and "close" is acceptable (state the error the owner accepts).

Say the cost class in plain words for the owner: "doubles when the data doubles" (linear), "four times when the data doubles" (quadratic), "barely grows" (logarithmic).

## 7. Hand-off
- The record names the Software Engineer (role not built yet; the boss routes the hand-off) as the one who writes and measures. In engine projects the Game & Technical Engineer (not built yet) does it.
- The QA / Test Engineer's performance sheet holds the budgets; the Architect cites them, never changes them.
- When the Software Engineer reports a measurement or friction, the boss sends it back; the Architect updates the record (or writes a new one that supersedes it).

## 8. Traps
- A fancy structure for a small n (a skip list for 200 items).
- "Fast enough" with no size and no measurement.
- A second data model in `docs/architecture/structure.md` that drifts from `docs/data/`.
- A persisted format treated as a two-way door (a binary dump of classes as a save file).
- Promising frames per second or milliseconds that nobody measured.

## Sources
[S-STR-26] [S-STR-27] [S-GAME-3]. Knuth (S-STR-25) is unverified and used only as a lead.
