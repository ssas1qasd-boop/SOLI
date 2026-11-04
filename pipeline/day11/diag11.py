# Week 3 Day 4 diagrams (English labels inside the SVG; Arabic captions in HTML). All numbers from the real runs.
import sys, math, re
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, GREEN, RED, PINK

P1 = open('/home/claude/day11/src/p1_stack_heap.txt').read()
ADDR = dict(re.findall(r'(&?\w+) = (0x[0-9a-f]+)', P1))


def p_mem():
    """stack block (adjacent, 0x7ff...) vs heap blocks (32 bytes apart, 0x5...) from the real run"""
    b = text(160, 20, 'STACK (0x7ff...)', TEAL, 'middle', 13, True) + text(480, 20, 'HEAP (0x5...)', ORANGE, 'middle', 13, True)
    b += '<rect x="20" y="32" width="280" height="196" rx="10" fill="#ecfdf5" stroke="#0d9488"/>'
    b += '<rect x="340" y="32" width="280" height="196" rx="10" fill="#fff7ed" stroke="#c2410c"/>'
    rows = [('&value', 'int value = 5', '4 B'), ('&vector', 'Vector3 vector  (10, 11, 12)', '12 B'), ('array', 'int array[5]  (2 2 2 2 2)', '20 B')]
    for i, (k, lab, sz) in enumerate(rows):
        y = 44 + i * 58
        b += box(32, y, 256, 44, '', '#fff', TEAL)
        b += text(160, y + 18, lab, INK, 'middle', 11.5, True) + text(160, y + 35, ADDR.get(k, '') + '   ' + sz, GRAY, 'middle', 10.5)
    b += text(160, 220, 'array - &vector = 12 = sizeof(Vector3)', TEAL, 'middle', 11, True)
    hrows = [('hvalue', 'new int  (5)', '4 B used'), ('harray', 'new int[5]', '20 B used'), ('hvector', 'new Vector3()', '12 B used')]
    for i, (k, lab, sz) in enumerate(hrows):
        y = 44 + i * 58
        b += box(352, y, 256, 44, '', '#fff', ORANGE)
        b += f'<rect x="352" y="{y}" width="{256 * (4 if i == 0 else 20 if i == 1 else 12) / 32:.0f}" height="44" rx="6" fill="#fed7aa" opacity="0.7"/>'
        b += text(480, y + 18, lab, INK, 'middle', 11.5, True) + text(480, y + 35, ADDR.get(k, '') + '   ' + sz + ' of 32', GRAY, 'middle', 10.5)
    b += text(480, 220, 'each block starts 32 bytes after the last', ORANGE, 'middle', 11, True)
    b += text(320, 250, 'stack: move the stack pointer   |   heap: malloc searches the free list and keeps notes', INK, 'middle', 11)
    return svg(262, b, (TEAL, ORANGE))


def t_wrap():
    """u from -1 to 2 -> what each mode gives (graphs of the 3 formulas)"""
    b = ''
    modes = [('REPEAT: u - floor(u)', lambda u: u - math.floor(u), BLUE), ('MIRRORED: 1 - |mod(u, 2) - 1|', lambda u: 1 - abs((u % 2.0) - 1), TEAL),
             ('CLAMP: clamp(u, 0, 1)', lambda u: min(max(u, 0), 1), ORANGE)]
    for k, (name, fn, col) in enumerate(modes):
        x0, y0, w, h = 24 + k * 206, 50, 186, 120
        b += text(x0 + w / 2, 30, name, col, 'middle', 11, True)
        b += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#f8fafc" stroke="#cbd5e1"/>'
        b += f'<rect x="{x0 + w / 3}" y="{y0}" width="{w / 3}" height="{h}" fill="#eef2ff"/>'
        pts = []
        for i in range(301):
            u = -1 + 3 * i / 300
            pts.append(f'{x0 + (u + 1) / 3 * w:.1f},{y0 + h - fn(u) * h:.1f}')
        b += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.5"/>'
        for u in (-1, 0, 1, 2):
            b += text(x0 + (u + 1) / 3 * w, y0 + h + 16, str(u), GRAY, 'middle', 10)
        b += text(x0 - 6, y0 + 4, '1', GRAY, 'end', 10) + text(x0 - 6, y0 + h + 2, '0', GRAY, 'end', 10)
        b += text(x0 + w / 2, y0 + h + 32, 'u in  ->  u used in the image', GRAY, 'middle', 10)
    b += text(320, 226, 'blue band = the real image (0..1). Our rectangle goes from -1 to 2: 3 copies.', INK, 'middle', 11)
    return svg(240, b, (BLUE,))


