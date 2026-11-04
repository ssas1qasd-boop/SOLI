# Day 3 step-by-step storyboards, same style as Day 1/2 (sb.py).
import sys, html
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK

def nametag(x, y, t, c=BLUE):
    w = len(t) * 7 + 14
    return (f'<rect x="{x}" y="{y}" width="{w}" height="18" rx="9" fill="#fff" stroke="{c}" stroke-width="1.4"/>'
            + lbl(x + w / 2, y + 13, t, c, 10, b=True))

def d3_ref():
    STK = region(20, 18, 280, 100, 'STACK')
    A = lambda v, st: cell(110, 40, 90, 40, v, st)
    f = [frame(1, 'int a = 5;', STK + A(5, 'new') + nametag(118, 88, 'a'), 'صندوق واحد اسمه <code>a</code> وجواه 5.'),
         frame(2, 'int& ref = a;', STK + A(5, 'n') + nametag(118, 88, 'a') + nametag(152, 88, 'ref', PURPLE), 'مفيش صندوق جديد! نفس الصندوق بقى ليه اسمين.'),
         frame(3, 'ref = 2;', STK + A(2, 'chg') + nametag(118, 88, 'a') + nametag(152, 88, 'ref', PURPLE), 'كتبنا في <code>ref</code>، فاتغير الصندوق نفسه. يعني <code>a</code> بقى 2.'),
         frame(4, 'std::cout << &a … &ref', STK + A(2, 'n') + nametag(118, 88, 'a') + nametag(152, 88, 'ref', PURPLE) + termbox(20, 124, 280, ['&a   = 0x7ffd1e13b91c', '&ref = 0x7ffd1e13b91c']), 'نفس العنوان بالظبط، لأنه نفس الصندوق.', 175)]
    return story('اسم تاني لنفس الصندوق', 'البرنامج 1', f)

def d3_rebind():
    STK = region(10, 18, 300, 112, 'STACK')
    def boxes(a, b, sa='n', sb_='n'):
        return cell(40, 40, 80, 38, a, sa) + nametag(48, 84, 'a') + cell(200, 40, 80, 38, b, sb_) + nametag(208, 84, 'b')
    REF = nametag(76, 84, 'ref', PURPLE)
    PTR = lambda tx: cell(120, 100, 70, 24, 'ptr', 'ptr', 10) + arr(155, 100, tx, 80, PURPLE)
    f = [frame(1, 'int& ref = a;', STK + boxes(5, 8) + REF, '<code>ref</code> اسم تاني لـ <code>a</code>.', 145),
         frame(2, 'ref = b;', STK + boxes(8, 8, 'chg') + REF, 'الاسم <code>ref</code> فضل على <code>a</code>. اللي حصل إن قيمة b (8) اتنسخت جوه <code>a</code>.', 145),
         frame(3, 'int* ptr = &a;  *ptr = 2;', STK + boxes(2, 8, 'chg') + REF + PTR(80), 'الـ Pointer صندوق جديد بيشاور على <code>a</code>، وكتبنا هناك 2.', 145),
         frame(4, 'ptr = &b;  *ptr = 1;', STK + boxes(2, 1, 'n', 'chg') + REF + PTR(240), 'الـ Pointer <b>اتنقل</b> لـ <code>b</code> وكتب هناك 1. ده اللي الـ Reference مايقدرش يعمله.', 145)]
    return story('الـ Reference مابيتنقلش، الـ Pointer بيتنقل', 'البرنامج 3', f)

def d3_hamming():
    L, R = 'AATG', 'AAA'
    def row(i, dist, stop=False):
        s = ''
        for k in range(5):
            x = 45 + k * 50
            cl = L[k] if k < 4 else '\\0'
            cr = R[k] if k < 3 else ('\\0' if k == 3 else '')
            def st(ch, other):
                if k == i: return 'warn' if ch != other else 'hot'
                return 'free' if ch in ('\\0', '') else 'n'
            s += cell(x, 34, 42, 28, cl, st(cl, cr), 11)
            if cr != '':
                s += cell(x, 82, 42, 28, cr, st(cr, cl), 11)
        x = 66 + i * 50
        s += cell(x - 22, 6, 44, 18, 'lhs', 'ptr', 9) + arr(x, 24, x, 32, BLUE)
        s += cell(x - 22, 124, 44, 18, 'rhs', 'ptr', 9) + arr(x, 124, x, 112, PINK)
        s += lbl(45, 165, f'distance = {dist}', ORANGE, 11, 'start', True)
        return s
    f = [frame(1, 'for (; *lhs && *rhs; …)   // A == A', row(0, 0), 'الـ Pointerين واقفين على أول حرف: A مع A، زي بعض.', 178),
         frame(2, 'lhs++, rhs++  …  *lhs != *rhs  ->  distance++', row(2, 1), 'الاتنين اتحركوا خطوتين لقدام: T مع A مختلفين، فالعدّاد بقى 1.', 178),
         frame(3, "lhs++, rhs++   ->   *rhs == '\\0'  ->  stop", row(3, 1), '<code>rhs</code> وصل لـ <code>\\0</code>، يعني <code>*rhs</code> = صفر = false، فاللوب وقف.', 178),
         frame(4, 'return (*lhs || *rhs) ? -1 : distance;', row(3, 1) + termbox(200, 150, 105, ['-1']), '<code>*lhs</code> لسه G (مش صفر)، يعني الطولين مختلفين: رجّع ‎-1.', 178)]
    return story('<bdi dir="ltr">compute("AATG", "AAA")</bdi> بالـ Pointers', 'الحل التاني من الفيديو · نفس فكرة <code>p++</code> بتاعة امبارح', f)

