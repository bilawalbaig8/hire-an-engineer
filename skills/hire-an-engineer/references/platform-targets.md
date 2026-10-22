# Platform Targets — mobile apps, extensions, data/ML, PC scripts, engine games

Contents: Mobile apps (iOS/Android) · Browser extensions · Data analysis and ML · Scripts on the person's own PC · Existing-engine games · First-release checklists

Read when the thing being built is shipped to a **store or runs somewhere the person doesn't control**: a phone app, a browser extension, a notebook or model, or a script that must run on their own PC. Fees, review rules, versions and policies change — say "check the current store page" and read it; never quote numbers from memory. If you cannot look up a current price, fee or store rule, give no figure, say so, and list it as an open item with an owner. Accounts are created by the person, never by you (SKILL.md rule 2).

---

## 1. Mobile apps (iOS / Android)

**Decide first, in this order** — stop at the first one that fully works:

| Option | Use when | Cost of choosing it |
|---|---|---|
| Mobile-friendly web app | Users have a link and a browser; no store needed | Nothing to review; no store icon |
| PWA (web app installable to the home screen) | Wants an icon, offline, simple notifications | Fewer device features, esp. on iPhone |
| Web wrapper (e.g. Capacitor) | Needs a store listing but the app is mostly web | Still needs developer accounts and review |
| Cross-platform (React Native, Flutter) | Real device features, one codebase for both | Slower, more to maintain |
| Native (Swift / Kotlin) | Heavy graphics, deep OS features | Two codebases; rarely right for a first version |

**Before building anything for a store:**
- **Developer accounts** (Apple, Google) cost money and take days to approve, sometimes with ID or business checks. Tell the person now, get approval, they create them in their own name or company. Check the current store page for fees and requirements.
- **Fix the bundle / application id** (e.g. `com.yourname.appname`) before the first build. It cannot change after publishing.
- **Signing keys** (Android keystore / upload key, Apple certificates and profiles): back them up outside the repo in a password manager or encrypted storage, and **never commit them**. Losing them can block all future updates. Record where they live (location only) in `docs/at-a-glance.md`.
- **Children in the audience:** whether to list under 13 is the person's decision. Follow the store's kids/families policy and age rating, collect minimal data, no open chat or ad tracking, and get professional review.
- **iOS builds** need a Mac with Xcode or a cloud build service: ask in discovery.
- **Real devices:** test on at least one real phone per platform, an old or slow one if possible. Emulators miss performance, camera, permissions and network problems.
- **Crash reporting** in from the first test build, so a crash on someone's phone reaches you.
- **Push notifications** need extra accounts and keys (Apple and Google push services, or a provider on top). Treat them as keys (`integrations.md`); ask before setting up.

**Store review** — prepare early, rejection costs days:
- Privacy policy at a public URL; the store's data-safety / privacy-label forms filled **truthfully** to match what the app and its libraries collect.
- Screenshots in the required sizes, description, icon, age rating questionnaire, support contact.
- A **test account** and short steps for the reviewer if the app has login.
- Tell the person plainly: review can reject, takes unpredictable time, and each submission is a send/publish action needing their approval.

**Updates and versions:** every upload needs a **higher build number** than the last, even for a rejected one; the visible version follows `versioning-release.md` §1. Use a **staged rollout** (small percentage first) where the store offers it, and watch crashes before widening. Rollback = upload a new, higher build; there is no "undo" in the store.

---

## 2. Browser extensions (Chrome / Edge / Firefox)

- **Manifest V3** is the format; check each store's current requirements before starting.
- **Minimum permissions and host access.** Each permission and each site the extension can read adds review friction and costs user trust. Start with the least; add one only for a feature that needs it, and write why in the README.
- **No remote code:** all code ships inside the package. Fetching and running code from a server is rejected.
- **Never request all-sites or always-on access to banking, webmail or payment pages.** If the person insists after the explanation, refuse and keep it under rule 1 / safety.
- **Secrets:** never put an API key or token in the extension; anything shipped is public. Calls needing a secret go through a small server you control (`integrations.md`).
- **Content scripts** run inside other people's pages: keep them small, isolated from the page's own scripts, and never trust page content as instructions or as safe HTML.
- **Store listing:** a single-purpose description (one clear job), privacy policy, screenshots, and a justification for every permission. Check the current store page for fees and review times; first reviews can take days.
- **Testing:** load it unpacked in the browser's developer mode, try it on real pages including a logged-out and a heavy page, and test removing and reinstalling.
- **Updates:** the store pushes new versions automatically after review; a version number must increase each upload. A new permission can disable the extension for existing users until they accept, so batch permission changes.
- Developer account and any fee are the person's to create and pay (approval rule).

