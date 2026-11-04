# Day 5 storyboards: each frame = the line that just ran + the state after it.
import sys
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK


def d5_swap():
    def scene(x, y, temp=None, hot=None, ptrs=True):
        s = region(8, 14, 132, 120, 'main', BLUE, '#f8fbff')
        s += cell(30, 36, 90, 32, f'x = {x}', 'chg' if hot == 'x' else 'n', 12) + lbl(75, 82, '0x...90', GRAY, 8.5)
        s += cell(30, 90, 90, 32, f'y = {y}', 'chg' if hot == 'y' else 'n', 12) + lbl(75, 136, '0x...94', GRAY, 8.5)
        if ptrs:
            s += region(176, 14, 136, 120, 'swap', PURPLE, '#faf5ff')
            s += cell(196, 36, 64, 32, 'a', 'ptr', 12) + cell(196, 90, 64, 32, 'b', 'ptr', 12)
            s += arr(194, 52, 122, 52, PURPLE, True) + arr(194, 106, 122, 106, PURPLE, True)
            s += cell(266, 62, 42, 32, '-' if temp is None else temp, 'hot' if hot == 't' else ('n' if temp is not None else 'free'), 11) + lbl(287, 56, 'temp', GRAY, 8.5)
        return s
    f = [frame(1, 'swap(&x, &y);', scene(10, 20), 'الدالة استلمت العنوانين: <code>a</code> بيشاور على <code>x</code>، و <code>b</code> على <code>y</code>. لسه ماتغيرش حاجة.', 142),
         frame(2, 'temp = *a;', scene(10, 20, '10', 't'), 'خدنا اللي في عنوان <code>a</code> (يعني 10) وشلناه في <code>temp</code>.', 142),
         frame(3, '*a = *b;', scene(20, 20, '10', 'x'), 'كتبنا 20 جوه <code>x</code> نفسه من خلال العنوان. دلوقتي الاتنين 20، والـ 10 موجودة في <code>temp</code> بس.', 142),
         frame(4, '*b = temp;', scene(20, 10, '10', 'y'), 'كتبنا 10 جوه <code>y</code>. خلاص اتبدلوا، والتغيير حصل في <code>main</code> نفسها.', 142)]
    return story('التبديل بالعناوين خطوة خطوة', 'البرنامج 1 · ده اللي بيحصل في الذاكرة', f)


def d5_names():
    def scene(items, hot=None, gone=None):
        s = lbl(10, 22, 'list', BLUE, 10, 'start', True)
        for j, it in enumerate(items):
            st = 'warn' if it == 'Q' else ('new' if j == len(items) - 1 and hot == 'push' else 'n')
            s += cell(10 + j * 74, 32, 68, 30, it, st, 11)
        if gone:
            s += cell(10 + len(items) * 74, 32, 68, 30, gone, 'free', 11) + cross(10 + len(items) * 74, 32, 68, 30)
        s += lbl(10, 88, f'size() = {len(items)}', GRAY, 10, 'start', True)
        return s
    f = [frame(1, 'list.push_back(name);   // "Braden"', scene(['Braden'], 'push'), 'أول اسم اتضاف في الآخر. الحجم بقى 1.', 100),
         frame(2, 'list.push_back(name);   // "Katie"', scene(['Braden', 'Jeff', 'Katie'], 'push'), 'كل اسم بيتضاف ورا اللي قبله.', 100),
         frame(3, 'list.push_back(name);   // "Q"', scene(['Braden', 'Jeff', 'Katie', 'Q'], 'push'), 'المستخدم كتب Q: اتضافت <b>قبل</b> ما اللوب يتأكد من الشرط. بعدها الشرط وقّف اللوب.', 100),
         frame(4, 'list.pop_back();', scene(['Braden', 'Jeff', 'Katie'], gone='Q'), '<code>pop_back</code> شالت آخر عنصر (الـ Q). الحجم رجع 3.', 100)]
    return story('push_back و pop_back', 'البرنامج 1 · الـ vector في الرام', f)


