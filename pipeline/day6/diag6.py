# Day 6 diagrams (English labels inside the SVG; Arabic captions in HTML).
import sys, math
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, tag, GREEN, RED, PINK


def k_pipeline():
    """source -> tokens -> tree -> bytecode -> VM"""
    st = [('source', 'var x = 1 + 2 * 3;', BLUE, '#dbeafe'), ('tokens', '[var] [x] [=] [1] [+]', PURPLE, '#ede9fe'),
          ('tree (AST)', '+ with * under it', TEAL, '#ccfbf1'), ('bytecode', 'LOAD_INT 1, 2, 3', ORANGE, '#ffedd5'), ('VM', 'stack: [7]', GREEN, '#dcfce7')]
    b = ''
    for i, (t, sub, c, f) in enumerate(st):
        x = 6 + i * 128
        b += box(x, 34, 112, 54, '', f, c, True)
        b += text(x + 56, 56, t, c, s=12.5, b=True) + text(x + 56, 76, sub, INK, s=9.5)
        if i < 4: b += line(x + 113, 61, x + 126, 61, GRAY)
    for i, n in enumerate(['Scan()', 'Parser', 'Compile()', 'Run()']):
        x = 6 + i * 128 + 120
        b += text(x, 112, n, GRAY, s=10.5)
    b += text(320, 18, 'each stage turns one shape of the program into the next', GRAY, s=11)
    return svg(124, b, (GRAY,))


def k_trees():
    """1 + 2 * 3: right tree (7) vs wrong tree (9)"""
    def node(x, y, t, c, f):
        return f'<circle cx="{x}" cy="{y}" r="17" fill="{f}" stroke="{c}" stroke-width="2"/>' + text(x, y + 5, t, c, s=14, b=True)
    def edge(x1, y1, x2, y2, c): return f'<line x1="{x1}" y1="{y1 + 17}" x2="{x2}" y2="{y2 - 17}" stroke="{c}" stroke-width="2"/>'
    b = text(160, 20, 'Addition calls Multiplication', GREEN, s=12, b=True) + text(480, 20, 'levels swapped', RED, s=12, b=True)
    b += edge(160, 50, 100, 110, GREEN) + edge(160, 50, 220, 110, GREEN) + edge(220, 110, 180, 170, GREEN) + edge(220, 110, 260, 170, GREEN)
    b += node(160, 50, '+', GREEN, '#dcfce7') + node(100, 110, '1', INK, '#fff') + node(220, 110, '*', GREEN, '#dcfce7') + node(180, 170, '2', INK, '#fff') + node(260, 170, '3', INK, '#fff')
    b += text(160, 214, '1 + (2 * 3) = 7', GREEN, s=13, b=True)
    b += edge(480, 50, 420, 110, RED) + edge(480, 50, 540, 110, RED) + edge(420, 110, 380, 170, RED) + edge(420, 110, 460, 170, RED)
    b += node(480, 50, '*', RED, '#fee2e2') + node(420, 110, '+', RED, '#fee2e2') + node(540, 110, '3', INK, '#fff') + node(380, 170, '1', INK, '#fff') + node(460, 170, '2', INK, '#fff')
    b += text(480, 214, '(1 + 2) * 3 = 9', RED, s=13, b=True)
    b += '<line x1="320" y1="30" x2="320" y2="220" stroke="#e2e6ee"/>'
    return svg(226, b, (GREEN,))


