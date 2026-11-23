---
name: "saudi-riyal-symbol"
description: "Use whenever an output shows Saudi riyal amounts (ريال, ر.س, SAR) — PDFs, HTML, charts, Word, PowerPoint, Excel — to set the \u20C1 symbol per SAMA's usage guidelines."
---

# Saudi Riyal symbol (⃁) per SAMA guidelines

Any amount in Saudi riyals in a deliverable uses the official symbol, set the way the Saudi Central Bank (SAMA) guide prescribes. Apply it silently in every medium where the font can be controlled; say so in one line when a medium cannot show it.

## Facts to rely on
- Approved 20 February 2025; announced by SAMA.
- Unicode: **U+20C1 SAUDI RIYAL SIGN** (Unicode 17.0, September 2025). Most system and web fonts do not have the glyph yet, so it shows as an empty box unless a font that has it is supplied.
- Official guide: SAMA, «دليل استخدام رمز الريال السعودي», usage rules on pp. 16–17 — https://www.sama.gov.sa/ar-sa/Currency/SRS/Documents/Guidelines.pdf (sama.gov.sa often refuses automated downloads; cite it, don't depend on fetching it).
- **Use SAMA's official artwork only** — the files in this skill's `assets/` folder. Never use third-party "riyal fonts" or redraw the symbol: their outlines and stroke weights differ from SAMA's.
- The official symbol has **one weight**. There is no bold or light version; never synthesise one.

## Bundled files (paths relative to this skill's folder)
| File | What it is | Use it for |
|---|---|---|
| `assets/sar-symbol.otf` | 1 KB font; its only glyph, U+20C1, is SAMA's outline scaled uniformly to 0.70 em | Text in HTML, PDF, charts, Office files — copy it next to the output |
| `assets/sama-riyal-symbol.svg` | SAMA's official vector file, unmodified | Inline graphic where a font can't be used; the reference to check shapes against |
| `assets/sama-riyal-symbol.png` | SAMA's official raster file, 3000 × 3353 px | Word/PowerPoint when the font can't be embedded |
| `assets/SOURCE.md` | Provenance and checksum | Citing the source |
| `scripts/sar_font.py` | Builds the font from the SVG | Only if SAMA issues a new file |

The SVG's fill is `#231f20`; in use, fill the symbol with the text colour (`currentColor`), per rule 10. SAMA also publishes an EPS for print and design tools; it is not bundled here.

**Match the body font's digit height (rule 7) with CSS, not a rebuild:** the symbol's `font-size` = digit height ÷ 0.70, where digit height is the top of the body font's «1» in em. Measure it with `python3 -c "import sys; sys.path.insert(0, 'scripts'); from sar_font import digit_height; print(digit_height('BODY.ttf') / 700)"` (run from the skill folder; prints the em factor). IBM Plex Sans Arabic ≈ 1.0em; Tajawal ≈ 0.90em. Check by rendering: the symbol's top meets the top of the digits.

**Rebuild** (only for a new SAMA file): `python3 scripts/sar_font.py NEW.svg assets/sar-symbol.otf --height 700`, then render the glyph large beside the SVG — they must be the same shape — and update the checksum in `SOURCE.md`. With the current SVG this rebuild gives the same glyph and metrics as the bundled font; only the build timestamp, and so the checksum, differs.

## SAMA usage rules (guide p. 17)
1. **Position:** the symbol sits to the **left** of the numeral, in every language.
2. **Spacing:** a space between symbol and numeral — use a no-break space (U+00A0) so they never split across lines.
3. **Written values:** with a written unit the symbol goes left of the unit: «10.71 مليون ⃁».
4. **Negative values:** the symbol goes left of both the minus sign and the numeral: ⃁ -1,250.
5–6. **Proportions and geometry:** never stretch, skew, redraw or substitute a look-alike.
7. **Alignment:** symbol height matches the surrounding text height.
8. **Direction:** follows the text direction.
9. **Clear space:** inside shapes/badges, keep clear space of one-third of the symbol's height around it.
10. **Contrast:** sufficient contrast with the background; same colour as the amount.

