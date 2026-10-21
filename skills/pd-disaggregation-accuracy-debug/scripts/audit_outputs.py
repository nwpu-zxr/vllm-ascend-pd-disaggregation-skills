#!/usr/bin/env python3
"""Audit normalized generated outputs; standard library only, no accuracy verdict."""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Three adjacent copies of a 16..128-character span, over bounded text windows.
REPEATED_SPAN = re.compile(r"(.{16,128}?)\1{2,}", re.DOTALL)
WINDOW = 8192


def repeated_span(text):
    windows = [(0, text[:WINDOW])]
    if len(text) > WINDOW:
        offset = len(text) - WINDOW
        windows.append((offset, text[offset:]))
    for offset, part in windows:
        match = REPEATED_SPAN.search(part)
        if match:
            return {
                "start_character": offset + match.start(),
                "span_characters": len(match.group(1)),
                "adjacent_copies": len(match.group(0)) // len(match.group(1)),
            }
    return None


def validate(record, line_number, seen):
    def invalid(reason):
        # Never echo malformed data, generated text or credentials from input.
        raise ValueError(f"line {line_number}: {reason}")

    if not isinstance(record, dict):
        invalid("expected a JSON object")
    if not isinstance(record.get("id"), str) or not record["id"]:
        invalid("id must be a nonempty string")
    if record["id"] in seen:
        invalid("duplicate id; assign unique IDs to response attempts")
    if not isinstance(record.get("text"), str):
        invalid("text must be a generated-output string")
    for key in ("output_tokens", "max_output_tokens"):
        value = record.get(key)
        if value is not None and (type(value) is not int or value < 0):
            invalid(f"{key} must be a nonnegative integer or null")
    if record.get("max_output_tokens") == 0:
        invalid("max_output_tokens must be positive when supplied")
    if record.get("finish_reason") is not None and not isinstance(record["finish_reason"], str):
        invalid("finish_reason must be a string or null")
    if record.get("correct") is not None and type(record["correct"]) is not bool:
        invalid("correct must be boolean or null")
    seen.add(record["id"])


def audit(records, expect_think_close=False):
    totals = Counter({key: 0 for key in (
        "samples", "closing_tag_zero", "closing_tag_one", "closing_tag_multiple",
        "missing_expected_closing_tag", "explicit_length_limit", "suspected_length_limit",
        "unknown_length_status", "no_length_limit_reported",
        "replacement_character_samples", "repetition_candidates",
        "correct_known", "correct_true", "correct_false", "correct_unknown",
    )})
    samples = []
    for record in records:
        text = record["text"]
        closing = text.count("</think>")
        reason = record.get("finish_reason")
        count, limit = record.get("output_tokens"), record.get("max_output_tokens")
        at_budget = count is not None and limit is not None and count >= limit
        if reason in ("length", "max_tokens", "max_output_tokens"):
            length_status = "explicit_length_limit"
        elif at_budget:
            length_status = "suspected_length_limit"
        elif reason in ("stop", "eos_token", "end_turn", "tool_calls", "function_call"):
            length_status = "no_length_limit_reported"
        else:
            length_status = "unknown_length_status"
        repeated = repeated_span(text)
        correct = record.get("correct")
        totals["samples"] += 1
        totals["closing_tag_zero" if closing == 0 else
               "closing_tag_one" if closing == 1 else "closing_tag_multiple"] += 1
        totals["missing_expected_closing_tag"] += int(expect_think_close and closing == 0)
        totals[length_status] += 1
        totals["replacement_character_samples"] += int("\ufffd" in text)
        totals["repetition_candidates"] += int(repeated is not None)
        totals["correct_unknown" if correct is None else "correct_known"] += 1
        if correct is not None:
            totals["correct_true" if correct else "correct_false"] += 1
        samples.append({
            "id": record["id"], "characters": len(text),
            "output_tokens": count, "max_output_tokens": limit,
            "finish_reason": reason, "opening_tags": text.count("<think>"),
            "closing_tags": closing, "length_status": length_status,
            "replacement_characters": text.count("\ufffd"),
            "repetition_candidate": repeated,
            "repetition_characters_scanned": min(len(text), 2 * WINDOW),
            "correct": correct,
        })
    return {
        "schema_version": 1, "expect_think_close": expect_think_close,
        "scope": "Heuristic candidate selection; no model tokenization or accuracy verdict. "
                 "Text is omitted; IDs and metadata remain visible. Repetition checks only "
                 "the first/last 8192 characters for three adjacent 16..128-character spans.",
        "summary": dict(totals), "samples": samples,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Normalized JSONL, one complete response attempt per line")
    parser.add_argument("--expect-think-close", action="store_true",
                        help="Mark zero closing tags only when the output contract requires one")
    args = parser.parse_args()
    records, seen = [], set()
    try:
        with args.input.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    raise ValueError(f"line {line_number}: invalid JSON") from None
                validate(record, line_number, seen)
                records.append(record)
        if not records:
            raise ValueError("input contains no response records")
    except (OSError, UnicodeError, ValueError) as error:
        print(f"audit_outputs: {error}", file=sys.stderr)
        return 2
    json.dump(audit(records, args.expect_think_close), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
