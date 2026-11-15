#!/usr/bin/env python3
"""Kontrast textu (WCAG AA) + WebP pro fotky v hero a CTA sekcích – 15. 11. 2026.

Kontrast:
- nová proměnná --gold-ink (#87671c) pro zlatý TEXT na světlém pozadí (5,3:1 na bílé, 4,9:1 na krémové),
- v tmavých sekcích (tmavé pozadí, hero s fotkou) se --gold-ink vrací na původní zlatou,
- bílý text na zlatém pozadí (tlačítka, štítky) -> tmavý text #1a1b1e (6,6:1),
- světle šedé drobné texty (--lgrey) na světlém pozadí -> --grey, v tmavé ceníkové kartě světlejší.
Barva pozadí tlačítek, rámečky a linky zůstávají ve značkové zlaté.

WebP:
- vytvoří .webp k hero/CTA fotkám, které ho ještě nemají (stejný snímek, stejný rozměr),
- v CSS za každé url(...jpg) přidá background-image:image-set(webp, jpg) – starší prohlížeče zůstanou na JPG,
- na homepage nahradí preload hero JPG třemi preloady WebP podle šířky okna (shodné s media queries v CSS).

Spouštět z kořene repa: python3 scripts/kontrast-webp-2026-11-15.py (vyžaduje Pillow s WebP).
"""
import pathlib
import re
import sys

from PIL import Image, features

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []
stats = {}


def bump(key, n=1):
    stats[key] = stats.get(key, 0) + n


GOLD_INK = "#87671c"
DARK_TEXT_CSS = "var(--black)"
DARK_TEXT_INLINE = "#1a1b1e"

# ---------- pomocné funkce pro barvy ----------
NAMED_DARK = {
    "var(--black)": 0.0, "var(--charcoal)": 0.0,
}


def luminance_of(value):
    """Vrátí relativní jas první barvy v hodnotě pozadí, nebo None, když barva není jasná."""
    v = value.strip().lower()
    for name in NAMED_DARK:
        if v.startswith(name):
            return 0.0
    m = re.match(r"#([0-9a-f]{6}|[0-9a-f]{3})\b", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
        alpha = 1.0
    else:
        m = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)", v)
        if not m:
            return None
        rgb = [int(m.group(i)) for i in (1, 2, 3)]
        alpha = float(m.group(4)) if m.group(4) else 1.0
        if alpha < 0.8:
            return None
    c = [x / 255 for x in rgb]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


BG_DECL = re.compile(r"(?<![-\w])background(?:-color)?\s*:\s*([^;{}]+)", re.I)
GOLD_BG = re.compile(r"(?<![-\w])background(?:-color)?\s*:\s*(?:var\(--gold(?:-l)?\)|#c49a3c|#d4af5a)", re.I)
WHITE_COLOR = re.compile(
    r"(?<![-\w])color(\s*):(\s*)(?:var\(--white\)|#fff(?:fff)?\b|white\b)(\s*!important)?", re.I)
GOLD_COLOR = re.compile(r"(?<![-\w])color(\s*):(\s*)(?:var\(--gold\)|#c49a3c)", re.I)


def has_dark_bg(body):
    for m in BG_DECL.finditer(body):
        val = m.group(1)
        if "gradient" in val or "url(" in val:
            continue
        lum = luminance_of(val)
        if lum is not None and lum < 0.06:
            return True
    return False


def fix_block(body, inline=False):
    """Upraví obsah jednoho CSS bloku nebo style="" atributu."""
    dark_text = DARK_TEXT_INLINE if inline else DARK_TEXT_CSS
    if GOLD_BG.search(body):
        body, n = WHITE_COLOR.subn(lambda m: f"color{m.group(1)}:{m.group(2)}{dark_text}{m.group(3) or ''}", body)
        bump("bily text na zlate -> tmavy", n)
    body, n = GOLD_COLOR.subn(lambda m: f"color{m.group(1)}:{m.group(2)}var(--gold-ink)", body)
    bump("zlaty text -> --gold-ink", n)
    if has_dark_bg(body) and "--gold-ink:var(--gold)" not in body:
        sep = "" if body.rstrip().endswith(";") or not body.strip() else ";"
        body = body.rstrip() + f"{sep}--gold-ink:var(--gold);"
        bump("tmave pozadi -> reset --gold-ink")
    return body


