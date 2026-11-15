#!/usr/bin/env python3
"""Rychlejší první zobrazení (LCP) – 15. 11. 2026.

1) Microsoft Clarity a Google Analytics (gtag.js) se na všech stránkách načítají až po načtení
   stránky (requestIdleCallback po události load) nebo při první interakci uživatele. Consent Mode
   default i konfigurace GA4 zůstávají v hlavičce, události z dataLayer se odešlou po načtení gtag.js.
2) Homepage: 6 dlaždic „Pro koho jsme“ (fw-back-*.jpg) načítá fotku až při přiblížení k výřezu
   (IntersectionObserver), ve WebP s JPG zálohou. Fotky samotné se nemění.
Spouštět z kořene repa: python3 scripts/perf-lcp-2026-11-15.py (vyžaduje Pillow s WebP).
"""
import pathlib
import re
import sys

from PIL import Image, features

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []

CLARITY = ('<script type="text/javascript">(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};'
           't=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];'
           'y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","x2d94kqdkf");</script>')
GTAG = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-NSHB184V2T"></script>'
LOADER = (
    "<!-- Clarity + GA4 se načítají až po načtení stránky nebo při první interakci (rychlejší LCP) -->\n"
    "<script>(function(w,d){w.clarity=w.clarity||function(){(w.clarity.q=w.clarity.q||[]).push(arguments)};"
    "var done=0;function go(){if(done)return;done=1;"
    "var c=d.createElement('script');c.async=1;c.src='https://www.clarity.ms/tag/x2d94kqdkf';d.head.appendChild(c);"
    "var g=d.createElement('script');g.async=1;g.src='https://www.googletagmanager.com/gtag/js?id=G-NSHB184V2T';d.head.appendChild(g);}"
    "function later(){if('requestIdleCallback' in w){w.requestIdleCallback(go,{timeout:3000})}else{setTimeout(go,1500)}}"
    "if(d.readyState==='complete'){later()}else{w.addEventListener('load',later)}"
    "['pointerdown','keydown','touchstart','scroll'].forEach(function(e){w.addEventListener(e,go,{once:true,passive:true})});"
    "})(window,document);</script>"
)

html_files = [p for p in ROOT.rglob("*.html") if "node_modules" not in p.parts and ".git" not in p.parts]
changed = 0
for p in html_files:
    t = p.read_text(encoding="utf-8")
    has_c, has_g = CLARITY in t, GTAG in t
    if not (has_c or has_g):
        continue
    if not (has_c and has_g):
        errors.append(f"{p.relative_to(ROOT)}: jen jeden z Clarity/gtag – přeskočeno")
        continue
    if t.index(CLARITY) > t.index(GTAG):
        errors.append(f"{p.relative_to(ROOT)}: neočekávané pořadí skriptů")
        continue
    t = t.replace("<!-- Microsoft Clarity -->\n" + CLARITY + "\n", "")
    t = t.replace(CLARITY + "\n", "").replace(CLARITY, "")
    t = t.replace(GTAG, LOADER)
    if "clarity.ms/tag" in t.replace(LOADER, "") or t.count(LOADER) != 1:
        errors.append(f"{p.relative_to(ROOT)}: náhrada se nepovedla")
        continue
    p.write_text(t, encoding="utf-8")
    changed += 1
if changed != 26:
    errors.append(f"analytika: čekáno 26 stránek, upraveno {changed}")

# ---------- přednačtení písem latin-ext (čeština: ě, š, č, ř, ž, ů …) ----------
INTER_LATIN = '<link rel="preload" href="/assets/fonts/inter-normal-var-latin.woff2" as="font" type="font/woff2" crossorigin>'
EXT = ('\n<link rel="preload" href="/assets/fonts/inter-normal-var-latin-ext.woff2" as="font" type="font/woff2" crossorigin>'
       '\n<link rel="preload" href="/assets/fonts/cormorant-garamond-normal-var-latin-ext.woff2" as="font" type="font/woff2" crossorigin>')
ext_pages = 0
for p in html_files:
    t = p.read_text(encoding="utf-8")
    if INTER_LATIN in t and "inter-normal-var-latin-ext.woff2\" as=\"font\"" not in t:
        p.write_text(t.replace(INTER_LATIN, INTER_LATIN + EXT, 1), encoding="utf-8")
        ext_pages += 1
