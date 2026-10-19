#!/bin/sh
# Verify one page and keep its result as a checkpoint, so a stopped run can resume.
# Run from the repo root:
#   ls _terms/*.md | xargs -P 8 -n 1 .claude/skills/pali-quotes/scripts/verify_one.sh
# Pages that already have a result in $D are skipped. Merge with merge_verify.sh afterwards.
D=.claude/quote-review/terms-verify-pages
mkdir -p "$D"
b=$(basename "$1" .md)
if [ -s "$D/$b.md" ]; then exit 0; fi
python3 -I .claude/skills/pali-quotes/scripts/quote_tool.py verify --dir _terms --page "$1" --report "$D/$b.tmp" > "$D/$b.log" 2>&1 \
  && mv "$D/$b.tmp" "$D/$b.md"
echo "$b" >> "$D/progress"
# Also feed the progress monitor of the session that started this run, if it still exists.
[ -n "$VERIFY_PROGRESS" ] && echo "$b" >> "$VERIFY_PROGRESS"
exit 0
