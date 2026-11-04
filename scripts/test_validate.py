#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["jsonschema>=4"]
# ///
"""Tests for validate.py. Each one builds a throwaway git repo in a temp folder.

    uv run scripts/test_validate.py      # or: pipx run scripts/test_validate.py
"""
import contextlib
import copy
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import validate

SCHEMA = "https://raw.githubusercontent.com/ilyichv/muna-courses/main/schema/"
INDEX = {"$schema": SCHEMA + "muna.v1.json", "name": "Test", "courses": ["demo"]}
COURSE = {
    "$schema": SCHEMA + "course.v1.json", "id": "demo", "version": "1.0.0",
    "title": "Demo", "language": "en", "kind": "mastery",
    "units": [{"id": "u1", "title": "One", "cards": [
        {"id": "demo-t01", "type": "learn", "title": "An idea", "body": "It **matters**."},
        {"id": "demo-001", "type": "mcq", "prompt": "Which?", "choices": ["a", "b"], "answer": 1},
        {"id": "demo-002", "type": "text", "prompt": "Type it", "answers": ["x"]},
        {"id": "demo-003", "type": "map", "prompt": "Where?", "map": "world", "feature": "AAA"},
    ]}],
}
MAP = {"type": "FeatureCollection", "features": [
    {"type": "Feature", "properties": {"id": "AAA"}, "geometry": None},
    {"type": "Feature", "properties": {"id": "BBB", "quizzable": False}, "geometry": None},
]}


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.git("init", "-q", "-b", "main")
        self.write("muna.json", INDEX)
        self.write("demo/world.geojson", MAP)
        self.course = copy.deepcopy(COURSE)
        self.save()
        self.git("add", ".")
        self.git("commit", "-qm", "base")

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args], check=True)

    def write(self, rel, data):
        (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.root / rel).write_text(json.dumps(data), encoding="utf-8")

    def save(self, folder="demo"):
        self.write(f"{folder}/course.json", self.course)

    @property
    def cards(self):
        return self.course["units"][0]["cards"]

    def run_validate(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = validate.main([str(self.root), "--base", "main"])
        return code, out.getvalue()

    def assert_fails(self, *messages):
        code, out = self.run_validate()
        self.assertEqual(code, 1, out)
        for message in messages:
            self.assertIn(message, out)

    def assert_passes(self):
        code, out = self.run_validate()
        self.assertEqual(code, 0, out)
        return out

    # Baselines

    def test_valid_repo_passes(self):
        self.assertIn("OK: 1 course(s), 4 card(s)", self.assert_passes())

    def test_outside_git_skips_version_checks(self):
        shutil.rmtree(self.root / ".git")
        self.course["version"] = "0.1.0"
        self.save()
        self.assertIn("version checks were skipped", self.assert_passes())

    def test_proper_removal_passes(self):
        del self.cards[2]
        self.course.update(version="2.0.0", retired=["demo-002"])
        self.save()
        self.assert_passes()

    # The schema's part

    def test_missing_schema(self):
        del self.course["$schema"]
        self.save()
        self.assert_fails('demo/course.json: missing "$schema"')

    def test_unknown_schema(self):
        self.course["$schema"] = SCHEMA + "course.v9.json"
        self.save()
        self.assert_fails('demo/course.json: unknown "$schema"', "course.v9.json")

    def test_course_schema_in_muna_json(self):
        self.write("muna.json", {**INDEX, "$schema": SCHEMA + "course.v1.json"})
        self.assert_fails('muna.json: unknown "$schema"')

    def test_missing_field(self):
        del self.cards[1]["answer"]
        self.save()
        self.assert_fails("units[0].cards[1] (demo-001): 'answer' is a required property")

    def test_unknown_field(self):
        self.cards[2]["hint"] = "x"
        self.save()
        self.assert_fails("units[0].cards[2] (demo-002): Additional properties are not allowed ('hint' was unexpected)")

    def test_unknown_card_type(self):
        self.cards[2]["type"] = "quiz"
        self.save()
        self.assert_fails("units[0].cards[2].type (demo-002): 'quiz' is not one of")

    def test_bad_id_format(self):
        self.cards[2]["id"] = "demo/002"
        self.save()
        self.assert_fails("units[0].cards[2].id (demo/002): 'demo/002' does not match")

    def test_bad_version(self):
        self.course["version"] = "1.0"
        self.save()
        self.assert_fails("demo/course.json: version: '1.0' does not match")

    # Rules a schema can't express

    def test_mcq_answer_out_of_range(self):
        self.cards[1]["answer"] = 2
        self.save()
        self.assert_fails("units[0].cards[1] (demo-001): answer 2 is out of range, there are 2 choices (0-1)")

    def test_unit_ending_with_learn_card(self):
        self.cards.append({"id": "demo-t02", "type": "learn", "title": "Last", "body": "Nothing after."})
        self.course["version"] = "1.1.0"
        self.save()
        self.assert_fails("units[0] (u1): ends with a learn card")

    def test_unquizzable_feature(self):
        self.cards[3]["feature"] = "BBB"
        self.course["version"] = "1.0.1"
        self.save()
        self.assert_fails("feature 'BBB' in map 'world' is not quizzable")

    def test_duplicate_card_id_across_courses(self):
        self.write("muna.json", {**INDEX, "courses": ["demo", "other"]})
        self.course.update(id="other", units=[{"id": "u1", "title": "One", "cards": [self.cards[2]]}])
        self.save("other")
        self.assert_fails("other/course.json: units[0].cards[0] (demo-002): duplicate card id, also in demo/course.json")

    def test_folder_name_differs_from_course_id(self):
        self.course["id"] = "demo-2"
        self.course["version"] = "1.0.1"
        self.save()
        self.assert_fails("demo/course.json: id 'demo-2' must equal its folder name 'demo'")

    def test_folder_missing_from_muna_json(self):
        self.course["id"] = "extra"
        self.course["units"][0]["cards"] = [{"id": "extra-001", "type": "text", "prompt": "?", "answers": ["x"]}]
        self.save("extra")
        self.assert_fails("extra/course.json: folder 'extra' is missing from muna.json")

    def test_listed_folder_missing(self):
        self.write("muna.json", {**INDEX, "courses": ["demo", "gone"]})
        self.assert_fails("muna.json: 'gone' is listed, but gone/course.json doesn't exist")

    # Against the base

    def test_change_without_version_bump(self):
        self.cards[2]["answers"].append("y")
        self.save()
        self.assert_fails("demo/course.json: changed since main, which needs a patch bump: version must be at least 1.0.1, not 1.0.0")

    def test_map_change_without_version_bump(self):
        self.write("demo/world.geojson", {**MAP, "features": MAP["features"][:1]})
        self.assert_fails("changed since main, which needs a patch bump")

    def test_new_card_needs_minor_bump(self):
        self.cards.append({"id": "demo-004", "type": "text", "prompt": "?", "answers": ["z"]})
        self.course["version"] = "1.0.1"
        self.save()
        self.assert_fails("adds demo-004 since main, which needs a minor bump: version must be at least 1.1.0, not 1.0.1")

    def test_removed_card_without_major_bump(self):
        del self.cards[2]
        self.course.update(version="1.1.0", retired=["demo-002"])
        self.save()
        self.assert_fails("removes demo-002 since main, which needs a major bump: version must be at least 2.0.0, not 1.1.0")

    def test_removed_card_missing_from_retired(self):
        del self.cards[2]
        self.course["version"] = "2.0.0"
        self.save()
        self.assert_fails("demo/course.json: demo-002 removed since main must be added to retired")

    def test_retired_shrinks(self):
        del self.cards[2]
        self.course.update(version="2.0.0", retired=["demo-002"])
        self.save()
        self.git("commit", "-qam", "retire demo-002")
        self.course.update(version="2.0.1", retired=[])
        self.save()
        self.assert_fails("retired only grows, but lost demo-002 since main")

    def test_card_using_retired_id(self):
        self.course["retired"] = ["demo-002"]
        self.course["version"] = "1.0.1"
        self.save()
        self.assert_fails("units[0].cards[2] (demo-002): id is retired in demo, so it can't be used again")


if __name__ == "__main__":
    unittest.main()
