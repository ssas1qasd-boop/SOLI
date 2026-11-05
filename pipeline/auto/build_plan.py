# Build plan.json (date -> {CAD, رياضيات, رسم, برمجة: [links]}) from the year-plan PDF, in one pass.
import sys, re, json, pymupdf
doc = pymupdf.open(sys.argv[1]); COLS = ['CAD', 'رياضيات', 'رسم', 'برمجة']; plan = {}
for page in doc:
    words = page.get_text('words')
    ds = sorted({(round(w[1]), w[4], w[0]) for w in words if re.fullmatch(r'\d\d-\d\d', w[4])})
    if not ds: continue
    links = [L for L in page.get_links() if L.get('uri')]
    for i, (y, d, x) in enumerate(ds):
        y0 = y - 4; y1 = ds[i + 1][0] - 4 if i + 1 < len(ds) else page.rect.height
        W = x / 4.0; cols = {c: [] for c in COLS}
        for L in links:
            my = (L['from'].y0 + L['from'].y1) / 2; mx = (L['from'].x0 + L['from'].x1) / 2
            if y0 <= my <= y1 and mx < x:
                c = COLS[min(3, int(mx // W))]
                if L['uri'] not in cols[c]: cols[c].append(L['uri'])
        if any(cols.values()): plan.setdefault(d, cols)
json.dump(plan, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
print(len(plan), 'days', sum(1 for v in plan.values() for c in v.values() for u in c if 'youtu' in u), 'youtube links')
