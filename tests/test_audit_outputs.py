import importlib.util
import json
from pathlib import Path
import random
import string
import subprocess
import sys
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "skills" /
          "pd-disaggregation-accuracy-debug" / "scripts" / "audit_outputs.py")
SPEC = importlib.util.spec_from_file_location("audit_outputs", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class OutputAuditTests(unittest.TestCase):
    def run_cli(self, text, *options):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "outputs.jsonl"
            source.write_text(text, encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), str(source), *options],
                                  capture_output=True, text=True, check=False)

    def test_tag_and_correctness_summary(self):
        records = [
            {"id": "a", "text": "<think>reason</think>answer", "correct": True},
            {"id": "b", "text": "unfinished", "correct": False},
            {"id": "c", "text": "</think>answer</think>\ufffd"},
        ]
        summary = AUDIT.audit(records, True)["summary"]
        self.assertEqual(summary["samples"], 3)
        self.assertEqual(summary["closing_tag_zero"], 1)
        self.assertEqual(summary["closing_tag_one"], 1)
        self.assertEqual(summary["closing_tag_multiple"], 1)
        self.assertEqual(summary["correct_known"], 2)
        self.assertEqual(summary["correct_true"], 1)
        self.assertEqual(summary["correct_false"], 1)
        self.assertEqual(summary["correct_unknown"], 1)
        self.assertEqual(summary["replacement_character_samples"], 1)

    def test_missing_tag_requires_opt_in(self):
        record = [{"id": "a", "text": "plain answer"}]
        self.assertEqual(AUDIT.audit(record)["summary"]["missing_expected_closing_tag"], 0)
        self.assertEqual(AUDIT.audit(record, True)["summary"]["missing_expected_closing_tag"], 1)

    def test_length_evidence_is_not_invented(self):
        variants = [
            ({"finish_reason": "length"}, "explicit_length_limit"),
            ({"output_tokens": 8, "max_output_tokens": 8}, "suspected_length_limit"),
            ({"output_tokens": 2, "max_output_tokens": 8}, "unknown_length_status"),
            ({"finish_reason": "stop"}, "no_length_limit_reported"),
            ({"finish_reason": "error"}, "unknown_length_status"),
        ]
        for fields, expected in variants:
            with self.subTest(fields=fields):
                sample = AUDIT.audit([dict(id="a", text="answer", **fields)])["samples"][0]
                self.assertEqual(sample["length_status"], expected)

    def test_repetition_crossing_original_split(self):
        rng = random.Random(42)
        noise = lambda n: "".join(rng.choices(string.ascii_letters + string.digits, k=n))
        text = noise(8190) + "abcdefghijklmnop" * 3 + noise(800)
        sample = AUDIT.audit([{"id": "a", "text": text}])["samples"][0]
        self.assertEqual(sample["repetition_candidate"]["start_character"], 8190)
        self.assertEqual(sample["repetition_characters_scanned"], len(text))

    def test_unscanned_middle_remains_a_documented_limit(self):
        rng = random.Random(43)
        noise = lambda n: "".join(rng.choices(string.ascii_letters + string.digits, k=n))
        text = noise(17000) + "abcdefghijklmnop" * 4 + noise(17000)
        sample = AUDIT.audit([{"id": "a", "text": text}])["samples"][0]
        self.assertIsNone(sample["repetition_candidate"])
        self.assertEqual(sample["repetition_characters_scanned"], 16384)

    def test_cli_omits_generated_text(self):
        result = self.run_cli(json.dumps({"id": "case-1", "text": "PRIVATE-GENERATED-CONTENT"}))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("PRIVATE-GENERATED-CONTENT", result.stdout)
        self.assertEqual(json.loads(result.stdout)["samples"][0]["id"], "case-1")

    def test_invalid_input_has_no_partial_report(self):
        cases = [
            "",
            "{PRIVATE-MALFORMED-CONTENT}",
            json.dumps({"id": "a"}),
            json.dumps({"id": "a", "text": "PRIVATE", "output_tokens": True}),
            json.dumps({"id": "a", "text": "PRIVATE", "max_output_tokens": 0}),
            json.dumps({"id": "a", "text": "PRIVATE", "correct": "true"}),
            '\n'.join([json.dumps({"id": "a", "text": "PRIVATE"})] * 2),
        ]
        for case in cases:
            with self.subTest(case_index=cases.index(case)):
                result = self.run_cli(case)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("PRIVATE", result.stderr)


if __name__ == "__main__":
    unittest.main()
