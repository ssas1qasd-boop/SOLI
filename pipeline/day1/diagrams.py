# Illustrative SVG diagrams (English labels inside; Arabic captions are added in HTML).
BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT = '#2563eb', '#0d9488', '#c2410c', '#7c3aed', '#8a8f98', '#1d2330', '#eef1f6'

def fig(svg, cap):
    return f'<div class="fig">{svg}<div class="figcap">{cap}</div></div>'

def arrowdefs(*cols):
    return '<defs>' + ''.join(
        f'<marker id="ar{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
        for c in cols) + '</defs>'

def svg(h, body, cols=(BLUE,)):
    return f'<svg width="100%" viewBox="0 0 640 {h}" xmlns="http://www.w3.org/2000/svg">{arrowdefs(*cols)}<g font-size="13" fill="{INK}">{body}</g></svg>'

def box(x, y, w, h, txt='', fill=SOFT, stroke='#c9d1de', bold=False, dash=False, tc=INK, fs=13):
    d = ' stroke-dasharray="5 4"' if dash else ''
    b = ' font-weight="bold"' if bold else ''
    t = f'<text x="{x+w/2}" y="{y+h/2+4.5}" text-anchor="middle"{b} fill="{tc}" font-size="{fs}">{txt}</text>' if txt != '' else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}"{d}/>' + t

def text(x, y, t, c=INK, a='middle', s=12, b=False):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" fill="{c}" font-size="{s}"{" font-weight=\"bold\"" if b else ""}>{t}</text>'

def line(x1, y1, x2, y2, c=BLUE, w=2, arrow=True, dash=False, curve=None):
    m = f' marker-end="url(#ar{c[1:]})"' if arrow else ''
    d = ' stroke-dasharray="5 4"' if dash else ''
    if curve:
        return f'<path d="M{x1} {y1} Q {curve[0]} {curve[1]} {x2} {y2}" fill="none" stroke="{c}" stroke-width="{w}"{m}{d}/>'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{m}{d}/>'

# ------------------------------------------------------------- POINTERS
def p_street():
    b = ''
    for i, (addr, val) in enumerate([('0x0FFC', '…'), ('0x1000', '8'), ('0x1004', '…'), ('0x1008', '…')]):
        x = 30 + i * 95
        hot = val == '8'
        b += f'<path d="M{x} 60 L{x+40} 30 L{x+80} 60 Z" fill="{"#bfdbfe" if hot else "#e2e6ee"}" stroke="{BLUE if hot else "#c9d1de"}"/>'
        b += box(x, 60, 80, 45, val, '#dbeafe' if hot else SOFT, BLUE if hot else '#c9d1de', hot)
        b += text(x + 40, 124, addr, BLUE if hot else GRAY, s=11)
    b += text(125, 142, 'var lives here', GRAY, s=11)
    b += box(450, 55, 160, 50, '0x1000', '#fff', BLUE, True, True, BLUE)
    b += text(530, 124, 'ptr = paper with the address', GRAY, s=11)
    b += line(450, 80, 215, 72, curve=(330, 20))
    b += text(320, 18, 'memory = a long street of houses (1 house = 1 byte)', GRAY, s=11)
    return svg(150, b)

def p_null():
    b = box(60, 40, 150, 50, 'ptr = 0', '#fff', BLUE, True, True, BLUE)
    b += line(210, 65, 370, 65, GRAY, dash=True, arrow=True)
    b += f'<g stroke="#dc2626" stroke-width="4"><line x1="390" y1="45" x2="430" y2="85"/><line x1="430" y1="45" x2="390" y2="85"/></g>'
    b += text(410, 110, 'points nowhere', '#dc2626', s=12)
    b += text(530, 60, 'reading here', GRAY, s=12) + text(530, 78, '= crash', '#dc2626', s=12, b=True)
    return svg(125, b, (GRAY,))

def p_addr():
    b = box(60, 40, 120, 55, '8', '#dbeafe', BLUE, True) + text(120, 115, 'var  @ 0x7ffe…9ac', BLUE, s=11)
    b += box(400, 40, 180, 55, '0x7ffe…9ac', '#fff', BLUE, True, True, BLUE) + text(490, 115, 'ptr = &var', GRAY, s=11)
    b += line(400, 67, 182, 67)
    b += text(290, 58, '& = "give me the address"', BLUE, s=11)
    return svg(130, b)

