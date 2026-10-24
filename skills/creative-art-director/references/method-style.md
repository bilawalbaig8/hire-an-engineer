# Method: Style (visual direction, style guide, palette, drift, prompt packs)

## 1. When to read this
"Give my game a look", a style guide, "is this palette OK", style tiles, "my icons all look different", a prompt pack for an image tool.

## 2. Steps
1. **Read first:** the brief, the chosen idea, the lessons files, and the game's style or brand guide if it has one (owner decision Q21). The guide wins; you refine it.
2. **No guide yet:** draft one, mark every line `draft`, and return it for the owner's approval.
3. **Direction (one page):** mood, shape language, palette, light, line, detail level, what is out of style, each choice with a reason. One page of direction plus a short guide with do and don't examples; never a long bible nobody reads.
4. **Palette:** measure contrast (section 3); mark failing pairs; suggest close colours that pass; note colour pairs that colour-blind players may confuse, labelled `inferred` unless a tool measured it.
5. **Open look:** offer two or three style tiles (text and colour values) and return the choice as `needs_approval`; do not pick alone. Explain each in plain words for an owner who is not an artist.
6. **Drifted set:** open every file, name the broken rule (outline weight, light direction, off-palette colour), add the rule to the guide, list a fix per file.
7. **Keep the guide up to date** after each job; a change to an approved line is an owner approval.
8. **Prompt packs** that follow the guide (section 4); any paid run stops for approval.

## 3. Contrast: measured or "not measured"
`contrast.py` is not built. To measure, read the contrast formula on the live W3C page (https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), write a small standard-library Python script in `docs/creative/scripts/`, run it on the palette values, and put the command and the output table in `evidence`. Reuse the script already in `docs/creative/scripts/` instead of writing a new one each job.

Known-answer check, before every use: compare the formula in the script with the live W3C page, then run the script on two pairs whose answer the formula fixes. White (`#FFFFFF`) on black (`#000000`) must give 21:1; any colour against itself must give 1:1. Put the check command and its output in `evidence`. If either answer is wrong, fix the script and run the check again, or write `contrast not measured`. No other expected number is written here; any threshold is read on the live page.

If it cannot run a script, write `contrast not measured` for every pair. Never state a ratio from memory or by eye. Colour-blind guidance to read live: https://jfly.uni-koeln.de/color/ (Okabe and Ito).

## 4. Prompt packs (for a person or the Artist to run)
No image or video tool is connected to this agent (not built), so it never generates art: it writes prompt packs for a person or the Artist; connecting the owner's tools, used only inside a credits budget the owner approves for each job, is a later build step (owner decision Q19).

Skeleton: `goal | tool (named by the owner) | prompt | reference images (with source and licence) | settings | negative list | tries allowed | cost formula: tries x price per try = estimate (price from the tool's live page, else unknown) | who runs it | approval id`

No living artist's name, no rival's character, no real person in any prompt. The run, the credits and every result line in the asset register wait for the owner's approval.

## 5. Skeletons
Style guide: `palette (hex values, role, contrast result or not measured) | shapes | line | light | detail level | do | don't | status (draft or approved) | date`

Style tile: `name | three words of mood | palette values | shape and line notes | type notes | what it gives up`

## 6. Where files go
`docs/creative/art-direction/` (direction, style guide, style tiles, prompt packs); helper scripts in `docs/creative/scripts/`. Never image files.

## 7. Done when
The direction and the guide exist in `docs/creative/art-direction/`; palette contrast is either measured by a script whose command and output are in `evidence`, or marked `not measured`; any open choice of look is returned to the owner.
