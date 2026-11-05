#!/usr/bin/env python3
"""Automatic code maps for every bench program: one HTML page per day (+ an index).
Blocks come from the program's own structure (includes, types, functions, main's paragraphs, loops);
every source line belongs to a block; bench step numbers come from the real run (out_days/data_dayN.json)."""
import json, re, html, os, sys

E = html.escape
DAYN = {1: 'اليوم 1', 2: 'اليوم 2', 3: 'اليوم 3', 4: 'اليوم 4', 5: 'اليوم 5', 6: 'اليوم 6', 7: 'اليوم 7', 8: 'الأسبوع 3 · اليوم 1', 9: 'الأسبوع 3 · اليوم 2', 10: 'الأسبوع 3 · اليوم 3', 11: 'الأسبوع 3 · اليوم 4', 12: 'الأسبوع 3 · اليوم 5', 13: 'الأسبوع 3 · اليوم 6', 14: 'الأسبوع 3 · اليوم 7'}
DATA = '/home/claude/bench2/out_days/data_day%d.json'
OUT = '/home/claude/maps/out'

# ---------------------------------------------------------------- syntax colours
KW = set('if else while for do return const static struct class public private protected void unsigned signed int float double char bool auto new delete '
         'nullptr true false sizeof using namespace include break continue switch case default template typename virtual override mutable extern inline '
         'long short enum this operator friend explicit constexpr'.split())
PYKW = set('def class return if elif else for while in import from as with try except finally raise pass break continue lambda and or not is None True False print len range'.split())
TY = set('GLFWwindow GLuint GLint GLenum GLchar GLsizei GLfloat std string vector size_t uint8_t uint32_t'.split())
TOK_C = re.compile(r'(?P<c>//.*|/\*.*?\*/)|(?P<s>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])\')|(?P<p>^\s*#\s*\w+)|(?P<n>\b\d+\.?\d*[fuUlL]?\b)|(?P<g>\bGL_[A-Z0-9_]+\b|\bGLFW_[A-Z0-9_]+\b)|(?P<w>[A-Za-z_]\w*)(?P<call>\s*\()?')
TOK_P = re.compile(r'(?P<c>#.*)|(?P<s>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(?P<p>$^)|(?P<n>\b\d+\.?\d*\b)|(?P<g>$^)|(?P<w>[A-Za-z_]\w*)(?P<call>\s*\()?')

def hl(line, py, vars_):
    tok = TOK_P if py else TOK_C
    out, pos = [], 0
    for m in tok.finditer(line):
        if m.start() == m.end():
            continue
        out.append(E(line[pos:m.start()])); pos = m.end(); k = m.lastgroup
        if m.group('w'):
            w = m.group('w'); call = m.group('call') or ''
            kw = PYKW if py else KW
            cls = 'sk' if w in kw else 'st' if w in TY else 'sf' if call else 'sv' if w in vars_ else None
            out.append((f'<span class="{cls}">{E(w)}</span>' if cls else E(w)) + E(call)); continue
        cls = {'c': 'sc', 's': 'ss', 'p': 'sp', 'n': 'sn', 'g': 'sg'}[k]
        out.append(f'<span class="{cls}">{E(m.group(0))}</span>')
    out.append(E(line[pos:])); return ''.join(out)

# ---------------------------------------------------------------- C/C++ structure
def strip_c(line, state):
    """remove strings, chars and comments; state['blk'] tracks /* */"""
    out, i, n = [], 0, len(line)
    while i < n:
        if state['blk']:
            j = line.find('*/', i)
            if j < 0: return ''.join(out)
            state['blk'] = False; i = j + 2; continue
        c = line[i]
        if line.startswith('//', i): break
        if line.startswith('/*', i): state['blk'] = True; i += 2; continue
        if c in '"\'':
            q = c; i += 1
            while i < n and line[i] != q:
                i += 2 if line[i] == '\\' else 1
            i += 1; out.append('""'); continue
        out.append(c); i += 1
    return ''.join(out)

def is_comment(t, py):
    s = t.strip()
    return s.startswith('#') if py else (s.startswith('//') or s.startswith('/*') or s.startswith('*'))

def comment_text(t):
    return re.sub(r'^\s*(//+|/\*+|\*+|#+)\s*', '', t).rstrip('*/ ').strip()

def code_lines(lines, a, b, py):
    return [lines[i - 1].strip() for i in range(a, b + 1) if lines[i - 1].strip() and not is_comment(lines[i - 1], py) and lines[i - 1].strip() not in ('{', '}', '};')]

