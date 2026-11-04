# House style

Conventions for the courses in this repo, on top of the format in `README.md`. Other authors don't have to follow them.

The validator checks only the public ID rule, not the ID patterns here, so keep to them by hand.

# Book courses

Conventions for book courses. DDIA teaches itself: each chapter's `learn` cards explain its ideas right before the questions on them, so reading the book is optional. It's a `mastery` course, so passing a chapter's unit test unlocks the next one.

The question rules were approved on the chapter 1 pilot the learn card rules later. `ddia/course.json` unit `ch01` is the reference example.

## Source
*Designing Data-Intensive Applications*, **2nd edition** (Martin Kleppmann and Chris Riccomini). EPUB at `~/Documents/books/designing-data-intensive-application.epub`. One unit per chapter:

| Unit | Title |
|---|---|
| `ch01` | Trade-Offs in Data Systems Architecture |
| `ch02` | Defining Nonfunctional Requirements |
| `ch03` | Data Models and Query Languages |
| `ch04` | Storage and Retrieval |
| `ch05` | Encoding and Evolution |
| `ch06` | Replication |
| `ch07` | Sharding |
| `ch08` | Transactions |
| `ch09` | The Trouble with Distributed Systems |
| `ch10` | Consistency and Consensus |
| `ch11` | Batch Processing |
| `ch12` | Stream Processing |
| `ch13` | A Philosophy of Streaming Systems |
| `ch14` | Doing the Right Thing |

Unit titles are the book's chapter titles, verbatim.

## Size and mix
- **About 40 questions per chapter**, plus the learn cards that teach them.
- **About 50% `mcq`, 35% `recall`, 15% `order`** (pilot: 20 / 14 / 6).
- About half of the `mcq` cards are **scenarios**: a concrete situation ("A team…", "Your database…") that asks you to apply the idea, not recite it.
- `order` cards need a real sequence: a pipeline, a data flow, a recovery procedure, or a spectrum with an unambiguous direction ("most in-house to most outsourced"). Don't force one where the chapter has none; give the slot to `mcq`.

## Depth
- Core concepts and trade-offs: what an idea is, why it exists, and when it breaks.
- **No trivia:** no cards on which named product does what, and no definitions that ask only for a name. Name a system only when the idea depends on it.
- Cover the whole chapter, including sidebars, in proportion to how much they matter. Give the summary's themes at least one card each.

## Wording
- Plain English, short sentences. A prompt is one or two sentences.
- **Write everything from scratch.** Never copy the book's sentences, examples, figures or tables. Restate the facts in your own words and invent your own scenarios. Check by looking for 7-word runs shared with the chapter text; there must be none.
- No em dashes; use a colon, semicolon or a new sentence. Straight quotes (`'`).
- Abbreviations the chapter defines (OLTP, ETL, HTAP) can be used without expanding them.

## Card types
### `mcq`
- **3 or 4 choices**, exactly one correct.
- Every wrong choice is a real misconception (reversed roles, a related but different concept, an overgeneralization like "always"), never filler or a joke.
- Wrong choices are about as long and as specific as the right one, so length doesn't give the answer away.
- Spread `answer` across positions; don't let index 0 or 1 dominate.
- **Explanation: 2–4 sentences** (about 40–70 words). First say why the right answer is right, then why each wrong choice is wrong.

### `recall`
- A "why" or "how" question.
- **2–4 key points.** Each is one short, checkable fact you can tick yes or no, distinct from the others.
- If the prompt names parts ("compare reads, writes…"), there is one key point per part.
- Explanation is optional: one sentence that adds context the key points don't cover. Leave it out if the points say it all.

### `order`
- 4–5 items, stored in the correct order.
- Only one order is defensible. Use words like "later" or "first" when two steps could otherwise swap.
- Explanation is optional: one or two sentences, often naming the variant or the trade-off (e.g. ELT swaps transform and load).

## Learn cards
A `learn` card teaches one idea right before the questions on it. It has a `title` and a `body`, nothing else.

- **Size:** one idea per card, **60–120 words** in the body, in one to three short paragraphs. If an idea needs more, it's two ideas.
- **Coverage:** every idea the chapter's questions test, plus any core idea of the chapter they miss. Add questions for those, so every learn card has questions after it.
- **Self-contained:** someone who never opened the book must be able to answer each question from the learn cards before it. Every `recall` key point and the fact behind every right `mcq` answer is stated in a learn card at or before the question.
- **Teach, don't give away:** explain the principle with your own example, not the scenario of the question that follows.
- **Tone:** plain and direct, in the second person, with short sentences. Open with a concrete everyday example when the idea is abstract (a food delivery app, a music app). The wording rules above apply, including the 7-word overlap check.
- **Title:** the idea's name, one to five words, sentence case ("OLTP and OLAP", "When a request times out").
- **Markdown:** paragraphs separated by a blank line (`\n\n` in JSON). `**bold**` for a term the first time it's introduced, `*italic*` for emphasis or a secondary term, `` `code` `` for identifiers. No lists, headings or links: write a list as a sentence.
- **Placement:** right before the first question it teaches. It teaches the questions after it, up to the next learn card, so move questions inside the unit to follow their learn card; their IDs don't change. Every learn card is followed by at least one question, and a unit never ends with one.

## IDs and order
- Questions: `<course>-<unit>-<nnn>`, e.g. `ddia-ch01-012`, numbered from `001` within each unit.
- Learn cards: `<course>-<unit>-t<nn>`, e.g. `ddia-ch01-t03`, numbered from `t01` in file order within each unit.
- Cards follow the chapter's order, so lessons walk through the chapter front to back.
- IDs are permanent. A card added later goes where it fits in the array but takes the next unused number. If a card's meaning changes, it gets a new ID; never renumber or reuse one.

# Geography courses
- Card IDs are `geo-<code>-<type>`: `geo-PER-map`, `geo-PER-cap`, `geo-PER-flag` (ISO 3166-1 alpha-3), and `geo-it-09-map` (ISTAT region code).
- IDs come only from those codes, never from the unit, so moving a country to another unit keeps its progress.
