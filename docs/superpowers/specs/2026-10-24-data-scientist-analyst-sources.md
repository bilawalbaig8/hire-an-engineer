# Sources for the BI / Analytics / Growth modes of "Data Scientist & Analyst"

Checked 2026-10-23. Method: each URL was fetched and the page title compared with the source title. Books were checked in the Open Library catalogue, papers in Crossref.
Status words: **verified** = page opened and title words matched. **verified (catalogue)** = book or paper confirmed in a catalogue listing, not the full text. **unverified** = reason given.
"n.d." = living web page with no clear year on the page. Years are given only when a catalogue or page showed them.
Not repeated here (already used): Kohavi et al., Storytelling with Data, Wilke, Tidy Data, Great Expectations, Game Analytics (Springer), Fader and Hardie, Unity Analytics docs, GameAnalytics docs, NIST Privacy Framework, Sweeney k-anonymity.

## 1. Metric definitions (metric dictionary, KPI trees, North Star, metrics layer, governance)

| # | Title | Author / publisher | Year | URL | What it gives the role | Status |
|---|---|---|---|---|---|---|
| 1 | About MetricFlow | dbt Labs (dbt Developer Hub) | n.d. | https://docs.getdbt.com/docs/build/about-metricflow | How to define a metric once (measures, dimensions, time grain) so every report gives the same number | verified |
| 2 | dbt Semantic Layer | dbt Labs | n.d. | https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl | Explains the "one definition, many tools" idea in plain terms; a model for the metric dictionary | verified |
| 3 | LookML terms and concepts | Google Cloud (Looker docs) | n.d. | https://cloud.google.com/looker/docs/lookml-terms-and-concepts | Shows how a modelling layer fixes measure and dimension definitions in one place | verified |
| 4 | North Star Playbook | Amplitude | n.d. | https://amplitude.com/books/north-star | How to choose one North Star metric and the input metrics under it (basis for a KPI tree) | verified |
| 5 | Lean Analytics: Use Data to Build a Better Startup Faster | Alistair Croll, Benjamin Yoskovitz (O'Reilly) | 2013 | https://leananalyticsbook.com/ | "One Metric That Matters" and stage-based metric choice for small teams | verified (book site; Open Library confirms Croll, 2013) |

## 2. Tracking plans and event taxonomy

| # | Title | Author / publisher | Year | URL | What it gives the role | Status |
|---|---|---|---|---|---|---|
| 6 | Naming conventions: why you need them for clean data | Segment (Twilio) | n.d. | https://segment.com/academy/collecting-data/naming-conventions-for-clean-data/ | Rules for event and property names (case, tense, object-action) to put in a tracking plan | verified |
| 7 | Plan your taxonomy | Amplitude Docs | n.d. | https://amplitude.com/docs/data/data-planning-playbook | Step-by-step plan for events, properties and ownership before instrumenting | verified |
| 8 | Tracking Best Practices | Mixpanel Docs | n.d. | https://docs.mixpanel.com/docs/tracking-best-practices | What to track, naming, and what not to send (for example personal data) | verified |
| 9 | Introduction to structuring your data with schemas | Snowplow Documentation | n.d. | https://docs.snowplow.io/docs/fundamentals/schemas/ | Schema checks on every event, so bad events are caught at collection time | verified |

## 3. Dashboard and report design

| # | Title | Author / publisher | Year | URL | What it gives the role | Status |
|---|---|---|---|---|---|---|
| 10 | Information Dashboard Design | Stephen Few (Analytics Press) | 2006 | https://openlibrary.org/search?q=information+dashboard+design+few | Core rules: one screen, glanceable, right chart for the question | verified (catalogue; publisher site blocked by a bot check) |
| 11 | Show Me the Numbers | Stephen Few (Analytics Press) | 2004 | https://openlibrary.org/search?q=show+me+the+numbers+few | Table and chart choice for business reports | verified (catalogue) |
| 12 | The Visual Display of Quantitative Information | Edward R. Tufte (Graphics Press) | 1983 | https://openlibrary.org/search?q=visual+display+of+quantitative+information | Data-ink, chart junk and graphical integrity: why a dashboard should not mislead | verified (catalogue; publisher page returned 403) |
| 13 | Tips for Designing a Great Power BI Dashboard | Microsoft Learn | n.d. | https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips | Vendor checklist: audience, layout, few tiles, titles | verified |
| 14 | BI dashboard best practices | Metabase Learn | n.d. | https://www.metabase.com/learn/metabase-basics/querying-and-dashboards/dashboards/bi-dashboard-best-practices | Practical rules for small teams: one question per dashboard, filters, naming | verified |
| 15 | Best practice: Create a positive experience for Looker users | Google Cloud (Looker docs) | n.d. | https://cloud.google.com/looker/docs/best-practices/how-to-create-a-positive-experience-for-looker-users | Curated content, clear ownership and clean-up so dashboards do not decay | verified |
| 16 | Tableau Governance | Tableau Blueprint (Salesforce) | n.d. | https://help.tableau.com/current/blueprint/en-us/bp_governance.htm | Content ownership, certification and review cycle for reports | verified |

## 4. Product and growth analytics

| # | Title | Author / publisher | Year | URL | What it gives the role | Status |
|---|---|---|---|---|---|---|
| 17 | Startup Metrics for Pirates (AARRR) | Dave McClure (SlideShare) | 2007 | https://www.slideshare.net/dmc500hats/startup-metrics-for-pirates-long-version | The original AARRR funnel: acquisition, activation, retention, referral, revenue | verified (title matches; year from general knowledge, not shown on page) |
| 18 | New data shows losing 80% of mobile users is normal, and why the best apps do better | Andrew Chen (andrewchen.com) | n.d. | https://andrewchen.com/new-data-shows-why-losing-80-of-your-mobile-users-is-normal-and-that-the-best-apps-do-much-better/ | Shape of mobile retention curves and why a flattening curve is the goal | verified |
| 19 | Why Retention Is The Silent Killer | Reforge Blog | n.d. | https://www.reforge.com/blog/retention-engagement-growth-silent-killer | Retention first, then growth; how to read cohort curves | verified |
| 20 | What is good retention | Lenny Rachitsky (Lenny's Newsletter) | n.d. | https://www.lennysnewsletter.com/p/what-is-good-retention-issue-29 | Benchmarks by product type and how to judge "good" retention | verified |

## 5. Mobile and game growth analytics

| # | Title | Author / publisher | Year | URL | What it gives the role | Status |
|---|---|---|---|---|---|---|
| 21 | SKAdNetwork | Apple Developer Documentation | n.d. | https://developer.apple.com/documentation/storekit/skadnetwork | What iOS install attribution can and cannot report (limited, delayed, privacy-thresholded) | verified |
| 22 | AdAttributionKit | Apple Developer Documentation | n.d. | https://developer.apple.com/documentation/adattributionkit | Apple's newer attribution framework; keep notes in step with it | verified |
| 23 | Overview of Attribution Reporting API | Google Privacy Sandbox | n.d. | https://privacysandbox.google.com/private-advertising/attribution-reporting | Android and web attribution with privacy limits; why numbers differ by platform | verified |
| 24 | Measuring Ad Effectiveness Using Geo Experiments | Jon Vaver, Jim Koehler (Google Research) | 2011 | https://research.google/pubs/measuring-ad-effectiveness-using-geo-experiments/ | Method for incrementality by region; basis for honest "did the ads cause installs" answers | verified (title matches; year from general knowledge, not checked on page) |
| 25 | Conversion Lift Testing for Incrementality Measurement | Meta for Business | n.d. | https://www.facebook.com/business/measurement/conversion-lift | Vendor description of lift tests (test vs control) | verified |
| 26 | What is ROAS (return on ad spend) and how to measure it? | AppsFlyer Glossary | n.d. | https://www.appsflyer.com/glossary/roas/ | ROAS definition and cohort windows (D1, D7, D30) for payback talk | verified |
| 27 | What is LTV? How to calculate it and why it's important | AppsFlyer Glossary | n.d. | https://www.appsflyer.com/glossary/ltv/ | Simple LTV definition and link to CAC and payback | verified |
| 28 | View app statistics | Google Play Console Help | n.d. | https://support.google.com/googleplay/android-developer/answer/139628 | What Play Console itself reports (installs, retention) as a cross-check against other tools | verified |

## 6. Data trust for reporting

| # | Title | Author / publisher | Year | URL | What it gives the role | Status |
|---|---|---|---|---|---|---|
| 29 | Source freshness | dbt Labs (dbt Developer Hub) | n.d. | https://docs.getdbt.com/docs/deploy/source-freshness | How to state and check how fresh a source must be before a report is trusted | verified |
| 30 | Data discrepancies | Adjust Help Center | n.d. | https://help.adjust.com/en/article/data-discrepancies | Why attribution tool numbers differ from store and network numbers; a checklist for reconciling | verified |
| 31 | Data Contracts: The Complete Guide to Data Contract Standards, Tools & Best Practices | datacontract.com | n.d. | https://datacontract.com/ | What a data contract is (schema, owner, quality, freshness promises) | verified |
| 32 | Open Data Contract Standard | Bitol (Linux Foundation) | n.d. | https://bitol-io.github.io/open-data-contract-standard/ | Open spec for writing a contract file | unverified (page only returned a redirect stub, title "Redirecting") |
| 33 | Driving Data Quality with Data Contracts | Andrew Jones (Packt) | 2023 | https://openlibrary.org/search?q=driving+data+quality+with+data+contracts | Book on contracts between data producers and users | verified (catalogue; publisher page returned 403) |
| 34 | Anomaly detection: A survey | Chandola, Banerjee, Kumar (ACM Computing Surveys) | 2009 | https://doi.org/10.1145/1541880.1541882 | Standard survey of anomaly types and methods; basis for alerting on KPI drops | verified (catalogue, Crossref DOI record; ACM page returned 403) |
| 35 | Forecasting at Scale | Taylor, Letham (The American Statistician) | 2018 | https://doi.org/10.1080/00031305.2017.1380080 | The Prophet method: expected-range bands for daily KPIs with weekly and holiday effects | verified (catalogue, Crossref DOI record) |

35 sources, 34 verified, 1 unverified, checked 2026-10-23