def parse_c(lines):
    """returns list of top-level items: dict(kind, a, b, name, body=(a,b) for functions)"""
    st = {'blk': False}; depth = 0; items = []; cur = None; pend = []  # pend: lines of a statement not yet closed at depth 0
    clean = [strip_c(l, st) for l in lines]
    n = len(lines); i = 0
    while i < n:
        c = clean[i]; s = c.strip()
        if depth == 0:
            if not s:
                if not pend: items.append({'kind': 'blank', 'a': i + 1, 'b': i + 1})
                i += 1; continue
            if s.startswith('#'):
                items.append({'kind': 'pp', 'a': i + 1, 'b': i + 1}); i += 1; continue
            pend.append(i)
            opens = c.count('{'); closes = c.count('}')
            if opens > closes:
                head = ' '.join(clean[k].strip() for k in pend)
                a = pend[0] + 1; pend = []
                # find the matching close
                d = opens - closes; j = i
                while d > 0 and j + 1 < n:
                    j += 1; d += clean[j].count('{') - clean[j].count('}')
                b = j + 1
                m = re.match(r'\s*(?:template\s*<[^>]*>\s*)?(struct|class|union|enum(?:\s+class)?|namespace)\s+([A-Za-z_]\w*)?', head)
                if m:
                    items.append({'kind': 'type' if m.group(1) != 'namespace' else 'ns', 'a': a, 'b': b, 'name': (m.group(1) + ' ' + (m.group(2) or '')).strip()})
                elif '(' in head:
                    nm = re.search(r'((?:[A-Za-z_]\w*::)*(?:operator\s*\S+?|~?[A-Za-z_]\w*))\s*\(', head)
                    name = nm.group(1) if nm else 'function'
                    # body starts at the line with the first '{'
                    bstart = next(k for k in range(a - 1, b) if '{' in clean[k]) + 1
                    items.append({'kind': 'fn', 'a': a, 'b': b, 'name': name, 'body': (bstart, b)})
                else:
                    items.append({'kind': 'glob', 'a': a, 'b': b})
                i = j + 1; continue
            if s.endswith(';') or s.endswith('}') or s.endswith('};'):
                items.append({'kind': 'glob', 'a': pend[0] + 1, 'b': i + 1}); pend = []
            i += 1; continue
        i += 1
    if pend: items.append({'kind': 'glob', 'a': pend[0] + 1, 'b': pend[-1] + 1})
    return items, clean

def split_body(lines, clean, a, b, py, depth_base):
    """split the inside of a function/loop (lines a..b, exclusive of header/closing) into paragraphs and loops.
    returns list of dict(kind='sec'|'loop', a, b, head, children)"""
    out = []; i = a; cur = None
    def flush():
        nonlocal cur
        if cur: out.append(cur); cur = None
    while i <= b:
        raw = lines[i - 1]; s = raw.strip()
        if not s:
            if cur: cur['b'] = i; cur['gap'] = True
            i += 1; continue
        if cur and cur.get('gap') and not is_comment(raw, py) is False:
            pass
        # loops start a container
        lm = re.match(r'(while|for|do)\b', s) if not py else re.match(r'(while|for)\b', s)
        if lm:
            if py:
                ind = len(raw) - len(raw.lstrip()); j = i
                while j + 1 <= b and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > ind):
                    j += 1
                while j > i and not lines[j - 1].strip(): j -= 1
                inner = split_body(lines, clean, i + 1, j, py, depth_base + 1)
            else:
                d = 0; j = i - 1; started = False
                while j < b:
                    d += clean[j].count('{') - clean[j].count('}')
                    if clean[j].count('{'): started = True
                    if started and d <= 0: break
                    if not started and clean[j].strip().endswith(';') and j > i - 1: break
                    j += 1
                j += 1
                if not started:  # one-line loop body
                    flush(); cur = {'kind': 'sec', 'a': i, 'b': j}; i = j + 1; continue
                first_open = next(k for k in range(i - 1, j) if '{' in clean[k]) + 1
                inner = split_body(lines, clean, first_open + 1, j - 1, py, depth_base + 1)
            flush(); out.append({'kind': 'loop', 'a': i, 'b': j, 'head': s, 'children': inner}); i = j + 1; continue
        # new paragraph after a blank line, or a comment that follows code
        if cur is None or cur.get('gap') or (is_comment(raw, py) and cur.get('code')):
            flush(); cur = {'kind': 'sec', 'a': i, 'b': i}
        # extend through nested braces (if/else blocks stay in one section)
        if not py:
            d = clean[i - 1].count('{') - clean[i - 1].count('}'); j = i
            while d > 0 and j < b:
                j += 1; d += clean[j - 1].count('{') - clean[j - 1].count('}')
            cur['b'] = j
            if not is_comment(raw, py): cur['code'] = True
            i = j + 1
        else:
            ind = len(raw) - len(raw.lstrip()); j = i
            if s.endswith(':'):
                while j + 1 <= b and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > ind):
                    j += 1
                while j > i and not lines[j - 1].strip(): j -= 1
            cur['b'] = j
            if not is_comment(raw, py): cur['code'] = True
            i = j + 1
    flush()
    # merge sections with < 2 code lines into the previous section
    merged = []
    for x in out:
        if x['kind'] == 'sec' and merged and merged[-1]['kind'] == 'sec' and len(code_lines(lines, x['a'], x['b'], py)) < 2 and len(code_lines(lines, merged[-1]['a'], merged[-1]['b'], py)) < 6:
            merged[-1]['b'] = x['b']; continue
        merged.append(x)
    if len(merged) > 1 and merged[0]['kind'] == 'sec' and len(code_lines(lines, merged[0]['a'], merged[0]['b'], py)) < 2 and merged[1]['kind'] == 'sec':
        merged[1]['a'] = merged[0]['a']; merged.pop(0)
    return merged

