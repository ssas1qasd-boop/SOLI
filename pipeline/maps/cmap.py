# Concept maps in the style of the hand-made day-7 map: zones, boxes, data arrows.
# Each program gets a hand-written spec in specs/dN.txt (DSL below); this file lays it out.
#
# DSL
#   @prog_id                         start a program
#   [Zone title] v|h|g2 [w=N] [zram|zgpu|zloop|none]     start a zone (new row starts with "row")
#   row                              start a new row of zones
#   id cls title | line1 ; line2 | arabic | ref           a box   (ref: "5-9, 12" | "f1:3-9" | "-")
#        lines may use $term (real terminal output) or $img (real final frame)
#   : note text                      extra explanation for the box above (Arabic, HTML allowed)
#   > a b label                      data arrow a -> b
#   ~ a b label                      control arrow a -> b
import re, json, html, os, sys
sys.path.insert(0, '/home/claude/maps')
import mapgen as M
E = html.escape

W = 1500; MX = 30; G = 150; RG = 110; TOP = 14; BG = 48

def parse(path):
    progs = {}; cur = None; zone = None; last = None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if not line.strip() or line.lstrip().startswith('#!'): continue
        s = line.strip()
        if s.startswith('@'):
            cur = {'rows': [[]], 'arrows': [], 'boxes': {}}; progs[s[1:].strip()] = cur; zone = None; continue
        if s == 'row': cur['rows'].append([]); zone = None; continue
        m = re.match(r'^\[(.*?)\]\s*(.*)$', s)
        if m:
            opts = m.group(2).split()
            zone = {'title': m.group(1), 'lay': 'v', 'w': 1.0, 'cls': 'zloop', 'boxes': []}
            for o in opts:
                if o in ('v', 'h', 'g2', 'g3'): zone['lay'] = o
                elif o.startswith('w='): zone['w'] = float(o[2:])
                elif o in ('zram', 'zgpu', 'zloop', 'none'): zone['cls'] = o
            cur['rows'][-1].append(zone); continue
        if s[0] in '>~' and s[1] == ' ':
            parts = s[2:].split(None, 2)
            cur['arrows'].append((s[0], parts[0], parts[1], parts[2] if len(parts) > 2 else '')); continue
        if s.startswith(': '):
            last['note'] = (last.get('note', '') + ' ' + s[2:]).strip(); continue
        # box
        head, *rest = [x.strip().replace('\x00', '|') for x in s.replace('\\|', '\x00').split('|')]
        bid, cls, title = head.split(None, 2)
        lines = [x.strip() for x in rest[0].split(' ; ')] if rest and rest[0] else []
        ar = rest[1] if len(rest) > 1 else ''
        ref = rest[2] if len(rest) > 2 else '-'
        f = 0
        mm = re.match(r'^f(\d+):(.*)$', ref)
        if mm: f = int(mm.group(1)); ref = mm.group(2)
        last = {'id': bid, 'cls': cls, 'title': title, 'lines': lines, 'ar': ar, 'ref': ref.strip(), 'f': f}
        if zone is None:
            zone = {'title': '', 'lay': 'v', 'w': 1.0, 'cls': 'none', 'boxes': []}; cur['rows'][-1].append(zone)
        zone['boxes'].append(last); cur['boxes'][bid] = last
    return progs

def rng(r):
    out = []
    if r in ('-', '—', ''): return out
    for p in r.split(','):
        m = re.match(r'\s*(\d+)(?:\s*-\s*(\d+))?\s*$', p)
        if not m: raise ValueError('bad ref ' + r)
        out.append((int(m[1]), int(m[2] or m[1])))
    return out

CW = {'bt': 7.5, 'bl': 6.62, 'ba': 6.7, 'stp': 6.4}

def text_w(s, k):
    # Arabic glyphs in Cairo are narrower than mono cells; count them at 0.85
    n = sum(0.85 if '؀' <= ch <= 'ۿ' else 1 for ch in s)
    return n * CW[k]

def build(pid, spec, p, warn):
    files = p['files']
    LS = {}
    for k, s in enumerate(p['steps'], 1): LS.setdefault((s.get('f', 0), s['ln']), []).append(k)
    boxes = spec['boxes']
    for b in boxes.values(): b['ranges'] = rng(b['ref'])
    # coverage: every non-blank line belongs to a box; strays go to the nearest box (same file) before them
    for f, fl in enumerate(files):
        cov = set()
        for b in boxes.values():
            if b['f'] == f:
                for x, y in b['ranges']: cov |= set(range(x, y + 1))
        miss = [n for n in range(1, len(fl['lines']) + 1) if n not in cov and fl['lines'][n - 1].strip()]
        if miss: warn.append(f'{pid} f{f}: auto-attached lines {miss[:12]}{"+" if len(miss) > 12 else ""} ({len(miss)})')
        for n in miss:
            cand = [b for b in boxes.values() if b['f'] == f and b['ranges']]
            if not cand: warn.append(f'{pid}: no box for file {f}'); break
            def dist(b):
                d = min(0 if x <= n <= y else min(abs(n - x), abs(n - y)) for x, y in b['ranges'])
                return (d, -min(x for x, y in b['ranges']))
            tgt = min(cand, key=dist)
            tgt.setdefault('extra', []).append(n)
        for b in boxes.values():
            if b['f'] == f and b.get('extra'):
                ex = sorted(b['extra']); grp = []
                for n in ex:
                    if grp and n == grp[-1][1] + 1: grp[-1][1] = n
                    else: grp.append([n, n])
                b['ranges'] += [tuple(g) for g in grp]
    for b in boxes.values():
        b['steps'] = sorted({k for (ff, ln), v in LS.items() if ff == b['f'] and any(x <= ln <= y for x, y in b['ranges']) for k in v})
    return boxes

def ref_str(b):
    parts = []
    for x, y in sorted(set(b['ranges'])):
        parts.append(str(x) if x == y else '%d-%d' % (x, y))
    return ', '.join(parts)

def ref_head(b):
    # what is printed on the box: the hand-written ref (before stray lines were added)
    r = rng(b['ref'])
    if not r: return ''
    full = 'L' + ', '.join(str(x) if x == y else '%d-%d' % (x, y) for x, y in r)
    if len(full) <= 16 or len(r) == 1: return full
    x, y = r[0]
    return ('L%d' % x if x == y else 'L%d-%d' % (x, y)) + ' +'

