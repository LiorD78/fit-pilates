# Fit Pilates — Deploy v3

**Datum:** 26. 4. 2026
**Verze:** 3.0 (comprehensive content + assets refresh)

## Co tento deploy obsahuje

### 1. Nové stránky (3)
- **`/blog/co-je-reformer-pilates/`** — Pillar SEO článek (~3000 slov)
  - BlogPosting + FAQPage + BreadcrumbList schema
  - 9 FAQ (rozšířeno z původních 8)
  - 11 sekcí: definice, anatomie reformeru, Joseph Pilates historie, vs matwork, přínosy, pro koho, první lekce, jak poznat kvalitní studio, 5 typických cviků, výsledky, FAQ
  - Inline `<picture>` s WebP pro detail-kettlebells + pillar-stretch
  - DNS metoda Koláře, Joseph Pilates citace, autor box, related cards
- **`/o-stefanovi/`** — Author page s plnou bio, timeline a credentials
  - Person schema s hasCredential array
  - Timeline 6 milestonů (2000 → dnes)
  - 4 credentials cards
  - 5-photo gallery s WebP
  - Quote banner s legendárním citátem
- **`/studio/`** — Galerie 25 fotek s lightboxem
  - 4 sekce: hlavní sál, šatny, Štefan v akci, vybavení
  - Keyboard-navigable lightbox (Escape, šipky)
  - WebP fallback v lightboxu
  - BreadcrumbList schema

### 2. Foto refresh
- **19 fotek × 6 variant** (1920/1200/800px JPG+WebP) v `/images/`
  - Studio interiér: studio-main, corridor, locker, shower, logo-wall, logo-badge
  - Detaily vybavení: detail-clock, detail-gloves, detail-kettlebells, detail-springs
  - Trainer alt: trainer-hero, trainer-logo, trainer-pilates, trainer-fitness, trainer-reformer
  - Pillar/author: pillar-stretch, stefan-handstand, stefan-doorway, stefan-portrait
- **25 fotek × 4 varianty** (400px thumb + 1600px full v JPG+WebP) v `/images/gallery/`
- **Restored**: původní `logo-badge.jpg` (345×400 favicon)

### 3. Zachované fotky (per user request)
- `hero.jpg`, `hero-w1200.jpg`, `hero-w800.jpg` — homepage hero
- `trainer-action*.jpg`, `trainer-door.jpg` — bio Štefana sekce
- `pilates.jpg`, `fitness.jpg`, `boxing-studio.jpg` (+ w600/w900) — 3 Programs dlaždice

### 4. Sdílený CSS
- `assets/css/site.css` (120 řádků) — používá `pilates-allegro`, pillar, author, studio
- Homepage `index.html` si nechává inline CSS (žádné riziko regrese)

### 5. Updates
- `sitemap.xml` — 6 URLs (homepage, pillar, allegro, author, studio, gdpr)
- `index.html` — 9 nových `<picture>` elementů s WebP fallback
- `pilates-allegro/index.html` — refactored s shared CSS, 2 inline `<picture>` figures
- Footer logo: `logo-light.png` místo `logo-wall.jpg` (lepší kompozice)

## Jak nasadit

```bash
cd /tmp/build/repo
./deploy-v3.sh
```

Skript provede 9 atomic git commitů a push na main. Netlify auto-deploy spustí během sekund.

## Před deployem ověř

1. ✅ Všechny HTML mají validní `<html>`, `<body>`, `</html>`, `</body>` tagy
2. ✅ Všechny JSON-LD bloky jsou validní JSON
3. ✅ Sitemap.xml má 6 URLs s správnými lastmod dates
4. ✅ Žádný odkaz na neexistující obrázek

## Post-deploy úkoly (manuálně)

1. **Google Search Console** — submit nový sitemap, request indexaci pillar článku
2. **Bing Webmaster** — totéž
3. **Google Business Profile** — citation cleanup (firmy.cz má starou adresu Háje/Dubnova)
4. **Schema.org validator** — zkontrolovat https://validator.schema.org/ na všech 4 nových stránkách
5. **PageSpeed Insights** — měření po deployi (cíl: LCP < 2.5s, CLS < 0.1)

## Cíle SEO (90 dnů)

- Top 3 Google CZ na "co je reformer pilates"
- Top 5 na "reformer pilates praha 10"
- Top 5 na "pilates praha 10"
- Featured snippet na "co je reformer pilates" (definice na začátku článku optimalizovaná)

## Anti-AI signály v tomto deployi

1. ✅ **51 autentických fotek** ze studia — nejsilnější signál
2. ✅ **Konkrétní fakta**: Joseph Pilates 1945, prof. Pavel Kolář, ACI 2000, 24 let praxe, U Trati 886/52
3. ✅ **Reálná čísla**: 590 Kč, 790 Kč, 1290 Kč, max 3 osoby, 4–5 pružin
4. ✅ **Štefanův hlas**: 1. osoba, "v mé 24leté praxi", citace
5. ✅ **Kontroverzní názory**: "Pro úplného začátečníka je reformer často snazší než matwork"
6. ✅ **Konkrétní disclaimers**: "akutní bolesti = nejprve k fyzioterapeutovi"
7. ✅ **DNS metoda Koláře** — silný CZ E-E-A-T signál
