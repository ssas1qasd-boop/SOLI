# Day 5 diagrams (English labels inside the SVG; Arabic captions in HTML).
import sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, tag, GREEN, RED, PINK


def p_swap():
    """x and y in main, a and b inside swap() holding their addresses, temp in the middle."""
    b = text(150, 18, 'main()', INK, s=12, b=True) + text(490, 18, 'swap(int* a, int* b)', PURPLE, s=12, b=True)
    b += f'<line x1="320" y1="30" x2="320" y2="245" stroke="#e2e6ee"/>'
    for i, (n, v, addr) in enumerate([('x', '10', '0x...90'), ('y', '20', '0x...94')]):
        y = 45 + i * 80
        b += box(90, y, 110, 50, v, '#dbeafe', BLUE, True, fs=16)
        b += text(70, y + 30, n, BLUE, s=14, b=True) + text(145, y + 66, 'address ' + addr, GRAY, s=10.5)
    for i, (n, addr) in enumerate([('a', '0x...90'), ('b', '0x...94')]):
        y = 45 + i * 80
        b += box(440, y, 110, 50, addr, '#fff', PURPLE, True, True, PURPLE, fs=12)
        b += text(570, y + 30, n, PURPLE, s=14, b=True)
        b += line(438, y + 25, 204, y + 25, PURPLE, dash=True)
    b += box(440, 196, 110, 34, 'temp', '#fef3c7', '#d97706', True, tc='#78350f')
    b += text(495, 248, '*a = the 10 inside x', PURPLE, s=11)
    return svg(258, b, (PURPLE,))


def p_three():
    b = ''
    cols = [('SwapValue(int a, int b)', 'copies: NEW boxes', ORANGE, False), ('SwapPointer(int* a, int* b)', 'addresses of x and y', PURPLE, True), ('SwapReference(int& a, int& b)', 'same boxes, new names', BLUE, True)]
    for i, (t, sub, c, ok) in enumerate(cols):
        x = 12 + i * 210
        b += text(x + 98, 18, t, c, s=11, b=True) + text(x + 98, 34, sub, GRAY, s=10.5)
        b += box(x + 20, 48, 70, 40, 'x 10', '#dbeafe', BLUE, True) + box(x + 110, 48, 70, 40, 'y 20', '#dbeafe', BLUE, True)
        if i == 0:
            b += box(x + 20, 112, 70, 34, 'a 10', '#ffedd5', ORANGE, True) + box(x + 110, 112, 70, 34, 'b 20', '#ffedd5', ORANGE, True)
            b += line(x + 55, 90, x + 55, 110, ORANGE, dash=True) + line(x + 145, 90, x + 145, 110, ORANGE, dash=True)
        elif i == 1:
            b += box(x + 20, 112, 70, 34, '&x', '#fff', PURPLE, True, True, PURPLE) + box(x + 110, 112, 70, 34, '&y', '#fff', PURPLE, True, True, PURPLE)
            b += line(x + 55, 110, x + 55, 92, PURPLE) + line(x + 145, 110, x + 145, 92, PURPLE)
        else:
            b += tag(x + 28, 96, 'a', BLUE) + tag(x + 118, 96, 'b', BLUE)
        b += text(x + 100, 172, 'x and y swapped?', INK, s=11) + text(x + 100, 192, 'YES' if ok else 'NO', GREEN if ok else RED, s=14, b=True)
    return svg(205, b, (ORANGE, PURPLE, BLUE))


def r_vec4():
    b = text(320, 18, 'the buffer gives 2 numbers per corner, the shader asks for vec4', GRAY, s=11)
    for i, (n, v, c, fill) in enumerate([('x', '-0.5', BLUE, '#dbeafe'), ('y', '-0.5', BLUE, '#dbeafe'), ('z', '0.0', GRAY, '#f3f4f6'), ('w', '1.0', GRAY, '#f3f4f6')]):
        x = 150 + i * 90
        b += box(x, 40, 80, 46, v, fill, c, True, i > 1, c, 15) + text(x + 40, 104, n, c, s=13, b=True)
    b += text(240, 130, 'from the buffer (size 2)', BLUE, s=11, b=True) + text(420, 130, 'filled in by OpenGL', GRAY, s=11, b=True)
    b += text(320, 158, 'layout(location = 0) in vec4 position;', INK, s=12)
    return svg(170, b, (BLUE,))


def r_pipeline():
    b = ''
    b += box(10, 60, 110, 70, 'positions', '#dbeafe', BLUE, True)
    b += text(65, 150, '3 corners', BLUE, s=11)
    b += box(150, 50, 140, 90, 'Vertex Shader', '#ccfbf1', TEAL, True, tc=TEAL)
    b += text(220, 158, 'runs 3 times', TEAL, s=11) + text(220, 174, 'x 1.5  +  v_Position', TEAL, s=11)
    b += box(320, 60, 120, 70, 'Rasterizer', '#f3f4f6', GRAY, True)
    b += text(380, 150, 'mixes v_Position', GRAY, s=11) + text(380, 166, 'for every pixel', GRAY, s=11)
    b += box(470, 50, 160, 90, 'Fragment Shader', '#fce7f3', PINK, True, tc=PINK)
    b += text(550, 158, 'runs once per pixel', PINK, s=11) + text(550, 174, 'color from position', PINK, s=11)
    b += line(122, 95, 148, 95) + line(292, 95, 318, 95, TEAL) + line(442, 95, 468, 95, GRAY)
    b += text(305, 30, 'out vec4 v_Position  ->  in vec4 v_Position', PURPLE, s=12, b=True)
    return svg(190, b, (BLUE, TEAL, GRAY))


