#!/bin/sh
# Merge the per-page results of verify_one.sh into one report. Run from the repo root.
# Lists any page still without a result, so you know whether the run is complete.
D=.claude/quote-review/terms-verify-pages
OUT=.claude/quote-review/terms-verify.md
missing=0
for p in _terms/*.md; do
  b=$(basename "$p" .md)
  [ -s "$D/$b.md" ] || { echo "no result yet: $b"; missing=$((missing+1)); }
done
{
  echo "# Quote verification report (_terms)"
  echo
  cat "$D"/*.md | grep -E "^\| [^P-]" | grep -v "^|---" | awk -F'|' '{print $4}' | sed 's/ [0-9]*%//; s/^ *//; s/ *$//' | sort | uniq -c | awk '{c=$1; $1=""; printf "%s:%s · ", substr($0,2), c} END{print ""}'
  echo
  echo "OK = found verbatim; CLOSE = minor differences; WEAK / NOT FOUND = check by hand; WRONG SOURCE = words real but not in the cited book; OK? = found, attribution names no checkable book."
  echo
  echo "| Page | Verified | Status | Found at | Cited as | Quote (start) |"
  echo "|---|---|---|---|---|---|"
  cat "$D"/*.md | grep -E "^\| " | grep -vE "^\| Page |^\|---"
} > "$OUT"
echo "pages without a result: $missing"
echo "report: $OUT"