def p_types():
    b = ''
    for i in range(8):
        b += box(70 + i * 62, 45, 58, 40, '', '#dbeafe' if i < 4 else SOFT, BLUE if i < 4 else '#c9d1de')
    b += text(40, 70, 'same', GRAY, s=11) + text(40, 84, 'address', GRAY, s=11)
    b += f'<path d="M72 100 L72 108 L314 108 L314 100" fill="none" stroke="{BLUE}" stroke-width="2"/>' + text(193, 126, 'int* reads 4 bytes', BLUE, s=12, b=True)
    b += f'<path d="M72 30 L72 22 L562 22 L562 30" fill="none" stroke="{ORANGE}" stroke-width="2"/>' + text(317, 15, 'double* reads 8 bytes (from the same start)', ORANGE, s=12, b=True)
    return svg(135, b)

def p_deref():
    b = text(150, 22, 'before', GRAY, s=12, b=True) + text(470, 22, 'after  *ptr = 10', GRAY, s=12, b=True)
    b += box(90, 40, 120, 50, '8', '#dbeafe', BLUE, True) + text(150, 108, 'var', BLUE, s=11)
    b += box(410, 40, 120, 50, '10', '#dcfce7', '#16a34a', True, tc='#15803d') + text(470, 108, 'var', BLUE, s=11)
    b += box(250, 120, 140, 40, 'ptr', '#fff', BLUE, True, True, BLUE)
    b += line(320, 120, 425, 92, curve=(380, 100)) + line(320, 120, 195, 92, GRAY, dash=True, curve=(260, 100))
    b += text(320, 180, '* = go to the address, then read or write', BLUE, s=11)
    return svg(190, b, (BLUE, GRAY))

def p_heap():
    b = box(30, 30, 260, 120, '', '#f8fafc', '#c9d1de') + text(160, 22, 'STACK  (0x7ffe…)', GRAY, s=12, b=True)
    b += box(80, 70, 160, 45, 'buffer = 0x55…', '#fff', BLUE, True, True, BLUE, fs=12)
    b += box(340, 30, 280, 120, '', '#fff7ed', '#fdba74') + text(480, 22, 'HEAP  (0x55…)  made by new', ORANGE, s=12, b=True)
    for i in range(8):
        b += box(355 + i * 32, 72, 28, 40, '0', '#fff', ORANGE, fs=12)
    b += line(240, 92, 352, 92)
    b += text(480, 135, '8 bytes, all 0 (memset)', ORANGE, s=11)
    b += text(160, 140, 'normal variables', GRAY, s=11)
    return svg(165, b, (BLUE,))

def p_chain():
    b = box(30, 50, 150, 50, 'ptr', '#fff', PURPLE, True, True, PURPLE) + text(105, 120, 'char**  (address of buffer)', GRAY, s=10)
    b += box(250, 50, 150, 50, 'buffer', '#fff', BLUE, True, True, BLUE) + text(325, 120, 'char*  (address of data)', GRAY, s=10)
    for i in range(4):
        b += box(470 + i * 38, 55, 34, 40, '0', '#fff7ed', ORANGE, fs=12)
    b += text(545, 120, 'the data', GRAY, s=10)
    b += line(180, 75, 247, 75, PURPLE) + line(400, 75, 467, 75)
    b += text(213, 65, '1st *', PURPLE, s=11) + text(433, 65, '2nd *', BLUE, s=11)
    return svg(135, b, (PURPLE, BLUE))

# ------------------------------------------------------------- UNIFORMS
def u_flow():
    b = box(20, 40, 180, 80, '', '#eff6ff', BLUE) + text(110, 30, 'CPU  (your C++)', BLUE, s=12, b=True)
    b += text(110, 75, 'glUniform4f(', INK, s=11) + text(110, 92, '0.2, 0.3, 0.8, 1)', INK, s=11)
    b += box(250, 40, 170, 80, '', '#ecfdf5', TEAL) + text(335, 30, 'GPU  (shader)', TEAL, s=12, b=True)
    b += text(335, 75, 'uniform vec4', INK, s=11) + text(335, 92, 'u_Color', INK, s=12, b=True)
    b += line(200, 80, 247, 80, TEAL, 3)
    b += line(420, 80, 467, 80, TEAL, 3)
    for r in range(3):
        for c in range(4):
            b += f'<rect x="{475+c*36}" y="{45+r*24}" width="32" height="20" fill="#3355cc" rx="2"/>'
    b += text(545, 30, 'every pixel', TEAL, s=12, b=True)
    return svg(135, b, (TEAL,))

