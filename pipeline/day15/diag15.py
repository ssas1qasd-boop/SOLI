# Week 4 Day 1 diagrams (English labels inside the SVG; Arabic captions in HTML). Numbers from the real runs.
import sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, GREEN, RED, PINK


def p_tpl():
    b = box(220, 20, 200, 40, 'template&lt;typename T&gt; Print(T)', '#ede9fe', PURPLE, True, fs=11.5)
    for i, (t, c) in enumerate([('Print(int)', BLUE), ('Print(float)', TEAL), ('Print(const char*)', ORANGE), ('Print(std::string)', GREEN)]):
        x = 20 + i * 155
        b += line(320, 60, x + 70, 110, GRAY, 1.4) + box(x, 110, 140, 36, t, '#f8fafc', c, True, fs=11)
    b += text(320, 172, 'the compiler writes one real function for each type you use', INK, 'middle', 12, True)
    b += text(320, 194, 'NeverCalled(T) is never written, so its mistake is never seen', GRAY, 'middle', 11)
    return svg(206, b, (GRAY,))


def t_steps():
    """rotate around the center = T(c) R T(-c), read right to left"""
    b = ''
    steps = [('T(-c): center to origin', BLUE), ('R(90): rotate', ORANGE), ('T(c): back', GREEN)]
    for i, (t, c) in enumerate(steps):
        x = 30 + i * 210
        b += box(x, 30, 180, 40, t, '#f8fafc', c, True, fs=11.5)
        if i: b += line(x - 30, 50, x, 50, c)
    b += text(320, 100, 'matrix = T(c) @ R @ T(-c)   (the rightmost one happens first)', INK, 'middle', 12, True)
    b += text(320, 126, 'one 3 x 3 matrix: [a b | e] [c d | f] [0 0 1]  ->  a b c d = rotation and scale, e f = translation', GRAY, 'middle', 10.5)
    b += text(320, 152, 'point (x, y, 1) moves.   direction (x, y, 0) only turns.', PURPLE, 'middle', 12, True)
    return svg(166, b, (BLUE, ORANGE, GREEN))


def m_cols():
    b = text(320, 22, 'M2 @ M1, column by column (3Blue1Brown)', INK, 'middle', 12.5, True)
    b += box(30, 40, 150, 50, 'M1 = [[1, -2], [1, 0]]', '#dbeafe', BLUE, True, fs=11)
    b += box(30, 100, 150, 50, 'M2 = [[0, 2], [1, 0]]', '#ffedd5', ORANGE, True, fs=11)
    b += text(200, 70, 'i-hat -> (1, 1)', GREEN, 'start', 11.5, True) + text(200, 130, 'j-hat -> (-2, 0)', RED, 'start', 11.5, True)
    b += line(330, 66, 380, 66, GREEN) + line(330, 126, 380, 126, RED)
    b += text(390, 70, 'M2 (1, 1) = (2, 1)', GREEN, 'start', 11.5, True) + text(390, 130, 'M2 (-2, 0) = (0, -2)', RED, 'start', 11.5, True)
    b += text(320, 180, 'M2 @ M1 = [[2, 0], [1, -2]]  =  np.matmul', PURPLE, 'middle', 12.5, True)
    return svg(194, b, (GREEN, RED))


def c_orbit():
    import math
    b = ''
    for k, (name, col) in enumerate([('T * R: spin in place', BLUE), ('R * T: orbit around 0', ORANGE)]):
        ox = 160 + k * 320
        b += text(ox, 22, name, col, 'middle', 12, True)
        b += f'<circle cx="{ox}" cy="130" r="4" fill="{GRAY}"/>' + text(ox + 6, 146, '0', GRAY, 'start', 10)
        for a in (0, 90, 180, 270):
            t = math.radians(a)
            if k == 0: cx, cy = ox + 70, 130
            else: cx, cy = ox + 70 * math.cos(t), 130 - 70 * math.sin(t)
            nx, ny = cx + 18 * math.cos(t), cy - 18 * math.sin(t)
            b += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="7" fill="{col}" fill-opacity="{0.3 + a / 400:.2f}"/>'
            b += f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{nx:.0f}" y2="{ny:.0f}" stroke="{INK}" stroke-width="2"/>'
            if k == 1: b += text(cx, cy + (22 if a != 90 else -12), str(a), GRAY, 'middle', 10)
        if k == 1: b += f'<circle cx="{ox}" cy="130" r="70" fill="none" stroke="{col}" stroke-dasharray="4 4"/>'
    b += text(320, 232, 'center from the run: T * R stays at (7, 0);  R * T goes (7, 0) -> (0, 7) -> (-7, 0) -> (0, -7)', INK, 'middle', 11)
    return svg(246, b, (BLUE,))