def fix_css(css, inline=False):
    # bloky bez vnořených závorek (pravidla uvnitř @media se zpracují také, @media samotné ne)
    return re.sub(r"\{([^{}]*)\}", lambda m: "{" + fix_block(m.group(1), inline) + "}", css)


# ---------- 1) WebP ----------
if not features.check("webp"):
    errors.append("Pillow bez podpory WebP")

site_css_path = ROOT / "assets" / "css" / "site.css"
css = site_css_path.read_text(encoding="utf-8")

jpgs = sorted(set(re.findall(r"url\('(/images/[^']+)\.jpg'\)", css)))
for base in jpgs:
    jpg = ROOT / (base.lstrip("/") + ".jpg")
    webp = ROOT / (base.lstrip("/") + ".webp")
    if not jpg.exists():
        errors.append(f"chybí {jpg}")
        continue
    if not webp.exists():
        im = Image.open(jpg).convert("RGB")
        im.save(webp, "WEBP", quality=80, method=6)
        bump("nove webp")
        if webp.stat().st_size >= jpg.stat().st_size:
            errors.append(f"{webp.name} není menší než JPG")


def add_image_set(m):
    decl = m.group(0)
    if "gradient" in decl or decl.count("url(") != 1:
        return decl
    base = m.group("base")
    bump("image-set")
    return (decl + f";background-image:image-set(url('{base}.webp') type('image/webp'),"
                   f"url('{base}.jpg') type('image/jpeg'))")


css = re.sub(r"(?<![-\w])background(?:-image)?\s*:[^;{}]*url\('(?P<base>/images/[^']+)\.jpg'\)[^;{}]*",
             add_image_set, css)

# ---------- 2) Kontrast v site.css ----------
if "--gold-ink" in css:
    errors.append("site.css už --gold-ink obsahuje")
css = css.replace("--gold-l:#d4af5a;", f"--gold-l:#d4af5a;--gold-ink:{GOLD_INK};", 1)
if f"--gold-ink:{GOLD_INK}" not in css:
    errors.append(":root – nepodařilo se vložit --gold-ink")

css = fix_css(css)

# šedé drobné texty v ceníku a recenzích
for old, new in [
    (".p-name{font-size:10px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--lgrey)",
     ".p-name{font-size:10px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--grey)"),
    (".p-per{font-size:12px;color:var(--lgrey)", ".p-per{font-size:12px;color:var(--grey)"),
    (".test-role{font-size:11px;color:var(--lgrey)", ".test-role{font-size:11px;color:var(--grey)"),
    (".p-card.feat .p-name{color:rgba(196,154,60,.7)}", ".p-card.feat .p-name{color:var(--gold-ink)}"),
    (".p-card.feat .p-per{color:rgba(255,255,255,.35)}", ".p-card.feat .p-per{color:rgba(255,255,255,.7)}"),
]:
    if css.count(old) != 1:
        errors.append(f"site.css: nenalezeno přesně jednou: {old[:50]}")
    css = css.replace(old, new)

# sekce s fotkou a tmavým překryvem (pozadí obrázkem, proto je automatika nepozná)
css += ("\n/* Kontrast 15. 11. 2026: v tmavých sekcích s fotkou zůstává zlatý text v původní zlaté */\n"
        ".hero,.page-hero,.cb,.fw,.vl-hero,nav:not(.s),.site-nav:not(.is-scrolled),.site-nav__overlay,"
        "#nav-overlay{--gold-ink:var(--gold)}\n")
site_css_path.write_text(css, encoding="utf-8")

