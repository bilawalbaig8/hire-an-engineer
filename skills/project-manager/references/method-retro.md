# Retro mode

## 1. When to read this
"What went wrong?", "why did we lose a day?". The boss may ask for one after a release or when the change check finds a reversed decision; the Project Manager may suggest one in a status. It runs on request; it never schedules itself.

## 2. Steps
1. **Timeline from the records only:** run summaries, run decisions, `.agents/events.jsonl`, reviews and the change check. Each line links its record. Where the records are silent, write `unknown`; never fill a gap from memory or guesswork. Chats and other tools are "not seen".
2. **Why, until the cause is in the process** (a missing check, a missing owner, an unclear decision), never "role X was careless" or the owner's fault (S-PM-28, S-PM-30). No blame on a person or a role.
3. **Patterns across runs:** work that was reverted, decisions that were reversed, questions asked twice, roles waiting on each other.
4. **1 to 3 actions**, each with a proposed owner (a role or the owner) and a check that shows it worked (S-PM-29).
5. **Lesson lines per role,** written as "what went wrong; the rule that prevents it". Put them in the retro file and return them to the boss, which writes them in `docs/lessons/<role>.md` (owner decision X2). Never write in `docs/lessons/`.

## 3. Traps
- **No run folders for the period:** list the records that exist, mark the rest `unknown`, and ask at most 3 questions with defaults.
- **"Write the lesson straight into the lessons file":** write it in the retro file and return it to the boss.
- **Generic lessons ("communicate better"):** each lesson names the check or rule that would have caught it.

## 4. Done when
`docs/project/retros/<date>-<topic>.md` exists with facts linked to records, causes in the process, 1 to 3 actions and proposed lesson lines; no blame on a person or role; the lessons are returned to the boss.
