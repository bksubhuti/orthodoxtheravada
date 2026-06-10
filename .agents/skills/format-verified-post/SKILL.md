---
name: format-verified-post
description: Formatting and standardizing verified glossary terms/posts, including adding the Verified tag, and formatting quote blocks (Pali and English).
---

# Formatting Verified Glossary Terms

Use this skill when the user asks to format a verified term, when a new term is marked as verified, or when cleaning up existing verified glossary posts.

## Verification Checklist

1. **Add the Verified Tag**
   - Place the word `Verified` on its own line with a blank line both before and after it, immediately following the front matter closing fence (`---`):
     ```markdown
     ---
     layout: single
     ...
     ---

     Verified

     ### Grammatical Analysis
     ```

2. **Format the Quote Section**
   - Place quotes under a `### Quote` heading.
   - Use standard markdown blockquotes (`> `).
   - Format Pali/English quote pairs as follows:
     - **Pāḷi line**: Entirely bolded (`**Pāli text**`), beginning with a capital letter and ending with two spaces to force a line break.
     - **English line**: Plain text on the very next line, beginning with a capital letter.
     - Separate different quote pairs with a blank blockquote line (`> `).
     - End the quote section with a blank blockquote line and an em-dash citation: `> — *Source* (Details)` or `> — [Link Text](/glossary/slug/) (Details)`.
   
   *Example quote block formatting:*
   ```markdown
   ### Quote
   > **Tena kho pana samayena aññataro bhikkhu tadahuposathe āpattiṃ āpanno hoti.**  
   > Now at that time, a certain bhikkhu had incurred an offense on the Uposatha day.  
   > 
   > **Atha kho tassa bhikkhuno etadahosi – ‘‘bhagavatā paññattaṃ ‘na sāpattikena uposatho kātabbo’ti.**  
   > Then it occurred to that bhikkhu: ‘The Blessed One has enjoined, “One who has incurred an offense should not perform the Uposatha.”  
   > 
   > — *Mahāvagga* (Uposathakkhandhaka, 169)
   ```
