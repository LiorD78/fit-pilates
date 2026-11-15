#!/usr/bin/env python3
"""Self-hosting písem (Cormorant Garamond + Inter) místo Google Fonts – 15. 11. 2026.

- stáhne CSS z Google Fonts (woff2), ponechá jen subsety latin a latin-ext (čeština),
- uloží woff2 do assets/fonts/ a @font-face vloží na začátek assets/css/site.css,
- ve všech HTML nahradí odkazy na Google Fonts (preconnect + preload/print/noscript)
  dvěma preloady klíčových písem,
- zvedne CSS ?v= na 15112026-fonts.
Spouštět z kořene repa: python3 scripts/selfhost-fonts-2026-11-15.py
"""
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_URL = (
    "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;"
    "0,600;0,700;1,300;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap"
)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
errors = []


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


css = get(FONT_URL).decode("utf-8")
blocks = re.findall(r"/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})", css, flags=re.S)
keep = [(subset, b) for subset, b in blocks if subset in ("latin", "latin-ext")]
if len(keep) < 20:
    errors.append(f"Google CSS: čekáno aspoň 20 bloků latin/latin-ext, nalezeno {len(keep)}")

fonts_dir = ROOT / "assets" / "fonts"
fonts_dir.mkdir(parents=True, exist_ok=True)
out_blocks = []
downloaded = {}
preload = {}
for subset, block in keep:
    family = re.search(r"font-family: '([^']+)'", block).group(1)
    style = re.search(r"font-style: (\w+)", block).group(1)
    weight = re.search(r"font-weight: (\d+)", block).group(1)
    m = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", block)
    if not m:
        errors.append(f"Blok bez woff2 URL: {family} {style} {weight} {subset}")
        continue
    src = m.group(1)
    slug = family.lower().replace(" ", "-")
    if src not in downloaded:
        # Obě písma jsou variabilní – jeden soubor na řez (normal/italic) a subset pro všechny tloušťky
        name = f"{slug}-{style}-var-{subset}.woff2"
        data = get(src)
        if len(data) < 5000:
            errors.append(f"{name}: podezřele malý soubor ({len(data)} B)")
        (fonts_dir / name).write_bytes(data)
        downloaded[src] = name
    name = downloaded[src]
    out_blocks.append(block.replace(src, f"/assets/fonts/{name}"))
    if subset == "latin" and ((slug == "inter" and weight == "400") or
                              (slug == "cormorant-garamond" and style == "normal" and weight == "700")):
        preload[slug] = name

if set(preload) != {"inter", "cormorant-garamond"}:
    errors.append(f"Preload písma nenalezena: {preload}")

font_css = "/* Self-hosted Google Fonts (latin, latin-ext) – 15. 11. 2026 */\n" + "\n".join(out_blocks) + "\n"

site_css = ROOT / "assets" / "css" / "site.css"
s = site_css.read_text(encoding="utf-8")
if "Self-hosted Google Fonts" in s:
    errors.append("site.css už @font-face obsahuje")
else:
    site_css.write_text(font_css + s, encoding="utf-8")

OLD_BLOCK = (
    '<link rel="preload" as="style" href="{u}">\n'
    '<link rel="stylesheet" href="{u}" media="print" onload="this.media=\'all\'">\n'
    '<noscript><link rel="stylesheet" href="{u}"></noscript>'
).format(u=FONT_URL)
NEW_BLOCK = (
    f'<link rel="preload" href="/assets/fonts/{preload.get("cormorant-garamond", "")}" as="font" type="font/woff2" crossorigin>\n'
    f'<link rel="preload" href="/assets/fonts/{preload.get("inter", "")}" as="font" type="font/woff2" crossorigin>'
)
PRECONNECTS = [
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n',
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n',
]

html_files = [p for p in ROOT.rglob("*.html") if "node_modules" not in p.parts and "_partials" not in p.parts]
block_count = 0
css_count = 0
for p in html_files:
    t = p.read_text(encoding="utf-8")
    orig = t
    if OLD_BLOCK in t:
        block_count += t.count(OLD_BLOCK)
        t = t.replace(OLD_BLOCK, NEW_BLOCK)
        for pc in PRECONNECTS:
            t = t.replace(pc, "")
            t = t.replace("  " + pc, "")
    if "site.css?v=15112026-perf" in t:
        css_count += t.count("site.css?v=15112026-perf")
        t = t.replace("site.css?v=15112026-perf", "site.css?v=15112026-fonts")
    if t != orig:
        p.write_text(t, encoding="utf-8")

if block_count != 24:
    errors.append(f"Blok Google Fonts: čekáno 24 výskytů, nalezeno {block_count}")
if css_count != 26:
    errors.append(f"CSS ?v=: čekáno 26 výskytů, nalezeno {css_count}")

headers = ROOT / "_headers"
h = headers.read_text(encoding="utf-8")
JS_RULE = "/assets/js/*\n  Cache-Control: public, max-age=31536000, immutable\n"
FONT_RULE = ("\n/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n"
             "  Access-Control-Allow-Origin: *\n")
if h.count(JS_RULE) != 1:
    errors.append("_headers: blok /assets/js/* nenalezen přesně jednou")
elif "/assets/fonts/*" not in h:
    headers.write_text(h.replace(JS_RULE, JS_RULE + FONT_RULE), encoding="utf-8")

leftover = [str(p.relative_to(ROOT)) for p in html_files if "fonts.googleapis.com" in p.read_text(encoding="utf-8")]

if errors:
    print("CHYBY – nic necommitovat:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print(f"OK – {len(downloaded)} woff2 souborů, {len(out_blocks)} @font-face, preload: {preload}")
if leftover:
    print("Info – Google Fonts zůstávají (mimo rozsah):", ", ".join(leftover))
