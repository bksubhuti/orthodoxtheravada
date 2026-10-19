---
name: pali-quotes
description: Verify and complete the Pāḷi "### Quote" sections of the Orthodox Theravada site (_lists, _terms). Use when the user asks to check, audit or verify the quotes or references on the site, to see how many pages are done, or to add/finish quotes ("find real quotes for the lists", "do the next batch of lists", "which pages still need a quote?").
---

# Pāḷi quotes for the Orthodox Theravada site

Every list and term page should carry one real Pāḷi quote, found in the Tipiṭaka Pali Reader (TPR) databases, never typed from memory. This skill checks the quotes that are there and adds the missing ones in the site's own style.

Tools:
- `.claude/skills/pali-quotes/scripts/quote_tool.py`: `status`, `verify`, `format` (run with `python3 -I`).
- `~/.claude/skills/tpr-research/scripts/tpr.py`: `search`, `count`, `show`, `books`, `commentary` (the tpr-research skill; read its SKILL.md once for the commands).

## Rules the owner has set

1. **No `Verified` marker in pages.** The site no longer uses one. The owner's review is tracked in `.claude/quote-review/review-decisions.json` by `scripts/review_app.py`, which diffs against the baseline commit in `.claude/quote-review/baseline.json`. Never write to either file; only the owner records decisions.
2. **Quote pass: add, don't rewrite.** When only adding quotes, change only the `### Quote` section. **In the content check (below), rewrite whatever the texts contradict.** The owner wants every page to match its quote, with no open notes left for the owner.
3. **Search before you claim.** Every quote comes from `tpr.py search`/`show`, read in context. If no source is found, say so in the report; don't force a quote.
4. Don't commit or push unless asked.

## Step 1: see what is done

```
python3 -I .claude/skills/pali-quotes/scripts/quote_tool.py status --dir _lists          # V/Q/L flags per page
python3 -I .claude/skills/pali-quotes/scripts/quote_tool.py status --dir _lists --missing
python3 -I .claude/skills/pali-quotes/scripts/quote_tool.py verify --dir _lists --report .claude/quote-review/lists-verify.md
```
`verify` checks each **bold** Pāḷi line of every Quote against all 1.28M sentences: **OK** (verbatim, and in the book the attribution names), **WRONG SOURCE** (the words are real, but not in the book cited — a misattributed quote), **OK?** (found, but the attribution names no book the tool knows), **CLOSE** (spelling or punctuation differences), **WEAK/NOT FOUND** (check by hand; possibly invented). It takes about 90 s per 300 pages. For `_terms` use `--dir _terms`.

## Step 2: choose the best quote

For each page, in this order of preference:
1. **The Mūla passage that sets out the whole list** in its stock formula ("Pañcimāni, bhikkhave, nīvaraṇāni. Katamāni pañca? …"). Search the formula: `tpr.py search '"kāmacchandanīvaraṇaṃ byāpādanīvaraṇaṃ"' --layer mula`.
2. If the page cites a sutta, prefer **that sutta's** passage, if it really contains the list. If it doesn't, use the passage that does and report the mismatch.
3. Sutta or Vinaya before Abhidhamma for practice lists; Dhammasaṅgaṇī/Vibhaṅga/Paṭṭhāna for Abhidhamma lists.
4. Only if there is no Mūla source: the **Aṭṭhakathā** (name it), then Ṭīkā or Abhidhammatthasaṅgaha. Say in the attribution which layer it is.
5. **Length:** the opening formula plus the list, at most about 6 sentences. For a long list (the 52 cetasikas, 24 paccayas) quote the heading and first items. Stock refrains between items ("Ayampi dhammo sāraṇīyo…") may be cut after the first item by ending the quote there.
6. Check the sutta number from the heading lines just before the passage (`tpr.py show BOOK PARA` on the paragraphs above, e.g. "2. Nīvaraṇasuttaṃ", "64. …").

## Step 3: write it in the house style

Generate the block, never hand-type it (give several refs to join consecutive paragraphs, e.g. `Th 3836:3-4 3837:1-2`):
```
python3 -I .claude/skills/pali-quotes/scripts/quote_tool.py format A-ix 444:1-3 \
  --cite "[Aṅguttara Nikāya](/glossary/anguttara-nikaya/) (AN 9.64, Nīvaraṇa Sutta)"
```
It prints:
```
### Quote
> **“Pañcimāni, bhikkhave, nīvaraṇāni. Katamāni pañca? Kāmacchandanīvaraṇaṃ, … pañca nīvaraṇāni.**  
> “Monks, there are these five hindrances. What are the five? …  
>  
> — [Aṅguttara Nikāya](/glossary/anguttara-nikaya/) (AN 9.64, Nīvaraṇa Sutta) · [TPR](https://tpr.pali.tools/open?…)
```
- Insert it **directly above `### Textual References`** (that is where the existing 260 quotes sit).
- The attribution links the collection's glossary page when one exists (`ls _terms | grep nikaya`). Slugs: `digha-nikaya`, `majjhima-nikaya`, `samyutta-nikaya`, `anguttara-nikaya`, `itivuttaka`, `culavagga`, `vinaya-pitaka`, `kathavatthu`, `abhidhammatthasangaha`, `visuddhimagga`.
- English is TPR's installed translation. If it is wrong or missing, write your own and add `(tr. Claude)` after it.
- A page that already has a Quote: leave it unless `verify` says WEAK/NOT FOUND. If the text is OK but there's no TPR link, add ` · [TPR](link)` to its attribution (`tpr.py link BOOK PARA:LINE`).