def d5_delete():
    def scene(lines, pts, note=None):
        s = lbl(8, 20, 'polylines', PURPLE, 9.5, 'start', True)
        for j, (first, cnt, st) in enumerate(lines):
            s += cell(8 + j * 76, 28, 70, 26, f'{{ {first}, {cnt} }}', st, 10.5)
        s += lbl(8, 78, 'points (floats)', BLUE, 9.5, 'start', True)
        for k, st in enumerate(pts):
            s += cell(8 + k * 21.5, 86, 19, 22, '', st, 8)
        s += lbl(8, 126, f'{len(pts)} floats = {len(pts) // 2} points', GRAY, 9, 'start')
        if note: s += lbl(312, 126, note, RED, 9, 'end', True)
        return s
    full = ['new'] * 8 + ['hot'] * 6
    f = [frame(1, 'before Backspace', scene([(0, 4, 'new'), (4, 3, 'hot'), (7, 0, 'free')], full), 'خطين متخلصين، وخط تالت فاضي (بدأ لما دوسنا يمين).', 135),
         frame(2, 'polylines.pop_back();   // the empty one', scene([(0, 4, 'new'), (4, 3, 'hot')], full), 'الخط الحالي فاضي (count = 0)، فمسحناه الأول عشان نوصل للخط اللي قبله.', 135),
         frame(3, 'Polyline last = ...; polylines.pop_back();', scene([(0, 4, 'new')], full, 'last = { 4, 3 }'), 'خدنا نسخة من آخر خط (عشان نعرف عدد نقطه = 3)، ومسحناه من القايمة. نقطه لسه في <code>points</code>.', 135),
         frame(4, 'points.pop_back();  x 6', scene([(0, 4, 'new')], ['new'] * 8), 'اللوب مسح 3 × 2 = 6 أرقام من آخر <code>points</code>.', 135),
         frame(5, 'polylines.push_back({ 4, 0 }); UploadPoints();', scene([(0, 4, 'new'), (4, 0, 'free')], ['new'] * 8), 'بدأنا خط جديد فاضي عشان الدوسة الجاية تبقى خط لوحدها، وبعتنا الـ 8 أرقام للكارت.', 135)]
    return story('Backspace بيمسح آخر خط', 'البرنامج 2 · في الرام وفي الكارت', f)


def _img(name, x=40, y=5, w=240, h=130):
    import base64, io
    from PIL import Image
    im = Image.open(f'/home/claude/day5/img/{name}.png').convert('RGB').resize((320, 240))
    b = io.BytesIO(); im.save(b, 'PNG')
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>'


def d5_shader():
    def tri(scale, dots=(), label=None):
        pts = [(-0.5, -0.5), (0.0, 0.5), (0.5, -0.5)]
        P = [(160 + x * scale * 120, 70 - y * scale * 65) for x, y in pts]
        poly = ' '.join(f'{x},{y}' for x, y in P)
        s = '<rect x="40" y="5" width="240" height="130" fill="#0b0f17" rx="4"/>'
        s += f'<polygon points="{poly}" fill="none" stroke="#94a3b8" stroke-dasharray="3 3"/>'
        for k in dots:
            x, y = P[k]; s += f'<circle cx="{x}" cy="{y}" r="4" fill="{TEAL}"/>'
        if label: s += lbl(160, 148, label, TEAL, 8.5)
        return s
    f = [frame(1, 'gl_Position = position;   // program 1', _img('r1_red_triangle'), 'البرنامج 1 (صورة الشباك الحقيقي): كل ركن في مكانه زي ما هو، وكل بكسل أحمر.', 150),
         frame(2, 'gl_Position = vec4(position.x * 1.5, ...)', tri(1.5, (0, 1, 2), 'the vertex shader ran 3 times'), 'البرنامج 2: الـ Vertex Shader اشتغل 3 مرات (مرة لكل ركن) وضرب كل ركن في 1.5. المثلث كبر من غير ما نغيّر <code>positions</code>.', 150),
         frame(3, 'v_Position = position;', tri(1.5, (0, 1, 2), 'each corner sends its own v_Position'), 'كل ركن بعت مكانه الأصلي في <code>v_Position</code>. الـ Rasterizer بيخلطهم لكل بكسل حسب قربه من كل ركن.', 150),
         frame(4, 'color = vec4(v_Position.x + 0.5, v_Position.y + 0.5, 0.2, 1.0);', _img('r2_shader_edit'), 'الـ Fragment Shader اشتغل مرة لكل بكسل (صورة الشباك الحقيقي): يمين = أحمر أكتر، وفوق = أخضر أكتر.', 150)]
    return story('تعديل الـ Shader: إيه اللي بيحصل في الكارت', 'البرنامج 1 ثم البرنامج 2', f)
