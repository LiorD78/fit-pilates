#!/usr/bin/env python3
"""
Mass marker injection do 14 zbývajících HTML souborů.

Pro každý soubor:
1. Smaže inline <style>#nav-overlay{display:none}...</style> v <head>
2. Nahradí <nav>...</nav> + <div id="nav-overlay">...</div> markery <!-- NAV-START --><!-- NAV-END -->
3. Nahradí <footer>...</footer> markery <!-- FOOTER-START --><!-- FOOTER-END -->
4. Smaže inline logo-swap <script> pokud existuje
"""

import re
from pathlib import Path

REPO = Path(__file__).parent.parent

# 14 souborů ke zpracování (studio už hotové)
FILES = [
    "index.html",
    "gdpr.html",
    "o-stefanovi/index.html",
    "pilates-allegro/index.html",
    "pilates-na-strojich/index.html",
    "pilates-praha-10/index.html",
    "rezervace/index.html",
    "silovy-trenink/index.html",
    "kondicni-box/index.html",
    "blog/index.html",
    "blog/co-je-reformer-pilates/index.html",
    "blog/pilates-apparatus-stroje/index.html",
    "blog/pilates-pro-zacatecniky/index.html",
    "blog/reformer-pilates-praha/index.html",
]

# Regex patterns
RE_INLINE_STYLE = re.compile(
    r'\n?\s*<style>#nav-overlay\{display:none\}[^<]*?</style>\n?',
    re.DOTALL
)

# Match <nav ...>...</nav> followed by optional whitespace and <div id="nav-overlay">...</div>
# Note: nav-overlay div has nested <div class="ov-meta"> etc., so we need to match outer </div>
RE_NAV_BLOCK = re.compile(
    r'<nav(?:\s[^>]*)?>.*?</nav>\s*<div\s+id="nav-overlay"[^>]*>.*?</div>\s*</div>',
    re.DOTALL
)

# Fallback: nav without overlay
RE_NAV_ONLY = re.compile(
    r'<nav(?:\s[^>]*)?>.*?</nav>',
    re.DOTALL
)

# Footer block
RE_FOOTER = re.compile(
    r'<footer(?:\s[^>]*)?>.*?</footer>',
    re.DOTALL
)

# Inline logo-swap script in head
RE_LOGO_SCRIPT = re.compile(
    r'\n?\s*<script>[^<]*?logoLight[^<]*?</script>\n?',
    re.DOTALL
)

# Drobečková nav uvnitř hero (musí ZŮSTAT) — match na <nav class="lph-bc">
RE_BREADCRUMB = re.compile(r'<nav\s+class="lph-bc"')

def process_file(filepath):
    """Process one HTML file. Returns (changed, summary_dict)."""
    path = REPO / filepath
    if not path.exists():
        return False, {"error": "file not found"}

    original = path.read_text(encoding="utf-8")
    content = original
    summary = {
        "inline_style_removed": False,
        "nav_replaced": False,
        "footer_replaced": False,
        "logo_script_removed": False,
        "has_breadcrumb": False,
    }

    # 1) Smazat inline <style>#nav-overlay...</style>
    new_content = RE_INLINE_STYLE.sub('\n', content)
    if new_content != content:
        summary["inline_style_removed"] = True
        content = new_content

    # 2) Check pro drobečkové nav uvnitř hero
    summary["has_breadcrumb"] = bool(RE_BREADCRUMB.search(content))

    # 3) Replace nav block (nav + overlay)
    new_content, count = RE_NAV_BLOCK.subn(
        '<!-- NAV-START -->\n<!-- NAV-END -->',
        content,
        count=1
    )
    if count > 0:
        summary["nav_replaced"] = True
        content = new_content
    else:
        # Fallback: jen nav bez overlay (např. gdpr.html může mít minimal nav)
        # ALE pozor — musíme přeskočit drobečkové nav (lph-bc) — ta není první!
        # Bezpečnější: hledat první <nav> co je hned po <body> nebo má id="nav" nebo class="site-nav"
        match = re.search(
            r'<nav(?:\s+(?:id="nav"|class="(?:site-nav|nav-solid|nav)"))[^>]*>.*?</nav>',
            content,
            re.DOTALL
        )
        if match:
            content = content[:match.start()] + '<!-- NAV-START -->\n<!-- NAV-END -->' + content[match.end():]
            summary["nav_replaced"] = True

    # 4) Replace footer block
    new_content, count = RE_FOOTER.subn(
        '<!-- FOOTER-START -->\n<!-- FOOTER-END -->',
        content,
        count=1
    )
    if count > 0:
        summary["footer_replaced"] = True
        content = new_content

    # 5) Smazat inline logo-swap script
    new_content = RE_LOGO_SCRIPT.sub('\n', content)
    if new_content != content:
        summary["logo_script_removed"] = True
        content = new_content

    # Write back if changed
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True, summary

    return False, summary


def main():
    print(f"Processing {len(FILES)} files in {REPO}\n")
    for f in FILES:
        changed, summary = process_file(f)
        marker = "✓" if changed else "·"
        actions = []
        if summary.get("inline_style_removed"):
            actions.append("style")
        if summary.get("nav_replaced"):
            actions.append("nav")
        if summary.get("footer_replaced"):
            actions.append("footer")
        if summary.get("logo_script_removed"):
            actions.append("logo-script")
        breadcrumb = " [has breadcrumb]" if summary.get("has_breadcrumb") else ""
        actions_str = ", ".join(actions) if actions else "no changes"
        print(f"  {marker} {f}: {actions_str}{breadcrumb}")
        if "error" in summary:
            print(f"      ERROR: {summary['error']}")

if __name__ == "__main__":
    main()
