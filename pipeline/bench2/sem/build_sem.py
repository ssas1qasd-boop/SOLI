# Learns "which Egyptian-Arabic words go with which code words" from our own aligned data:
# every code line has an Arabic explanation (days 1-9), plus word-by-word chips and the glossary.
# Output: sem.json = {assoc: {arabic_stem: [[code_token, weight], ...]}, vocab: [...words for typo fixing]}
import re, json, math, sys, html, collections
sys.path.insert(0, '/home/claude/bench2'); sys.path.insert(0, '/home/claude/steps')
import edicts, allwords
JS = open('/home/claude/bench2/agent.js').read()
STOP = set(re.search(r"const STOP = new Set\(\((.*?)\)\.split", JS, re.S).group(1).replace("'", '').replace('+', ' ').split())
TAT = re.compile('[ً-ْـ‎‏‪-‮]')
def strip(h): return html.unescape(re.sub(r'<[^>]+>', ' ', str(h or '')))
def norm(s):
    s = TAT.sub('', strip(s))
    for a, b in (('أ', 'ا'), ('إ', 'ا'), ('آ', 'ا'), ('ٱ', 'ا'), ('ة', 'ه'), ('ى', 'ي'), ('ؤ', 'و'), ('ئ', 'ي')): s = s.replace(a, b)
    s = ''.join(str('٠١٢٣٤٥٦٧٨٩'.index(c)) if c in '٠١٢٣٤٥٦٧٨٩' else c for c in s)
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s)
    return s.lower()
def stem(w):
    if re.fullmatch(r'[a-z0-9_]+', w): return w
    for p in ('وبال', 'وال', 'بال', 'كال', 'فال', 'لل', 'ال'):
        if w.startswith(p) and len(w) - len(p) >= 2: w = w[len(p):]; break
    if len(w) > 3 and w[0] == 'و': w = w[1:]
    if len(w) >= 5 and w[0] == 'ل': w = w[1:]
    if len(w) >= 5 and w[:2] in ('بي', 'بت', 'بن'): w = w[2:]
    elif len(w) >= 4 and w[0] in 'يتنا': w = w[1:]
    if len(w) >= 4 and w[0] == 'ت': w = w[1:]
    for s_ in ('ات', 'ين', 'ون', 'ها', 'هم', 'ه'):
        if w.endswith(s_) and len(w) - len(s_) >= 3: w = w[:-len(s_)]; break
    return w
def ar_words(s):
    out = set()
    for w in re.split(r'[^a-z0-9_ء-ي]+', norm(s)):
        if not w or w in STOP or not re.search('[ء-ي]', w): continue
        w = stem(w)
        if w and w not in STOP and len(w) >= 2: out.add(w)
    return out
def code_words(s):
    out = set()
    for ident in re.findall(r'[A-Za-z_][A-Za-z0-9_]{2,}', strip(s)):
        out.add(ident.lower())
        for part in re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', ident):
            if len(part) >= 3: out.add(part.lower())
    return out
pairs = []  # (arabic set, code set)
E = edicts.load()
for d in ('day9',):  # day9's E already contains every earlier day
    for code, ex in E[d].items(): pairs.append((ar_words(ex), code_words(code)))
for d, over in E.items():
    if d.endswith('_over'):
        for f, m in over.items():
            for code, ex in m.items(): pairs.append((ar_words(ex), code_words(code)))
W = allwords.all_words()
for line, block in W.items():
    for tok, mean in re.findall(r'<div class="tok"><span class="ltr">(.*?)</span></div><div class="mean">(.*?)</div>', block):
        pairs.append((ar_words(mean), code_words(html.unescape(tok)) | code_words(line)))
    note = re.search(r'<div class="wnote">(.*?)</div>', block)
    if note: pairs.append((ar_words(note.group(1)), code_words(line)))
G = open('/home/claude/bench2/gloss.js').read()
for t, a, b in re.findall(r"^\s*'([^']+)':\s*\['((?:[^'\\]|\\.)*)',\s*'((?:[^'\\]|\\.)*)'\]", G, re.M):
    pairs.append((ar_words(a + ' ' + b), code_words(t + ' ' + a)))
pairs = [(a, c) for a, c in pairs if a and c]
N = len(pairs)
fa, fc, fac = collections.Counter(), collections.Counter(), collections.Counter()
for a, c in pairs:
    fa.update(a); fc.update(c)
    for x in a:
        for y in c: fac[(x, y)] += 1
assoc = collections.defaultdict(list)
for (x, y), n in fac.items():
    if n < 2 or fa[x] < 2: continue
    pmi = math.log(n * N / (fa[x] * fc[y])); npmi = pmi / -math.log(n / N)
    if npmi < .25: continue
    w = npmi * min(1, n / 4)
    assoc[x].append((y, round(w, 3)))
assoc = {x: sorted(v, key=lambda t: -t[1])[:6] for x, v in assoc.items()}
vocab = sorted(set(w for w in fa if fa[w] >= 2) | set(w for w in fc if fc[w] >= 2))
json.dump({'assoc': assoc, 'vocab': vocab, 'pairs': N}, open('/home/claude/bench2/sem/sem.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('pairs', N, 'arabic words with links', len(assoc), 'vocab', len(vocab), 'bytes', len(json.dumps({'assoc': assoc, 'vocab': vocab}, ensure_ascii=False, separators=(',', ':')).encode()))
for w in ['امسح', 'مسح', 'اربط', 'ربط', 'ابعت', 'نسخ', 'صندوق', 'شباك', 'لون', 'ركن', 'ترتيب', 'ارسم', 'لف', 'ترجم', 'خانه', 'مكان', 'صوره', 'شفاف', 'مثلث']:
    print(w, assoc.get(stem(norm(w)), '—'))
