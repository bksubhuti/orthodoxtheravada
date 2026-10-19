#!/usr/bin/env python3
"""Check and write the ### Quote sections of the Orthodox Theravada site.

  status  [--dir _lists]                 which pages are verified / have a quote / have a TPR link
  verify  [--dir _lists] [--page FILE]   check every bold Pali line of each Quote against the TPR database
          [--report FILE]                (writes a Markdown review report as well as printing a summary)
  format  BOOK PARA:L1-L2 --cite TEXT    print a Quote block in the site's house style, with a TPR link

Uses tpr.py from the tpr-research skill (TPR_PY, or ~/.claude/skills/tpr-research/scripts/tpr.py).
Everything is read-only except the report file you name.
"""
import argparse
import difflib
import glob
import importlib.util
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
TPR_PY = os.environ.get("TPR_PY", os.path.expanduser("~/.claude/skills/tpr-research/scripts/tpr.py"))
if not os.path.exists(TPR_PY):
    sys.exit(f"tpr.py not found at {TPR_PY}. Install the tpr-research skill or set TPR_PY.")
spec = importlib.util.spec_from_file_location("tpr", TPR_PY)
tpr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tpr)

VERIFIED = re.compile(r"\A---.*?---\s*verified", re.S | re.I)
QUOTE_HEAD = re.compile(r"^##{1,3}\s+Quote\b.*$", re.M)
NEXT_HEAD = re.compile(r"^##{1,3}\s", re.M)
BOLD = re.compile(r"\*\*(.+?)\*\*")
WORD = re.compile(r"[a-zāīūṃṁñṅṇṭḍḷ]+")
SKIP = {"pe", "la", "ti", "ca", "vā", "pi", "hi", "na", "ti"}


def connect():
    return tpr.connect(tpr.find_dir())


def words(t):
    t = tpr.VARIANT.sub("", tpr.TAG.sub("", t).lower())   # <b>x</b>ti stays one word, as in tpr.clean
    t = re.sub(r"\([^)]*\d[^)]*\)", " ", t)          # (ma. ni. 1.12) style refs
    return [w for w in WORD.findall(t) if w not in {"pe"}]


def pages(d, page=None):
    if page:
        return [page]
    return sorted(glob.glob(os.path.join(ROOT, d, "*.md")))


def quote_section(text):
    m = QUOTE_HEAD.search(text)
    if not m:
        return None
    rest = text[m.end():]
    n = NEXT_HEAD.search(rest)
    return rest[: n.start()] if n else rest


def quote_sections(text):
    """Every Quote block on the page (pages may carry one per layer: Mūla, Aṭṭhakathā, Abhidhamma)."""
    out = []
    for m in QUOTE_HEAD.finditer(text):
        rest = text[m.end():]
        n = NEXT_HEAD.search(rest)
        out.append(rest[: n.start()] if n else rest)
    return out


def page_info(path):
    text = open(path, encoding="utf-8").read()
    q = quote_section(text)
    return {
        "file": os.path.relpath(path, ROOT),
        "verified": bool(VERIFIED.match(text)),
        "quote": q is not None,
        "link": bool(q and "tpr.pali.tools" in q),
        "bold": [b.strip() for b in BOLD.findall(q or "")],
        "text": text,
        "blocks": quote_sections(text),
    }