def d3_parse():
    def state(line, typ, v, fr, hl=None):
        s = cell(10, 18, 300, 24, line, 'hot', 9.5, bold=False)
        s += lbl(14, 62, 'type =', GRAY, 10, 'start') + cell(60, 48, 100, 22, typ, 'new' if typ == 'VERTEX' else ('gpu' if typ == 'FRAGMENT' else 'free'), 9.5)
        s += cell(10, 84, 145, 50, '', 'new' if hl == 0 else 'n') + lbl(16, 98, 'ss[0]  (vertex)', BLUE, 9, 'start', True) + lbl(16, 116, v, INK, 8.5, 'start')
        s += cell(165, 84, 145, 50, '', 'gpu' if hl == 1 else 'n') + lbl(171, 98, 'ss[1]  (fragment)', TEAL, 9, 'start', True) + lbl(171, 116, fr, INK, 8.5, 'start')
        return s
    f = [frame(1, 'getline -> "#shader vertex"', state('#shader vertex', 'VERTEX', '', ''), 'السطر فيه <code>#shader</code> و vertex: غيّر <code>type</code> بس. السطر نفسه مابيتنسخش.', 142),
         frame(2, 'getline -> "#version 330 core"', state('#version 330 core', 'VERTEX', '#version 330 core', '', 0), 'سطر عادي: اتكتب في <code>ss[0]</code> لأن <code>type</code> = VERTEX = 0.', 142),
         frame(3, 'getline -> … (until #shader fragment)', state('#shader fragment', 'FRAGMENT', '#version … main() {…}', ''), 'كل سطور الـ Vertex دخلت <code>ss[0]</code>. ودلوقتي قابلنا fragment، فـ <code>type</code> اتغير.', 142),
         frame(4, 'getline -> fragment lines … end of file', state('(end of file)', 'FRAGMENT', '#version … main() {…}', '#version … color = …', 1), 'باقي السطور دخلت <code>ss[1]</code>. الملف خلص، فالدالة بترجّع النصين.', 142)]
    return story('ParseShader بتقرا الملف إزاي', 'البرنامج 1 · سطر سطر', f)

def d3_click():
    def scene(pts, vec, line_pairs=0):
        s = f'<rect x="10" y="18" width="150" height="112" rx="4" fill="#0b0f17"/>'
        P = [(28, 112), (75, 44), (100, 120)][:pts]
        for k in range(line_pairs):
            (x1, y1), (x2, y2) = P[2 * k], P[2 * k + 1]
            s += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="1.5"/>'
        for (x, y) in P:
            s += f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" fill="#f97316"/>'
        s += lbl(240, 30, 'std::vector<float> points', BLUE, 9, b=True)
        for k, v in enumerate(vec):
            s += cell(172 + (k % 4) * 35, 40 + (k // 4) * 30, 32, 24, v, 'new' if k >= len(vec) - 2 else 'n', 8)
        s += lbl(240, 125, f'count = {len(vec) // 2}  ->  {line_pairs} line(s)', PURPLE, 9.5, b=True)
        return s
    f = [frame(1, 'click (100, 380)', scene(1, ['-0.69', '-0.58']), 'اتحوّل لـ (‎-0.69, ‎-0.58) واتضاف للقايمة. نقطة واحدة: مفيش خط لسه.', 138),
         frame(2, 'click (300, 120)', scene(2, ['-0.69', '-0.58', '-0.06', '0.5'], 1), 'نقطتين = خط. <code>glBufferData</code> بعتت الـ 4 أرقام، و <code>GL_LINES</code> وصّلتهم.', 138),
         frame(3, 'click (380, 400)', scene(3, ['-0.69', '-0.58', '-0.06', '0.5', '0.19', '-0.67'], 1), 'نقطة تالتة: لسه مالهاش شريك، فبتترسم كنقطة بس لحد الدوسة الجاية.', 138)]
    return story('من الدوسة للخط', 'البرنامج 2 · الأرقام من التشغيل الحقيقي', f)
