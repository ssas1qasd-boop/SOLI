# Week 3 Day 3 diagrams (English labels inside the SVG; Arabic captions in HTML). All numbers from the real runs.
import sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, GREEN, RED, PINK


def p_choose():
    """which constructor runs for each line of p1 (from the output)"""
    b = text(320, 22, 'the compiler picks the constructor from what is inside ( )', INK, 'middle', 12.5, True)
    rows = [('Entity e1;', 'Entity()', '0, 0'), ('Entity e2(10.0f, 5.0f);', 'Entity(float x, float y)', '10, 5'),
            ('new Entity(3.0f, 4.0f)', 'Entity(float x, float y)', '3, 4'), ('new NoInit', '(no constructor)', 'garbage')]
    for i, (call, ctor, outp) in enumerate(rows):
        y = 40 + i * 44
        bad = i == 3
        b += box(20, y, 200, 32, call, '#fff', BLUE, False, fs=11.5)
        b += line(222, y + 16, 272, y + 16, RED if bad else BLUE)
        b += box(276, y, 210, 32, ctor, '#fee2e2' if bad else '#dbeafe', RED if bad else BLUE, True, fs=11.5)
        b += line(488, y + 16, 528, y + 16, GRAY)
        b += box(532, y, 90, 32, outp, '#fef9c3' if bad else '#dcfce7', GRAY, True, fs=11.5)
    b += text(320, 232, 'Log l;  ->  error: use of deleted function Log::Log()   (Log() = delete)', RED, 'middle', 11)
    return svg(246, b, (BLUE, RED, GRAY))


def p_life():
    """lifetimes from p2's output: stack object dies at }, heap object dies at delete, Buffer dies at the inner }"""
    b = text(320, 20, 'time goes down: one row per line of output', INK, 'middle', 12, True)
    out = ['Function start', 'Created Entity!', 'Function end', 'Destroyed Entity!', 'back in main', 'Created Entity!',
           'heap Entity still alive', 'Destroyed Entity!', 'Buffer(16): new float[16]', 'inside the { }: data[0] = 1.5',
           '~Buffer(): delete[] 16 floats', 'after the { }']
    for i, t in enumerate(out):
        y = 36 + i * 22
        col = RED if 'Destroyed' in t or '~Buffer' in t else (TEAL if 'Created' in t or 'Buffer(' in t else INK)
        b += text(30, y + 14, t, col, 'start', 11, col != INK)
    for (a, z, x, name, c) in [(1, 3, 300, 'Entity e (stack)  dies at }', TEAL), (5, 7, 300, 'new Entity (heap)  dies at delete', ORANGE),
                                (8, 10, 300, 'Buffer b  dies at the inner }', PURPLE)]:
        y1, y2 = 36 + a * 22 + 4, 36 + z * 22 + 18
        b += f'<rect x="{x - 14}" y="{y1}" width="10" height="{y2 - y1}" rx="4" fill="{c}" opacity="0.85"/>'
        b += text(x + 6, (y1 + y2) / 2 + 4, name, c, 'start', 11.5, True)
    return svg(312, b, (BLUE,))


def t_class():
    """Texture class: constructor = load + upload, two objects in two units, destructor deletes (order 2 then 1)"""
    b = ''
    for k, (name, f, info, unit, col, fill) in enumerate([
            ('Texture crate', 'res/crate.png', '64 x 64, 3 ch -> GL_RGB, ID 1', 'GL_TEXTURE0', ORANGE, '#ffedd5'),
            ('Texture face', 'res/face.png', '32 x 32, 4 ch -> GL_RGBA, ID 2', 'GL_TEXTURE1', TEAL, '#ecfdf5')]):
        y = 20 + k * 92
        b += box(16, y, 150, 30, f, '#fff', GRAY, False, fs=11)
        b += line(168, y + 15, 196, y + 15, col)
        b += box(200, y - 6, 220, 74, '', fill, col)
        b += text(310, y + 14, name + '(path)', col, 'middle', 12, True)
        b += text(310, y + 34, 'constructor: stbi_load + glTexImage2D', INK, 'middle', 10.5)
        b += text(310, y + 52, info, INK, 'middle', 10.5, True)
        b += line(422, y + 15, 456, y + 15, col)
        b += box(460, y, 160, 30, unit + '  (Bind(' + str(k) + '))', '#fff', col, True, fs=11)
    b += box(200, 196, 420, 30, 'fragment: tex0 reads unit 0, tex1 reads unit 1  (glUniform1i)', '#eef2ff', BLUE, False, fs=11)
    b += text(320, 252, 'end of { }:  ~Texture() ID 2, then ~Texture() ID 1  (last made = first destroyed)', RED, 'middle', 11.5, True)
    return svg(266, b, (ORANGE, TEAL))


