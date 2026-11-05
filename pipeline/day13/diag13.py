# Week 3 Day 6 diagrams (English labels inside the SVG; Arabic captions in HTML). All numbers from the real runs.
import sys, math
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, GREEN, RED, PINK


def p_books():
    """The Cherno's pile of books: each scope = a book on top; leaving the scope removes it with its objects"""
    b = text(320, 22, 'the stack = a pile of books (one book per scope)', INK, 'middle', 12.5, True)
    books = [('main: Entity a', TEAL, 'lives to the end of main'), ('{ } : Entity b', BLUE, 'Destroyed b at its }'), ('if : Entity c', BLUE, 'Destroyed c at its }'), ('for : Entity d0, d1', BLUE, 'a new book every loop')]
    for i, (t, c, note) in enumerate(books):
        y = 200 - i * 40
        b += box(120, y, 220, 34, t, '#ecfdf5' if i == 0 else '#dbeafe', c, True, fs=12)
        b += text(356, y + 22, note, GRAY, 'start', 11)
    b += box(120, 40, 220, 34, '{ } : Entity* h  (8 bytes)', '#dbeafe', BLUE, True, fs=12)
    b += line(340, 57, 470, 57, ORANGE) + box(470, 40, 150, 34, 'HEAP: Entity heap', '#ffedd5', ORANGE, True, fs=11.5)
    b += text(545, 92, 'never destroyed', RED, 'middle', 11, True)
    b += text(230, 252, 'only the top book can be removed', GRAY, 'middle', 11)
    return svg(264, b, (ORANGE,))


def p_scoped():
    """ScopedPtr on the stack holds the heap pointer; its destructor deletes it"""
    b = text(160, 22, 'STACK', TEAL, 'middle', 12, True) + text(480, 22, 'HEAP', ORANGE, 'middle', 12, True)
    b += box(60, 50, 200, 50, 'ScopedPtr e  (8 bytes)', '#ecfdf5', TEAL, True, fs=12) + text(160, 118, 'm_Ptr', GRAY, 'middle', 10.5)
    b += line(260, 75, 400, 75, ORANGE) + box(400, 50, 160, 50, 'Entity', '#ffedd5', ORANGE, True)
    b += text(320, 150, 'at the } :  ~ScopedPtr()  ->  delete m_Ptr  ->  ~Entity()', INK, 'middle', 12, True)
    b += text(320, 176, 'output: Destroyed Entity, then "after the scope"', GREEN, 'middle', 11.5)
    b += text(320, 202, 'std::unique_ptr does the same, and refuses to be copied', PURPLE, 'middle', 11.5)
    return svg(216, b, (ORANGE,))


def t_flip():
    """letter.png rows in memory with and without flip; OpenGL's (0, 0) is bottom-left"""
    G = [['W'] * 8 for _ in range(8)]
    b = ''
    cols = {'W': '#f5f5f0', 'R': '#dc2626', 'G': '#16a34a'}
    for k, (title, first) in enumerate([('flip = 0: first byte = top-left', 'white (245, 245, 240)'), ('flip = 1: first byte = bottom-left', 'red (220, 38, 38)')]):
        ox = 40 + k * 320
        b += text(ox + 120, 22, title, INK, 'middle', 12, True)
        for r in range(8):
            y = 40 + r * 18
            row_img = r if k == 0 else 7 - r
            for c in range(8):
                col = 'W'
                if row_img == 0 and c == 7: col = 'G'
                if row_img == 7 and c == 0: col = 'R'
                b += f'<rect x="{ox + c * 18}" y="{y}" width="17" height="17" fill="{cols[col]}" stroke="#cbd5e1" stroke-width="0.5"/>'
            b += text(ox + 152, y + 13, f'row {r}', GRAY, 'start', 9.5)
        b += text(ox + 120, 200, 'memory row 0 is drawn at v = 0 (bottom)', GRAY, 'middle', 10.5)
        b += text(ox + 120, 218, first, RED if k else GRAY, 'middle', 11, True)
    return svg(232, b, (BLUE,))


def t_atlas():
    """4 x 4 atlas, cell 5 -> u 0.25..0.5, v 0.25..0.5"""
    b = text(150, 22, 'atlas 64 x 64 = 4 x 4 cells', INK, 'middle', 12, True)
    for r in range(4):
        for c in range(4):
            cell = r * 4 + c
            y = 200 - (r + 1) * 40
            f = '#fde68a' if cell in (0, 5, 10, 15) else '#f1f5f9'
            b += box(70 + c * 40, y, 38, 38, str(cell), f, '#94a3b8', cell in (0, 5, 10, 15), fs=12)
    for i, t in enumerate(['0', '0.25', '0.5', '0.75', '1']):
        b += text(70 + i * 40, 216, t, GRAY, 'middle', 10) + text(60, 204 - i * 40, t, GRAY, 'end', 10)
    b += text(150, 234, 'u', BLUE, 'middle', 11, True) + text(30, 120, 'v', BLUE, 'middle', 11, True)
    x = 340
    for i, t in enumerate(['cell 5 = column 1, row 1', 'u0 = 1 / 4 = 0.25,  u1 = 0.5', 'v0 = 1 / 4 = 0.25,  v1 = 0.5', '5 quads, 1 texture, 1 draw call', '320 bytes of vertices + 120 of indices']):
        b += text(x, 70 + i * 28, t, INK if i < 3 else TEAL, 'start', 12, i == 0)
    return svg(246, b, (BLUE,))


