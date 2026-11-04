import sys
sys.path.insert(0, '/home/claude/day1')
from diagrams import svg, box, text, line, fig, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT

def c_family():
    b = box(260, 20, 120, 44, 'C  (1972)', '#eff6ff', BLUE, True, tc=BLUE)
    kids = ['C++', 'C#', 'Java', 'Objective-C', 'Go']
    for i, k in enumerate(kids):
        x = 20 + i * 125
        b += box(x, 120, 105, 38, k, '#fff', '#c9d1de', fs=12)
        b += line(320, 64, x + 52, 118, GRAY, 1.5)
    b += text(320, 186, 'Unix, Linux, Git and most device drivers are written in C', GRAY, s=11)
    return svg(195, b, (GRAY,))

def c_arith():
    b = ''
    for i, v in enumerate([10, 20, 30, 40]):
        x = 90 + i * 120
        b += box(x, 50, 110, 46, str(v), '#dbeafe' if i == 0 else SOFT, BLUE if i == 0 else '#c9d1de', True)
        b += text(x + 55, 116, ['…e40', '…e44', '…e48', '…e4c'][i], GRAY, s=11)
    b += text(45, 77, 'arr', BLUE, s=12, b=True)
    for i in range(3):
        x = 145 + i * 120
        b += line(x, 36, x + 112, 36, ORANGE, 2, True, curve=(x + 56, 8))
        b += text(x + 56, 14, 'p++  (+4 bytes)', ORANGE, s=10)
    b += text(320, 145, 'p++ jumps to the NEXT int (4 bytes), not the next byte', INK, s=12)
    return svg(160, b, (ORANGE,))

def c_byvalue():
    b = text(160, 20, 'doubleIt(int number)  — a COPY', GRAY, s=12, b=True)
    b += box(60, 40, 90, 44, '21', '#dbeafe', BLUE, True) + text(105, 102, 'score', BLUE, s=11)
    b += box(190, 40, 90, 44, '42', '#fee2e2', '#dc2626', True) + text(235, 102, 'number (copy)', '#dc2626', s=11)
    b += line(150, 62, 188, 62, GRAY, 1.5)
    b += text(160, 128, 'score stays 21', '#dc2626', s=12, b=True)
    b += text(480, 20, 'doubleIt(int* number)  — the ADDRESS', GRAY, s=12, b=True)
    b += box(380, 40, 90, 44, '42', '#dcfce7', '#16a34a', True) + text(425, 102, 'score', '#15803d', s=11)
    b += box(510, 40, 110, 44, '&score', '#fff', BLUE, True, True, BLUE) + text(565, 102, 'number', BLUE, s=11)
    b += line(510, 62, 472, 62, BLUE, 2)
    b += text(480, 128, 'score becomes 42', '#15803d', s=12, b=True)
    return svg(140, b, (GRAY, BLUE))

def va_layout():
    b = ''
    names = ['x', 'y', 'r', 'g', 'b']
    for v in range(3):
        for i in range(5):
            x = 20 + v * 205 + i * 39
            col = '#dbeafe' if i < 2 else '#fce7f3'
            stroke = BLUE if i < 2 else '#db2777'
            b += box(x, 70, 36, 34, names[i], col, stroke, fs=12)
        b += text(20 + v * 205 + 97, 124, f'vertex {v}', GRAY, s=11)
    b += f'<path d="M20 58 L20 50 L215 50 L215 58" fill="none" stroke="{TEAL}" stroke-width="2"/>'
    b += text(118, 42, 'stride = 5 floats = 20 bytes', TEAL, s=12, b=True)
    b += line(225, 62, 300, 62, TEAL, 2) + text(300, 30, '(jump to the next vertex)', TEAL, s=10)
    b += f'<path d="M20 112 L20 140 L98 140" fill="none" stroke="#db2777" stroke-width="2" marker-end="url(#ar{"db2777"})"/>'
    b += text(60, 158, 'offset of color = 2 floats = 8 bytes', '#db2777', s=12, a='start', b=True)
    b += text(420, 150, 'blue = attribute 0 (position)', BLUE, s=11, a='start')
    b += text(420, 168, 'pink = attribute 1 (color)', '#db2777', s=11, a='start')
    return svg(180, b, (TEAL, '#db2777'))

def va_slots():
    b = box(20, 30, 230, 110, '', '#eff6ff', BLUE) + text(135, 22, 'C++  (glVertexAttribPointer)', BLUE, s=12, b=True)
    b += box(40, 50, 190, 32, 'index 0 → 2 floats', '#fff', BLUE, fs=12)
    b += box(40, 95, 190, 32, 'index 1 → 3 floats', '#fff', '#db2777', fs=12)
    b += box(390, 30, 230, 110, '', '#ecfdf5', TEAL) + text(505, 22, 'Vertex Shader', TEAL, s=12, b=True)
    b += box(405, 50, 200, 32, 'location = 0 · vec2', '#fff', BLUE, fs=12)
    b += box(405, 95, 200, 32, 'location = 1 · vec3', '#fff', '#db2777', fs=12)
    b += line(230, 66, 403, 66, BLUE, 2) + line(230, 111, 403, 111, '#db2777', 2)
    b += text(320, 158, 'the numbers must match, or the shader reads zeros', GRAY, s=11)
    return svg(168, b, (BLUE, '#db2777'))

