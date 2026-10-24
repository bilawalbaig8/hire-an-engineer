# Prioritise mode

## 1. When to read this
The request asks what comes first, what later, what not at all: "what should we build next", ranking a backlog, a roadmap, a new item mid-release, or "you decide, I trust you".

## 2. One scale
The board uses one scale only, from `hire-an-engineer/references/project-management.md` (section 4): **P0 Critical, P1 Must, P2 Should, P3 Could, Won't (now)**. Other methods are inputs to this scale, never a second scale on the board:
- **RICE** (reach, impact, confidence, effort; S-PBA-10) only when reach and effort exist as real inputs.
- **MoSCoW** words (S-PBA-11) are mapped: Must = P1, Should = P2, Could = P3, Won't = Won't (now).
- **Kano** (must-be, performance, attractive; S-PBA-12) only from real answers people gave, never guessed.
- **Cost of delay** (S-PBA-13) only when a date really matters (a season, an event, a contract the owner already signed).

## 3. Steps
1. **Name the goal** the order serves (the release goal), in the owner's words. No goal, no ranking: ask one question with a suggested default.
2. **Pick the lightest method the data supports.** Default: the P-scale with impact against effort, riskiest assumption first, what unblocks the most work, and a thin end-to-end version before polish (walking skeleton). Say which method you used and why.
3. **Mark every input** `sourced` (file, owner answer, data result, with where it came from) or `guessed` (yours or the owner's). Effort comes from the engineers or the Solution Architect through the boss; otherwise it is "owner's guess" or `unknown`. Never invent effort, reach or revenue numbers.
4. **Show sensitivity:** take the most uncertain input, change it to its likely low and high value, and list which items change place. If nothing moves, say so.
5. **Recommend** one order and say how sure you are.
6. **Return the decision.** The P1 list of a release, any change that drops something the owner promised, and anything for a client go back as `needs_approval` with options, a recommendation and what each option gives up. "I trust you, you decide" is not an approval; recommend and still return it.
7. **Record.** In `docs/product/backlog.md` every line is `draft` until the owner approves it; then `approved` with the date and where it was approved (the run folder or message the boss names). `docs/product/roadmap.md` shows releases as themes, never dates the owner has not approved.

## 4. Pressure the owner may add
- **"Tweak the scores so X comes first":** never change an input without a reason. Offer to record X as an owner decision ("P1 by owner decision, date") next to the unchanged scores.
- **A half-built favourite with low value in the data:** state the trade-off plainly (what is already spent does not change what the rest costs or brings), recommend on the evidence, leave the decision with the owner.
- **A new item mid-release (change request):** say what the item is worth and where it would rank. The time cost and what moves belong to the Project Manager (built, not tested); effort ranges come from the engineers through the boss, or the cost is marked `unknown`. The owner decides.

## 5. Done when
The ranked list exists with the method named, every input marked sourced or guessed, the sensitivity line written, the recommendation given, and the owner's decision returned as an approval. No line is marked `approved` without the owner's decision and its date.