# ---------- 3) Kontrast + preload v HTML ----------
html_files = [p for p in ROOT.rglob("*.html") if "node_modules" not in p.parts and ".git" not in p.parts]
css_v = 0
for p in html_files:
    t = p.read_text(encoding="utf-8")
    orig = t
    t = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + fix_css(m.group(2), True) + m.group(3),
               t, flags=re.S)
    t = re.sub(r'style="([^"]*)"', lambda m: 'style="' + fix_block(m.group(1), inline=True) + '"', t)
    # světle šedý text na světlém pozadí -> --grey (kromě míst na tmavém pozadí)
    def lgrey_block(m):
        sel, body = m.group(1), m.group(2)
        if "essay-breadcrumb" in sel:
            return m.group(0)
        return sel + "{" + re.sub(r"(color\s*:\s*)var\(--lgrey\)", r"\1var(--grey)", body) + "}"
    t = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)",
               lambda m: m.group(1) + re.sub(r"([^{}]*)\{([^{}]*)\}", lgrey_block, m.group(2)) + m.group(3),
               t, flags=re.S)
    t = re.sub(r"<[^<>]*style=\"[^\"]*var\(--lgrey\)[^\"]*\"[^<>]*>",
               lambda m: m.group(0) if "hero" in m.group(0) else
               re.sub(r"(color\s*:\s*)var\(--lgrey\)", r"\1var(--grey)", m.group(0)), t)
    # drobné popisky na tmavém pozadí: průhlednost bílé .4 -> .65
    if p.name == "index.html" and p.parent.name in ("rezervace", "pribeh-libor"):
        for sel in (".res-access-label", ".essay-cta-price"):
            t = re.sub(r"(" + re.escape(sel) + r"\s*\{[^{}]*?color:\s*)rgba\(255,\s*255,\s*255,\s*\.4\)",
                       r"\1rgba(255,255,255,.65)", t)
    n = t.count("site.css?v=15112026-fonts")
    css_v += n
    t = t.replace("site.css?v=15112026-fonts", "site.css?v=15112026-kontrast")
    if t != orig:
        p.write_text(t, encoding="utf-8")

index = ROOT / "index.html"
t = index.read_text(encoding="utf-8")
OLD_PRELOAD = re.search(r'<link rel="preload" as="image" href="images/hero-w800\.jpg"[^>]*>', t)
if not OLD_PRELOAD:
    errors.append("index.html: preload hero JPG nenalezen")
else:
    NEW_PRELOAD = (
        '<link rel="preload" as="image" href="/images/hero-w800.webp" type="image/webp" media="(max-width: 800px)" fetchpriority="high">\n'
        '<link rel="preload" as="image" href="/images/hero-w1200.webp" type="image/webp" media="(min-width: 801px) and (max-width: 1200px)" fetchpriority="high">\n'
        '<link rel="preload" as="image" href="/images/hero.webp" type="image/webp" media="(min-width: 1201px)" fetchpriority="high">'
    )
    t = t.replace(OLD_PRELOAD.group(0), NEW_PRELOAD)
    index.write_text(t, encoding="utf-8")

if css_v != 26:
    errors.append(f"CSS ?v=: čekáno 26 výskytů, nalezeno {css_v}")

# ---------- kontroly ----------
final_css = site_css_path.read_text(encoding="utf-8")
if final_css.count("{") != final_css.count("}"):
    errors.append("site.css: nesouhlasí počet závorek")
leftover = []
for p in html_files + [site_css_path]:
    s = p.read_text(encoding="utf-8")
    if re.search(r"(?<![-\w])color\s*:\s*(?:var\(--gold\)|#c49a3c)", s):
        leftover.append(str(p.relative_to(ROOT)))
if leftover:
    errors.append("zůstal zlatý text bez --gold-ink: " + ", ".join(leftover))

if errors:
    print("CHYBY – nic necommitovat:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK –", ", ".join(f"{k}: {v}" for k, v in stats.items()))