def u_attr():
    b = text(160, 22, 'attribute: different per vertex', GRAY, s=12, b=True)
    b += '<defs><linearGradient id="gA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ef4444"/><stop offset=".5" stop-color="#22c55e"/><stop offset="1" stop-color="#3b82f6"/></linearGradient></defs>'
    b += '<path d="M160 40 L250 150 L70 150 Z" fill="url(#gA)"/>'
    for (x, y, c) in [(160, 40, '#ef4444'), (70, 150, '#22c55e'), (250, 150, '#3b82f6')]:
        b += f'<circle cx="{x}" cy="{y}" r="7" fill="{c}" stroke="#fff" stroke-width="2"/>'
    b += text(480, 22, 'uniform: one value for all', GRAY, s=12, b=True)
    b += '<path d="M480 40 L570 150 L390 150 Z" fill="#3355cc"/>'
    for (x, y) in [(480, 40), (390, 150), (570, 150)]:
        b += f'<circle cx="{x}" cy="{y}" r="7" fill="#3355cc" stroke="#fff" stroke-width="2"/>'
    return svg(165, b)

def u_wave():
    b = line(50, 140, 610, 140, GRAY, 1, False) + line(50, 140, 50, 25, GRAY, 1, False)
    b += text(40, 40, '1', GRAY, s=11, a='end') + text(40, 144, '0', GRAY, s=11, a='end') + text(330, 162, 'frames →', GRAY, s=11)
    pts = []
    r, inc = 0.0, 0.05
    for f in range(90):
        pts.append(f'{50 + f*6.2:.1f},{140 - r*105:.1f}')
        if r > 1.0: inc = -0.05
        elif r < 0.0: inc = 0.05
        r += inc
    b += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#db2777" stroke-width="3"/>'
    b += line(50, 35, 610, 35, GRAY, 1, False, True)
    b += text(560, 28, 'r > 1 → go down', '#db2777', s=11) + text(205, 158, 'r < 0 → go up', '#db2777', s=11)
    b += f'<rect x="20" y="150" width="14" height="12" fill="#3355cc"/><rect x="20" y="22" width="14" height="12" fill="#ee44cc"/>'
    return svg(170, b)

# ------------------------------------------------------------- DOT
def d_proj():
    b = '<g font-size="13">'
    b += f'<line x1="60" y1="120" x2="420" y2="120" stroke="{ORANGE}" stroke-width="3" marker-end="url(#ar{ORANGE[1:]})"/>' + text(432, 125, 'v', ORANGE, s=14, b=True)
    b += f'<line x1="60" y1="120" x2="260" y2="25" stroke="{BLUE}" stroke-width="3" marker-end="url(#ar{BLUE[1:]})"/>' + text(270, 25, 'w', BLUE, s=14, b=True)
    b += line(260, 29, 260, 120, GRAY, 1.5, False, True)
    b += f'<line x1="60" y1="134" x2="260" y2="134" stroke="{TEAL}" stroke-width="5"/>' + text(160, 152, 'shadow of w on v', TEAL, s=12)
    b += text(520, 60, 'v · w = shadow × |v|', INK, s=14, b=True) + '</g>'
    return svg(160, b, (ORANGE, BLUE))

def d_signs():
    b = ''
    for i, (ang, lab, val, col) in enumerate([(40, 'same side', '> 0', '#16a34a'), (90, 'perpendicular', '= 0', '#d97706'), (150, 'opposite', '< 0', '#dc2626')]):
        import math
        ox, oy = 40 + i * 210, 110
        b += f'<line x1="{ox}" y1="{oy}" x2="{ox+120}" y2="{oy}" stroke="{ORANGE}" stroke-width="3" marker-end="url(#ar{ORANGE[1:]})"/>'
        ex, ey = ox + 80 * math.cos(math.radians(ang)) + (60 if ang == 150 else 0), oy - 80 * math.sin(math.radians(ang))
        sx = ox + (60 if ang == 150 else 0)
        b += f'<line x1="{sx}" y1="{oy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{BLUE}" stroke-width="3" marker-end="url(#ar{BLUE[1:]})"/>'
        b += text(ox + 75, 140, lab, col, s=12, b=True) + text(ox + 75, 158, f'v · w {val}', col, s=12)
    return svg(170, b, (ORANGE, BLUE))