## Logical order (the part that goes wrong)
"Left of the number" is a visual rule. In Unicode text:
- **Arabic (RTL) text:** amount, NBSP, symbol — `10,713,120 ⃁`, `10.71 مليون ⃁`. The RTL paragraph puts the symbol on the left.
- **English (LTR) text:** symbol, NBSP, amount — `⃁ 1,250`.
- **Negatives, or any place where direction is uncertain** (table cells of mixed direction, labels in charts): wrap in an LTR isolate with the symbol first — `<span dir="ltr" style="unicode-bidi:isolate">⃁ -1,250</span>`. This renders symbol-left in both languages.
- Never put the symbol before the amount in Arabic logical order; it lands on the right.

## Converting existing text
Replace riyal words that follow an amount; leave the word in prose (كل ريال، بالريال، لا يُصرف ريال).

```python
import re
SAR_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)((?:\s+(?:مليون|ملايين|ألف|آلاف|مليار|مليارات))?)\s+(?:ريالًا|ريالا|ريال|ر\.س)(?![ء-ي])")
def sar(text, sym=' <span class="sar">⃁</span>'):
    text = SAR_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}{sym}", text)
    return text.replace("(ر.س)", '(<span class="sar">⃁</span>)')   # unit labels in table headers
```
- «ر.س.» at a sentence end: match only «ر.س» so the full stop survives.
- English «SAR 1,250» / «1,250 SAR» → `⃁ 1,250`.
- Don't touch quoted legal text or names of documents that contain «ريال».

## Per medium
- **HTML / PDF (Chromium or WeasyPrint):** copy `assets/sar-symbol.otf` next to the output and embed it. Either a class on the symbol — `@font-face{font-family:SAR;src:url(sar-symbol.otf)}` + `.sar{font-family:SAR;font-weight:normal;font-style:normal;font-synthesis:none}` — or, in Chromium, add a face under the body font's own family name with `unicode-range:U+20C1`, so plain text needs no span. WeasyPrint: use the class approach. Check `pdffonts out.pdf` lists the SAR font as embedded.
- **When a font can't be used** (an image-only design tool, a slide template, signage): place `assets/sama-riyal-symbol.svg` (or SAMA's EPS, in print tools) as an inline graphic, scaled uniformly to the digit height, filled with the text colour, sitting on the baseline: `<svg viewBox="0 0 1124.14 1256.39" style="height:0.7em;width:auto;vertical-align:baseline;fill:currentColor">…</svg>`.
- **Charts:** SVG text needs the font too. When rasterising with Chromium, use the unicode-range face; WeasyPrint's SVG renderer mangles Arabic, so rasterise charts with Chromium (deviceScaleFactor 4) and embed the PNG. matplotlib: register `assets/sar-symbol.otf` with `font_manager.fontManager.addfont` and list it as a fallback family.
- **Excel (openpyxl):** number format with the symbol first, e.g. `'"⃁" #,##0'` (visual left in both directions), and set the cell font to one that has U+20C1. If the recipient's machine lacks such a font it shows a box: tell the user in one line.
- **Word / PowerPoint:** put the symbol in its own run in the SAR font and embed the font when the tool allows. If it cannot be embedded, insert `assets/sama-riyal-symbol.png` inline at digit height instead, or keep «ريال» and say why in one line — never risk an empty box.
- **Docs or pages where the font can't be set (Claude Docs, chat replies, email):** keep «ريال»/«ر.س»; don't emit U+20C1.

## Verify before delivering
- Render the page and look: the symbol is left of the amount, same height as the digits, not on its own line, no empty boxes.
- Count conversions (`text.count('⃁')`) and grep for leftover «ر.س» next to numbers.
- Bold contexts (headers, highlighted chart labels) keep the single official weight: no faux bold (`font-synthesis:none`), no added stroke.
- The symbol's shape matches SAMA's file, and nothing from a third-party riyal font is in the output (`pdffonts` shows only the SAR Symbol font).