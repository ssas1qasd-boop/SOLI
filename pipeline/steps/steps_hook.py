# Glue: append the "write it yourself" section right after the P.append() that showed a registered program.
import os, sys, importlib
sys.path.insert(0, '/home/claude/steps')
import render as R

CSS = R.CSS
_reg, _pending, _done = {}, [], set()
_cfg = {}

def setup(spec_modules, mode, hl, imgdir='img'):
    _cfg.update(mode=mode, hl=hl, imgdir=os.path.abspath(imgdir))
    import shutil; shutil.rmtree('cpfiles', ignore_errors=True)
    for m in spec_modules:
        for path, prog in importlib.import_module(m).programs().items():
            prog.build_and_run()
            _reg[os.path.abspath(path)] = prog

def seen(path):
    p = os.path.abspath(path)
    if p in _reg and _reg[p].pid not in _done:
        _pending.append(_reg[p])

class PList(list):
    def append(self, x):
        super().append(x)
        while _pending:
            prog = _pending.pop(0)
            if prog.pid in _done: continue
            _done.add(prog.pid)
            super().append(R.render(prog, _cfg['hl'], _cfg['mode'], _cfg['imgdir']))

def missing():
    return [p.pid for p in _reg.values() if p.pid not in _done]

# ---------------------------------------------------------------- copy without leaving the PDF:
# the 📋 button jumps to a plain copy of the code (no line numbers, no buttons) in an appendix at the end.
import html as _h, re as _r
_copies = []
_files = {}
CSS += '''
.cpapp h2 { font-size:15pt; margin:0 0 2mm; }
.cphow { font-size:10pt; background:#eef2ff; border:1px solid #c7d2fe; border-radius:2mm; padding:2mm 3mm; margin-bottom:4mm; }
.cpblk { margin:0; page-break-before:always; }
.cphead { display:block; overflow:hidden; background:#1e293b; color:#e2e8f0; border-radius:2mm 2mm 0 0; padding:1.2mm 3mm; font-size:9pt; }
.cphead a { margin-right:6mm; color:#a5b4fc !important; text-decoration:none; font-weight:bold; }
.cpimgs { text-align:right; margin:0 0 2mm; }
.cphimg { height:9mm; display:inline-block; margin:0 0 0 2mm; vertical-align:middle; }
.attlink { color:#0f766e !important; }
.cpcode { direction:ltr; text-align:left; white-space:pre; font-family:"DejaVu Sans Mono",monospace; font-size:8pt; line-height:1.4;
          background:#f8fafc; color:#0f172a; border:0; padding:0; margin:0; }
'''

def copylink(aid, label, raw, step=None):
    cid = f'{aid}-{len(_copies) + 1}'
    _copies.append((cid, label, raw, step))
    fn = _attach_file(label, raw, step)
    return (f' <a class="copylink" id="cpl-{cid}" href="#cp-{cid}">📋 اضغط هنا عشان تنسخ الكود</a>'
            f' <a class="copylink attlink" rel="attachment" href="{fn}">📎 افتح الملف نفسه</a>')

def _attach_file(label, raw, step):
    base, ext = os.path.splitext(_r.sub(r'[^A-Za-z0-9_.-]', '_', label))
    name = f'{base}_step{step}{ext}' if step else f'{base}{ext}'
    os.makedirs('cpfiles', exist_ok=True)
    p = os.path.join('cpfiles', name)
    k = 2
    while os.path.exists(p) and open(p).read() != raw:
        p = os.path.join('cpfiles', f'{os.path.splitext(name)[0]}_{k}{ext}'); k += 1
    open(p, 'w').write(raw)
    _files[id(raw), label, step] = p
    return p

def _header_images(items):
    """Render each block header (label + back arrow) to a PNG so 'Select all' on the page copies only the code."""
    import weasyprint, subprocess, glob, tempfile, hashlib
    key = hashlib.md5(repr([(l, st) for _, l, _, st in items]).encode()).hexdigest()[:10]
    d = f'/home/claude/steps/work/cphead_{key}'
    if not os.path.isdir(d) or len(glob.glob(d + '/h-*.png')) != len(items):
        os.makedirs(d, exist_ok=True)
        for f in glob.glob(d + '/*'): os.remove(f)
        pages = []
        for _, label, _, step in items:
            st = f'خطوة {step}' if step else 'البرنامج كامل'
            pages.append(f'<div class="h"><span class="b">↩ ارجع للكود</span><span class="t">📋 <span dir="ltr">{_h.escape(label)}</span> — {st}</span></div>')
        doc = ('<html dir="rtl"><style>@page{size:180mm 9mm;margin:0} body{margin:0;font-family:"Cairo","DejaVu Sans",sans-serif}'
               '.h{height:9mm;background:#1e293b;color:#e2e8f0;font-size:10pt;display:block;padding:0 3mm;line-height:9mm;page-break-after:always;overflow:hidden}'
               '.b{float:left;color:#a5b4fc;font-weight:bold}</style><body>' + ''.join(pages) + '</body></html>')
        weasyprint.HTML(string=doc).write_pdf(d + '/h.pdf')
        subprocess.run(['pdftoppm', '-r', '220', '-png', d + '/h.pdf', d + '/h'], check=True)
    files = sorted(glob.glob(d + '/h-*.png'), key=lambda p: int(_r.search(r'-(\d+)\.png$', p).group(1)))
    return files

