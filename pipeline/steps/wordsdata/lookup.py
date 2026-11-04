# Word-by-word data for every code line: curated W blocks (words*.py) first, then wordsdata/dN.py.
import re, sys, html, runpy, importlib
for p in ['/home/claude/day1', '/home/claude/day2', '/home/claude/day3', '/home/claude/day4']:
    if p not in sys.path: sys.path.insert(0, p)
norm = lambda t: re.sub(r'\s+', ' ', t).strip()
_cur, _gen = {}, {}

def _load():
    if _gen: return
    for d, mod in [(1, 'words'), (2, 'words2'), (3, 'words3'), (4, 'words4')]:
        m = importlib.import_module(mod); dd = _cur.setdefault(d, {})
        for v in vars(m).values():
            if isinstance(v, list) and v and all(isinstance(x, str) and 'class="wline"' in x for x in v):
                for blk in v:
                    mm = re.match(r'<div class="wline"><div class="wcode"><span class="ltr">(.*?)</span></div>(.*)</div>$', blk, re.S)
                    if mm: dd.setdefault(norm(html.unescape(mm.group(1))), mm.group(2))
        L = runpy.run_path(f'/home/claude/steps/wordsdata/d{d}.py')['L']
        g = _gen.setdefault(d, {})
        for t, (chips, note) in L.items():
            c = ''.join(f'<div class="chip"><div class="tok"><span class="ltr">{html.escape(a)}</span></div><div class="mean">{b}</div></div>' for a, b in chips)
            g[norm(t)] = f'<div class="chips">{c}</div>' + (f'<div class="wnote">{note}</div>' if note else '')

def get(text, day):
    _load(); t = norm(text)
    if not t: return None
    order = [day] + [d for d in (1, 2, 3, 4) if d != day]
    for src in (_cur, _gen):
        for d in order:
            if t in src.get(d, {}): return src[d][t]
    return None
