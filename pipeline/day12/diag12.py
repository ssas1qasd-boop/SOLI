# Week 3 Day 5 diagrams (English labels inside the SVG; Arabic captions in HTML). All numbers from the real runs.
import sys, math
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, GREEN, RED, PINK


def p_new():
    """new = malloc + constructor; new Entity[3] = 8 + 3 x 32 = 104"""
    b = text(110, 24, 'new Entity()', BLUE, 'middle', 13, True) + text(320, 24, 'malloc(sizeof(Entity))', ORANGE, 'middle', 13, True) + text(530, 24, 'new (b) Vector3(1, 2, 3)', PURPLE, 'middle', 13, True)
    b += box(30, 40, 160, 34, '1. malloc(32)', '#dbeafe', BLUE, True) + line(110, 74, 110, 92, BLUE) + box(30, 94, 160, 34, '2. Entity()  name = Unknown', '#dbeafe', BLUE, True, fs=11.5)
    b += box(240, 40, 160, 34, '1. malloc(32)', '#ffedd5', ORANGE, True) + box(240, 94, 160, 34, 'no constructor', '#fff', ORANGE, False, True, RED, 12)
    b += box(450, 40, 160, 34, 'no allocation: use b', '#fff', PURPLE, False, True, PURPLE, 11.5) + line(530, 74, 530, 92, PURPLE) + box(450, 94, 160, 34, 'Vector3(1, 2, 3) at b', '#ede9fe', PURPLE, True, fs=11.5)
    b += text(110, 146, 'free with: delete', BLUE, 'middle', 11) + text(320, 146, 'free with: free', ORANGE, 'middle', 11) + text(530, 146, 'free with: v->~Vector3() only', PURPLE, 'middle', 11)
    b += text(320, 180, 'new Entity[3] asked for 104 bytes:', INK, 'middle', 12, True)
    b += box(110, 192, 60, 34, '8: count 3', '#fde68a', ORANGE, True, fs=10.5)
    for i in range(3):
        b += box(172 + i * 120, 192, 116, 34, f'Entity {i}  (32)', '#dbeafe', BLUE, True, fs=11)
    b += line(172, 246, 172, 228, BLUE) + text(172, 260, 'the pointer you get', BLUE, 'middle', 10.5)
    b += text(470, 256, 'delete[] reads the 3, runs 3 destructors', GRAY, 'middle', 10.5)
    return svg(272, b, (BLUE, PURPLE))


def t_mip():
    """the 9 levels (sizes from the run) and the colors we gave them"""
    cols = ['#dc2626', '#ea580c', '#eab308', '#16a34a', '#0d9488', '#2563eb', '#7c3aed', '#db2777', '#ffffff']
    b = text(320, 22, 'mip levels: each one half the size of the one before', INK, 'middle', 12.5, True)
    x = 20
    for lv in range(9):
        w = 256 >> lv
        s = max(4, w * 0.62)
        b += f'<rect x="{x}" y="{200 - s}" width="{s}" height="{s}" fill="{cols[lv]}" stroke="#334155" stroke-width="1"/>'
        b += text(x + s / 2, 218, str(lv), INK, 'middle', 11, True) + text(x + s / 2, 234, f'{w}', GRAY, 'middle', 10)
        x += s + (14 if lv < 4 else 18)
    b += text(320, 258, 'all levels = 262,143 bytes = 1.333 x level 0 (196,608)', ORANGE, 'middle', 12, True)
    return svg(270, b, (BLUE,))


def t_aniso():
    """a far pixel covers a long thin strip of the texture: mipmap picks by the long side, aniso samples along it"""
    b = text(160, 22, 'one far pixel on the floor', INK, 'middle', 12, True) + text(480, 22, 'what it covers in the texture', INK, 'middle', 12, True)
    b += '<polygon points="60,200 260,200 190,60 130,60" fill="#f1f5f9" stroke="#94a3b8"/>'
    b += '<rect x="154" y="70" width="12" height="12" fill="#fde68a" stroke="#c2410c" stroke-width="2"/>' + text(176, 80, 'pixel', ORANGE, 'start', 10.5, True)
    b += f'<rect x="360" y="110" width="240" height="30" fill="#fde68a" stroke="#c2410c" stroke-width="2"/>'
    b += text(480, 104, 'about 16 texels long, 1 wide', ORANGE, 'middle', 11, True)
    b += text(480, 170, 'mipmap only: picks a level by the LONG side', GRAY, 'middle', 11)
    b += text(480, 188, '-> too small a level -> grey blur', RED, 'middle', 11, True)
    for i in range(8):
        b += f'<circle cx="{375 + i * 30}" cy="125" r="4" fill="{TEAL}"/>'
    b += text(480, 214, 'anisotropic (16): up to 16 samples along it', TEAL, 'middle', 11, True)
    b += text(480, 232, '-> sharper far away', TEAL, 'middle', 11, True)
    return svg(246, b, (BLUE,))


