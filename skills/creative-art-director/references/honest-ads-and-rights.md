# Shared: honest ads, rights and provenance (flags only, not legal advice)

## 1. When to read this
Ad creative direction mode, and any concept, brief, guide or review that shows gameplay, uses a reference or a third-party asset, or involves an AI tool.

## 2. Honest ads
- An ad shows only gameplay, rewards and features the game really has, and that are typical of what a player meets. Check against the game description or the Game Designer's notes through the boss; a feature marked "planned" is not in the game.
- A small "not actual gameplay" line does not make unrepresentative gameplay honest. UK regulators have ruled against game ads on this point (see the ASA rulings below).
- No fake rewards, fake reviews or made-up numbers in a concept.
- A dramatised scene (not real gameplay) is the owner's decision: return it as `needs_approval` with the honest option next to it, and label it "dramatised" in the concept.
- AI-made assets: note them for the platform's AI label where the platform asks for one; read the live page, do not remember the rule.

## 3. Rights (flag, never advise)
- Take the lesson from a rival's ad (the need, the type of hook), never its look, characters, music, slogans or logos.
- No living artist's style by name, no real person's likeness, no trademarked character. Describe the qualities wanted (soft shapes, warm light) as an original direction.
- A third-party asset (stock, font, music, a reference image someone wants to use in the final work) is `needs_approval` with its licence, or `unknown` with the reason.
- Never write "safe to use", "free to use" or "original" without a recorded licence and a note of what was checked.
- UK, US and EU rules are background only. Every flag ends "not legal advice; a lawyer decides".

## 4. Children: every time
The audience age is unknown unless the brief proves it (owner decision Q23). Flag children's rules in every answer and keep working; stop and return `needs_approval` only when children are known or likely to be targeted, or when a file holds personal data.

If the UA & Growth Marketer skill is installed, see its `ua-growth-marketer/references/policy-flags.md` section 4 for the checked children's pages. If it is not installed, EU, UK and US children's rules are flagged as `unknown` and a lawyer decides. EU children's rules: no verified page yet in either case; mark them `unknown`; a lawyer decides.

## 5. Asset register
One line per asset in `docs/creative/asset-register.md`; add lines, never rewrite earlier ones:

`file | made by (person or tool) | prompt or source | licence or terms | date | status (draft, approved, rejected) | who approved any spend | what was checked`

Write `unknown` with the reason when a field is not known (for example "stock image, no licence file given").

## 6. Live pages to re-read (checked to open on 2026-10-23; the claims inside were not all checked)
| Area | Page |
|---|---|
| UK ruling: unrepresentative game ads | https://www.asa.org.uk/rulings/plr-worldwide-sales-ltd-g20-1061644-plr-worldwide-sales-ltd.html |
| UK ruling: images not from gameplay | https://www.asa.org.uk/rulings/mutant-box-interactive-ltd-a17-368932.html |
| Google Ads misrepresentation policy | https://support.google.com/adspolicy/answer/6020955?hl=en |
| Google App campaign creative (includes AI labels in some regions) | https://support.google.com/google-ads/answer/6167158?hl=en |
| US Copyright Office, AI hub | https://www.copyright.gov/ai/ |
| US registration guidance for works with AI material | https://www.federalregister.gov/documents/2023/03/16/2023-05321/copyright-registration-guidance-works-containing-material-generated-by-artificial-intelligence |
| Steam: AI content | https://store.steampowered.com/news/group/4145017/view/3862463747997849618 |
| Google Play: AI-generated content | https://support.google.com/googleplay/android-developer/answer/13985936?hl=en |
| Content Credentials (C2PA) | https://c2pa.org/specifications/specifications/2.2/index.html |
| Creative Commons licences | https://creativecommons.org/share-your-work/cclicenses/ |

If a page cannot be read, the rule is `unknown`: say so and do not use a remembered rule.
