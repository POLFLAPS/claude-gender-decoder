# Coded word lists + rewrite guidance

The deterministic scoring lives in `decode.py` — these stems are mirrored here
so the LLM step can reason about hits and propose replacements without re-running
the script. **If you change a stem, change it in `decode.py` too** (the script is
the source of truth for the score).

## Source

Gaucher, D., Friesen, J., & Kay, A. C. (2011). *Evidence That Gendered Wording in
Job Advertisements Exists and Sustains Gender Inequality.* Journal of Personality
and Social Psychology, 101(1), 109–128.

Stem lists adapted from the open-source Gender Decoder by lovedaybrooke
(https://github.com/lovedaybrooke/gender-decoder), reused under the MIT License:

> The MIT License (MIT) — Copyright (c) 2016 lovedaybrooke. Permission is hereby
> granted, free of charge, to any person obtaining a copy of this software and
> associated documentation files (the "Software"), to deal in the Software without
> restriction… The above copyright notice and this permission notice shall be
> included in all copies or substantial portions of the Software.

(Full text: https://github.com/lovedaybrooke/gender-decoder/blob/master/License.md)

A token counts as coded if it **starts with** one of these stems (so `lead` catches
"leader", "leadership"; `respon` catches "responsible", "responsive").

## Masculine-coded stems (54)

active, adventurous, aggress, ambitio, analy, assert, athlet, autonom, battle,
boast, challeng, champion, compet, confident, courag, decid, decision, decisive,
defend, determin, domina, dominant, driven, fearless, fight, force, greedy,
head-strong, headstrong, hierarch, hostil, impulsive, independen, individual,
intellect, lead, logic, objective, opinion, outspoken, persist, principle,
reckless, self-confiden, self-relian, self-sufficien, selfconfiden, selfrelian,
selfsufficien, stubborn, superior, unreasonab

## Feminine-coded stems (50)

agree, affectionate, child, cheer, collab, commit, communal, compassion, connect,
considerate, cooperat, co-operat, depend, emotiona, empath, feel, flatterable,
gentle, honest, interpersonal, interdependen, interpersona, inter-personal,
inter-dependen, inter-persona, kind, kinship, loyal, modesty, nag, nurtur,
pleasant, polite, quiet, respon, sensitiv, submissive, support, sympath, tender,
together, trust, understand, warm, whin, enthusias, inclusive, yield, share, sharin

## Neutral-rewrite patterns

The goal is **balance, not erasure** — a JD with zero personality is also a bad JD.
Rewrite to describe the *work and outcomes* rather than personality traits. Examples:

| Coded phrasing | Neutral alternative |
|----------------|---------------------|
| "competitive, driven self-starter" | "motivated by clear goals; works independently" |
| "dominant player, crush the competition" | "grow our market share" |
| "strong, confident leader" | "guides the team and owns decisions" |
| "aggressive growth targets" | "ambitious, measurable growth targets" (or restate the number) |
| "ninja / rockstar / guru" | name the actual skill ("expert in X") |
| "supportive, nurturing team player" | "collaborates closely and shares knowledge" |
| "we're a family" | "we support each other and value the team" |

## Watch for false positives (the LLM's job)

Stem matching is dumb. Flag, don't silently trust:
- **Negation** — "we don't tolerate aggressive behavior" scores masculine but isn't.
- **Domain words** — "objective" (a goal), "decision" (a database term), "active"
  (an active record), "principle" vs "principal", "share" (equity/shares).
- **Off-list coded language** the 2011 list misses: rockstar, ninja, guru, hacker,
  "work hard play hard", "no excuses", "thick skin", "high-pressure", "world-class".