def m_compose():
    """(1, 1): scale then rotate = (-1, 2); rotate then scale = (-2, 1)"""
    def P(x, y, ox): return ox + x * 40, 140 - y * 40
    b = ''
    for k, (title, mid, end, col) in enumerate([('R @ (S @ p): scale, then rotate', (2, 1), (-1, 2), ORANGE), ('S @ (R @ p): rotate, then scale', (-1, 1), (-2, 1), PURPLE)]):
        ox = 160 + k * 320
        b += text(ox, 22, title, col, 'middle', 12, True)
        b += f'<line x1="{ox - 120}" y1="140" x2="{ox + 120}" y2="140" stroke="#cbd5e1"/><line x1="{ox}" y1="30" x2="{ox}" y2="200" stroke="#cbd5e1"/>'
        for (x, y), lab, c in [((1, 1), 'p (1, 1)', GRAY), (mid, f'{mid}', col), (end, f'{end}', col)]:
            px, py = P(x, y, ox)
            b += f'<circle cx="{px}" cy="{py}" r="5" fill="{c}"/>' + text(px + 8, py - 8, lab.replace(' ', ''), c, 'start', 11, True)
        (x1, y1), (x2, y2), (x3, y3) = P(1, 1, ox), P(*mid, ox), P(*end, ox)
        b += line(x1, y1, x2, y2, col, 1.6, True, True) + line(x2, y2, x3, y3, col, 1.6, True, True)
    b += text(320, 222, 'R @ S != S @ R : the order of transformations matters', RED, 'middle', 12, True)
    return svg(236, b, (ORANGE, PURPLE))


def m_proj():
    """projection of (2, 3) on the line through (2, 1)"""
    def P(x, y): return 120 + x * 50, 200 - y * 50
    b = ''
    x0, y0 = P(-0.4, -0.2); x1, y1 = P(4, 2)
    b += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{TEAL}" stroke-width="2"/>' + text(x1 + 4, y1, 'line L (through u = (2, 1))', TEAL, 'start', 11, True)
    ox, oy = P(0, 0); xx, xy = P(2, 3); px, py = P(2.8, 1.4)
    b += line(ox, oy, xx, xy, BLUE, 2) + text(xx + 6, xy, 'x = (2, 3)', BLUE, 'start', 11.5, True)
    b += line(ox, oy, px, py, ORANGE, 2.5) + text(px + 8, py + 16, 'proj = (2.8, 1.4)', ORANGE, 'start', 11.5, True)
    b += f'<line x1="{xx}" y1="{xy}" x2="{px}" y2="{py}" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5 4"/>' + text((xx + px) / 2 + 8, (xy + py) / 2 - 18, 'x - proj = (-0.8, 1.6), at 90 degrees', RED, 'start', 10.5)
    b += text(470, 236, 'P = u u^T / 5 = [[0.8, 0.4], [0.4, 0.2]]', INK, 'middle', 11.5, True)
    return svg(250, b, (BLUE, ORANGE))


def c_csg():
    """sphere A and box B from the program, and the three results (2D slice z = 0)"""
    b = ''
    ops = [('A union B', lambda a, bb: a or bb), ('A inter B', lambda a, bb: a and bb), ('A minus B', lambda a, bb: a and not bb)]
    for k, (name, f) in enumerate(ops):
        ox, oy, s = 40 + k * 205, 40, 44
        b += text(ox + 80, 24, name, [BLUE, TEAL, PURPLE][k], 'middle', 12, True)
        n = 46
        for i in range(n):
            for j in range(n):
                x = -1.6 + 3.8 * (i + 0.5) / n; y = 1.2 - 2.4 * (j + 0.5) / n
                a = x * x + y * y <= 1; bb = 0 <= x <= 2 and -0.5 <= y <= 0.5
                if f(a, bb):
                    b += f'<rect x="{ox + (x + 1.6) * s:.1f}" y="{oy + (1.2 - y) * s:.1f}" width="{3.8 * s / n + 0.4:.1f}" height="{2.4 * s / n + 0.4:.1f}" fill="{[BLUE, TEAL, PURPLE][k]}" fill-opacity="0.55"/>'
        b += f'<circle cx="{ox + 1.6 * s}" cy="{oy + 1.2 * s}" r="{s}" fill="none" stroke="{GRAY}" stroke-dasharray="3 3"/>'
        b += f'<rect x="{ox + 1.6 * s}" y="{oy + 0.7 * s}" width="{2 * s}" height="{s}" fill="none" stroke="{GRAY}" stroke-dasharray="3 3"/>'
    b += text(320, 168, 'slice at z = 0. dashed: sphere A (r = 1) and box B (x 0..2, y -0.5..0.5)', GRAY, 'middle', 11)
    b += text(320, 190, 'set operations: || (union), && (intersect), && ! (difference)', INK, 'middle', 12, True)
    return svg(202, b, (BLUE,))


def c_reg():
    """1D: A [0,2], C [2,4] touching -> [2,2] -> regularized: nothing"""
    def X(v): return 80 + v * 100
    b = ''
    rows = [('A', 0, 2, BLUE), ('C', 2, 4, TEAL)]
    for i, (n, a, c, col) in enumerate(rows):
        y = 40 + i * 32
        b += text(50, y + 5, n, col, 'middle', 12, True) + f'<line x1="{X(a)}" y1="{y}" x2="{X(c)}" y2="{y}" stroke="{col}" stroke-width="8" stroke-linecap="butt"/>'
    for v in range(5):
        b += text(X(v), 120, str(v), GRAY, 'middle', 10)
    b += f'<circle cx="{X(2)}" cy="150" r="5" fill="{RED}"/>' + text(X(2) + 12, 154, 'A inter C = [2, 2]: length 0 (a point; in 3D a face with no volume)', RED, 'start', 11.5, True)
    b += text(X(2) + 12, 182, 'regularized: removed -> 0 pieces', GREEN, 'start', 11.5, True)
    return svg(196, b, (BLUE,))