def box_lines(b, p, w):
    out = []
    for l in b['lines']:
        if l == '$term':
            t = term_lines(p)
            cap = int((w - 20) / CW['bl'])
            rows_ = []
            for x in t:
                x = x.rstrip()
                while len(x) > cap:
                    cut = x.rfind(' ', 0, cap)
                    if cut < cap // 2: cut = cap
                    rows_.append(x[:cut]); x = '  ' + x[cut:].lstrip()
                rows_.append(x)
            for x in rows_[:9]: out.append(('t', x))
            if len(rows_) > 9: out.append(('tx', f'وعدد {len(rows_) - 9} سطر كمان في الشرح'))
        elif l == '$termnote':
            continue
        elif l == '$img':
            out.append(('img', None))
        else:
            out.append(('l', l))
    return out

def term_lines(p):
    # the bench stored stdout in flush-sized pieces; glue pieces that belong to one printed line
    out = []
    for x in p.get('term') or []:
        x = ''.join(ch if ch >= ' ' else '' for ch in x)
        if out and (out[-1].endswith((' ', '[')) or x.startswith((', ', ']')) or re.match(r'^ -?\d', x)): out[-1] += x
        else: out.append(x)
    return out

IMG_H = 120

def box_h(b, p, w):
    h = 30 + 22
    for k, l in box_lines(b, p, w):
        h += IMG_H + 8 if k == 'img' else 16
    return max(h, 62)

def layout(pid, spec, p, warn):
    rows = spec['rows']; boxes = spec['boxes']
    pos = {}; zrects = []; y = TOP
    rowspan = []
    for ri, row in enumerate(rows):
        if not row: continue
        n = len(row); avail = W - 2 * MX - G * (n - 1); tw = sum(z['w'] for z in row)
        x = MX; zh = []
        for zi, z in enumerate(row):
            zw = avail * z['w'] / tw
            z['x'], z['y'], z['wd'], z['ri'] = x, y, zw, ri
            top = y + (30 if z['title'] else 4)
            lay = z['lay']; bs = z['boxes']
            if lay == 'v':
                bw = zw - 20; cy = top
                for o, b in enumerate(bs):
                    h = box_h(b, p, bw); b.update(x=x + 10, y=cy, w=bw, h=h, z=z, o=o); cy += h + BG
                bottom = cy - BG + 10
            else:
                cols = len(bs) if lay == 'h' else int(lay[1])
                gap = 90 if lay == 'h' else BG
                bw = (zw - 20 - gap * (cols - 1)) / cols
                cy = top; bottom = top
                for o in range(0, len(bs), cols):
                    chunk_ = bs[o:o + cols]
                    hh = max(box_h(b, p, bw) for b in chunk_)
                    for j, b in enumerate(chunk_):
                        b.update(x=x + 10 + j * (bw + gap), y=cy, w=bw, h=hh, z=z, o=o + j)
                    cy += hh + BG; bottom = cy - BG + 10
            zh.append(bottom - y); x += zw + G
        H = max(zh) if zh else 0
        for z in row: z['ht'] = H
        rowspan.append((y, y + H)); y += H + RG
    total_h = y - RG + TOP
    return rowspan, total_h