# Attribution keyword (diacritics stripped, lower case) -> ePitaka book-id prefixes it can refer to.
SOURCES = {
    "digha": ["D-"], "dn ": ["D-"], "majjhima": ["M-"], "mn ": ["M-"], "samyutta": ["S-"], "sn ": ["S-"],
    "anguttara": ["A-"], "an ": ["A-"], "khuddakapatha": ["Khp"], "dhammapada": ["Dhp"], "udana": ["Ud"],
    "itivuttaka": ["It"], "iti ": ["It"], "sutta nipata": ["Sn"], "suttanipata": ["Sn"], "snp": ["Sn"],
    "vimanavatthu": ["Vv"], "petavatthu": ["Pv"], "theragatha": ["Th"], "therigatha": ["Thī"],
    "apadana": ["Ap"], "buddhavamsa": ["Bv"], "cariyapitaka": ["Cp"], "jataka": ["Ja"], "niddesa": ["Nidd"],
    "patisambhida": ["Paṭis"], "milinda": ["Mil"], "netti": ["Nett"], "petakopadesa": ["Pet"],
    "vinaya": ["Vin"], "parajika": ["Vin-i"], "pacittiya": ["Vin-ii"], "mahavagga": ["Vin-iii", "D-ii", "S-v"],
    "culavagga": ["Vin-iv"], "cullavagga": ["Vin-iv"], "parivara": ["Vin-v"], "patimokkha": ["Vin", "Dvem"],
    "dhammasangani": ["Dhs"], "vibhanga": ["Vibh", "Vin-i", "Vin-ii"], "dhatukatha": ["Dhātuk", "Dhatuk"],
    "puggala": ["Pp"], "kathavatthu": ["Kv"], "yamaka": ["Yam"], "patthana": ["Paṭṭh"],
    "abhidhammattha": ["Abhidh-s"], "sangaha": ["Abhidh-s"], "vibhavini": ["Abhidh-s-t"],
    "abhidhammavatara": ["Abhidh-av"], "visuddhimagga": ["Vism"], "vism": ["Vism"],
    "atthasalini": ["As"], "sammohavinodani": ["Vibh-a"], "samantapasadika": ["Sp"], "kankhavitarani": ["Kkh"],
    "sumangala": ["Sv"], "papancasudani": ["Ps"], "saratthappakasini": ["Spk"], "manorathapurani": ["Mp"],
    "paramatthajotika": ["Pj"], "paramatthadipani": ["Ud-a", "It-a", "Vv-a", "Pv-a", "Th-a", "Thī-a", "Cp-a", "PmtDīp"],
    "madhuratthavilasini": ["Bv-a"], "visuddhajanavilasini": ["Ap-a"], "saddhammappakasini": ["Paṭis-a"],
    "saddhammapajjotika": ["Nidd-a"], "dhammapadatthakatha": ["Dhp-a"], "jatakatthakatha": ["Ja-a"],
    "khuddasikkha": ["Khuddas"], "saratthadipani": ["Sp-t"], "vimativinodani": ["Vmv"],
    "vajirabuddhi": ["Vjb"], "mahavamsa": ["Mhv"], "mp-t": ["Mp-t"], "sv-pt": ["Sv-pt"], "mahavaggatika": ["Sv-pt"], "mahavaggatika ": ["Sv-pt"], "thupavamsa": ["Thup"], "dhatuvamsa": ["Dhātv"], "mulatika": ["As-mt", "Vibh-mt"], "anutika": ["Dhs-anuṭ", "Vibh-anuṭ"], "paramatthadipani ": ["PmtDīp"],
}


def plain(t):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def cited_prefixes(attribution):
    a = plain(re.sub(r"\]\([^)]*\)", "]", attribution)) + " "
    return sorted({p for k, ps in SOURCES.items() if k in a for p in ps})


def find(con, segment, prefer=()):
    """Location of a bold Pali segment: (status, ratio, book, para, line, layer, all_ok_books).
    Among verbatim matches it prefers a book the attribution names, then the Mūla."""
    ws = words(segment)
    if len(ws) < 3:
        return ("short", 1.0, None, None, None, None, [])
    keys = sorted({w for w in ws if len(w) >= 5}, key=len, reverse=True)[:4] or ws[:2]
    # Score paragraphs by how many key words they hold (a quote may span several sentences).
    # The first letter is dropped so LIKE is not defeated by a capital with a diacritic.
    score, first = {}, {}
    for k in keys:
        hit = set()
        for book, para, line, cat in con.execute(
                "SELECT s.book_id, s.para_id, s.line_id, b.category FROM epi.sentences s JOIN epi.books b "
                "ON b.book_id=s.book_id WHERE s.pali LIKE ? LIMIT 5000", (f"%{k[1:]}%",)):
            for p in range(para - 3, para + 4):
                if (book, p) not in hit:
                    hit.add((book, p))
                    score[(book, p)] = score.get((book, p), 0) + 1
            first.setdefault((book, para), (line, cat))
    extra = []
    if prefer:   # also shortlist the best paragraphs inside the cited books
        sc = {}
        for k in keys:
            seen = set()
            for book, para, line, cat in con.execute(
                    "SELECT s.book_id, s.para_id, s.line_id, b.category FROM epi.sentences s JOIN epi.books b "
                    "ON b.book_id=s.book_id WHERE s.pali LIKE ? AND (" + " OR ".join("s.book_id LIKE ?" for _ in prefer)
                    + ") LIMIT 3000", [f"%{k[1:]}%"] + [p + "%" for p in prefer]):
                if (book, para) not in seen:
                    seen.add((book, para))
                    sc[(book, para)] = sc.get((book, para), 0) + 1
                first.setdefault((book, para), (line, cat))
        extra = sorted(sc, key=lambda kp: -sc[kp])[:20]
    cands = sorted((kp for kp in score if kp in first), key=lambda kp: -score[kp])[:60]
    cands += [kp for kp in extra if kp not in cands]
    found = []
    for book, para in cands:
        line, cat = first[(book, para)]
        ctx = con.execute("SELECT pali FROM epi.sentences WHERE book_id=? AND para_id BETWEEN ? AND ? "
                          "ORDER BY para_id, line_id", (book, para - 3, para + 6)).fetchall()
        cw = words(" ".join(r[0] for r in ctx))
        sm = difflib.SequenceMatcher(None, ws, cw, autojunk=False)
        found.append((sum(b.size for b in sm.get_matching_blocks()) / len(ws), book, para, line, cat))
    if not found:
        return ("NOT FOUND", 0.0, None, None, None, None, [])
    top = max(f[0] for f in found)
    ok = [f for f in found if f[0] >= max(0.97, top - 0.02)]
    rank = lambda f: (any(f[1].startswith(p) for p in prefer), f[4] == "Mūla", f[0])
    r, book, para, line, cat = max(ok or found, key=rank)
    status = "OK" if r >= 0.97 else "CLOSE" if r >= 0.85 else "WEAK"
    return (status, r, book, para, line, cat, sorted({f[1] for f in ok}))


