# Fit Pilates — Project Context for Claude Code

## Co je tento projekt
**Fit Pilates** — boutique premium pilates studio v Praze 10 – Strašnicích.
- Web: **fitpilates.cz**
- Vlastník/lektor: **Štefan Bitto** (24+ let praxe, ACI Trenér fitness I. třídy, certifikovaný instruktor pilates)
- Adresa: U Trati 886/52, 100 00 Praha 10 – Strašnice
- Telefon: +420 604 925 249, email: stefanbitto@seznam.cz, IČO: 76121674

## Cílovka & positioning
- **Premium concierge service** pro affluent CZ klientelu — manažeři/CEO/podnikatelé/lékaři 35–55
- Time-poor, high disposable income
- Tón: **discreet luxury**, ne lifestyle
- Štefan = jediný osobní trenér klienta. Hybrid brand: Štefan + Fit Pilates

## Tech stack
- **Pure HTML/CSS/JS** — žádný framework, žádný npm build
- **GitHub** (LiorD78/fit-pilates) → **Netlify Edge** auto-deploy z `main` (deploy ~30–60s)
- **Doména:** fitpilates.cz (přes Netlify)
- **1 global CSS:** `assets/css/site.css`
- **1 global JS:** `assets/js/site.js`
- **11 HTML stránek:** index.html + 9 podstránek + gdpr.html
- **4 blog články** v /blog/
- **Pre-build skript:** připravujeme v `scripts/build-partials.sh` pro injection `_partials/nav.html` a `_partials/footer.html` do markerů `<!-- NAV-START --><!-- NAV-END -->` a `<!-- FOOTER-START --><!-- FOOTER-END -->`

## Designové konvence
- **Fonty:** Cormorant Garamond (nadpisy), Inter (body)
- **Barvy:** charcoal `#2b2e33`, gold `#c49a3c`, red `#c0392b`, cream `#f8f7f4`
- **Premium boutique vzhled** — vyhýbat se generickým SaaS prvkům, bento gridům, AI vzhledu
- **Reálné fotky** (51 profesionálních z 23.9.2025) jsou klíčový asset — neměnit hero, neměnit dlaždice programů
- **Allegro = název reformeru** (Balanced Body brand), NE disciplína. Důležité při psaní copy.
- **CTA:** „Diagnostická konzultace 590 Kč" (nahradilo dřívější „Vstupní lekce")

## Ceník
- Diagnostická konzultace / vstupní lekce: 590 Kč
- Skupinová lekce (max 3 osoby): 790 Kč
- Individuální lekce: 1 290 Kč
- Balíček 10 lekcí skupinový: 6 990 Kč
- Balíček 10 lekcí individuální: 11 490 Kč

## Equipment (vše Balanced Body)
- 3× Allegro reformer (jeden s Tower)
- Cadillac (Trapeze Table Speed-Rail)
- Ladder Barrel se Spine Corrector boxem
- Wunda Chair (Combo Chair)
- BOSU Elite, kettlebelly, TRX, Everlast box

## Pravidla pro Claude Code

### Git workflow
- **Nikdy commit do `main` přímo** — vždy do feature branche, pak PR
- Branch naming: `refactor/...`, `fix/...`, `feat/...`, `content/...`
- Commit messages česky, krátké a popisné (např. „Sjednocení nav lišty + footer napříč všemi stránkami")
- Před commit: `git status` check + smysluplné staging

### Kódové konvence
- HTML: 2-space indent, lowercase tag names, double-quoted attributes
- CSS: jeden global soubor `assets/css/site.css`, BEM-ish naming (`.site-nav__brand`), CSS custom properties v `:root`
- JS: vanilla, IIFE pattern, žádné dependencies, žádný npm
- Žádné inline `<style>` overrides v jednotlivých HTML souborech (čistit když najdeš)
- Žádné inline `<script>` blocks (kromě JSON-LD schema)

### Co NIKDY neměnit bez explicitního pokynu
- Homepage hero fotky a dlaždice programů (Štefan v nich není záměrně)
- Schema.org JSON-LD strukturovaná data (LocalBusiness, FAQPage, BreadcrumbList…)
- Souřadnice studia (50.0653696, 14.4951578)
- Telefon, email, IČO, adresu

### SEO konvence
- Každá stránka má **canonical URL**
- Meta description **150–160 znaků**
- OG image: `/opengraph-image.jpg`
- Strukturovaná data podle Schema.org (LocalBusiness, Service, FAQPage, BreadcrumbList, Person)
- Sitemap.xml manuálně udržovaný

### Po každé větší změně
1. Aktualizovat `llms.txt` pokud se přidá/odstraní stránka
2. Aktualizovat `sitemap.xml` pokud se přidá stránka
3. Aktualizovat datum v meta (cache-busting query strings `?v=DDMMYYYY` v CSS link)
4. Po deploy: ověřit live URL přes Netlify (~30-60s)

## Aktuální stav (17.5.2026)
- 7 indexovaných URL v Google
- Cílový 90-day goal: top 3 Google CZ pro core pilates keywords (Local Pack + organic)
- SEO progress: on-site 85%, technical 95%, lokální on-site 90%, **off-site (GBP+citace) 15%** ← největší díra
- Hub-and-spoke interní prolinkování: každá stránka má 7+ inbound linků

## Konkurenti SEO
- Organic: LIYOGA.cz, Natima.cz, Pilates4U.cz, PetraGlen.cz
- Lokálně Praha 10: FIT S LUCKOU, Bonpilates, Studio Pilates
- Premium ICP: Concept Health Club, BBC Health Club, privátní PT pro VIP

## Štefanův citát (signature messaging)
> „Cvičení není trest za to, co jste snědli. Je to oslava toho, co vaše tělo dokáže."
