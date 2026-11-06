---
name: publish
description: Publish a muna course repo to GitHub. Refreshes and runs the validator, creates a public repo if there's none, commits and pushes after asking, and prints the link to paste into muna. Use when someone wants to publish, share or push their muna courses.
---

# Publish muna courses

Ask one question at a time. Never create a repo, commit or push without the author's OK.

## 1. Check
- Refresh the validator and schemas, unless this repo is `ilyichv/muna-courses` itself:
  ```sh
  mkdir -p scripts schema
  curl -fsSL https://raw.githubusercontent.com/ilyichv/muna-courses/main/scripts/validate.py -o scripts/validate.py
  curl -fsSL https://raw.githubusercontent.com/ilyichv/muna-courses/main/schema/muna.v1.json -o schema/muna.v1.json
  curl -fsSL https://raw.githubusercontent.com/ilyichv/muna-courses/main/schema/course.v1.json -o schema/course.v1.json
  ```
- Run `git fetch -q` if there's a remote, then `uv run scripts/validate.py` (or `pipx run scripts/validate.py`).
- **Stop on any error.** Show it, and suggest `/muna:write` to fix it.

## 2. GitHub
- No GitHub remote: offer `gh repo create <name> --public --source . --remote origin`, suggesting the folder's name. muna can only read public repos.
- A remote that `gh repo view --json visibility` says is private: tell the author muna can't read it until it's public.
- If `gh` is missing or not logged in, ask the author to install it or run `gh auth login`.

## 3. Commit and push
- Show what changed (`git status --short`) and propose a short commit message ("Add unit 2 of Roman history").
- Ask, then commit. Ask again, then push: `git push -u origin <branch>`.

## 4. The link
Print `https://github.com/<owner>/<repo>`, or `https://github.com/<owner>/<repo>/tree/<branch>` when the branch isn't the repo's default (`gh repo view --json url,defaultBranchRef`). Tell the author: in muna, tap **+** on Home and paste it.
