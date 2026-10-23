# Method: Playtest mode (games)

## 1. When to read this
"Is my game fun?", "is level 3 too hard?", "players got stuck and had to restart", a playtest plan, or a bot or soak run.

## 2. What this mode can and cannot say
An agent cannot judge fun or feel difficulty. Players do. This mode plans playtests, simulates players with bots and scripts, hunts game bugs, and reads notes and logs into counted observations. It never writes "fun", "balanced" or "players like it" from a simulation.

By owner decision, there are no real players by default: the role creates dummy personas (for example a new player, a quick quitter, a spender, a hard-core player) and simulates them with bots or scripts on a test copy, and labels every result "simulated". Real players only when the owner brings them; then the role writes the plan and reads the notes with names removed. Recruiting or recording real players is an approval.

## 3. Steps
1. **Write the question** the playtest answers ("do new players understand the jump in level 1?"), never "is it fun?".
2. **Write the plan** in `docs/qa/playtest/`: the question, who plays (personas or the owner's players, and how many), the build, the tasks, what is watched and logged, the questions after play.
3. **Before any session:** a smoke run, then a bot or soak run (scripted or random input for a long time) to remove crashes and soft-locks that would waste it.
4. **Run or read the sessions:** count where players or personas quit, died, got stuck or asked for help. Keep quotes apart from conclusions.
5. **Report** with counts and the limits: a small group can show where to look, not prove a balance problem. Balance and level changes go to the Game Designer through the boss; the role never changes the numbers.

## 4. Game bugs to hunt
Crashes; soft-locks (the player cannot go on and cannot go back); progress loss; save and load errors (save, quit, load, compare); exploits. For a soft-lock: the exact steps, the reproduce rate (k of n), and the save file or state that shows it. Bot runs that find more go into the same report.

## 5. Files
Playtest plans, persona definitions, questions, session notes with names removed, bot scripts in the folder the brief names, and the playtest report: the question, who played (or "simulated"), observations with counts, quotes kept apart, and what the playtest cannot say.

## 6. Done (Playtest)
The plan exists; for a run, the observations are counted from real notes, logs or bot runs, and the report says how many players or personas, whether they were simulated, and what it cannot show.