def k_stack():
    ops = [('LOAD_INT 1', [1]), ('LOAD_INT 2', [1, 2]), ('LOAD_INT 3', [1, 2, 3]), ('MULTIPLY', [1, 6]), ('ADD', [7])]
    b = ''
    for i, (op, st) in enumerate(ops):
        x = 18 + i * 124
        b += text(x + 50, 18, op, ORANGE if op in ('MULTIPLY', 'ADD') else BLUE, s=11.5, b=True)
        b += f'<path d="M{x} 40 L{x} 160 L{x + 100} 160 L{x + 100} 40" fill="none" stroke="#94a3b8" stroke-width="2"/>'
        for j, v in enumerate(st):
            new = j == len(st) - 1
            b += box(x + 10, 128 - j * 32, 80, 28, str(v), '#ffedd5' if new and op in ('MULTIPLY', 'ADD') else ('#dbeafe' if new else '#f8fafc'), ORANGE if new and op in ('MULTIPLY', 'ADD') else BLUE, new, fs=14)
        if i < 4: b += line(x + 104, 100, x + 120, 100, GRAY)
    b += text(320, 184, 'push puts on top, an operation pops two and pushes one', GRAY, s=11)
    return svg(194, b, (GRAY,))


def u_one_vs_many():
    """attribute: one value per corner. uniform: one value for the whole draw."""
    b = text(160, 18, 'attribute: one per corner', BLUE, s=12, b=True) + text(480, 18, 'uniform: one for the whole draw', PURPLE, s=12, b=True)
    pts = [(70, 160), (250, 160), (250, 50), (70, 50)]
    b += f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="#eef2ff" stroke="{BLUE}" stroke-width="1.5"/>'
    for k, (x, y) in enumerate(pts):
        b += f'<circle cx="{x}" cy="{y}" r="7" fill="{BLUE}"/>' + text(x + (-30 if x < 160 else 32), y + (16 if y > 100 else -6), f'pos {k}', BLUE, s=10.5, b=True)
    pts2 = [(390, 160), (570, 160), (570, 50), (390, 50)]
    b += f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts2)}" fill="#b05fd3" stroke="{PURPLE}" stroke-width="1.5"/>'
    b += box(430, 88, 100, 34, 'u_Color', '#fff', PURPLE, True, tc=PURPLE)
    b += text(480, 190, 'glUniform4f(location, r, 0.3, 0.8, 1)', PURPLE, s=11)
    b += text(160, 190, 'glVertexAttribPointer(0, 2, ...)', BLUE, s=11)
    return svg(200, b, (BLUE,))


def u_zigzag():
    """r over frames: 0 -> 1 -> 0 (with flip) vs 0 -> 8.5 clamped (without)."""
    b = '<line x1="50" y1="150" x2="620" y2="150" stroke="#cbd5e1"/><line x1="50" y1="20" x2="50" y2="150" stroke="#cbd5e1"/>'
    b += text(40, 154, '0', GRAY, 'end', 10) + text(40, 64, '1', GRAY, 'end', 10) + '<line x1="50" y1="60" x2="620" y2="60" stroke="#e2e8f0" stroke-dasharray="4 4"/>'
    r, inc, P, Q = 0.0, 0.05, [], []
    rr = 0.0
    for f in range(110):
        x = 50 + f * 5.1
        P.append(f'{x:.1f},{150 - r * 90:.1f}'); Q.append(f'{x:.1f},{150 - min(rr, 1.0) * 90:.1f}')
        if r > 1.0: inc = -0.05
        elif r < 0.0: inc = 0.05
        r += inc; rr += 0.05
    b += f'<polyline points="{" ".join(Q)}" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="6 4"/>'
    b += f'<polyline points="{" ".join(P)}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>'
    b += text(335, 176, 'frames', GRAY, s=11) + text(60, 16, 'red (r) sent with glUniform4f', INK, 'start', 11)
    b += text(612, 48, 'without the if: stuck at 1 (clamped)', RED, 'end', 10.5, True) + text(612, 140, 'with the if: 0 -> 1 -> 0', BLUE, 'end', 10.5, True)
    return svg(184, b, (BLUE,))