def route(spec, rowspan, warn, pid):
    boxes = spec['boxes']; rows = spec['rows']
    lanes = {}
    def gut(xl):
        # one shared set of lanes per gutter (gutter = the gap that starts at x = xl)
        if xl < MX: return lane(('g', 'L'), MX - 8, 6, -1)          # left page margin
        if xl >= W - MX - 1: return lane(('g', 'R'), W - MX + 8, 6)  # right page margin
        return lane(('g', round(xl)), xl + 12, 9)
    def lane(key, base, step, sign=1):
        k = lanes.get(key, 0); lanes[key] = k + 1
        return base + sign * step * k
    # first pass: decide sides, then spread the ports along each side
    plans = []
    for kind, a, b, lab in spec['arrows']:
        if a not in boxes or b not in boxes:
            warn.append(f'{pid}: arrow to unknown box {a}->{b}'); continue
        A, B = boxes[a], boxes[b]
        za, zb = A['z'], B['z']
        ra, rb = za['ri'], zb['ri']
        plans.append((kind, A, B, lab))
    ports = {}
    def port(bx, side):
        ports.setdefault((bx['id'], side), 0); ports[(bx['id'], side)] += 1
    resolved = []
    for kind, A, B, lab in plans:
        za, zb = A['z'], B['z']; ra, rb = za['ri'], zb['ri']
        if za is zb and za['lay'] == 'v':
            if B['o'] == A['o'] + 1: mode = ('down',)
            elif B['o'] == A['o'] - 1: mode = ('up',)
            else: mode = ('side', 'r')
        elif za is zb:
            if abs(B['y'] - A['y']) < 1:
                mode = ('hr',) if B['x'] > A['x'] else ('hl',)
            else:
                mode = ('vrow',) if B['y'] > A['y'] else ('vrowu',)
        elif ra == rb:
            row = rows[ra]; ia, ib = row.index(za), row.index(zb)
            if abs(ia - ib) > 1: mode = ('gfar',)
            else: mode = ('gr',) if zb['x'] > za['x'] else ('gl',)
        elif rb == ra + 1: mode = ('nextrow',)
        elif rb == ra - 1: mode = ('prevrow',)
        else: mode = ('far',)
        resolved.append((kind, A, B, lab, mode))
        s_out, s_in = {'down': ('b', 't'), 'up': ('t', 'b'), 'side': ('r', 'r'), 'hr': ('r', 'l'), 'hl': ('l', 'r'),
                       'vrow': ('b', 't'), 'vrowu': ('t', 'b'), 'gr': ('r', 'l'), 'gl': ('l', 'r'),
                       'nextrow': ('X', 't'), 'prevrow': ('Y', 'b'), 'far': ('r', 't'), 'gfar': ('r', 'l')}[mode[0]]
        port(A, s_out); port(B, s_in)
    def run(counting):
        lanes.clear(); used.clear()
        if counting: ports.clear()
        def pt(bx, side):
            if counting: ports[(bx['id'], side)] = ports.get((bx['id'], side), 0) + 1
            n = max(1, ports.get((bx['id'], side), 1)); k = used.get((bx['id'], side), 0); used[(bx['id'], side)] = k + 1
            k = min(k, n - 1)
            x, y, w, h = bx['x'], bx['y'], bx['w'], bx['h']
            if side in 'lr':
                ys = [y + h * (i + 1) / (n + 1) for i in range(n)] if n > 1 else [y + h / 2]
                return (x if side == 'l' else x + w, ys[k])
            span = min(w - 40, 60 * n)
            xs = [x + w / 2 - span / 2 + span * i / (n - 1) for i in range(n)] if n > 1 else [x + w / 2]
            return (xs[k], y if side == 't' else y + h)
        paths = []
        for kind, A, B, lab, mode in resolved:
            za, zb = A['z'], B['z']; m = mode[0]
            if m == 'down':
                p0 = pt(A, 'b'); p1 = pt(B, 't'); x = (p0[0] + p1[0]) / 2; pts = [(x, p0[1]), (x, p1[1])]
            elif m == 'up':
                p0 = pt(A, 't'); p1 = pt(B, 'b'); x = (p0[0] + p1[0]) / 2 + 36; pts = [(x, p0[1]), (x, p1[1])]
            elif m == 'side':
                p0 = pt(A, 'r'); p1 = pt(B, 'r'); gx = gut(za['x'] + za['wd'])
                pts = [p0, (gx, p0[1]), (gx, p1[1]), p1]
            elif m in ('hr', 'hl'):
                p0 = pt(A, 'r' if m == 'hr' else 'l'); p1 = pt(B, 'l' if m == 'hr' else 'r')
                if abs(p0[1] - p1[1]) < 1: pts = [p0, p1]
                else:
                    mx = (p0[0] + p1[0]) / 2; pts = [p0, (mx, p0[1]), (mx, p1[1]), p1]
            elif m in ('vrow', 'vrowu'):
                p0 = pt(A, 'b' if m == 'vrow' else 't'); p1 = pt(B, 't' if m == 'vrow' else 'b')
                my = (p0[1] + p1[1]) / 2; pts = [p0, (p0[0], my), (p1[0], my), p1]
            elif m in ('gr', 'gl'):
                p0 = pt(A, 'r' if m == 'gr' else 'l'); p1 = pt(B, 'l' if m == 'gr' else 'r')
                gx = gut(zb['x'] - G) if m == 'gr' else gut(zb['x'] + zb['wd'])
                pts = [p0, (gx, p0[1]), (gx, p1[1]), p1] if abs(p0[1] - p1[1]) > 0.5 else [p0, p1]
            elif m == 'gfar':
                # under the zones in between: A's right gutter -> the gap below the row -> B's left gutter
                right = zb['x'] > za['x']
                p0 = pt(A, 'r' if right else 'l'); p1 = pt(B, 'l' if right else 'r')
                row = rows[za['ri']]; ia, ib = row.index(za), row.index(zb)
                mids = [bx for z in row[min(ia, ib) + 1:max(ia, ib)] for bx in z['boxes']]
                free = lambda yy: all(not (bx['y'] - 6 <= yy <= bx['y'] + bx['h'] + 6) for bx in mids)
                if free(p0[1]):
                    g2 = gut(zb['x'] - G) if right else gut(zb['x'] + zb['wd'])
                    pts = [p0, (g2, p0[1]), (g2, p1[1]), p1]
                elif free(p1[1]):
                    g1 = gut(za['x'] + za['wd']) if right else gut(za['x'] - G)
                    pts = [p0, (g1, p0[1]), (g1, p1[1]), p1]
                else:
                    g1 = gut(za['x'] + za['wd']) if right else gut(za['x'] - G)
                    g2 = gut(zb['x'] - G) if right else gut(zb['x'] + zb['wd'])
                    ly = lane(('rg', za['ri']), rowspan[za['ri']][1] + 14, 8)
                    pts = [p0, (g1, p0[1]), (g1, ly), (g2, ly), (g2, p1[1]), p1]
            elif m in ('nextrow', 'prevrow', 'far'):
                down = m != 'prevrow'
                # leave A: bottom (or top) when nothing of its zone is in the way, else the side gutter
                sib = [b for b in za['boxes'] if (b['y'] > A['y'] + 1 if down else b['y'] < A['y'] - 1) and b['x'] < A['x'] + A['w'] and b['x'] + b['w'] > A['x']]
                ya_top, ya_bot = rowspan[za['ri']]
                gap_y = lambda r, below: (rowspan[r][1] if below else rowspan[r][0])
                if m == 'far':
                    # leave A into the row gap next to its row, run along the right page margin,
                    # then come into the row gap next to B's row and enter B
                    dn = zb['ri'] > za['ri']
                    sibA = [b for b in za['boxes'] if (b['y'] > A['y'] + 1 if dn else b['y'] < A['y'] - 1) and b['x'] < A['x'] + A['w'] and b['x'] + b['w'] > A['x']]
                    lyA = lane(('rg', za['ri'] if dn else za['ri'] - 1), (rowspan[za['ri']][1] + 14) if dn else (rowspan[za['ri']][0] - 14), 8, 1 if dn else -1)
                    if sibA:
                        right = za['x'] + za['wd'] < W - MX - 5
                        p0 = pt(A, 'r' if right else 'l')
                        gx = gut(za['x'] + za['wd']) if right else gut(za['x'] - G)
                        head = [p0, (gx, p0[1]), (gx, lyA)]
                    else:
                        p0 = pt(A, 'b' if dn else 't'); head = [p0, (p0[0], lyA)]
                    rx = gut(W - MX)
                    lyB = lane(('rg', zb['ri'] - 1 if dn else zb['ri']), (rowspan[zb['ri']][0] - 14) if dn else (rowspan[zb['ri']][1] + 14), 8, -1 if dn else 1)
                    bsib = [b for b in zb['boxes'] if (b['y'] < B['y'] - 1 if dn else b['y'] > B['y'] + 1) and b['x'] < B['x'] + B['w'] and b['x'] + b['w'] > B['x']]
                    if bsib:
                        bl = zb['x'] > MX + 5
                        p1 = pt(B, 'l' if bl else 'r')
                        gx2 = gut(zb['x'] - G) if bl else gut(zb['x'] + zb['wd'])
                        pts = head + [(rx, lyA), (rx, lyB), (gx2, lyB), (gx2, p1[1]), p1]
                    else:
                        p1 = pt(B, 't' if dn else 'b')
                        pts = head + [(rx, lyA), (rx, lyB), (p1[0], lyB), p1]
                else:
                    tgt_row = zb['ri']
                    ly = lane(('rg', min(za['ri'], tgt_row)), (rowspan[za['ri']][1] + 14) if down else (rowspan[za['ri']][0] - 14), 8, 1 if down else -1)
                    # boxes of B's zone between the row gap and B block a straight entry
                    bsib = [b for b in zb['boxes'] if (b['y'] < B['y'] - 1 if down else b['y'] > B['y'] + 1) and b['x'] < B['x'] + B['w'] and b['x'] + b['w'] > B['x']]
                    if sib:
                        right = za['x'] + za['wd'] < W - MX - 5
                        p0 = pt(A, 'r' if right else 'l')
                        gx = gut(za['x'] + za['wd']) if right else gut(za['x'] - G)
                        head = [p0, (gx, p0[1]), (gx, ly)]
                    else:
                        p0 = pt(A, 'b' if down else 't'); head = [p0, (p0[0], ly)]
                    if bsib:
                        bl = zb['x'] > MX + 5
                        p1 = pt(B, 'l' if bl else 'r')
                        gx2 = gut(zb['x'] - G) if bl else gut(zb['x'] + zb['wd'])
                        pts = head + [(gx2, ly), (gx2, p1[1]), p1]
                    else:
                        p1 = pt(B, 't' if down else 'b')
                        pts = head + [(p1[0], ly), p1]
            # collapse zero-length / colinear points
            clean = [pts[0]]
            for q in pts[1:]:
                if abs(q[0] - clean[-1][0]) < 0.5 and abs(q[1] - clean[-1][1]) < 0.5: continue
                clean.append(q)
            paths.append((kind, clean, lab, A['id'], B['id']))
        return paths
    used = {}
    run(True)
    return run(False)