def m_slice():
    """Keith's 2 x 7 matrix with m[1, 5], m[:, 2] and m[0, 1:6:2] highlighted"""
    M = [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14]]
    b = text(320, 22, 'm (2 x 7)', INK, 'middle', 12, True)
    for i in range(2):
        for j in range(7):
            f = '#fde68a' if (i, j) == (1, 5) else '#ccfbf1' if j == 2 else '#dbeafe' if (i == 0 and j in (1, 3, 5)) else '#fff'
            b += box(150 + j * 50, 40 + i * 44, 46, 38, str(M[i][j]), f, '#94a3b8', True, fs=13)
    for j in range(7):
        b += text(173 + j * 50, 142, str(j), GRAY, 'middle', 10)
    b += text(130, 64, '0', GRAY, 'end', 10) + text(130, 108, '1', GRAY, 'end', 10)
    b += text(110, 170, 'yellow: m[1, 5] = 13', ORANGE, 'start', 11.5, True) + text(280, 170, 'teal: m[:, 2] = [3 10]', TEAL, 'start', 11.5, True)
    b += text(450, 170, 'blue: m[0, 1:6:2] = [2 4 6]', BLUE, 'start', 11.5, True)
    return svg(184, b, (BLUE,))


def c_three():
    """the same cube three ways: edges / faces / inside"""
    def pr(p, ox):
        x, y, z = p
        return ox + x * 46 + y * 22, 130 - z * 46 - y * 14
    V = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
    E = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    F = [(0, 1, 5, 4), (1, 2, 6, 5), (4, 5, 6, 7)]
    b = ''
    for k, (name, col, ox) in enumerate([('wireframe: 12 edges', BLUE, 110), ('surface: 6 faces', TEAL, 320), ('solid: 6 half-spaces', PURPLE, 530)]):
        b += text(ox, 22, name, col, 'middle', 12, True)
        if k >= 1:
            for f in F:
                pts = ' '.join('%.1f,%.1f' % pr(V[i], ox) for i in f)
                b += f'<polygon points="{pts}" fill="{"#ccfbf1" if k == 1 else "#ddd6fe"}" fill-opacity="{0.55 if k == 1 else 0.95}" stroke="none"/>'
        for a, c in E:
            (x1, y1), (x2, y2) = pr(V[a], ox), pr(V[c], ox)
            b += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="1.8"/>'
    b += text(110, 214, 'length 24', INK, 'middle', 11.5, True) + text(110, 232, 'area ?  volume ?', RED, 'middle', 11.5)
    b += text(320, 214, 'length 24, area 24', INK, 'middle', 11.5, True) + text(320, 232, 'volume ?', RED, 'middle', 11.5)
    b += text(530, 214, 'area 24, volume 8', INK, 'middle', 11.5, True) + text(530, 232, '(0,0,0) inside, (1.5,0,0) outside', GREEN, 'middle', 11)
    return svg(246, b, (BLUE,))


def c_param():
    """Dr. Patil's table: which of R, theta, H are free -> point / curve / surface / solid"""
    rows = [('point', 'R = 10, theta = pi, H = 25', '0', '1'), ('circle', 'theta free', '1', '3'), ('cylinder', 'theta, H free', '2', '9'),
            ('disk', 'R, theta free', '2', '9'), ('solid cyl.', 'R, theta, H free', '3', '27'), ('hollow', 'R 5..10, theta, H free', '3', '27')]
    b = ''
    hd = [('shape', 40), ('what changes', 160), ('free params', 400), ('sample points (n = 3)', 500)]
    for t, x in hd:
        b += text(x, 26, t, GRAY, 'start', 11, True)
    colr = {'0': GRAY, '1': BLUE, '2': TEAL, '3': PURPLE}
    for i, (a, w, f, c) in enumerate(rows):
        y = 52 + i * 26
        b += text(40, y, a, INK, 'start', 12, True) + text(160, y, w, INK, 'start', 11.5) + text(430, y, f, colr[f], 'middle', 13, True) + text(560, y, c, GRAY, 'middle', 11.5)
    b += text(320, 222, 'x = R sin(theta),  y = R cos(theta),  z = H', ORANGE, 'middle', 12, True)
    return svg(236, b, (BLUE,))