def cmd_status(a):
    infos = [page_info(p) for p in pages(a.dir, a.page)]
    for i in infos:
        flags = ("V" if i["verified"] else "-") + ("Q" if i["quote"] else "-") + ("L" if i["link"] else "-")
        if not a.missing or not i["quote"]:
            print(f"{flags}  {i['file']}")
    n = len(infos)
    print(f"\n{n} pages · verified {sum(i['verified'] for i in infos)} · with Quote {sum(i['quote'] for i in infos)}"
          f" · with TPR link {sum(i['link'] for i in infos)} · needing a Quote {sum(not i['quote'] for i in infos)}")
    print("Flags: V = body starts with 'verified', Q = has ### Quote, L = Quote has a TPR link")


def cmd_verify(a):
    con = connect()
    out, tally = [], {}
    todo = pages(a.dir, a.page)
    for n, p in enumerate(todo, 1):
        if not os.path.exists(p):      # renamed or deleted while the run was going
            continue
        print(f"[{n}/{len(todo)}] {os.path.basename(p)}", flush=True)
        i = page_info(p)
        if not i["quote"]:
            status = "NO QUOTE"
            tally[status] = tally.get(status, 0) + 1
            out.append(f"| {i['file']} | {'✓' if i['verified'] else ''} | NO QUOTE | | |")
            continue
        checks = []
        for blk in i["blocks"]:
            attrib = " ".join(re.findall(r"^>\s*[—–-]\s*(.+)$", blk, re.M))
            bold = [b.strip() for b in BOLD.findall(blk)]
            checks += [(seg, attrib, True) for seg in bold] or [("(no bold Pali in Quote)", attrib, False)]
        for seg, attrib, has_bold in checks:
            prefer = cited_prefixes(attrib)
            st, ratio, book, para, line, cat, oks = (find(con, seg, prefer) if has_bold
                                                     else ("NO BOLD", 0, None, None, None, None, []))
            if st == "short":
                continue
            # Attribution check: the source named under the quote should be where the words are.
            if st == "OK" and prefer and not any(b.startswith(p) for b in oks for p in prefer):
                st = "WRONG SOURCE"
            elif st == "OK" and not prefer:
                st = "OK?"          # found, but the attribution names no book the tool knows
            tally[st] = tally.get(st, 0) + 1
            where = f"{book} {para}:{line} ({cat})" if book else ""
            cited = re.sub(r"\s*·\s*\[TPR\]\([^)]*\)", "", attrib)[:60].replace("|", "/")
            out.append(f"| {i['file']} | {'✓' if i['verified'] else ''} | {st} {ratio:.0%} | {where} | {cited} | "
                       f"{seg[:60].replace('|', '/')}{'…' if len(seg) > 60 else ''} |")
            print(f"{st:12} {ratio:5.0%}  {i['file']}  {where}  [cited: {cited}]", flush=True)
    summary = " · ".join(f"{k}: {v}" for k, v in sorted(tally.items()))
    print("\n" + summary)
    if a.report:
        with open(a.report, "w", encoding="utf-8") as f:
            f.write(f"# Quote verification report\n\n{summary}\n\n"
                    "OK = found verbatim (≥97% of words in order); CLOSE = minor differences (spelling, "
                    "punctuation, omitted words); WEAK / NOT FOUND = check by hand. WRONG SOURCE = the words "
                    "are real but are not in the book the attribution names. OK? = found, but the attribution "
                    "names no book the tool can check.\n\n"
                    "| Page | Verified | Status | Found at | Cited as | Quote (start) |\n|---|---|---|---|---|---|\n")
            f.write("\n".join(out) + "\n")
        print(f"Report written to {a.report}")