def chunk(lines, secs, py):
    """split long paragraphs (more than 6 code lines) where the kind of code changes, or every 5 lines"""
    out = []
    for x in secs:
        if x['kind'] == 'loop':
            x['children'] = chunk(lines, x['children'], py); out.append(x); continue
        cl = [i for i in range(x['a'], x['b'] + 1) if lines[i - 1].strip() and not is_comment(lines[i - 1], py) and lines[i - 1].strip() not in ('{', '}', '};')]
        if len(cl) <= 6: out.append(x); continue
        cur = {'kind': 'sec', 'a': x['a'], 'b': x['a']}; n = 0; c0 = None; depth = 0; complete = True
        for i in range(x['a'], x['b'] + 1):
            t = lines[i - 1]
            if i in cl and i > x['a']:
                pv = [k for k in cl if k < i]
                if pv:
                    pt = re.sub(r'//.*$', '', lines[pv[-1] - 1]).strip()
                    complete = (pt.endswith((';', '{', '}')) if not py else not pt.endswith((',', '(', '[', '\\', ':')))
            if i in cl:
                c = cat(t) or 'x'
                ok = complete and depth == 0
                if ok and (n >= 5 or (n >= 2 and c != c0 and c0 is not None)):
                    out.append(cur); cur = {'kind': 'sec', 'a': i, 'b': i}; n = 0
                n += 1; c0 = c
            if i in cl:
                ct = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', t)
                ct = re.sub(r'#.*$' if py else r'//.*$', '', ct)
                depth += ct.count('(') + ct.count('[') + ct.count('{') - ct.count(')') - ct.count(']') - ct.count('}')
                if depth < 0: depth = 0
            cur['b'] = i
        out.append(cur)
    return out

# ---------------------------------------------------------------- Python structure
def parse_py(lines):
    items = []; n = len(lines); i = 0
    while i < n:
        raw = lines[i]; s = raw.strip()
        if not s: items.append({'kind': 'blank', 'a': i + 1, 'b': i + 1}); i += 1; continue
        if raw[0] in ' \t':
            items.append({'kind': 'stmt', 'a': i + 1, 'b': i + 1}); i += 1; continue
        m = re.match(r'(def|class)\s+([A-Za-z_]\w*)', s)
        j = i
        if s.endswith(':') or m:
            while j + 1 < n and (not lines[j + 1].strip() or lines[j + 1][0] in ' \t'):
                j += 1
            while j > i and not lines[j].strip(): j -= 1
        if m:
            items.append({'kind': 'fn' if m.group(1) == 'def' else 'type', 'a': i + 1, 'b': j + 1, 'name': m.group(2) if m.group(1) == 'def' else 'class ' + m.group(2), 'body': (i + 2, j + 1)})
        elif re.match(r'(import|from)\b', s):
            items.append({'kind': 'pp', 'a': i + 1, 'b': j + 1})
        else:
            items.append({'kind': 'stmt', 'a': i + 1, 'b': j + 1})
        i = j + 1
    return items

