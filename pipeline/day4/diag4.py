# Day 4 diagrams.
import sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, tag, GREEN, RED, PINK

def lock(x, y, c=RED):
    return (f'<rect x="{x}" y="{y + 6}" width="14" height="11" rx="2" fill="{c}"/>'
            f'<path d="M{x + 3} {y + 6} V{y + 2} a4 4 0 0 1 8 0 V{y + 6}" fill="none" stroke="{c}" stroke-width="2"/>')

def s_linker():
    b = text(320, 16, 'each .cpp is compiled alone, then the Linker joins them', GRAY, s=11)
    for x, name, items in [(20, 'main.cpp', [('int s_Variable = 10', False), ('void Function()', False), ('main()', False)]),
                           (440, 'static.cpp', [('static int s_Variable = 5', True), ('static void Function()', True), ('void PrintStatic()', False)])]:
        b += box(x, 30, 180, 150, '', '#f8fafc', '#94a3b8') + text(x + 90, 48, name, INK, s=12, b=True)
        for i, (t, hidden) in enumerate(items):
            y = 60 + i * 38
            b += box(x + 10, y, 160, 30, t, '#fee2e2' if hidden else '#dbeafe', RED if hidden else BLUE, fs=10.5)
            if hidden: b += lock(x + 150, y + 6)
    b += box(250, 75, 140, 60, 'Linker', '#f5f3ff', PURPLE, True, tc=PURPLE, fs=14)
    b += line(202, 105, 248, 105, PURPLE) + line(438, 105, 392, 105, PURPLE)
    b += text(320, 160, 'sees only the blue names', PURPLE, s=11, b=True)
    b += text(320, 200, 'red + lock = static: hidden from the Linker, so the same name in main.cpp is OK', RED, s=11)
    return svg(210, b, (PURPLE,))

def c_const4():
    b = ''
    cases = [('int* p', True, True), ('const int* p', False, True), ('int* const p', True, False), ('const int* const p', False, False)]
    for i, (t, val_ok, ptr_ok) in enumerate(cases):
        x = 10 + i * 158
        b += text(x + 72, 18, t, INK, s=11.5, b=True)
        b += box(x + 5, 35, 60, 40, 'p', '#fff', BLUE if ptr_ok else RED, True, True, BLUE if ptr_ok else RED)
        b += box(x + 90, 35, 55, 40, '5', '#dbeafe' if val_ok else '#fee2e2', BLUE if val_ok else RED, True)
        b += line(x + 66, 55, x + 88, 55, GRAY)
        if not ptr_ok: b += lock(x + 28, 80)
        if not val_ok: b += lock(x + 110, 80)
        b += text(x + 35, 118, 'move p', GREEN if ptr_ok else RED, s=10.5, b=True) + text(x + 35, 132, '✓' if ptr_ok else '✗', GREEN if ptr_ok else RED, s=13, b=True)
        b += text(x + 117, 118, 'change *p', GREEN if val_ok else RED, s=10.5, b=True) + text(x + 117, 132, '✓' if val_ok else '✗', GREEN if val_ok else RED, s=13, b=True)
    return svg(142, b, (GRAY,))

def e_indices():
    P = {0: (60, 170), 1: (220, 170), 2: (220, 40), 3: (60, 40)}
    b = f'<polygon points="{P[0][0]},{P[0][1]} {P[1][0]},{P[1][1]} {P[2][0]},{P[2][1]}" fill="#bfdbfe" stroke="{BLUE}"/>'
    b += f'<polygon points="{P[2][0]},{P[2][1]} {P[3][0]},{P[3][1]} {P[0][0]},{P[0][1]}" fill="#ccfbf1" stroke="{TEAL}"/>'
    for k, (x, y) in P.items():
        b += f'<circle cx="{x}" cy="{y}" r="12" fill="#fff" stroke="{INK}"/>' + text(x, y + 4.5, str(k), INK, s=12, b=True)
    b += text(170, 140, 'tri 1', BLUE, s=11, b=True) + text(110, 80, 'tri 2', TEAL, s=11, b=True)
    b += text(450, 30, 'positions (4 corners, no repeats)', GRAY, s=11, b=True)
    for k in range(4):
        b += box(300 + k * 75, 40, 70, 28, ['-.5,-.5', '.5,-.5', '.5,.5', '-.5,.5'][k], SOFT, '#c9d1de', fs=10.5) + text(335 + k * 75, 82, str(k), GRAY, s=10)
    b += text(450, 112, 'indices (which corners make each triangle)', GRAY, s=11, b=True)
    for k, v in enumerate([0, 1, 2, 2, 3, 0]):
        c, f = (BLUE, '#bfdbfe') if k < 3 else (TEAL, '#ccfbf1')
        b += box(300 + k * 50, 122, 45, 28, str(v), f, c, True)
    b += text(450, 172, 'glDrawElements reads 6 indices -> 2 triangles', INK, s=11)
    return svg(190, b)

