#!/usr/bin/env python3
"""
Gender Decoder — deterministic core.

Faithful reproduction of the gender-coded-language scorer behind
gender-decoder.katmatfield.com, which implements the validated word list from:

    Gaucher, D., Friesen, J., & Kay, A. C. (2011).
    "Evidence That Gendered Wording in Job Advertisements Exists and
    Sustains Gender Inequality." Journal of Personality and Social
    Psychology, 101(1), 109-128.

This script is the *citable* layer: same input -> same verdict, every time.
It does NOT understand context (negation, sarcasm, off-list coded phrasing).
That is the LLM's job, layered on top per SKILL.md. Do not "improve" the word
lists or matching here — its value is being a faithful, reproducible instrument.

Usage:
    python3 decode.py path/to/job-ad.txt
    python3 decode.py < job-ad.txt
    echo "We need a confident, competitive leader" | python3 decode.py
    python3 decode.py --json path/to/job-ad.txt     # machine-readable only
"""

import json
import re
import sys

# --- Word lists (stems), verbatim from the Gender Decoder ---------------------
# A token counts as coded if it STARTS WITH one of these stems.

MASCULINE_CODED_STEMS = [
    "active", "adventurous", "aggress", "ambitio", "analy", "assert", "athlet",
    "autonom", "battle", "boast", "challeng", "champion", "compet", "confident",
    "courag", "decid", "decision", "decisive", "defend", "determin", "domina",
    "dominant", "driven", "fearless", "fight", "force", "greedy", "head-strong",
    "headstrong", "hierarch", "hostil", "impulsive", "independen", "individual",
    "intellect", "lead", "logic", "objective", "opinion", "outspoken", "persist",
    "principle", "reckless", "self-confiden", "self-relian", "self-sufficien",
    "selfconfiden", "selfrelian", "selfsufficien", "stubborn", "superior",
    "unreasonab",
]

FEMININE_CODED_STEMS = [
    "agree", "affectionate", "child", "cheer", "collab", "commit", "communal",
    "compassion", "connect", "considerate", "cooperat", "co-operat", "depend",
    "emotiona", "empath", "feel", "flatterable", "gentle", "honest",
    "interpersonal", "interdependen", "interpersona", "inter-personal",
    "inter-dependen", "inter-persona", "kind", "kinship", "loyal", "modesty",
    "nag", "nurtur", "pleasant", "polite", "quiet", "respon", "sensitiv",
    "submissive", "support", "sympath", "tender", "together", "trust",
    "understand", "warm", "whin", "enthusias", "inclusive", "yield", "share",
    "sharin",
]


def tokenize(text):
    """Lowercase, drop non-ASCII, split on punctuation — but keep hyphens,
    because several stems are hyphenated (co-operat, self-relian)."""
    ascii_text = "".join(c if ord(c) < 128 else " " for c in text)
    ascii_text = re.sub(r"\s", " ", ascii_text)
    cleaned = re.sub(r"""[\.\t,"""
                     + r"""“”‘’<>\*\?\!"\[\]@':;\(\)\./&]""", " ", ascii_text)
    return [w.lower() for w in cleaned.split(" ") if w]


def find_hits(tokens, stems):
    """Return list of (token, matched_stem) for every token starting with a stem."""
    hits = []
    for token in tokens:
        for stem in stems:
            if token.startswith(stem):
                hits.append((token, stem))
                break
    return hits


def assess(feminine_count, masculine_count):
    """Verdict thresholds, identical to the original tool."""
    score = feminine_count - masculine_count
    if score == 0:
        return ("neutral" if feminine_count else "empty"), score
    if score > 3:
        return "strongly feminine-coded", score
    if score > 0:
        return "feminine-coded", score
    if score < -3:
        return "strongly masculine-coded", score
    return "masculine-coded", score


def decode(text):
    tokens = tokenize(text)
    masc = find_hits(tokens, MASCULINE_CODED_STEMS)
    fem = find_hits(tokens, FEMININE_CODED_STEMS)
    verdict, score = assess(len(fem), len(masc))
    return {
        "verdict": verdict,
        "coding_score": score,  # feminine_count - masculine_count
        "masculine_count": len(masc),
        "feminine_count": len(fem),
        "masculine_words": [w for w, _ in masc],
        "feminine_words": [w for w, _ in fem],
        "word_count": len(tokens),
    }


VERDICT_LINE = {
    "empty": "No coded words found.",
    "neutral": "Neutral — equal masculine and feminine coding.",
    "feminine-coded": "Feminine-coded (mild).",
    "strongly feminine-coded": "STRONGLY feminine-coded.",
    "masculine-coded": "Masculine-coded (mild).",
    "strongly masculine-coded": "STRONGLY masculine-coded.",
}


def human_report(r):
    lines = []
    lines.append("=" * 60)
    lines.append(f"VERDICT: {r['verdict']}")
    lines.append(VERDICT_LINE[r["verdict"]])
    lines.append("=" * 60)
    lines.append(f"Masculine-coded hits : {r['masculine_count']}")
    lines.append(f"Feminine-coded hits  : {r['feminine_count']}")
    lines.append(f"Coding score (F - M) : {r['coding_score']}")
    lines.append(f"Total words          : {r['word_count']}")
    if r["masculine_words"]:
        lines.append("\nMasculine-coded words found:")
        lines.append("  " + ", ".join(r["masculine_words"]))
    if r["feminine_words"]:
        lines.append("\nFeminine-coded words found:")
        lines.append("  " + ", ".join(r["feminine_words"]))
    lines.append("\nNote: stem-matched and context-blind. Hand to the LLM step")
    lines.append("to strike false positives and catch off-list coded language.")
    return "\n".join(lines)


def main():
    args = [a for a in sys.argv[1:]]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]

    if args:
        with open(args[0], "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    result = decode(text)
    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(human_report(result))
        print("\n--- JSON ---")
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
