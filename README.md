# claude-gender-decoder

A [Claude Code](https://claude.com/claude-code) skill that checks job ads for
subtly **gender-coded language** — and helps you fix it.

It's a **hybrid** of a deterministic scorer and an LLM:

- **`decode.py`** reproduces the validated word-list method from the research, so
  the verdict is reproducible and citable — the same JD always scores the same.
- **The LLM** layers context on top: it strikes false positives the word list
  can't (negation, domain terms), catches coded phrasing the list misses
  ("rockstar", "work hard / play hard"), and writes a balanced rewrite.

Based on Gaucher, Friesen & Kay (2011), *Evidence That Gendered Wording in Job
Advertisements Exists and Sustains Gender Inequality.* Masculine-coded wording
("competitive", "dominant", "driven") makes roles less appealing to women and
lowers their sense of belonging; feminine-coded wording has little effect on men.

## Install (as a Claude Code skill)

Clone into your skills directory:

```bash
git clone https://github.com/POLFLAPS/claude-gender-decoder.git \
  ~/.claude/skills/gender-decoder
```

Then in Claude Code:

```
/gender-decoder paste-or-point-at-your-JD
```

Claude runs the decoder, reports the verdict, reviews the flagged words in
context, and offers a neutral rewrite.

## Use the scorer on its own (no Claude required)

`decode.py` is plain Python 3, standard library only:

```bash
python3 decode.py path/to/job-ad.txt        # human-readable + JSON
python3 decode.py --json path/to/job-ad.txt  # JSON only
echo "We need a confident, competitive leader" | python3 decode.py
```

Example output:

```
VERDICT: strongly masculine-coded
Masculine-coded hits : 5
Feminine-coded hits  : 0
Coding score (F - M) : -5
Masculine-coded words found:
  competitive, confident, ambitious, leader, dominate
```

## Verdict scale

| Coding score (feminine − masculine) | Verdict |
|---|---|
| both 0 | no coded words |
| 0 (with hits) | neutral |
| +1 … +3 | feminine-coded |
| > +3 | strongly feminine-coded |
| −1 … −3 | masculine-coded |
| < −3 | strongly masculine-coded |

Masculine-coded is the verdict that measurably deters candidates — prioritise
fixing those.

## Caveats

- **Binary framing** — the research only studied masculine vs feminine coding and
  excluded non-binary participants/language. Directional signal, not a full
  inclusivity audit.
- **"Neutral" ≠ bias-free** — says nothing about ageism, ableist phrasing, or
  unnecessary requirements. Read the whole ad.
- **English-only** word list — it will mis-score non-English JDs.
- **Stem matching is crude** — which is why the LLM context-review step matters.

## Tests

```bash
python3 tests.py
```

## Credits & license

- **Research:** Gaucher, D., Friesen, J., & Kay, A. C. (2011), *J. Personality &
  Social Psychology*, 101(1), 109–128.
- **Word lists & algorithm:** adapted from the open-source
  [Gender Decoder by lovedaybrooke](https://github.com/lovedaybrooke/gender-decoder)
  (MIT, © 2016 lovedaybrooke), live at
  [gender-decoder.katmatfield.com](https://gender-decoder.katmatfield.com).

MIT licensed — see [`LICENSE`](LICENSE). The license carries both copyright
notices.
