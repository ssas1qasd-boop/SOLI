import sys
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK


def d15_hom():
    def m(rows, v, res, term):
        s = region(6, 16, 308, 74, 'M x v', PURPLE, '#f5f3ff')
        for i, r in enumerate(rows):
            for j, val in enumerate(r):
                s += cell(14 + j * 40, 26 + i * 20, 36, 18, val, 'hot' if j == 2 and i < 2 else 'n', 9)
        s += lbl(146, 56, 'x', INK, 12, 'middle', True)
        for i, val in enumerate(v): s += cell(158, 26 + i * 20, 36, 18, val, 'new', 9)
        s += lbl(210, 56, '=', INK, 12, 'middle', True)
        for i, val in enumerate(res): s += cell(224, 26 + i * 20, 50, 18, val, 'chg', 9)
        return s + termbox(6, 96, 308, term)
    M = [('0', '-1', '3'), ('1', '0', '2'), ('0', '0', '1')]
    f = [frame(1, 'Mat3 M = Multiply(T, R);', m(M, ('', '', ''), ('', '', ''), ['M = T(3, 2) R(90): [0, -1, 3] [1, 0, 2] [0, 0, 1]']), 'العمود التالت (الأصفر) = التحريك.', 124),
         frame(2, 'Apply(M, position)   // w = 1', m(M, ('1', '0', '1'), ('3', '3', '1'), ['position (1, 0, w = 1) -> (3, 3, w = 1)']), 'w = 1 بيضرب في العمود الأصفر: النقطة اتحركت.', 124),
         frame(3, 'Apply(M, direction)   // w = 0', m(M, ('1', '0', '0'), ('0', '1', '0'), ['direction (1, 0, w = 0) -> (0, 1, w = 0)']), 'w = 0: العمود الأصفر اتضرب في صفر. لف بس.', 124)]
    return story('نقطة واتجاه بنفس المصفوفة', 'البرنامج 2 · homogeneous.cpp', f)
