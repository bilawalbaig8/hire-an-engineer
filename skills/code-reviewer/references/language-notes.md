# Language and ecosystem notes

When to read this: when the change is in one of these languages or touches SQL, an API, logging or a user interface. Short checklists of the traps reviewers most often meet. Items marked "general practice" come from experience, not from a cited source. Read only the part you need.

## Python
- **Mutable default arguments** (`def f(x, items=[])`) are shared between calls. [S-LNG-1] [S-LNG-3]
- **Late binding in closures:** lambdas or inner functions created in a loop all see the last loop value. [S-LNG-3]
- **Copy versus reference:** assigning a list or dict does not copy it; shallow copies share inner objects. [S-LNG-1]
- **Blocking calls inside async code** freeze the loop; coroutines never awaited are silently lost; exceptions in tasks can vanish. [S-LNG-4]
- **Broad `except:` and bare `pass`** hide failures; catch the specific error. (general practice)
- **Types:** if the project uses type hints, a change that adds `Any` or silences the checker needs a reason. [S-LNG-5]
- **Idioms and style:** follow the project's conventions; cite the style guides only for disputes. [S-LNG-2] [S-LNG-6]
- SQL built with f-strings or `%` is an injection risk (see `security-review`).

## JavaScript and TypeScript (and React)
- **Floating promises:** an async call whose result is neither awaited nor handled loses errors; a missing `return` in a promise chain breaks the chain. [S-LNG-8]
- **Strictness:** a change that loosens the TypeScript strict settings or adds `any`/`as` casts to silence errors hides bugs. [S-LNG-9] [S-LNG-10]
- **Silent errors** that strict mode would turn into exceptions (undeclared variables, accidental globals). [S-LNG-7]
- **Blocking the event loop:** synchronous file or crypto calls, huge JSON parsing, expensive regular expressions on request paths. [S-LNG-12]
- **Node security and dependencies:** request body size, prototype pollution, untrusted package scripts. [S-LNG-11]
- **React:** state derived in an effect that could be computed during render; event logic placed in effects; effects without cleanup or with fetch race conditions; lists keyed by array index when the list can change. [S-LNG-13] [S-LNG-14]
- `==` versus `===`, truthiness of `0` and empty strings, floating point money, date handling with the local time zone. (general practice)

## C# and .NET
- Follow the project's conventions and the framework design guidelines for public APIs: naming, exceptions, disposal. [S-LNG-15] [S-LNG-16]
- **Disposable resources** (streams, connections, HTTP clients) created without disposal or created per call; `async void` outside event handlers; blocking on `.Result`/`.Wait()` in async code; swallowed exceptions; shared mutable state across tasks. (general practice)

## Unity (C#)
- **Per-frame cost:** allocation in `Update` (new lists, string building, boxing), `Find`/`FindObjectsOfType`/`FindGameObjectsWithTag` and `GetComponent` in hot loops; cache references in `Awake` or `Start`. [S-UNI-1]
- **Pooling:** frequent `Instantiate`/`Destroy` should use a pool; Unity provides an object pool type and a profiler to measure. [S-UNI-5]
- **Destroyed objects:** a destroyed Unity object compares equal to null through Unity's custom equality, but the null-conditional (`?.`) and null-coalescing (`??`) operators bypass that check; code that keeps using an object after `Destroy` throws. Check references after destruction and on scene changes. [S-UNI-4]
- **Serialization:** serialized fields, public versus private, renamed fields losing data, nested types and collections have rules that surprise people. [S-UNI-3]
- **Update order, coroutines left running, event handlers not unsubscribed, physics in `Update` rather than `FixedUpdate`.** (general practice)
- You cannot compile or run Unity code here: say so, and label runtime claims `likely` or `needs-check`. A vendor performance guide exists (unverified source S-UNI-2).

## Java and Kotlin
- Equality and hashing (`equals` with `hashCode`), mutable objects as map keys, unchecked casts, resource handling with try-with-resources, `Optional` misuse. [S-LNG-17]
- **Concurrency:** shared mutable state, visibility, lock ordering, check-then-act; prefer the safe building blocks. [S-LNG-18]
- **Kotlin:** follow the official conventions; coroutines need structured scope and cancellation handling; do not swallow `CancellationException`; nullability escapes (`!!`). [S-LNG-19] [S-LNG-20]

## Go
- **Ignored errors** (`_ = f()`), errors returned but not checked; `defer` inside loops; goroutines with no way to stop (leaks); data races on shared maps; loop variable capture in goroutines (depends on version); `nil` interface values. [S-LNG-21] [S-LNG-22] [S-LNG-23]

## SQL and migrations
- Parameters, not string building; keys and constraints that the code relies on; indexes for new filters; transactions around multi-step changes; safe, stepwise migrations (see `performance-and-data`). [S-DBS-1] [S-DBS-2] [S-DBS-3] [S-DBS-6]

## APIs and public contracts
- Resource naming, error shape, paging, filtering, and versioning follow the project's guidelines or a recognised standard. [S-API-1] [S-API-2]
- A change that renames or removes a field, changes a type, or tightens validation breaks callers: that is a hard-to-undo concern; check versioning rules. [S-API-3]
- Being lenient in what you accept can hide errors and erode compatibility over time; be deliberate. [S-API-4]

## Errors and logging
- Errors carry enough context to act on and are not swallowed; logs are structured and contain no secrets or personal data; sensitive actions are logged. [S-LOG-1] [S-LOG-2] [S-LOG-3] [S-LOG-4]

## User interface changes (accessibility basics)
- Text alternatives for images, keyboard operation, visible focus, colour contrast, labels on form fields, not relying on colour alone. [S-ACC-1] [S-ACC-2]

## Sources
[S-LNG-1] [S-LNG-2] [S-LNG-3] [S-LNG-4] [S-LNG-5] [S-LNG-6] [S-LNG-7] [S-LNG-8] [S-LNG-9] [S-LNG-10] [S-LNG-11] [S-LNG-12] [S-LNG-13] [S-LNG-14] [S-LNG-15] [S-LNG-16] [S-LNG-17] [S-LNG-18] [S-LNG-19] [S-LNG-20] [S-LNG-21] [S-LNG-22] [S-LNG-23] [S-UNI-1] [S-UNI-3] [S-UNI-4] [S-UNI-5] [S-DBS-1] [S-DBS-2] [S-DBS-3] [S-DBS-6] [S-API-1] [S-API-2] [S-API-3] [S-API-4] [S-LOG-1] [S-LOG-2] [S-LOG-3] [S-LOG-4] [S-ACC-1] [S-ACC-2] and, as an unverified lead only, S-UNI-2
