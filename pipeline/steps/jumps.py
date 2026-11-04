# Jump links between code rows and their word-by-word blocks, with matching numbers (📍 N) on link and target.
import re, html, hashlib as _hl
REFS = {}
WTEXT = {}
WMARK = ' <span style="color:#2563eb">(شرحه كلمة كلمة فوق)</span>'
def wid(line): return 'w-' + _hl.md5(re.sub(r'\s+', ' ', line.strip()).encode()).hexdigest()[:10]
def link_words(h):
    seen = set()
    def add(m):
        i = wid(html.unescape(m.group(1)))
        if i in seen: return m.group(0)
        seen.add(i)
        back = ''.join(f'<a class="wback" href="#{rid}">↩ ارجع للسطر {ln} في <span class="ltr">{lb}</span></a>' for lb, ln, rid in REFS.get(i, []))
        return (f'<div class="wline" id="{i}"><div class="wcode"><span class="ltr">{m.group(1)}</span></div>'
                + (f'<div class="wbacks">{back}</div>' if back else ''))
    h = re.sub(r'<div class="wline"><div class="wcode"><span class="ltr">(.*?)</span></div>', add, h)
    miss = set(re.findall(r'href="#(w-[0-9a-f]{10})"', h)) - seen
    if miss:
        # lines explained word by word on another day: copy that block into a section at the end of this file
        import allwords
        A = allwords.all_words(); extra = []
        for i in sorted(miss, key=lambda x: min(r[1] for r in REFS.get(x, [('', 0, '')]))):
            w = A.get(re.sub(r'\s+', ' ', WTEXT.get(i, '')))
            if w:
                extra.append(w); 
        if extra:
            sec = ('<section class="wextra" style="page-break-before:always"><h2>🔍 كلمة كلمة: سطور اتشرحت في أيام تانية</h2>'
                   '<p class="what">السطور دي في برامج النهارده، وشرحها كلمة كلمة كان في يوم تاني، فجبناه هنا.</p>' + ''.join(extra) + '</section>')
            k = h.find('<section class="cpapp"')
            h = (h[:k] + sec + h[k:]) if k >= 0 else h + sec
            h = re.sub(r'<div class="wline"><div class="wcode"><span class="ltr">(.*?)</span></div>', add, h)
            for i in miss & seen:
                h = h.replace(f'<a class="wlink" href="#{i}">(شرحه كلمة كلمة فوق 🔗)</a>', f'<a class="wlink" href="#{i}">(شرحه كلمة كلمة في آخر الملف 🔗)</a>')
        miss = miss - seen
        if miss: print('WORD LINKS WITHOUT TARGET:', len(miss), [WTEXT.get(i) for i in miss])
    def fix(m): return m.group(0) if m.group(1) in seen else '<span style="color:#2563eb">(شرحه كلمة كلمة فوق)</span>'
    return re.sub(r'<a class="wlink" href="#(w-[0-9a-f]{10})">\(شرحه كلمة كلمة فوق 🔗\)</a>', fix, h)

JPRE = r'(?:sw|sl|tr|w|r)-[A-Za-z0-9_-]+'
def jump_numbers(h):
    """every jump link and its target get the same number: after a jump, look for the 📍 with that number."""
    tg = set(re.findall(r'href="#(' + JPRE + ')"', h))
    ids = [m.group(1) for m in re.finditer(r'id="(' + JPRE + ')"', h) if m.group(1) in tg]
    num = {}
    for i in ids: num.setdefault(i, len(num) + 1)
    def a(m):
        i = m.group(2)
        return m.group(0) if i not in num else f'{m.group(1)}{m.group(3)}<b class="jn">{num[i]}</b></a>'
    h = re.sub(r'(<a [^>]*href="#(' + JPRE + r')"[^>]*>)(.*?)</a>', a, h, flags=re.S)
    def t(m):
        i = m.group(2)
        if i not in num: return m.group(0)
        badge = f'<span class="jbadge">📍 {num[i]}</span>'
        tag = m.group(1)
        if tag.startswith('<tr'): return m.group(0)
        return m.group(0) + badge
    h = re.sub(r'<div class="wline" id="(' + JPRE + r')"[^>]*>', lambda m: m.group(0) + (f'<span class="jbadge">📍 {num[m.group(1)]}</span>' if m.group(1) in num else ''), h)
    # code lines inside the step blocks: badge at the END of the line, so the code keeps its indentation
    h = re.sub(r'(<span class="[^"]*" id="(' + JPRE + r')"[^>]*>(?:(?!id="sl-).)*?<a class="wl-go"[^>]*>.*?</a>)', lambda m: m.group(0) + (f'<span class="jbadge">📍 {num[m.group(2)]}</span>' if m.group(2) in num else ''), h, flags=re.S)
    h = re.sub(r'(<tr[^>]* id="(' + JPRE + r')"[^>]*>(?:(?!</tr>).)*?<td class="e">)', lambda m: m.group(0) + (f'<span class="jbadge">📍 {num[m.group(2)]}</span>' if m.group(2) in num else ''), h, flags=re.S)
    print('jump numbers:', len(num))
    return h

def mark(e, t, label, lnum):
    """in a program-table row: turn the 'explained word by word above' note into a link; returns (e, ' id=...' or '')"""
    if WMARK not in e: return e, ''
    w_ = wid(t.strip()); WTEXT[w_] = t.strip(); rid = f'r-{w_}-{len(REFS.setdefault(w_, [])) + 1}'; REFS[w_].append((label, lnum, rid))
    return e.replace(WMARK, f' <a class="wlink" href="#{w_}">(شرحه كلمة كلمة فوق 🔗)</a>'), f' id="{rid}"'

def apply(doc, LN, ext):
    return jump_numbers(LN.apply(link_words(doc), ext))

CSS = '''.wlink{color:#2563eb !important;text-decoration:underline;font-weight:bold}
.wline[id]{border:2px solid #f59e0b;border-radius:2mm;padding:1mm}
.jn{display:inline-block;min-width:4mm;margin:0 .8mm;padding:0 1mm;border-radius:2mm;background:#dc2626;color:#fff !important;font-size:7.5pt;line-height:1.5;text-align:center;font-family:"DejaVu Sans",sans-serif}
.jbadge{display:inline-block;margin:0 1mm 0 1mm;padding:.2mm 1.8mm;border-radius:2mm;background:#dc2626;color:#fff;font-size:8.5pt;font-weight:bold;font-family:"DejaVu Sans","CairoAr",sans-serif;direction:ltr;unicode-bidi:isolate}
.wbacks{margin:1mm 0;text-align:right}
.wback{display:inline-block;margin:0 0 1mm 2mm;padding:.6mm 2.5mm;border-radius:3mm;background:#fef3c7;border:1px solid #f59e0b;color:#92400e !important;font-size:9pt;font-weight:bold;text-decoration:none}
tr[id] td.e{background:#fffbeb;box-shadow:inset -3px 0 0 #f59e0b}
@keyframes wglow{0%,100%{box-shadow:0 0 0 0 rgba(245,158,11,0)}15%,70%{box-shadow:0 0 0 6px rgba(245,158,11,.75)}}
.wline:target,tr:target td{animation:wglow 3.5s ease-out 1}'''
