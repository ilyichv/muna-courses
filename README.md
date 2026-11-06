# muna courses

Courses for [muna](https://github.com/ilyichv/muna), a spaced-repetition iPhone app, and the spec for writing your own.

| Course | Folder | Language |
|---|---|---|
| Designing Data-Intensive Applications | [`ddia/`](ddia) | en |
| Paesi del mondo (countries, capitals, flags) | [`geo-world/`](geo-world) | it |
| Regioni d'Italia | [`geo-italia/`](geo-italia) | it |

**To add them in muna:** tap **+** on Home, paste `github.com/ilyichv/muna-courses`, and pick the courses you want.

---

# Writing a course

A course is a folder of JSON in any public repo or HTTPS location. Anyone can publish one, and muna adds it from a pasted link. There's no catalog and no sign-up.

## Writing with an agent
The `muna` plugin writes courses with you in [Claude Code](https://claude.com/claude-code) or [Codex](https://developers.openai.com/codex). Install it:

```sh
# Claude Code
/plugin marketplace add ilyichv/muna-courses
/plugin install muna@muna-courses

# Codex
codex plugin marketplace add ilyichv/muna-courses
codex plugin add muna@muna-courses
```

Then, in an empty folder, run its four skills in order: `/muna:new Roman history` plans the course, `/muna:write` writes one unit at a time, `/muna:review` checks the cards in a new session, and `/muna:publish` puts the repo on GitHub and gives you the link to paste into muna. In Codex, type `$muna:new` and so on.

## Layout
```
your-repo/
├── muna.json                  ← the index
├── spanish/                   ← one folder per course, named after the course's id
│   └── course.json
└── capitals/
    ├── course.json
    ├── world.geojson          ← "map": "world" means this file, next to course.json
    └── ATTRIBUTION.md         ← the app ignores every other file
```

## `muna.json`
```json
{
  "$schema": "https://raw.githubusercontent.com/ilyichv/muna-courses/main/schema/muna.v1.json",
  "name": "Alice's courses",
  "courses": ["spanish", "capitals"]
}
```
- `courses` lists the course folders, which sit next to `muna.json`. Every course folder must be listed.
- `name` is shown at the top of the picker when someone pastes your repo's link.

## `course.json`
```jsonc
{
  "$schema": "https://raw.githubusercontent.com/ilyichv/muna-courses/main/schema/course.v1.json",
  "id": "spanish",                      // same as the folder name
  "version": "1.0.0",                   // this course's own version (see Versioning)
  "title": "Spanish basics",
  "language": "en",                     // the language of the content
  "kind": "mastery",                    // "mastery" or "book"
  "color": "orange",                    // optional; missing means violet
  "retired": ["spanish-old-1"],         // optional: removed card and unit IDs (see Versioning)
  "units": [{
    "id": "greetings", "title": "Greetings",
    "cards": [
      { "id": "spanish-t01", "type": "learn", "title": "Saying hello", "body": "**Hola** works any time of day.\n\n**Buenos días** is for the morning." },
      { "id": "spanish-001", "type": "mcq", "prompt": "What do you say at 9 am?", "choices": ["Buenas noches", "Buenos días"], "answer": 1, "explanation": "…" },
      { "id": "spanish-002", "type": "text", "prompt": "Hello, in Spanish?", "answers": ["Hola"] }
    ]
  }]
}
```
- **`kind`:** in a `mastery` course, scoring at least 85% on a unit's test unlocks the next unit. In a `book` course, a unit unlocks when the learner marks its chapter as read, because the book does the teaching.
- **`color`:** one of `violet`, `blue`, `sky`, `teal`, `gold`, `orange`, `pink`, `fuchsia`.
- Units come in learning order, and lessons introduce each unit's cards in order.

## Card types
| Type | Fields | Used for | Grading |
|---|---|---|---|
| `learn` | `title`, `body` | One idea, explained in a few sentences, right before the questions on it | None: the learner taps GOT IT |
| `mcq` | `prompt`, `choices` (at least 2, shown in this order), `answer` (index from 0) | Concepts, true/false, scenarios | Automatic |
| `recall` | `prompt`, `keyPoints` (at least 1) | "Why" and "how" questions | The learner answers, then ticks the key points they covered |
| `order` | `prompt`, `items` (at least 2, distinct, stored in the correct order) | Steps of a process. The app shuffles them. | Automatic |
| `map` | `prompt`, `map`, `feature` | Tap the country or region | Automatic |
| `text` | `prompt`, `answers` (at least 1) | Type the answer. List every spelling you accept. | Automatic, ignoring case and accents |

- Every card has an `id` and a `type`.
- `explanation` is optional on every question type. It's shown after the answer.
- **`learn` cards** teach the questions that follow them in the unit, up to the next `learn` card. A unit must not end with one.
  - `body` is inline Markdown: paragraphs separated by a blank line, `**bold**`, `*italic*` and `` `code` ``. No lists or headings. Links are shown as plain text.
  - They aren't graded or scheduled: each is shown once, in its lesson.
- **Flags** are emoji in a prompt, answered with `map` or `text`. No image files are needed.

## Maps
A `map` card's `map` names a GeoJSON file in the course's own folder: `"map": "world"` means `world.geojson` next to `course.json`. Maps are downloaded with the course and are part of its version. Courses don't share maps.

- A map file is a `FeatureCollection` in longitude/latitude.
- Each feature's `properties.id` is what a card's `feature` refers to.
- `properties.quizzable` is optional and defaults to true. A shape with `false` is drawn but is never an answer. Other properties are ignored.
- If the map comes from someone else's data, credit it in an `ATTRIBUTION.md` in the course folder.

## IDs
- Course and unit IDs use lowercase letters, digits and dashes. A unit ID is unique within its course.
- Card IDs use letters, digits, `.`, `_` and `-`, and never `/`.
- **A card ID is unique across your whole repo,** including every course's `retired` list. muna stores progress under your repo + card ID, so two repos can use the same IDs without clashing.
- **Card IDs are permanent.** Never rename or reuse one. If a card's meaning changes, give it a new ID, so updates never corrupt anyone's progress.

## `$schema`
Every `muna.json` and `course.json` must start with its `"$schema"` line, exactly as above.
- **The URL names the format and its version:** `course.v1.json` is version 1. There's no separate version field.
- **In your editor:** VS Code and other editors that read JSON Schema show every field's description on hover, autocomplete field names and card types, and underline mistakes as you type. No setup is needed beyond the `$schema` line.
- **muna ships with each schema version it supports** and checks every file against its own copy. It never downloads a schema.
- **A published schema version never changes.** Any change, even a new card type, is a new version. An app that doesn't know your file's version keeps what it has installed and shows "Needs a newer muna". Any other URL shows "Not a muna course".
- The schemas are in [`schema/`](schema). A schema can't check rules that span fields or files: an `mcq` answer within its choices, unique IDs, a folder named after its course, a unit not ending with a `learn` card, map features existing, `retired`, and version bumps. The validator and the app check those.

## Versioning
`version` is `MAJOR.MINOR.PATCH`, digits only. Whatever is on your repo's default branch is the latest version. Raise it whenever anything in the course folder changes, by at least:

| Change | Minimum bump | In the app |
|---|---|---|
| Edits only: text, choices, card order, map files | patch | Installs silently |
| New cards or units, plus any edits | minor | Installs silently |
| Any card or unit ID removed | major | Asks first, with a summary of what's removed |

- **`retired` only ever grows.** Every card or unit ID you remove goes into it, and no card or unit may use an ID that's in it.
- A course whose folder changed without a higher `version` fails the validator, and the app ignores the change.
- A new course folder can start at any version.
- The app decides whether an update removes anything by comparing IDs itself, not from the version number. Removing a unit can lock the units after it again.

## Checking your course
The validator checks every file against its schema, then the rules a schema can't express. In a git repo, it also compares each course with your default branch: version bumps and `retired`. It needs [uv](https://docs.astral.sh/uv/) or [pipx](https://pipx.pypa.io), which install its one dependency.

```sh
git clone https://github.com/ilyichv/muna-courses
uv run muna-courses/scripts/validate.py path/to/your-repo                      # or: pipx run …
uv run muna-courses/scripts/validate.py path/to/your-repo --base origin/master  # default: origin/main
```
Run `git fetch` first so the base branch is up to date. Outside a git repo, or without the base branch, it skips the version checks and says so.

To run it in CI, copy `scripts/validate.py` and `schema/` into your repo, and see [`.github/workflows/validate.yml`](.github/workflows/validate.yml).

## Adding a course in muna
Tap **+** on Home and paste a link:
- **A repo link** lists its courses, and you pick which ones to add: `github.com/alice/spanish`, or the URL of any folder that holds a `muna.json`.
- **A course folder link** adds just that course: `github.com/alice/spanish/tree/main/spanish`, or the URL of any folder that holds a `course.json`.

GitHub links are read through `raw.githubusercontent.com`, so the repo must be public. Anywhere else, the files must be served over HTTPS. Each file can be up to 5 MB.

muna downloads the course and its maps and checks them all before saving anything; any failure keeps what's installed and shows the reason. It checks for a newer `version` when it opens and on pull-to-refresh.

## License
`scripts/` and `schema/` are MIT. The courses are not licensed for reuse. See [`LICENSE`](LICENSE).
