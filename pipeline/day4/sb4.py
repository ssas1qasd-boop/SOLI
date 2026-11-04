# Day 4 storyboards.
import sys
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK

def _lock(x, y):
    return (f'<rect x="{x}" y="{y + 5}" width="10" height="8" rx="1.5" fill="{RED}"/>'
            f'<path d="M{x + 2} {y + 5} V{y + 2} a3 3 0 0 1 6 0 V{y + 5}" fill="none" stroke="{RED}" stroke-width="1.5"/>')

def d4_static():
    def files(ok_static=True, link=None):
        s = region(8, 16, 140, 92, 'main.cpp', BLUE, '#f8fbff') + region(172, 16, 140, 92, 'static.cpp', ORANGE, '#fffaf5')
        s += cell(14, 32, 128, 20, 's_Variable = 10', 'new', 8.5) + cell(14, 56, 128, 20, 'Function()', 'new', 8.5) + cell(14, 80, 128, 20, 'needs PrintStatic', 'free', 8.5)
        st = 'warn' if ok_static else 'new'
        s += cell(178, 32, 128, 20, ('static ' if ok_static else '') + 's_Variable = 5', st, 8.5) + cell(178, 56, 128, 20, ('static ' if ok_static else '') + 'Function()', st, 8.5)
        s += cell(178, 80, 128, 20, 'PrintStatic()', 'new', 8.5)
        if ok_static:
            s += _lock(292, 36) + _lock(292, 60)
        if link == 'ok':
            s += arr(142, 90, 176, 90, GREEN) + termbox(8, 116, 304, ['main.cpp sees:   10', 'static.cpp sees: 5'])
        elif link == 'bad':
            s += arr(142, 42, 176, 42, RED) + termbox(8, 116, 304, ["ld: multiple definition of `s_Variable'"])
        return s
    f = [frame(1, 'g++ -c main.cpp   g++ -c static.cpp', files(), 'كل ملف بيترجم لوحده. الأحمر بالقفل <code>static</code>: مخفي عن أي ملف تاني.', 120),
         frame(2, 'link  (with static)', files(link='ok'), 'الـ Linker شايف <code>s_Variable</code> واحدة بس (بتاعة main.cpp)، فمفيش خناقة. وكل ملف بيستخدم نسخته.', 158),
         frame(3, 'link  (static removed)', files(False, 'bad'), 'من غير <code>static</code>: الـ Linker شايف اسمين زي بعض، فيرفض.', 150)]
    return story('ترجمة ملفين وربطهم', 'البرنامج 1 · ده بيحصل لما تعمل Build', f)

