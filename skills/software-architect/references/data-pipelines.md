# Data and analytics pipelines

When to read this: data must be collected from several places, cleaned, stored and turned into reports, dashboards, features or models, in batches or in real time.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Start small | **One database or warehouse, a scheduled job that loads data, and a few well-defined reports** while volumes are modest. | A streaming system and a data lake only when a measured need (volume, freshness, variety) calls for it. [S-DATA-3] | Starting small gives up some flexibility and scale later; starting big gives up simplicity and money now. |
| Batch or streaming | **Batch** (run every hour or day) when decisions can wait; it is simpler, cheaper and easier to fix. | **Streaming** when results must be seconds fresh (fraud, live operations, live dashboards). Understand windows, late data and exactly-once limits first. [S-DATA-4] | Streaming gives up simplicity, easy re-runs and low cost for freshness. |
| Where raw data lands | **Keep an untouched copy of raw data first**, then clean and model it in later steps, so mistakes can be re-run. | Transform on the way in only for tiny, stable sources. | Keeping raw data gives up some storage cost; it buys the ability to fix and replay. |
| Storage layout | **A warehouse for analysis** and, only if you need files and machine-learning workloads alongside, one open storage layer that serves both (the lakehouse idea). (unverified source S-DATA-2 describes it) | Separate lake and warehouse for very large, mixed estates. | One layer gives up some best-of-breed features; two layers give up simplicity and add copying. |
| Who owns data | **A named owner for each dataset**, with a written meaning, freshness promise and contact; treat datasets that others rely on like products. [S-DATA-1] | Central ownership for small companies. | Ownership gives up a little speed of change for trust. |
| Data quality | **Check data at the edges**: schema, types, ranges, duplicates and freshness checks that stop or flag a bad load. | Spot checks for throwaway analysis. | Checks give up a little speed; bad data otherwise reaches decisions silently. |
| Orchestration | **A scheduler that retries, records every run and shows dependencies**; every step safe to re-run (idempotent). [S-DATA-3] | Cron and scripts for a handful of jobs, with logging. | A scheduler gives up simplicity of a script for visibility and recovery. |
| Personal data | **Collect only what is needed, mask or pseudonymise early, restrict access, and set a retention period.** | Keep identifiers only where a stated purpose requires them. | Less data gives up some analysis. |
| Modelling | **Model for the questions people ask** (clear facts and dimensions, one definition per metric, documented). | Wide raw tables for exploration, never for shared metrics. | Modelling gives up upfront time for consistent numbers. |
| Large multi-team estates | **Split by business domain with clear ownership and a shared platform** when many teams produce and consume data. [S-DATA-1] | Central team for smaller organisations. | Decentralised ownership gives up central control and needs strong standards. |

## Typical shapes

- **Operational database to warehouse, nightly:** copy changes, transform with SQL, publish a few tables and dashboards.
- **Event stream to warehouse:** applications emit events, a queue holds them, a loader writes them in micro-batches.
- **Raw, cleaned, modelled layers:** keep raw data, then a cleaned layer, then a layer modelled for reporting, each re-runnable from the previous one. [S-DATA-3]
- **Real-time path alongside batch:** a fast path for a few live numbers, the batch path remains the source of truth. [S-DATA-4]
- **Feature pipeline for machine learning:** the same definitions used for training and serving, checked for drift.

## Failure modes

- **Two definitions of one number:** different reports show different revenue.
- **Silent breakage:** a source changes a column and the pipeline keeps running with wrong data.
- **Late or duplicate events** double-count or miss records.
- **Pipelines you cannot re-run** safely or cheaply after a bug.
- **No owner:** nobody notices or fixes a dataset that everyone uses.
- **Personal data everywhere:** copied into many tables and exports with no retention rule.
- **Cost surprises** from scanning everything or keeping everything forever.

## Questions that change the design

- Which decisions will this data inform, and how fresh must it be for them?
- How much data per day now and in a year? From which systems, in which formats?
- Who owns each source, and what happens when a source changes?
- Is personal, financial or health data involved? Which retention and access rules apply?
- Who uses the output (people, dashboards, models, other systems)?

## Checks before you hand it back

- [ ] Each metric has one written definition and one owner.
- [ ] Raw data is kept, and every step can be re-run without side effects.
- [ ] Quality checks exist at each load and stop or flag bad data.
- [ ] The freshness promise for each dataset is written and monitored.
- [ ] Personal data is minimised, access is limited and retention is set.
- [ ] Cost is estimated, and the biggest cost driver is named.
- [ ] The first thing that breaks at 10 times the data is named.

## Sources
[S-DATA-1] [S-DATA-3] [S-DATA-4] and, as an unverified lead only, S-DATA-2