def va_blend():
    b = '<defs><linearGradient id="g1" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#ef4444"/><stop offset=".5" stop-color="#22c55e"/><stop offset="1" stop-color="#3b82f6"/></linearGradient></defs>'
    b += '<path d="M200 20 L320 170 L80 170 Z" fill="url(#g1)" opacity=".9"/>'
    for (x, y, c, t) in [(200, 20, '#22c55e', 'green (0,1,0)'), (80, 170, '#ef4444', 'red (1,0,0)'), (320, 170, '#3b82f6', 'blue (0,0,1)')]:
        b += f'<circle cx="{x}" cy="{y}" r="8" fill="{c}" stroke="#fff" stroke-width="2"/>'
        b += text(x, y + (-12 if y < 100 else 24), t, c, s=11, b=True)
    b += '<circle cx="200" cy="120" r="5" fill="#fff" stroke="#111"/>' + text(205, 136, 'mix of all 3', INK, s=10, a='start')
    b += text(470, 70, '3 corners have colors.', INK, s=12) + text(470, 92, 'Every pixel in between', INK, s=12) + text(470, 114, 'gets a mix of them,', INK, s=12) + text(470, 136, 'weighted by distance.', INK, s=12)
    return svg(200, b)

def m_pyth():
    b = f'<path d="M120 170 L200 170 L200 30 Z" fill="#eff6ff" stroke="{BLUE}" stroke-width="2"/>'
    b += line(120, 170, 200, 30, ORANGE, 3, True)
    b += text(160, 190, 'x = 2', BLUE, s=12, b=True) + text(212, 105, 'y = 5', BLUE, s=12, a='start', b=True)
    b += text(140, 90, '‖v‖ = √29', ORANGE, s=13, a='end', b=True)
    b += f'<rect x="188" y="158" width="12" height="12" fill="none" stroke="{BLUE}"/>'
    b += text(430, 60, 'Pythagoras:  2² + 5² = 29', INK, s=13, b=True)
    b += text(430, 90, 'length = √29 ≈ 5.385', INK, s=13)
    b += text(430, 130, 'and  [2,5]·[2,5] = 4 + 25 = 29', TEAL, s=13, b=True)
    b += text(430, 155, 'so  ‖v‖² = v · v', TEAL, s=13)
    return svg(200, b, (ORANGE,))

def v_growth():
    b = ''
    rows = [(1, 1), (2, 2), (3, 4), (5, 8), (9, 16)]
    for r, (size, cap) in enumerate(rows):
        y = 18 + r * 34
        b += text(70, y + 17, f'size {size}', GRAY, s=11, a='end')
        for i in range(cap):
            filled = i < size
            b += f'<rect x="{85 + i*24}" y="{y}" width="20" height="22" rx="3" fill="{"#3b82f6" if filled else "#fff"}" stroke="{"#2563eb" if filled else "#c9d1de"}"/>'
        b += text(85 + cap * 24 + 8, y + 16, f'capacity {cap}', BLUE, s=11, a='start')
    b += text(320, 196, 'full? → reserve a bigger block, copy everything, free the old one', ORANGE, s=12, b=True)
    return svg(206, b)

def v_dangling():
    b = text(150, 20, 'before push_back', GRAY, s=12, b=True) + text(470, 20, 'after push_back (moved!)', GRAY, s=12, b=True)
    b += box(60, 40, 60, 34, '1,2,3', '#dbeafe', BLUE, fs=11) + text(90, 92, 'old block', GRAY, s=10)
    b += box(380, 40, 60, 34, '1,2,3', '#dbeafe', BLUE, fs=11) + box(444, 40, 60, 34, '4,5,6', '#dbeafe', BLUE, fs=11) + text(442, 92, 'new block', GRAY, s=10)
    b += box(190, 40, 100, 34, 'first', '#fff', '#dc2626', True, True, '#dc2626')
    b += line(190, 57, 122, 57, '#dc2626', 2)
    b += f'<g stroke="#dc2626" stroke-width="3"><line x1="72" y1="44" x2="108" y2="70"/><line x1="108" y1="44" x2="72" y2="70"/></g>'
    b += text(320, 125, 'the old block was freed, but "first" still points at it', '#dc2626', s=12, b=True)
    return svg(140, b, ('#dc2626',))
