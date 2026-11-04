# Week 3 Day 1 diagrams (English labels inside the SVG; Arabic captions in HTML).
import sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, GREEN, RED, PINK


def c_objects():
    """class = template; two objects in RAM (real addresses from one run); one Move() for both"""
    b = '<rect x="12" y="20" width="190" height="150" rx="10" fill="#f5f3ff" stroke="#7c3aed" stroke-dasharray="5 4"/>' + text(107, 40, 'class Player (template)', PURPLE, 'middle', 12, True)
    for i, t in enumerate(['int x, y;', 'int speed;', 'void Move(int xa, int ya)']):
        b += box(26, 52 + i * 36, 162, 28, t, '#fff', PURPLE, i == 2, fs=11)
    b += '<rect x="236" y="20" width="390" height="190" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="4 3"/>' + text(246, 40, 'RAM (stack)', GRAY, 'start', 11, True)
    rows = [('player', '@ 0x7ffe1b2768e0', [('x', '4'), ('y', '-4'), ('speed', '2')]), ('enemy', '', [('x', '5'), ('y', '10'), ('speed', '5')])]
    for r, (n, a, cells) in enumerate(rows):
        y = 56 + r * 72
        b += text(250, y + 18, n, BLUE, 'start', 12, True) + text(250, y + 34, a, GRAY, 'start', 8.5)
        for k, (cn, cv) in enumerate(cells):
            b += box(370 + k * 82, y, 78, 30, cv, '#dbeafe' if r == 0 else '#e0f2fe', BLUE, True, fs=12) + text(409 + k * 82, y + 44, cn + ' (+' + str(4 * k) + ')', GRAY, 'middle', 9)
    b += line(188, 74, 366, 72, PURPLE, dash=True) + line(188, 110, 366, 144, PURPLE, dash=True)
    b += text(320, 232, 'one Move() for every object: player.Move(1, -1) runs with this = &player', INK, 'middle', 11.5, True)
    b += text(320, 252, 'sizeof(Player) = 12 bytes = 3 ints. The method takes no room inside the object.', GRAY, 'middle', 10.5)
    return svg(262, b, (PURPLE,))


def t_uv():
    """quad corners -> texture coordinates -> slot -> sampler2D"""
    Y0, Y1 = 60, 220
    b = text(110, 16, 'the square (positions)', TEAL, 'middle', 12, True)
    b += f'<rect x="30" y="{Y0}" width="160" height="160" fill="#ecfdf5" stroke="#0d9488" stroke-width="2"/>'
    for (x, y, p, uv) in [(30, Y1, '(-0.5,-0.5)', '(0,0)'), (190, Y1, '(0.5,-0.5)', '(1,0)'), (190, Y0, '(0.5,0.5)', '(1,1)'), (30, Y0, '(-0.5,0.5)', '(0,1)')]:
        top = y == Y0
        b += f'<circle cx="{x}" cy="{y}" r="5" fill="#0d9488"/>' + text(x, y + (-10 if top else 18), p, INK, 'middle', 9.5) + text(x, y + (-23 if top else 31), 'uv ' + uv, ORANGE, 'middle', 9.5, True)
    b += text(400, 16, 'the image (texture coordinates)', ORANGE, 'middle', 12, True)
    b += f'<rect x="320" y="{Y0}" width="160" height="160" fill="#fff7ed" stroke="#c2410c" stroke-width="2"/>'
    b += text(330, Y1 + 14, '(0,0)', ORANGE, 'start', 10, True) + text(470, Y1 + 14, '(1,0)', ORANGE, 'end', 10, True) + text(470, Y0 - 6, '(1,1)', ORANGE, 'end', 10, True) + text(330, Y0 - 6, '(0,1)', ORANGE, 'start', 10, True)
    b += f'<circle cx="400" cy="{Y0 + 80}" r="46" fill="#f2781e"/><polygon points="400,{Y0 + 46} 424,{Y0 + 76} 410,{Y0 + 76} 410,{Y0 + 110} 390,{Y0 + 110} 390,{Y0 + 76} 376,{Y0 + 76}" fill="#fff"/><rect x="326" y="{Y0 + 6}" width="22" height="22" fill="#2563eb"/>'
    b += line(196, Y0 + 80, 314, Y0 + 80, ORANGE)
    b += text(255, Y0 + 72, 'texture()', INK, 'middle', 10)
    b += box(510, 80, 118, 34, 'slot 0', '#e0f2fe', BLUE, True, fs=12) + box(510, 150, 118, 44, '', '#fff', PURPLE) + text(569, 168, 'u_Texture = 0', PURPLE, 'middle', 10.5, True) + text(569, 184, '(glUniform1i)', GRAY, 'middle', 9)
    b += line(484, 100, 506, 98, BLUE) + line(569, 146, 569, 118, PURPLE)
    b += text(320, 276, 'every pixel between the corners gets an in-between uv (interpolation)', INK, 'middle', 11.5, True)
    return svg(288, b, (ORANGE, BLUE, PURPLE))


