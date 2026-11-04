# Day 7 diagrams (English labels inside the SVG; Arabic captions in HTML).
import sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, GREEN, RED, PINK


def p_chain():
    """stack: var, ptr, buffer, ptrToBuffer; heap: 8 bytes (real addresses from one run)"""
    b = '<rect x="10" y="26" width="300" height="196" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="4 3"/>' + text(20, 42, 'STACK', GRAY, 'start', 11, True)
    b += '<rect x="360" y="26" width="270" height="110" rx="8" fill="#fffaf5" stroke="#c2410c" stroke-dasharray="4 3"/>' + text(370, 42, 'HEAP (new char[8])', ORANGE, 'start', 11, True)
    rows = [('var', '10', '@ 0x7ffe9daad634'), ('ptr, intPtr', '0x7ffe9daad634', ''), ('buffer', '0x5621906ee2c0', '@ 0x7ffe9daad638'), ('ptrToBuffer', '0x7ffe9daad638', '')]
    for i, (n, v, a) in enumerate(rows):
        y = 50 + i * 42
        b += text(22, y + 16, n, BLUE, 'start', 11, True) + (text(22, y + 30, a, GRAY, 'start', 8.5) if a else '')
        b += box(150, y + 2, 150, 28, v, '#dbeafe' if i % 2 == 0 else '#fff', BLUE, False, fs=10.5)
    for k, ch in enumerate(['H', 'i', '0', '0', '0', '0', '0', '0']):
        b += box(372 + k * 31, 62, 28, 30, ch, '#ffedd5' if k < 2 else '#fff', ORANGE, k < 2, fs=12)
    b += text(495, 116, '@ 0x5621906ee2c0', GRAY, 'middle', 9)
    b += line(150, 108, 146, 66, BLUE, curve=(128, 86))
    b += line(300, 150, 370, 80, ORANGE)
    b += line(300, 192, 302, 156, PURPLE, curve=(326, 176))
    b += text(320, 246, '*ptrToBuffer = buffer (an address)    **ptrToBuffer = H', INK, 'middle', 11.5, True)
    return svg(256, b, (BLUE, ORANGE, PURPLE))


def v_vao_box():
    """what lives inside a VAO"""
    b = '<rect x="20" y="20" width="360" height="170" rx="10" fill="#ecfdf5" stroke="#0d9488" stroke-width="2"/>' + text(200, 40, 'VAO (vao)', TEAL, 'middle', 14, True)
    b += box(36, 54, 330, 30, 'attribute 0: enabled', '#fff', TEAL, fs=11.5)
    b += box(36, 92, 330, 40, '', '#fff', TEAL) + text(200, 108, 'attribute 0 reads buffer: 2 floats, stride 8, offset 0', INK, 'middle', 10.5) + text(200, 124, '(saved by glVertexAttribPointer)', GRAY, 'middle', 9.5)
    b += box(36, 140, 330, 34, 'element buffer: ibo (6 indices)', '#fff', TEAL, fs=11.5)
    b += box(420, 40, 200, 40, 'buffer: 8 floats', '#dbeafe', BLUE, True, fs=11.5) + box(420, 140, 200, 34, 'ibo: 0 1 2 2 3 0', '#ffedd5', ORANGE, True, fs=11.5)
    b += line(366, 112, 418, 66, BLUE) + line(366, 157, 418, 157, ORANGE)
    b += box(420, 92, 200, 34, 'NOT inside: shader, uniforms', '#fee2e2', RED, fs=10.5)
    b += text(320, 212, 'glBindVertexArray(vao) brings all of this back in one call', INK, 'middle', 11.5, True)
    return svg(222, b, (BLUE, ORANGE))


def v_two_methods():
    b = text(160, 18, 'method 1: one global VAO', ORANGE, 'middle', 12, True) + text(480, 18, 'method 2: one VAO per object', GREEN, 'middle', 12, True)
    l1 = ['glBindVertexArray(globalVao)', 'glBindBuffer(GL_ARRAY_BUFFER, squareBuffer)', 'glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, 0)', 'glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, squareIbo)', 'glDrawElements', 'glBindBuffer(GL_ARRAY_BUFFER, triangleBuffer)', 'glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, 0)', 'glDrawArrays']
    l2 = ['glBindVertexArray(squareVao)', 'glDrawElements', 'glBindVertexArray(triangleVao)', 'glDrawArrays']
    for i, t in enumerate(l1):
        dr = t.startswith('glDraw')
        b += box(14, 30 + i * 26, 296, 22, t, '#dcfce7' if dr else '#ffedd5', GREEN if dr else ORANGE, False, fs=8.8)
    for i, t in enumerate(l2):
        dr = t.startswith('glDraw')
        b += box(340, 30 + i * 26, 280, 22, t, '#dcfce7' if dr else '#e0f2fe', GREEN if dr else BLUE, False, fs=10)
    b += text(480, 160, 'same picture, 2 binds instead of 6', GREEN, 'middle', 11, True)
    b += '<line x1="320" y1="28" x2="320" y2="240" stroke="#e2e6ee"/>'
    return svg(246, b, (GRAY,))