def d_machine():
    b = box(30, 50, 130, 50, '[4, 3]', '#fff', BLUE, True, tc=BLUE) + text(95, 120, 'any vector in', GRAY, s=11)
    b += box(240, 35, 170, 80, '', '#fff7ed', ORANGE) + text(325, 70, 'vector [1, −2]', ORANGE, s=13, b=True) + text(325, 92, 'as a machine', GRAY, s=11)
    b += box(490, 50, 120, 50, '−2', '#fff', TEAL, True, tc=TEAL) + text(550, 120, 'one number out', GRAY, s=11)
    b += line(160, 75, 237, 75, GRAY) + line(410, 75, 487, 75, GRAY)
    b += text(325, 140, '1×4 + (−2)×3 = −2', INK, s=12)
    return svg(150, b, (GRAY,))

# ------------------------------------------------------------- CAMERA
def c_vectors():
    b = '<circle cx="250" cy="120" r="9" fill="#7c3aed"/>' + text(250, 148, 'Position', PURPLE, s=12, b=True)
    b += f'<line x1="250" y1="120" x2="420" y2="120" stroke="{ORANGE}" stroke-width="3" marker-end="url(#ar{ORANGE[1:]})"/>' + text(470, 125, 'Orientation', ORANGE, s=12, b=True) + text(470, 140, '(where you look)', GRAY, s=10)
    b += f'<line x1="250" y1="120" x2="250" y2="30" stroke="{TEAL}" stroke-width="3" marker-end="url(#ar{TEAL[1:]})"/>' + text(250, 20, 'Up', TEAL, s=12, b=True)
    b += f'<line x1="250" y1="120" x2="170" y2="170" stroke="{BLUE}" stroke-width="3" marker-end="url(#ar{BLUE[1:]})" stroke-dasharray="6 4"/>' + text(140, 185, 'Right = cross(Orientation, Up)', BLUE, s=11, b=True)
    b += '<path d="M560 70 L610 120 L560 170 Z" fill="#f59e0b" opacity=".85"/>' + text(585, 190, 'object', GRAY, s=10)
    return svg(200, b, (ORANGE, TEAL, BLUE))

def c_wasd():
    b = text(320, 18, 'top view', GRAY, s=11)
    b += '<circle cx="320" cy="110" r="10" fill="#7c3aed"/>'
    for (dx, dy, k, c) in [(0, -70, 'W', ORANGE), (0, 70, 'S', ORANGE), (-90, 0, 'A', BLUE), (90, 0, 'D', BLUE)]:
        b += f'<line x1="{320 + dx*0.15}" y1="{110 + dy*0.15}" x2="{320+dx}" y2="{110+dy}" stroke="{c}" stroke-width="3" marker-end="url(#ar{c[1:]})"/>'
        b += box(320 + dx * 1.35 - 16, 110 + dy * 1.25 - 15, 32, 30, k, '#fff', c, True, tc=c)
    b += text(470, 50, 'W / S: ± Orientation', ORANGE, s=11, a='start') + text(470, 70, 'A / D: ± Right (cross)', BLUE, s=11, a='start')
    b += text(470, 90, 'each frame: + speed (0.1)', GRAY, s=11, a='start')
    return svg(205, b, (ORANGE, BLUE))

def c_fov():
    b = ''
    for i, (deg, lab) in enumerate([(45, 'FOV 45°'), (90, 'FOV 90°')]):
        import math
        ox, oy = 60 + i * 320, 100
        h = math.tan(math.radians(deg / 2)) * 80
        b += f'<path d="M{ox} {oy} L{ox+80} {oy-h:.0f} L{ox+80} {oy+h:.0f} Z" fill="#ede9fe" stroke="{PURPLE}" opacity=".9"/>'
        b += f'<circle cx="{ox}" cy="{oy}" r="6" fill="{PURPLE}"/>' + f'<path d="M{ox+60} {oy-10} L{ox+72} {oy+10} L{ox+48} {oy+10} Z" fill="#f59e0b"/>'
        b += text(ox + 100, 195, lab, PURPLE, s=12, b=True)
    b += text(160, 15, 'narrow → object looks big', GRAY, s=11) + text(480, 15, 'wide → see more, object smaller', GRAY, s=11)
    return svg(205, b)