def m_add():
    """Khan's example: A + B element by element"""
    A = [[1, -7, 5], [0, 3, -10]]; B = [[5, 0, 3], [11, -1, 7]]; C = [[A[i][j] + B[i][j] for j in range(3)] for i in range(2)]
    b = ''
    def mat(x, M, col, fill, hl=None):
        s = ''
        for i in range(2):
            for j in range(3):
                f = '#fde68a' if hl == (i, j) else fill
                s += box(x + j * 46, 40 + i * 40, 42, 34, str(M[i][j]), f, col, True, fs=13)
        return s
    b += mat(20, A, BLUE, '#dbeafe', (0, 0)) + text(176, 82, '+', INK, 'middle', 22, True)
    b += mat(196, B, TEAL, '#ccfbf1', (0, 0)) + text(352, 82, '=', INK, 'middle', 22, True)
    b += mat(372, C, ORANGE, '#ffedd5', (0, 0))
    b += text(84, 30, 'A (2 x 3)', BLUE, 'middle', 11.5, True) + text(260, 30, 'B (2 x 3)', TEAL, 'middle', 11.5, True) + text(436, 30, 'A + B (2 x 3)', ORANGE, 'middle', 11.5, True)
    b += text(560, 66, '1 + 5 = 6', INK, 'middle', 12, True) + text(560, 88, '-10 + 7 = -3', INK, 'middle', 12)
    b += text(320, 146, 'same place + same place.  3 x 2 + 2 x 2 = undefined (some cells have no partner)', RED, 'middle', 11.5)
    return svg(160, b, (BLUE,))


def c_obj():
    """the cube from the OBJ file: vertex numbers, and the bottom face order 1 4 3 2 -> normal down"""
    P = {1: (1, -1, 0), 2: (1, 1, 0), 3: (-1, 1, 0), 4: (-1, -1, 0), 5: (1, -1, 2), 6: (1, 1, 2), 7: (-1, 1, 2), 8: (-1, -1, 2)}
    def pr(p):
        x, y, z = p
        return 160 + x * 70 + y * 38, 190 - z * 60 - y * 26
    b = ''
    for a, c in [(1, 2), (2, 3), (3, 4), (4, 1), (5, 6), (6, 7), (7, 8), (8, 5), (1, 5), (2, 6), (3, 7), (4, 8)]:
        (x1, y1), (x2, y2) = pr(P[a]), pr(P[c])
        dash = ' stroke-dasharray="5 4"' if 3 in (a, c) else ''
        b += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GRAY}" stroke-width="1.8"{dash}/>'
    for k, p in P.items():
        x, y = pr(p)
        b += f'<circle cx="{x}" cy="{y}" r="4" fill="{PURPLE}"/>' + text(x + (12 if p[0] > 0 else -12), y + 4, str(k), PURPLE, 'middle', 12, True)
    cx, cy = pr((0, 0, 0))
    b += line(cx, cy, cx, cy + 46, RED, 2.5) + text(cx + 10, cy + 44, 'normal of f 1 4 3 2: (0, 0, -4)', RED, 'start', 11, True)
    x = 360
    for i, (t, c) in enumerate([('cube.obj (written by the program):', INK), ('v 1 -1 0   ... 8 lines "v x y z"', GRAY), ('f 1 4 3 2   bottom  -> (0, 0, -4) outward', TEAL),
                                ('f 5 6 7 8   top     -> (0, 0, 4) outward', TEAL), ('f 1 2 6 5   x = 1   -> (4, 0, 0) outward', TEAL),
                                ('6 faces outward, V - E + F = 8 - 12 + 6 = 2', INK), ('f 1 2 3 4 for the bottom -> INWARD', RED)]):
        b += text(x, 40 + i * 26, t, c, 'start', 11.5, c != GRAY)
    return svg(250, b, (RED,))


def c_mesh():
    """true circle vs the 8-gon: the chord height is the error"""
    b = text(150, 22, 'n = 8: the mesh is an octagon', INK, 'middle', 12, True)
    cx, cy, r = 150, 140, 100
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{PURPLE}" stroke-width="2.5"/>'
    pts = ' '.join(f'{cx + r * math.cos(2 * math.pi * i / 8):.1f},{cy - r * math.sin(2 * math.pi * i / 8):.1f}' for i in range(8))
    b += f'<polygon points="{pts}" fill="#fff7ed" fill-opacity="0.6" stroke="{ORANGE}" stroke-width="2"/>'
    mx, my = cx + r * math.cos(math.pi / 8) * math.cos(math.pi / 8), cy - r * math.cos(math.pi / 8) * math.sin(math.pi / 8)
    ex, ey = cx + r * math.cos(math.pi / 8), cy - r * math.sin(math.pi / 8)
    b += f'<line x1="{mx:.1f}" y1="{my:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{RED}" stroke-width="3"/>'
    b += text(ex + 8, ey + 4, 'error', RED, 'start', 11, True)
    b += text(150, 262, 'purple = B-Rep (exact),  orange = mesh', GRAY, 'middle', 10.5)
    x = 320
    rows = [('n', 'triangles', 'bytes', 'max error'), ('8', '28', '528', '0.0761'), ('32', '124', '2256', '0.00482'), ('128', '508', '9168', '0.000301'), ('512', '2044', '36816', '0.0000188')]
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            b += text(x + 10 + j * 76, 52 + i * 28, v, INK if i else GRAY, 'start', 12, i == 0)
    b += text(x + 150, 206, 'error = R (1 - cos(pi / n)),  R = 1', ORANGE, 'middle', 11.5, True)
    b += text(x + 150, 232, 'R = 50 mm, 0.01 mm  ->  n = 256, 1020 triangles', PURPLE, 'middle', 11.5, True)
    return svg(274, b, (RED,))