def n_list_vs_np():
    b = text(160, 18, 'Python list [1, 2, 3]', ORANGE, s=12, b=True) + text(480, 18, 'np.array([1, 2, 3])', TEAL, s=12, b=True)
    for i in range(3):
        b += box(40 + i * 75, 40, 60, 30, 'ptr', '#fff', ORANGE, True, True, ORANGE, 11)
        b += box(30 + i * 85, 115 + (i % 2) * 22, 70, 38, f'int {i + 1}', '#ffedd5', ORANGE, True, fs=11)
        b += line(70 + i * 75, 72, 65 + i * 85, 113 + (i % 2) * 22, ORANGE)
    b += text(160, 200, 'each int is a full Python object (~28 bytes)', ORANGE, s=10.5)
    b += f'<line x1="320" y1="30" x2="320" y2="210" stroke="#e2e6ee"/>'
    for i in range(3):
        b += box(370 + i * 70, 70, 70, 44, str(i + 1), '#ccfbf1', TEAL, True)
    b += text(475, 135, '8 bytes each, side by side', TEAL, s=11, b=True) + text(475, 152, 'nbytes = 3 x 8 = 24', TEAL, s=11)
    b += text(475, 200, 'one fast loop in C over all of them', TEAL, s=10.5)
    return svg(215, b, (ORANGE,))


def n_shape():
    b = text(320, 16, 'b.shape = (2, 3): 2 rows x 3 columns, counting from 0', INK, s=12, b=True)
    vals = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    for g, (hl, title) in enumerate([(lambda r, c: r == 1 and c == 2, 'b[1, 2] = 6.0'), (lambda r, c: r == 0, 'b[0, :] = row 0'), (lambda r, c: c == 1, 'b[:, 1] = column 1')]):
        x0 = 20 + g * 210
        for r in range(2):
            for c in range(3):
                on = hl(r, c)
                b += box(x0 + 20 + c * 52, 40 + r * 44, 48, 38, str(vals[r][c]), '#fef3c7' if on else '#f8fafc', '#d97706' if on else '#cbd5e1', on)
        b += text(x0 + 98, 150, title, '#b45309', s=11.5, b=True)
        b += text(x0 + 8, 63, '0', GRAY, s=10) + text(x0 + 8, 107, '1', GRAY, s=10)
        for c in range(3): b += text(x0 + 44 + c * 52, 36, str(c), GRAY, s=10)
    return svg(165, b, (GRAY,))


def v_pushpop():
    rows = [('list = []', []), ('push_back("Braden")', ['Braden']), ('push_back("Jeff")', ['Braden', 'Jeff']), ('push_back("Katie")', ['Braden', 'Jeff', 'Katie']),
            ('push_back("Q")', ['Braden', 'Jeff', 'Katie', 'Q']), ('pop_back()', ['Braden', 'Jeff', 'Katie'])]
    b = ''
    for i, (t, items) in enumerate(rows):
        y = 12 + i * 36
        b += text(150, y + 21, t, PURPLE if 'pop' in t else (BLUE if 'push' in t else GRAY), a='end', s=11.5, b=True)
        for j, it in enumerate(items):
            last = j == len(items) - 1 and i > 0
            hot = it == 'Q'
            b += box(170 + j * 92, y, 86, 28, it, '#fee2e2' if hot else ('#dbeafe' if last else '#f8fafc'), RED if hot else (BLUE if last else '#cbd5e1'), last or hot, fs=11.5)
        b += text(560, y + 20, f'size = {len(items)}', GRAY, a='start', s=11)
    b += text(320, 236, 'push_back adds at the END, pop_back removes the LAST one (the Q)', INK, s=11.5)
    return svg(245, b, (BLUE,))


def c_delete():
    b = text(320, 16, 'points (2 floats per point)    polylines (first, count)', INK, s=12, b=True)
    cols = [BLUE] * 8 + [ORANGE] * 6
    for i, c in enumerate(cols):
        b += box(20 + i * 43, 32, 40, 30, 'x' if i % 2 == 0 else 'y', '#dbeafe' if c == BLUE else '#ffedd5', c, fs=11)
    b += text(20 + 4 * 43, 80, 'line 0: 4 points = 8 floats', BLUE, s=11, b=True) + text(20 + 11 * 43, 80, 'line 1: 3 points = 6 floats', ORANGE, s=11, b=True)
    b += box(60, 100, 120, 34, '{ 0, 4 }', '#dbeafe', BLUE, True) + box(200, 100, 120, 34, '{ 4, 3 }', '#ffedd5', ORANGE, True) + box(340, 100, 120, 34, '{ 7, 0 }', '#f3f4f6', GRAY, False, True)
    b += text(400, 152, 'empty line after right click', GRAY, s=10.5)
    b += text(320, 185, 'Backspace: skip the empty line, then pop_back() the orange line', PURPLE, s=12, b=True)
    b += text(320, 205, 'and pop_back() its 3 x 2 = 6 floats from points', PURPLE, s=12, b=True)
    return svg(215, b, (PURPLE,))
