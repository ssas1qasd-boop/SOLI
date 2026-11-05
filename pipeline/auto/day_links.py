# Usage: python3 day_links.py PLAN.pdf 05-11  -> the 4 lectures of that day with every link and its author (from the PDF itself)
import sys, re, json, pymupdf
pdf, want = sys.argv[1], sys.argv[2]
COLS = {0: 'CAD', 1: 'رياضيات', 2: 'رسم', 3: 'برمجة'}   # columns left -> right
doc = pymupdf.open(pdf)
for pno, page in enumerate(doc):
    words = page.get_text('words')
    dates = sorted({(round(w[1]), w[4]) for w in words if re.fullmatch(r'\d\d-\d\d', w[4])})
    hit = [d for d in dates if d[1] == want]
    if not hit: continue
    y0 = hit[0][0] - 4
    later = [d[0] for d in dates if d[0] > y0 + 8]
    y1 = (min(later) - 4) if later else page.rect.height
    # column edges from the vertical grid: use x of the day label column as the right edge
    dayx = min(w[0] for w in words if w[4] == want)
    lines = [b for b in page.get_text('dict')['blocks'] if b.get('lines')]
    xs = sorted({round(r.x0) for r in [pymupdf.Rect(l['bbox']) for b in lines for l in b['lines']] if y0 <= r.y0 <= y1 and r.x1 < dayx})
    W = dayx / 4.0
    out = {c: {'topic': '', 'items': []} for c in range(4)}
    links = [L for L in page.get_links() if L.get('uri') and y0 <= (L['from'].y0 + L['from'].y1) / 2 <= y1]
    for c in range(4):
        cx0, cx1 = c * W, (c + 1) * W
        txt = page.get_text('text', clip=pymupdf.Rect(cx0, y0, cx1, y1))
        out[c]['text'] = ' '.join(t.strip() for t in txt.splitlines() if t.strip())
        for L in links:
            mx = (L['from'].x0 + L['from'].x1) / 2
            if cx0 <= mx < cx1 and L['uri'] not in out[c]['items']: out[c]['items'].append(L['uri'])
    print(json.dumps({'page': pno + 1, 'day': want, 'cols': {COLS[c]: out[c] for c in range(4)}}, ensure_ascii=False, indent=1))
    break
else:
    print('day not found')