# ---------------------------------------------------------------- Arabic labels for common code
CATS = [
    (r'glfwInit|glfwWindowHint|glfwCreateWindow|glfwMakeContextCurrent|glfwSwapInterval', 'الشباك والـ Context'),
    (r'gladLoadGL|glewInit', 'تحميل دوال الكارت'),
    (r'glGenVertexArrays|glBindVertexArray\(\s*[a-zA-Z]', 'VAO: وصف الأركان'),
    (r'glVertexAttribPointer|glEnableVertexAttribArray', 'وصف شكل الركن'),
    (r'glGenBuffers|glBufferData|glBufferSubData', 'صناديق على الكارت'),
    (r'glGenTextures|glTexImage2D|glTexParameter|stbi_load', 'الصورة (Texture)'),
    (r'CreateShader\(|glUseProgram|ParseShader|Shader\s+\w+\(', 'الـ Shader'),
    (r'glGetUniformLocation|glUniform', 'الـ Uniforms'),
    (r'glClear|glDraw|glfwSwapBuffers|glfwPollEvents', 'الرسم'),
    (r'glfwSet\w+Callback', 'ربط الماوس والكيبورد'),
    (r'glDelete|glfwTerminate', 'التنضيف'),
    (r'std::string\s+\w+\s*=|R"\(', 'نص الـ Shader'),
    (r'np\.cross|np\.dot|np\.linalg', 'حسابات NumPy'),
    (r'np\.array|np\.zeros|np\.ones', 'مصفوفات NumPy'),
    (r'^\s*(float|double|int|unsigned)\s+\w+\[', 'مصفوفة في الرام'),
    (r'\bnew\b|malloc|memset|delete\b|free\(', 'حجز ومسح ذاكرة'),
    (r'push_back|emplace_back|erase\(|std::vector', 'vector'),
    (r'std::cout|printf\(|print\(', 'طباعة'),
]
def cat(text):
    for rx, ar in CATS:
        if re.search(rx, text): return ar
    return ''

