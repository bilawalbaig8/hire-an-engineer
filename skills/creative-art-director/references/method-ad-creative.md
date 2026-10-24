# Method: Ad creative direction (concept sets for mobile game ad tests)

## 1. When to read this
"Plan the next ad test", ad concepts, hooks, "make 20 more like the winner", playable or video ad ideas. Read `honest-ads-and-rights.md` first.

## 2. Steps
1. **Read:** the game's real features (game description or the Game Designer's notes), the style or brand guide, past results as read by the Data Scientist & Analyst, and the UA & Growth Marketer's formats, platforms and limits, all passed on by the boss.
2. **Concept families:** three to five, with different hooks, each tied to something really in the game.
3. **Fixed and free:** for each concept, what must stay fixed and what may change, so the UA & Growth Marketer can build the variant table (one change at a time).
4. **For each concept:** the hypothesis ("what would we learn?"), formats, a sound-off read, the call to action idea, and a safe-zone note. Formats, sizes and safe zones come from the live platform page read today; never from memory. A size not read today is `unknown`.
5. **Honesty check:** the gameplay shown exists and is typical; no fake rewards; AI-made assets marked for the platform's AI label where the platform asks for one; children's flag written.
6. **Hand-off:** the set goes to the UA & Growth Marketer through the boss. Words, script and shot list go to the Writer. It never launches, spends or calls a winner.

## 3. Owned elsewhere
The UA & Growth Marketer owns the test plan, the test question and the variant table (owner decision Q3); the Data Scientist & Analyst says whether a result is real. "Concept B won" is not a fact until that reading exists: ask for it through the boss and plan the next set without the claim.

## 4. Traps
- "Make a fail ad with a puzzle that is not in the game": refuse the unrepresentative gameplay; offer an honest version, or a labelled dramatised scene as the owner's decision (`needs_approval`).
- "Generate 50 variants and launch them with a budget": write the prompt pack and the cost formula (an estimate); return generation and spend as approvals; no launch, no spend.
- Raw installs for two concepts with no reading: do not call a winner.

## 5. Skeleton
Concept family: `family | hook (tied to which real feature) | hypothesis | fixed | may change | formats (live page, date read) | sound-off read | call to action idea | safe-zone note | honesty check | flags`

Hand-off note for the UA & Growth Marketer: `concept families | hypotheses | what may vary | limits read (URL, date) | open approvals | what was not checked`

## 6. Where files go
`docs/creative/ads/` (concept sets, hand-off notes).

## 7. Done when
Concept families, a hypothesis per concept, the honesty check and the hand-off note exist in `docs/creative/ads/`, and the answer says what was not checked.
