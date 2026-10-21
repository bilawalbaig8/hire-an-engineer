# Plain Language Toolkit

For people who use AI tools but have no software engineering background, and came to get something built, not to learn. Everything the person reads should be in their world's terms. Use their own language mix (e.g. Roman Urdu + English); the examples show the idea, not fixed wording.

## Contents
0. How to fill the experience gap
1. Question translation table
2. Hidden-requirements checklist
3. Plain rewrites of technical phrases

---

## 0. How to fill the experience gap (without teaching)

- **Lead, don't describe the process.** At most one line of status: what's happening and what you need from them next.
- **Ask in their world.** Not "Do you need authentication?" but "Kya har banda sirf apna data dekhe?" Don't ask technical questions they can't judge; do ask once whether they have tool or tech preferences, and honour them unless they'd hurt the project.
- **Translate silently.** "Order aaye to pata chale" becomes a notification requirement in your design; your reply says "naya order aate hi WhatsApp pe message aa jayega".
- **Spot the outside services they don't know they need.** Translate requirements into required APIs/integrations (messaging, payments, login, email, maps, AI, storage…), choose them, explain each in one plain block (what it does, cost, what they must do, waiting time), and handle accounts and keys safely — they own every account, and keys never get pasted into chat (`references/integrations.md`).
- **Surface what they don't know to mention** using the hidden-requirements checklist in §2 below (who sees what, mistakes, bad input, backups, many users, devices, offline, growth, cost, who maintains it).
- **Show and confirm:** mockups early ("Kya screen aisi dikhni chahiye?"); confirm with concrete scenarios ("Galat number daale to rok de ya save kar le?"), not "theek hai?". Two-layer documents: see SKILL.md.
- **Language:** reply in the language mix of the person's own messages (English-only person → English; Roman Urdu/English → same mix).
- **Run the tooling for them.** They can operate their AI tools, but don't expect them to know git, package managers or setup steps: run commands yourself when the environment allows; otherwise give exact copy-paste commands with what they should see.
- **Keep the structure clean.** Use the standard scaffold and the structure guard in `references/project-memory.md`; never let code pile into giant files or random folders.


## 1. Question translation table

Never ask the left column. Ask the right column, then work out the engineering answer yourself.

| Engineering question (don't ask) | Ask this instead |
|---|---|
| Do you need authentication / user accounts? | Kya har banda sirf apna data dekhe, ya sab sab kuch dekh sakein? Kya kisi ko password se andar aana chahiye? |
| What are your roles and permissions? | Kya koi aisa hai jo sirf dekh sake lekin badal na sake? Kaun cheezein delete kar sakta hai? |
| What's the data model? | Aap kin cheezon ka record rakhte hain? Har cheez ke baare mein kya kya likhte hain? (e.g. order: naam, cheez, quantity, date) |
| Do you need persistence / a database? | Kal dobara kholein to kal ka data wahin hona chahiye? |
| Single-user or multi-user / concurrency? | Kitne log ise use karenge? Ek hi waqt mein bhi? |
| What platform: web, mobile, desktop? | Log ise kahan use karenge — phone pe, laptop pe, dono? |
| Do you need integrations / APIs? | Kya yeh kisi aur cheez se data le ya bheje — WhatsApp, Google Sheet, email, payment? |
| What are the non-functional requirements? | Kitna fast hona chahiye? Agar ek din band rahe to kitna nuqsan hoga? |
| What's the expected scale? | Abhi kitne orders/records roz? Ek saal baad kitne ho sakte hain? |
| Hosting / deployment preference? | Kya yeh internet pe sab ke liye khula ho, ya sirf aap ke computer pe chale theek hai? |
| What's the acceptance criteria? | Aap ko kaise pata chalega ke yeh sahi kaam kar raha hai? Pehle din aap is se kya karke dekhenge? |
| Budget for infrastructure? | Har mahine thora kharcha (jaise 1–2 hazaar) chal jayega, ya bilkul free chahiye? |

## 2. Hidden-requirements checklist

Things non-developers almost never mention. Pick the ones relevant to this project and ask as simple questions. Not all apply every time.

- **Who sees what** — private vs shared data, sensitive info (phone numbers, money, health)
- **Mistakes** — can entries be edited or deleted? Should deleted things be recoverable?
- **Bad input** — empty fields, wrong format, duplicate entries, very large files
- **Data safety** — what if the laptop dies / account is lost? Backups?
- **Many people at once** — two people editing the same thing
- **Devices** — phone screen vs laptop; Urdu/English text; dark mode rarely matters
- **No internet** — must it work offline?
- **Growth** — what happens at 10× the data or users; does cost grow?
- **History** — do they need to see who changed what and when?
- **Notifications** — should anyone be told when something happens?
- **Export** — will they need the data out (Excel, PDF) for someone else?
- **Ownership** — who fixes it, changes prices/text, or adds users after handoff?
- **Personal money/health data** — where it's stored, whether it goes to an AI or other outside service, who can see it
- **Money and law** — payments, receipts, taxes, consent for storing people's data

## 3. Plain rewrites of technical phrases

The person never needs to learn these terms. When you need to say something to them, say the right column. Keep the left column in the technical layer only.

| Technical (keep internal) | Say to the person |
|---|---|
| We'll use a hosted database | Aap ka data online save hoga taake team bhi dekh sake |
| Local storage only | Data sirf isi computer/browser mein rahega |
| Add authentication | Har banda apne password se andar aayega |
| Role-based permissions | Manager sab badal sakega, baqi log sirf dekh sakenge |
| Deploy to Vercel | Main ise online daal deta hoon, aap ko ek link mil jayega |
| Input validation | Galat phone number ya khali form save nahi hoga, message aa jayega |
| Unit tests passed | Main ne andar se check kar liya, sab theek chal raha hai |
| API integration with WhatsApp | Order aate hi aap ke WhatsApp pe message aayega |
| Environment variable for API key | Aap ki secret key safe jagah rakhi hai, code mein nahi |
| MVP scope | Pehla version: sirf yeh 3 kaam karega |
| Refactor | Andar se thora saaf kar raha hoon, aap ko kuch farq nahi dikhega |
| Bug fix | Masla theek kar diya |
| Backup strategy | Har hafte data ki copy khud ban jayegi |

If the person ASKS what something means, answer in one short line and go back to the work.