# ---------------------------------------------------------------- one program
def build_program(p, day):
    pid = p['id']; files = p['files']; steps = p['steps']
    py_of = lambda f: files[f]['name'].endswith('.py')
    LS = {}  # (f, ln) -> [step numbers]
    for k, s in enumerate(steps, 1):
        LS.setdefault((s.get('f', 0), s['ln']), []).append(k)
    SINFO = {k: s for k, s in enumerate(steps, 1)}
    blocks = []  # dict(id, f, ranges[(a,b)], title, preview[], ar, col, kind, steps[], calls[], depth)
    flow = []    # ordered list of flow items (block or loop group)
    fnames = {}
    def mk(f, a, b, title, kind, col, extra_ranges=()):
        lines = files[f]['lines']; py = py_of(f)
        rng = [(a, b)] + list(extra_ranges)
        ks = sorted({k for (ff, ln), v in LS.items() if ff == f and any(x <= ln <= y for x, y in rng) for k in v})
        txt = '\n'.join(lines[a - 1:b])
        ar = cat(txt)
        if not ar and ks: ar = SINFO[ks[0]].get('ti') or ''
        cls_ = code_lines(lines, a, b, py)
        prev = [l for l in cls_ if l != title.strip()][:2] if cls_ and cls_[0] == title.strip() else cls_[:2]
        bid = f'b{len(blocks)}'
        blk = {'id': bid, 'f': f, 'ranges': rng, 'title': title, 'preview': prev, 'ar': ar, 'col': col, 'kind': kind, 'steps': ks, 'calls': [], 'txt': txt}
        blocks.append(blk); return blk
    tops = []
    for f, fl in enumerate(files):
        lines = fl['lines']; py = py_of(f)
        if fl['name'].endswith('.shader'):
            # split shader files at "#shader" markers
            starts = [i + 1 for i, l in enumerate(lines) if l.strip().startswith('#shader')] or [1]
            for j, a in enumerate(starts):
                b = (starts[j + 1] - 1) if j + 1 < len(starts) else len(lines)
                if j == 0 and a > 1: a = 1
                tops.append((f, {'kind': 'shader', 'a': a, 'b': b, 'name': lines[starts[j] - 1].strip() if lines else fl['name']}))
            continue
        items = parse_py(lines) if py else parse_c(lines)[0]
        for it in items: tops.append((f, it))
    # group top-level items: preprocessor/imports block, globals, types, functions
    main = None
    side_groups = []
    for f, fl in enumerate(files):
        py = py_of(f); lines = fl['lines']
        its = [it for ff, it in tops if ff == f]
        # absorb blanks into the previous item
        merged = []
        for it in its:
            if it['kind'] == 'blank':
                if merged: merged[-1]['b'] = it['b']
                else: merged.append({'kind': 'pp' if not py else 'stmt', 'a': it['a'], 'b': it['b']})
                continue
            if merged and it['kind'] in ('pp',) and merged[-1]['kind'] == 'pp': merged[-1]['b'] = it['b']; continue
            if merged and it['kind'] == 'glob' and merged[-1]['kind'] == 'glob': merged[-1]['b'] = it['b']; continue
            merged.append(dict(it))
        for it in merged:
            if it['kind'] == 'fn' and re.search(r'(^|::)main$', it['name']) and not py:
                main = (f, it); continue
            side_groups.append((f, it))
    # python without def main: the top-level statements are the flow
    flow_src = None
    if main:
        f, it = main; lines = files[f]['lines']; _, clean = parse_c(lines)
        ba, bb = it['body']
        secs = chunk(lines, split_body(lines, clean, ba + 1, bb - 1, False, 1), False)
        flow_src = (f, secs, (it['a'], ba), (bb, bb), it['name'] + '()')
    else:
        pf = next((f for f in range(len(files)) if py_of(f)), None)
        if pf is not None:
            lines = files[pf]['lines']
            stm = [it for ff, it in side_groups if ff == pf and it['kind'] == 'stmt']
            side_groups = [(ff, it) for ff, it in side_groups if not (ff == pf and it['kind'] == 'stmt')]
            # runs of top-level statements (separated only by blank lines) -> paragraphs and loops
            runs = []
            for it in sorted(stm, key=lambda x: x['a']):
                if runs and all(not lines[k - 1].strip() for k in range(runs[-1][1] + 1, it['a'])): runs[-1][1] = it['b']
                else: runs.append([it['a'], it['b']])
            m2 = []
            for a, b in runs: m2 += split_body(lines, None, a, b, True, 0)
            m2 = chunk(lines, m2, True)
            flow_src = (pf, m2, None, None, files[pf]['name'])
    # side blocks
    for f, it in side_groups:
        lines = files[f]['lines']; py = py_of(f)
        k = it['kind']
        if k == 'pp': title = ('import' if py else '#include') + (' × %d' % len(code_lines(lines, it['a'], it['b'], py)) if len(code_lines(lines, it['a'], it['b'], py)) > 1 else '')
        elif k == 'fn': title = it['name'] + '()'; fnames[it['name'].split('::')[-1]] = None
        elif k in ('type', 'ns'): title = it['name']
        elif k == 'shader': title = it['name']
        else:
            first = code_lines(lines, it['a'], it['b'], py)
            title = 'globals' if len(first) > 1 else (first[0] if first else 'globals')
        b = mk(f, it['a'], it['b'], title, k, 'side')
        if k == 'fn': fnames[it['name'].split('::')[-1]] = b
        if k == 'type':
            for mm in re.finditer(r'\b([A-Za-z_]\w*)\s*\([^;{]*\)\s*(const\s*)?\{', b['txt']):
                fnames.setdefault(mm.group(1), b)
    # flow blocks
    loops = []
    if flow_src:
        f, secs, head, tail, fname = flow_src; lines = files[f]['lines']; py = py_of(f)
        def title_of(a, b):
            for i in range(a, b + 1):
                t = lines[i - 1]
                if is_comment(t, py) and comment_text(t): return comment_text(t)
            cl = code_lines(lines, a, b, py)
            return cl[0] if cl else 'سطر %d' % a
        def add(secs, depth):
            for j, x in enumerate(secs):
                if x['kind'] == 'loop':
                    lb = mk(f, x['a'], x['b'], x['head'].rstrip('{').strip(), 'loop', 'flow')
                    lb['depth'] = depth; lb['loopstart'] = len(flow); flow.append(('loopstart', lb))
                    add(x['children'], depth + 1)
                    flow.append(('loopend', lb)); loops.append(lb)
                else:
                    extra = []
                    blk = mk(f, x['a'], x['b'], title_of(x['a'], x['b']), 'sec', 'flow')
                    blk['depth'] = depth; flow.append(('blk', blk))
        add(secs, 0)
        if head:  # function header & closing brace belong to the first/last flow block
            fb = next((b for t, b in flow if t == 'blk'), None)
            lb_ = next((b for t, b in reversed(flow) if t == 'blk'), None)
            if fb: fb['ranges'].append(head)
            if lb_: lb_['ranges'].append(tail)
            if fb: fb['ranges'] = [(min(fb['ranges'][0][0], head[0]), fb['ranges'][0][1])] + fb['ranges'][1:]
    # calls: which helper each block calls
    for b in blocks:
        if b['col'] == 'flow' and b['kind'] != 'loop' or (b['col'] == 'side' and b['kind'] == 'fn'):
            seen = []
            for nm, tb in fnames.items():
                if tb is None or tb is b: continue
                if re.search(r'(?<![\w.])' + re.escape(nm) + r'\s*\(', re.sub(r'^\s*\S[^(]*\b' + re.escape(nm) + r'\s*\([^)]*\)\s*$', '', b['txt'], flags=re.M) if b['kind'] == 'fn' and b['title'].startswith(nm) else b['txt']):
                    if tb['id'] not in seen: seen.append(tb['id']); b['calls'].append(tb)
    # coverage check: every line of every file belongs to a block (steps are recomputed after)
    for f, fl in enumerate(files):
        cov = set()
        for b in blocks:
            if b['f'] == f:
                for x, y in b['ranges']: cov |= set(range(x, y + 1))
        miss = [n for n in range(1, len(fl['lines']) + 1) if n not in cov and fl['lines'][n - 1].strip()]
        if miss:
            # attach any stray line to the nearest block before it
            for n in miss:
                cand = [b for b in blocks if b['f'] == f and b['ranges'][0][0] <= n]
                tgt = max(cand, key=lambda b: b['ranges'][0][0]) if cand else next(b for b in blocks if b['f'] == f)
                tgt['ranges'].append((n, n))
    for b in blocks:
        rng = b['ranges']; f = b['f']
        b['steps'] = sorted({k for (ff, ln), v in LS.items() if ff == f and any(x <= ln <= y for x, y in rng) for k in v})
        if not b['ar'] and b['steps']: b['ar'] = SINFO[b['steps'][0]].get('ti') or ''
    return blocks, flow, loops

