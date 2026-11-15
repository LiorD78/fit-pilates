#!/usr/bin/env python3
"""Odstranění kanibalizace reformer / Praha 10 (16. 11. 2026).

Cílení po úpravě:
  /                              reformer pilates Praha (10), pilates Praha 10 – hlavní komerční stránka
  /reformer-pilates-praha-10/    skupinové lekce na reformeru (max. 3 osoby)
  /individualni-reformer-pilates-praha/  soukromé lekce 1:1
  /pilates-allegro/              stroj Allegro reformer (Balanced Body)
  /blog/reformer-pilates-praha/  ceny a výběr studia (informační)
  /blog/co-je-reformer-pilates/  co je reformer pilates (informační)
  /pilates-praha-10/             zrušeno, 301 na /

Spouštět z kořene repozitáře: python3 scripts/kanibalizace-2026-11.py
Skript kontroluje, že každá náhrada proběhla; když něco nesedí, skončí chybou a nic nezapíše.
"""
import glob
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

files = {}


def load(path):
    if path not in files:
        with open(path, encoding="utf-8") as fh:
            files[path] = fh.read()
    return files[path]


def rep(path, old, new, count=1):
    s = load(path)
    n = s.count(old)
    if n != count:
        sys.exit(f"CHYBA {path}: čekal jsem {count}× „{old[:80]}“, nalezeno {n}×")
    files[path] = s.replace(old, new)


def rep_re(path, pattern, new, count=1, flags=re.S):
    s = load(path)
    out, n = re.subn(pattern, new, s, flags=flags)
    if n != count:
        sys.exit(f"CHYBA {path}: regex {pattern[:80]} nahradil {n}×, čekal jsem {count}×")
    files[path] = out


html_files = sorted(p for p in glob.glob("**/*.html", recursive=True)
                    if not p.startswith("pilates-praha-10/") and not p.startswith("node_modules/"))

# ---------------------------------------------------------------- 1. Homepage
H = "index.html"
OLD_T = "Pilates Praha 10 – privátní studio ve Strašnicích"
NEW_T = "Reformer pilates Praha 10 – privátní studio ve Strašnicích"
rep(H, f"<title>{OLD_T}</title>", f"<title>{NEW_T}</title>")
rep(H, f'<meta property="og:title" content="{OLD_T}">', f'<meta property="og:title" content="{NEW_T}">')
rep(H, f'<meta name="twitter:title" content="{OLD_T}">', f'<meta name="twitter:title" content="{NEW_T}">')
rep(H, "<h1>Privátní pilates<br>Praha 10<br>lekce <em>1:1</em> se Štefanem</h1>",
       "<h1>Privátní reformer pilates<br>Praha 10<br>se <em>Štefanem</em></h1>")
rep(H, 'Pilates studio v srdci<br><em>Prahy 10</em></h2>',
       'Reformer pilates studio v srdci<br><em>Prahy 10</em></h2>')
rep(H, '"description": "Pilates studio v Praze 10 – Strašnice. Reformer pilates, silový a funkční trénink, kondiční box pod jednou střechou.',
       '"description": "Reformer pilates studio v Praze 10 – Strašnice. Pilates na strojích Balanced Body, silový a funkční trénink a kondiční box pod jednou střechou.')
# odkazy na zrušenou /pilates-praha-10/ z homepage
rep(H, '<a href="/pilates-praha-10/" class="pill" style="text-decoration:none;">✦ Studio Praha 10</a>',
       '<a href="#kde-jsme" class="pill" style="text-decoration:none;">✦ Studio Praha 10</a>')
rep(H, 'celá <a href="/pilates-praha-10/" style="color: var(--gold-ink);">Praha 10</a>', 'celá Praha 10')
rep(H, ' Více podrobností o lokalitě najdete na stránce <a href="/pilates-praha-10/">pilates Praha 10</a>.', '')
rep(H, 'ať už jde o malou skupinu nebo <a href="/individualni-reformer-pilates-praha/">individuální reformer pilates</a> – zbytek je na vás. Stejné ceny platí pro <a href="/reformer-pilates-praha-10/">reformer pilates v Praze 10</a>, silový trénink i kondiční box.',
       'ať už jde o <a href="/reformer-pilates-praha-10/">skupinové lekce na reformeru</a> nebo <a href="/individualni-reformer-pilates-praha/">individuální reformer pilates</a> – zbytek je na vás. Stejné ceny platí pro reformer pilates, silový trénink i kondiční box.')

# ---------------------------------------------------------------- 2. Skupinové lekce (/reformer-pilates-praha-10/)
G = "reformer-pilates-praha-10/index.html"
rep(G, "<title>Reformer Pilates Praha | Privátní studio Praha 10</title>",
       "<title>Skupinové lekce na reformeru Praha 10 – max. 3 osoby | Fit Pilates</title>")
