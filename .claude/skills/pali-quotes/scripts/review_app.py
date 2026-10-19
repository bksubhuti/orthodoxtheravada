#!/usr/bin/env python3
"""Review app for the content-check changes (terms first, then lists).

Run from the repo root:   python3 .claude/skills/pali-quotes/scripts/review_app.py
Then open http://127.0.0.1:8765 (it opens by itself).

Each page that changed since the baseline commit is shown as the real site page (from a local
`jekyll serve`, started here if it is not already running) with a review bar above it.
The baseline (the commit before the content changes) and the renames are kept in
.claude/quote-review/baseline.json, so the work can be committed and pushed and still be reviewed here.
  Approve      -> git add the page if it has changes since the last commit
  Needs work   -> saved with your note, nothing staged
  Reject       -> saved, nothing staged or restored
Decisions are kept in .claude/quote-review/review-decisions.json, so you can stop and resume.
Only the standard library is used.
"""
import atexit, html, json, os, re, socket, subprocess, sys, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

# This file lives in .claude/skills/pali-quotes/scripts/ (a dot-folder, so Jekyll never publishes it).
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
REVIEW = os.path.join(ROOT, ".claude", "quote-review")
DECISIONS = os.path.join(REVIEW, "review-decisions.json")
BASELINE = os.path.join(REVIEW, "baseline.json")
JEKYLL_LOG = os.path.join(REVIEW, "jekyll.log")
PORT = 8765
JEKYLL_PORT = 4000
JEKYLL = f"http://127.0.0.1:{JEKYLL_PORT}"
URL_PREFIX = {"_terms": "/glossary/", "_lists": "/lists/"}


def git(*args, text=True):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=text).stdout


def changed_pages():
    """[(path, old_path, kind)] for _terms then _lists; kind is M, R (renamed) or D."""
    # Renames come from baseline.json (saved from the git mv staging), since git cannot detect
    # a rename once the page was rewritten.
    renamed = BASE_INFO["renames"]
    old_names = set(renamed.values())
    out = []
    for line in git("diff", BASE_INFO["base"], "--name-status", "-M", "--", "_terms", "_lists").splitlines():
        parts = line.split("\t")
        st, path = parts[0][0], parts[-1]
        if path in renamed:
            out.append((path, renamed[path], "R"))
        elif st == "D" and path in old_names:
            continue
        elif st in "MD":
            out.append((path, path, st))
        elif st == "A":
            out.append((path, None, "A"))
    key = lambda p: (0 if p[0].startswith("_terms/") else 1, p[0])
    return sorted(out, key=key)


