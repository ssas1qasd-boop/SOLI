# Week 3 Day 2 storyboards: each frame = the line that just ran + the state after it (values from the real runs).
import sys
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK


def d9_struct():
    def two(sv, cv, st):
        s = region(10, 16, 300, 96, 'STACK')
        for r, (n, vals) in enumerate((('s', sv), ('c', cv))):
            y = 32 + r * 40
            s += lbl(24, y + 17, n, TEAL if r == 0 else PURPLE, 11, 'start', True)
            for k, v in enumerate(vals):
                s += cell(56 + k * 82, y, 76, 26, v, st[r][k], 11) + (lbl(94 + k * 82, y + 36, ('x', 'y', 'speed')[k], GRAY, 8.5) if r == 1 else '')
        return s
    f = [frame(1, 's.x = 0; s.y = 0; s.speed = 2;   c.x = 0; c.y = 0; c.speed = 2;', two(('0', '0', '2'), ('0', '0', '2'), (('new',) * 3, ('new',) * 3)),
               'نفس الـ 3 أوامر شغالة مع الاتنين: الـ struct public لوحده، والـ class عشان كتبنا <code>public:</code>.', 130),
         frame(2, 's.Move(1, -1);   c.Move(1, -1);', two(('2', '-2', '2'), ('2', '-2', '2'), (('chg', 'chg', 'n'), ('chg', 'chg', 'n'))),
               'نفس الحركة ونفس الحجم (12 بايت لكل واحد). الفرق كان في الكتابة بس، مش في الرام.', 130),
         frame(3, 'position.Add(velocity);  position.Add(velocity);', region(10, 16, 300, 70, 'STACK') + lbl(24, 49, 'position', BLUE, 10, 'start', True)
               + cell(100, 32, 90, 26, '1 -> 1.5 -> 2', 'chg', 10) + cell(200, 32, 90, 26, '2 -> 1 -> 0', 'chg', 10) + lbl(145, 70, 'x', GRAY, 8.5) + lbl(245, 70, 'y', GRAY, 8.5)
               + termbox(10, 92, 300, ['position after 2 Add: (2, 0)', 'sizeof(Vec2) = 8 bytes']),
               'Vec2 = رقمين وبس (8 بايت). ده اللي The Cherno بيسميه struct.', 145)]
    return story('struct و class في الرام', 'البرنامج 1 · struct_class.cpp', f)


def d9_texture():
    def scene(ram, gpu, lv, note=None):
        s = region(8, 16, 96, 96, 'RAM', BLUE, '#eff6ff') + region(112, 16, 200, 96, 'GPU texture (id 1)', TEAL, '#ecfdf5')
        if ram: s += cell(14, 44, 84, 40, ram, 'new' if ram != 'freed' else 'free', 9)
        if gpu: s += cell(118, 34, 70, 40, gpu, 'chg', 9)
        for k, t in enumerate(lv):
            s += cell(196 + k * 22, 44, 20, 20, t, 'new', 7.5)
        if note: s += termbox(8, 118, 304, [note])
        return s
    f = [frame(1, 'stbi_load("res/pixel_cat.png", &widthImg, &heightImg, &numColCh, 0);', scene('16x16x4 = 1024 B', '', [], 'pixel_cat.png: 16 x 16, channels = 4'),
               'آخر رقم 0 = «زي الملف». الملف طلع 4 قنوات، فـ <code>glTexImage2D</code> لازم يقول <code>GL_RGBA</code>.', 145),
         frame(2, 'glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, …, bytes);', scene('16x16x4 = 1024 B', 'level 0: 16x16', []),
               'البكسلات اتنسخت للكارت في المستوى 0.', 120),
         frame(3, 'glGenerateMipmap(GL_TEXTURE_2D);  stbi_image_free(bytes);', scene('freed', 'level 0: 16x16', ['8', '4', '2', '1']),
               'الكارت عمل 4 نسخ أصغر لوحده، ورجّعنا الرام.', 120),
         frame(4, 'glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);', scene('freed', 'level 0: 16x16', ['8', '4', '2', '1'], 'frame 0 drawn, glGetError() = 0'),
               'المربع كبير على الشاشة، فالكارت قرا من المستوى 0 بـ NEAREST: مربعات حادة.', 145)]
    return story('القطة من الملف للكارت', 'البرنامج 1 · pixel_cat.cpp', f)


def d9_mesh():
    def scene(e, res, st='new'):
        s = cell(10, 24, 92, 34, 'V = 8', 'n', 11) + cell(114, 24, 92, 34, f'E = {e}', st, 11) + cell(218, 24, 92, 34, 'F = 12', 'n', 11)
        return s + termbox(10, 72, 300, res)
    f = [frame(1, 'std::vector<Triangle> triangles = { {0, 2, 1}, … };', scene('?', ['face list: 432 bytes', 'indexed:   240 bytes'], 'n'),
               'الأركان مرة واحدة، والمثلثات أرقام. 240 بايت بدل 432.', 130),
         frame(2, 'edges.insert({ std::min(p, q), std::max(p, q) });   (x 36)', scene('18', ['V - E + F = 8 - 18 + 12 = 2']),
               'اتنادت عدد 36 مرة (12 مثلث × 3 أضلاع)، بس الـ set خد 18 بس: كل ضلع داخلي جه مرتين.', 130),
         frame(3, 'Barycentric(1, 1);  …  Barycentric(3, 3);', cell(10, 24, 300, 34, 'triangle (0,0) (4,0) (0,4)', 'n', 11)
               + termbox(10, 66, 300, ['(1, 1): 0.5  0.25  0.25   inside', '(2, 2): 0    0.5   0.5    on an edge', '(4, 0): 0    1     0      on a vertex', '(3, 3): -0.5 0.75  0.75   outside']),
               'المجموع دايماً 1. أي واحدة سالبة = برّه.', 160)]
    return story('مكعب من مثلثات', 'البرنامج 1 · mesh.cpp', f)
