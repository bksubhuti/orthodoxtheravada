# Where the work stands (2026-10-18)

**2026-10-18 3rd window:** the 120 verified terms still without a row (TV_04b + TV_05–07) were re-split into /tmp/TVF_00–03 (30 each), 4 Sonnet agents running → content-TVF_00–03.md. If cut off: rerun on pages without a row (check `git diff` on the next page). Then terms-verify.
**2026-10-18 4th window (2nd seat):** TVF run cut off at 85/120. The 35 left are in /tmp/TVG_00–02 (3 Sonnet agents → content-TVG_00–02.md; sammasananana and vinaya were half-edited and the agents were told to finish them). Then terms-verify.
**To continue (next seat):** (1) for each /tmp/TVF_0N, list pages whose slug has no `| slug |` row in content-TVF_0N.md; (2) for the first unfinished page of each batch, check `git diff` for a half-done edit and finish or revert it; (3) launch Sonnet agents on the leftovers with the same prompt as the TVF run (batch-prompt.md + term pattern, keep `verified`, FIXED-VERIFIED), appending to the same report files; (4) check every page has a row; (5) run `python3 -I .claude/skills/pali-quotes/scripts/quote_tool.py verify --dir _terms --report .claude/quote-review/terms-verify.md`. At 50% of the window, 49/120 were done (~1%/page).

**2026-10-18 run:** quote_tool.py Peṭ→Pet fixed. Running: OWNER_FIX (/tmp/OWNER_FIX, 32 pages: all OWNER rows + open questions + puthujjana → content-OWNER_FIX.md), TU_04 rerun, TU_05 rerun, TV_00. TU_04 DONE (24 FIXED). OWNER_FIX DONE (24 FIXED-VERIFIED, 8 FIXED; renamed three-types-of-full-moon-uposatha-days → three-types-of-uposatha-days; all blocks verify OK). TU_05 DONE (19 FIXED, 1 FIXED-VERIFIED, DELETE? vacidhamma — already in the owner-approval queue; kamma-patha links to it). Window ran out mid-run: TV_00 DONE (32/32 rows); TV_01 7/32, TV_02 2/32, TV_03 4/32 (rerun these: append, skip pages with a row, check `git diff` on the next page for a half-done edit); TV_04–07 not started. Then terms-verify.
2026-10-18 (2nd account, budget 70%): owner approved renaming kayadhamma/vacidhamma/manodhamma → kayakamma/vacikamma/manokamma (git mv done, kamma-patha links fixed) and rewriting them (agent → content-KAMMA.md). Finishing TV_01–03 from /tmp/TVR_01–03 (remaining pages only). KAMMA DONE. TV_01 DONE (32). TV_02 DONE (32). TV_04a DONE (8). TV_03 DONE (32). Window ended at 86% (target was 75%): ~0.9% per verified-term page. 120 pages left ≈ 1.1 windows; launch 3 agents, stop launching at ~60%. TV_04 split: /tmp/TV_04a (8 pages, running) and /tmp/TV_04b (24, not started; append to content-TV_04.md). Next window: TV_04b, TV_05–07, then terms-verify. Still for owner: delete three-roots-of-demerit? Then TV_02–07 (4 at a time), then terms-verify. quote_tool.py verify now checks EVERY Quote block on a page (was first only).
Term pattern (owner, 2026-10-18): Mūla quote is the minimum; add the Aṭṭhakathā/Ṭīkā detailed definition and the Abhidhamma definition where they apply. Quotes must match tpr.py; Textual References must be correct even where no quote backs them.

# Earlier state (2026-10-17)

**Owner's rule (2026-10-17): no OWNER rows and no open questions.** Rewrite and requote every page, verified ones included (keep the marker), so that title, items, explanations and quote all match the texts. batch-prompt.md and SKILL.md already say this.

**Tomorrow, first:** go back through the OWNER rows and owner notes from earlier and fix them, using 1–2 agents:
- verified lists: three-supreme-shrines, two-types-of-gifts, twelve-links-of-dependent-origination, twenty-five-beautiful-mental-factors, twenty-four-conditional-relations, and every other row marked OWNER in content-L00–L14.
- open questions: two-chief-lay-female-supporters (Bv "Nandamātā ca uttarā"); triad-of-arisen-not-arisen-bound-to-arise (quote all of Dhs 54–56); three-divisions-of-the-vinaya-pitaka; paccekabuddha (Paramatthadīpanī attribution); three-types-of-full-moon-uposatha-days (title vs the 14th day).
- puthujjana: settled by Pp-a 214:5–7 ("Maggakkhaṇasmiñhi tesaṃ pahānāya paṭipanno nāma hoti … ettāvatā vissaṭṭhakammaṭṭhāno thūlabālaputhujjanova idha kathito"). Pp 199 means only the gross, foolish worldling who has given up meditation, so it does not conflict with the kalyāṇa-puthujjana. Put this on the page.
- quote_tool.py line 82: change "Peṭ" to "Pet".

