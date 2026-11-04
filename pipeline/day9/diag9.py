# Week 3 Day 2 diagrams (English labels inside the SVG; Arabic captions in HTML). All numbers from the real runs.
import sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, GREEN, RED, PINK


def s_visibility():
    """struct vs class: same members, only the default visibility differs; same 12 bytes (p1 output)"""
    b = ''
    for k, (kw, col, fill, dflt, wrote, ok) in enumerate([
            ('struct PlayerS', TEAL, '#ecfdf5', 'default: public', '(nothing written)', 's.x = 0;  works'),
            ('class PlayerC', PURPLE, '#f5f3ff', 'default: private', 'public:  (we wrote it)', 'c.x = 0;  works')]):
        x = 20 + k * 315
        b += f'<rect x="{x}" y="14" width="290" height="186" rx="10" fill="{fill}" stroke="{col}"/>'
        b += text(x + 145, 38, kw, col, 'middle', 14, True) + text(x + 145, 58, dflt, col, 'middle', 11.5, True)
        b += text(x + 20, 82, wrote, GRAY, 'start', 10.5)
        for i, t in enumerate(['int x, y;', 'int speed;', 'void Move(int xa, int ya)']):
            b += box(x + 20, 92 + i * 30, 250, 24, t, '#fff', col, False, fs=11)
        b += text(x + 145, 188, ok, INK, 'middle', 11, True)
    b += text(320, 226, 'output: struct x = 2, y = -2, sizeof = 12   |   class x = 2, y = -2, sizeof = 12', INK, 'middle', 11.5, True)
    b += text(320, 246, 'remove public: from the class (or add private: to the struct) -> "is private within this context"', RED, 'middle', 10.5)
    return svg(258, b, (TEAL,))


def v_layout():
    """Vertex square[4] in RAM: 64 bytes, stride 16, offset of u = 8, numbers[10] = square[2].u"""
    b = text(320, 20, 'Vertex square[4]  =  64 bytes  =  16 floats in a row', INK, 'middle', 12.5, True)
    W = 37
    for i in range(16):
        c, f = divmod(i, 4)
        x = 24 + i * W
        isuv = f >= 2
        hot = i == 10
        fill = '#fde68a' if hot else ('#ffedd5' if isuv else '#dbeafe')
        b += box(x, 44, W - 3, 34, 'xyuv'[f], fill, ORANGE if isuv else BLUE, hot, fs=12)
        b += text(x + (W - 3) / 2, 94, str(i), GRAY, 'middle', 9.5)
    for c in range(4):
        x = 24 + c * 4 * W
        b += f'<path d="M{x} 104 v8 h{4 * W - 3} v-8" fill="none" stroke="{INK}"/>' + text(x + 2 * W - 2, 128, f'square[{c}]', INK, 'middle', 10.5, True)
    b += line(24, 150, 24 + 4 * W - 3, 150, PURPLE) + text(24 + 2 * W, 168, 'stride = sizeof(Vertex) = 16', PURPLE, 'middle', 10.5, True)
    b += line(24, 186, 24 + 2 * W, 186, ORANGE) + text(24 + 2 * W + 6, 190, 'offsetof(Vertex, u) = 8', ORANGE, 'start', 10.5, True)
    b += line(24 + 10.5 * W, 34, 24 + 10.5 * W - 2, 40, RED, arrow=False)
    b += text(24 + 10.5 * W, 32, 'numbers[10] = square[2].u', RED, 'middle', 10.5, True)
    b += text(320, 222, 'so: glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, (void*)8)   (stride 16, offset 8)', INK, 'middle', 10.5)
    b += text(320, 242, 'the GPU sees only bytes: the names x, y, u, v stay in C++', GRAY, 'middle', 10.5)
    return svg(254, b, (PURPLE, ORANGE))