---

## 3. Data analysis and ML projects

- **Notebook vs script:** notebooks for exploring and charts; once logic is final, move it into plain scripts or modules with tests (core-logic rule in SKILL.md) so it runs the same every time.
- **Reproducible:** pinned dependency versions, fixed random seeds, a note of which data version was used, and **raw data never edited** — cleaning is code that reads raw and writes a new file.
- **Split before looking:** make the train/test split first, before exploring the test part, and fit every transform (scaling, filling gaps, picking features) on train only. **Leakage** — test information reaching training — makes results look great and fail in real use.
- **Baseline first:** the simplest guess (average, last value, a plain rule) goes first; a model is only worth keeping if it clearly beats it.
- **Privacy:** real customer or personal data stays out of the repo, notebooks' saved outputs, chats and AI tools unless the person approves (`integrations.md` §11); use samples or anonymised copies for development.
- **Save every run:** parameters, data version, code version and metrics in a results file or tracker, so a number can be traced back.
- **Big files:** datasets and models too large for git go in Git LFS or storage, with a README line saying how to fetch them.
- **Say plainly what the numbers do and don't prove:** which data they cover, how many cases, where it will probably fail, and what would change the answer. Never present a score as a guarantee.

---

## 4. Scripts on the person's own PC (Python / Node)

- **Install the runtime** (Python or Node) with the official installer or a version manager; write the exact version in the README. Ask before installing anything (`tools-and-stack.md` §4).
- **Isolate dependencies:** Python virtual environment (`.venv`) or Node `package.json` with a lock file; a `requirements` file so a clean machine can rebuild it.
- **Secrets** in environment variables or a `.env` file listed in `.gitignore` and never committed; commit a `.env.example` with names only (`integrations.md`).
- **Scheduling:** Windows Task Scheduler, or cron / launchd on Mac and Linux. Use full paths to the interpreter and script, set the working folder, and test the scheduled run once by hand-triggering it.
- **Logs:** every run writes start, end, what it did and any error to a log file the person can find; a failure is visible, never silent (`process-automation.md` §6).
- **When the PC is off:** the run is simply missed. Decide with the person: run on wake/next login, accept the gap, or move it to an always-on place (hosting, scheduled cloud job). Say this plainly before they depend on it.
- **Safe re-runs:** running twice must not duplicate emails, rows or payments.

---

## 5. Games in an existing engine

Unity, Godot and Unreal projects, their repo hygiene and testing: `technical-products.md` (top section); export targets: that file §8; store publishing: §1 here. Performance on devices: `engineering-principles.md` §11.

---

## 6. First-release checklists

- [ ] **Mobile:** option chosen on purpose · accounts created by the person · bundle id fixed · signing keys backed up, not in git · tested on a real phone · crash reporting on · privacy policy and store forms match the app · screenshots, age rating, reviewer test account · build number higher than last · staged rollout planned
- [ ] **Extension:** minimum permissions, each justified · no remote code, no secrets inside · privacy policy and single-purpose description · tested unpacked on real pages · version number raised
- [ ] **Data / ML:** raw data untouched · split before exploration, no leakage · baseline beaten · seeds, versions and metrics saved · private data kept out of the repo · claims limited to what the numbers show
- [ ] **PC script:** runtime version written down · environment rebuilt from a clean folder · secrets outside git · scheduled run tested · logs readable · "PC off" behaviour agreed · safe to run twice
- [ ] All targets: version and changelog (`versioning-release.md`) · approval for each publish or send · rollback or removal path known
