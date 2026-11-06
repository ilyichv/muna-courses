---
name: write
description: Write or fix cards in a muna course (a course.json in a repo with muna.json). Writes the next unit from the course's README.md, a given unit, more cards, or a fix to a card, then runs the validator. Use after /muna:new, or whenever someone asks to add or change muna cards.
---

# Write muna cards

You write cards for a muna course. The format is `README.md` in `ilyichv/muna-courses` (`https://raw.githubusercontent.com/ilyichv/muna-courses/main/README.md`). Ask one question at a time.

## 1. What to write
- **The course:** the folder with the course's `README.md` (its structure, from `/muna:new`) and, once a unit is written, `course.json`. If the repo has several, ask which.
- **The job,** from what the author asked: a unit, more cards, or a fix to a card. With nothing asked, propose the first unit in the course README whose ID isn't in `course.json` yet, and ask to confirm.
- A unit missing from the README: ask what it covers and its sources, and add it to the README's unit list in learning order.

## 2. Rules
Read before writing:
- `cards.md` next to this file: how to write each card.
- `maps.md` next to this file, for `map` cards.
- The repo's house style, if it has one (`STYLE.md`, `CLAUDE.md`, `AGENTS.md`). It wins where it differs from `cards.md`.
- The unit's sources from the course README. Read the part this unit covers. With general knowledge only, stick to well-established facts.

## 3. Write
- **First unit:** create `<course>/course.json` from the README (title, language, kind, colour), with `"version": "1.0.0"` and the `$schema` line exactly as in the format, and add the course ID to `courses` in `muna.json`.
- Units go in the README's order. Inside a unit, cards go in learning order.
- **Size:** follow the house style. Without one, about 10–20 questions per unit, mostly `mcq`, `recall` for "why" and "how", `order` only for real sequences, plus the learn cards that teach them (`mastery`).
- **Card IDs** use letters, digits, `.`, `_` and `-`. Without a house pattern, questions are `<course>-<unit>-<nnn>` from `001`, and learn cards `<course>-<unit>-t<nn>` from `t01`.
  - An ID is unique across the whole repo, including every course's `retired` list.
  - IDs are permanent: never rename, renumber or reuse one. A new card takes the next unused number, wherever it goes in the unit.
  - A card whose meaning changes gets a new ID, and the old ID goes into `retired`. So does every card or unit ID you remove.
  - That's only for published IDs, the ones on `origin/main`. An ID that was never pushed has no learner progress, so change or drop it without retiring it.
- Typo and wording fixes keep the ID.

## 4. Check
After every edit to a course file:
```sh
git fetch -q                  # only if the repo has a remote
uv run scripts/validate.py    # or: pipx run scripts/validate.py
```
- Fix every error and run it again until it prints `OK`.
- If it says a version must be at least some number, set the course's `version` to exactly that.
- Without `scripts/validate.py`, run `/muna:new` first. Without uv or pipx, ask the author to install uv (`https://docs.astral.sh/uv/`).

## 5. Finish
Say what you wrote (cards per type) and the validator's last line. Suggest `/muna:review` **in a new session**, so a fresh context checks the cards, then `/muna:publish`.
