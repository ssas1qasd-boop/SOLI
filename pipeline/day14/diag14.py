# Week 3 Day 7 diagrams (English labels inside the SVG; Arabic captions in HTML). All numbers from the real runs.
import sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day3')
from diagrams import box, text, line, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT
from diag3 import svg, GREEN, RED, PINK


def p_shallow():
    """shallow copy: two Strings, one buffer; deep copy: two buffers"""
    b = text(160, 22, 'shallow copy (default)', RED, 'middle', 12.5, True) + text(480, 22, 'deep copy (our copy constructor)', GREEN, 'middle', 12.5, True)
    b += box(30, 44, 110, 44, 'string', '#dbeafe', BLUE, True) + box(30, 110, 110, 44, 'second', '#dbeafe', BLUE, True)
    b += box(200, 76, 110, 44, 'C h a r n o', '#fee2e2', RED, True, fs=11.5)
    b += line(140, 66, 200, 92, RED) + line(140, 132, 200, 104, RED)
    b += text(160, 182, 'same buffer: both print Charno', RED, 'middle', 11) + text(160, 200, '2 x delete[] -> double free', RED, 'middle', 11, True)
    b += box(350, 44, 110, 44, 'string', '#dbeafe', BLUE, True) + box(350, 110, 110, 44, 'second', '#dbeafe', BLUE, True)
    b += box(520, 44, 110, 44, 'C h e r n o', '#dcfce7', GREEN, True, fs=11.5) + box(520, 110, 110, 44, 'C h a r n o', '#dcfce7', GREEN, True, fs=11.5)
    b += line(460, 66, 520, 66, GREEN) + line(460, 132, 520, 132, GREEN)
    b += text(480, 182, 'two buffers: Cherno / Charno', GREEN, 'middle', 11) + text(480, 200, 'each destructor deletes its own', GREEN, 'middle', 11, True)
    return svg(214, b, (RED, GREEN))


def t_copy():
    """Describe(Texture) by value: the copy dies and deletes id 2"""
    b = ''
    steps = [('Texture blue  (id 2)', BLUE, '#dbeafe'), ('Describe(blue): copy with id 2', ORANGE, '#ffedd5'), ('copy dies: glDeleteTextures(id 2)', RED, '#fee2e2'), ('blue.id = 2, but glIsTexture(2) = 0', RED, '#fee2e2'), ('Bind(2): GL_INVALID_OPERATION -> red stays bound', RED, '#fee2e2')]
    for i, (t, c, f) in enumerate(steps):
        y = 20 + i * 44
        b += box(120, y, 400, 34, t, f, c, True, fs=12)
        if i: b += line(320, y - 10, 320, y, c)
    b += text(320, 248, 'fix: Describe(const Texture&)  and  Texture(const Texture&) = delete', GREEN, 'middle', 12, True)
    return svg(262, b, (BLUE, ORANGE, RED))


def m_det():
    """unit square -> parallelogram (area 2 = det) and -> line (det 0)"""
    def P(x, y, ox): return ox + x * 46, 222 - y * 30
    b = ''
    for k, (name, pts, col, note) in enumerate([('A = [[2, 1], [0, 1]]', [(0, 0), (2, 0), (3, 1), (1, 1)], ORANGE, 'area 2 = det(A)'), ('B = [[1, 2], [2, 4]]', [(0, 0), (1, 2), (3, 6), (2, 4)], PURPLE, 'area 0 = det(B): a line')]):
        ox = 60 + k * 320
        b += text(ox + 90, 22, name, col, 'middle', 12, True)
        sq = ' '.join('%.0f,%.0f' % P(x, y, ox) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)])
        b += f'<polygon points="{sq}" fill="#e5e7eb" stroke="#9ca3af"/>'
        pp = ' '.join('%.0f,%.0f' % P(x, y, ox) for x, y in pts)
        b += f'<polygon points="{pp}" fill="{col}" fill-opacity="0.35" stroke="{col}" stroke-width="2"/>'
        b += text(ox + 90, 248, note, col, 'middle', 11.5, True)
    return svg(262, b, (BLUE,))


def c_git():
    """working folder -> staging -> commits; v1..v4 and checkout back to v1"""
    b = ''
    for i, (t, c) in enumerate([('working folder', BLUE), ('staging area', ORANGE), ('repository (.git)', PURPLE)]):
        b += box(20 + i * 210, 30, 180, 40, t, '#f8fafc', c, True)
    b += line(200, 50, 230, 50, ORANGE) + text(215, 90, 'git add', ORANGE, 'middle', 11, True)
    b += line(410, 50, 440, 50, PURPLE) + text(425, 90, 'git commit', PURPLE, 'middle', 11, True)
    commits = [('372ae88', 'v1 blue', '#2563eb'), ('a25f620', 'v2 pink', '#db2777'), ('e846659', 'v3 green', '#16a34a'), ('c03766c', 'v4 orange', '#ea580c')]
    for i, (h, t, c) in enumerate(commits):
        x = 70 + i * 140
        b += f'<circle cx="{x}" cy="150" r="14" fill="{c}"/>' + text(x, 182, h, INK, 'middle', 10.5, True) + text(x, 198, t, GRAY, 'middle', 10.5)
        if i: b += line(x - 126, 150, x - 14, 150, GRAY, 1.6, False)
    b += f'<path d="M 490 132 Q 280 92 78 132" fill="none" stroke="{RED}" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#ar{RED[1:]})"/>'
    b += text(280, 110, 'git checkout 372ae88 -- site.css  (back to blue)', RED, 'middle', 11, True)
    b += text(320, 226, 'one folder, 4 versions. same content = same hash = stored once', TEAL, 'middle', 11.5, True)
    return svg(240, b, (ORANGE, PURPLE, RED))
