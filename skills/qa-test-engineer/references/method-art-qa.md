# Method: Art QA mode (Gate, Spot check, Re-check)

## 1. When to read this
Finished art or creative files must be checked before they ship: icons, store screenshots, AI-generated images, ad images or videos, a set of variants.

## 2. Pick the sub-mode
- **Gate:** a whole set before release.
- **Spot check:** one file, one question.
- **Re-check:** a fixed file against the earlier notes, with both results side by side.
If unclear, ask one question with a suggested default (default: Gate).

## 3. Steps
1. Read the brief, the style guide, the asset register (source and licence) and the target platforms. Missing style guide or platform is a question.
2. Read each platform's current spec page today and write the limits into a check list in `docs/qa/art/`, with the page and the date for every limit. Never take limits from memory or from a readme.
3. Measure (pixel size, aspect ratio, format, transparency, file weight, frame rate, duration, loudness, contrast) and keep the command and its output. The skill's own measuring scripts are not built yet: use a tool already installed in the project or a small standard-library script written in `docs/qa/art/`. Every number must come from a tool that actually ran on the file in this session; a check with no working tool (for example loudness with no audio tool) is listed as "not run", never estimated. Judge the measured file, not its description.
4. Look at every file at real size (phone screen, store icon, ad thumbnail); for video, the first second, the last frame and frames between.
5. Hunt defects: AI artefacts (hands, broken text, extra limbs, melted edges), compression blocks, banding, halos, black frames, flicker; compare each file with the rest of the set (one character looks like one character).
6. Flags: brand and legal doubts (logos, real people's likenesses, music and font licences, misleading claims) and accessibility (text contrast, colour as the only signal, captions, flashing), each marked `verified`, `inferred` or `unknown`. Flag, never judge: a lawyer or the owner decides.
7. Verdict per file: **pass**, **fix** (an exact note for the artist) or **reject** (why), with the check, the measured value, the limit and a crop or frame.
8. Say what was not checked (no real phone, no ad preview tool, sound not heard).

## 4. Limits of this mode
- Never edit, crop, re-export or "just fix" a file; the note goes to the artist or editor through the boss.
- The Creative & Art Director sets the look and reads verdicts that touch it.
- Automatic image scores help find changes; they do not decide whether art is good or correct.
- A pass means the listed checks passed. Never "safe to run", "will perform" or "no legal issues".

## 5. Done (Art QA)
A check list exists with the source and date of each limit, each file has a verdict with evidence, and the answer says what was not checked.
