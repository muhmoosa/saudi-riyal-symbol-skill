# Saudi Riyal symbol (⃁) — Agent Skill

An [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that makes Claude (and other skill-aware agents) set Saudi riyal amounts with the official symbol **⃁** (U+20C1 SAUDI RIYAL SIGN), following the Saudi Central Bank (SAMA) usage guide — in chat replies and email as well as HTML, PDF, charts, Word, PowerPoint and Excel.

U+20C1 is in Unicode 17.0 and the major operating systems display it in plain text, so the agent writes the symbol directly in chat replies and email, falling back to «ر.س» only where it truly cannot be shown. For files it produces, this skill ships a 1 KB font built from SAMA's official artwork, so the symbol keeps SAMA's exact shape everywhere, and tells the agent how to place it correctly: left of the number, no-break space, correct bidi order in Arabic text, negatives, matching digit height, one weight only.

## Install

**Claude Code (plugin marketplace)**
```
/plugin marketplace add muhmoosa/saudi-riyal-symbol-skill
/plugin install saudi-riyal-symbol@saudi-riyal-symbol-skill
```

**skills CLI**
```
npx skills add muhmoosa/saudi-riyal-symbol-skill
```

**Manually** — copy `skills/saudi-riyal-symbol/` into `~/.claude/skills/`, or zip that folder and upload it in Claude.ai → Settings → Capabilities → Skills.

## Contents
```
skills/saudi-riyal-symbol/
├── SKILL.md                     instructions and SAMA's usage rules
├── assets/sar-symbol.otf        one-glyph font (U+20C1), SAMA outline at 0.70 em
├── assets/sama-riyal-symbol.svg SAMA's official vector file, unmodified
├── assets/sama-riyal-symbol.png SAMA's official raster file, unmodified
├── assets/SOURCE.md             provenance and checksum
└── scripts/sar_font.py          rebuilds the font from a new SAMA SVG
```

## Sources
- SAMA, «دليل استخدام رمز الريال السعودي» (Saudi Riyal Symbol Usage Guide), usage rules pp. 16–17 — https://www.sama.gov.sa/ar-sa/Currency/SRS/Documents/Guidelines.pdf
- Unicode 17.0, U+20C1 SAUDI RIYAL SIGN.

## Licence
The skill's text and script are under the MIT licence (see `LICENSE`).
The Saudi Riyal symbol and its official artwork (`assets/sama-riyal-symbol.svg`, `assets/sama-riyal-symbol.png`, and the glyph outline in `assets/sar-symbol.otf`) belong to the Saudi Central Bank (SAMA). They are included unmodified, as SAMA published them, to help apply the symbol correctly; they are not covered by the MIT licence.

## Author
Mohammed Al-Mousa ([@muhmoosa](https://github.com/muhmoosa))
