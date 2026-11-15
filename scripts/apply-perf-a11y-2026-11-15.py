#!/usr/bin/env python3
"""Jednorázové úpravy 15. 11. 2026: neblokující Google Fonts, kontrast šedých textů,
popisky selectů, CSS cache-busting a nové titulky/popisy dvou článků.
Spouštět z kořene repa: python3 scripts/apply-perf-a11y-2026-11-15.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []
changed = set()


def replace(path, old, new, expected=None):
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    n = text.count(old)
    if expected is not None and n != expected:
        errors.append(f"{path}: čekáno {expected}× '{old[:60]}', nalezeno {n}×")
        return
    if n == 0:
        return
    p.write_text(text.replace(old, new), encoding="utf-8")
    changed.add(path)


html_files = sorted(
    str(p.relative_to(ROOT))
    for p in ROOT.rglob("*.html")
    if "node_modules" not in p.parts and "_partials" not in p.parts
)

# 1) Google Fonts – neblokující načtení (preload + media=print/onload + noscript)
FONT_URL = (
    "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;"
    "0,600;0,700;1,300;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap"
)
OLD_FONT = f'<link href="{FONT_URL}" rel="stylesheet">'
NEW_FONT = (
    f'<link rel="preload" as="style" href="{FONT_URL}">\n'
    f'<link rel="stylesheet" href="{FONT_URL}" media="print" onload="this.media=\'all\'">\n'
    f'<noscript><link rel="stylesheet" href="{FONT_URL}"></noscript>'
)
font_count = 0
for f in html_files:
    t = (ROOT / f).read_text(encoding="utf-8")
    if OLD_FONT in t:
        font_count += t.count(OLD_FONT)
        replace(f, OLD_FONT, NEW_FONT)
if font_count != 24:
    errors.append(f"Google Fonts: čekáno 24 výskytů, nalezeno {font_count}")

# 2) Kontrast – šedé texty (bez změny značkové zlaté)
replace(
    "assets/css/site.css",
    ".rev-meta{font-size:12px;color:var(--lgrey);",
    ".rev-meta{font-size:12px;color:var(--grey);",
    expected=1,
)
replace(
    "assets/css/site.css",
    "background:var(--warm);color:var(--grey);border:1px solid var(--border)}",
    "background:var(--warm);color:#565c68;border:1px solid var(--border)}",
    expected=1,
)

# 3) Popisek pro select „zájem“ ve formulářích
for f in [
    "index.html",
    "pilates-praha-10/index.html",
    "bolest-zad-praha/index.html",
    "osobni-trener-praha-10/index.html",
    "restart-po-40/index.html",
]:
    replace(f, '<select name="zajem">', '<select name="zajem" aria-label="Zájem o program">', expected=1)

# 4) CSS cache-busting
css_count = 0
for f in html_files:
    t = (ROOT / f).read_text(encoding="utf-8")
    c = t.count("site.css?v=20102026-podminky")
    if c:
        css_count += c
        replace(f, "site.css?v=20102026-podminky", "site.css?v=15112026-perf")
if css_count != 26:
    errors.append(f"CSS ?v=: čekáno 26 výskytů, nalezeno {css_count}")

# 5) Titulky a popisy – vyšší CTR (texty prošly crew GPT + Gemini)
A = "blog/co-je-reformer-pilates/index.html"
A_T_OLD = "Pilates reformer: co to je, jak funguje a pro koho se hodí"
A_T_NEW = "Pilates reformer: jak funguje, přínosy a první lekce"
A_D_OLD = ("Jak funguje pilates reformer, čím se liší od cvičení na podložce a co čekat od první lekce. "
           "Zkuste ho ve Strašnicích: max. 3 lidé, vstupní lekce 590 Kč.")
A_D_NEW = ("Co je pilates reformer a jak funguje? Přínosy, rozdíl oproti podložce i průběh první lekce – "
           "průvodce od lektora s 24 lety praxe ze studia v Praze 10.")
replace(A, f"<title>{A_T_OLD}</title>", f"<title>{A_T_NEW}</title>", expected=1)
replace(A, f'<meta name="description" content="{A_D_OLD}">', f'<meta name="description" content="{A_D_NEW}">', expected=1)
replace(A, f'<meta property="og:title" content="{A_T_OLD}">', f'<meta property="og:title" content="{A_T_NEW}">', expected=1)
replace(A, f'<meta name="twitter:title" content="{A_T_OLD}">', f'<meta name="twitter:title" content="{A_T_NEW}">', expected=1)

B = "blog/reformer-pilates-praha/index.html"
B_T_OLD = "Reformer pilates Praha: ceny a jak vybrat studio"
B_T_NEW = "Reformer pilates Praha: přehled cen a jak vybrat studio"
B_D_OLD = ("Kolik stojí reformer pilates v Praze a jak poznat dobré studio: velikost skupiny, stroje, "
           "zkušenost lektora. Přehled cen od 300 do 1 500 Kč za lekci.")
B_D_NEW = ("Kolik stojí reformer pilates v Praze (300–1 500 Kč) a čím se liší velká studia od komorních? "
           "Proč rozhoduje velikost skupiny, stroje a zkušenost lektora.")
replace(B, f"<title>{B_T_OLD}</title>", f"<title>{B_T_NEW}</title>", expected=1)
replace(B, f'<meta name="description" content="{B_D_OLD}">', f'<meta name="description" content="{B_D_NEW}">', expected=1)
replace(B, f'<meta property="og:title" content="{B_T_OLD}">', f'<meta property="og:title" content="{B_T_NEW}">', expected=1)
replace(B, f'<meta name="twitter:title" content="{B_T_OLD}">', f'<meta name="twitter:title" content="{B_T_NEW}">', expected=1)

if errors:
    print("CHYBY – nic necommitovat:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print(f"OK – upraveno {len(changed)} souborů")
for c in sorted(changed):
    print(" ", c)