def svg_for(pid, spec, p, warn):
    rowspan, H = layout(pid, spec, p, warn)
    paths = route(spec, rowspan, warn, pid)
    H = max([H] + [y_ + 14 for _, pts_, *_r in paths for _, y_ in pts_])
    boxes = spec['boxes']
    out = []; placed = []
    for row in spec['rows']:
        for z in row:
            if z['cls'] != 'none':
                out.append(f'<rect class="{z["cls"]}" x="{z["x"]:.0f}" y="{z["y"]:.0f}" width="{z["wd"]:.0f}" height="{z["ht"]:.0f}" rx="10"/>')
            if z['title']:
                out.append(f'<text class="zt" x="{z["x"] + 10:.0f}" y="{z["y"] + 19:.0f}">{E(z["title"])}</text>')
                if text_w(z['title'], 'bl') > z['wd'] - 16: warn.append(f'{pid}: zone title too long: {z["title"]}')
    for kind, pts, lab, ia, ib in paths:
        cls = 'actl' if kind == '~' else 'adat'
        d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
        _lm = re.match(r'^L(\d+)$', (lab or '').strip())
        out.append(f'<path class="{cls}" data-a="{ia}" data-b="{ib}" data-l="{_lm.group(1) if _lm else ""}" d="{d}" marker-end="url(#{("mc" if kind == "~" else "md") + "-" + pid})"/>')
        if lab:
            lw = text_w(lab, 'bl')
            segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
            hs = [s_ for s_ in segs if abs(s_[0][1] - s_[1][1]) < 0.5 and abs(s_[0][0] - s_[1][0]) > lw + 10]
            if hs:
                (x0, y0), (x1, y1) = max(hs, key=lambda s_: abs(s_[0][0] - s_[1][0]))
                lo, hi = min(x0, x1) + lw / 2 + 4, max(x0, x1) - lw / 2 - 4
                cx = (x0 + x1) / 2
                # slide along the line until it does not sit on another label
                for tries in range(40):
                    r = (cx - lw / 2, y0 - 15, cx + lw / 2, y0 - 2)
                    if not any(r[0] < q[2] and q[0] < r[2] and r[1] < q[3] and q[1] < r[3] for q in placed): break
                    cx += (lw / 2 + 8) * (1 if tries % 2 == 0 else -1) * (tries // 2 + 1)
                    cx = min(max(cx, lo), hi)
                placed.append((cx - lw / 2, y0 - 15, cx + lw / 2, y0 - 2))
                out.append(f'<text class="al" x="{cx:.0f}" y="{y0 - 5:.0f}" text-anchor="middle">{E(lab)}</text>')
            else:
                vs = [s_ for s_ in segs if abs(s_[0][0] - s_[1][0]) < 0.5]
                (x0, y0), (x1, y1) = max(vs or segs, key=lambda s_: abs(s_[0][1] - s_[1][1]))
                my = (y0 + y1) / 2
                if abs(y1 - y0) > lw + 16:
                    rects = [(bx['x'], bx['y'], bx['x'] + bx['w'], bx['y'] + bx['h']) for bx in boxes.values()]
                    def clash(xa, xb):
                        return any(xa < r[2] and r[0] < xb and my - lw / 2 < r[3] and r[1] < my + lw / 2 for r in rects)
                    tx = x0 - 5 if not clash(x0 - 17, x0 - 4) else x0 + 15
                    out.append(f'<text class="al" x="{tx:.0f}" y="{my:.0f}" transform="rotate(-90 {tx:.0f} {my:.0f})" text-anchor="middle">{E(lab)}</text>')
                else:
                    if abs(y1 - y0) < 20: warn.append(f'{pid}: no room for label {lab}')
                    out.append(f'<text class="al" x="{x0 + 8:.0f}" y="{my + 4:.0f}">{E(lab)}</text>')
                    placed.append((x0 + 8, my - 8, x0 + 8 + lw, my + 5))
    for b in boxes.values():
        x, y, w, h = b['x'], b['y'], b['w'], b['h']
        rs = ref_str(b)
        out.append(f'<g class="blk {b["cls"]}" data-id="{b["id"]}" data-f="{b["f"]}" data-r="{E(rs)}" data-t="{E(b["title"])}" tabindex="0" role="button" aria-label="{E(b["title"])}">')
        out.append(f'<rect class="bb" x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="7"/>')
        rh = ref_head(b)
        out.append(f'<text class="bt" x="{x + 10:.0f}" y="{y + 19:.0f}">{E(b["title"])}</text>')
        out.append(f'<text class="ln" x="{x + w - 8:.0f}" y="{y + 19:.0f}" text-anchor="end">{E(rh)}</text>')
        if text_w(b['title'], 'bt') + text_w(rh, 'stp') + 26 > w: warn.append(f'{pid}/{b["id"]}: title + ref too wide ({b["title"]})')
        cy = y + 37
        for k, l in box_lines(b, p, w):
            if k == 'img':
                fm = (p.get('frames') or [None])[-1]
                if fm:
                    iw0, ih0 = p.get('W') or 4, p.get('H') or 3
                    ih = IMG_H; iw = ih * iw0 / ih0
                    if iw > w - 40: iw = w - 40; ih = iw * ih0 / iw0
                    out.append(f'<image href="{fm}" x="{x + (w - iw) / 2:.0f}" y="{cy - 8 + (IMG_H - ih) / 2:.0f}" width="{iw:.0f}" height="{ih:.0f}"/>')
                else: warn.append(f'{pid}: $img but no frame')
                cy += IMG_H + 8; continue
            if k == 'tx':
                out.append(f'<text class="bl" x="{x + w - 10:.0f}" y="{cy:.0f}" text-anchor="start" direction="rtl">{E(l)}</text>'); cy += 16; continue
            out.append(f'<text class="bl{" tm" if k == "t" else ""}" x="{x + 10:.0f}" y="{cy:.0f}">{E(l)}</text>')
            if k == 'l' and text_w(l, 'bl') > w - 18: warn.append(f'{pid}/{b["id"]}: line too wide: {l}')
            cy += 16
        st = M.comp(b['steps']); t = ('step ' + ', '.join(st)) if st else ''
        room = w - 26 - text_w(b['ar'], 'ba')
        cut = False
        while t and text_w(t, 'stp') > room and len(st) > 1:
            st = st[:-1]; t = 'step ' + ', '.join(st) + ' +'; cut = True
        if t and text_w(t, 'stp') > room: t = ''
        if t: out.append(f'<text class="stp" x="{x + 10:.0f}" y="{y + h - 9:.0f}">{E(t)}</text>')
        if text_w(b['ar'], 'ba') > w - 20: warn.append(f'{pid}/{b["id"]}: arabic too wide: {b["ar"]}')
        out.append(f'<text class="ba" x="{x + w - 10:.0f}" y="{y + h - 9:.0f}" text-anchor="start" direction="rtl">{E(b["ar"])}</text>')
        out.append('</g>')
    return (f'<svg viewBox="0 0 {W} {H:.0f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{E(p["title"])}">'
            f'<defs><marker id="md-{pid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="mkd"/></marker>'
            f'<marker id="mc-{pid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="mkc"/></marker></defs>'
            + ''.join(out) + '</svg>')

def _short(v, n=16):
    v = html.unescape(re.sub(r'<[^>]+>', '', str(v))).replace('…', '').replace('...', '').strip()
    if re.search(r'[\u0600-\u06FF]', v): v = 'address' if 'عنوان' in v else ''
    if v.startswith('{') or v.startswith('['):
        items = [x.strip() for x in re.split(r',\s*', v.strip('{}[] ')) if x.strip()]
        if len(items) > 3: v = v[0] + ', '.join(items[:3]) + ' +more' + ('}' if v[0] == '{' else ']')
        n = max(n, 24)
    return v if len(v) <= n else v[:n - 1].rstrip() + '›'

def _vtype(name, v, dy):
    v = str(v)
    if name.startswith('GL_') or name.startswith('GLFW_'): return 'enum'
    if name.startswith('&') or v.startswith('0x') or 'عنوان' in v: return 'ptr'
    if v.startswith('"'): return 'text'
    if re.match(r'^[{\[]', v): return 'struct' if '=' in v else ('float' if '.' in v else 'int')
    if re.match(r'^-?\d+$', v): return 'int'
    if re.match(r'^-?[\d.]+(e[+-]?\d+)?f?$', v): return 'float'
    if v in ('true', 'false', 'True', 'False'): return 'bool'
    return 'data'

def _packet(s):
    """the named balls that travel for one step: [[name, value, type], ...] from the real trace"""
    lv = s.get('lv') or []; dy = ' '.join(map(str, s.get('dy') or []))
    out = []
    for m in re.finditer(r'<code>(.*?)</code>\s*=\s*(?:<b[^>]*>(.*?)</b>|([^،<]+))', dy):
        nm = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip(); val = m.group(2) if m.group(2) is not None else m.group(3)
        if 'القيم الحقيقية' not in dy[:dy.find(m.group(0))] and not out and 'بعد السطر ده' not in dy[:dy.find(m.group(0))]: continue
        if len(nm) > 22: continue
        out.append([nm, _short(val), _vtype(nm, html.unescape(re.sub(r'<[^>]+>', '', str(val))).strip(), dy)])
    if lv:
        kind, _, t = lv[0]; t = str(t)
        if '<error' in t: t = ''
        if kind == 'ram' and ' = ' in t and not out:
            nm, val = t.split(' = ', 1); ty = _vtype(nm, val, dy)
            m = re.search(r'النوع:</b>(.*?)(?:\'|$)', dy)
            if m and ty in ('int', 'float', 'data', 'struct'):
                d2 = m.group(1)
                for k2, v2 in (('Pointer', 'ptr'), ('double', 'float'), ('float', 'float'), ('GLfloat', 'float'), ('unsigned', 'uint'), ('GLuint', 'uint'), ('bool', 'bool'), ('char', 'text'), ('int', 'int'), ('class', 'struct'), ('struct', 'struct')):
                    if k2 in d2: ty = v2; break
            out.append([nm.strip(), _short(val), ty])
        elif kind == 'buf':
            m = re.search(r'(\d[\d,]*) بايت', t); m2 = re.search(r'(Buffer \d+)', t)
            if m: out.insert(0, [m.group(1) + ' B', '→ ' + (m2.group(1) if m2 else 'GPU'), 'bytes'])
            elif m2 and not out: out.append([m2.group(1), '', 'gpu'])
        elif kind == 'prn':
            out = [['cout', _short(t[len('اتطبع: '):] if t.startswith('اتطبع: ') else t, 22), 'text']] + out[:2]
        elif kind == 'cpu':
            m = re.search(r'([A-Za-z_][\w:~]*\(\))', t)
            if m: out = [[m.group(1), 'return' if 'خلصت' in t else 'call', 'fn']] + out
        elif kind in ('vao', 'prog', 'vs', 'fs'):
            m = re.search(r'((?:VAO|Program|Shader|Vertex Shader|Fragment Shader|Buffer|Texture) ?\d*)', t)
            if m and not out: out.append([m.group(1).strip(), '', 'gpu'])
    if 'النوع:' in dy:
        d2 = dy.split('النوع:', 1)[1].split('بعد السطر', 1)[0]
        for it in out:
            if it[2] in ('int', 'float', 'data', 'struct'):
                for k2, v2 in (('Pointer', 'ptr'), ('double', 'float'), ('float', 'float'), ('unsigned', 'uint'), ('GLuint', 'uint'), ('bool', 'bool'), ('char', 'text'), ('int', 'int'), ('class', 'struct'), ('struct', 'struct')):
                    if k2 in d2: it[2] = v2; break
                break
    order = {'bytes': 0, 'fn': 1, 'text': 2, 'gpu': 3, 'enum': 9}
    out.sort(key=lambda x: order.get(x[2], 5))
    return out[:6]

LEG = [('ram', 'بيانات في الرام'), ('buf', 'على الكارت (Buffer / Texture)'), ('vao', 'وصف أو نوع (VAO / struct / class)'), ('prg', 'كود بيشتغل (Shader / دالة)'), ('out', 'النتيجة (شاشة / Terminal)'), ('m1', 'خطوة بتتكرر'), ('m2', 'الرسم كل فريم'), ('ctl', 'إعداد وتحكم')]
def _legend(spec):
    used = {b['cls'] for b in spec['boxes'].values()}
    chips = ''.join(f'<span class="lg {c}"><i></i>{E(t)}</span>' for c, t in LEG if c in used)
    return f'<div class="lgd" aria-label="دليل الألوان">{chips}<span class="lg la"><i></i>سهم أزرق = بيانات</span><span class="lg lc"><i></i>متقطع = ترتيب التنفيذ</span></div>'

def _nav_html(p):
    files = p['files']; N = len(p['steps'])
    st = ','.join(f"{s.get('f', 0)}:{s['ln']}" for s in p['steps'])
    fsel = ('<select class="nf" aria-label="الملف">' + ''.join(f'<option value="{i}">{E(f["name"])}</option>' for i, f in enumerate(files)) + '</select>') if len(files) > 1 else ''
    pk = E(json.dumps([_packet(x) for x in p['steps']], ensure_ascii=False, separators=(',', ':')))
    return (f'<div class="nav2" data-pk="{pk}" data-steps="{st}" data-nl="{"|".join(str(len(f["lines"])) for f in files)}">'
            + (f'<div class="nrow nfile"><span class="nlab">📄 الملف</span>{fsel}</div>' if fsel else '') +
            '<div class="ngrp">' +
            ''.join(f'<div class="nrow"><span class="nlab">{lab}</span>'
                    f'<button type="button" class="nb" data-k="{k}" data-d="-1">السابق</button>'
                    f'<input class="ni" data-k="{k}" type="number" inputmode="numeric" min="1" max="{mx}" placeholder="1-{mx}" aria-label="{aria}">'
                    f'<button type="button" class="nb ngo" data-k="{k}" data-d="0">Go</button>'
                    f'<button type="button" class="nb" data-k="{k}" data-d="1">التالي</button></div>'
                    for k, lab, mx, aria in (('line', '📍 سطر', len(files[0]['lines']), 'رقم السطر'), ('step', '👣 خطوة', N, 'رقم الخطوة'))) +
            '</div>' +
            ('<div class="nrow nplay"><span class="nlab">🎬 شغّل</span><button type="button" class="nb npl" aria-pressed="false">▶ تشغيل</button>'
             '<span class="nspd"><span class="nsl">🐢</span><input class="nsp" type="range" min="-2" max="2" step="0.25" value="0" aria-label="السرعة"><span class="nsl">🐇</span><output class="nsv" dir="ltr">1×</output></span></div>' if N else '') +
            f'<div class="nmsg" aria-live="polite"></div></div>')

def prog_html(p, spec, warn):
    pid = p['id']; files = p['files']
    boxes = build(pid, spec, p, warn)
    svg = svg_for(pid, spec, p, warn)
    LS = {}
    for k, s in enumerate(p['steps'], 1): LS.setdefault((s.get('f', 0), s['ln']), []).append(k)
    vars_ = set()
    for s in p['steps']:
        for fr in s.get('st') or []:
            for v in fr.get('v') or []: vars_.add(v[0])
    codes = []
    for f, fl in enumerate(files):
        py = fl['name'].endswith('.py')
        rows = []
        for n, t in enumerate(fl['lines'], 1):
            ks = LS.get((f, n), [])
            cs = ('·'.join(map(str, ks[:2])) + ('+' if len(ks) > 2 else '')) if ks else ''
            title = ('خطوة ' + '، '.join(map(str, ks))) if ks else ''
            rows.append(f'<span class="cl" data-f="{f}" data-n="{n}"><span class="cn">{n}</span><span class="cs" title="{E(title)}">{cs}</span>{M.hl(t, py, vars_) or " "}</span>')
        codes.append(f'<div class="cf"><div class="cfn">📄 <bdi dir="ltr">{E(fl["name"])}</bdi> · عدد {len(fl["lines"])} سطر</div><pre class="src" dir="ltr"><code>{"".join(rows)}</code></pre></div>')
    det = []
    for b in boxes.values():
        ks = b['steps']
        info = ''.join(f'<li><b>خطوة {k}</b> · سطر {p["steps"][k - 1]["ln"]}: {E(p["steps"][k - 1].get("ti") or "")}{(" — " + E(re.sub("<[^>]+>", "", p["steps"][k - 1].get("ex") or ""))) if p["steps"][k - 1].get("ex") else ""}</li>' for k in ks[:12])
        more = f'<li>وعدد {len(ks) - 12} خطوة كمان (أرقامها: {E("، ".join(M.comp(ks[12:])))})</li>' if len(ks) > 12 else ''
        note = f'<p>{b["note"]}</p>' if b.get('note') else ''
        if ('$term' in b['lines'] or '$termnote' in b['lines']) and p.get('term'):
            tl = term_lines(p)
            note += f'<p>اللي اتطبع في الـ Terminal في التشغيل الحقيقي (عدد {len(tl)} سطر):</p><pre class="src" dir="ltr"><code>' + E(chr(10).join(tl)) + '</code></pre>'
        rs = ref_str(b)
        det.append(f'<details data-d="{b["id"]}"><summary><bdi dir="ltr">{E(b["title"])}</bdi><span class="sl">{("📄 " + E(files[b["f"]]["name"]) + " · ") if len(files) > 1 else ""}{("سطر " + E(rs)) if rs else "مالوش سطر"}</span></summary>'
                   f'<p><b>{E(b["ar"])}</b></p>{note}' + (f'<p class="dst">🧭 خطوات البنش: {E("، ".join(M.comp(ks)))}</p><ul>{info}{more}</ul>' if ks else '<p class="dst">مفيش خطوات بنش على السطور دي (تعريفات أو أقواس، أو حاجة بتحصل جوه الكارت).</p>') +
                   (f'<button type="button" class="goc" data-id="{b["id"]}">👁 وريني السطور دي في الكود</button>' if rs else '') + '</details>')
    return (f'<section class="prog" id="{pid.replace("_", "-")}" data-pid="{pid}"><details class="pd"><summary class="ph"><span class="pk">{E(p["kind"])}</span><b>{E(p["title"])}</b><span class="sl">عدد {sum(len(f["lines"]) for f in files)} سطر · عدد {len(p["steps"])} خطوة</span></summary>'
            f'<p class="desc">{E(re.sub("<[^>]+>", "", p.get("desc") or ""))}</p>'
            + _nav_html(p) +
            _legend(spec) + f'<div class="zbar" dir="ltr"><button type="button" class="zb" data-z="-1" aria-label="صغّر">−</button><span class="zv">100%</span><button type="button" class="zb" data-z="1" aria-label="كبّر">+</button><button type="button" class="zb zfit" data-z="0">⤢ كلها</button><button type="button" class="zb zamb" aria-pressed="false">⚡ تيار</button><span class="zh" dir="rtl">قرّب بصباعين، أو Ctrl + العجلة، أو دوس مرتين</span></div><div class="frame wide fit" dir="ltr">{svg}</div><p class="hint">دوس على أي صندوق يوديك على سطوره في الكود، ودوس على أي سطر يوديك على مكانه في الخريطة. الرقم الأحمر = رقم الخطوة في البنش. الأسهم الزرقا = البيانات رايحة فين، والمتقطعة الرمادي = ترتيب التنفيذ.</p>'
            f'<details class="notes"><summary>📝 شرح كل صندوق (عدد {len(boxes)})</summary>{"".join(det)}</details>'
            f'<details class="codebox"><summary>💻 الكود كله</summary><button type="button" class="back">⬆ ارجع للخريطة</button>{"".join(codes)}</details>'
            f'</details></section>'), boxes

CSS_EXTRA = '.eball{pointer-events:none;font-size:11px} .eball circle{filter:drop-shadow(0 0 3px currentColor);stroke:var(--paper);stroke-width:1.2} .eball text{paint-order:stroke;stroke:var(--paper);stroke-width:4px;stroke-linejoin:round} .enm{font:800 1em var(--mono)} .evl{font:600 .85em var(--mono);fill:var(--fg)} .etk{font:700 11px var(--mono);paint-order:stroke;stroke:var(--paper);stroke-width:4px;stroke-linejoin:round;pointer-events:none} .ety{font-weight:800;letter-spacing:.04em} .cur{fill:none;stroke-width:3;opacity:.8;stroke-dasharray:3 9;stroke-linecap:round;filter:drop-shadow(0 0 3px currentColor);animation:flow .5s linear infinite;pointer-events:none} @keyframes flow{to{stroke-dashoffset:-12}} .cur.tube{stroke-dasharray:none;opacity:.22;animation:none;stroke-linecap:round;filter:blur(1px)} .spk{fill:none;stroke-width:2.5;pointer-events:none} .blk.zap .bb{animation:zap .45s ease-out} @keyframes zap{0%{stroke-width:8;stroke:#fbbf24}100%{}} .ambient path.adat{stroke-dasharray:2 8;stroke-linecap:round;animation:flow 1.2s linear infinite} .zb.zamb[aria-pressed=true]{background:var(--gpu);color:var(--paper)} .pkt rect{fill:#fef3c7;stroke:#d97706;stroke-width:1.5} .pkt text{font:700 12px var(--mono);fill:#78350f} .pkt .pty{fill:#b45309;font-size:9.5px} .pkt.pop{opacity:0} .lgd{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:.76rem;color:var(--muted)} .lg{display:inline-flex;align-items:center;gap:5px} .lg i{width:13px;height:11px;border-radius:3px;border:2px solid;display:inline-block} .lg.ram i{background:var(--ramf);border-color:var(--ram)} .lg.buf i{background:var(--gpuf);border-color:var(--gpu)} .lg.vao i{background:var(--vaof);border-color:var(--vao)} .lg.prg i{background:var(--prgf);border-color:var(--prg)} .lg.out i{background:var(--outf);border-color:var(--out)} .lg.m1 i{background:var(--m1f);border-color:var(--m1)} .lg.m2 i{background:var(--m2f);border-color:var(--m2)} .lg.ctl i{background:var(--ctlf);border-color:var(--ctl);border-style:dashed} .lg.la i{height:0;border-width:2px 0 0;border-color:var(--gpu);border-radius:0} .lg.lc i{height:0;border-width:2px 0 0;border-color:var(--ctl);border-style:dashed;border-radius:0} .nspd{display:flex;align-items:center;gap:6px;flex:1;min-width:0} .nsp{flex:1;min-width:90px;max-width:320px;accent-color:var(--gpu);height:28px} .nsl{font-size:.9rem} .nsv{font:700 .82rem var(--mono);min-width:3.2em;text-align:center;color:var(--gpu)} .npl[aria-pressed=true]{background:var(--gpu);color:var(--paper)} .adat.aglow{stroke:#f59e0b;stroke-width:4;filter:drop-shadow(0 0 4px #f59e0b)} .compact .bl,.compact .ln,.compact .stp,.compact .ba,.compact .al{display:none} .frame.wide.fit svg{min-width:0!important} .zbar{display:flex;align-items:center;gap:6px;flex-wrap:wrap} .zb{font:700 1rem var(--sans);min-width:2.2em;padding:2px 8px;border-radius:8px;border:1px solid var(--gpu);background:var(--paper);color:var(--gpu);cursor:pointer} .zb.zfit{font-size:.8rem;font-weight:600} .zv{font:600 .8rem var(--mono);min-width:3.4em;text-align:center} .zh{font-size:.75rem;color:var(--muted)} .frame.fit{touch-action:pan-x pan-y;overscroll-behavior:contain} .frame.fit svg{transition:none} .blk.glow .bb{stroke:#f59e0b;stroke-width:3.5} .blk.glow{filter:drop-shadow(0 0 3px #f59e0b) drop-shadow(0 0 9px #f59e0b)} @media (prefers-reduced-motion: no-preference){.blk.glow{animation:glw 1.2s ease-in-out 3}} @keyframes glw{50%{filter:drop-shadow(0 0 6px #fbbf24) drop-shadow(0 0 16px #fbbf24)}} .nav2{display:grid;gap:8px;padding:8px 8px;border:1px solid var(--rule);border-radius:10px;background:var(--bg)} .ngrp{display:flex;flex-wrap:wrap;gap:8px 18px} .nrow{display:flex;flex-wrap:nowrap;align-items:center;gap:9px} .nplay{flex-wrap:wrap;row-gap:6px} .nplay .nspd{flex-basis:100%} @media (max-width:350px){.nrow{gap:6px}}  .nlab{font-weight:700;font-size:.82rem;white-space:nowrap} .nb{font:inherit;font-size:.8rem;padding:3px 6px;white-space:nowrap;border-radius:999px;border:1px solid var(--gpu);background:var(--paper);color:var(--gpu);cursor:pointer} .nb:hover{background:var(--gpuf)} .nb.ngo{background:var(--gpu);color:var(--paper);font-weight:700} .nb.ngo:hover{opacity:.85} .ni{font:600 .9rem var(--mono);width:3.5em;padding-inline:4px!important;padding:4px 8px;border:1px solid var(--rule);border-radius:8px;background:var(--paper);color:var(--fg);text-align:center} .nf{font:inherit;font-size:.82rem;padding:3px 6px;border:1px solid var(--rule);border-radius:8px;background:var(--paper);color:var(--fg)} .nmax{font-size:.8rem;color:var(--muted)} .nmsg{margin:0;font-size:.88rem;min-height:1.4em} .nmsg .ncode{display:block;margin-top:4px;padding:4px 8px;border-radius:6px;background:var(--code);color:var(--so);font:.82rem var(--mono);white-space:pre-wrap;overflow-wrap:anywhere;text-align:left} .days{display:grid;gap:6px} .days details.wk{padding:2px 12px} .days details.wk summary{font-size:.9rem;padding-block:4px} .wkl{display:flex;flex-wrap:wrap;gap:6px;padding:2px 0 8px} .frame.wide svg{min-width:1500px} .bl.tm{fill:var(--fg)}'

def page(day, progs, specs, warn, extra=''):
    title = 'خرائط ' + M.DAYN[day]
    def wk_links(w):
        ds = range(1, 8) if w == 2 else range(8, 15)
        return ''.join(f'<a href="day{d}.html" class="{"on" if d == day else ""}">اليوم {d if w == 2 else d - 7}</a>' for d in ds)
    nav = ''.join(f'<details class="wk"{" open" if (day >= 8) == (w == 3) else ""}><summary>الأسبوع {w}</summary><div class="wkl">{wk_links(w)}</div></details>' for w in (2, 3))
    body = []
    for p in progs:
        sp = specs.get(p['id'])
        if not sp: warn.append(f'NO SPEC {p["id"]}'); continue
        h, _ = prog_html(p, sp, warn); body.append(h)
    toc = ''.join(f'<a href="#{p["id"].replace("_", "-")}" class="tc"><span class="pk">{E(p["kind"])}</span>{E(p["title"])}</a>' for p in progs)
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover"><title>{E(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>{M.CSS}{CSS_EXTRA}</style></head><body><main>
<nav class="days">{nav}</nav>
<h1>🗺 {E(title)}</h1>
<p class="lede">لكل برنامج في {E(M.DAYN[day])} خريطة بنفس طريقة خريطة كود اليوم 7: البرنامج متقسم مناطق (الرام، الكارت، الشاشة أو الـ Terminal، اللوب، الدوال المساعدة)، والأسهم الزرقا بتوضح البيانات بتروح فين. جنب كل صندوق أرقام سطوره، والأرقام الحمرا خطوات التشغيل الحقيقي في البنش. افتح أي برنامج تحت.</p>
<div class="toc">{toc}</div>
{extra}
{"".join(body)}
<p class="found" id="found" hidden></p>
</main><script>{M.JS}</script></body></html>'''

if __name__ == '__main__':
    days = [int(a) for a in sys.argv[1:]] or list(range(1, 15))
    warn = []; counts = []
    for d in range(1, 15):
        progs = json.load(open(M.DATA % d))['programs']; counts.append((d, len(progs)))
        if d not in days: continue
        sp_path = f'/home/claude/maps/specs/d{d}.txt'
        specs = parse(sp_path) if os.path.exists(sp_path) else {}
        extra = '<p class="note">⭐ لبرنامج «تجربة حرة: الطريقتين جنب بعض» فيه كمان الخريطة الأصلية المفصّلة اللي اتعملت الأول: <a href="https://claude.ai/artifact/AikUx1b9Gx3VPTVrYhsREp" target="_blank" rel="noopener">خريطة كود اليوم 7 ↗</a></p>' if d == 7 else ''
        open(f'/home/claude/maps/out2/day{d}.html', 'w').write(page(d, progs, specs, warn, extra))
        print('day', d, os.path.getsize(f'/home/claude/maps/out2/day{d}.html'))
    def wk_cards(w):
        ds = [(d, n) for d, n in counts if (d >= 8) == (w == 3)]
        cards = ''.join(f'<a class="dcard" href="day{d}.html"><b>اليوم {d if w == 2 else d - 7}</b><span>عدد {n} برامج</span></a>' for d, n in ds)
        return f'<details class="wkc" open><summary>الأسبوع {w} <span class="sl">عدد {len(ds)} أيام · عدد {sum(n for _, n in ds)} برنامج</span></summary><div class="dgrid">{cards}</div></details>'
    idx = M.index_page(counts)
    idx = re.sub(r'<div class="dgrid">.*?</div></main>', lambda m_: wk_cards(2) + wk_cards(3) + '</main>', idx, flags=re.S)
    idx = idx.replace('</style>', '.wkc{padding:4px 14px 14px} .wkc summary{font-size:1.05rem}</style>', 1)
    idx = idx.replace('خريطة لكل برنامج في البنش', 'خريطة لكل برنامج في البنش بنفس طريقة خريطة كود اليوم 7')
    open('/home/claude/maps/out2/index.html', 'w').write(idx)
    for w_ in warn: print('WARN', w_)