- **Lists (_lists):** content check DONE for all lists (content-L00–L14). Still to do: (1) fix the verified lists marked OWNER, keeping the marker (the owner approved this on 2026-10-17); (2) the owner has to approve deleting three-roots-of-demerit, which duplicates three-roots-of-unwholesome-action (the `git rm` was blocked by the permission system). Also waiting for the owner's approval to delete, as invented terms: _terms/kayadhamma.md, manodhamma.md and vacidhamma.md (count of kāyadhamm-/manodhamm-/vacīdhamm- in the Mūla: 0/0/0; the real terms are kāyakamma, vacīkamma and manokamma; double-checked by the main session).
- **Terms (_terms, 397 pages):** IN PROGRESS. Unverified terms: /tmp/TU_00–05 (reports content-TU_NN.md). Verified terms: /tmp/TV_00–07; the owner allows fixing these too, keeping the marker, with status FIXED-VERIFIED. Done: TU_00, TU_01. TU_02 and TU_03 are DONE too (96 of 141 unverified terms). TU_04 was STOPPED after 1 row and TU_05 before writing any, so rerun both (skip pages that already have a row, and re-check the page TU_04 was editing when it stopped). Then do TV_00–07. Tool bug: quote_tool.py maps petakopadesa to the book id 'Peṭ', but TPR uses 'Pet', so _terms/petakopadesa.md gives a false WRONG SOURCE.
- **Real cost:** a term batch of 24 costs about 5–6% of a 5-hour window, not 2.5% (the usage went from 14% to 74% over 4 list and 4 term batches). Plan about 3 term batches per window. About 155 still need a Quote, and the existing quotes are unchecked.
- **Deleted so far** (staged, not committed): four-ways-of-pacing-the-alms-round, four-types-of-fear-in-the-forest, four-stages-of-the-patimokkha-confession, three-types-of-solitary-buddhas, eight-things-that-overcome-a-monks-mind, eleven-duties-of-a-novice, four-kinds-of-clinging-aggregates, four-objects-of-insight-meditation, four-types-of-speech-to-be-avoided-by-monks, four-types-of-lay-offerings-to-monastics, ten-subjects-for-frequent-recollection.
- **Nothing is committed.** The owner reviews, commits and pushes.

## To continue with the terms

1. `ls _terms/*.md > /tmp/terms.txt; split -l 25 -d /tmp/terms.txt /tmp/T_`
2. For each batch, start one Sonnet agent with this prompt: "Read your full instructions in .claude/skills/pali-quotes/batch-prompt.md and follow them exactly. These are TERM pages (glossary entries, not lists): check that the Quote defines or uses the term, that the Grammatical Analysis and Orthodox Definition match the texts and commentaries, and that the Textual References are correct; add a Quote if one is missing. Your pages: /tmp/T_NN. Your report: .claude/quote-review/content-T_NN.md"
3. Run about 3 agents at once. After each batch, check that every page has a row, and double-check any DELETE? before deleting anything.
4. Finally, run `python3 -I .claude/skills/pali-quotes/scripts/quote_tool.py verify --dir _terms --report .claude/quote-review/terms-verify.md`.

Budget: about 2.5% of a 5-hour window per batch of 25 pages.

## Later: more terms

The owner suggests puredhamma.net and dhammawiki.com as sources of term NAMES only:
- Take headwords from their page titles and indexes, read politely, respecting robots.txt.
- Never copy their text. It's copyrighted, and Pure Dhamma's readings often depart from the Aṭṭhakathā.
- Drop terms the glossary already has, then keep only those with `tpr.py count` > 0 in the Mūla or Aṭṭhakathā.
- Build each new term page quote-first from the texts and commentaries.

Other site ideas the owner may want:
- The research papers as articles.
- The ~18 missing core lists.
- A Dhammasaṅgaṇī mātikā index.
- An Abhidhammattha-saṅgaha chapter guide.
- Paritta pages.
- Owner: NEVER copy Pure Dhamma or Dhamma Wiki text; use their term lists only as a checklist. The goal is a reliable, more comprehensive orthodox site.
- Duplicate check: before adding a term, fold diacritics and spelling variants (thīna/thina, -a/-ā endings, Sanskrit forms such as nirvana → nibbāna) and compare with `_terms` slugs, titles and pali_spelling. Skip any match.

**2026-10-18 terms-verify (resumable):** the one-process verify was too slow (hours, silent), so it now runs per page, 8 in parallel, with each page's result kept as a checkpoint in `.claude/quote-review/terms-verify-pages/`. To start or resume, from the repo root: `ls _terms/*.md | xargs -P 8 -n 1 .claude/skills/pali-quotes/scripts/verify_one.sh` (pages that already have a result are skipped). When every page has a result: `.claude/skills/pali-quotes/scripts/merge_verify.sh` → `.claude/quote-review/terms-verify.md` (it also lists any page still missing). Then fix the WRONG SOURCE / NOT FOUND / WEAK rows.
**2026-10-18 terms-verify DONE:** all 397 term pages, 1,350 quotes: OK 1340, OK? 9 (attribution correct, the tool doesn't know those book names), CLOSE 1 (sammohavinodani: the verses match Vibh-a 7–14 exactly, but they span more paragraphs than the tool's window; no fix needed). Fixed: anathapindika (SN 10.8 quote joined two passages 16 paragraphs apart → split into S-i 3105:1-4 and 3122:1-7) and dhatukatha (Dhatuk 14 + 18 joined → split). Report: .claude/quote-review/terms-verify.md. Content check of the whole site is complete. Left: three-roots-of-demerit stays (owner, 2026-10-18); the owner reviews, commits and pushes.
**2026-10-18 owner review:** the owner had `Verified` removed from every edited page (281; list in .claude/quote-review/verified-removed.txt), so the site shows no ✔️ until re-approved. Review app: `python3 .claude/skills/pali-quotes/scripts/review_app.py` → http://127.0.0.1:8765, terms first and then lists (706 pages). Approve = git add (with an option to put `Verified` back); Needs work / Reject are saved with a note in .claude/quote-review/review-decisions.json and are resumable. Pages marked "needs" come back to Claude for fixing.