def c_pitch():
    import math
    ox, oy = 200, 105
    b = f'<circle cx="{ox}" cy="{oy}" r="8" fill="{PURPLE}"/>'
    for sgn in (1, -1):
        a1, a3 = math.radians(90 - 14), math.radians(90 + 14)
        p = f'M{ox} {oy} L{ox + 90*math.cos(a1):.0f} {oy - sgn*90*math.sin(a1):.0f} L{ox + 90*math.cos(a3):.0f} {oy - sgn*90*math.sin(a3):.0f} Z'
        b += f'<path d="{p}" fill="#fecaca" stroke="#dc2626"/>'
    b += f'<line x1="{ox}" y1="{oy}" x2="{ox+110}" y2="{oy-55}" stroke="{ORANGE}" stroke-width="3" marker-end="url(#ar{ORANGE[1:]})"/>'
    b += f'<path d="M{ox+55} {oy} A55 55 0 0 0 {ox+49} {oy-25}" fill="none" stroke="{GRAY}"/>'
    b += text(ox - 40, 22, 'Up', TEAL, s=12, b=True)
    b += text(370, 40, 'red = forbidden zone (5°, drawn bigger)', '#dc2626', s=12, a='start', b=True)
    b += text(370, 62, 'a new direction inside it', GRAY, s=11, a='start')
    b += text(370, 80, 'is rejected → no flipping', GRAY, s=11, a='start')
    b += text(370, 120, 'but a huge mouse jump can', GRAY, s=11, a='start') + text(370, 138, 'skip over the red zone!', '#dc2626', s=11, a='start')
    return svg(210, b, (ORANGE,))

# ------------------------------------------------------------- GLSL words
def u_vec4():
    b = text(320, 18, 'vec4 = one box that holds 4 float numbers', INK, s=13, b=True)
    for row, (labs, vals, col, title) in enumerate([(('x', 'y', 'z', 'w'), ('-0.5', '-0.5', '0.0', '1.0'), BLUE, 'as a position'),
                                                    (('r', 'g', 'b', 'a'), ('0.2', '0.3', '0.8', '1.0'), TEAL, 'as a color')]):
        y = 40 + row * 80
        b += text(95, y + 32, title, col, s=12, b=True)
        for i in range(4):
            x = 170 + i * 105
            b += box(x, y, 95, 45, vals[i], '#fff', col, True, tc=INK)
            b += text(x + 47, y + 62, '.' + labs[i], col, s=12, b=True)
    b += f'<rect x="174" y="80" width="95" height="40" fill="#3355cc" rx="4" opacity="0"/>'
    b += text(320, 205, 'vec2 = 2 numbers · vec3 = 3 numbers · mat4 = 4×4 table (16 numbers)', GRAY, s=11)
    return svg(215, b)

def u_slot():
    b = box(10, 45, 150, 70, '', '#eff6ff', BLUE) + text(85, 35, 'C++ array', BLUE, s=12, b=True)
    b += text(85, 75, '-0.5f, -0.5f,', INK, s=11) + text(85, 93, '(only 2 numbers)', GRAY, s=10)
    b += box(215, 45, 120, 70, '', '#fff7ed', ORANGE) + text(275, 35, 'slot 0', ORANGE, s=12, b=True)
    b += text(275, 75, 'location = 0', INK, s=11) + text(275, 93, 'AttribPointer(0,…)', GRAY, s=10)
    b += box(390, 45, 240, 70, '', '#ecfdf5', TEAL) + text(510, 35, 'in vec4 position', TEAL, s=12, b=True)
    b += text(510, 75, '(-0.5, -0.5, 0.0, 1.0)', INK, s=12, b=True) + text(510, 95, 'GPU fills the missing z = 0, w = 1', GRAY, s=10)
    b += line(160, 80, 212, 80, ORANGE, 3) + line(335, 80, 387, 80, TEAL, 3)
    return svg(130, b, (ORANGE, TEAL))

