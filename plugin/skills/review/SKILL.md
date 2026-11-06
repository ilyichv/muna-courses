---
name: review
description: Accuracy review of a muna course's cards (course.json). Checks facts against the course's sources, one right mcq answer, clear wording, checkable recall points, one valid order, matching explanations and no copied source text, lists the problems, then fixes the ones the author approves. Use to check cards before publishing them.
---

# Review muna cards

**Run in a fresh context.** If you wrote or edited this course's cards earlier in this conversation, stop: tell the author to start a new session and run `/muna:review` there, so the writer never reviews its own cards.

Ask one question at a time.

## 1. Scope
- What the author named: a course, a unit, or a diff ("my changes", a branch, a commit).
- With nothing named: the cards added or changed since `origin/main` (`git fetch -q`, then compare with `git show origin/main:<course>/course.json`), or every card if the course isn't there yet. If the repo has several courses, ask which.

## 2. Read
- `../write/cards.md` next to this file, and `../write/maps.md` if there are `map` cards.
- The repo's house style, if it has one (`STYLE.md`, `CLAUDE.md`, `AGENTS.md`).
- The course's `README.md` for its sources, then the sources themselves.

## 3. Check every card in scope
- **Facts** against the course's sources. When you can't confirm a fact, mark the card **uncertain**; never guess.
- **`mcq`:** exactly one right answer; every wrong one clearly wrong but believable.
- **Clarity:** a careful reader who knows the material can't argue for another answer.
- **`recall`:** key points complete, distinct, and checkable yes or no.
- **`order`:** only one defensible order.
- **`text`:** every reasonable spelling of the answer is accepted.
- **Explanations** match the answer.
- **Learn cards** (`mastery`): every question can be answered from the learn cards before it.
- **No copied source text:** no 7-word runs shared with the source.
- Everything else in `cards.md` and the house style.

## 4. Report, then fix
List the problems in three groups, each with the card ID, the problem, and the fix you propose:
- **Wrong:** a fact or answer is incorrect.
- **Unclear:** ambiguous wording, a second defensible answer, a weak distractor, a broken rule.
- **Uncertain:** you couldn't confirm it against the sources.

Ask which fixes to make (all, some, or none), and make only those. Follow `../write/SKILL.md` for IDs: a fix that changes a card's meaning gives it a new ID and retires the old one. After each edit, run the validator as `../write/SKILL.md` says, raising `version` when it asks.

## 5. Finish
End with: how many cards you checked, how many you fixed, and how many are uncertain, then list each uncertain card's ID and what to confirm.
