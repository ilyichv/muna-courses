# muna-courses

Courses for the muna app. `README.md` is the format spec, `plugin/skills/write/cards.md` the card rules, and `STYLE.md` the house style for these courses.

## Commands
```sh
git fetch origin main && uv run scripts/validate.py   # what CI runs (pipx run works too)
uv run scripts/test_validate.py                      # validator tests
```

## Layout
- `muna.json`: the index. Every course folder is listed in it.
- `<course>/course.json`: one folder per course, named after its `id`. Map files sit next to the course that uses them, with its `ATTRIBUTION.md`.
- `schema/`: `muna.v1.json` and `course.v1.json`. The app bundles them, so a published version never changes; any change is a new `v2` file.
- `scripts/`: `validate.py` and its tests.
- `plugin/`: the `muna` plugin for Claude Code and Codex. Its skills are `new`, `write`, `review` and `publish` in `skills/`; `skills/write/cards.md` holds the card rules. `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json` list it.

## Rules
- **IDs are permanent.** Never rename or reuse a card or unit ID; a card whose meaning changes gets a new ID.
- **Raise `version` whenever anything in a course folder changes:** patch for edits, minor for new cards or units, major when an ID is removed (README > Versioning).
- **Removed IDs go into `retired`,** which only grows.

## Commits
[Conventional Commits](https://www.conventionalcommits.org): `type(scope): summary`, lowercase, imperative, no period. PR titles use the same format.
- Types: `feat`, `fix`, `test`, `refactor`, `docs`, `chore`, `ci`, `build`.
- Scope is a course folder (`ddia`, `geo-world`, `geo-italia`), or `schema`, `scripts`, `plugin`, `ci`, `docs`. Omit it when a commit spans several areas.
- Examples: `feat(ddia): add chapter 2 learn cards`, `fix(geo-world): accept "Mexico City" for geo-MEX-cap`, `fix(scripts): skip version checks outside git`.