def x_rows():
    """Khan's three rows: cover one column, the middle one reversed"""
    b = ''
    rows = [('row 1: hide a1, b1', 'a2 b3 - a3 b2', '(-7)(4) - (1)(2) = -30', BLUE), ('row 2: hide a2, b2, REVERSED', 'a3 b1 - a1 b3', '(1)(5) - (1)(4) = 1', RED), ('row 3: hide a3, b3', 'a1 b2 - a2 b1', '(1)(2) - (-7)(5) = 37', BLUE)]
    for i, (t, f, n, c) in enumerate(rows):
        y = 18 + i * 52
        b += text(20, y + 18, t, c, 'start', 11.5, True) + box(250, y + 2, 150, 28, f, '#fff', c, True, fs=12) + text(420, y + 21, n, INK, 'start', 12)
    b += text(320, 182, '[1, -7, 1] x [5, 2, 4] = [-30, 1, 37]', GREEN, 'middle', 13, True)
    return svg(192, b, (BLUE,))


def x_hand():
    """i x j = k and the normal of a triangle"""
    o = (130, 150)
    b = f'<line x1="{o[0]}" y1="{o[1]}" x2="{o[0] + 110}" y2="{o[1]}" stroke="{BLUE}" stroke-width="3" marker-end="url(#ar{BLUE[1:]})"/>'
    b += f'<line x1="{o[0]}" y1="{o[1]}" x2="{o[0] - 60}" y2="{o[1] + 45}" stroke="{ORANGE}" stroke-width="3" marker-end="url(#ar{ORANGE[1:]})"/>'
    b += f'<line x1="{o[0]}" y1="{o[1]}" x2="{o[0]}" y2="{o[1] - 115}" stroke="{GREEN}" stroke-width="3" marker-end="url(#ar{GREEN[1:]})"/>'
    b += text(o[0] + 122, o[1] + 4, 'i (x)', BLUE, 'start', 12, True) + text(o[0] - 70, o[1] + 60, 'j (y)', ORANGE, 'middle', 12, True) + text(o[0] + 8, o[1] - 118, 'k = i x j', GREEN, 'start', 12, True)
    pts = [(380, 175), (560, 175), (430, 95)]
    b += f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.5"/>'
    b += text(372, 192, 'p0', INK, 'middle', 11) + text(566, 192, 'p1', INK, 'middle', 11) + text(424, 88, 'p2', INK, 'middle', 11)
    b += f'<line x1="456" y1="150" x2="456" y2="40" stroke="{GREEN}" stroke-width="3" marker-end="url(#ar{GREEN[1:]})"/>' + text(466, 46, 'n = (p1 - p0) x (p2 - p0)', GREEN, 'start', 11.5, True)
    return svg(232, b, (BLUE, ORANGE, GREEN))


def g_areas():
    """working folder -> staging -> repository"""
    b = ''
    cols = [('working folder', 'refactored.cpp (edited)', '#fff7ed', ORANGE), ('staging area', 'ready for the commit', '#eff6ff', BLUE), ('repository (.git)', 'commits = save points', '#ecfdf5', GREEN)]
    for i, (t, s, f, c) in enumerate(cols):
        x = 14 + i * 212
        b += box(x, 30, 190, 64, '', f, c, True) + text(x + 95, 56, t, c, 'middle', 13, True) + text(x + 95, 78, s, INK, 'middle', 10.5)
    b += line(206, 62, 224, 62, BLUE) + text(215, 112, 'git add .', BLUE, 'middle', 11, True)
    b += line(418, 62, 436, 62, GREEN) + text(427, 112, 'git commit -m', GREEN, 'middle', 11, True)
    for k, (h, m) in enumerate([('84180e1', 'add refactored polyline tool'), ('ed785af', 'make points bigger: 10 -> 12 px')]):
        y = 132 + k * 30
        b += box(330, y, 64, 24, h, '#dcfce7', GREEN, True, fs=10.5) + text(400, y + 16, m, INK, 'start', 10.5)
    b += line(362, 156, 362, 162, GREEN, arrow=False)
    b += text(20, 140, 'git status: which box', GRAY, 'start', 10.5) + text(20, 156, 'each change is in', GRAY, 'start', 10.5)
    return svg(196, b, (BLUE, GREEN))


def g_hash():
    """file -> blob -> tree -> commit id"""
    st = [('refactored.cpp', '227 lines', '#f1f5f9', GRAY), ('blob', 'd088e29', '#dbeafe', BLUE), ('tree', 'c298df0', '#ede9fe', PURPLE), ('commit', '84180e1', '#dcfce7', GREEN)]
    b = ''
    for i, (t, s, f, c) in enumerate(st):
        x = 10 + i * 158
        b += box(x, 30, 140, 56, '', f, c, True) + text(x + 70, 52, t, c, 'middle', 12.5, True) + text(x + 70, 74, s, INK, 'middle', 11)
        if i < 3: b += line(x + 142, 58, x + 156, 58, GRAY)
    b += text(320, 112, 'SHA-1 of the bytes', GRAY, 'middle', 10.5)
    b += text(320, 134, 'commit text = tree id + author + time + message', INK, 'middle', 11)
    return svg(146, b, (GRAY,))
