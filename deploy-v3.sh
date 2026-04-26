#!/bin/bash
# Fit Pilates Deploy v3 — comprehensive update
# Adds: pillar article, author page, studio gallery, shared CSS, photo refresh
set -e

echo "=== Fit Pilates Deploy v3 ==="
echo ""
echo "Changes summary:"
echo "  - 19 new authentic photos (homepage gallery, pillar, author)"
echo "  - 25 new photos in studio gallery (with lightbox)"
echo "  - WebP fallback for all new <picture> elements"
echo "  - NEW: blog/co-je-reformer-pilates/ (~3000 word pillar article)"
echo "  - NEW: o-stefanovi/ (author page with timeline + credentials)"
echo "  - NEW: studio/ (gallery with 25 photos in lightbox)"
echo "  - NEW: assets/css/site.css (shared styles)"
echo "  - Updated: sitemap.xml (6 URLs)"
echo "  - Refactored: pilates-allegro to use shared CSS + 2 inline figures"
echo "  - Restored: logo-badge.jpg favicon (small 345x400)"
echo ""

# Sanity check
echo "Sanity check..."
test -f index.html || { echo "FAIL: index.html missing"; exit 1; }
test -f blog/co-je-reformer-pilates/index.html || { echo "FAIL: pillar missing"; exit 1; }
test -f o-stefanovi/index.html || { echo "FAIL: author page missing"; exit 1; }
test -f studio/index.html || { echo "FAIL: studio gallery missing"; exit 1; }
test -f assets/css/site.css || { echo "FAIL: shared CSS missing"; exit 1; }
test -f sitemap.xml || { echo "FAIL: sitemap missing"; exit 1; }
test -f images/pillar-stretch.jpg || { echo "FAIL: pillar hero image missing"; exit 1; }
test -f images/gallery/gallery-01-courtyard-thumb.jpg || { echo "FAIL: gallery photos missing"; exit 1; }
echo "  ✓ All required files present"
echo ""

# Git commits — split into logical chunks for clean history
git add assets/css/site.css
git commit -m "feat(css): shared site.css for article pages (Allegro, pillar, author, studio)"

git add images/*.jpg images/*.webp
git commit -m "feat(images): 19 authentic photos × 6 variants (JPG+WebP, 3 sizes) for homepage refresh, pillar, author"

git add images/gallery/
git commit -m "feat(images): 25 gallery photos × 4 variants for /studio/ gallery"

git add index.html
git commit -m "refactor(homepage): replace generic photos with authentic FP studio shots, add WebP fallback via <picture>; preserve hero, bio Štefana, Programs cards"

git add pilates-allegro/index.html
git commit -m "refactor(allegro): use shared site.css; add 2 inline figures with WebP fallback"

git add blog/co-je-reformer-pilates/
git commit -m "feat(blog): pillar article 'Co je reformer pilates' (~3000 words, BlogPosting + FAQPage + BreadcrumbList schema)"

git add o-stefanovi/
git commit -m "feat(author): /o-stefanovi/ page with timeline, 4 credentials, photo gallery, Person schema"

git add studio/
git commit -m "feat(studio): /studio/ gallery page with 25 photos in lightbox (keyboard-navigable, WebP)"

git add sitemap.xml
git commit -m "feat(seo): sitemap.xml updated with pillar, author, studio (6 URLs total)"

echo ""
echo "=== Push to main ==="
git push origin main

echo ""
echo "✓ Deploy v3 complete. Netlify auto-deploy should trigger within seconds."
echo "  Check: https://app.netlify.com/projects/tagra-eu"
echo "  Live URL: https://fitpilates.cz"
