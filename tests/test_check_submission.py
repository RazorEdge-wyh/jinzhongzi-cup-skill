"""Tests for skills/jinzhongzi-cup/scripts/check_submission.py.

Run: python -m unittest discover -s tests -v
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "jinzhongzi-cup"
SCRIPT = SKILL / "scripts" / "check_submission.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_module():
    spec = importlib.util.spec_from_file_location("check_submission", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


cs = load_module()


class TestSections(unittest.TestCase):
    def test_good_plan_has_all_sections(self):
        text = (FIXTURES / "plan_good.md").read_text(encoding="utf-8")
        errors, found = cs.check_sections(text, "plan")
        self.assertEqual(errors, [])
        self.assertEqual(len(found), len(cs.REQUIRED_SECTIONS["plan"]))

    def test_bad_plan_missing_sections(self):
        text = (FIXTURES / "plan_bad.md").read_text(encoding="utf-8")
        errors, _ = cs.check_sections(text, "plan")
        self.assertTrue(errors)
        self.assertTrue(any("团队" in e or "财务" in e for e in errors))


class TestEvidence(unittest.TestCase):
    def test_filler_detected(self):
        text = (FIXTURES / "plan_bad.md").read_text(encoding="utf-8")
        hits = cs.check_filler(text)
        words = {h["word"] for h in hits}
        self.assertIn("国际领先", words)
        self.assertIn("填补空白", words)

    def test_annotation_leak_detected(self):
        text = (FIXTURES / "plan_bad.md").read_text(encoding="utf-8")
        leaks = cs.check_annotations(text)
        marks = " ".join(a["mark"] for a in leaks)
        self.assertIn("[待补]", marks)
        self.assertIn("⚠️", marks)

    def test_label_style_detected(self):
        text = (FIXTURES / "plan_bad.md").read_text(encoding="utf-8")
        labels = cs.check_label_style(text)
        self.assertIn("定位宣言", labels)

    def test_markers_counted(self):
        text = (FIXTURES / "plan_good.md").read_text(encoding="utf-8")
        warnings, counts = cs.check_markers(text)
        self.assertGreater(counts["实测"], 0)
        self.assertGreater(counts["估算"], 0)
        self.assertEqual(counts["待补"], 0)

    def test_unsourced_claim_detected(self):
        text = (FIXTURES / "plan_bad.md").read_text(encoding="utf-8")
        missing = cs.check_claims(text)
        self.assertGreater(len(missing), 0)


class TestCitations(unittest.TestCase):
    def test_citation_mismatch_is_error(self):
        text = (FIXTURES / "paper_bad_citations.md").read_text(encoding="utf-8")
        errors, warnings = cs.check_citations(text)
        joined = " ".join(errors)
        self.assertIn("缺失的序号", joined)  # [2] and [3] missing
        self.assertTrue(any("幽灵引用" in w for w in warnings))  # [5] unused

    def test_good_references_pass(self):
        text = (FIXTURES / "plan_good.md").read_text(encoding="utf-8")
        errors, warnings = cs.check_citations(text)
        self.assertEqual(errors, [])


class TestMapping(unittest.TestCase):
    def test_mapping_required_for_plan(self):
        text = (FIXTURES / "plan_bad.md").read_text(encoding="utf-8")
        self.assertTrue(cs.check_mapping(text))

    def test_mapping_present_in_good_plan(self):
        text = (FIXTURES / "plan_good.md").read_text(encoding="utf-8")
        self.assertEqual(cs.check_mapping(text), [])

    def test_mapping_skeleton_has_dimensions(self):
        skeleton = cs.mapping_skeleton(["痛点", "团队"])
        for dim in ("产品创新与技术突破", "财务分析与融资规划", "社会价值与持续发展"):
            self.assertIn(dim, skeleton)


class TestCli(unittest.TestCase):
    def run_cli(self, *args: str):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

    def test_version(self):
        r = self.run_cli("--version")
        self.assertEqual(r.returncode, 0)
        self.assertIn(cs.__version__, r.stdout)

    def test_mapping_flag(self):
        r = self.run_cli("--mapping")
        self.assertEqual(r.returncode, 0)
        self.assertIn("评分维度", r.stdout)

    def test_good_plan_passes_cli(self):
        r = self.run_cli(str(FIXTURES / "plan_good.md"), "--kind", "plan")
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    def test_bad_plan_fails_cli(self):
        r = self.run_cli(str(FIXTURES / "plan_bad.md"), "--kind", "plan")
        self.assertEqual(r.returncode, 1, msg=r.stdout + r.stderr)

    def test_json_output(self):
        r = self.run_cli(str(FIXTURES / "plan_good.md"), "--kind", "plan", "--json")
        self.assertEqual(r.returncode, 0)
        import json

        data = json.loads(r.stdout)
        self.assertIn("dimension_coverage", data)


if __name__ == "__main__":
    unittest.main()
