# Method: Email / CRM (lifecycle messages, consent and sender checks)

## 1. When to read this
Welcome, first-week help, come-back (win-back), update and event messages; who gets them; consent, unsubscribe and sender checks.

## 2. Personal data first
Email lists are handled as counts and fields only. If a file holds real addresses or other personal data, stop before reading them further and return `needs_approval` (the consent basis and a redacted or counted export). Never use a bought, rented or scraped list.

## 3. Message plan
1. One goal per message and the audience rule (who gets it, who never gets it: people who opted out, accounts that may be children's).
2. The consent basis to confirm for each market (US, UK and EU rules in `policy-flags.md`; Canada unverified). The owner or a lawyer decides.
3. The one key message and the claims list; the Writer writes the words.
4. A send checklist for the person who sends: an honest sender and subject, an unsubscribe in every marketing message, the inbox providers' sender rules (authentication, low spam rate, one-click unsubscribe) read from their live pages with the date.
5. Sending code, the unsubscribe endpoint and list storage belong to the Backend & Integration Engineer.

Template: `Message | Goal | Audience rule | Consent basis to confirm | Key message | Claims | Send checklist | Who sends`

## 4. Where files go
`docs/marketing/email/` (message plans, audience rules, consent checklist); flags in `docs/marketing/flags.md`.

## 5. Traps
- "Email everyone in this CSV we bought from a partner": stop before reading the addresses, ask for approval and the consent basis, flag consent rules.
- "Subject 'Re: your order', no unsubscribe": fix both, list the sender rules for the person who sends.
- "Send it now to all players": plan and send checklist, `needs_approval` with `one_way_door: true`; never say "sent".

## 6. Done when
The plan is in `docs/marketing/email/`, the audience rule and consent basis to confirm are written, every message has an unsubscribe and an honest sender and subject in its brief, sender rules come from live pages with dates, and sending is returned as an approval.
