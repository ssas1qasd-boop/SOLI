# Week 3 Day 4 storyboards: each frame = the line that just ran + the state after it (values from the real runs).
import sys, re
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK

P1 = open('/home/claude/day11/src/p1_stack_heap.txt').read()
A = dict(re.findall(r'(&?\w+) = (0x[0-9a-f]+)', P1))
def short(a): return '…' + a[-4:]


def d11_mem():
    def sc(stack, heap, term=None, extra=''):
        s = region(6, 16, 150, 112, 'STACK', TEAL, '#ecfdf5') + region(164, 16, 150, 112, 'HEAP', ORANGE, '#fff7ed')
        for i, (n, v, st) in enumerate(stack):
            s += lbl(14, 42 + i * 30, n, TEAL, 8.5, 'start', True) + cell(66, 28 + i * 30, 84, 24, v, st, 9.5)
        for i, (n, v, st) in enumerate(heap):
            s += lbl(172, 42 + i * 30, n, ORANGE, 8.5, 'start', True) + cell(226, 28 + i * 30, 84, 24, v, st, 9.5)
        if term: s += termbox(6, 134, 308, term)
        return s + extra
    f = [frame(1, 'int value = 5;  int array[5];  Vector3 vector;', sc([('value', '5', 'new'), ('vector', '10 11 12', 'new'), ('array', '2 2 2 2 2', 'new')], []),
               'التلاتة على الـ Stack ورا بعض. الـ Stack Pointer اتحرك 4 + 12 + 20 بايت.', 132),
         frame(2, 'int* hvalue = new int;  *hvalue = 5;', sc([('value', '5', 'n'), ('vector', '10 11 12', 'n'), ('hvalue', short(A['hvalue']), 'ptr')], [('', '5', 'new')]) + arr(150, 40, 224, 40, ORANGE),
               'الـ Pointer على الـ Stack، والـ 5 على الـ Heap عند ' + A['hvalue'] + '.', 132),
         frame(3, 'new int[5];  new Vector3();', sc([('hvalue', short(A['hvalue']), 'ptr'), ('harray', short(A['harray']), 'ptr'), ('hvector', short(A['hvector']), 'ptr')],
                                                   [('+0', '5', 'n'), ('+32', '2 2 2 2 2', 'new'), ('+64', '10 11 12', 'new')]),
               'كل حاجة على الـ Heap بعد 32 بايت من اللي قبلها، مع إن الأحجام 4 و 20 و 12.', 132),
         frame(4, 'delete hvalue;  delete[] harray;  delete hvector;', sc([('hvalue', short(A['hvalue']), 'ptr'), ('harray', short(A['harray']), 'ptr'), ('hvector', short(A['hvector']), 'ptr')],
                                                   [('', '5', 'free'), ('', '2 2 2 2 2', 'free'), ('', '10 11 12', 'free')]) + cross(226, 28, 84, 84),
               'رجعوا للـ Heap. والـ Stack هيترجع لوحده عند الـ <code>}</code> بتاعة main (valgrind: 0 بايت ضايعين).', 132)]
    return story('الـ Stack والـ Heap في الرام', 'البرنامج 1 · stack_heap.cpp', f)


def d11_wrap():
    def nums(rows, hl=None):
        s = region(10, 16, 300, 26 + 30 * len(rows), 'u  ->  u used')
        for i, (name, a, b) in enumerate(rows):
            y = 36 + i * 30
            s += lbl(20, y + 15, name, BLUE, 10, 'start', True) + cell(130, y, 70, 24, a, 'n', 11) + arr(202, y + 12, 226, y + 12, GRAY) + cell(230, y, 70, 24, b, 'chg' if hl == i else 'n', 11)
        return s
    f = [frame(1, 'mode 1: uv - floor(uv)', nums([('u = 1.3', '1.3', '0.3'), ('u = -0.3', '-0.3', '0.7')], 1), 'floor(‎-0.3) = ‎-1، فالنتيجة 0.7: نفس مكان 0.7 في الصورة.', 110),
         frame(2, 'mode 2: 1 - |mod(u, 2) - 1|', nums([('u = 0.4', '0.4', '0.4'), ('u = 1.3', '1.3', '0.7')], 1), 'من 1 لـ 2 بتمشي بالعكس: 1.3 بقت 0.7.', 110),
         frame(3, 'mode 3: clamp(uv, 0, 1)', nums([('u = -0.3', '-0.3', '0'), ('u = 1.3', '1.3', '1')], 0), 'برّه الصورة = لون الحرف.', 110),
         frame(4, 'top row (card) vs bottom row (Wrap)', region(10, 16, 300, 80, 'pixels compared') + lbl(160, 50, '0 of 72,384 pixels differ', GREEN, 13, 'middle', True) + lbl(160, 76, 'in each of the 3 columns', GRAY, 10),
               'قارنّا صورة الشباك: الصفين متطابقين بكسل ببكسل.', 110)]
    return story('دالة Wrap بالأرقام', 'البرنامج 1 · wrap_by_hand.cpp', f)
