# Day 3 illustrative diagrams (English labels; Arabic captions in HTML).
import sys
sys.path.insert(0, '/home/claude/day1')
from diagrams import box, text, line, arrowdefs, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
GREEN, RED, PINK = '#16a34a', '#dc2626', '#db2777'

def svg(h, body, cols=(BLUE,)):
    return (f'<svg width="100%" viewBox="0 0 640 {h}" xmlns="http://www.w3.org/2000/svg" direction="ltr" style="direction:ltr">'
            f'{arrowdefs(*cols)}<g font-size="13" fill="{INK}">{body}</g></svg>')

def tag(x, y, t, c):
    return (f'<rect x="{x}" y="{y}" width="{len(t) * 9 + 18}" height="24" rx="12" fill="#fff" stroke="{c}" stroke-width="1.5"/>'
            + text(x + (len(t) * 9 + 18) / 2, y + 16.5, t, c, s=12, b=True))

# ---------------------------------------------------------------- references
def r_alias():
    b = text(160, 20, 'reference:  int& ref = a;', BLUE, s=12, b=True) + text(480, 20, 'pointer:  int* ptr = &a;', PURPLE, s=12, b=True)
    b += box(110, 60, 100, 55, '2', '#dbeafe', BLUE, True)
    b += tag(70, 125, 'a', BLUE) + tag(160, 125, 'ref', BLUE)
    b += text(160, 175, 'ONE box, two names', BLUE, s=11) + text(160, 190, '&a == &ref', GRAY, s=11)
    b += f'<line x1="320" y1="35" x2="320" y2="195" stroke="#e2e6ee"/>'
    b += box(370, 60, 90, 55, '2', '#dbeafe', BLUE, True) + text(415, 135, 'a', BLUE, s=12, b=True)
    b += box(510, 60, 100, 55, '&a', '#fff', PURPLE, True, True, PURPLE) + text(560, 135, 'ptr', PURPLE, s=12, b=True)
    b += line(510, 87, 462, 87, PURPLE)
    b += text(490, 175, 'TWO boxes: ptr holds the address', PURPLE, s=11)
    return svg(200, b, (BLUE, PURPLE))

def r_three():
    b = ''
    cols = [('IncrementCopy(int value)', 'copy', ORANGE, '5'), ('IncrementPointer(int* value)', 'address', PURPLE, '6'), ('IncrementReference(int& value)', 'same box', BLUE, '7')]
    for i, (sig, how, c, res) in enumerate(cols):
        x = 15 + i * 210
        b += text(x + 95, 20, sig, c, s=10.5, b=True)
        b += box(x + 10, 40, 70, 40, 'a', '#dbeafe', BLUE, True) + text(x + 45, 98, 'main', GRAY, s=10)
        if i == 0:
            b += box(x + 110, 40, 70, 40, 'value', '#fff7ed', ORANGE, True, tc=ORANGE, fs=11) + line(x + 82, 60, x + 108, 60, ORANGE)
            b += text(x + 145, 98, 'a new box', ORANGE, s=10)
        elif i == 1:
            b += box(x + 110, 40, 70, 40, '&a', '#fff', PURPLE, True, True, PURPLE) + line(x + 110, 60, x + 82, 60, PURPLE)
            b += text(x + 145, 98, 'holds the address', PURPLE, s=10)
        else:
            b += tag(x + 100, 48, 'value', BLUE) + text(x + 145, 98, 'just another name', BLUE, s=10)
        b += text(x + 95, 125, f'a after: {res}', GREEN if res != '5' else RED, s=12, b=True)
    return svg(135, b, (ORANGE, PURPLE))

# ---------------------------------------------------------------- hamming
def h_strands():
    a, c = 'GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT'
    b = text(18, 50, 'lhs', GRAY, 'start', 11) + text(18, 92, 'rhs', GRAY, 'start', 11)
    for i in range(18):
        x = 50 + i * 32
        if i == 17:
            b += box(x, 32, 28, 28, '\\0', '#f3f4f6', '#d1d5db', tc=GRAY, fs=10) + box(x, 74, 28, 28, '\\0', '#f3f4f6', '#d1d5db', tc=GRAY, fs=10)
            continue
        diff = a[i] != c[i]
        f, s = ('#fee2e2', RED) if diff else (SOFT, '#c9d1de')
        b += box(x, 32, 28, 28, a[i], f, s, diff, fs=12) + box(x, 74, 28, 28, c[i], f, s, diff, fs=12)
        if diff: b += text(x + 14, 120, '^', RED, s=12, b=True)
    b += text(320, 18, 'compare letter by letter; red = different', GRAY, s=11)
    b += text(320, 142, '7 differences  ->  Hamming distance = 7', RED, s=12, b=True)
    return svg(150, b)

