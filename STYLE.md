# House style

What's specific to the courses in this repo, on top of the format in `README.md` and the card rules in [`plugin/skills/write/cards.md`](plugin/skills/write/cards.md). Other authors don't have to follow it.

The validator checks only the public ID rule, not the ID patterns here, so keep to them by hand.

# Book courses

DDIA teaches itself: each chapter's `learn` cards explain its ideas right before the questions on them, so reading the book is optional. It's a `mastery` course, so passing a chapter's unit test unlocks the next one. `ddia/course.json` unit `ch01`, the approved pilot, is the reference example.

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

## IDs
- Questions: `<course>-<unit>-<nnn>`, e.g. `ddia-ch01-012`, numbered from `001` within each unit.
- Learn cards: `<course>-<unit>-t<nn>`, e.g. `ddia-ch01-t03`, numbered from `t01` in file order within each unit.
- A card added later goes where it fits in the array but takes the next unused number.

# Geography courses
- Card IDs are `geo-<code>-<type>`: `geo-PER-map`, `geo-PER-cap`, `geo-PER-flag` (ISO 3166-1 alpha-3), and `geo-it-09-map` (ISTAT region code).
- IDs come only from those codes, never from the unit, so moving a country to another unit keeps its progress.
