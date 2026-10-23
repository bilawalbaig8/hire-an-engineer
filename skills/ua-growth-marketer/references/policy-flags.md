# Shared: policy flags and the live pages to re-read

## 1. When to read this
Every call. Each mode touches at least one store, platform, inbox or privacy rule.

## 2. How to use the table
- The table says which page to read, not what the rule says today. Rules change and differ by country: read the live page with WebFetch when a rule or limit matters, and write the URL and the date read next to it.
- If the page cannot be read, the rule is `unknown`: say so, do not use a remembered rule, and return `blocked` if the work depends on it.
- A page describes a platform's own rules; it is not legal advice and not proof that a tactic works.
- These URLs were checked to open (title matched) on 2026-10-23 or 2026-10-24 during the role research; the claims inside them were not all checked. A URL that no longer opens is reported, not guessed.

## 3. Pages to re-read
| Area | When it matters | Live page |
|---|---|---|
| Apple store listing | name, subtitle, screenshots, metadata | https://developer.apple.com/app-store/product-page/ and https://developer.apple.com/app-store/review/guidelines/ |
| Apple store tests | product page tests and custom product pages | https://developer.apple.com/app-store/product-page-optimization/ and https://developer.apple.com/app-store/custom-product-pages/ |
| Apple search | how people find apps | https://developer.apple.com/app-store/search/ |
| Apple ratings | asking for ratings, replying to reviews | https://developer.apple.com/app-store/ratings-and-reviews/ |
| Google Play listing | titles and listing text | https://support.google.com/googleplay/android-developer/answer/9898842 |
| Google Play tests | store listing experiments, custom store listings | https://support.google.com/googleplay/android-developer/answer/6227309 and https://support.google.com/googleplay/android-developer/answer/9867158 |
| Google Play ratings | no manipulation of ratings, reviews or installs | https://support.google.com/googleplay/android-developer/answer/9898684 |
| Ads in Play apps | ads shown inside the game | https://support.google.com/googleplay/android-developer/answer/9857753 |
| Children (Play) | apps and ads aimed at children | https://support.google.com/googleplay/android-developer/answer/9893335 |
| Google Ads | misleading claims | https://support.google.com/adspolicy/answer/6020955 |
| Meta ads | ad rules | https://transparency.meta.com/policies/ad-standards/ |
| TikTok ads | ad rules (the link opened the general policy index in the last check) | https://ads.tiktok.com/help/article/tiktok-advertising-policies-ad-creatives-landing-page |
| EU consent | consent for ads and measurement for EU users | https://www.google.com/about/company/user-consent-policy/ |
| iOS attribution | what can be measured, how late | https://developer.apple.com/documentation/storekit/skadnetwork, https://developer.apple.com/documentation/adattributionkit, https://developer.apple.com/documentation/apptrackingtransparency |
| SEO | basics, spam, people-first pages | https://developers.google.com/search/docs/fundamentals/seo-starter-guide, https://developers.google.com/search/docs/essentials/spam-policies, https://developers.google.com/search/docs/fundamentals/creating-helpful-content |
| Disclosure (US) | creators and endorsements | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers and https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking |
| Fake reviews and engagement (US) | reviews, testimonials, fake social indicators | https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers |
| Disclosure (UK) | labelling paid content | https://www.asa.org.uk/resource/influencers-guide.html |
| YouTube | paid promotion label | https://support.google.com/youtube/answer/154235 |
| Email (US) | commercial email rules | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business |
| Email (UK, EU) | consent for marketing email | https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/ and https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en |
| Inbox sender rules | authentication, spam rate, one-click unsubscribe | https://support.google.com/a/answer/81126, https://senders.yahooinc.com/best-practices/, https://www.rfc-editor.org/rfc/rfc8058 |
| Email (Canada) | anti-spam rules | https://crtc.gc.ca/eng/com500/faq500.htm (unverified: the site blocked the check; say "unverified") |
| Children (US, UK) | children's privacy | https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions and https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/ |
| PR | honesty and disclosure in PR | https://www.prsa.org/about/prsa-code-of-ethics |

## 4. Children: every time
The audience age is unknown unless the brief proves it (owner decision Q23). Flag children's rules in every answer and keep working; stop and return `needs_approval` only when children are known or likely to be targeted, or when a file holds personal data.

The flag line names the children's pages above (US and UK) and the store's family policies; a lawyer decides. EU children's rules: no verified page yet, a lawyer decides. Do not use a remembered EU rule; mark it `unknown`.

## 5. The flag line
Write each flag in `docs/marketing/flags.md`, one line each, never rewriting earlier lines:

`date | mode | what | rule and live page (URL, date read) | risk | status: open | not legal advice; a human or lawyer decides`

## 6. Refusals
When the brief asks for something a rule forbids (rewarded ratings, bought followers, hidden paid posts, fake gameplay, a bought list, ads aimed at children against the rules), refuse that item in one line, name the rule and its page, and offer the allowed way.
