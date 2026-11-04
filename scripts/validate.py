#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["jsonschema>=4"]
# ///
"""Validate a folder of muna courses against the format in README.md.

    uv run scripts/validate.py [ROOT] [--base REF]      # or: pipx run scripts/validate.py …

ROOT is the folder with muna.json (default: the current folder). Checks muna.json and every
<folder>/course.json against the schema their "$schema" names, from schema/ next to this script,
then the rules a schema can't express. If ROOT is in a git repo where REF exists (default
origin/main), it also compares each course with REF: version bumps and retired IDs.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import jsonschema

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schema"
SCHEMAS = {s["$id"]: s for s in (json.loads(p.read_text(encoding="utf-8")) for p in SCHEMA_DIR.glob("*.json"))}
BUMPS = ("major", "minor", "patch")


def load(root, rel, kind, errors):
    """The file's data if it's valid against its schema, else None, with the reasons added to errors."""
    try:
        data = json.loads((root / rel).read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{rel}: not found")
        return None
    except (OSError, ValueError) as e:
        errors.append(f"{rel}: not valid JSON: {e}")
        return None
    known = sorted(url for url in SCHEMAS if url.rsplit("/", 1)[1].startswith(f"{kind}."))
    url = data.get("$schema") if isinstance(data, dict) else None
    if url not in known:
        problem = 'missing "$schema"' if url is None else f'unknown "$schema" {url!r}'
        errors.append(f"{rel}: {problem}, expected one of: {', '.join(known)}")
        return None
    found = sorted(jsonschema.Draft7Validator(SCHEMAS[url]).iter_errors(data), key=lambda e: [str(p) for p in e.absolute_path])
    errors += [f"{rel}: {where(data, e.absolute_path)}: {e.message}" for e in found]
    return None if found else data


def where(data, path):
    """A schema error's location, e.g. "units[2].cards[5] (geo-PER-cap)"."""
    path = list(path)
    text = "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in path).lstrip(".") or "top level"
    if path[:1] == ["units"] and path[2:3] == ["cards"] and len(path) > 3:
        try:
            text += f" ({data['units'][path[1]]['cards'][path[3]]['id']})"
        except (LookupError, TypeError):
            pass
    return text


def load_map(path, cache):
    """Feature ID -> quizzable, or None if the map file is missing or unreadable."""
    if path not in cache:
        try:
            features = json.loads(path.read_text(encoding="utf-8"))["features"]
            cache[path] = {f["properties"]["id"]: f["properties"].get("quizzable", True) for f in features}
        except (OSError, ValueError, LookupError, TypeError):
            cache[path] = None
    return cache[path]


def check_course(root, name, course):
    """The rules a schema can't express, for one schema-valid course."""
    rel = f"{name}/course.json"
    errors = [] if course["id"] == name else [f"{rel}: id '{course['id']}' must equal its folder name '{name}'"]
    retired, unit_ids, maps = set(course.get("retired", [])), set(), {}
    for i, unit in enumerate(course["units"]):
        at = f"{rel}: units[{i}] ({unit['id']})"
        if unit["id"] in unit_ids:
            errors.append(f"{at}: duplicate unit id")
        if unit["id"] in retired:
            errors.append(f"{at}: unit id is retired")
        unit_ids.add(unit["id"])
        if unit["cards"][-1]["type"] == "learn":
            errors.append(f"{at}: ends with a learn card, which would teach nothing")
        for j, card in enumerate(unit["cards"]):
            at = f"{rel}: units[{i}].cards[{j}] ({card['id']})"
            if card["type"] == "mcq" and card["answer"] >= len(card["choices"]):
                errors.append(f"{at}: answer {card['answer']} is out of range, there are {len(card['choices'])} choices (0-{len(card['choices']) - 1})")
            elif card["type"] == "map":
                features = load_map(root / name / f"{card['map']}.geojson", maps)
                if features is None:
                    errors.append(f"{at}: map '{card['map']}' has no readable file {name}/{card['map']}.geojson")
                elif card["feature"] not in features:
                    errors.append(f"{at}: feature '{card['feature']}' is not in map '{card['map']}'")
                elif features[card["feature"]] is False:
                    errors.append(f"{at}: feature '{card['feature']}' in map '{card['map']}' is not quizzable")
    return errors


