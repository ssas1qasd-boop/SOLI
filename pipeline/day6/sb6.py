# Day 6 storyboards: each frame = the line that just ran + the state after it.
import sys
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK


def _img(name, x=40, y=5, w=240, h=130):
    import base64, io
    from PIL import Image
    im = Image.open(name if name.startswith('/') else f'/home/claude/day6/img/{name}.png').convert('RGB').resize((320, 240))
    b = io.BytesIO(); im.save(b, 'PNG')
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>'


def d6_scan():
    src = 'var x = 1 + 2 * 3;'
    def scene(i, toks, hot=None):
        s = lbl(8, 18, 'source', GRAY, 9.5, 'start', True)
        for k, ch in enumerate(src):
            st = 'hot' if k == i else ('new' if hot and hot[0] <= k < hot[1] else 'n')
            s += cell(8 + k * 17, 24, 16, 24, ch if ch != ' ' else '·', st, 10)
        s += lbl(8 + i * 17 + 8, 62, 'i', RED, 10, 'middle', True)
        s += lbl(8, 86, 'tokens', PURPLE, 9.5, 'start', True)
        x = 8
        for t in toks:
            w = max(24, len(t) * 9 + 10); s += cell(x, 92, w, 24, t, 'new' if t == toks[-1] else 'n', 10); x += w + 4
        return s
    f = [frame(1, "isalpha('v') -> read the whole word", scene(3, ['var'], (0, 3)), 'حرف: الـ Scanner مشي لحد آخر الكلمة وطلّع <code>var</code>. الـ i واقف بعدها على المسافة.', 125),
         frame(2, "isspace(' ') -> i++; continue;", scene(4, ['var']), 'مسافة: اتعدّت ومفيش Token.', 125),
         frame(3, "isdigit('1') -> Number", scene(9, ['var', 'x', '=', '1'], (8, 9)), 'بعد <code>x</code> و <code>=</code>: رقم. كل رقم = Token لوحده.', 125),
         frame(4, "c == ';' -> Semicolon", scene(17, ['var', 'x', '=', '1', '+', '2', '*', '3', ';'], (17, 18)), 'آخر الجملة الأولى: 9 Tokens. والجملة التانية بنفس الطريقة، وفي الآخر <code>end</code>.', 125)]
    return story('الـ Scanner بيقرا حرف حرف', 'البرنامج 1 · المرحلة 1', f)


def d6_parse():
    def node(x, y, t, st='n'): return cell(x - 16, y - 12, 32, 24, t, st, 11)
    def tree(stage):
        s = ''
        if stage >= 1: s += node(60, 40, '1', 'new' if stage == 1 else 'n')
        if stage >= 2:
            s += node(200, 40, '+', 'new' if stage == 2 else 'n') + arr(190, 52, 72, 52, GRAY)
        if stage >= 3:
            s += node(200, 100, '*', 'new' if stage == 3 else 'n') + node(150, 140, '2') + node(250, 140, '3')
            s += arr(196, 88, 196, 54, TEAL) + arr(160, 128, 192, 112, GRAY) + arr(240, 128, 208, 112, GRAY)
        return s
    f = [frame(1, 'Addition() -> Multiplication() -> Primary()', tree(1), 'الجمع نده الضرب، والضرب نده Primary: خد <code>1</code>. مفيش <code>*</code> بعدها، فالضرب رجّع 1.', 160),
         frame(2, 'Match(Plus)', tree(2), 'الجمع لقى <code>+</code>: هيعمل عقدة <code>+</code> شمالها 1، ولسه محتاج يمينها.', 160),
         frame(3, "left = new Node{ '+', 0, \"\", left, Multiplication() };", tree(3), 'يمين الـ <code>+</code> = Multiplication كاملة: خدت 2، ولقت <code>*</code>، وخدت 3. فـ 2 × 3 بقت فرع واحد تحت الـ <code>+</code>.', 160)]
    return story('الـ Parser بيبني الشجرة', 'البرنامج 1 · المرحلة 2', f)