# ---------------------------------------------------------------- shader file
def s_split():
    lines = [('#shader vertex', 'mark'), ('#version 330 core', 'v'), ('layout(location = 0) in vec4 position;', 'v'), ('void main() { gl_Position = position; }', 'v'),
             ('#shader fragment', 'mark'), ('#version 330 core', 'f'), ('layout(location = 0) out vec4 color;', 'f'), ('void main() { color = vec4(0.2, 0.3, 0.8, 1.0); }', 'f')]
    b = text(130, 18, 'res/shaders/Basic.shader', GRAY, s=11, b=True)
    for i, (t, k) in enumerate(lines):
        y = 28 + i * 24
        c = {'mark': ORANGE, 'v': BLUE, 'f': TEAL}[k]
        f = {'mark': '#fff7ed', 'v': '#dbeafe', 'f': '#ccfbf1'}[k]
        b += f'<rect x="10" y="{y}" width="250" height="21" rx="3" fill="{f}" stroke="{c}" stroke-width=".8"/>'
        b += f'<text x="16" y="{y + 15}" font-size="9.5" font-family="DejaVu Sans Mono, monospace" fill="{INK}">{t}</text>'
    b += box(300, 95, 110, 50, 'ParseShader', '#f5f3ff', PURPLE, True, tc=PURPLE, fs=12)
    b += line(262, 120, 298, 120, PURPLE)
    b += box(460, 45, 165, 50, 'ss[0]  VertexSource', '#dbeafe', BLUE, True, fs=11) + box(460, 145, 165, 50, 'ss[1]  FragmentSource', '#ccfbf1', TEAL, True, fs=11)
    b += line(412, 112, 458, 72, BLUE) + line(412, 128, 458, 168, TEAL)
    b += text(320, 238, 'the orange "#shader" lines only switch the target; they are never copied', ORANGE, s=11)
    return svg(248, b, (PURPLE, BLUE, TEAL))

# ---------------------------------------------------------------- cross product
def x_parallelogram():
    O = (190, 150); s = 32
    P = lambda x, y: (O[0] + x * s, O[1] - y * s)
    v, w = (-3, 1), (2, 1)
    vx, vy = P(*v); wx, wy = P(*w); sx, sy = P(v[0] + w[0], v[1] + w[1])
    b = ''.join(f'<line x1="{O[0] + i * s}" y1="20" x2="{O[0] + i * s}" y2="180" stroke="#eef1f6"/>' for i in range(-5, 5))
    b += ''.join(f'<line x1="20" y1="{O[1] - j * s}" x2="360" y2="{O[1] - j * s}" stroke="#eef1f6"/>' for j in range(-1, 5))
    b += f'<polygon points="{O[0]},{O[1]} {vx},{vy} {sx},{sy} {wx},{wy}" fill="#fde68a" fill-opacity=".6" stroke="#d97706"/>'
    b += line(O[0], O[1], vx, vy, ORANGE, 2.5) + text(vx - 8, vy - 6, 'v = (-3, 1)', ORANGE, 'end', 12, True)
    b += line(O[0], O[1], wx, wy, BLUE, 2.5) + text(wx + 6, wy + 16, 'w = (2, 1)', BLUE, 'start', 12, True)
    b += text(O[0] - 20, O[1] - 40, 'area 5', '#92400e', s=12, b=True)
    b += text(510, 45, 'v x w = (-3)(1) - (1)(2)', INK, s=13) + text(510, 72, '= -5', RED, s=16, b=True)
    b += text(510, 100, 'minus: v is on the LEFT of w', GRAY, s=11)
    b += text(510, 135, 'w x v = +5', GREEN, s=14, b=True) + text(510, 157, '(swap the order -> flip the sign)', GRAY, s=11)
    return svg(190, b, (ORANGE, BLUE))

