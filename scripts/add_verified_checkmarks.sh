#!/bin/bash
# ============================================================
# add_verified_checkmarks.sh  (DEPRECATED — now handled in glossary.md)
#
# The glossary template (glossary.md) now AUTOMATICALLY shows a
# ✔️ checkmark next to any term whose page body starts with
# "Verified".  No script is needed — just add/remove the word
# "Verified" at the top of a term's body content.
#
# This script is kept only for auditing purposes: it lists which
# terms are verified and which are not.
#
# Usage:
#   cd <project-root>
#   bash scripts/add_verified_checkmarks.sh
# ============================================================

set -euo pipefail

TERMS_DIR="_terms"
VERIFIED=0
NOT_VERIFIED=0

if [[ ! -d "$TERMS_DIR" ]]; then
  echo "ERROR: '$TERMS_DIR' directory not found."
  echo "       Run this script from the project root."
  exit 1
fi

echo "═══════════════════════════════════════════"
echo "  Verified Terms Audit"
echo "═══════════════════════════════════════════"
echo

for file in "$TERMS_DIR"/*.md; do
  [[ -f "$file" ]] || continue
  filename=$(basename "$file")

  # Find closing front-matter fence
  closing_fence=$(awk '/^---$/{n++; if(n==2){print NR; exit}}' "$file")
  [[ -z "$closing_fence" ]] && continue

  body_start=$((closing_fence + 1))
  body_peek=$((closing_fence + 3))
  peek=$(sed -n "${body_start},${body_peek}p" "$file")

  if echo "$peek" | grep -q "^Verified"; then
    echo "  ✔️  $filename"
    VERIFIED=$((VERIFIED + 1))
  else
    NOT_VERIFIED=$((NOT_VERIFIED + 1))
  fi
done

echo
echo "═══════════════════════════════════════════"
echo "  Summary"
echo "═══════════════════════════════════════════"
echo "  Verified:   $VERIFIED"
echo "  Unverified: $NOT_VERIFIED"
echo "  Total:      $((VERIFIED + NOT_VERIFIED))"
echo "═══════════════════════════════════════════"
