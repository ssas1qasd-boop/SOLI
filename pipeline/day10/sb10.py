# Week 3 Day 3 storyboards: each frame = the line that just ran + the state after it (values from the real runs).
import sys
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK

GARB = open('/home/claude/day10/src/p1_constructor.txt').read().splitlines()[0].split(': ')[1].split(', ')


def d10_ctor():
    def ent(rows):
        s = region(10, 16, 300, 26 + 38 * len(rows), 'STACK / HEAP')
        for r, (n, x, y, st, where) in enumerate(rows):
            yy = 34 + r * 38
            s += lbl(24, yy + 17, n, BLUE, 10.5, 'start', True) + lbl(24, yy + 30, where, GRAY, 8, 'start')
            s += cell(96, yy, 96, 26, x, st, 10) + cell(200, yy, 96, 26, y, st, 10)
        return s
    f = [frame(1, 'NoInit* raw = new NoInit;', ent([('raw', GARB[0], GARB[1], 'warn', 'heap')]) + lbl(196, 86, 'x            y', GRAY, 8.5),
               'مفيش Constructor: الأرقام اللي في المكان ده من قبل كده (بتتغير كل تشغيلة).', 100),
         frame(2, 'Entity e1;', ent([('e1', '0', '0', 'new', 'stack')]) + termbox(10, 62, 300, ['Entity() ran']),
               'الـ compiler نادى <code>Entity()</code> لوحده وحط أصفار.', 100),
         frame(3, 'Entity e2(10.0f, 5.0f);', ent([('e1', '0', '0', 'n', 'stack'), ('e2', '10', '5', 'new', 'stack')]) + termbox(10, 100, 300, ['Entity(float, float) ran']),
               'قوسين فيهم رقمين: اشتغل التاني، و <code>this-&gt;x = x</code> حط 10.', 138),
         frame(4, 'Entity* e3 = new Entity(3.0f, 4.0f);', ent([('e1', '0', '0', 'n', 'stack'), ('e2', '10', '5', 'n', 'stack'), ('*e3', '3', '4', 'new', 'heap')]),
               'على الـ Heap: نفس الـ Constructor برضه. وبعدين <code>delete e3;</code>.', 150)]
    return story('مين اللي اتنادى؟', 'البرنامج 1 · constructor.cpp', f)


def d10_dtor():
    def sc(stack, heap, term):
        s = region(8, 16, 148, 70, 'STACK', TEAL, '#ecfdf5') + region(164, 16, 148, 70, 'HEAP', ORANGE, '#fff7ed')
        for i, (n, st) in enumerate(stack):
            s += cell(16 + i * 70, 40, 64, 30, n, st, 10)
        for i, (n, st) in enumerate(heap):
            s += cell(172 + i * 70, 40, 64, 30, n, st, 10)
        return s + termbox(8, 94, 304, term)
    f = [frame(1, 'Function();   // Entity e;', sc([('e', 'new')], [], ['Function start', 'Created Entity!']),
               'e اتولد على الـ Stack جوه Function.', 136),
         frame(2, '}   // end of Function', sc([('e', 'free')], [], ['Function end', 'Destroyed Entity!']) + cross(16, 40, 64, 30),
               'وصلنا الـ <code>}</code>: الـ <code>~Entity</code> اشتغل لوحده.', 136),
         frame(3, 'Entity* heap = new Entity();', sc([('heap', 'ptr')], [('Entity', 'new')], ['Created Entity!', 'heap Entity still alive']) + arr(80, 55, 170, 55, BLUE),
               'على الـ Heap: هيفضل عايش لحد <code>delete</code>.', 136),
         frame(4, 'delete heap;', sc([('heap', 'ptr')], [('Entity', 'free')], ['Destroyed Entity!']) + cross(172, 40, 64, 30),
               'delete = الـ Destructor + رجّع المكان.', 136),
         frame(5, '{  Buffer b(16);', sc([('b', 'new')], [('16 floats', 'new')], ['Buffer(16): new float[16]', 'inside the { }: data[0] = 1.5']) + arr(80, 55, 170, 55, BLUE),
               'b على الـ Stack، والـ 16 رقم على الـ Heap.', 136),
         frame(6, '}   // end of the inner { }', sc([('b', 'free')], [('16 floats', 'free')], ['~Buffer(): delete[] 16 floats', 'after the { }']) + cross(16, 40, 64, 30) + cross(172, 40, 64, 30),
               'الـ <code>}</code>: الـ ~Buffer رجّع الـ 16 رقم. مفيش حاجة ضاعت (valgrind: 0).', 136)]
    return story('إمتى الـ object بيموت؟', 'البرنامج 2 · destructor.cpp', f)


def d10_brep():
    def counts(c, st, extra=None):
        s = region(10, 16, 300, 70, 'count[edge]')
        for i, v in enumerate(c):
            s += cell(30 + i * 92, 38, 76, 30, v, st[i], 12) + lbl(68 + i * 92, 82, f'e{i}', GRAY, 9)
        return s + (extra or '')
    f = [frame(1, 'loop 0 (top): e0+', counts(('1', '0', '0'), ('chg', 'n', 'n')), 'الغطا لمس الدايرة اللي فوق مرة.', 100),
         frame(2, 'loop 1 (side): e0- e1+ e2+ e1-', counts(('2', '2', '1'), ('chg', 'chg', 'chg')), 'الجنب لمس الدايرتين مرة، واللحام مرتين.', 100),
         frame(3, 'loop 2 (bottom): e2-', counts(('2', '2', '2'), ('n', 'n', 'chg')) + termbox(10, 96, 300, ['edge 0 is used 2 times  (ok: manifold)', 'V - E + F = 2']),
               'كل ضلع 2: الشكل مقفول (Manifold).', 150),
         frame(4, '(without the last e1-)', counts(('2', '1', '2'), ('n', 'warn', 'n')) + termbox(10, 96, 300, ['edge 1 is used 1 times  (NOT manifold)']),
               'التجربة: لو نسينا اللحام الراجع، ضلع 1 = 1: فيه فتحة.', 136)]
    return story('عدّ الأضلاع في الأسطوانة', 'البرنامج 1 · brep_cylinder.cpp', f)