def x_3d():
    # simple oblique axes
    O = (200, 140)
    b = line(O[0], O[1], O[0], 30, GRAY, 1.5) + text(O[0], 22, 'y', GRAY, s=12)
    b += line(O[0], O[1], O[0] - 90, O[1] + 60, GRAY, 1.5) + text(O[0] - 98, O[1] + 72, 'z', GRAY, s=12)
    b += line(O[0], O[1], 340, O[1], GRAY, 1.5) + text(350, O[1] + 4, 'x', GRAY, s=12)
    b += line(O[0], O[1], O[0] - 60, O[1] + 40, ORANGE, 3) + text(O[0] - 66, O[1] + 30, 'v = (0,0,2)', ORANGE, 'end', 12, True)
    b += line(O[0], O[1], O[0], O[1] - 70, BLUE, 3) + text(O[0] + 8, O[1] - 60, 'w = (0,2,0)', BLUE, 'start', 12, True)
    b += line(O[0], O[1], O[0] - 140, O[1], RED, 3) + text(O[0] - 140, O[1] - 10, 'v x w = (-4,0,0)', RED, 'start', 12, True)
    b += text(500, 45, 'length = area of the square = 2 x 2 = 4', INK, s=12)
    b += text(500, 75, 'direction = perpendicular to both', INK, s=12)
    b += text(500, 105, 'right hand: index -> v, middle -> w,', GRAY, s=11)
    b += text(500, 122, 'thumb -> v x w  (here: toward -x)', GRAY, s=11)
    b += text(500, 160, 'check: (v x w) . v = 0  and  (v x w) . w = 0', GREEN, s=11, b=True)
    return svg(210, b, (GRAY, ORANGE, BLUE, RED))

# ---------------------------------------------------------------- CAD
def l_pixels():
    b = box(30, 30, 240, 180, '', '#0b0f17', '#334155')
    b += text(150, 22, 'GLFW: pixels', GRAY, s=12, b=True)
    b += text(36, 48, '(0, 0)', '#93c5fd', 'start', 11) + text(264, 204, '(640, 480)', '#93c5fd', 'end', 11)
    b += f'<circle cx="80" cy="170" r="5" fill="#f97316"/>' + text(88, 166, '(100, 380)', '#fdba74', 'start', 10.5)
    b += line(285, 120, 345, 120, PURPLE) + text(315, 108, 'convert', PURPLE, s=11)
    b += box(360, 30, 240, 180, '', '#0b0f17', '#334155')
    b += text(480, 22, 'OpenGL: -1 .. +1', GRAY, s=12, b=True)
    b += f'<line x1="480" y1="30" x2="480" y2="210" stroke="#334155"/><line x1="360" y1="120" x2="600" y2="120" stroke="#334155"/>'
    b += text(366, 116, '-1', '#93c5fd', 'start', 11) + text(596, 116, '+1', '#93c5fd', 'end', 11) + text(484, 44, '+1', '#93c5fd', 'start', 11) + text(484, 206, '-1', '#93c5fd', 'start', 11)
    b += f'<circle cx="397" cy="172" r="5" fill="#f97316"/>' + text(405, 168, '(-0.69, -0.58)', '#fdba74', 'start', 10.5)
    b += text(170, 235, 'x = 2*px/width - 1', INK, s=12, b=True) + text(470, 235, 'y = 1 - 2*py/height  (flipped)', INK, s=12, b=True)
    return svg(245, b, (PURPLE,))

def l_pipeline():
    steps = [('click', 'mouse callback', ORANGE), ('push_back(x, y)', 'std::vector<float>', BLUE), ('glBufferData', 'copy to GPU', TEAL), ('glDrawArrays', 'GL_LINES + GL_POINTS', PURPLE)]
    b = ''
    for i, (t, s, c) in enumerate(steps):
        x = 10 + i * 158
        b += box(x, 30, 140, 50, t, '#fff', c, True, tc=c, fs=12) + text(x + 70, 98, s, GRAY, s=10.5)
        if i < 3: b += line(x + 142, 55, x + 156, 55, c)
    return svg(110, b, (ORANGE, BLUE, TEAL))