# ---------------------------------------------------------------- SVG layout
W = 800; COLA = (20, 380); COLB = (420, 360)
def fit(s, n):
    s = s.replace('\t', ' ')
    return s if len(s) <= n else s[:n - 1] + '…'
def comp(ks):
    out = []
    for k in sorted(ks):
        if out and k == out[-1][1] + 1: out[-1][1] = k
        else: out.append([k, k])
    return ['%d' % a if a == b else '%d–%d' % (a, b) for a, b in out]
def ref_str(b):
    parts = []
    for x, y in sorted(set(b['ranges'])):
        parts.append(str(x) if x == y else '%d-%d' % (x, y))
    return ', '.join(parts)
def ref_short(b):
    x, y = b['ranges'][0]
    return 'L%d' % x if x == y else 'L%d-%d' % (x, y)

KIND_CLS = {'pp': 'ctl', 'glob': 'ram', 'type': 'vao', 'ns': 'vao', 'fn': 'prg', 'shader': 'prg', 'sec': 'buf', 'loop': 'm1', 'stmt': 'ram'}
def block_svg(b, x, y, w, multi):
    lines = [fit(l, int((w - 20) / 6.6)) for l in b['preview']]
    if b['calls']:
        lines = lines[:1] + [fit('→ ' + ', '.join(c['title'] for c in b['calls']), int((w - 20) / 6.6))]
    h = 30 + 15 * len(lines) + 24
    cls = KIND_CLS.get(b['kind'], 'buf')
    fn = ''
    out = [f'<g class="blk {cls}" data-id="{b["id"]}" data-f="{b["f"]}" data-r="{E(ref_str(b))}" data-t="{E(b["title"])}" tabindex="0" role="button" aria-label="{E(b["title"])}">',
           f'<rect class="bb" x="{x}" y="{y}" width="{w}" height="{h}" rx="7"/>',
           f'<text class="bt" x="{x + 10}" y="{y + 19}">{E(fit(b["title"], int((w - 70) / 7.4)))}</text>',
           f'<text class="ln" x="{x + w - 8}" y="{y + 19}" text-anchor="end">{E(ref_short(b))}</text>']
    for j, l in enumerate(lines):
        out.append(f'<text class="bl" x="{x + 10}" y="{y + 37 + j * 15}">{E(l)}</text>')
    st = comp(b['steps']); t = ('step ' + ', '.join(st)) if st else ''
    room = int((w - 30 - len(b['ar']) * 6.6) / 6.4)
    while t and len(t) > room and len(st) > 1:
        st = st[:-1]; t = 'step ' + ', '.join(st) + ' …'
    if t and len(t) > room: t = ''
    if t: out.append(f'<text class="stp" x="{x + 10}" y="{y + h - 9}">{E(t)}</text>')
    ar = b['ar'] if len(b['ar']) * 6.6 < w - 20 else fit(b['ar'], int((w - 20) / 6.6))
    out.append(f'<text class="ba" x="{x + w - 10}" y="{y + h - 9}" text-anchor="start" direction="rtl">{E(ar)}</text>')
    out.append('</g>')
    return '\n'.join(out), h