def cmd_link(a):
    """Add a TPR link to every Quote that verifies but has none. Changes no wording."""
    con = connect()
    done = skipped = 0
    for p in pages(a.dir, a.page):
        if not os.path.exists(p):
            continue
        i = page_info(p)
        if not i["quote"] or i["link"] or not i["bold"]:
            continue
        text = i["text"]
        q = quote_section(text)
        attrib = " ".join(re.findall(r"^>\s*[—–-]\s*(.+)$", q, re.M))
        seg = max(i["bold"], key=lambda b: len(words(b)))      # skip short bold headings
        st, ratio, book, para, line, cat, oks = find(con, seg, cited_prefixes(attrib))
        if st != "OK":
            skipped += 1
            print(f"skip ({st} {ratio:.0%})  {i['file']}")
            continue
        first = con.execute("SELECT pali FROM epi.sentences WHERE book_id=? AND para_id=? AND line_id=?",
                            (book, para, line)).fetchone()
        r = tpr.tpr_link(con, book, para, line, first[0] if first else "")
        if not r:
            skipped += 1
            print(f"skip (no TPR page for {book})  {i['file']}")
            continue
        url = r[0]
        lines = q.split("\n")
        idx = [n for n, l in enumerate(lines) if re.match(r"^>\s*[—–-]\s*\S", l)]
        if idx:
            n = idx[-1]
            lines[n] = lines[n].rstrip() + f" · [TPR]({url})"
        else:
            name = con.execute("SELECT book_name FROM epi.books WHERE book_id=?", (book,)).fetchone()[0]
            bq = [n for n, l in enumerate(lines) if l.lstrip().startswith(">")]
            if not bq:
                skipped += 1
                print(f"skip (quote is not a > block)  {i['file']}")
                continue
            last = bq[-1]
            lines[last + 1:last + 1] = [">  ", f"> — *{name}* · [TPR]({url})"]
        new_q = "\n".join(lines)
        print(f"link  {i['file']}  -> {book} {para}:{line}")
        if not a.dry_run:
            open(p, "w", encoding="utf-8").write(text.replace(q, new_q, 1))
        done += 1
    print(f"\n{'would add' if a.dry_run else 'added'} {done} links · skipped {skipped}")


def cmd_format(a):
    con = connect()
    lang = tpr.default_lang(con, "en")
    rows, para = [], None
    for ref in a.ref:                      # several refs are joined, e.g. 3836:4-5 3837:1-2
        p, l1, l2 = tpr.parse_ref(ref)
        para = para or p
        rows += tpr.lines(con, a.book, p, l1, l2, lang)
    pali = " ".join(tpr.clean(r[1]) for r in rows).replace("‘‘ ", "“").replace(" ’’", "”")
    pali = re.sub(r"^\(?\d+\)?\s*\.\s*", "", pali)       # leading paragraph number "64."
    trans = " ".join(tpr.clean(r[2]) for r in rows if r[2]).strip()
    link = tpr.tpr_link(con, a.book, para, rows[0][0], rows[0][1])
    tail = f" · [TPR]({link[0]})" if link else ""
    print("### Quote")
    print(f"> **{pali}**  ")
    if trans:
        print(f"> {trans}  ")
    print(">  ")
    print(f"> — {a.cite}{tail}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("status", "verify"):
        s = sub.add_parser(name)
        s.add_argument("--dir", default="_lists", help="_lists, _terms or _articles (default _lists)")
        s.add_argument("--page", help="one page file instead of the whole folder")
        if name == "status":
            s.add_argument("--missing", action="store_true", help="only list pages without a Quote")
        else:
            s.add_argument("--report", help="write a Markdown report to this file")
    l = sub.add_parser("link", help="add a TPR link to every verified Quote that lacks one (no wording changes)")
    l.add_argument("--dir", default="_lists")
    l.add_argument("--page")
    l.add_argument("--dry-run", action="store_true")
    f = sub.add_parser("format")
    f.add_argument("book")
    f.add_argument("ref", nargs="+", help="PARA:L1-L2 (give several to join consecutive paragraphs)")
    f.add_argument("--cite", required=True,
                   help='attribution, e.g. "[Aṅguttara Nikāya](/glossary/anguttara-nikaya/) (AN 9.64)"')
    a = ap.parse_args()
    {"status": cmd_status, "verify": cmd_verify, "format": cmd_format, "link": cmd_link}[a.cmd](a)


if __name__ == "__main__":
    main()