def t_pipeline():
    """file -> stbi_load (16x16x4 = 1024 bytes) -> glTexImage2D level 0 -> glGenerateMipmap 8,4,2,1 -> texture()"""
    b = box(14, 30, 108, 48, 'pixel_cat.png', '#fff7ed', ORANGE, True, fs=11)
    b += box(150, 30, 120, 48, '', '#fff', BLUE) + text(210, 50, 'stbi_load', BLUE, 'middle', 11.5, True) + text(210, 67, '16 x 16 x 4 = 1024 B', GRAY, 'middle', 9.5)
    b += box(298, 30, 130, 48, '', '#fff', PURPLE) + text(363, 50, 'glTexImage2D', PURPLE, 'middle', 11.5, True) + text(363, 67, 'level 0, GL_RGBA', GRAY, 'middle', 9.5)
    b += box(456, 30, 170, 48, '', '#fff', TEAL) + text(541, 50, 'glGenerateMipmap', TEAL, 'middle', 11.5, True) + text(541, 67, 'levels 1 to 4', GRAY, 'middle', 9.5)
    b += line(122, 54, 146, 54, BLUE) + line(270, 54, 294, 54, PURPLE) + line(428, 54, 452, 54, TEAL)
    x = 40
    for lv, s in enumerate([16, 8, 4, 2, 1]):
        px = s * 5 if s > 1 else 6
        b += f'<rect x="{x}" y="{196 - px}" width="{px}" height="{px}" fill="#ccfbf1" stroke="#0d9488"/>'
        b += text(x + px / 2, 214, f'{s}x{s}', TEAL, 'middle', 10, True) + text(x + px / 2, 228, f'level {lv}', GRAY, 'middle', 9)
        x += px + 34
    b += text(420, 120, 'MIN_FILTER = NEAREST_MIPMAP_NEAREST', INK, 'start', 10.5, True)
    b += text(420, 138, 'small on screen -> read a small level', GRAY, 'start', 10)
    b += text(420, 162, 'MAG_FILTER = NEAREST', INK, 'start', 10.5, True)
    b += text(420, 180, 'big on screen -> sharp squares', GRAY, 'start', 10)
    b += text(420, 204, 'no glGenerateMipmap -> black', RED, 'start', 10.5, True)
    b += text(320, 252, 'each level is half the one before: the GPU keeps all of them', INK, 'middle', 11.5, True)
    return svg(264, b, (BLUE, PURPLE, TEAL))


def t_wrap():
    """texCoord from -0.5 to 1.5: the middle is the image, the ring around it is decided by WRAP"""
    b = ''
    names = ['GL_REPEAT', 'GL_MIRRORED_REPEAT', 'GL_CLAMP_TO_EDGE', 'GL_CLAMP_TO_BORDER']
    what = ['copy again', 'copy, flipped', 'stretch the last pixel', 'one color (border)']
    for i in range(4):
        x = 16 + i * 156
        b += f'<rect x="{x}" y="20" width="140" height="140" fill="#f1f5f9" stroke="#94a3b8"/>'
        b += f'<rect x="{x + 35}" y="55" width="70" height="70" fill="#ffedd5" stroke="{ORANGE}" stroke-width="2"/>'
        b += text(x + 70, 94, '0..1', ORANGE, 'middle', 11, True)
        b += text(x + 70, 178, names[i], INK, 'middle', 10, True) + text(x + 70, 194, what[i], GRAY, 'middle', 9.5)
    b += text(16, 14, '-0.5', GRAY, 'start', 9) + text(156, 14, '1.5', GRAY, 'end', 9)
    b += text(320, 222, 'texCoord = aTex * 2.0 - 0.5  ->  from -0.5 to 1.5', INK, 'middle', 11.5, True)
    b += text(320, 242, 'the gray ring is outside the image: WRAP_S (across) and WRAP_T (up) decide its color', GRAY, 'middle', 10.5)
    return svg(254, b)


def m_mapping():
    """T: R3 -> R2, the two Khan examples, and the same thing as the matrix A (2 x 3)"""
    b = '<ellipse cx="120" cy="100" rx="96" ry="70" fill="#eff6ff" stroke="#2563eb"/>' + text(120, 22, 'R3 (3 numbers)', BLUE, 'middle', 12, True)
    b += '<ellipse cx="520" cy="100" rx="96" ry="70" fill="#fff7ed" stroke="#c2410c"/>' + text(520, 22, 'R2 (2 numbers)', ORANGE, 'middle', 12, True)
    for k, (a, c) in enumerate([('(1, 1, 1)', '(3, 3)'), ('(2, 4, 1)', '(10, 3)'), ('(0, 0, 0)', '(0, 0)')]):
        y = 66 + k * 34
        b += text(120, y + 4, a, INK, 'middle', 12, True) + text(520, y + 4, c, INK, 'middle', 12, True) + line(170, y, 470, y, PURPLE)
    b += text(320, 52, 'T(x1, x2, x3) = (x1 + 2 x2, 3 x3)', PURPLE, 'middle', 12, True)
    b += text(320, 200, 'A = [[1, 2, 0], [0, 0, 3]]   (2 rows = 2 outputs, 3 columns = 3 inputs)', INK, 'middle', 11.5, True)
    b += text(320, 222, 'A times (2, 4, 1) = (1*2 + 2*4 + 0*1,  0*2 + 0*4 + 3*1) = (10, 3)', GRAY, 'middle', 10.5)
    b += text(320, 244, 'yesterday\'s cube projection is the same kind: P is 2 x 3, R3 -> R2', TEAL, 'middle', 10.5, True)
    return svg(256, b, (PURPLE,))


