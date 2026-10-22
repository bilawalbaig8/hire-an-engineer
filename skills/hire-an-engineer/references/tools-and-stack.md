# Tools & Stack — choosing and setting up

---

## 1. The approach ladder

Stop at the **first** rung that fully meets the must-haves. Each rung up adds cost, setup and maintenance. (Automating an existing manual process? Use `process-automation.md` §5 instead.)

| Rung | Approach | Good when | Watch out |
|---|---|---|---|
| 0 | Existing product / no-code (Forms, Airtable, Notion, Glide, Zapier) | Common need, simple data | Monthly cost, limits, lock-in |
| 1 | Spreadsheet + formulas / Apps Script | Data already in sheets; internal | Messy past ~10k rows or complex logic |
| 2 | Single script (Python) | Batch jobs, files, reports | No UI unless added |
| 3 | Single HTML file | Small interactive tools, prototypes, no shared data | Data stays in one browser |
| 4 | Web app + hosted DB/auth (e.g. Supabase, Firebase) | Shared data, login | Keys, limits, access rules |
| 5 | Custom full stack | Real business logic, scale, integrations | Most effort to build and maintain |
| — | Native mobile | Deep phone features / store presence | Try a mobile-friendly web app first |

Deciding questions: shared data? needs a screen? login? money/personal data? who maintains it in 6 months? (nobody technical → stay low). Compare options on maintenance burden too (who patches it, ~hours/month). The brief states why an existing or no-code tool isn't enough; if it is enough, recommend it.

## 2. Tool categories

Decide per category: needed or not, which tool. List only what's needed.

| Category | Say it like this | Typical picks |
|---|---|---|
| Where it runs | Jahan software chalega | From the ladder above |
| Hosting | Internet pe link | Vercel, Netlify, GitHub Pages (free plans need a public repo, which exposes history and docs), tool's own hosting |
| Code & history | Har version safe | GitHub (private) — `github.md` |
| Data & backup | Data kahan, copy kaise | `database.md` |
| Tracking | Kya hua, kya baqi | GitHub Projects, Trello, Notion, Linear, Asana, sheet |
| Documents | Plans aur guides | `docs/` in repo (always) + their doc tool for sharing |
| Design | Screens kaisi dikhengi | HTML mockups, Figma, Canva |
| Notifications / automation | Khabar mile, kaam khud ho | Email, WhatsApp/Telegram, Slack, Zapier/Make — `integrations.md` |
| Payments / login | Only if needed | Proven providers — `integrations.md` |

## 3. How to choose

- Their stated preferences and what they already use or pay for come first, unless clearly harmful (then say why).
- Free tiers for v1; say when cost starts. Free plans change and often exclude commercial use (e.g. Vercel Hobby), backups or always-on running, and may pause inactive projects: check the provider's current pricing page and terms against how the person will use it.
- Popular, well-documented, few moving parts; one tool per job.
- Check current availability and pricing with a quick search when it affects the decision.
- Present a short table: Tool · Is ke liye · Kharcha · Pehle se hai? · Status — then confirm before setting up.

## 4. Setting up

- With available tools/connectors/terminal: do it yourself — repos, folders, sheets, boards, projects, config files.
- Approvals follow SKILL.md rule 2. Never type their passwords, payment or ID details — they do those steps, then you continue.
- Otherwise give exact steps (click-by-click only for tools they don't know), say what they should see, and verify each tool works before the next.

## 5. Tools register

Keep in `docs/ops/tools-setup.md`:

| Tool | Is ke liye | Kharcha | Account owner | Link | Status |
|---|---|---|---|---|---|

Never record passwords or key values — only where they're stored. Third-party APIs go in the integrations register (`integrations.md` §7); costs in `cost-management.md` §3.