def layout(blocks, flow, loops, files):
    svg = []; multi = len(files) > 1
    ya = 50; yb = 50
    svg.append(f'<text class="zt" x="{COLA[0]}" y="34">التنفيذ بالترتيب</text>')
    svg.append(f'<text class="zt" x="{COLB[0]}" y="34">تعريفات ودوال</text>')
    pos = {}
    stack = []
    prev_bottom = None
    for t, b in flow:
        if t == 'loopstart':
            d = len(stack); x = COLA[0] + 14 * d; w = COLA[1] - 28 * d
            svg.append(f'@@LOOP{b["id"]}@@')
            stack.append((b, ya, x, w));
            # loop header block (thin)
            hdr = f'<g class="blk m1 lh" data-id="{b["id"]}" data-f="{b["f"]}" data-r="{E(ref_str(b))}" data-t="{E(b["title"])}" tabindex="0" role="button" aria-label="{E(b["title"])}"><rect class="bb" x="{x}" y="{ya}" width="{w}" height="34" rx="7"/><text class="bt" x="{x + 10}" y="{ya + 21}">🔁 {E(fit(b["title"], int((w - 90) / 7.4)))}</text><text class="ln" x="{x + w - 8}" y="{ya + 21}" text-anchor="end">{E(ref_short(b))}</text></g>'
            if prev_bottom is not None: svg.append(f'<path class="actl" d="M{x + 30} {prev_bottom} L{x + 30} {ya}" marker-end="url(#mc)"/>')
            svg.append(hdr); pos[b['id']] = (x, ya, w, 34); prev_bottom = ya + 34; ya += 46
            continue
        if t == 'loopend':
            lb, y0, x, w = stack.pop()
            y1 = ya + 4
            svg[svg.index(f'@@LOOP{lb["id"]}@@')] = f'<rect class="zloopr" x="{x - 6}" y="{y0 - 6}" width="{w + 12}" height="{y1 - y0 + 6}" rx="10"/>'
            # back arrow on the right side
            svg.append(f'<path class="actl" d="M{x + w - 4} {y1 - 8} L{x + w + 2} {y1 - 8} L{x + w + 2} {y0 + 17} L{x + w - 2} {y0 + 17}" marker-end="url(#mc)"/>')
            svg.append(f'<text class="al" x="{x + w - 6}" y="{y1 - 12}" text-anchor="end">كل لفة</text>')
            prev_bottom = y1; ya = y1 + 18
            continue
        d = len(stack); x = COLA[0] + 14 * d; w = COLA[1] - 28 * d
        g, h = block_svg(b, x, ya, w, multi)
        if prev_bottom is not None: svg.append(f'<path class="actl" d="M{x + 30} {prev_bottom} L{x + 30} {ya}" marker-end="url(#mc)"/>')
        svg.append(g); pos[b['id']] = (x, ya, w, h); prev_bottom = ya + h; ya += h + 16
    lastf = None
    for b in [b for b in blocks if b['col'] == 'side']:
        if multi and b['f'] != lastf:
            svg.append(f'<text class="zt" x="{COLB[0]}" y="{yb + 12}">📄 {E(files[b["f"]]["name"])}</text>'); yb += 22; lastf = b['f']
        g, h = block_svg(b, COLB[0], yb, COLB[1], multi)
        svg.append(g); pos[b['id']] = (COLB[0], yb, COLB[1], h); yb += h + 14
    H = max(ya, yb) + 20
    body = '\n'.join(svg)
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img">'
            '<defs><marker id="mc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="mkc"/></marker></defs>'
            + body + '</svg>')

