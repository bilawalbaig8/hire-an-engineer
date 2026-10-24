# Sources

Moved from section 15 of the design spec (`docs/superpowers/specs/2026-10-24-project-manager-design.md` in the source repo). Checked 2026-10-24: "verified" means the page, or its Open Library or arXiv record, was opened with WebFetch and the title matched. The checks covered title, author and year, not every claim inside each source. Only `verified` rows count as backing; S-PM-1 and S-PM-32 are unverified and are named only with that word. These IDs back the methods; they are never a source for a date, an effort number or a status claim about a project.

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-PM-1 | The Standard for Project Management and A Guide to the Project Management Body of Knowledge (PMBOK Guide), 7th ed. | PMI | 2021 | https://www.pmi.org/standards/pmbok | Planning, risk, tailoring to the project | not recorded | unverified |
| S-PM-2 | The 2020 Scrum Guide | Ken Schwaber, Jeff Sutherland | 2020 | https://scrumguides.org/scrum-guide.html | Goals per increment, retrospective as an event | not recorded | verified |
| S-PM-3 | The Kanban Guide | Coleman, Vacanti and others (Kanban Guides) | 2025 | https://kanbanguides.org/english/ | Visible flow, work in progress, blocked work | not recorded | verified |
| S-PM-4 | Shape Up: Stop Running in Circles and Ship Work that Matters | Ryan Singer (Basecamp) | not on page (book 2019) | https://basecamp.com/shapeup | Fixed time, variable scope; scope cutting | not recorded | verified |
| S-PM-5 | Shape Up, chapter 13: Show Progress | Ryan Singer (Basecamp) | not on page | https://basecamp.com/shapeup/3.4-chapter-13 | Status that shows unknowns, not task counts | not recorded | verified |
| S-PM-6 | NASA Work Breakdown Structure (WBS) Handbook, NASA/SP-2016-3404/REV1 | Stefanie M. Terrell (NASA) | 2018 | https://ntrs.nasa.gov/citations/20180000844 | Breakdown by product, WBS dictionary | not recorded | verified |
| S-PM-7 | GAO Schedule Assessment Guide: Best Practices for Project Schedules (GAO-16-89G) | U.S. GAO | 2015 | https://www.gao.gov/products/gao-16-89g | Dependencies, critical path, schedule health | not recorded | verified |
| S-PM-8 | Cost Estimating and Assessment Guide (GAO-20-195G) | U.S. GAO | 2020 | https://www.gao.gov/products/gao-20-195g | Estimates with ranges and documented basis | not recorded | verified |
| S-PM-9 | The Orange Book: Management of Risk | HM Treasury | page shows first published 2013 (the PBA check recorded the 2023 edition) | https://www.gov.uk/government/publications/orange-book | Risk register fields and owners | not recorded | verified |
| S-PM-10 | Performing a Project Premortem | Gary Klein (HBR) | 2007 | https://hbr.org/2007/09/performing-a-project-premortem | Seeding the risk register | not recorded | verified |
| S-PM-11 | How to Run Pre-Mortem Exercises | Atlassian Team Playbook | current | https://www.atlassian.com/team-playbook/plays/pre-mortem | A practical pre-mortem format | not recorded | verified |
| S-PM-12 | From Nobel Prize to Project Management: Getting Risks Right | Bent Flyvbjerg | arXiv record 2013 (paper 2006, not confirmed on the record) | https://arxiv.org/abs/1302.3642 | Reference-class forecasting; plans are too hopeful | preprint record | verified |
| S-PM-13 | Delusions of Success: How Optimism Undermines Executives' Decisions | Dan Lovallo, Daniel Kahneman (HBR) | 2003 | https://hbr.org/2003/07/delusions-of-success-how-optimism-undermines-executives-decisions | The planning fallacy and the outside view | not recorded | verified |
| S-PM-14 | Software Estimation: Demystifying the Black Art | Steve McConnell | 2006 | https://openlibrary.org/search.json?q=Software+Estimation+Demystifying+the+Black+Art | Ranges, not points; estimate vs. target vs. commitment | book (record checked) | verified |
| S-PM-15 | The Cone of Uncertainty | Construx (author not named on page) | n.d. | https://www.construx.com/books/the-cone-of-uncertainty/ | Estimates narrow only as decisions are made | not recorded | verified |
| S-PM-16 | Agile Estimating and Planning | Mike Cohn | 2005 | https://openlibrary.org/search.json?q=Agile+Estimating+and+Planning+Cohn | Release planning with ranges | book (record checked) | verified |
| S-PM-17 | Evidence Based Scheduling | Joel Spolsky | 2007 | https://www.joelonsoftware.com/2007/10/26/evidence-based-scheduling/ | Forecast from real past durations | not recorded | verified |
| S-PM-18 | Purpose Of Estimation | Martin Fowler | 2013 | https://martinfowler.com/bliki/PurposeOfEstimation.html | Estimate only when a decision needs it | not recorded | verified |
| S-PM-19 | How to Measure Anything | Douglas W. Hubbard | 2007 | https://openlibrary.org/search.json?q=How+to+Measure+Anything+Hubbard | Calibrated ranges, value of information | book (record checked) | verified |
| S-PM-20 | Actionable Agile Metrics for Predictability | Daniel S. Vacanti | 2015 | https://openlibrary.org/search.json?q=Actionable+Agile+Metrics+for+Predictability | Forecasting from flow data | book (record checked) | verified |
| S-PM-21 | Critical Chain | Eliyahu M. Goldratt | 1997 | https://openlibrary.org/search.json?q=Critical+Chain+Goldratt | One visible project buffer instead of hidden padding | book (record checked) | verified |
| S-PM-22 | The Goal | Eliyahu M. Goldratt, Jeff Cox | record 1986 (first edition 1984 not confirmed) | https://openlibrary.org/search.json?q=The+Goal+Goldratt | One constraint sets the pace | book (record checked) | verified |
| S-PM-23 | Waltzing With Bears: Managing Risk on Software Projects | Tom DeMarco, Tim Lister | 2003 | https://openlibrary.org/search.json?q=Waltzing+with+Bears | Risk management for software | book (record checked) | verified |
| S-PM-24 | The Mythical Man-Month | Frederick P. Brooks | record 1974 (first edition 1975 not confirmed) | https://openlibrary.org/search.json?q=The+Mythical+Man-Month | Communication cost; adding people late slows work | book (record checked) | verified |
| S-PM-25 | Reliable Product Launches at Scale (Site Reliability Engineering, ch. 27) | Google | 2017 (page) | https://sre.google/sre-book/reliable-product-launches/ | Launch checklists owned by a coordinator | not recorded | verified |
| S-PM-26 | The Checklist Manifesto | Atul Gawande | record 2010 (first edition 2009 not confirmed) | https://openlibrary.org/search.json?q=The+Checklist+Manifesto | Short checklists at decision points | book (record checked) | verified |
| S-PM-27 | DORA's software delivery performance metrics | DORA (Google Cloud) | current | https://dora.dev/guides/dora-metrics-four-keys/ | Delivery measures that do not need opinions | not recorded | verified |
| S-PM-28 | Postmortem Culture: Learning from Failure (Site Reliability Engineering, ch. 15) | Google | 2017 (page) | https://sre.google/sre-book/postmortem-culture/ | Blameless postmortems | not recorded | verified |
| S-PM-29 | Agile Retrospectives: Making Good Teams Great | Esther Derby, Diana Larsen | record 2012 (first edition 2006 not confirmed) | https://openlibrary.org/search.json?q=Agile+Retrospectives+Derby+Larsen | Retro structure: data, insights, actions | book (record checked) | verified |
| S-PM-30 | Project Retrospectives: A Handbook for Team Reviews | Norman L. Kerth | 2001 | https://openlibrary.org/search.json?q=Project+Retrospectives+Kerth | The prime directive; no blame | book (record checked) | verified |
| S-PM-31 | What each role does in a service team (delivery manager) | GOV.UK Service Manual | current | https://www.gov.uk/service-manual/the-team/delivery-manager | Delivery manager removes blockers, keeps the team's plan visible | not recorded | verified |
| S-PM-32 | Weeknotes and show and tells (plain status reporting) | GOV.UK Service Manual | n/a | https://www.gov.uk/service-manual/agile-delivery/writing-weeknotes | Plain status in short notes | not recorded | unverified |
| S-PM-33 | DACI: A Decision-Making Framework | Atlassian Team Playbook | current | https://www.atlassian.com/team-playbook/plays/daci | One driver, one approver per decision | not recorded | verified |
| S-PM-34 | Documenting Architecture Decisions | Michael Nygard | 2011 | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions | Short decision records with "superseded by" | not recorded | verified |
| S-PM-35 | Building Effective Agents | Anthropic (byline "Erik S.", Barry Zhang) | 2024 | https://www.anthropic.com/research/building-effective-agents | Keep agent workflows simple; scripts for deterministic steps | not recorded | verified |

35 sources: 33 verified, 2 unverified.

Notes:
- S-PM-1 is unverified because two pmi.org URLs returned 403 on 2026-10-24.
- S-PM-32 is unverified because no page was found: the URL above and `/service-manual/agile-delivery/running-a-show-and-tell` and `/service-manual/agile-delivery/show-and-tells` all returned 404, and search found no page. The URL is the first address tried, not a working page.
- The spec's table had no Cost/licence column. It was added here so the source checker can read the table: "book (record checked)" for Open Library records and "preprint record" for arXiv come from the kind of record checked; "not recorded" means cost and licence were not part of the check.
- Most sources were written for human teams and large projects; their ideas are adapted, not proven, for a small team of AI agents with one owner. No source gives a base rate for how long AI agent work takes; the role uses only this project's records and says how few runs a range rests on.