rep(G, '<meta name="description" content="Reformer pilates ve Strašnicích, Praha 10. Lekce 1:1 nebo skupina max. 3 osob na strojích Balanced Body, vede Štefan Bitto, 24+ let praxe. Vstupní lekce 590 Kč.">',
       '<meta name="description" content="Skupinové lekce na reformeru ve Strašnicích, Praha 10: nejvýš 3 lidé, stroje Balanced Body, vede Štefan Bitto (24+ let praxe). 790 Kč, vstupní lekce 590 Kč.">')
rep(G, '<meta property="og:title" content="Reformer pilates Praha — privátní studio v Praze 10">',
       '<meta property="og:title" content="Skupinové lekce na reformeru Praha 10 – max. 3 osoby">')
rep(G, '<meta property="og:description" content="Reformer pilates ve Strašnicích: individuální lekce 1:1 za 1 290 Kč nebo skupina maximálně tří osob za 790 Kč. Kompletní stroje Balanced Body, vede Štefan Bitto.">',
       '<meta property="og:description" content="Skupinové lekce na reformeru ve Strašnicích: nejvýš tři lidé, 790 Kč za lekci. Kompletní stroje Balanced Body, vede Štefan Bitto.">')
rep(G, '<meta name="twitter:title" content="Reformer pilates Praha — Fit Pilates Strašnice">',
       '<meta name="twitter:title" content="Skupinové lekce na reformeru Praha 10 – Fit Pilates">')
rep(G, '<meta name="twitter:description" content="Individuální lekce 1:1 nebo skupina max 3 osoby. Kompletní stroje Balanced Body.">',
       '<meta name="twitter:description" content="Skupina nejvýš 3 lidí, 790 Kč. Kompletní stroje Balanced Body ve Strašnicích.">')
rep(G, '"name": "Reformer pilates Praha 10", "item": "https://fitpilates.cz/reformer-pilates-praha-10/"',
       '"name": "Skupinové lekce na reformeru", "item": "https://fitpilates.cz/reformer-pilates-praha-10/"')
rep(G, '"name": "Reformer pilates Praha 10 — individuální lekce a malá skupina",',
       '"name": "Skupinové lekce na reformeru Praha 10 (max. 3 osoby)",')
rep(G, "<h1>Reformer pilates<br>ve <em>Strašnicích</em><br>Praha 10</h1>",
       "<h1>Skupinové lekce<br>na <em>reformeru</em><br>Praha 10</h1>")

# ---------------------------------------------------------------- 3. Blog průvodce cenami
B = "blog/reformer-pilates-praha/index.html"
OLD_BT = "Reformer pilates Praha: přehled cen a jak vybrat studio"
NEW_BT = "Reformer pilates Praha: ceny lekcí a jak vybrat studio"
rep(B, f"<title>{OLD_BT}</title>", f"<title>{NEW_BT}</title>")
rep(B, f'<meta property="og:title" content="{OLD_BT}">', f'<meta property="og:title" content="{NEW_BT}">')
rep(B, f'<meta name="twitter:title" content="{OLD_BT}">', f'<meta name="twitter:title" content="{NEW_BT}">')
rep(B, "Praktický průvodce od lektora s 24 lety praxe.</p>",
       'Praktický průvodce od lektora s 24 lety praxe, který vede <a href="/">reformer pilates v Praze 10 – Strašnicích</a>.</p>')
rep_re(B, r'Konkrétní nabídku lekcí najdete na stránce <a href="/reformer-pilates-praha-10/"([^>]*)>reformer pilates Praha</a>',
          r'Konkrétní nabídku lekcí najdete na stránce <a href="/"\1>reformer pilates Praha 10</a>')
rep_re(B, r'(termíny skupinových lekcí ve Strašnicích, najdete je na stránce )<a href="/reformer-pilates-praha-10/"([^>]*)>reformer pilates Praha 10</a>',
          r'\1<a href="/reformer-pilates-praha-10/"\2>skupinové lekce na reformeru</a>')
rep_re(B, r'(Přehled lekcí a cen: )<a href="/reformer-pilates-praha-10/"([^>]*)>reformer pilates Praha 10</a>',
          r'\1<a href="/"\2>reformer pilates Praha 10</a>')
rep_re(B, r'(formátů lekcí je na stránce )<a href="/reformer-pilates-praha-10/"([^>]*)>reformer pilates v Praze 10</a>',
          r'\1<a href="/"\2>reformer pilates v Praze 10</a>')
rep_re(B, r'<a href="/reformer-pilates-praha-10/"([^>]*)>reformer pilates ve Strašnicích</a>',
          r'<a href="/"\1>reformer pilates ve Strašnicích</a>')
rep_re(B, r'Více v sekci <a href="/pilates-praha-10/"[^>]*>Pilates Praha 10</a>\. ', '')
# vstupní lekce je od listopadu 2026 jen pro jednoho
rep(B, "je vždy individuální nebo v páru", "je vždy individuální", count=2)