def e_dup():
    b = text(150, 18, 'glDrawArrays: 6 corners', GRAY, s=11, b=True) + text(480, 18, 'glDrawElements: 4 corners + 6 indices', GRAY, s=11, b=True)
    labels = ['-.5,-.5', '.5,-.5', '.5,.5', '.5,.5', '-.5,.5', '-.5,-.5']
    for k, t in enumerate(labels):
        dup = k in (3, 5)
        b += box(10 + k * 47, 30, 44, 30, t, '#fee2e2' if dup else SOFT, RED if dup else '#c9d1de', fs=9)
    b += text(150, 80, 'red = the same corner written twice', RED, s=10.5)
    for k, t in enumerate(['-.5,-.5', '.5,-.5', '.5,.5', '-.5,.5']):
        b += box(340 + k * 72, 30, 66, 30, t, SOFT, '#c9d1de', fs=10)
    for k, v in enumerate([0, 1, 2, 2, 3, 0]):
        b += box(340 + k * 48, 66, 42, 24, str(v), '#ecfdf5', TEAL, fs=11)
    return svg(100, b)

def v_vao():
    b = ''
    for i, (name, c, buf, n) in enumerate([('houseVao', BLUE, 'houseBuffer (24 floats)', 12), ('sunVao', ORANGE, 'sunBuffer (8 floats)', 4)]):
        y = 20 + i * 95
        b += box(20, y, 210, 75, '', '#fff', c) + text(125, y + 18, name, c, s=13, b=True)
        b += text(30, y + 42, 'slot 0 <- ' + buf.split(' ')[0], INK, 'start', 11) + text(30, y + 60, '2 floats per point, stride 8', GRAY, 'start', 10.5)
        b += box(300, y + 15, 170, 45, buf, '#ecfdf5', TEAL, fs=11) + line(232, y + 37, 298, y + 37, c)
        b += box(510, y + 15, 110, 45, f'draw {n} pts', '#f5f3ff', PURPLE, fs=11)
    b += text(320, 210, 'in the loop: glBindVertexArray(houseVao) -> draw; glBindVertexArray(sunVao) -> draw', INK, s=11, b=True)
    return svg(220, b, (BLUE, ORANGE))

def x_khan():
    b = ''
    rows = [(0, 'a2b3 - a3b2', '(-7)(4) - (1)(2) = -30', 'same order'), (1, 'a3b1 - a1b3', '(1)(5) - (1)(4) = 1', 'REVERSED'), (2, 'a1b2 - a2b1', '(1)(2) - (-7)(5) = 37', 'same order')]
    a, bb = [1, -7, 1], [5, 2, 4]
    for i, (hide, f, num, note) in enumerate(rows):
        x = 10 + i * 210
        for k in range(3):
            hidden = k == hide
            b += box(x + 20, 20 + k * 30, 40, 26, str(a[k]), '#f3f4f6' if hidden else '#dbeafe', '#d1d5db' if hidden else BLUE, fs=11, tc=GRAY if hidden else INK)
            b += box(x + 70, 20 + k * 30, 40, 26, str(bb[k]), '#f3f4f6' if hidden else '#ffedd5', '#d1d5db' if hidden else ORANGE, fs=11, tc=GRAY if hidden else INK)
            if hidden:
                b += f'<line x1="{x + 15}" y1="{33 + k * 30}" x2="{x + 115}" y2="{33 + k * 30}" stroke="{GRAY}" stroke-width="2"/>'
        b += text(x + 160, 45, f'row {i + 1}', INK, s=11, b=True) + text(x + 160, 62, f'hide row {hide + 1}', GRAY, s=10)
        b += text(x + 100, 128, f, RED if i == 1 else INK, s=11.5, b=True) + text(x + 100, 146, num, INK, s=10.5)
        b += text(x + 100, 164, note, RED if i == 1 else GRAY, s=10.5, b=i == 1)
    b += text(320, 188, '[1, -7, 1] x [5, 2, 4] = [-30, 1, 37]', GREEN, s=13, b=True)
    return svg(198, b)
