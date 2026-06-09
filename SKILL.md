---
name: gender-decoder
description: Use when checking or fixing a job ad, job description (JD), careers page, recruiter outreach, or any hiring copy for subtly gender-coded language. Detects masculine-coded and feminine-coded wording (Gaucher, Friesen & Kay 2011), returns a verdict from strongly masculine-coded to strongly feminine-coded, then proposes neutral replacements and a balanced rewrite. Keywords: gender-coded, gendered wording, biased job ad, inclusive hiring, gender decoder.
---

# Gender Decoder

## Overview

Job ads with masculine-coded language ("competitive", "dominant", "driven") make
roles less appealing to women and lower their sense of belonging — without changing
how men read them (Gaucher, Friesen & Kay, 2011). This skill flags that coding and
helps fix it.

**Hybrid by design:**
- `decode.py` is the **citable, reproducible** core — it implements the validated
  word list exactly, so the verdict matches the public Gender Decoder and is
  defensible ("we ran it through the Gaucher et al. instrument").
- **You (the LLM)** are the smart editor layered on top: strike the script's
  false positives, catch coded language the 1980s/2011 list misses, and write the
  balanced rewrite.

Never present a model-invented "bias score" — the *number* always comes from the
script. Your contextual judgment is labelled as commentary, not measurement.

## When to use

- Reviewing or writing a JD, careers-page blurb, or recruiter outreach
- Someone asks "is this job ad biased / inclusive / off-putting to women?"
- Final pass before a role goes live

## Process

1. **Get the text.** Use the JD/ad as plain text. If it's in a file, point the
   script at it; otherwise pipe it via stdin.

2. **Run the deterministic decode:**
   ```bash
   python3 decode.py path/to/job-ad.txt
   # or:  pbpaste | python3 decode.py     # from clipboard (macOS)
   # or:  python3 decode.py < draft.txt
   ```
   This returns the verdict, the masculine/feminine counts, the coding score
   (feminine − masculine), and the exact words matched.

3. **Report the verdict** in a short table: verdict, counts, coding score, and the
   flagged words grouped masculine vs feminine.

4. **Context review (the part the original tool can't do).** Go through the flagged
   words and:
   - **Strike false positives** — negation ("don't tolerate aggressive behavior"),
     domain terms ("objective" = a goal, "share" = equity, "active record").
     Say which hits you're discounting and why.
   - **Add off-list catches** — coded phrasing the 2011 list misses: rockstar,
     ninja, guru, "work hard / play hard", "thick skin", "no excuses", "world-class".
   See `references/wordlists.md` for the lists and common traps.

5. **Propose neutral replacements** for each genuine hit — describe the *work and
   outcomes*, not personality traits. Aim for **balance, not a sterile JD**.
   Replacement patterns are in `references/wordlists.md`.

6. **Offer a balanced rewrite** of the full ad with the changes applied.

## Verdict scale

| Coding score (F − M) | Verdict |
|----------------------|---------|
| both counts 0 | no coded words found |
| 0 (with hits) | neutral |
| +1 to +3 | feminine-coded |
| > +3 | strongly feminine-coded |
| −1 to −3 | masculine-coded |
| < −3 | strongly masculine-coded |

Masculine-coded is the one that measurably deters candidates — prioritise fixing
those. A mild feminine lean is far less of a problem.

## Caveats — state these, don't hide them

- **Binary framing.** The underlying research only studied masculine vs feminine
  coding and excluded non-binary participants and non-binary-coded language. This is
  a directional signal, not a verdict on a JD's overall inclusivity.
- **"Neutral" ≠ bias-free.** The score says nothing about ageism, ableist phrasing,
  unnecessary requirements, or tone. Read the whole ad.
- **English-only.** The stem list is English. It will mis-score non-English JDs —
  flag that and assess non-English copy qualitatively instead of trusting the number.
- **Stem matching is crude** — that's exactly why step 4 (the context review) is
  mandatory, not optional.

## Source & credits

- **Research:** Gaucher, D., Friesen, J., & Kay, A. C. (2011). *Evidence That
  Gendered Wording in Job Advertisements Exists and Sustains Gender Inequality.*
  Journal of Personality and Social Psychology, 101(1), 109–128.
- **Word lists & algorithm:** adapted from the open-source Gender Decoder by
  lovedaybrooke — https://github.com/lovedaybrooke/gender-decoder (MIT License,
  © 2016 lovedaybrooke), live at https://gender-decoder.katmatfield.com.
  `decode.py` is an independent reimplementation; the curated stem lists are reused
  under MIT. See `LICENSE`.