# ---------------------------------------------------------------- 4. Ostatní kontextové odkazy na skupinovou stránku
C = "blog/co-je-reformer-pilates/index.html"
rep_re(C, r'<a href="/reformer-pilates-praha-10/"([^>]*)>reformer pilates v Praze 10</a>', r'<a href="/"\1>reformer pilates v Praze 10</a>')
rep_re(C, r'<a href="/reformer-pilates-praha-10/"([^>]*)>reformer pilates Praha 10</a>', r'<a href="/"\1>reformer pilates Praha 10</a>')
I = "individualni-reformer-pilates-praha/index.html"
rep_re(I, r'(podrobnosti najdete na stránce )<a href="/reformer-pilates-praha-10/"([^>]*)>reformer pilates Praha 10</a>',
          r'\1<a href="/reformer-pilates-praha-10/"\2>skupinové lekce na reformeru</a>')
rep(I, '<a href="/reformer-pilates-praha-10/" class="card card--cream related-card">\n    <h3>Reformer pilates Praha 10</h3>',
       '<a href="/reformer-pilates-praha-10/" class="card card--cream related-card">\n    <h3>Skupinové lekce na reformeru</h3>')
rep("pilates-na-strojich/index.html", '<a href="/reformer-pilates-praha-10/"><strong>reformer v Praze 10</strong></a>',
    '<a href="/"><strong>reformer v Praze 10</strong></a>')
rep("podminky/index.html", 'Stejné ceny platí pro <a href="/reformer-pilates-praha-10/">reformer pilates</a>,',
    'Stejné ceny platí pro <a href="/">reformer pilates</a>,')

# ---------------------------------------------------------------- 5. Patička na všech stránkách
FOOT = [
    ('<li><a href="/pilates-allegro/">Reformer Pilates</a></li>', '<li><a href="/pilates-allegro/">Allegro reformer</a></li>'),
    ('<li><a href="/pilates-praha-10/">Pilates Praha 10</a></li>', '<li><a href="/">Reformer pilates Praha 10</a></li>'),
    ('<li><a href="/reformer-pilates-praha-10/">Reformer pilates Praha</a></li>', '<li><a href="/reformer-pilates-praha-10/">Skupinové lekce na reformeru</a></li>'),
]
for path in html_files + ["_partials/footer.html"]:
    s = load(path)
    for old, new in FOOT:
        s = s.replace(old, new)
    # duplicitní odkaz na Allegro ve druhém sloupci patičky
    s = re.sub(r'\n[ \t]*<li><a href="/pilates-allegro/">Pilates Allegro</a></li>', '', s)
    files[path] = s

# ---------------------------------------------------------------- 6. Všechny zbylé odkazy na /pilates-praha-10/ → /
for path in html_files:
    s = load(path)
    s = s.replace('href="/pilates-praha-10/"', 'href="/"').replace('href="https://fitpilates.cz/pilates-praha-10/"', 'href="https://fitpilates.cz/"')
    files[path] = s

# ---------------------------------------------------------------- 7. Přesměrování, sitemap, llms.txt
rep("_redirects", "# Záloha pro případ výpadku edge funkce fp-go",
    "# Zrušená stránka – sloučeno s homepage (16. 11. 2026)\n/pilates-praha-10/  /  301!\n/pilates-praha-10   /  301!\n\n# Záloha pro případ výpadku edge funkce fp-go")
rep_re("sitemap.xml", r'\n  <url>\n    <loc>https://fitpilates.cz/pilates-praha-10/</loc>.*?</url>', "")
for loc in ["https://fitpilates.cz/", "https://fitpilates.cz/reformer-pilates-praha-10/", "https://fitpilates.cz/blog/reformer-pilates-praha/"]:
    rep_re("sitemap.xml", r'(<loc>' + re.escape(loc) + r'</loc>\n    <lastmod>)[0-9-]+(</lastmod>)', r'\g<1>2026-11-16\2')
rep("llms.txt", "- [Hlavní stránka](https://fitpilates.cz/): Přehled studia, programů a ceník",
    "- [Reformer pilates Praha 10 – hlavní stránka](https://fitpilates.cz/): Privátní studio ve Strašnicích, programy, ceník, doprava a parkování")
rep("llms.txt", "- [Reformer pilates Praha 10](https://fitpilates.cz/reformer-pilates-praha-10/): Individuální lekce 1:1 i skupinové lekce na reformeru (max. 3 osoby) ve Strašnicích",
    "- [Skupinové lekce na reformeru](https://fitpilates.cz/reformer-pilates-praha-10/): Skupina nejvýš 3 lidí na reformerech Balanced Body ve Strašnicích, 790 Kč")
rep_re("llms.txt", r'\n- \[Pilates Praha 10\]\(https://fitpilates\.cz/pilates-praha-10/\)[^\n]*', "")
s = load("_headers")
files["_headers"] = re.sub(r'\n/pilates-praha-10/\*\n(?:[ \t]+[^\n]*\n)*', "\n", s)

# ---------------------------------------------------------------- kontrola a zápis
for path, s in files.items():
    if path.endswith(".html") and ("/pilates-praha-10/" in s):
        sys.exit(f"CHYBA {path}: zůstal odkaz na /pilates-praha-10/")
for path, s in files.items():
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(s)
if os.path.isdir("pilates-praha-10"):
    shutil.rmtree("pilates-praha-10")
print(f"Hotovo, upraveno {len(files)} souborů, /pilates-praha-10/ smazána.")