def _header_images(items):
    """Render each block header (file, step, back button) to a PNG so it is not text: 'Select all' on the page then copies only the code."""
    import hashlib
    from playwright.sync_api import sync_playwright
    os.makedirs('img/cp', exist_ok=True)
    font = '/home/claude/day3/fonts/cairo-arabic-700-normal.woff'
    out, todo = {}, []
    for cid, label, step in items:
        st = f'خطوة {step}' if step else 'البرنامج كامل'
        key = hashlib.md5(f'v2|{label}|{st}'.encode()).hexdigest()[:16]
        p = f'img/cp/{key}.png'; out[cid] = p
        if not os.path.exists(p): todo.append((p, label, st))
    if todo:
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(device_scale_factor=3)
            for p, label, st in todo:
                pg.set_content(f"""<html><head><style>@font-face{{font-family:C;src:url(file://{font})}}
                body{{margin:0;background:transparent}}
                #h{{display:inline-flex;align-items:center;gap:14px;direction:rtl;font-family:C,sans-serif;font-size:15px;color:#e2e8f0;
                     background:#1e293b;border-radius:8px;padding:7px 12px;white-space:nowrap}}
                .f{{font-family:'DejaVu Sans Mono',monospace;direction:ltr}} .b{{background:#4338ca;color:#fff;border-radius:6px;padding:3px 10px}}
                .t{{color:#94a3b8;font-size:12px}}</style></head><body><div id="h">
                <span>📋</span><span class="f">{_h.escape(label)}</span><span>— {st}</span>
                <span class="b">↩ ارجع للكود</span><span class="t">ضغطة طويلة على الكود ← تحديد الكل ← نسخ</span></div></body></html>""")
                pg.locator('#h').screenshot(path=p, omit_background=True)
            b.close()
    return out

def _att_img():
    p = 'img/cp/attach_v1.png'
    if os.path.exists(p): return p
    from playwright.sync_api import sync_playwright
    os.makedirs('img/cp', exist_ok=True)
    font = '/home/claude/day3/fonts/cairo-arabic-700-normal.woff'
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(device_scale_factor=3)
        pg.set_content(f"""<html><head><style>@font-face{{font-family:C;src:url(file://{font})}}body{{margin:0}}
        #h{{display:inline-block;direction:rtl;font-family:C,sans-serif;font-size:15px;color:#fff;background:#0f766e;border-radius:8px;padding:7px 12px;white-space:nowrap}}</style></head>
        <body><div id="h">📎 افتح الملف نفسه (Cxxdroid)</div></body></html>""")
        pg.locator('#h').screenshot(path=p, omit_background=True); b.close()
    return p

def copy_appendix():
    global CSS
    if not _copies: return ''
    imgs = _header_images([(c, l, st) for c, l, r, st in _copies])
    h = ['<section class="cpapp" style="page-break-before:always"><h2>📋 الأكواد جاهزة للنسخ</h2>'
         '<div class="cphow"><b>ازاي تنسخ:</b> كل كود هنا في صفحة لوحده، والصفحة على قده بالظبط، فمش هيتقسم على صفحتين. '
         'ومفيش في الصفحة أي كلام غير الكود (اسم الملف والزرار صورة). '
         'اعمل <b>ضغطة طويلة على أي كلمة في الكود ← «تحديد الكل» ← «نسخ»</b>، هيتنسخ الكود كله ومفيش حاجة غيره. '
         'وبعدها دوس زرار «↩ ارجع للكود» اللي فوق الكود. '
         '<br><b>أو من غير نسخ خالص:</b> دوس <b>📎 افتح الملف نفسه</b>، والملف متخزن جوه الـ PDF. Foxit هيفتحه أو يسألك تفتحه بإيه: اختار Cxxdroid، وتدوس Run على طول.</div></section>']
    FS = 8.0
    for n, (cid, label, raw, step) in enumerate(_copies, 1):
        lines = raw.rstrip().split('\n')
        w = max(210, int(max(len(l.expandtabs(4)) for l in lines) * 0.61 * FS * 0.3528) + 24)
        hgt = int(len(lines) * FS * 1.4 * 0.3528 * 1.04) + 34
        CSS += f'@page cp{n} {{ size:{w}mm {hgt}mm; margin:6mm 8mm; @bottom-center {{ content:none; }} @top-center {{ content:none; }} }}\n'
        att = _files.get((id(raw), label, step))
        attl = f'<a rel="attachment" href="{att}"><img class="cphimg" src="{_att_img()}"></a>' if att else ''
        h.append(f'<div class="cpblk" id="cp-{cid}" style="page:cp{n}"><div class="cpimgs"><a href="#cpl-{cid}"><img class="cphimg" src="{imgs[cid]}"></a>{attl}</div>'
                 f'<pre class="cpcode">{_h.escape(raw.rstrip())}</pre></div>')
    return ''.join(h)
