# Method: Review (verdict per file against the brief and the guide)

## 1. When to read this
"Do these 12 icons look like one set", "check this art", "check this ad video", "mark these approved".

Read `what-it-can-see.md` and `critique.md` first; this file only adds the steps.

## 2. Steps
1. **Scope:** which files, against which brief and guide, for which use (store icon, ad thumbnail, in-game, store screenshot).
2. **Open each image file.** For video, use exported frames plus the script. For anything it cannot open, say so and ask for an export.
3. **Check** each file with the checks in `critique.md` section 3.
4. **Verdict** per file: approve, fix (with the exact note) or redo, with severity 4 to 1.
5. **Provenance:** add or update the line in `docs/creative/asset-register.md`; `unknown` with the reason when the licence or tool terms are not known; a third-party asset with no licence is `needs_approval`, never "safe to use".
6. **Send on:** the result goes to the maker, to Art QA (QA / Test Engineer) and to the owner through the boss.

## 3. Not the last check
"You directed these, mark them approved for the store": give a recommendation only; the final check is Art QA and the owner. The owner reviews results for now; every issue the owner reports becomes a lesson in `docs/creative/lessons.md` (owner decision Q22).

## 4. Not Art QA
It reviews the look against the brief and the guide. It does not check file size, format, resolution, atlas fit, compression, store or ad network specs; that is the QA / Test Engineer in Art QA mode. If it notices such a problem, it notes it for Art QA without measuring it.

## 5. Skeleton
Review note: header `scope | brief and guide used | use`, then one line per file (the note skeleton in `critique.md`), then the three lists: opened, read about only, not checked.

## 6. Where files go
`docs/creative/art-direction/` (review notes); provenance in `docs/creative/asset-register.md`.

## 7. Done when
Each file has a verdict with the check it was judged on; the answer says which files it opened, which it only read about, and what it did not check (for example "not checked on a real phone").
