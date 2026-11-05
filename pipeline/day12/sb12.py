# Week 3 Day 5 storyboards: each frame = the line that just ran + the state after it (values from the real runs).
import sys, re
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK

P2 = open('/home/claude/day12/src/p2_placement.txt').read()
B = re.search(r'new int\[50\] at (0x[0-9a-f]+)', P2).group(1)
H = re.search(r'Vector3\(4, 5, 6\) at (0x[0-9a-f]+)', P2).group(1)
def short(a): return '…' + a[-4:]


def d12_new():
    def heap(cells, term=None, extra=''):
        s = region(6, 16, 308, 70, 'HEAP', ORANGE, '#fff7ed')
        x = 14
        for w, v, st in cells:
            s += cell(x, 32, w, 40, v, st, 9.5); x += w + 4
        if term: s += termbox(6, 94, 308, term)
        return s + extra
    f = [frame(1, 'int* b = new int;  new int[50];', heap([(40, '4 B', 'new'), (150, 'int[50]  200 B', 'new')], ['new int: 4 bytes', 'new int[50]: 200 bytes']),
               'operator new بتاعتنا استلمت الحجم: 4 ثم 200.', 136),
         frame(2, 'Entity* e = new Entity();', heap([(40, '4', 'n'), (90, '200', 'n'), (110, 'name=Unknown', 'new')], ['Entity() ran', 'new Entity(): 32 bytes, name = Unknown']),
               'حجز 32 بايت، وبعدين الـ Constructor حط Unknown.', 136),
         frame(3, 'Entity* entities = new Entity[3];', heap([(30, '8', 'hot'), (84, 'Entity 0', 'new'), (84, 'Entity 1', 'new'), (84, 'Entity 2', 'new')], ['Entity() ran  x 3', 'new Entity[3]: 104 bytes (sizeof(Entity) = 32)']),
               'الـ Constructor 3 مرات، والحجم 104 = 8 + 3 × 32. الـ 8 (أصفر) فيهم العدد.', 136),
         frame(4, 'Entity* m = (Entity*)malloc(sizeof(Entity));', heap([(110, 'name = ???', 'warn')], ['malloc(sizeof(Entity)): no "Entity() ran"']),
               '32 بايت بس من غير Constructor: name ماتعملش.', 136)]
    return story('new بتحجز وبتنادي الـ Constructor', 'البرنامج 1 · new_operator.cpp', f)


def d12_place():
    def mem(cells, term, extra=''):
        s = region(6, 16, 308, 70, 'HEAP  ' + short(B), ORANGE, '#fff7ed')
        x = 14
        for w, v, st in cells:
            s += cell(x, 32, w, 40, v, st, 9.5); x += w + 4
        return s + (termbox(6, 94, 308, term) if term else '') + extra
    f = [frame(1, 'int* b = new int[50];', mem([(290, 'int[50]  200 bytes', 'new')], ['new int[50] at ' + B]), 'حجز 200 بايت عادي.', 136),
         frame(2, 'Vector3* v = new (b) Vector3(1, 2, 3);', mem([(110, 'x=1 y=2 z=3', 'chg'), (176, 'rest of the 200', 'n')], ['Vector3(1, 2, 3) at ' + B, 'same address as b: yes']),
               'مفيش حجز: الـ Constructor اشتغل جوه الـ 200 بايت عند b نفسه.', 136),
         frame(3, 'v->~Vector3();', mem([(110, 'x=1 y=2 z=3', 'free'), (176, 'rest of the 200', 'n')], ['~Vector3() at ' + B]), 'الـ Destructor بس. الـ 200 بايت لسه محجوزين.', 136),
         frame(4, 'delete[] b;', mem([(290, 'returned', 'free')], []) + cross(14, 32, 290, 40), 'دلوقتي الـ 200 بايت رجعوا.', 136)]
    return story('Placement new', 'البرنامج 2 · placement_new.cpp', f)


def d12_mip():
    cols = ['#dc2626', '#ea580c', '#eab308', '#16a34a', '#0d9488', '#2563eb', '#7c3aed', '#db2777', '#ffffff']
    def lv(n, hl):
        s = region(6, 16, 308, 80, 'texture levels uploaded', TEAL, '#ecfdf5')
        x = 16
        for i in range(n):
            w = max(6, 60 >> i)
            s += f'<rect x="{x}" y="{86 - w}" width="{w}" height="{w}" fill="{cols[i]}" stroke="#334155"/>' + lbl(x + w / 2, 92 + 0, '', GRAY)
            x += w + 8
        return s + lbl(160, 110, hl, INK, 10, 'middle', True)
    f = [frame(1, 'glTexImage2D(..., level 0, 256 x 256 ...)', lv(1, 'level 0: 196,608 bytes'), 'المستوى 0 = الأصل (أحمر).', 120),
         frame(2, 'level 1 .. 4', lv(5, 'levels 0..4'), 'كل مستوى نص اللي قبله.', 120),
         frame(3, 'level 5 .. 8', lv(9, 'all levels: 262,143 bytes = 1.333 x level 0'), 'لحد 1 × 1 (أبيض). الكارت بقى يقدر يستخدم الـ Texture.', 120),
         frame(4, 'draw: near = red, far = purple', region(6, 16, 308, 80, 'floor') + '<polygon points="20,90 300,90 200,24 120,24" fill="#ea580c"/>' + '<polygon points="20,90 300,90 270,70 50,70" fill="#dc2626"/>' + '<polygon points="120,24 200,24 190,30 130,30" fill="#7c3aed"/>'
               + lbl(160, 110, 'far away = smaller level', INK, 10, 'middle', True), 'الكارت بيختار مستوى أصغر كل ما الأرضية تبعد.', 120)]
    return story('المستويات بالألوان', 'البرنامج 2 · mip_levels.cpp', f)
