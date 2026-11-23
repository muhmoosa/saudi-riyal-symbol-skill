"""Build sar-symbol.otf (one glyph, U+20C1) from SAMA's official SVG.
The outline is only scaled uniformly (SAMA rules 5-6); --height 700 reproduces the glyph and metrics of assets/sar-symbol.otf (only the build timestamp differs).
usage: python3 sar_font.py OFFICIAL.svg OUT.otf [--height 700 | --match BODYFONT.ttf]
"""
import argparse, re
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont
UPM = 1000
def digit_height(path):                      # height of '1' (no overshoot) in a 1000-unit em
    f = TTFont(path); gs = f.getGlyphSet(); p = BoundsPen(gs)
    gs[f.getBestCmap()[ord("1")]].draw(p); return p.bounds[3] * UPM / f["head"].unitsPerEm
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("svg"); ap.add_argument("out")
    ap.add_argument("--match"); ap.add_argument("--height", type=float, default=700)
    a = ap.parse_args()
    target = digit_height(a.match) if a.match else a.height
    svg = open(a.svg, encoding="utf-8").read()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    w, h = vb[2], vb[3]; s = target / h; side = round(0.08 * target); adv = round(w * s) + 2 * side
    cs = T2CharStringPen(adv, None)
    tp = TransformPen(cs, (s, 0, 0, -s, side - vb[0] * s, (vb[1] + h) * s))   # flip y, uniform scale
    for d in re.findall(r'<path[^>]*\sd="([^"]+)"', svg): parse_path(d, tp)
    fb = FontBuilder(UPM, isTTF=False)
    fb.setupGlyphOrder([".notdef", "space", "uni20C1"])
    fb.setupCharacterMap({0x20: "space", 0x20C1: "uni20C1"})
    fb.setupCFF("SARSymbol", {"FullName": "SAR Symbol"}, {".notdef": T2CharStringPen(500, None).getCharString(),
                "space": T2CharStringPen(250, None).getCharString(), "uni20C1": cs.getCharString()}, {})
    fb.setupHorizontalMetrics({".notdef": (500, 0), "space": (250, 0), "uni20C1": (adv, side)})
    fb.setupHorizontalHeader(ascent=900, descent=-250)
    fb.setupNameTable({"familyName": "SAR Symbol", "styleName": "Regular",
                       "copyright": "Glyph: Saudi Riyal symbol, official file of the Saudi Central Bank (SAMA)"})
    fb.setupOS2(sTypoAscender=900, sTypoDescender=-250, usWinAscent=900, usWinDescent=250, sxHeight=500, sCapHeight=round(target))
    fb.setupPost(); fb.save(a.out)
