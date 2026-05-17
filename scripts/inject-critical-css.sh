#!/usr/bin/env bash
# ============================================================
# Fit Pilates — Critical CSS Injection (FOUC fix)
# ============================================================
# Purpose: prevent FOUC on iOS Safari mobile where the unstyled
# nav menu + overlay + giant logo briefly appear before site.css
# applies. Inlines mobile-first safety defaults directly into <head>.
# ============================================================

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

CRITICAL_CSS='<style id="critical-css">
/* Critical CSS — FOUC prevention, mobile-first safety defaults.
   Full styling lives in /assets/css/site.css. */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Inter,sans-serif;color:#2b2e33;background:#fff;overflow-x:hidden;line-height:1.7}
img{max-width:100%;height:auto;display:block}
.site-nav{position:fixed;top:0;left:0;right:0;z-index:1000;display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:rgba(20,21,24,.32);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px)}
.site-nav__brand{display:flex;align-items:center;text-decoration:none;line-height:0}
.site-nav__logo{height:36px;width:auto;display:block}
.site-nav__logo--dark{display:none}
.site-nav__menu{display:none}
.site-nav__cta{display:none}
.site-nav__burger{display:block;background:transparent;border:0;cursor:pointer;padding:8px;width:44px;height:44px;position:relative;z-index:1001}
.site-nav__burger span{display:block;width:24px;height:2px;background:#fff;margin:5px auto;border-radius:2px}
.site-nav__overlay{display:none}
@media (min-width:901px){
  .site-nav__menu{display:flex;gap:30px;align-items:center;list-style:none}
  .site-nav__cta{display:inline-block;padding:11px 22px;background:#c49a3c;color:#fff;text-decoration:none}
  .site-nav__burger{display:none}
  .site-nav__logo{height:44px}
  .site-nav{padding:14px 56px}
}
</style>'

# Escape for sed
CRITICAL_CSS_ESC=$(printf '%s\n' "$CRITICAL_CSS" | sed 's/[&/\]/\\&/g' | tr '\n' '\f')

COUNT=0
for f in $(find . -name "index.html" -not -path "./node_modules/*"); do
  # Skip if already has critical CSS
  if grep -q 'id="critical-css"' "$f"; then
    echo "SKIP (already has critical CSS): $f"
    continue
  fi

  # Inject right before </head>
  python3 -c "
import sys
critical = '''$CRITICAL_CSS'''
path = '$f'
with open(path,'r',encoding='utf-8') as fh:
    html = fh.read()
if '</head>' not in html:
    print('NO </head> in '+path, file=sys.stderr); sys.exit(1)
new = html.replace('</head>', critical + '\n</head>', 1)
with open(path,'w',encoding='utf-8') as fh:
    fh.write(new)
print('  injected:', path)
"
  COUNT=$((COUNT + 1))
done

echo ""
echo "✓ Critical CSS injected into $COUNT file(s)"
