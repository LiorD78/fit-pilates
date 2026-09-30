#!/usr/bin/env python3
"""Jednorázové nasazení propojení s CLEANEE FITNESS CARE (30. 9. 2026).
Upraví /studio/, /blog/co-je-reformer-pilates/, /blog/, sitemap.xml, llms.txt
a stáhne 2 obrázky z cdn.cleanee.cz do images/blog/cisteni/. Po spuštění smazat."""
import os, sys, urllib.request
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(R, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(R, p), 'w', encoding='utf-8').write(s)
def once(s, old, new, label):
    n = s.count(old)
    if n != 1: sys.exit(f'CHYBA {label}: kotva nalezena {n}x (čekáno 1)')
    return s.replace(old, new)

# 1) obrázky
os.makedirs(os.path.join(R, 'images/blog/cisteni'), exist_ok=True)
for src, dst in [('cleanee-yoga-mat-cleaner-hero-v4.webp', 'cleanee-yoga-mat-cleaner.webp'),
                 ('cleanee-gym-cleaner-hero-v2.webp', 'cleanee-gym-cleaner.webp')]:
    req = urllib.request.Request('https://cdn.cleanee.cz/data/user-content/' + src, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=60).read()
    if len(data) < 50000: sys.exit('CHYBA: obrázek ' + src + ' je podezřele malý')
    open(os.path.join(R, 'images/blog/cisteni', dst), 'wb').write(data)

# 2) /studio/ – blok Čistota ve studiu před „Štefan v akci“
p = 'studio/index.html'; s = rd(p)
block = '''  <h2>Čistota <em>ve studiu</em></h2>
  <p class="lead">Studio je privátní a mezi klienty mám vyhrazený čas na přípravu. Stroje, podložky a madla se čistí po každém klientovi, takže každý přichází k utřenému reformeru a čisté podložce.</p>
  <blockquote style="font-family: 'Cormorant Garamond', serif; font-size: 1.35rem; font-style: italic; color: var(--charcoal); border-left: 3px solid var(--gold); padding: 12px 0 12px 22px; margin: 0 0 20px; max-width: 820px; line-height: 1.5;">„Na prostředí, ve kterém se cvičí, záleží. Čistá podložka a utřené stroje jsou první věc, které si klient všimne.“<cite style="display: block; font-size: .9rem; font-style: normal; color: var(--grey); margin-top: 8px; font-family: 'Inter', sans-serif;">— Štefan Bitto</cite></blockquote>
  <p class="lead">Ve studiu uklízíme s řadou <a href="https://www.cleanee.cz/fitness-care-c106/" target="_blank" rel="sponsored noopener" style="color: var(--gold);">CLEANEE FITNESS CARE</a> (spolupráce). Jak čistit podložku a reformer krok za krokem, popisuji v článku <a href="/blog/jak-cistit-podlozku-a-reformer/" style="color: var(--gold);">Jak vyčistit podložku a reformer po cvičení</a>.</p>

  <h2>Štefan <em>v akci</em></h2>'''
s = once(s, '  <h2>Štefan <em>v akci</em></h2>', block, 'studio'); wr(p, s)

# 3) /blog/co-je-reformer-pilates/ – bod 6 v kapitole Jak poznat kvalitní reformer studio
p = 'blog/co-je-reformer-pilates/index.html'; s = rd(p)
anchor = 'Ve Fit Pilates kombinujeme všechny tři disciplíny pod jednou střechou — pilates pro kontrolu pohybu, silovka pro budování síly, box pro kardio a koordinaci.</p>\n'
add = anchor + '''
  <h3>6. Čistota strojů a podložek</h3>
  <p>Všimněte si, jestli jsou madla, opěrky a podložky při vašem příchodu utřené. V kvalitním studiu se stroje a podložky čistí po každém klientovi, ne jednou za den. Jak na to, popisuji v článku <a href="/blog/jak-cistit-podlozku-a-reformer/">Jak vyčistit podložku a reformer po cvičení</a>.</p>
'''
s = once(s, anchor, add, 'co-je'); wr(p, s)

# 4) /blog/ – karta + schema
p = 'blog/index.html'; s = rd(p)
s = once(s, '''    "blogPost": [
''', '''    "blogPost": [
      {
        "@type": "BlogPosting",
        "headline": "Jak vyčistit podložku a reformer po cvičení",
        "url": "https://fitpilates.cz/blog/jak-cistit-podlozku-a-reformer/",
        "datePublished": "2026-09-30",
        "author": { "@type": "Person", "name": "Štefan Bitto" }
      },
''', 'blog-schema')
s = once(s, '''<main class="blog-grid">
''', '''<main class="blog-grid">

  <article>
    <a href="/blog/jak-cistit-podlozku-a-reformer/" class="post-card">
      <picture>
        <source type="image/webp" srcset="/images/gallery/gallery-21-stefan-feet-thumb.webp">
        <img src="/images/gallery/gallery-21-stefan-feet-thumb.jpg" alt="Jak vyčistit podložku a reformer po cvičení" loading="lazy" decoding="async" width="800" height="500">
      </picture>
      <div class="post-body">
        <span class="post-cat">Studio v praxi</span>
        <h2>Jak vyčistit podložku a reformer po cvičení</h2>
        <p>Postup krok za krokem pro podložku na jógu i pilates a pro reformer. Citlivé materiály a rozdíl mezi čištěním a dezinfekcí. Ve spolupráci se značkou CLEANEE.</p>
        <div class="post-meta">
          <span>9 minut čtení · 30. 9. 2026</span>
          <span class="post-cta">Číst →</span>
        </div>
      </div>
    </a>
  </article>
''', 'blog-card'); wr(p, s)

# 5) sitemap.xml
p = 'sitemap.xml'; s = rd(p)
s = once(s, '''  <url>
    <loc>https://fitpilates.cz/blog/pilates-cviky/</loc>''', '''  <url>
    <loc>https://fitpilates.cz/blog/jak-cistit-podlozku-a-reformer/</loc>
    <lastmod>2026-09-30</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <image:image>
      <image:loc>https://fitpilates.cz/images/gallery/gallery-21-stefan-feet-full.jpg</image:loc>
      <image:title>Štefan Bitto na reformeru s podložkou — Fit Pilates Praha 10</image:title>
    </image:image>
  </url>
  <url>
    <loc>https://fitpilates.cz/blog/pilates-cviky/</loc>''', 'sitemap')
for f in ['studio/', 'blog/co-je-reformer-pilates/', 'blog/']:
    import re
    s, n = re.subn(r'(<loc>https://fitpilates\.cz/' + re.escape(f) + r'</loc>\s*<lastmod>)[0-9-]+(</lastmod>)', r'\g<1>2026-09-30\2', s)
wr(p, s)

# 6) llms.txt
p = 'llms.txt'; s = rd(p)
a = '- [Pilates aparáty](https://fitpilates.cz/blog/pilates-apparatus-stroje/): Srovnání Reformer, Cadillac, Chair, Ladder Barrel\n'
s = once(s, a, a + '- [Jak vyčistit podložku a reformer](https://fitpilates.cz/blog/jak-cistit-podlozku-a-reformer/): Postup čištění podložky a reformeru, čištění vs. dezinfekce (spolupráce CLEANEE)\n', 'llms'); wr(p, s)
import subprocess
subprocess.run([sys.executable, os.path.join(R,'scripts/_cleanee/build_article.py')], check=True)
print('OK – vše aplikováno')
