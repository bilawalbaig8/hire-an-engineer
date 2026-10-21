# Integrations & Third-Party APIs

The person won't know that their idea needs outside services, what an API or API key is, or how to get one. You discover the need, choose the service, get it set up safely, integrate it robustly, and keep it working. They only hear it in their terms: "WhatsApp pe message bhejne ke liye ek service ka account chahiye hoga."

---

## 1. Discover which APIs are needed

During Phases 1–4, translate every requirement that touches the outside world into a capability, silently:

| Person says | Capability | Typical service type |
|---|---|---|
| "Order aaye to WhatsApp pe pata chale" | Send messages | WhatsApp Business API provider, Telegram bot, SMS gateway |
| "Customers online pay karein" | Payments | Payment gateway (choose one that works in their country/currency) |
| "Login Google se ho" | Authentication | Auth provider / OAuth |
| "Email receipt jaye" | Transactional email | Email API |
| "Address se map dikhe / distance" | Maps & geocoding | Maps API |
| "AI se summary / jawab" | AI model | LLM API |
| "Sheet se data aaye / jaye" | Spreadsheet sync | Google Sheets API, connector |
| "Instagram/Facebook orders" | Social platform data | Platform's official API (often restricted) |
| "Photos upload" | File storage | Object storage |
| "Report PDF bane" | Document generation | Library or PDF API |
| "Ad network / analytics events" | Tracking | Analytics / attribution SDKs |

Also ask: does it **receive** data from outside (webhooks: payment confirmed, message received)? List every integration in the System Design Doc with a sequence diagram.

Prefer, in order: built-in features of tools already chosen (e.g. the database's auth) → a library that needs no external service → an official API → a reputable third-party aggregator → no-code automation (Zapier/Make) for simple, low-volume flows.

## 2. Research and choose

For each capability, compare 2–3 options with a quick web search (current docs and pricing — never rely on memory for these). Check:

| Criterion | Questions |
|---|---|
| Fit | Does it do exactly what's needed? Official or unofficial? |
| Availability | Works in the person's country, currency, language? Business verification needed? |
| Cost | Free tier, per-use pricing, monthly minimums; estimate monthly cost at expected volume |
| Limits | Rate limits, quotas, message/template rules, size limits |
| Approval & terms | Account review, business documents, content policies; is the intended use allowed by its terms? |
| Reliability | Status page, uptime history, support |
| Developer quality | Clear docs, official SDK, sandbox/test mode, webhooks |
| Data & privacy | What data is sent, where it's stored, compliance |
| Lock-in | How hard to switch later |

Never use unofficial/scraping workarounds that break a platform's terms (e.g. automating a personal WhatsApp account); explain the official route even if slower.

## 3. Explain it to the person

One short block per service, in their terms:

```
WhatsApp alerts ke liye: [Service]
Kya karega: naya order aate hi aap ko message
Kharcha: [free up to X / approx. Y per month at your volume]
Aap ko karna hoga: account banana + business verify (1–3 din lag sakte hain)
Alternative: email alert (free, foran) — WhatsApp approval tak isay use kar sakte hain
```

Flag early anything with waiting time (business verification, app review, payment gateway approval) — put it on the board as a person-owned task with a date, because it often becomes the critical path. Plan a temporary fallback so the build isn't blocked.

## 4. Accounts and keys — the safe way

- **The person owns every account**, in their/their business name. They create accounts themselves; you ask before suggesting any new account. Never enter their passwords, ID documents or payment details; guide them click by click (screenshots of what they'll see).
- **API keys are secrets.** Tell the person plainly: "Yeh key password jaisi hai — chat mein paste na karein."
  Instead, guide them to put it directly where the software reads it: hosting environment variables, GitHub Actions secrets, the database's secrets/vault, or a local `.env` file that is git-ignored. Give exact click paths.
- If a key does get pasted into chat, a doc or code: treat it as exposed — have them revoke/rotate it in the provider dashboard and create a new one.
- **Test vs live keys:** always start with sandbox/test keys; switch to live only at release, with approval.
- **Least scope:** create keys with only the permissions needed; separate keys per environment.
- Never write key values in documents — record only the key's name, where it's stored, who owns it, and when it was created/rotated.

## 5. Integration design

Build every integration so an outside failure never breaks the person's core work:
- **Adapter/wrapper module per service** (one place in code talks to it) — easy to test, mock and swap providers.
- **Server-side only** for secret keys; the browser never sees them.
- **Timeouts and retries** with backoff for temporary failures; give up gracefully.
- **Idempotency:** retries must not double-charge or double-send (use idempotency keys / check before acting).
- **Webhooks:** verify signatures, respond fast, process asynchronously, handle duplicates and out-of-order events.
- **Rate limits:** respect them; queue and throttle bulk sends.
- **Fallbacks:** if the service is down, queue and retry later, or fall back (e.g. email when WhatsApp fails); tell the user clearly in the UI.
- **Logging:** log each call's status, latency and errors (no sensitive content); AI calls also go to the AI usage log (`cost-management.md`).
- **Data minimisation:** send only the fields the service needs.

## 6. Testing integrations

- **Unit tests with mocks** of the adapter (success, failure, timeout, rate-limited, malformed response).
- **Integration tests against the sandbox** for the main flows.
- **Contract tests:** check real responses still match what the code expects; run in CI on a schedule to catch provider changes.
- **Webhook tests:** replay sample events, duplicates, bad signatures.
- **End-to-end on test environment** before release; one controlled live check after release, with approval, using owner-controlled test accounts/recipients only (e.g. a test message to the owner).

## 7. Integrations register

A table in the Tools & Setup Guide (and technical section), kept current:

| Service | Used for | Account owner | Plan / cost | Key name & where stored | Test/live | Limits | Status page | Docs | Last rotated |
|---|---|---|---|---|---|---|---|---|---|

## 8. Keeping integrations healthy

- Monitor failures and error rates; alert the person (in plain words) only when it affects their users or money.
- Watch provider announcements: deprecations, API version changes, price changes — plan updates as board tasks before deadlines.
- Rotate keys periodically and when anyone with access leaves.
- Re-check costs against the cost register each release.
- In the Handoff Guide: list of integrations, what each does, what to do if one stops working (step by step), and how to replace a key.