def d4_ebo():
    P = {0: (40, 118), 1: (130, 118), 2: (130, 30), 3: (40, 30)}
    def scene(k):
        s = ''
        if k >= 1: s += f'<polygon points="40,118 130,118 130,30" fill="#bfdbfe" stroke="{BLUE}"/>'
        if k >= 2: s += f'<polygon points="130,30 40,30 40,118" fill="#ccfbf1" stroke="{TEAL}"/>'
        for i, (x, y) in P.items():
            s += f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="{INK}"/>' + lbl(x, y + 3.5, str(i), INK, 9, b=True)
        for j, v in enumerate([0, 1, 2, 2, 3, 0]):
            hot = (k == 1 and j < 3) or (k == 2 and j >= 3)
            s += cell(170 + (j % 3) * 45, 30 + (j // 3) * 40, 40, 30, v, 'hot' if hot else ('n' if k > j // 3 else 'free'), 11)
        s += lbl(237, 22, 'indices', GRAY, 9, b=True)
        return s
    f = [frame(1, 'glBufferData(GL_ELEMENT_ARRAY_BUFFER, …)', scene(0), 'كارت الشاشة عنده 4 أركان، وعنده الترتيب. لسه مارسمش حاجة.', 132),
         frame(2, 'glDrawElements  ->  indices 0, 1, 2', scene(1), 'أول 3 أرقام: الأركان 0 و 1 و 2 = المثلث الأزرق.', 132),
         frame(3, 'glDrawElements  ->  indices 2, 3, 0', scene(2), 'التلاتة اللي بعدهم: 2 و 3 و 0 = المثلث التاني. الركنين 0 و 2 اتستخدموا مرتين من غير تكرار.', 132)]
    return story('glDrawElements بيقرا الترتيب', 'البرنامج 2', f)

def d4_vao():
    def scene(house=0, sun=0, bound=None, draw=None):
        s = ''
        for i, (name, n, c) in enumerate([('houseVao', house, BLUE), ('sunVao', sun, ORANGE)]):
            y = 20 + i * 55
            st = 'hot' if bound == name else ('n' if n else 'free')
            s += cell(10, y, 120, 44, '', st) + lbl(70, y + 16, name, c, 10, b=True)
            s += lbl(70, y + 34, ['empty', 'buffer bound', 'slot 0 recorded'][n], GRAY if n < 2 else GREEN, 9)
        if draw:
            s += f'<rect x="160" y="20" width="150" height="100" rx="4" fill="#0b0f17"/>'
            if 'house' in draw:
                s += '<polyline points="195,105 275,105 275,75 195,75 195,105" fill="none" stroke="#fff"/><polyline points="188,75 235,40 282,75" fill="none" stroke="#fff"/>'
            if 'sun' in draw:
                s += '<line x1="285" y1="35" x2="303" y2="35" stroke="#facc15"/><line x1="294" y1="26" x2="294" y2="44" stroke="#facc15"/>'
        return s
    f = [frame(1, 'glBindVertexArray(houseVao);  glBindBuffer(…, houseBuffer);', scene(1, 0, 'houseVao'), 'شغّلنا دفتر البيت، واخترنا buffer البيت.', 132),
         frame(2, 'glVertexAttribPointer(0, 2, …);', scene(2, 0, 'houseVao'), 'السطر ده سجّل في الدفتر: «الخانة 0 = من houseBuffer، رقمين لكل نقطة».', 132),
         frame(3, '… same for sunVao …  glBindVertexArray(0);', scene(2, 2), 'نفس الكلام للشمس في دفتر تاني. بعدين فكّينا الاتنين.', 132),
         frame(4, 'loop: bind houseVao -> draw;  bind sunVao -> draw', scene(2, 2, 'sunVao', 'house sun'), 'في اللوب: سطر bind واحد بيرجّع كل إعدادات الشكل، وبعده الرسم.', 132)]
    return story('الـ VAO = دفتر بيفتكر الإعدادات', 'البرنامج 3', f)

def d4_poly():
    def scene(pts, lines, stage):
        s = f'<rect x="10" y="18" width="140" height="105" rx="4" fill="#0b0f17"/>'
        P = [(22, 110), (50, 85), (78, 102), (106, 70), (40, 45), (80, 28), (120, 45)][:pts]
        groups = [(0, min(pts, 4)), (4, max(0, min(pts, 7) - 4))]
        for g, (a, n) in enumerate(groups[:lines]):
            if n >= 2:
                s += '<polyline points="' + ' '.join(f'{x},{y}' for x, y in P[a:a + n]) + '" fill="none" stroke="#fff"/>'
        for x, y in P:
            s += f'<rect x="{x - 3}" y="{y - 3}" width="6" height="6" fill="#f97316"/>'
        s += lbl(235, 28, 'polylines', BLUE, 9.5, b=True)
        for k, (first, count) in enumerate(stage):
            s += cell(165, 36 + k * 28, 140, 24, f'[{k}] first={first} count={count}', 'new' if k == len(stage) - 1 else 'n', 9)
        return s
    f = [frame(1, 'left click x4', scene(4, 1, [(0, 4)]), 'أربع دوسات شمال: الخط 0 بقى فيه 4 نقط متصلة.', 135),
         frame(2, 'right click', scene(4, 1, [(0, 4), (4, 0)]), 'يمين: الخط 0 خلص، واتعمل خط 1 فاضي بيبدأ من النقطة رقم 4.', 135),
         frame(3, 'left click x3', scene(7, 2, [(0, 4), (4, 3)]), 'ثلاث دوسات: الخط 1 فيه 3 نقط. ونرسم كل خط لوحده بـ <code>GL_LINE_STRIP</code> من <code>first</code> بعدد <code>count</code>.', 135)]
    return story('Polylines بالماوس', 'البرنامج 4 · نفس الدوسات اللي في التشغيل الحقيقي', f)