def check_card_ids(courses):
    """Card IDs are unique across the repo, including every course's retired list."""
    errors, seen = [], {}
    retired = {rid: name for name, course in courses.items() for rid in course.get("retired", [])}
    for name, course in courses.items():
        for i, unit in enumerate(course["units"]):
            for j, card in enumerate(unit["cards"]):
                cid, at = card["id"], f"{name}/course.json: units[{i}].cards[{j}] ({card['id']})"
                if cid in retired:
                    errors.append(f"{at}: id is retired in {retired[cid]}, so it can't be used again")
                elif cid in seen:
                    errors.append(f"{at}: duplicate card id, also in {seen[cid]}")
                seen.setdefault(cid, f"{name}/course.json")
    return errors, len(seen)


def ids(course):
    return {x["id"] for unit in course["units"] for x in (unit, *unit["cards"])}


def version(text):
    return tuple(int(n) for n in text.split("."))


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def check_against_base(root, base, courses):
    """(errors, note): version bumps and retired IDs for each course that also exists on base."""
    try:
        if git(root, "rev-parse", "--git-dir").returncode != 0:
            return [], f"{root} is not in a git repo, so version checks were skipped"
    except FileNotFoundError:
        return [], "git is not installed, so version checks were skipped"
    if git(root, "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}").returncode != 0:
        return [], f"there is no {base} to compare with, so version checks were skipped (try `git fetch origin main`)"

    errors = []
    for name, course in courses.items():
        rel = f"{name}/course.json"
        shown = git(root, "show", f"{base}:./{rel}")
        if shown.returncode != 0:
            continue  # a new course can start at any version
        try:
            old = json.loads(shown.stdout)
            old_ids, old_retired, old_version = ids(old), old.get("retired", []), version(old["version"])
        except (ValueError, LookupError, TypeError, AttributeError):
            continue  # a broken course on base has nothing to compare with

        retired, now = set(course.get("retired", [])), ids(course)
        removed, added = sorted(old_ids - now), sorted(now - old_ids)
        changed = git(root, "diff", "--quiet", base, "--", name).returncode != 0 or git(root, "ls-files", "--others", "--exclude-standard", "--", name).stdout.strip()
        if changed:
            bump = 0 if removed else 1 if added else 2
            minimum = old_version[:bump] + (old_version[bump] + 1,) + (0,) * (2 - bump)
            if version(course["version"]) < minimum:
                why = f"removes {', '.join(removed)}" if removed else f"adds {', '.join(added)}" if added else "changed"
                errors.append(f"{rel}: {why} since {base}, which needs a {BUMPS[bump]} bump: version must be at least "
                              f"{'.'.join(map(str, minimum))}, not {course['version']}")
        lost = [x for x in old_retired if x not in retired]
        if lost:
            errors.append(f"{rel}: retired only grows, but lost {', '.join(lost)} since {base}")
        unretired = [x for x in removed if x not in retired]
        if unretired:
            errors.append(f"{rel}: {', '.join(unretired)} removed since {base} must be added to retired")
    return errors, None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."), help="folder with muna.json (default: .)")
    parser.add_argument("--base", default="origin/main", help="git ref to compare versions with (default: origin/main)")
    args = parser.parse_args(argv)
    root, errors = args.root, []

    index = load(root, "muna.json", "muna", errors)
    folders = sorted(p.parent.name for p in root.glob("*/course.json"))
    if index:
        errors += [f"muna.json: '{n}' is listed, but {n}/course.json doesn't exist" for n in index["courses"] if n not in folders]
        errors += [f"{n}/course.json: folder '{n}' is missing from muna.json" for n in folders if n not in index["courses"]]

    courses = {}
    for name in folders:
        course = load(root, f"{name}/course.json", "course", errors)
        if course:
            courses[name] = course
            errors += check_course(root, name, course)
    id_errors, card_count = check_card_ids(courses)
    base_errors, note = check_against_base(root, args.base, courses)
    errors += id_errors + base_errors

    if note:
        print(f"note: {note}")
    for e in errors:
        print(f"error: {e}")
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        return 1
    print(f"OK: {len(courses)} course(s), {card_count} card(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