def c_bary():
    """triangle (0,0) (4,0) (0,4), P = (1,1): the three small triangles; alpha = A0 / A (c1 output)"""
    def Q(x, y): return (40 + x * 50, 230 - y * 50)
    p0, p1, p2, p = Q(0, 0), Q(4, 0), Q(0, 4), Q(1, 1)
    def tri(a, c, d, f): return f'<polygon points="{a[0]},{a[1]} {c[0]},{c[1]} {d[0]},{d[1]}" fill="{f}" stroke="#fff" stroke-width="1.5"/>'
    b = tri(p, p1, p2, '#fecaca') + tri(p0, p, p2, '#bbf7d0') + tri(p0, p1, p, '#bfdbfe')
    b += f'<polygon points="{p0[0]},{p0[1]} {p1[0]},{p1[1]} {p2[0]},{p2[1]}" fill="none" stroke="{INK}" stroke-width="2"/>'
    for (pt, n, dx, dy) in [(p0, 'P0 (0,0)', -6, 18), (p1, 'P1 (4,0)', 0, 18), (p2, 'P2 (0,4)', 8, -4)]:
        b += f'<circle cx="{pt[0]}" cy="{pt[1]}" r="5" fill="{INK}"/>' + text(pt[0] + dx, pt[1] + dy, n, INK, 'start' if dx >= 0 else 'middle', 10.5, True)
    b += f'<circle cx="{p[0]}" cy="{p[1]}" r="5" fill="{PURPLE}"/>' + text(p[0] + 8, p[1] - 6, 'P (1,1)', PURPLE, 'start', 10.5, True)
    b += text(128, 168, 'A0', RED, 'middle', 11, True) + text(60, 150, 'A1', GREEN, 'middle', 11, True) + text(100, 218, 'A2', BLUE, 'middle', 11, True)
    rows = [('alpha = A0 / A = 0.5   (opposite P0)', RED), ('beta  = A1 / A = 0.25  (opposite P1)', GREEN), ('gamma = A2 / A = 0.25  (opposite P2)', BLUE),
            ('sum = 1  ->  P = 0.5 P0 + 0.25 P1 + 0.25 P2', INK), ('one of them negative  ->  outside', GRAY),
            ('color = alpha red + beta green + gamma blue', PURPLE)]
    for i, (t, c) in enumerate(rows):
        b += text(300, 50 + i * 30, t, c, 'start', 11.5, i in (3, 5))
    return svg(262, b)


def c_indexed():
    """cube as 12 triangles: face list 432 bytes vs indexed 240 bytes; E = 18 with std::set (c1 output)"""
    b = text(160, 22, 'face list (each triangle keeps its corners)', ORANGE, 'middle', 11, True)
    for i in range(36):
        b += f'<rect x="{20 + (i % 12) * 23}" y="{34 + (i // 12) * 22}" width="20" height="18" rx="3" fill="#ffedd5" stroke="#c2410c"/>'
    b += text(160, 116, '36 corners x 12 bytes = 432 bytes', ORANGE, 'middle', 11, True)
    b += text(480, 22, 'indexed (Indexed Face List)', TEAL, 'middle', 11, True)
    for i in range(8):
        b += box(340 + i * 35, 34, 31, 22, str(i), '#ccfbf1', TEAL, True, fs=10)
    for i in range(12):
        b += f'<rect x="{340 + (i % 6) * 47}" y="{66 + (i // 6) * 22}" width="43" height="18" rx="3" fill="#e0f2fe" stroke="#2563eb"/>'
    b += text(480, 116, '8 x 12 + 12 x 12 = 240 bytes', TEAL, 'middle', 11, True)
    b += text(320, 150, 'every inside edge belongs to 2 triangles:', INK, 'middle', 11.5, True)
    b += text(320, 172, 'std::set keeps it once  ->  E = 18,  V - E + F = 8 - 18 + 12 = 2', GREEN, 'middle', 11, True)
    b += text(320, 194, 'std::vector keeps both  ->  E = 36,  V - E + F = -16', RED, 'middle', 11)
    b += text(320, 222, 'the same idea as the EBO: vertices once, triangles point to them by number', GRAY, 'middle', 10.5)
    return svg(234, b)
