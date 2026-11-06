# Card rules

How to write good muna cards. `README.md` in `ilyichv/muna-courses` is the format; this is the craft. A repo's own house style (`STYLE.md`, `CLAUDE.md`, `AGENTS.md`) wins where it differs.

## Depth
- Test core ideas and trade-offs: what an idea is, why it exists, and when it breaks.
- **No trivia:** no cards that only ask for a name or a definition. Name a person, product or date only when the idea depends on it.
- Cover the whole unit's source in proportion to what matters, including side notes. Give each of its main themes at least one card.
- Cards follow the source's order, so lessons walk through it front to back.

## Wording
- Plain language, short sentences. A prompt is one or two sentences.
- **Write everything in your own words.** Never copy the source's sentences, examples, figures or tables. Restate the facts and invent your own examples and scenarios. When you have the source text, check for runs of 7 words shared with it: there must be none.
- No em dashes; use a colon, a semicolon or a new sentence. Straight quotes (`'`).
- Abbreviations the source defines can be used without expanding them.

## Learn cards
A `learn` card teaches one idea right before the questions on it. In a `mastery` course they teach everything the questions test. In a `book` course the source does the teaching, so they're optional.

- **Coverage:** every idea the unit's questions test, plus any core idea of the unit they miss. Add questions for those, so every learn card has questions after it.
- **One idea per card,** 60–120 words in the body, in one to three short paragraphs. An idea that needs more is two ideas.
- **Self-contained:** a learner who never saw the source can answer each question from the learn cards before it. Every `recall` key point and the fact behind every right `mcq` answer is stated in a learn card at or before the question.
- **Teach, don't give away:** explain the idea with your own example, not the scenario of the question that follows.
- **Tone:** plain and direct, in the second person. Open with a concrete everyday example when the idea is abstract.
- **Title:** the idea's name, one to five words, sentence case.
- **Markdown:** paragraphs separated by a blank line (`\n\n` in JSON). `**bold**` for a term the first time it appears, `*italic*` for emphasis, `` `code` `` for identifiers. No lists, headings or links: write a list as a sentence.
- **Placement:** right before the first question it teaches. It teaches the questions after it, up to the next learn card. Every learn card has at least one question after it, and a unit never ends with one.

## Questions
- **Explanations teach:** say why the right answer is right, and correct the likely mistake.
- About half the `mcq` cards are **scenarios**: a concrete situation ("A team…", "Your database…") that asks the learner to apply the idea, not recite it.

### `mcq`
- **3 or 4 choices,** exactly one right.
- Every wrong choice is a real misconception (reversed roles, a related but different idea, an overgeneralisation like "always"), never filler or a joke.
- Wrong choices are about as long and as specific as the right one, so length doesn't give the answer away.
- Spread `answer` across positions; don't let one index dominate.
- **Explanation: 2–4 sentences** (about 40–70 words). First why the right answer is right, then why each wrong choice is wrong.

### `recall`
- A "why" or "how" question.
- **2–4 key points.** Each is one short fact the learner can tick yes or no, distinct from the others.
- If the prompt names parts ("compare reads, writes…"), there's one key point per part.
- Explanation is optional: one sentence of context the key points don't cover. Leave it out if the points say it all.

### `order`
- Only for a real sequence: steps of a process, a timeline, or a spectrum with a clear direction. Don't force one where the source has none; write an `mcq` instead.
- 4–5 items, stored in the right order. Only one order is defensible; use words like "first" or "later" when two steps could swap.
- Explanation is optional: one or two sentences, often naming a variant.

### `text`
- One short, exact answer: a word, a name, a number.
- `answers` lists every spelling you accept: other names, with and without articles, common variants ("Rome", "Roma"). Case and accents are ignored.

### `map`
- See `maps.md` next to this file.
