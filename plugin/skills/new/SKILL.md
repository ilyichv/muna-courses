---
name: new
description: Start a new muna course. Sets up a course repo (muna.json, validator, CI) if the folder has none, agrees the topic, audience, sources and units with the author, and saves the structure in the course's README.md. Use when someone wants to create or plan a muna course.
---

# New muna course

You plan a course for muna, a spaced-repetition app; `/muna:write` writes its units afterwards. The format is `README.md` in `ilyichv/muna-courses`: read it from `https://raw.githubusercontent.com/ilyichv/muna-courses/main/README.md` if you don't know it.

Ask one question at a time, as multiple choice with your recommendation first when there are options. If the author gave a topic with the command, don't ask for it again.

## 1. The repo
Skip this if the current folder has a `muna.json`. Otherwise ask before setting up this folder as a course repo, then:
- `git init -b main` if it isn't a git repo.
- Ask what to call the collection (shown when someone pastes the repo's link, e.g. "Alice's courses") and write `muna.json`. Its `courses` stays empty until `/muna:write` writes the first unit, so the validator fails until then:
  ```json
  {
    "$schema": "https://raw.githubusercontent.com/ilyichv/muna-courses/main/schema/muna.v1.json",
    "name": "Alice's courses",
    "courses": []
  }
  ```
- Download the validator and schemas:
  ```sh
  mkdir -p scripts schema .github/workflows
  curl -fsSL https://raw.githubusercontent.com/ilyichv/muna-courses/main/scripts/validate.py -o scripts/validate.py
  curl -fsSL https://raw.githubusercontent.com/ilyichv/muna-courses/main/schema/muna.v1.json -o schema/muna.v1.json
  curl -fsSL https://raw.githubusercontent.com/ilyichv/muna-courses/main/schema/course.v1.json -o schema/course.v1.json
  ```
- Write `.github/workflows/validate.yml`:
  ```yaml
  name: validate
  on: [push, pull_request]

  jobs:
    validate:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v5
        - name: Fetch main for the version checks
          run: git fetch --depth=1 origin +refs/heads/main:refs/remotes/origin/main
        - run: pipx run scripts/validate.py
  ```

## 2. The course
Ask, in this order:
1. **Topic,** and how deep to go.
2. **Audience:** who it's for and what they already know.
3. **Content language** (`en`, `it`…).
4. **Sources:** a book (ask for the file), notes, URLs, or general knowledge. Read what they give you.
5. **Kind:** `mastery` (learn cards teach everything, and passing a unit's test unlocks the next) or `book` (the learner reads the source, and marking a chapter read unlocks the next unit).
6. **Course ID:** lowercase letters, digits and dashes, permanent, and the folder name. Suggest one from the title; it must not be a folder that already exists.
7. **Colour,** optional: `violet` (the default), `blue`, `sky`, `teal`, `gold`, `orange`, `pink` or `fuchsia`.

## 3. The units
Propose the units in learning order: for each, an ID (lowercase letters, digits and dashes, permanent), a title, what it covers, and which sources it draws on. A book usually gets one unit per chapter, titled as the chapter. Revise until the author approves.

## 4. Save the structure
Write `<course-id>/README.md`. muna ignores it, and GitHub shows it when someone opens the course's link:

```markdown
# <Title>

<What the course covers and who it's for, in one to three sentences.>

To add it, tap **+** on Home in muna and paste this folder's link.

- **Language:** en
- **Kind:** mastery
- **Colour:** teal
- **Sources:** <each source: title and author, file name, or URL; or "general knowledge">

## Units
1. **<Unit title>** (`<unit-id>`): <what it covers>. Sources: <which>.
2. …
```

Don't create `course.json` or add the course to `muna.json`: a unit needs at least one card, so `/muna:write` does both with the first unit. Finish by telling the author to run `/muna:write` to write unit 1.
