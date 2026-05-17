#!/usr/bin/env bash
# scripts/build-partials.sh
# Injekce _partials/nav.html a _partials/footer.html do markerů ve všech HTML souborech.
# Idempotentní — lze spouštět opakovaně.
#
# Markery v HTML:
#   <!-- NAV-START -->...<!-- NAV-END -->
#   <!-- FOOTER-START -->...<!-- FOOTER-END -->
#
# Použití:
#   bash scripts/build-partials.sh
#   nebo přes Netlify build command, nebo přes git pre-push hook.

set -euo pipefail
shopt -s nullglob globstar

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

NAV="_partials/nav.html"
FOOT="_partials/footer.html"

if [[ ! -f "$NAV" ]]; then
  echo "ERROR: $NAV not found" >&2
  exit 1
fi
if [[ ! -f "$FOOT" ]]; then
  echo "ERROR: $FOOT not found" >&2
  exit 1
fi

# Najít všechny HTML soubory (root + 1 úroveň podadresářů + blog/*)
mapfile -t HTML_FILES < <(
  find . -maxdepth 3 -name "*.html" \
    -not -path "./.git/*" \
    -not -path "./_partials/*" \
    -not -path "./node_modules/*" \
    -not -path "./scripts/*" \
    | sort
)

echo "Found ${#HTML_FILES[@]} HTML files"
PROCESSED=0
SKIPPED=0

for f in "${HTML_FILES[@]}"; do
  if ! grep -q "<!-- NAV-START -->" "$f" 2>/dev/null && ! grep -q "<!-- FOOTER-START -->" "$f" 2>/dev/null; then
    echo "  - skip (no markers): $f"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  TMP="$(mktemp)"
  awk -v NAV_FILE="$NAV" -v FOOT_FILE="$FOOT" '
    function slurp(path,   line, content){
      content = ""
      while ((getline line < path) > 0){
        content = content line "\n"
      }
      close(path)
      return content
    }
    BEGIN {
      nav_content = slurp(NAV_FILE)
      foot_content = slurp(FOOT_FILE)
      in_nav = 0
      in_foot = 0
    }
    /<!-- NAV-START -->/ {
      print "<!-- NAV-START -->"
      printf "%s", nav_content
      in_nav = 1
      next
    }
    /<!-- NAV-END -->/ {
      print "<!-- NAV-END -->"
      in_nav = 0
      next
    }
    /<!-- FOOTER-START -->/ {
      print "<!-- FOOTER-START -->"
      printf "%s", foot_content
      in_foot = 1
      next
    }
    /<!-- FOOTER-END -->/ {
      print "<!-- FOOTER-END -->"
      in_foot = 0
      next
    }
    in_nav || in_foot { next }
    { print }
  ' "$f" > "$TMP"

  if ! cmp -s "$f" "$TMP"; then
    mv "$TMP" "$f"
    echo "  ✓ updated: $f"
  else
    rm "$TMP"
    echo "  = no change: $f"
  fi
  PROCESSED=$((PROCESSED + 1))
done

echo ""
echo "Done. Processed: $PROCESSED, Skipped: $SKIPPED"