if ext_pages != 24:
    errors.append(f"preload latin-ext: čekáno 24 stránek, upraveno {ext_pages}")

# ---------- dlaždice „Pro koho jsme“ na homepage ----------
if not features.check("webp"):
    errors.append("Pillow bez podpory WebP")
for i in range(1, 7):
    jpg = ROOT / "images" / f"fw-back-{i}.jpg"
    webp = jpg.with_suffix(".webp")
    if not webp.exists():
        Image.open(jpg).convert("RGB").save(webp, "WEBP", quality=80, method=6)
    if webp.stat().st_size >= jpg.stat().st_size:
        errors.append(f"{webp.name} není menší než JPG")

index = ROOT / "index.html"
t = index.read_text(encoding="utf-8")
t, n = re.subn(r"""style="background-image:url\('images/(fw-back-\d)\.jpg\?v=2'\);?([^"]*)\"""",
               lambda m: f'data-bg="/images/{m.group(1)}"' + (f' style="{m.group(2)}"' if m.group(2) else ""), t)
if n != 6:
    errors.append(f"index.html: čekáno 6 dlaždic fw, nalezeno {n}")
LAZY = (
    "<script>(function(){var els=document.querySelectorAll('.fw[data-bg]');"
    "function show(el){var b=el.getAttribute('data-bg');el.removeAttribute('data-bg');"
    "el.style.backgroundImage=\"url('\"+b+\".jpg?v=2')\";"
    "el.style.backgroundImage=\"image-set(url('\"+b+\".webp?v=2') type('image/webp'),url('\"+b+\".jpg?v=2') type('image/jpeg'))\";}"
    "if(!('IntersectionObserver' in window)){els.forEach(show);return;}"
    "var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);show(e.target);}});},{rootMargin:'600px 0px'});"
    "els.forEach(function(el){io.observe(el);});})();</script>\n"
)
anchor = '<div class="fw rv d2" data-bg="/images/fw-back-6"'
pos = t.find(anchor)
end = t.find("</div>\n</div>", pos) if pos >= 0 else -1
if end < 0:
    errors.append("index.html: konec mřížky fw nenalezen")
else:
    cut = end + len("</div>\n</div>\n")
    t = t[:cut] + LAZY + t[cut:]
# ---------- dlaždice programů: WebP + přesnější sizes (na mobilu stačí 600w) ----------
for base in ("fitness-w600", "fitness-w900"):
    jpg = ROOT / "images" / f"{base}.jpg"
    webp = jpg.with_suffix(".webp")
    if not webp.exists():
        Image.open(jpg).convert("RGB").save(webp, "WEBP", quality=80, method=6)
    if webp.stat().st_size >= jpg.stat().st_size:
        errors.append(f"{webp.name} není menší než JPG")

PROG_SIZES = "(max-width:900px) calc(100vw - 120px), 360px"


def prog_picture(m):
    img = m.group(0)
    srcset = re.search(r'srcset="([^"]+)"', img).group(1)
    webp_srcset = re.sub(r"\.jpg(\s)", r".webp\1", srcset)
    for part in webp_srcset.split(","):
        f = ROOT / part.strip().split()[0]
        if not f.exists():
            errors.append(f"chybí {f.relative_to(ROOT)}")
    img = img.replace('sizes="(max-width:768px) 100vw, 33vw"', f'sizes="{PROG_SIZES}"')
    return (f'<picture style="display:block"><source type="image/webp" srcset="{webp_srcset}" sizes="{PROG_SIZES}">'
            f"{img}</picture>")


t, n = re.subn(r'<img src="images/(?:pilates|fitness|boxing-studio)-w600\.jpg"[^>]*class="prog-img"[^>]*>', prog_picture, t)
if n != 3:
    errors.append(f"index.html: čekány 3 obrázky programů, nalezeno {n}")
index.write_text(t, encoding="utf-8")

if errors:
    print("CHYBY – nic necommitovat:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"OK – latin-ext preload {ext_pages} stránek, analytika odložena na {changed} stránkách, 6 dlaždic fw líně (WebP)")