def u_screen():
    b = f'<rect x="200" y="20" width="240" height="240" fill="#f8fafc" stroke="{GRAY}"/>'
    b += line(320, 20, 320, 260, '#d1d5db', 1, False) + line(200, 140, 440, 140, '#d1d5db', 1, False)
    b += f'<rect x="260" y="80" width="120" height="120" fill="#3355cc"/>'
    for (x, y, t, a) in [(200, 278, '-1', 'middle'), (440, 278, '+1', 'middle'), (190, 264, '-1', 'end'), (190, 26, '+1', 'end')]:
        b += text(x, y, t, GRAY, a=a, s=11)
    b += text(320, 296, 'x →', GRAY, s=11) + text(170, 145, 'y ↑', GRAY, s=11, a='end')
    for (x, y, t) in [(260, 200, '(-0.5,-0.5)'), (380, 200, '(0.5,-0.5)'), (380, 80, '(0.5,0.5)'), (260, 80, '(-0.5,0.5)')]:
        b += f'<circle cx="{x}" cy="{y}" r="4" fill="{ORANGE}"/>' + text(x + (-8 if x < 320 else 8), y + (16 if y > 140 else -8), t, ORANGE, s=10, a='end' if x < 320 else 'start')
    b += text(540, 120, 'gl_Position', TEAL, s=13, b=True) + text(540, 140, 'puts each corner', GRAY, s=11) + text(540, 156, 'on this −1 … +1 screen', GRAY, s=11)
    return svg(305, b)

# ------------------------------------------------------------- WHY
def w_three_mains():
    b = ''
    cols = [(BLUE, 'int main()', 'C++  on the CPU', 'runs ONCE', 'starts the whole program'),
            (ORANGE, 'void main()', 'vertex shader on the GPU', 'runs 4× per frame', 'once for each corner'),
            (TEAL, 'void main()', 'fragment shader on the GPU', 'runs ~77,000× per frame', 'once for each pixel of the square')]
    for i, (c, name, where, times, why) in enumerate(cols):
        x = 15 + i * 210
        b += box(x, 20, 195, 150, '', '#fff', c)
        b += f'<rect x="{x}" y="20" width="195" height="34" rx="6" fill="{c}"/>' + text(x + 97, 42, name, '#fff', s=14, b=True)
        b += text(x + 97, 78, where, c, s=12, b=True)
        b += text(x + 97, 112, times, INK, s=13, b=True)
        b += text(x + 97, 140, why, GRAY, s=11)
    b += text(320, 195, 'same name "main", but 3 different programs on 2 different processors', GRAY, s=12)
    return svg(205, b)

def w_timeline():
    b = ''
    steps1 = ['glfwInit', 'window', 'GLAD', 'data → GPU', 'shader']
    b += text(20, 22, 'SETUP  (once)', BLUE, s=12, a='start', b=True)
    for i, t in enumerate(steps1):
        x = 20 + i * 122
        b += box(x, 32, 108, 36, t, '#eff6ff', BLUE, fs=12)
        if i < 4: b += line(x + 108, 50, x + 120, 50, BLUE, 2)
    b += text(20, 102, 'LOOP  (every frame, ~60 times a second)', ORANGE, s=12, a='start', b=True)
    steps2 = ['glClear', 'glUniform4f', 'glDraw…', 'SwapBuffers', 'PollEvents']
    for i, t in enumerate(steps2):
        x = 20 + i * 122
        b += box(x, 112, 108, 36, t, '#fff7ed', ORANGE, fs=12)
        if i < 4: b += line(x + 108, 130, x + 120, 130, ORANGE, 2)
    b += f'<path d="M560 150 C 600 190, 40 190, 74 152" fill="none" stroke="{ORANGE}" stroke-width="2" marker-end="url(#ar{ORANGE[1:]})"/>'
    b += text(320, 196, 'repeat until the window is closed', ORANGE, s=11)
    b += text(20, 228, 'CLEANUP  (once)', TEAL, s=12, a='start', b=True)
    for i, t in enumerate(['glDeleteProgram', 'glfwTerminate']):
        x = 20 + i * 140
        b += box(x, 238, 126, 34, t, '#ecfdf5', TEAL, fs=12)
    b += line(562, 68, 562, 108, GRAY, 1.5, True, True)
    return svg(285, b, (BLUE, ORANGE, GRAY))