def d6_vm():
    def scene(op, st, reg=None, out=None):
        s = lbl(10, 18, op, ORANGE, 10.5, 'start', True) + lbl(10, 40, 'stack', BLUE, 9.5, 'start', True)
        for k, v in enumerate(st): s += cell(10 + k * 46, 46, 42, 28, str(v), 'new' if k == len(st) - 1 else 'n', 12)
        if not st: s += cell(10, 46, 42, 28, '', 'free', 12)
        s += lbl(200, 40, 'registers', PURPLE, 9.5, 'start', True) + cell(200, 46, 70, 28, f'x = {reg if reg is not None else 0}', 'chg' if reg else 'n', 11)
        if out: s += termbox(10, 90, 300, [out])
        return s
    f = [frame(1, 'LOAD_INT 1 · LOAD_INT 2 · LOAD_INT 3', scene('3 pushes', [1, 2, 3]), 'تلات أرقام فوق بعض.', 120),
         frame(2, 'MULTIPLY', scene('MULTIPLY', [1, 6]), 'شال 3 و 2 وحط 6.', 120),
         frame(3, 'ADD · STORE_VAR 0', scene('ADD, then STORE_VAR 0', [], 7), 'الجمع طلّع 7، و STORE حطها في خانة <code>x</code> (رقم 0) وفضّى الـ Stack.', 120),
         frame(4, 'LOAD_VAR 0 · LOAD_INT 2 · MULTIPLY · PRINT', scene('x * 2', [], 7, '  result: 14'), 'قرا <code>x</code> من خانتها، ضربها في 2، وطبع 14.', 135)]
    return story('الـ VM بتنفذ الـ Bytecode', 'البرنامج 1 · المرحلة 4', f)


def d6_anim():
    f = [frame(i + 1, c, _img(n), cap, 140) for i, (c, n, cap) in enumerate([
        ('glUniform4f(location, r, 0.3f, 0.8f, 1.0f);   // r small', 'r1_animated_color_3', 'r قليل: اللون أزرق (0.3 أخضر و 0.8 أزرق ثابتين).'),
        ('r += increment;   // r bigger', 'r1_animated_color_1', 'r زاد: بقى بنفسجي.'),
        ('r += increment;   // r near 1', 'r1_animated_color_5', 'r قرب من 1: بنفسجي فاتح. بعدها الـ if بيعكس ويبدأ ينقص.')])]
    return story('اللون بيتحرك', 'البرنامج 1 · صور حقيقية من الشباك وقت التشغيل', f)


def d6_time():
    f = [frame(i + 1, c, _img(n), cap, 140) for i, (c, n, cap) in enumerate([
        ('glUniform1f(timeLocation, time);   // t ≈ 0.4 s', 'r2_time_colors_1', 'الوقت قليل: كل بكسل لونه حسب مكانه (شمال وتحت غير يمين وفوق).'),
        ('glUniform1f(timeLocation, time);   // t ≈ 1.6 s', 'r2_time_colors_4', 'الوقت زاد: كل الألوان اتزحزحت مع بعض.'),
        ('glUniform1f(timeLocation, time);   // t ≈ 2.4 s', 'r2_time_colors_6', 'وكمان. الـ CPU بعت رقم واحد بس، والكارت حسب لون مختلف لكل بكسل.')])]
    return story('الوقت بيحرّك الألوان', 'البرنامج 2 · صور حقيقية من الشباك', f)


def d6_same():
    def pair(n):
        return _img(f'c1_{n}', 8, 5, 148, 110) + _img(f'/home/claude/day6/exp/c0_{n}.png', 164, 5, 148, 110) + lbl(82, 128, 'refactored', GREEN, 9, 'middle', True) + lbl(238, 128, 'yesterday', GRAY, 9, 'middle', True)
    f = [frame(1, 'after 9 clicks', pair(9), 'بعد 9 دوسات: نفس الصورة بالظبط.', 140),
         frame(2, 'Backspace', pair(10), 'Backspace: نفس الصورة.', 140),
         frame(3, '2 more Backspace', pair(15), 'Backspace مرتين كمان: نفس الصورة. والـ 17 لقطة اتقارنوا بالكمبيوتر بكسل بكسل.', 140)]
    return story('من برا: نفس البرنامج', 'البرنامج 1 · امبارح والنهارده بنفس الدوسات', f)