def m_columns():
    """Khan: put T(e1), T(e2) as columns -> A (3 x 2); A @ (1, 1) = (4, 4, 5)"""
    b = text(320, 20, 'T(x1, x2) = (x1 + 3x2,  5x2 - x1,  4x1 + x2)', INK, 'middle', 13, True)
    b += box(20, 46, 110, 30, 'e1 = (1, 0)', '#dbeafe', BLUE, True, fs=12) + box(20, 112, 110, 30, 'e2 = (0, 1)', '#ccfbf1', TEAL, True, fs=12)
    b += line(132, 61, 196, 61, BLUE) + line(132, 127, 196, 127, TEAL)
    b += box(200, 46, 130, 30, 'T(e1) = (1, -1, 4)', '#dbeafe', BLUE, False, fs=11.5) + box(200, 112, 130, 30, 'T(e2) = (3, 5, 1)', '#ccfbf1', TEAL, False, fs=11.5)
    b += line(332, 61, 400, 80, BLUE) + line(332, 127, 400, 108, TEAL)
    x0 = 410
    for c, (vals, col, fill) in enumerate([((1, -1, 4), BLUE, '#dbeafe'), ((3, 5, 1), TEAL, '#ccfbf1')]):
        for r, v in enumerate(vals):
            b += box(x0 + 8 + c * 52, 40 + r * 34, 46, 30, str(v), fill, col, True, fs=13)
    b += text(x0 - 6, 98, 'A =', INK, 'end', 14, True)
    b += f'<path d="M{x0 + 4} 38 L{x0} 38 L{x0} 144 L{x0 + 4} 144" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    b += f'<path d="M{x0 + 112} 38 L{x0 + 116} 38 L{x0 + 116} 144 L{x0 + 112} 144" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    b += text(x0 + 58, 162, '3 rows (output R3) x 2 columns (input R2)', GRAY, 'middle', 10.5)
    b += text(320, 196, 'A @ (1, 1) = 1 x column 1 + 1 x column 2 = (1+3, -1+5, 4+1) = (4, 4, 5) = T(1, 1)', ORANGE, 'middle', 12, True)
    return svg(212, b, (BLUE, TEAL))


def c_cyl():
    """cylinder B-Rep (Glen Gray): tree of shell/faces/loops/edges/vertices, and the side face unrolled in (u, v)"""
    b = box(20, 14, 120, 28, 'Shell', '#f5f3ff', PURPLE, True)
    faces = [('face 0: top', 'loop: e0+'), ('face 1: side', 'loop: e0- e1+ e2+ e1-'), ('face 2: bottom', 'loop: e2-')]
    for i, (f, l) in enumerate(faces):
        y = 58 + i * 50
        b += line(80, 42, 80, y + 14, PURPLE, 1.4, False) + line(80, y + 14, 100, y + 14, PURPLE, 1.4)
        b += box(104, y, 120, 28, f, '#fff', PURPLE, False, fs=11.5)
        b += box(232, y, 150, 28, l, '#fafafa', GRAY, False, fs=11)
    b += text(200, 226, 'e0 = circle z = 2,  e1 = seam line,  e2 = circle z = 0', INK, 'middle', 11)
    b += text(200, 244, 'V = 2, E = 3, F = 3:  V - E + F = 2', PURPLE, 'middle', 12, True)
    x, y, w, h = 420, 50, 190, 140
    b += text(x + w / 2, 30, 'face 1 unrolled: S(u, v)', INK, 'middle', 12, True)
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f5f3ff" stroke="none"/>'
    b += line(x + w, y, x, y, BLUE, 3) + text(x + w / 2, y - 6, 'e0 (top circle)', BLUE, 'middle', 10.5, True)
    b += line(x, y, x, y + h, ORANGE, 3) + text(x - 6, y + h / 2, 'e1', ORANGE, 'end', 11, True)
    b += line(x, y + h, x + w, y + h, TEAL, 3) + text(x + w / 2, y + h + 16, 'e2 (bottom circle)', TEAL, 'middle', 10.5, True)
    b += line(x + w, y + h, x + w, y, ORANGE, 3) + text(x + w + 6, y + h / 2, 'e1', ORANGE, 'start', 11, True)
    b += text(x + w / 2, y + h / 2 - 4, 'u: 0 -> 2 pi', GRAY, 'middle', 10.5) + text(x + w / 2, y + h / 2 + 12, 'v: 0 -> 2', GRAY, 'middle', 10.5)
    b += text(x + w / 2, 236, 'the seam e1 is used twice', ORANGE, 'middle', 11, True)
    return svg(258, b, (BLUE, ORANGE, TEAL, PURPLE))


def c_hole():
    """top face of the box: outer loop 4-5-6-7 + inner trim loop 12-15-14-13 (the hole)"""
    b = text(170, 20, 'top face = 1 surface + 2 loops', INK, 'middle', 12.5, True)
    b += '<rect x="40" y="36" width="260" height="200" fill="#f5f3ff" stroke="#7c3aed" stroke-width="3"/>'
    b += '<rect x="105" y="86" width="130" height="100" fill="#ffffff" stroke="#c2410c" stroke-width="3" stroke-dasharray="6 4"/>'
    for (px, py, n) in [(40, 236, '4'), (300, 236, '5'), (300, 36, '6'), (40, 36, '7'), (105, 186, '12'), (235, 186, '13'), (235, 86, '14'), (105, 86, '15')]:
        b += f'<circle cx="{px}" cy="{py}" r="4" fill="{INK}"/>' + text(px + (-10 if px < 170 else 10), py + (14 if py > 130 else -6), n, INK, 'middle', 11, True)
    b += text(170, 140, 'hole: not in the face', ORANGE, 'middle', 10.5, True)
    b += text(170, 58, 'outer loop', PURPLE, 'middle', 11, True)
    x = 350
    for i, (t, c) in enumerate([('box with a hole (from the run):', INK), ('V = 16, E = 24, F = 10, loops = 12', INK), ('V - E + F = 2   (looks like a cube!)', GRAY),
                                ('V - E + F - (loops - F) = 0', PURPLE), ('= 2 (S - G) = 2 (1 - 1): one hole through', PURPLE),
                                ('remove the 2 inner loops:', RED), ('8 edges used by 1 face -> not closed', RED)]):
        b += text(x, 60 + i * 26, t, c, 'start', 11.5, c != GRAY)
    return svg(254, b, (BLUE,))