# ---------------------------------------------------------------- page
def prog_html(p, day):
    blocks, flow, loops = build_program(p, day)
    files = p['files']; pid = p['id']
    LS = {}
    for k, s in enumerate(p['steps'], 1): LS.setdefault((s.get('f', 0), s['ln']), []).append(k)
    vars_ = set()
    for s in p['steps']:
        for fr in s.get('st') or []:
            for v in fr.get('v') or []: vars_.add(v[0])
    svg = layout(blocks, flow, loops, files)
    codes = []
    for f, fl in enumerate(files):
        py = fl['name'].endswith('.py')
        rows = []
        for n, t in enumerate(fl['lines'], 1):
            ks = LS.get((f, n), [])
            cs = ('·'.join(map(str, ks[:2])) + ('+' if len(ks) > 2 else '')) if ks else ''
            title = ('خطوة ' + '، '.join(map(str, ks))) if ks else ''
            rows.append(f'<span class="cl" data-f="{f}" data-n="{n}"><span class="cn">{n}</span><span class="cs" title="{E(title)}">{cs}</span>{hl(t, py, vars_) or " "}</span>')
        codes.append(f'<div class="cf"><div class="cfn">📄 <bdi dir="ltr">{E(fl["name"])}</bdi> · عدد {len(fl["lines"])} سطر</div><pre class="src" dir="ltr"><code>{"".join(rows)}</code></pre></div>')
    det = []
    for b in blocks:
        ks = b['steps']
        info = ''.join(f'<li><b>خطوة {k}</b> · سطر {p["steps"][k - 1]["ln"]}: {E(p["steps"][k - 1].get("ti") or "")}{(" — " + E(re.sub("<[^>]+>", "", p["steps"][k - 1].get("ex") or ""))[:220]) if p["steps"][k - 1].get("ex") else ""}</li>' for k in ks[:10])
        more = f'<li>… وعدد {len(ks) - 10} خطوة كمان</li>' if len(ks) > 10 else ''
        calls = ('<p>بينادي: ' + '، '.join(f'<bdi dir="ltr">{E(c["title"])}</bdi>' for c in b['calls']) + '</p>') if b['calls'] else ''
        det.append(f'<details data-d="{b["id"]}"><summary><bdi dir="ltr">{E(fit(b["title"], 60))}</bdi><span class="sl">{("📄 " + E(files[b["f"]]["name"]) + " · ") if len(files) > 1 else ""}سطر {E(ref_str(b))}</span></summary>'
                   f'<p>{E(b["ar"])}</p>{calls}' + (f'<p class="dst">🧭 خطوات البنش: {E("، ".join(comp(ks)))}</p><ul>{info}{more}</ul>' if ks else '<p class="dst">مفيش خطوات هنا: السطور دي مااتنفذتش لوحدها (تعريفات أو أقواس).</p>') +
                   f'<button type="button" class="goc" data-id="{b["id"]}">👁 وريني السطور دي في الكود</button></details>')
    return (f'<section class="prog" id="{pid.replace("_", "-")}" data-pid="{pid}"><details class="pd"><summary class="ph"><span class="pk">{E(p["kind"])}</span><b>{E(p["title"])}</b><span class="sl">عدد {sum(len(f["lines"]) for f in files)} سطر · عدد {len(p["steps"])} خطوة</span></summary>'
            f'<p class="desc">{E(re.sub("<[^>]+>", "", p.get("desc") or ""))}</p>'
            f'<div class="frame" dir="ltr">{svg}</div><p class="hint">دوس على أي صندوق يوديك على سطوره في الكود، ودوس على أي سطر يوديك على مكانه في الخريطة. الرقم الأحمر = رقم الخطوة في البنش.</p>'
            f'<details class="notes"><summary>📝 شرح كل صندوق (عدد {len(blocks)})</summary>{"".join(det)}</details>'
            f'<details class="codebox"><summary>💻 الكود كله</summary><button type="button" class="back">⬆ ارجع للخريطة</button>{"".join(codes)}</details>'
            f'</details></section>'), blocks

CSS = open('/home/claude/maps/style.css').read()
JS = open('/home/claude/maps/page.js').read()

def page(day, progs, extra=''):
    title = 'خرائط ' + DAYN[day]
    nav = ''.join(f'<a href="day{d}.html" class="{ "on" if d == day else ""}">{E(DAYN[d])}</a>' for d in range(1, 10))
    body = []; total = 0
    for p in progs:
        h, bl = prog_html(p, day); body.append(h); total += len(bl)
    toc = ''.join(f'<a href="#{p["id"].replace("_", "-")}" class="tc"><span class="pk">{E(p["kind"])}</span>{E(p["title"])}</a>' for p in progs)
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover"><title>{E(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><main>
<nav class="days">{nav}</nav>
<h1>🗺 {E(title)}</h1>
<p class="lede">لكل برنامج في {E(DAYN[day])} خريطة بتتعمل من الكود نفسه: كل صندوق حتة من البرنامج وجنبه أرقام سطوره، والأرقام الحمرا خطوات التشغيل الحقيقي في البنش. افتح أي برنامج تحت.</p>
<div class="toc">{toc}</div>
{extra}
{"".join(body)}
<p class="found" id="found" hidden></p>
</main><script>{JS}</script></body></html>'''

def index_page(counts):
    cards = ''.join(f'<a class="dcard" href="day{d}.html"><b>{E(DAYN[d])}</b><span>عدد {n} برامج</span></a>' for d, n in counts)
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover"><title>خرائط الكود</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><main>
<h1>🗺 خرائط الكود</h1><p class="lede">خريطة لكل برنامج في البنش: عدد {sum(n for _, n in counts)} برنامج في عدد {len(counts)} أيام (7 أيام الأسبوع اللي فات، و{len(counts) - 7} الأسبوع ده). كل يوم في صفحة لوحده.</p>
<div class="dgrid">{cards}</div></main></body></html>'''

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True); counts = []
    for d in range(1, 10):
        progs = json.load(open(DATA % d))['programs']
        extra = ''
        if d == 7:
            extra = '<p class="note">⭐ لبرنامج «تجربة حرة: الطريقتين جنب بعض» فيه كمان خريطة مفصّلة متعملة بإيدنا: <a href="https://claude.ai/artifact/AikUx1b9Gx3VPTVrYhsREp" target="_blank" rel="noopener">خريطة كود اليوم 7 ↗</a></p>'
        open(f'{OUT}/day{d}.html', 'w').write(page(d, progs, extra)); counts.append((d, len(progs)))
        print(d, len(progs), os.path.getsize(f'{OUT}/day{d}.html'))
    open(f'{OUT}/index.html', 'w').write(index_page(counts))
