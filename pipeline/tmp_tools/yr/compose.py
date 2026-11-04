# Rebuild the year plan PDF: every original page is copied as vector strips, and the new videos are
# added inside their cells (rows grow when needed). Links are copied and shifted.
import pymupdf, json, html, sys
SRC = '/tmp/claude-0/yr/y.pdf'
F = '/tmp/claude-0/fonts/'
CSS = f"""
@font-face {{ font-family: ar; src: url(ar400.ttf); }}
@font-face {{ font-family: arb; src: url(ar600.ttf); }}
@font-face {{ font-family: la; src: url(la400.ttf); }}
* {{ font-family: la, ar; font-size: 7pt; line-height: 1.32; margin: 0; padding: 0; }}
div {{ text-align: right; direction: rtl; color: #e6e6e3; }}
.new {{ color: #ffb454; font-family: arb, la; }}
.au {{ color: #6abf69; }}
.lk {{ color: #6abf69; }}
.t {{ direction: ltr; text-align: right; }}
.u {{ color: #7fb0ff; text-decoration: underline; direction: ltr; text-align: left; }}
"""
ARCH = pymupdf.Archive(F)
BG = (0.118, 0.118, 0.114); LINE = (0.29, 0.29, 0.278); DAYBG = (0.149, 0.149, 0.145)

import re
def _soft(t, n=9):
    # long unbreakable words (channel handles) get break points so the box never shrinks
    return re.sub(r'\S{%d,}' % (n + 1), lambda m: '\u200b'.join(m.group(0)[i:i + n] for i in range(0, len(m.group(0)), n)), t)
def block_html(v):
    u = v['url']; parts = [u[i:i + 14] for i in range(0, len(u), 14)]
    return (f'<div class="new">➕ فيديو مضاف</div>'
            f'<div class="au">{html.escape(_soft(v["channel"]))}</div>'
            f'<div class="{"t" if not any("\u0600" <= ch <= "\u06ff" for ch in v["title"]) else ""}">{html.escape(_soft(v["title"]))}</div>'
            f'<div class="lk">رابط الفيديو مباشر</div>'
            f'<div class="u">{"<br>".join(html.escape(p) for p in parts)}</div>')

_scratch = pymupdf.open(); _sp = _scratch.new_page(width=300, height=2000)
def measure(w, h_):
    r = pymupdf.Rect(0, 0, w, 1000)
    spare, scale = _sp.insert_htmlbox(r, h_, css=CSS, archive=ARCH, overlay=True)
    return 1000 - spare

def build(cells, adds, out):
    src = pymupdf.open(SRC); dst = pymupdf.open()
    by_page = {}
    for c in cells: by_page.setdefault(c['page'], []).append(c)
    link_jobs = []
    for pno in range(len(src)):
        sp = src[pno]; W, H = sp.rect.width, sp.rect.height
        cs = by_page.get(pno + 1)
        if not cs:
            np_ = dst.new_page(width=W, height=H); np_.show_pdf_page(np_.rect, src, pno)
            link_jobs.append((pno, len(dst) - 1, lambda y: y)); continue
        # rows (day bands) in order
        bands = sorted({(round(c['bbox'][1], 2), round(c['bbox'][3], 2)) for c in cs})
        chars = sp.get_text('rawdict')['blocks']
        def content_bottom(x0, t, x1, b):
            m = t
            for bl in chars:
                for ln in bl.get('lines', []):
                    r = pymupdf.Rect(ln['bbox'])
                    if r.x0 >= x0 - 1 and r.x1 <= x1 + 1 and r.y0 >= t - 1 and r.y1 <= b + 1: m = max(m, r.y1)
            return m
        plan = []; shift = 0
        for (t, b) in bands:
            row = [c for c in cs if round(c['bbox'][1], 2) == t]
            ext = 0; places = []
            for c in row:
                key = f"{c['page']}|{c['day']}|{c['col']}"
                if key not in adds: continue
                x0, _, x1, _ = c['bbox']; w = x1 - x0 - 4
                h_ = block_html(adds[key]); bh = measure(w, h_)
                cb = content_bottom(x0, t, x1, b) + 5
                ext = max(ext, cb + bh + 4 - b)
                places.append((x0 + 2, cb, x1 - 2, bh, h_, adds[key]['url']))
            plan.append((t, b, ext, places)); 
        top0 = bands[0][0]; tail0 = bands[-1][1]
        total_ext = sum(p[2] for p in plan)
        np_ = dst.new_page(width=W, height=H + total_ext)
        np_.draw_rect(np_.rect, color=None, fill=BG)
        np_.show_pdf_page(pymupdf.Rect(0, 0, W, top0), src, pno, clip=pymupdf.Rect(0, 0, W, top0))
        y = top0; segs = []  # (orig_t, orig_b, new_t)
        xs = sorted({round(c['bbox'][0], 2) for c in cs} | {round(c['bbox'][2], 2) for c in cs})
        dayx = max(xs); 
        for (t, b, ext, places) in plan:
            np_.show_pdf_page(pymupdf.Rect(0, y, W, y + (b - t)), src, pno, clip=pymupdf.Rect(0, t, W, b))
            segs.append((t, b, y))
            if ext > 0:
                ey0, ey1 = y + (b - t), y + (b - t) + ext
                # day column background + vertical borders over the extension
                np_.draw_rect(pymupdf.Rect(dayx, ey0, dayx + 31.5, ey1), color=None, fill=DAYBG)
                for x in xs + [dayx + 31.5]:
                    np_.draw_rect(pymupdf.Rect(x, ey0, x + 0.75, ey1), color=None, fill=LINE)
            for (x0, cb, x1, bh, h_, url) in places:
                ny = y + (cb - t)
                np_.insert_htmlbox(pymupdf.Rect(x0, ny, x1, ny + bh + 2), h_, css=CSS, archive=ARCH)
                link_jobs.append(('new', len(dst) - 1, pymupdf.Rect(x0, ny, x1, ny + bh), url))
            y += (b - t) + ext
        np_.show_pdf_page(pymupdf.Rect(0, y, W, y + (H - tail0)), src, pno, clip=pymupdf.Rect(0, tail0, W, H))
        def mapy(yy, segs=segs, top0=top0, tail0=tail0, y_end=y):
            if yy < top0: return yy
            for (t, b, ny) in segs:
                if t <= yy <= b: return ny + (yy - t)
            return y_end + (yy - tail0)
        link_jobs.append((pno, len(dst) - 1, mapy))
    # links
    for job in link_jobs:
        if job[0] == 'new': continue
        pno, dno, mapy = job
        for L in src[pno].get_links():
            r = L['from']; nr = pymupdf.Rect(r.x0, mapy(r.y0), r.x1, mapy(r.y0) + r.height)
            d = {'kind': L['kind'], 'from': nr}
            if L['kind'] == pymupdf.LINK_URI: d['uri'] = L['uri']
            elif L['kind'] == pymupdf.LINK_GOTO: d['page'] = L['page']; d['to'] = L.get('to', pymupdf.Point(0, 0))
            else: continue
            dst[dno].insert_link(d)
    return dst, link_jobs

if __name__ == '__main__':
    cells = json.load(open('/tmp/claude-0/yr/cells2.json'))
    adds = json.load(open(sys.argv[1]))
    dst, jobs = build(cells, adds, sys.argv[2])
    # links for the new blocks: whole block clickable
    for job in jobs:
        if job[0] != 'new': continue
        dst[job[1]].insert_link({'kind': pymupdf.LINK_URI, 'from': job[2], 'uri': job[3]})
    dst.save(sys.argv[2], garbage=4, deflate=True, deflate_fonts=True)
