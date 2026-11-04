# Step-by-step storyboards: each frame = the line that just ran + the state of memory/GPU after it.
import html
BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, SOFT, RED, GREEN, PINK = '#2563eb', '#0d9488', '#c2410c', '#7c3aed', '#8a8f98', '#1d2330', '#eef1f6', '#dc2626', '#16a34a', '#db2777'

CSS = '''
.story { margin:3mm 0 5mm; border:1px solid #c7d2fe; border-radius:3mm; background:#f8faff; padding:2.5mm 3mm 1mm; }
.frame:nth-child(2n+1) { margin-left:0; }
.story .sthead { page-break-after:avoid; font-weight:bold; color:#3730a3; font-size:10.5pt; margin:0 1mm 2mm; }
.story .sthead span { font-weight:normal; color:#5b6372; font-size:9.5pt; }
.frames { font-size:0; }
.frame { display:inline-block; vertical-align:top; box-sizing:border-box; width:48.5%; margin:0 0 2mm 3%; font-size:10pt; background:#fff; border:1px solid #e2e6ee; border-radius:2mm; page-break-inside:avoid; overflow:hidden; }
.fhead { display:flex; align-items:center; gap:2mm; background:#141a26; padding:1.2mm 2mm; }
.fnum { flex:none; width:5mm; height:5mm; border-radius:50%; background:#6366f1; color:#fff; font-size:8pt; font-weight:bold; display:inline-flex; align-items:center; justify-content:center; }
.fcode { color:#e6e9ef; font-family:"JetBrains Mono","DejaVu Sans Mono",monospace; font-size:7.6pt; direction:ltr; text-align:left; flex:1; white-space:pre-wrap; word-break:break-word; }
.frame svg { display:block; width:100%; height:auto; }
.fcap code { font-size:8.5pt; }
@media screen and (max-width:640px) { .frame { width:100%; margin-left:0; } }
.fcap { font-size:9pt; line-height:1.5; padding:1mm 2.5mm 1.8mm; color:#1f2937; }
'''

def _defs(cols):
    return '<defs>' + ''.join(
        f'<marker id="sb{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
        for c in cols) + '</defs>'

def svgf(body, h=150, w=320):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" direction="ltr" style="direction:ltr">{_defs([BLUE, RED, GREEN, ORANGE, TEAL, PURPLE, GRAY, PINK])}<g font-family="DejaVu Sans, sans-serif" font-size="11" fill="{INK}">{body}</g></svg>'