## Step 4: the review report

Append one row per page to `.claude/quote-review/YYYY-MM-DD.md` (create the folder if needed; Jekyll ignores dot-folders):

```
| Page | Quote source | Status | Note for the owner |
|---|---|---|---|
| five-hindrances | A-ix 444:1-3 (AN 9.64) | added | Textual References says SN 46.55; the Nīvaraṇa Sutta is AN 9.64 (SN 46.55 = Saṅgārava, the water similes). |
| seven-vows-of-sakka | S-i 3334:2-4 (SN 11.11) | added | Page says SN 11.11 was taught to Mahāli; it is addressed to the monks. Mahāli = SN 11.13 (S-i 3365). |
| forty-tooth-relics… | none | NO SOURCE | Searched "dāṭhā", "cattālīsa dant": 0 Mūla, 0 Aṭṭhakathā. Later tradition? |
```
Write each row as soon as the page is done (not at the end), so a network outage loses nothing. Then run `verify --page` on every page you touched; each new quote must come back **OK**.

## Doing many pages

- Work in batches of about 25 pages (`status --missing` gives the list, and `split -l 24` cuts it up). With the Agent tool, give each batch to one agent (model `sonnet`), with this SKILL.md path, the page list and its **own** report file (`.claude/quote-review/batch-NN.md`) so that parallel agents never write to the same file. Run about 3 batches at once.
- After each batch: run `verify` on the batch, read 2–3 new quotes yourself with `tpr.py show`, and give the user the report rows that need their attention (wrong references, NO SOURCE).
- Cost guide: about 1–2% of a 5-hour Claude plan window per 25 pages.

## Known pitfalls

- A stock formula appears in many places (`verify` may report "found at" a different sutta with the same words). That's fine if the cited sutta also has it; check with `show`.
- Search with the compound as written in CST: `thinamiddha` (not `thīna`), `uddhaccakukkucca`, and so on. Try `prefix*` forms when a search comes back empty.
- 67 non-canonical books (Abhidhammāvatāra, Cūḷagandhavaṃsa, Jātaka-ṭīkā, …) are not in TPR's page index: `format` then prints no TPR link. Cite by book and paragraph and note it in the report.

## Content check: does the page match its quote?

Much of the site was first written by an AI, and some of it is invented. A page passes only if what it says is backed by its quote and the texts. For each page:

1. **Pull the source fresh.** Take the passage from the Quote's TPR link or attribution, and run `tpr.py show BOOK PARA` on it and on the paragraphs around it, including the sutta heading. Also run `quote_tool.py verify --page`; it must say OK (not WRONG SOURCE or WEAK).
2. **Check, against the source:**
   - **Title and `list_count`:** the number in the title, the slug and `list_count` match the number of items the source gives.
   - **`pali_title`:** the Pāḷi name occurs in the texts (`tpr.py count`). If it doesn't, use the source's own wording.
   - **The List:** every item is in the source, in the source's order, with the source's Pāḷi spelling. No items are missing and none are added.
   - **Explanations:** each concrete claim (who taught it, to whom, where, a number, a story detail) is in the sutta or its Aṭṭhakathā. General, uncontroversial glosses are fine.
   - **Textual References:** sutta names and numbers match the headings in the text (CST numbering; note PTS/Bodhi numbering only if you are sure). Each cited text really contains the list.
   - **Quote relevance:** the quote is the list itself (or the term's definition), not merely a passage that mentions it.
3. **Fix it on the page:**
   - Correct the count, title, slug (with `git mv`), `pali_title`, item names and spellings, and references, so they match the source.
   - Delete specific claims that have no source; don't invent replacements.
   - Replace an irrelevant or weak quote with the right one (made with `format`).
   - Keep the owner's structure and tone, and keep edits as small as the truth allows.
4. **Leave no open questions:** settle each one from the Aṭṭhakathā or Ṭīkā, rewrite the page, and replace the quote so that everything matches. (Owner, 2026-10-17.)
5. **No source at all** (the list itself is invented): don't fix it. Mark it **DELETE?** in the report, with the searches you ran and their counts; the main session double-checks and deletes.
6. **Report:** one row per page in your `content-NN.md`:
   `| Page | PASS / FIXED / DELETE? | What was wrong and what you changed (with refs) |`

Afterwards, grep the repo (excluding `_site`, `.claude` and `scratch`) for links to any slug you renamed, and update them.
