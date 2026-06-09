#!/usr/bin/env python3
"""Smoke tests for decode.py. Run: python3 tests.py"""

from decode import decode


def check(name, text, expected_verdict, expected_score):
    r = decode(text)
    ok = r["verdict"] == expected_verdict and r["coding_score"] == expected_score
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}: verdict={r['verdict']!r} score={r['coding_score']}")
    if not ok:
        print(f"        expected verdict={expected_verdict!r} score={expected_score}")
    return ok


def main():
    results = [
        check(
            "masculine sample",
            "We need a competitive, confident, ambitious leader who can dominate the market.",
            "strongly masculine-coded", -5,
        ),
        check(
            "feminine sample",
            "We want a supportive, collaborative, empathetic team player who is honest and kind.",
            "strongly feminine-coded", 5,
        ),
        check("empty", "", "empty", 0),
        check(
            "hyphenated stems balance to neutral",
            "A self-reliant and co-operative person.",
            "neutral", 0,
        ),
    ]
    passed = sum(results)
    print(f"\n{passed}/{len(results)} passed")
    raise SystemExit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