STATES = {
    'n': (SOFT, '#c9d1de', INK), 'new': ('#dbeafe', BLUE, INK), 'chg': ('#dcfce7', GREEN, '#14532d'),
    'free': ('#f3f4f6', '#d1d5db', '#9ca3af'), 'ptr': ('#ffffff', BLUE, BLUE), 'warn': ('#fee2e2', RED, '#7f1d1d'),
    'hot': ('#fef3c7', '#d97706', '#78350f'), 'pink': ('#fce7f3', PINK, INK), 'gpu': ('#ecfdf5', TEAL, INK),
}
def cell(x, y, w, h, val, st='n', fs=11, dash=False, bold=True):
    f, s, t = STATES[st]
    d = ' stroke-dasharray="4 3"' if (dash or st == 'ptr') else ''
    b = ' font-weight="bold"' if bold else ''
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{f}" stroke="{s}" stroke-width="1.4"{d}/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 4}" text-anchor="middle" fill="{t}" font-size="{fs}"{b}>{html.escape(str(val))}</text>')
def lbl(x, y, t, c=GRAY, s=9.5, a='middle', b=False):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" fill="{c}" font-size="{s}"{" font-weight=\"bold\"" if b else ""}>{html.escape(t)}</text>'
def arr(x1, y1, x2, y2, c=BLUE, dash=False, curve=None, w=1.8):
    d = ' stroke-dasharray="4 3"' if dash else ''
    if curve:
        return f'<path d="M{x1} {y1} Q{curve[0]} {curve[1]} {x2} {y2}" fill="none" stroke="{c}" stroke-width="{w}" marker-end="url(#sb{c[1:]})"{d}/>'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" marker-end="url(#sb{c[1:]})"{d}/>'
def region(x, y, w, h, title, c=GRAY, fill='#fafafa'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{c}" stroke-dasharray="3 3"/>' + lbl(x + 6, y + 12, title, c, 9, 'start', True)
def cross(x, y, w, h, c=RED):
    return f'<g stroke="{c}" stroke-width="2"><line x1="{x}" y1="{y}" x2="{x + w}" y2="{y + h}"/><line x1="{x + w}" y1="{y}" x2="{x}" y2="{y + h}"/></g>'
def termbox(x, y, w, lines):
    h = 14 + 13 * len(lines)
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#0b0f17"/>'
    for i, l in enumerate(lines):
        s += f'<text x="{x + 6}" y="{y + 16 + 13 * i}" fill="#b8f2c4" font-family="DejaVu Sans Mono, monospace" font-size="9.5">{html.escape(l)}</text>'
    return s

def frame(n, code, body, cap, h=150):
    return (f'<div class="frame"><div class="fhead"><span class="fnum">{n}</span><span class="fcode">{html.escape(code)}</span></div>'
            f'{svgf(body, h)}<div class="fcap">{cap}</div></div>')
def story(title, sub, frames):
    return (f'<div class="story"><div class="sthead">🎬 خطوة بخطوة: {title} <span>· {sub}</span></div>'
            '<div class="frames">' + ''.join(frames) + '</div></div>')

# ======================================================================= DAY 1
def d1_deref():
    VAR = lambda v, st: cell(40, 45, 80, 40, v, st) + lbl(80, 100, 'var  @ …9ac', BLUE)
    PTR = cell(190, 45, 100, 40, '…9ac', 'ptr', 10) + lbl(240, 100, 'ptr', BLUE)
    STK = region(20, 20, 285, 95, 'STACK')
    f = [frame(1, 'int var = 8;', STK + VAR(8, 'new'), 'اتعمل «بيت» اسمه <code>var</code> وجواه 8، ليه عنوان (…9ac).'),
         frame(2, 'int* ptr = &var;', STK + VAR(8, 'n') + PTR + arr(190, 65, 123, 65), 'اتعمل <code>ptr</code> وجواه <b>عنوان</b> var، مش قيمته. السهم = «بيشاور على».'),
         frame(3, '*ptr = 10;', STK + VAR(10, 'chg') + PTR + arr(190, 65, 123, 65, GREEN, w=2.4), 'النجمة = امشي على السهم. رحنا لـ var وكتبنا 10 مكان 8.'),
         frame(4, 'std::cout << var;', STK + VAR(10, 'n') + PTR + arr(190, 65, 123, 65) + termbox(20, 122, 140, ['10']), 'لما نطبع <code>var</code> نفسه يطلع 10، لأننا غيرناه من خلال عنوانه.', 170)]
    return story('روح للعنوان وغيّر اللي جواه', 'كود 4', f)

def d1_heap():
    def heap(vals, st):
        s = region(150, 20, 160, 90, 'HEAP', ORANGE, '#fffaf5')
        for i, v in enumerate(vals):
            s += cell(158 + i * 18.5, 50, 16, 30, v, st, 9)
        return s
    STK = region(10, 20, 125, 90, 'STACK')
    B = lambda st='ptr': cell(22, 50, 100, 30, 'buffer = 0x55…', st, 9.5)
    f = [frame(1, 'char* buffer = new char[8];', STK + B() + heap('????????', 'new') + arr(122, 65, 156, 65), '<code>new</code> حجزت 8 بايت في الـ Heap وادتنا عنوانهم. اللي جواهم لسه مجهول (<b>؟</b>): بواقي قديمة.'),
         frame(2, 'memset(buffer, 0, 8);', STK + B() + heap('00000000', 'chg') + arr(122, 65, 156, 65, GREEN), '<code>memset</code> راحت للعنوان وكتبت 0 في الـ 8 بايت.'),
         frame(3, 'delete[] buffer;', STK + B('warn') + heap('        ', 'free') + cross(158, 50, 145, 30) + arr(122, 65, 156, 65, RED, True), 'الـ 8 بايت رجعوا للنظام. بس <code>buffer</code> لسه شايل العنوان القديم! ده Pointer «بايظ»: ماتستخدموش تاني.')]
    return story('حجز ذاكرة ورجوعها', 'كود 5', f)

def d1_chain():
    STK = region(10, 18, 160, 112, 'STACK')
    PP = lambda st='ptr': cell(22, 40, 60, 30, 'ptr', st, 10)
    BU = lambda st='ptr': cell(100, 40, 60, 30, 'buffer', st, 10)
    def heap(st0='n'):
        s = region(185, 18, 130, 112, 'HEAP', ORANGE, '#fffaf5')
        for i in range(4):
            s += cell(195 + i * 29, 45, 26, 26, 0, st0 if i == 0 else 'n', 10)
        return s
    base = STK + heap()
    f = [frame(1, 'char* buffer = new char[8];', STK + BU() + heap() + arr(160, 55, 193, 57), 'زي الكود اللي فات: <code>buffer</code> بيشاور على البيانات.'),
         frame(2, 'char** ptr = &buffer;', base + PP('new') + BU() + arr(82, 55, 98, 55, PURPLE) + arr(160, 55, 193, 57), '<code>ptr</code> بيشاور على <code>buffer</code> نفسه (عنوان لعنوان).'),
         frame(3, '*ptr', base + PP() + BU('hot') + arr(82, 55, 98, 55, PURPLE, w=2.4) + arr(160, 55, 193, 57) + lbl(130, 95, '= the address of the data', ORANGE, 9), 'نجمة واحدة = خطوة واحدة على السهم: وصلنا لـ <code>buffer</code>، يعني عنوان البيانات.'),
         frame(4, '(*ptr)[0]', STK + heap('hot') + PP() + BU() + arr(82, 55, 98, 55, PURPLE, w=2.4) + arr(160, 55, 193, 57, ORANGE, w=2.4) + lbl(208, 95, 'the data: 0', ORANGE, 9), 'خطوة تانية + <code>[0]</code>: وصلنا للبايت الأول من البيانات نفسها.')]
    return story('سلسلة النجمتين', 'كود 6', f)

def d1_gpu():
    def panels(cpu='', gpu=''):
        return (region(6, 18, 118, 120, 'C++  (RAM)', BLUE, '#f8fbff') + region(140, 18, 175, 120, 'GPU  (VRAM)', TEAL, '#f5fffb') + cpu + gpu)
    CPU = cell(14, 34, 102, 22, 'positions[8]', 'new', 9) + cell(14, 62, 102, 22, 'indices[6]', 'new', 9)
    VAO = lambda st='gpu', t='VAO (empty)': cell(148, 32, 160, 22, t, st, 9)
    VBO = lambda st='gpu': cell(148, 60, 160, 22, 'VBO: 8 floats', st, 9)
    IBO = lambda st='gpu': cell(148, 88, 75, 22, 'IBO: 0,1,2…', st, 8.5)
    PRG = lambda st='gpu', t='shader ✓': cell(228, 88, 80, 22, t, st, 8.5)
    f = [frame(1, 'float positions[] = {…};  unsigned int indices[] = {…};', panels(CPU), 'البيانات لسه في ذاكرة الجهاز العادية. كارت الشاشة فاضي.'),
         frame(2, 'glGenVertexArrays(1, &vao); glBindVertexArray(vao);', panels(CPU, VAO('new')), 'اتعمل VAO: «دفتر» فاضي هيتسجل فيه كل الإعدادات الجاية.'),
         frame(3, 'glBufferData(GL_ARRAY_BUFFER, …, positions, …);', panels(CPU, VAO() + VBO('new')) + arr(116, 45, 146, 71, TEAL), 'الأركان <b>اتنسخت</b> لذاكرة كارت الشاشة (VBO).'),
         frame(4, 'glVertexAttribPointer(0, 2, GL_FLOAT, …);', panels(CPU, VAO('hot', 'VAO: slot 0 = 2 floats') + VBO()), 'الـ VAO اتسجل فيه: «الخانة 0 = كل ركن رقمين من الـ VBO».'),
         frame(5, 'glBufferData(GL_ELEMENT_ARRAY_BUFFER, …, indices, …);', panels(CPU, VAO('gpu', 'VAO: slot 0 = 2 floats') + VBO() + IBO('new')) + arr(116, 73, 146, 99, TEAL), 'ترتيب الرسم كمان اتنسخ (IBO).'),
         frame(6, 'glUseProgram(shader);', panels(CPU, VAO('gpu', 'VAO: slot 0 = 2 floats') + VBO() + IBO() + PRG('new')), 'برنامج الـ Shader اتعمل واتشغّل.'),
         frame(7, 'glUniform4f(location, r, 0.3f, 0.8f, 1.0f);', panels(CPU + cell(14, 96, 102, 22, 'r = 0.35', 'hot', 9), VAO('gpu', 'VAO: slot 0 = 2 floats') + VBO() + IBO() + PRG('hot', 'u_Color =')) + arr(116, 107, 226, 101, ORANGE), 'اللون اتحط في خانة <code>u_Color</code> جوه البرنامج. ده الشيء الوحيد اللي بيتبعت كل فريم.'),
         frame(8, 'glDrawElements(…); glfwSwapBuffers(window);', panels(CPU, VAO('gpu', 'VAO: slot 0 = 2 floats') + VBO() + IBO() + PRG()) + f'<rect x="188" y="114" width="120" height="20" fill="#5a55cc"/>' + lbl(150, 128, 'screen:', TEAL, 9, 'start', True), 'كارت الشاشة استخدم كل اللي فوق ورسم المربع، و <code>SwapBuffers</code> عرضه على الشاشة.')]
    return story('الـ C++ بيجهّز كارت الشاشة إزاي', 'البرنامج 1 و 2 · كل ده بيحصل مرة واحدة قبل اللوب ماعدا خطوة 7 و 8', f)

def d1_dot():
    def boxes(hl):
        s = ''
        for i, (a, b) in enumerate([(1, 3), (2, 4)]):
            y = 30 + i * 40
            sa = 'hot' if hl == i else 'n'
            s += cell(30, y, 40, 30, a, sa) + lbl(85, y + 20, '×', INK, 13) + cell(100, y, 40, 30, b, sa)
        return s + lbl(50, 22, 'v', ORANGE, 11, b=True) + lbl(120, 22, 'w', BLUE, 11, b=True)
    f = [frame(1, '[1, 2] · [3, 4]   — first pair', boxes(0) + lbl(160, 50, '= 3', GREEN, 13, 'start', True), 'خد أول رقم من كل واحد واضربهم: 1 × 3 = 3.'),
         frame(2, 'second pair', boxes(1) + lbl(160, 50, '3', GRAY, 13, 'start') + lbl(160, 90, '= 8', GREEN, 13, 'start', True), 'بعدين التاني: 2 × 4 = 8.'),
         frame(3, 'add them up', boxes(-1) + lbl(160, 50, '3', INK, 13, 'start') + lbl(160, 90, '8', INK, 13, 'start') + f'<line x1="155" y1="100" x2="215" y2="100" stroke="{INK}"/>' + lbl(160, 122, '11', GREEN, 15, 'start', True) + lbl(205, 122, '← one number', GRAY, 9.5, 'start'), 'اجمع: 3 + 8 = 11، وده نفس اللي البرنامج طبعه. النتيجة <b>رقم واحد</b> مش متجه.')]
    return story('حساب [1, 2] · [3, 4]', 'نفس اللي بيعمله لوب <code>sum += v[i] * w[i]</code> في الكود', f)

def d1_camera():
    # top view: x to the right, z downward (towards the viewer), pyramid at origin. scale 40px per unit, origin at (160, 55)
    def view(px, pz, ox, oz, hl=False):
        X = lambda x: 160 + x * 40
        Z = lambda z: 40 + z * 40
        s = ''.join(f'<line x1="{X(i)}" y1="{Z(-0.6)}" x2="{X(i)}" y2="{Z(3.0)}" stroke="#eef1f6"/>' for i in range(-3, 4))
        s += ''.join(f'<line x1="{X(-3.5)}" y1="{Z(j)}" x2="{X(3.5)}" y2="{Z(j)}" stroke="#eef1f6"/>' for j in range(0, 4))
        s += f'<rect x="{X(-0.5)}" y="{Z(-0.5)}" width="40" height="40" fill="#f59e0b" opacity=".85"/>' + lbl(X(0), Z(0) + 4, 'pyramid', '#78350f', 8)
        s += f'<circle cx="{X(px)}" cy="{Z(pz)}" r="6" fill="{PURPLE}"/>'
        s += arr(X(px), Z(pz), X(px + ox * 1.1), Z(pz + oz * 1.1), ORANGE, w=2.4)
        s += lbl(8, 145, f'Position = ({px:.2f}, 0, {pz:.2f})', PURPLE if hl else INK, 9.5, 'start', True)
        s += lbl(8, 160, f'Orientation = ({ox:.2f}, 0, {oz:.2f})', ORANGE, 9.5, 'start', True)
        s += lbl(300, 16, 'top view', GRAY, 8.5, 'end')
        return s
    f = [frame(1, 'Camera camera(width, height, glm::vec3(0.0f, 0.0f, 2.0f));', view(0, 2, 0, -1), 'الكاميرا (النقطة البنفسجي) واقفة ورا الهرم بمسافة 2، وبتبص لقدام (السهم) ناحيته.', 168),
         frame(2, 'W × 10 frames:  Position += speed * Orientation;', view(0, 1, 0, -1, True), 'كل فريم +0.1 (speed) في اتجاه السهم. بعد 10 فريمات قرّبنا وحدة كاملة.', 168),
         frame(3, 'D × 10 frames:  Position += speed * normalize(cross(Orientation, Up));', view(1, 2, 0, -1, True), 'من البداية تاني: D بتحرّك يمين (عمودي على السهم). المكان اتغير، والسهم زي ما هو.', 168),
         frame(4, 'mouse 100px right × 2 frames:  Orientation = rotate(Orientation, radians(-rotY), Up);', view(0, 2, 0.42, -0.91), 'الماوس ما حرّكش المكان خالص. كل فريم <code>rotY</code> = 100 × 100 ÷ 800 = 12.5°، فبعد فريمين السهم لف 25° يمين.', 168)]
    return story('متغيرات الكاميرا بعد كل زرار', 'الأرقام محسوبة بنفس معادلات Camera.cpp (expcam/story_nums.cpp) · المنظر من فوق', f)

# ======================================================================= DAY 2
def d2_malloc():
    STK = region(8, 18, 110, 92, 'STACK')
    def heap(vals, st):
        s = region(130, 18, 185, 92, 'HEAP', ORANGE, '#fffaf5')
        for i, v in enumerate(vals):
            s += cell(138 + i * 35, 50, 32, 30, v, st, 10)
        return s + lbl(222, 100, '5 ints × 4 bytes = 20 bytes', ORANGE, 8.5)
    N = lambda st='ptr': cell(16, 50, 94, 30, 'numbers', st, 10)
    f = [frame(1, 'int* numbers = malloc(count * sizeof(int));', STK + N() + heap('?????', 'new') + arr(110, 65, 136, 65), 'اتحجز 20 بايت في الـ Heap. اللي جواهم مجهول.'),
         frame(2, 'for (…) numbers[i] = i * 10;', STK + N() + heap(['0', '10', '20', '30', '40'], 'chg') + arr(110, 65, 136, 65, GREEN), 'اللوب ملا الخانات: 0، 10، 20، 30، 40.'),
         frame(3, 'free(numbers);', STK + N('warn') + heap('     ', 'free') + cross(138, 50, 172, 30) + arr(110, 65, 136, 65, RED, True), 'الذاكرة رجعت. و <code>numbers</code> لسه شايل العنوان، فماتلمسوش تاني (زي <code>delete[]</code> بالظبط).')]
    return story('malloc و free', 'برنامج 2', f)

def d2_arith():
    def st(k):
        s = ''
        for i, v in enumerate([10, 20, 30, 40]):
            s += cell(20 + i * 72, 55, 64, 34, v, 'hot' if i == k else 'n') + lbl(52 + i * 72, 104, ['…e40', '…e44', '…e48', '…e4c'][i], GRAY, 9)
        x = 52 + k * 72
        s += cell(x - 32, 8, 64, 24, 'p', 'ptr', 10) + arr(x, 32, x, 53)
        return s + termbox(20, 112, 280, [f'p = …{["e40", "e44", "e48", "e4c"][k]}   *p = {(k + 1) * 10}'])
    f = [frame(i + 1, 'printf(…); p++;' if i else 'int* p = arr;   printf(…);', st(i), cap, 145) for i, cap in enumerate([
        '<code>p</code> بيشاور على أول خانة (10).', 'بعد <code>p++</code>: العنوان زاد 4 (من e40 لـ e44)، فبقى على 20.',
        '<code>p++</code> تاني: +4 كمان، على 30.', 'آخر واحدة: 40. ولو عملنا <code>p++</code> كمان هنطلع برا المصفوفة (جربناها: الأداة مسكتها).'])]
    return story('p++ بيمشي على المصفوفة', 'برنامج 3 · العناوين من التشغيل الحقيقي', f)

def d2_double():
    MAIN = region(8, 18, 140, 100, 'main()', BLUE, '#f8fbff')
    def score(v, st): return cell(30, 52, 96, 34, f'score = {v}', st, 11)
    FN = region(170, 18, 145, 100, 'doubleIt()', PURPLE, '#faf7ff')
    NUM = cell(185, 52, 115, 34, 'number = &score', 'ptr', 9.5)
    f = [frame(1, 'int score = 21;', MAIN + score(21, 'new'), 'في <code>main</code> عندنا <code>score</code> = 21.'),
         frame(2, 'doubleIt(&score);', MAIN + score(21, 'n') + FN + NUM + arr(185, 69, 128, 69, PURPLE), 'الدالة اشتغلت، ومدخلها <code>number</code> جواه <b>عنوان</b> score.'),
         frame(3, '*number = *number * 2;', MAIN + score(42, 'chg') + FN + NUM + arr(185, 69, 128, 69, GREEN, w=2.4), 'الدالة مشيت على السهم، وضربت اللي هناك في 2. التعديل حصل في <code>score</code> نفسه.'),
         frame(4, 'std::cout << "after:  " << score;', MAIN + score(42, 'n') + region(170, 18, 145, 100, 'doubleIt() — finished', GRAY, '#f9fafb') + termbox(178, 50, 128, ['after:  42']), 'الدالة خلصت واتمسحت، بس التغيير فضل، لأنه حصل في <code>main</code>.')]
    return story('دالة بتغيّر متغير مش بتاعها', 'برنامج 4', f)

def d2_va():
    def row(v):
        s = ''
        names = ['x', 'y', 'r', 'g', 'b']
        for i in range(15):
            vert, k = divmod(i, 5)
            st = ('new' if k < 2 else 'pink') if vert == v else 'n'
            s += cell(8 + i * 20.3, 40, 18, 26, names[k], st, 8.5)
        for vert in range(3):
            s += lbl(8 + vert * 101.5 + 50, 82, f'vertex {vert}', BLUE if vert == v else GRAY, 9, b=vert == v)
        x0 = 8 + v * 101.5
        s += cell(x0, 96, 60, 22, 'aPosition', 'new', 8.5) + arr(x0 + 19, 68, x0 + 25, 94, BLUE)
        s += cell(x0 + 62, 96, 44, 22, 'aColor', 'pink', 8.5) + arr(x0 + 70, 68, x0 + 80, 94, PINK)
        if v > 0:
            s += arr(8 + (v - 1) * 101.5 + 10, 30, x0 + 8, 30, TEAL, curve=(8 + (v - 0.5) * 101.5, 8)) + lbl(8 + (v - 0.5) * 101.5 + 8, 14, '+20 bytes (stride)', TEAL, 8.5)
        return s
    f = [frame(1, 'vertex shader run #1', row(0), 'كارت الشاشة بيبدأ من أول الـ buffer. أول رقمين بيروحوا لـ <code>aPosition</code>. وبعد 8 بايت (offset) فيه 3 أرقام بيروحوا لـ <code>aColor</code>.', 125),
         frame(2, 'vertex shader run #2', row(1), 'ينط 20 بايت (stride) ويعيد نفس القراية للركن التاني.', 125),
         frame(3, 'vertex shader run #3', row(2), 'ينط 20 كمان للركن التالت. 3 أركان = الـ Vertex Shader اشتغل 3 مرات.', 125)]
    return story('كارت الشاشة بيقرا الـ buffer إزاي', 'البرنامج 2 · ده اللي بيقوله <code>glVertexAttribPointer</code> بالظبط', f)

def d2_length():
    f = [frame(1, 'dot(a, a, 2)  — square each number', cell(30, 40, 50, 34, 2) + lbl(105, 62, '→  2 × 2 = 4', INK, 11, 'start') + cell(30, 84, 50, 34, 5) + lbl(105, 106, '→  5 × 5 = 25', INK, 11, 'start'), 'المتجه في نفسه = كل رقم في نفسه (مربعه).'),
         frame(2, 'sum += …', lbl(40, 62, '4 + 25', INK, 13, 'start') + lbl(40, 100, '= 29', GREEN, 16, 'start', True) + lbl(130, 100, '← length squared', GRAY, 9.5, 'start'), 'اجمعهم: 29. ده «مربع الطول».'),
         frame(3, 'std::sqrt(29)', lbl(40, 62, '√29', INK, 15, 'start') + lbl(40, 100, '= 5.385', GREEN, 16, 'start', True) + lbl(150, 100, '← the length', GRAY, 9.5, 'start'), 'الجذر = الطول الحقيقي. وده نفس الرقم اللي البرنامج طبعه.')]
    return story('حساب طول [2, 5]', 'نفس ترتيب الكود: dot الأول، وبعدين sqrt', f)

def d2_growth():
    data = [(1, 1, 'A', True), (2, 2, 'B', True), (3, 4, 'C', True), (4, 4, 'C', False), (5, 8, 'D', True)]
    fr = []
    for n, (size, cap, addr, moved) in enumerate(data, 1):
        s = ''
        if moved and n > 1:
            pc = data[n - 2][1]
            for i in range(pc):
                s += cell(10 + i * 30, 22, 26, 24, i + 1, 'free', 9)
            s += lbl(12 + pc * 30, 38, 'old (freed)', GRAY, 8.5, 'start')
            s += arr(22, 48, 22, 66, ORANGE) + lbl(32, 61, 'copy', ORANGE, 8.5, 'start')
        for i in range(cap):
            st = 'new' if i == size - 1 else ('n' if i < size else 'free')
            s += cell(10 + i * 30, 70, 26, 26, i + 1 if i < size else '', st, 9)
        s += lbl(10, 118, f'size {size} · capacity {cap} · address {addr}', BLUE if moved else INK, 10, 'start', True)
        cap_txt = ('اتنقل لمكان جديد أكبر: اتحجز ' + str(cap) + '، واتنسخ القديم، والقديم رجع.') if (moved and n > 1) else ('أول عنصر: اتحجز مكان لواحد.' if n == 1 else 'فيه مكان فاضي، فاتحط على طول من غير نقل.')
        fr.append(frame(n, f'numbers.push_back({size});', s, cap_txt, 130))
    return story('الـ vector وهو بيكبر', 'برنامج 5 · الأرقام من التشغيل الحقيقي (g++)', fr)

def d2_erase():
    V = lambda vals, sts: ''.join(cell(20 + i * 95, 45, 88, 34, v, sts[i], 10) for i, v in enumerate(vals))
    f = [frame(1, 'vertices.push_back(…) × 2', V(['1, 2, 3', '4, 5, 6'], ['n', 'n']) + lbl(20, 105, 'size = 2', INK, 10, 'start', True), 'القايمة فيها نقطتين.', 120),
         frame(2, 'vertices.erase(vertices.begin() + 1);', V(['1, 2, 3', '4, 5, 6'], ['n', 'warn']) + cross(115, 45, 88, 34) + lbl(20, 22, 'begin()', BLUE, 9, 'start') + arr(45, 26, 55, 43, BLUE) + lbl(140, 22, 'begin() + 1', RED, 9, 'start') + arr(160, 26, 160, 43, RED) + lbl(20, 105, 'size = 1', INK, 10, 'start', True), '<code>begin()</code> = أول عنصر، و <code>+1</code> = اللي بعده. اتمسح.', 120),
         frame(3, 'vertices.clear();', V(['', ''], ['free', 'free']) + lbl(20, 105, 'size = 0', INK, 10, 'start', True), 'كل حاجة اتمسحت.', 120)]
    return story('المسح من الـ vector', 'برنامج 3', f)

def d2_dangling():
    f = [frame(1, 'Vertex* first = &vertices[0];', cell(20, 55, 70, 30, '1, 2, 3', 'n', 10) + lbl(55, 100, 'capacity 1', GRAY, 9) + cell(170, 55, 80, 30, 'first', 'ptr', 10) + arr(170, 70, 92, 70), '<code>first</code> شايل عنوان أول نقطة. لحد هنا تمام.', 115),
         frame(2, 'vertices.push_back({ 4, 5, 6 });', cell(20, 25, 70, 26, '1, 2, 3', 'free', 9) + cross(20, 25, 70, 26) + lbl(55, 64, 'old (freed)', GRAY, 8.5) + cell(140, 75, 70, 28, '1, 2, 3', 'n', 9) + cell(214, 75, 70, 28, '4, 5, 6', 'new', 9) + lbl(212, 118, 'new place', BLUE, 9) + cell(170, 20, 80, 26, 'first', 'warn', 10) + arr(170, 33, 92, 38, RED, True), 'القايمة اتملت، فاتنقلت لمكان جديد والقديم رجع. بس <code>first</code> لسه بيشاور على القديم!', 125),
         frame(3, 'first->x', cell(20, 25, 70, 26, '?', 'free', 9) + cross(20, 25, 70, 26) + cell(170, 20, 80, 26, 'first', 'warn', 10) + arr(170, 33, 92, 38, RED, True) + termbox(20, 70, 285, ['ERROR: heap-use-after-free']), 'القراية من مكان اترجع. الأداة مسكتها، ومن غيرها ممكن تقرا رقم بايظ وماتعرفش.', 125)]
    return story('ليه ماتحتفظش بعنوان عنصر في vector', 'التجربة رقم 7 في «ليه كتبناها» بتاعة الـ vector', f)
