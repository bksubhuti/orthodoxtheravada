You are checking and fixing pages on the Orthodox Theravada website at /Users/bhantesubhuti/git/orthodoxtheravada (a Jekyll site; the owner is an orthodox Theravāda monk). The pages were first written by an AI, so some have wrong counts, items, names or references. Every page should now match its verified Pāḷi quote.

Read /Users/bhantesubhuti/git/orthodoxtheravada/.claude/skills/pali-quotes/SKILL.md in full, and follow the section "Content check: does the page match its quote?" exactly, along with the earlier rules (house style, never add "verified", don't commit). Skim /Users/bhantesubhuti/.claude/skills/tpr-research/SKILL.md for the tpr.py commands. Run tools as `python3 -I <full path> ...`. This is zsh on macOS: pass arguments separately, and do edits with Python or the Edit tool, not `sed -i`. If a command fails with "database is locked", wait a moment and retry.

Earlier quote-review reports in /Users/bhantesubhuti/git/orthodoxtheravada/.claude/quote-review/ (batch-*.md, rewrites.md) already note problems with many pages; read the row for each page first. Skip any path that no longer exists, since it may have been renamed or deleted. If a page has no quote, add one following the earlier sections of SKILL.md.

- A list with a real name but the wrong number or items gets FIXED, not deleted. If the count changes, rename the file with `git mv`.
- A traditional list that is real but post-canonical (a chant, or a commentary-only list) is fixed and cited from the latest layer that has it, or, if TPR has no source, the unsourced claims are removed.
- DELETE? is only for lists whose items or key terms don't exist at all, or that duplicate another page exactly; name the other page.
- Pages with the "verified" marker: FIX them too (the owner asked for this on 2026-10-17: "that was the point of going over my work"). Keep the marker exactly as it is, and use status FIXED-VERIFIED, listing every change.
- Don't leave open questions or "notes for the owner". When the page and the texts disagree, or something is unclear, settle it from the texts and commentaries (Aṭṭhakathā first, then Ṭīkā), then rewrite the page and replace the quote so that everything matches. Report what you did, not what the owner should decide.

Never write anything from memory: every Pāḷi word, count and reference you put on a page or in the report must come from a tpr.py result you saw.

Write one report row per page as soon as you finish it. At the end, check that every page has a row.

Reply briefly with: counts of PASS, FIXED, FIXED-VERIFIED and DELETE?; the renamed files; the DELETE? pages and the evidence for each; and the number of tool commands you ran.
