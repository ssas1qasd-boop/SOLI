import os
# Visual-Studio-style line numbers for every code block in the lecture files.
import re, html as H

CSS = '''
.ln { display:inline-block; min-width:6.5mm; padding-left:1mm; margin-right:2.5mm; text-align:right; color:#7c8594; font-style:normal; font-weight:normal;
      border-right:1px solid #3a4152; user-select:none; -webkit-user-select:none; }
.cl td.k .ln { color:#8b93a1; }
.wline .wcode .ln, .fcode .ln { border-right-color:#c9d1de; color:#6b7280; }
'''

def num(n):
    return f'<i class="ln">{n}</i>'

def _programs(doc):
    """[(pos, {stripped_line: [numbers]})] for every program table marker in the document."""
    progs = []
    for m in re.finditer(r'<!--PROG:(.*?)-->', doc):
        path = m.group(1)
        d = {}
        for i, l in enumerate(open(path), 1):
            s = l.strip()
            if s: d.setdefault(s, []).append(i)
        progs.append((m.start(), d))
    return progs

def _lecture_bounds(doc):
    return [m.start() for m in re.finditer(r'<section class="(lec|final|quick|selftest|answers)', doc)] + [len(doc)]

def _lookup(text, pos, progs, bounds, seq=None):
    s = text.strip()
    if not s:
        return None
    lo = max([b for b in bounds if b <= pos], default=0)
    hi = min([b for b in bounds if b > pos], default=len(bounds))
    before = [p for p in progs if lo <= p[0] < pos][::-1]
    after = [p for p in progs if pos < p[0] < hi]
    for _, d in before + after:
        if s in d and len(d[s]) == 1:
            return d[s][0]
        if s in d:
            if seq is not None:   # n-th time we meet this text -> n-th occurrence in the program
                key = (id(d), s); k = seq.get(key, 0); seq[key] = k + 1
                return d[s][k] if k < len(d[s]) else None
            return None   # appears several times in that program: ambiguous
    return None

def apply(doc, ext=''):
    progs = _programs(doc)
    bounds = _lecture_bounds(doc)
    out, last = [], 0
    # "why" blocks: <div class="whycode"><div>line</div>...</div>
    def fix_why(m):
        inner = m.group(1)
        lines = re.findall(r'<div>(.*?)</div>', inner)
        nums = [_lookup(H.unescape(re.sub(r'<[^>]+>', '', t)), m.start(), progs, bounds) for t in lines]
        real = [n for n, t in zip(nums, lines) if t.strip()]
        ok = real and all(n is not None for n in real) and all(a < b for a, b in zip(real, real[1:]))
        if not ok:
            return m.group(0)   # schematic excerpt: no trustworthy line numbers
        return '<div class="whycode">' + ''.join(f'<div>{num(n)}{t}</div>' for n, t in zip(nums, lines)) + '</div>'
    doc = re.sub(r'<div class="whycode">((?:<div>.*?</div>)*)</div>', fix_why, doc, flags=re.S)
    # word-by-word lines
    state = {'d': None, 'n': 0, 'lec': -1}
    def fix_word(m):
        text = H.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
        pos = m.start()
        lec = max([x for x in bounds if x <= pos], default=0)
        if lec != state['lec']:
            state.update(d=None, n=0, lec=lec)
        n = None
        d = state['d']
        if d is not None and text in d:
            later = [x for x in d[text] if x > state['n']]
            if later: n = later[0]
        if n is None and text not in ('{', '}', '};'):
            lo = lec; hi = min([x for x in bounds if x > pos], default=len(doc))
            for p, dd in [p for p in progs if lo <= p[0] < pos][::-1] + [p for p in progs if pos < p[0] < hi]:
                if text in dd:
                    later = [x for x in dd[text] if dd is not d or x > state['n']] or dd[text]
                    n = later[0]; d = dd; break
        if n is not None:
            state.update(d=d, n=n)
        return f'<div class="wcode">{num(n) if n else ""}<span class="ltr">{m.group(1)}</span></div>'
    doc = re.sub(r'<div class="wcode"><span class="ltr">(.*?)</span></div>', fix_word, doc, flags=re.S)
    doc = links(doc, ext)
    return re.sub(r'<!--PROG:.*?-->', '', doc)

# ---------------------------------------------------------------- jump links: code line -> its word-by-word breakdown
CSS += '''
.wl-go { display:inline-block; text-decoration:none; font-size:8pt; line-height:1; padding:0.6mm 1.6mm; margin:0 1mm; border-radius:2mm;
         background:#e0e7ff; color:#3730a3 !important; border:1px solid #a5b4fc; vertical-align:middle; white-space:nowrap; font-family:"CairoAr","Cairo",sans-serif; }
.wl-go:hover { background:#c7d2fe; }
.wcode .wl-go, .whycode .wl-go { background:#312e81; color:#e0e7ff !important; border-color:#4f46e5; }
.wl-backs { font-size:8.5pt; color:#4338ca; margin:0 0 1mm; line-height:1.9; }
.wl-src { display:inline-block; text-decoration:none; color:#fff !important; background:#4338ca; border-radius:2mm; padding:0.3mm 1.8mm; margin:0 0.8mm; white-space:nowrap; }
.wl-prev { float:left; font-size:8.5pt; text-decoration:none; color:#fff !important; background:#4338ca; border-radius:2mm; padding:0.4mm 1.8mm; margin:0.3mm 1mm 0 0; }
.wl-back { float:left; font-size:8.5pt; text-decoration:none; color:#4338ca; margin:0.5mm 1mm 0 0; }
[id^=sl-]:target, .wline:target, tr:target td { outline:2px solid #6366f1; outline-offset:1px; }
'''

def _norm(t):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', t))).strip()

def links(doc, ext=''):
    """Each program-table row gets a 🔍 to the word-by-word block of that same line, which sits right under
    the step where the line is written (render.py makes it, with back links to the step line and to this row)."""
    import steps_hook as STH, render as R
    idx = {}
    for prog in STH._reg.values():
        for f, path in prog.files.items():
            idx[os.path.abspath(path)] = (prog.pid, f)
    have = set(re.findall(r'id="sw-([^"]+)"', doc))
    def fix_table(m):
        path, table = m.group(1), m.group(2)
        if path not in idx: return m.group(0)
        pid, f = idx[path]
        def fix_row(r):
            cls, code, expl = r.group(1), r.group(2), r.group(3)
            nm = re.match(r'<i class="ln">(\d+)</i>', code)
            if not nm: return r.group(0)
            a = R.anchor(pid, f, int(nm.group(1)))
            if a not in have: return r.group(0)
            expl = expl.replace(' <span style="color:#2563eb">(شرحه كلمة كلمة فوق)</span>', '')
            return f'<tr{cls} id="tr-{a}"><td class="k">{code}</td><td class="e">{expl} <a class="wl-go" href="#sw-{a}">🔍 كلمة كلمة</a></td></tr>'
        table = re.sub(r'<tr((?: class="[^"]*")?)><td class="k">(.*?)</td><td class="e">(.*?)</td></tr>', fix_row, table, flags=re.S)
        return m.group(0)[:m.start(2) - m.start(0)] + table
    return re.sub(r'<!--PROG:(.*?)-->(.*?</table>)', fix_table, doc, flags=re.S)
