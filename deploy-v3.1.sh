#!/usr/bin/env bash
# ============================================================
# Fit Pilates — Deploy v3.1 (CSS Refactor + Allegro Hero)
# ============================================================
# Run from inside the fit-pilates repo root.
# This patch unifies all CSS into site.css and adds Allegro
# hero photo. Apply on top of v3.
# ============================================================

set -e

echo "▸ Deploy v3.1: CSS Refactor + Allegro Hero"
echo ""

# Sanity check
if [ ! -f "index.html" ] || [ ! -f "assets/css/site.css" ]; then
  echo "✗ Error: run from fit-pilates repo root (with v3 already deployed)"
  exit 1
fi

git status --short

echo ""
read -p "Continue? [y/N] " confirm
[ "$confirm" != "y" ] && exit 0

# 1. CSS unification — extract homepage inline CSS to site.css
git add assets/css/site.css
git commit -m "refactor(css): unify all page styles into site.css

- Extract homepage inline <style> block (~25KB) into site.css
- Add unified .page-hero typography (matches homepage h1 weight 700, line-height 0.95)
- Add .nav-solid modifier for sub-page nav state
- Add hero-allegro, hero-stretch, hero-doorway, hero-studio modifiers
- Single source of truth — no inline <style> blocks except page-specific tweaks"

# 2. Allegro hero photo
git add images/allegro-hero*
git commit -m "feat(images): authentic Allegro hero photo

- Add allegro-hero.jpg/webp at 800/1200/1600/2000px from FP_portrety_010
- Štefan demonstrating lunge on Balanced Body Allegro reformer
- Used as background for /pilates-allegro/ hero section"

# 3. Homepage refactor (remove inline style, add link)
git add index.html
git commit -m "refactor(homepage): replace inline <style> with site.css link

- Strip 25KB inline CSS block, all rules moved to assets/css/site.css
- Page weight reduced from ~64KB to ~41KB
- Behavior unchanged — same rules, single source"

# 4. Sub-page hero cleanup
git add pilates-allegro/index.html blog/co-je-reformer-pilates/index.html o-stefanovi/index.html studio/index.html gdpr.html
git commit -m "refactor(sub-pages): clean hero, unify typography

- Remove duplicate visual breadcrumb in hero (kept in JSON-LD schema)
- Apply hero modifier classes (hero-allegro, hero-stretch, hero-doorway, hero-studio)
- Add nav-solid class to all sub-page navs
- Wrap hero content in .page-hero-inner for proper max-width
- Allegro page now uses authentic photo background"

echo ""
echo "✓ All commits created. Push:"
echo "  git push origin main"
echo ""
echo "Netlify will auto-deploy in ~30s."