def load(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def jekyll_up():
    try:
        socket.create_connection(("127.0.0.1", JEKYLL_PORT), timeout=0.3).close()
        return True
    except OSError:
        return False


def start_jekyll():
    if jekyll_up():
        print(f"Using the Jekyll server already running at {JEKYLL}")
        return
    print(f"Starting Jekyll at {JEKYLL} (log: {JEKYLL_LOG}); the first build takes a while.")
    env = dict(os.environ, JEKYLL_NO_BUNDLER_REQUIRE="1")
    proc = subprocess.Popen(
        ["bundle", "exec", "jekyll", "serve", "--config", "_config.yml,_config_local.yml",
         "--future", "--livereload", "--host", "127.0.0.1", "--port", str(JEKYLL_PORT)],
        cwd=ROOT, env=env, stdout=open(JEKYLL_LOG, "w"), stderr=subprocess.STDOUT)
    atexit.register(proc.terminate)


CSS = """
:root{--bg:#fbfaf7;--fg:#222;--mut:#777;--line:#e4e0d8;--acc:#7a5c1e;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1c1b19;--fg:#e8e6e1;--mut:#9a968e;--line:#3a3833;--acc:#d9b26a;--card:#262522}}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,system-ui,sans-serif;display:flex;flex-direction:column}
header{background:var(--card);border-bottom:1px solid var(--line);padding:8px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
header b{font-size:16px} .mut{color:var(--mut)} a{color:var(--acc)}
main{padding:16px;max-width:1400px;margin:auto;width:100%;box-sizing:border-box;overflow:auto}
.bar{height:6px;background:var(--line);border-radius:3px;flex:1;min-width:80px}.bar i{display:block;height:100%;background:var(--acc);border-radius:3px}
button{font:inherit;padding:6px 14px;border-radius:6px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer}
button.ok{background:#2e7d32;color:#fff;border-color:#2e7d32} button.warn{background:#b26a00;color:#fff;border-color:#b26a00} button.no{background:#b23b2e;color:#fff;border-color:#b23b2e}
form{display:flex;gap:8px;align-items:center;flex:1 1 520px;flex-wrap:wrap}
input[type=text]{flex:1;min-width:160px;font:inherit;background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:5px 8px}
iframe{flex:1;border:0;width:100%;background:#fff}
pre{white-space:pre-wrap;word-wrap:break-word;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px}
.tag{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;border:1px solid var(--line)}
.approved{background:#2e7d32;color:#fff}.needs{background:#b26a00;color:#fff}.rejected{background:#b23b2e;color:#fff}
ul.list{columns:3 260px;font-size:13px;padding-left:18px} ul.list li{break-inside:avoid}
"""


def page_list(pages, dec):
    done = sum(1 for p, *_ in pages if p in dec)
    items = []
    for i, (p, old, kind) in enumerate(pages):
        d = dec.get(p, {}).get("decision", "")
        tag = f' <span class="tag {d}">{d}</span>' if d else ""
        items.append(f'<li><a href="/page?i={i}">{html.escape(p)}</a>{" (" + kind + ")" if kind != "M" else ""}{tag}</li>')
    nxt = next((i for i, (p, *_) in enumerate(pages) if p not in dec), None)
    go = f'<a href="/page?i={nxt}"><button class="ok">Continue with the next unreviewed page →</button></a>' if nxt is not None else "<b>All pages reviewed.</b>"
    counts = {}
    for v in dec.values():
        counts[v.get("decision")] = counts.get(v.get("decision"), 0) + 1
    summ = " · ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    jk = "" if jekyll_up() else f"<p class='mut'>Jekyll is not answering at {JEKYLL} yet (still building?). See {html.escape(JEKYLL_LOG)}.</p>"
    return (f"<header><b>Content review</b><span>{done} / {len(pages)} reviewed</span>"
            f'<div class="bar"><i style="width:{100 * done / max(1, len(pages)):.1f}%"></i></div><span class="mut">{summ}</span></header>'
            f"<main>{jk}<p>{go}</p><p class='mut'>Order: terms, then lists. Keys on a page (click the bar first if the page has focus): "
            f"<b>a</b> approve · <b>n</b> needs work · <b>r</b> reject · <b>j</b>/<b>k</b> next/previous.</p><ul class='list'>{''.join(items)}</ul></main>")


def page_view(pages, i, dec):
    p, old, kind = pages[i]
    folder, fname = p.split("/", 1)
    d = dec.get(p, {})
    done = sum(1 for q, *_ in pages if q in dec)
    if kind == "D":
        old_text = git("show", f"{BASE_INFO['base']}:{old}")
        title = re.search(r'^title:\s*"?(.*?)"?\s*$', old_text, re.M)
        title = title.group(1) if title else fname[:-3]
        body = (f"<main><p><b>This page was deleted.</b> Approve to accept the deletion. Its text before:</p>"
                f"<pre>{html.escape(old_text)}</pre></main>")
        refresh = ""
    else:
        text = open(os.path.join(ROOT, p), encoding="utf-8").read()
        title = re.search(r'^title:\s*"?(.*?)"?\s*$', text, re.M)
        title = title.group(1) if title else fname[:-3]
        url = f"{JEKYLL}{URL_PREFIX[folder]}{fname[:-3]}/"
        if jekyll_up():
            body, refresh = f'<iframe src="{html.escape(url)}"></iframe>', ""
        else:
            body = f"<main><p>Jekyll is still building the site; this page reloads by itself. Log: {html.escape(JEKYLL_LOG)}</p></main>"
            refresh = '<meta http-equiv="refresh" content="5">'
    renamed = f' <span class="mut">(renamed from {html.escape(os.path.basename(old))})</span>' if kind == "R" else ""
    status = f'<span class="tag {d.get("decision", "")}">{d.get("decision", "not reviewed")}</span>'
    note = html.escape(d.get("note", ""))
    prev_l = f'<a href="/page?i={i - 1}" id="prev">← prev</a>' if i > 0 else ""
    next_l = f'<a href="/page?i={i + 1}" id="next">next →</a>' if i + 1 < len(pages) else ""
    return f"""{refresh}<header><a href="/">☰</a><b>{html.escape(title)}</b>{renamed}{status}
<span class="mut">{i + 1} / {len(pages)}</span>
<div class="bar"><i style="width:{100 * done / max(1, len(pages)):.1f}%"></i></div>{prev_l} {next_l}
<form method="post" action="/decide" id="f">
<input type="hidden" name="i" value="{i}">
<input type="text" name="note" value="{note}" placeholder="Note (for Needs work / Reject)">
<button class="ok" name="decision" value="approved">Approve (a)</button>
<button class="warn" name="decision" value="needs">Needs work (n)</button>
<button class="no" name="decision" value="rejected">Reject (r)</button>
</form></header>
{body}
<script>
document.addEventListener('keydown',e=>{{if(e.target.tagName==='INPUT')return;
const f=document.getElementById('f'),b=v=>f.querySelector('button[value='+v+']').click();
if(e.key==='a')b('approved');if(e.key==='n')b('needs');if(e.key==='r')b('rejected');
if(e.key==='j'){{const n=document.getElementById('next');n&&n.click()}}
if(e.key==='k'){{const n=document.getElementById('prev');n&&n.click()}}}});
</script>"""


class H(BaseHTTPRequestHandler):
    def send(self, body, code=200):
        b = f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Content review</title><style>{CSS}</style>{body}".encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):
        pass

    def do_GET(self):
        u = urlparse(self.path)
        pages, dec = changed_pages(), load(DECISIONS)
        if u.path == "/page":
            i = int(parse_qs(u.query).get("i", ["0"])[0])
            if 0 <= i < len(pages):
                return self.send(page_view(pages, i, dec))
        self.send(page_list(pages, dec))

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(n).decode())
        i = int(form["i"][0])
        decision = form.get("decision", [""])[0]
        pages, dec = changed_pages(), load(DECISIONS)
        p, old, kind = pages[i]
        if decision == "approved":
            if kind != "D":
                git("add", "--", p)
            if old and old != p:
                git("add", "-A", "--", old)
        dec[p] = {"decision": decision, "note": form.get("note", [""])[0].strip()}
        json.dump(dec, open(DECISIONS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        nxt = next((j for j in range(i + 1, len(pages)) if pages[j][0] not in dec), None)
        if nxt is None:
            nxt = next((j for j in range(len(pages)) if pages[j][0] not in dec), None)
        self.send_response(303)
        self.send_header("Location", f"/page?i={nxt}" if nxt is not None else "/")
        self.end_headers()


def main():
    global BASE_INFO
    BASE_INFO = load(BASELINE)
    if not BASE_INFO.get("base"):
        sys.exit(f"Missing {BASELINE} (needs a 'base' commit and a 'renames' map).")
    BASE_INFO.setdefault("renames", {})
    start_jekyll()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = f"http://127.0.0.1:{PORT}/"
    print(f"Review app running at {url}  (Ctrl+C to stop)")
    if "--no-open" not in sys.argv:
        threading.Timer(0.5, webbrowser.open, [url]).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


BASE_INFO = {}
if __name__ == "__main__":
    main()