def m_columns():
    """columns of M = where i-hat and j-hat land; M v = x * col1 + y * col2 (3Blue1Brown example)"""
    b = text(110, 22, 'M (written row by row)', INK, 'middle', 12, True)
    b += '<rect x="44" y="34" width="34" height="76" rx="6" fill="#dcfce7" stroke="#16a34a"/><rect x="88" y="34" width="34" height="76" rx="6" fill="#fee2e2" stroke="#dc2626"/>'
    b += text(61, 64, '1', INK, 'middle', 16, True) + text(61, 96, '-2', INK, 'middle', 16, True) + text(105, 64, '3', INK, 'middle', 16, True) + text(105, 96, '0', INK, 'middle', 16, True)
    b += text(61, 128, 'i lands', GREEN, 'middle', 10, True) + text(105, 128, 'j lands', RED, 'middle', 10, True)
    b += text(160, 78, 'x', INK, 'middle', 16) + '<rect x="176" y="34" width="34" height="76" rx="6" fill="#e0f2fe" stroke="#2563eb"/>' + text(193, 64, '-1', INK, 'middle', 16, True) + text(193, 96, '2', INK, 'middle', 16, True)
    b += text(330, 60, '= -1 * [1, -2] + 2 * [3, 0]', INK, 'middle', 14) + text(330, 98, '= [-1 + 6, 2 + 0] = [5, 2]', INK, 'middle', 14, True)
    gx, gy, s = 480, 100, 20
    for k in range(-3, 4):
        b += f'<line x1="{gx + k * s}" y1="{gy - 3 * s}" x2="{gx + k * s}" y2="{gy + 3 * s}" stroke="#e5e7eb"/><line x1="{gx - 3 * s}" y1="{gy + k * s}" x2="{gx + 3 * s}" y2="{gy + k * s}" stroke="#e5e7eb"/>'
    b += line(gx, gy, gx + 1 * s, gy + 2 * s, GREEN) + line(gx, gy, gx + 3 * s, gy, RED) + line(gx, gy, gx + 5 * s * 0.6, gy - 2 * s * 0.6, BLUE, dash=True)
    b += text(gx + 30, gy + 58, "i' = (1, -2)", GREEN, 'start', 10, True) + text(gx + 70, gy - 6, "j' = (3, 0)", RED, 'start', 10, True) + text(gx + 60, gy - 30, '(5, 2) (scaled)', BLUE, 'start', 9.5)
    b += text(320, 196, 'know where i and j go  ->  you know where every vector goes', INK, 'middle', 11.5, True)
    b += text(320, 216, 'lines stay lines, the origin stays put: that is a linear transformation', GRAY, 'middle', 10.5)
    return svg(228, b, (GREEN, RED, BLUE))


def b_cube():
    """cube B-Rep: vertex numbers, edge numbers, front face highlighted; same projection as wireframe.cpp"""
    def P(x, y, z): return (170 + ((x - .5) * .9 + (y - .5) * .45) * 150, 122 - ((z - .5) * .9 + (y - .5) * .35) * 150)
    V = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    E = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    front = {0, 9, 4, 8}
    b = '<polygon points="' + ' '.join('%.0f,%.0f' % P(*V[i]) for i in (0, 1, 5, 4)) + '" fill="#ffedd5" opacity=".7"/>'
    for k, (a, c) in enumerate(E):
        (x1, y1), (x2, y2) = P(*V[a]), P(*V[c])
        col = ORANGE if k in front else '#9ca3af'
        b += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" stroke-width="{3 if k in front else 1.5}"/>'
        ox, oy = {11: (0, 24), 2: (20, 0), 4: (-28, 0)}.get(k, (0, 0))
        mx, my = (x1 + x2) / 2 + ox, (y1 + y2) / 2 + oy
        b += f'<rect x="{mx - 9:.0f}" y="{my - 8:.0f}" width="18" height="15" rx="3" fill="#fff" stroke="{col}"/>' + text(mx, my + 4, str(k), col, 'middle', 9, True)
    for i, v in enumerate(V):
        x, y = P(*v)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="#2563eb"/>' + text(x, y + 4, str(i), '#fff', 'middle', 10, True)
    rows = [('V = 8 vertices', BLUE), ('E = 12 edges (each joins 2 vertices)', GRAY), ('F = 6 faces (each = a loop of 4 edges)', ORANGE), ('front face = edges 0, 9, 4, 8', ORANGE), ('F - E + V = 6 - 12 + 8 = 2', INK)]
    for i, (t, c) in enumerate(rows):
        b += text(360, 50 + i * 30, t, c, 'start', 12, i == 4)
    b += text(320, 250, 'B-Rep = geometry (where the vertices are) + topology (who is connected to whom)', INK, 'middle', 11.5, True)
    return svg(262, b, (ORANGE,))