def u_time_flow():
    b = ''
    items = [('CPU', 'glfwGetTime() = 1.44', '#ffedd5', ORANGE), ('uniform', 'u_Time = 1.44', '#ede9fe', PURPLE), ('fragment x many', 'sin(u_Time + x*3) per pixel', '#dbeafe', BLUE)]
    for i, (t, s, f, c) in enumerate(items):
        x = 14 + i * 212
        b += box(x, 30, 190, 58, '', f, c, True) + text(x + 95, 52, t, c, s=12.5, b=True) + text(x + 95, 74, s, INK, s=10.5)
        if i < 2: b += line(x + 192, 59, x + 210, 59, GRAY)
    b += text(320, 112, 'one number per frame from the CPU, a different colour per pixel on the GPU', GRAY, s=11)
    return svg(122, b, (GRAY,))


def m_pythagoras():
    o = (90, 180); s = 30
    ax, ay = o[0] + 2 * s, o[1] - 5 * s
    b = f'<line x1="{o[0]}" y1="{o[1]}" x2="{o[0] + 2 * s}" y2="{o[1]}" stroke="{ORANGE}" stroke-width="3"/>'
    b += f'<line x1="{o[0] + 2 * s}" y1="{o[1]}" x2="{ax}" y2="{ay}" stroke="{TEAL}" stroke-width="3"/>'
    b += f'<line x1="{o[0]}" y1="{o[1]}" x2="{ax}" y2="{ay}" stroke="{BLUE}" stroke-width="3" marker-end="url(#ar{BLUE[1:]})"/>'
    b += text(o[0] + s, o[1] + 20, '2', ORANGE, s=14, b=True) + text(ax + 16, o[1] - 2.5 * s, '5', TEAL, s=14, b=True) + text(o[0] + 6, o[1] - 2.8 * s, '|a|', BLUE, 'end', 14, True)
    b += text(200, 30, 'a = [2, 5]', BLUE, 'start', 14, True)
    b += text(200, 64, '|a|² = 2² + 5² = 29', INK, 'start', 13)
    b += text(200, 92, 'a · a = 2·2 + 5·5 = 29', INK, 'start', 13)
    b += text(200, 126, '|a| = √29 ≈ 5.385', BLUE, 'start', 14, True)
    b += text(200, 160, 'same formula for 3, 50 or 1000 numbers', GRAY, 'start', 11)
    return svg(200, b, (BLUE,))


def c_layers():
    b = text(160, 18, 'before: callbacks do everything', RED, s=12, b=True) + text(480, 18, 'after: small named actions', GREEN, s=12, b=True)
    b += box(30, 34, 260, 70, 'MouseButtonCallback (22 lines)', '#fee2e2', RED, True, fs=11.5)
    b += box(30, 112, 260, 70, 'KeyCallback (24 lines)', '#fee2e2', RED, True, fs=11.5)
    b += box(30, 190, 260, 34, 'while loop: clear, 2 colours, 2 draws', '#fee2e2', RED, fs=11)
    b += box(350, 34, 120, 34, 'Mouse callback', '#f1f5f9', GRAY, fs=11) + box(350, 80, 120, 34, 'Key callback', '#f1f5f9', GRAY, fs=11)
    b += box(500, 34, 120, 26, 'AddPoint', '#dcfce7', GREEN, True, fs=11) + box(500, 64, 120, 26, 'FinishLine', '#dcfce7', GREEN, True, fs=11) + box(500, 94, 120, 26, 'DeleteLastLine', '#dcfce7', GREEN, True, fs=11)
    b += line(471, 46, 498, 46, GREEN) + line(471, 52, 498, 76, GREEN) + line(471, 97, 498, 106, GREEN)
    b += box(500, 140, 120, 26, 'StartNewLine', '#ecfccb', GREEN, fs=11) + box(500, 170, 120, 26, 'UploadPoints', '#ecfccb', GREEN, fs=11)
    b += box(350, 190, 120, 34, 'DrawScene', '#dcfce7', GREEN, True, fs=11) + text(560, 218, 'SetColor, PointCount', GREEN, s=10.5)
    b += '<line x1="320" y1="30" x2="320" y2="226" stroke="#e2e6ee"/>'
    return svg(232, b, (GREEN,))
