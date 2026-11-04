# Week 2 · Day 7 (Saturday 31-10). Same structure as Days 1-6. MODE="web" builds the copy page; default builds the PDF.
import html, re, os, base64, sys
for d in ('day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7'):
    sys.path.insert(0, f'/home/claude/{d}')
import weasyprint
import diagrams as D1
import diag7 as D
from data7 import E, OVER
from words7 import *
import why_day7 as WHY
import sb as SB
import sb7 as SB7
import quick as Q
import quick7 as Q7

os.chdir('/home/claude/day7')
MODE = globals().get('MODE', 'pdf')
ART = os.environ.get('ART_URL', '').strip()
css = open('final.css', encoding='utf-8').read()
exec(open('hl_src.py', encoding='utf-8').read())
KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4|struct|size_t|auto|enum|static|extern|mutable|private|using|namespace|import|as|def|continue)\b'

def rd(p): return open(p).read()
def term(t): return '<div class="run"><div class="bar">● ● ●  &nbsp;Terminal — output after Run</div>' + html.escape(t.rstrip('\n')) + '</div>'
def res(body, title='▶ النتيجة لما نعمل Run'): return f'<div class="result"><div class="rh">{title}</div>{body}</div>'
def shot(img, cap): return f'<td><img src="img/{img}.png"><div class="cap">{cap}</div></td>'
def grid(cells, cols):
    rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
    return '<table class="shots">' + ''.join('<tr>' + ''.join(r) + '</tr>' for r in rows) + '</table>'
def bigimg(name, cap, w='80mm'):
    return f'<img src="img/{name}.png" style="width:{w};display:block;margin:2mm auto;border-radius:2mm"><div style="text-align:center;font-size:9.5pt;color:#5b6372;margin-bottom:2mm">{cap}</div>'
LEGEND = ('<div class="legend"><span class="badge b-req">إجباري</span> = من غيره مش هيشتغل أو هيطلع غلط · <span class="badge b-imp">مش إجباري، بس مهم جداً</span> = هيشتغل، بس هتتعب · '
          '<span class="badge b-opt">اختياري</span> = تحسين أو مثال</div>')

def prog(path, label, new=None):
    STH.seen(path)
    aid = re.sub(r'[^A-Za-z0-9_-]', '-', label)
    raw = open(path).read().rstrip('\n') + '\n'
    over = OVER.get(os.path.basename(path), {})
    if MODE == 'web':
        head = (f'<div class="copybar" id="{aid}"><span class="fname"><span class="ltr">{label}</span></span>'
                f'<button type="button" class="copy" data-src="src-{aid}">📋 نسخ الكود كامل</button></div>'
                f'<pre class="rawsrc" id="src-{aid}" hidden>{html.escape(raw)}</pre>')
    else:
        link = STH.copylink(aid, label, raw)
        head = f'<div class="fname"><span class="ltr">{label}</span></div>{link}'
    h = [f'<!--PROG:{os.path.abspath(path)}-->' + head + '<table class="cl">']
    for lnum, line in enumerate(open(path), 1):
        t = line.rstrip('\n')
        if not t.strip(): continue
        isnew = new is not None and t.strip() in new
        cls = ' class="new"' if isnew else (' class="br"' if t.strip() in ('{', '}', '};') else '')
        e = over[t.strip()] if t.strip() in over else E[t.strip()]
        if isnew: e = '<b>★ جديد:</b> ' + e
        rid = ''
        if WMARK in e:
            w_ = wid(t.strip()); rid = f'r-{w_}-{len(REFS.setdefault(w_, [])) + 1}'; REFS[w_].append((label, lnum, rid))
            e = e.replace(WMARK, f' <a class="wlink" href="#{w_}">(شرحه كلمة كلمة فوق 🔗)</a>')
        h.append(f'<tr{cls}{f" id={chr(34)}{rid}{chr(34)}" if rid else ""}><td class="k"><i class="ln">{lnum}</i>{hl(t)}</td><td class="e">{e}</td></tr>')
    h.append('</table>')
    return ''.join(h)

REFS = {}
WMARK = ' <span style="color:#2563eb">(شرحه كلمة كلمة فوق)</span>'
import hashlib as _hl
def wid(line): return 'w-' + _hl.md5(re.sub(r'\s+', ' ', line.strip()).encode()).hexdigest()[:10]
def link_words(h):
    seen = set()
    def add(m):
        i = wid(html.unescape(m.group(1)))
        if i in seen: return m.group(0)
        seen.add(i)
        back = ''.join(f'<a class="wback" href="#{rid}">↩ ارجع للسطر {ln} في <span class="ltr">{lb}</span></a>' for lb, ln, rid in REFS.get(i, []))
        return (f'<div class="wline" id="{i}"><div class="wcode"><span class="ltr">{m.group(1)}</span></div>'
                + (f'<div class="wbacks">{back}</div>' if back else ''))
    h = re.sub(r'<div class="wline"><div class="wcode"><span class="ltr">(.*?)</span></div>', add, h)
    miss = set(re.findall(r'href="#(w-[0-9a-f]{10})"', h)) - seen
    if miss: print('WORD LINKS WITHOUT TARGET:', len(miss))
    def fix(m): return m.group(0) if m.group(1) in seen else '<span style="color:#2563eb">(شرحه كلمة كلمة فوق)</span>'
    return re.sub(r'<a class="wlink" href="#(w-[0-9a-f]{10})">\(شرحه كلمة كلمة فوق 🔗\)</a>', fix, h)

JPRE = r'(?:sw|sl|tr|w|r)-[A-Za-z0-9_-]+'
def jump_numbers(h):
    """every jump link and its target get the same number: after a jump, look for the 📍 with that number."""
    tg = set(re.findall(r'href="#(' + JPRE + ')"', h))
    ids = [m.group(1) for m in re.finditer(r'id="(' + JPRE + ')"', h) if m.group(1) in tg]
    num = {}
    for i in ids: num.setdefault(i, len(num) + 1)
    def a(m):
        i = m.group(2)
        return m.group(0) if i not in num else f'{m.group(1)}{m.group(3)}<b class="jn">{num[i]}</b></a>'
    h = re.sub(r'(<a [^>]*href="#(' + JPRE + r')"[^>]*>)(.*?)</a>', a, h, flags=re.S)
    def t(m):
        i = m.group(2)
        if i not in num: return m.group(0)
        badge = f'<span class="jbadge">📍 {num[i]}</span>'
        tag = m.group(1)
        if tag.startswith('<tr'): return m.group(0)
        return m.group(0) + badge
    h = re.sub(r'<div class="wline" id="(' + JPRE + r')"[^>]*>', lambda m: m.group(0) + (f'<span class="jbadge">📍 {num[m.group(1)]}</span>' if m.group(1) in num else ''), h)
    # code lines inside the step blocks: badge at the END of the line, so the code keeps its indentation
    h = re.sub(r'(<span class="[^"]*" id="(' + JPRE + r')"[^>]*>(?:(?!id="sl-).)*?<a class="wl-go"[^>]*>.*?</a>)', lambda m: m.group(0) + (f'<span class="jbadge">📍 {num[m.group(2)]}</span>' if m.group(2) in num else ''), h, flags=re.S)
    h = re.sub(r'(<tr[^>]* id="(' + JPRE + r')"[^>]*>(?:(?!</tr>).)*?<td class="e">)', lambda m: m.group(0) + (f'<span class="jbadge">📍 {num[m.group(2)]}</span>' if m.group(2) in num else ''), h, flags=re.S)
    print('jump numbers:', len(num))
    return h

def lec(cls, tag, title, meta):
    return f'<section class="lec {cls}"><div class="lec-head"><div class="tag">{tag}</div><h2>{title}</h2><div class="meta">{meta}</div></div>'

SRC = 'src/'
sys.path.insert(0, '/home/claude/steps')
import steps_hook as STH
STH.setup(['specs_d7'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثاني: المؤشرات والـ Shaders</div>
  <h1>اليوم السابع — السبت 31 أكتوبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> مراجعة الأسبوع (Pointers) — <span style="color:#5b6372">The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> تجربة حرة (Vertex Arrays) — <span style="color:#5b6372">The Cherno و learnopengl</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> اختبر نفسك (Cross product) — <span style="color:#5b6372">Khan Academy</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> Commit في Git — <span style="color:#5b6372">The Net Ninja و git-scm.com</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:5mm;background:#fffbeb"><b>النهارده يوم مراجعة:</b> Pointers و VAO و Cross product بأسئلة تصحّح نفسها. والـ CAD هيحفظ برنامج امبارح في Git.</div>
  <div class="howto" style="margin-top:5mm"><b>على Windows:</b> العناوين من غير <code>0x</code> وبتتغير كل تشغيلة. والـ IDs بتاعة Git هتختلف عندك (اسمك ووقتك).</div>
</section>''')

# ================================================================== 1 · pointers review
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'مراجعة الأسبوع: الـ Pointers', 'The Cherno · POINTERS in C++ (الحلقة 16، مراجعة) · <span class="ltr">youtu.be/DTxHyVn0ODg</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> «الـ Pointer مجرد رقم فيه عنوان في الذاكرة. خلاص كده.» (The Cherno). النوع موجود بس عشان الـ compiler يعرف يقرا ويكتب كام بايت.</div>
<p class="what">ده نفس فيديو يوم الأحد. البرنامج 1 بيمشي على كل أمثلة The Cherno بالترتيب ويطبع العناوين الحقيقية: <code>void*</code>، والكتابة من خلال <code>int*</code>، وحجم الـ Pointer، والـ Heap، والـ Pointer لـ Pointer. والبرنامج 2 «اختبر نفسك»: 4 دوال صغيرة بالـ Pointers، وكل واحدة ليها اختبار PASS أو FAIL زي exercism.</p>''')
P.append(D1.fig(D.p_chain(), 'العناوين الحقيقية من تشغيلة واحدة: <code>ptr</code> بيشاور على <code>var</code>، و <code>buffer</code> على الـ 8 بايت في الـ Heap، و <code>ptrToBuffer</code> على <code>buffer</code> نفسه.'))
P.append(POINTER_TABLE)
P.append('<h3 id="pointer-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(POINTER_WORDS))
P.append('<h3>البرنامج 1: كل أمثلة The Cherno في ملف واحد</h3><p class="what">كل سطر طباعة بيوريك القيمة والعنوان مع بعض.</p>'
         + prog(SRC + 'p1_pointers_review.cpp', 'pointers_review.cpp') + res(term(rd(SRC + 'p1_pointers_review.txt')) + '<p style="font-size:10pt"><code>&amp;var</code> و <code>ptr</code> نفس الرقم. و <code>*ptrToBuffer</code> = <code>buffer</code> بالظبط. والعناوين هتختلف عندك.</p>'))
P.append(SB7.d7_ptr())
P.append('<h3>البرنامج 2: اختبر نفسك</h3><p class="what">قبل ما تقرا الشرح: حاول تتوقع كل دالة هتعمل إيه. وبعدين شغّل.</p>'
         + prog(SRC + 'p2_pointer_quiz.cpp', 'pointer_quiz.cpp') + res(term(rd(SRC + 'p2_pointer_quiz.txt'))))
P.append('<h3 id="why-pointers">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_pointers() + '<h3>البرنامج 2</h3>' + WHY.build_quiz())
P.append('''<div class="sum"><b>الملخص:</b><ul><li><code>&amp;</code> = هات العنوان. <code>*</code> قدام اسم = روح للعنوان.</li>
 <li>النوع بيحدد كام بايت. الحجم نفسه 8 بايت لأي Pointer على 64-bit.</li>
 <li><code>new</code> ↔ <code>delete</code>، و <code>new[]</code> ↔ <code>delete[]</code>، مرة واحدة بس.</li>
 <li>عشان دالة تغيّر متغير: ابعتلها عنوانه. وعشان تغيّر Pointer: ابعتلها عنوانه (<code>**</code>).</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اطبع <code>sizeof(char**)</code> (لازم 8). 2. اكتب <code>void Fill(int* arr, int count, int value)</code> تملا مصفوفة، واعملها اختبار. 3. في البرنامج 1 اطبع <code>(void*)(buffer + 1)</code>: لازم يطلع عنوان <code>buffer</code> + 1.</div></section>''')

# ================================================================== 2 · vertex arrays
r1n = {l.strip() for l in open(SRC + 'r1_vertex_array.cpp') if l.strip()} - {l.strip() for l in open('/home/claude/day6/src/r1_animated_color.cpp') if l.strip()}
P.append(lec('l2', 'المحاضرة 2 · رسم', 'تجربة حرة: الـ Vertex Arrays', 'قناة The Cherno · Vertex Arrays in OpenGL · <span class="ltr">youtu.be/Bcs56Mm-FJY</span> · learnopengl.com'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Vertex Buffer فيه الأرقام. والـ VAO بيربط الـ Buffer بالـ Layout بتاعه (كل ركن كام رقم، وطوله كام بايت). فبدل ما تعيد 4 أوامر قبل كل رسمة، بتربط الـ VAO في سطر.</div>
<p class="what">النهارده «تجربة حرة»: بنجرب كلام The Cherno بنفسنا. البرنامج 1 هو كوده: الـ Core Profile، وتجربة «من غير VAO» بـ <code>glGetError</code>، وبعدين بنفك كل حاجة ونربط في اللوب. والبرنامج 2 بيرسم نفس الشكل بالطريقتين اللي The Cherno قارن بينهم، جنب بعض.</p>''')
P.append(D1.fig(D.v_vao_box(), 'جوه الـ VAO: تفعيل المدخل، والـ Layout مع الصندوق، وصندوق الترتيب. والـ Shader برّه.'))
P.append(VAO_TABLE)
P.append('<h3 id="vao-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(VAO_WORDS) + '<h4>ومن الأيام اللي فاتت (موجودين في كود النهارده)</h4>' + ''.join(REVIEW_WORDS))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD)، ونفس الـ Core Profile من يوم التلات.</div>')
P.append('<h3>البرنامج 1: كود The Cherno (نفك كل حاجة ونربط قبل الرسم)</h3><p class="what">ده برنامج امبارح (الأحمر بيطلع وينزل)، والسطور <b>بالأصفر</b> هي الجديدة: تجربة من غير VAO، وفك الـ 4 روابط، والربط في اللوب، وطباعة <code>glGetError</code>.</p>'
         + prog(SRC + 'r1_vertex_array.cpp', 'vertex_array.cpp', new=r1n)
         + res(term('\n'.join(rd(SRC + 'r1_vertex_array.txt').splitlines()[:5]))
               + grid([shot('r1_vertex_array_1', 'لقطة'), shot('r1_vertex_array_2', 'بعدها'), shot('r1_vertex_array_3', 'وبعدها')], 3)
               + '<p style="font-size:10pt">أول سطر: الأمر اللي قبل الـ VAO اترفض (1282). وبعد كده كل الفريمات 0: الربط في اللوب شغال.</p>', '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(SB7.d7_vao())
P.append(D1.fig(D.v_two_methods(), 'أوامر الربط في الفريم الواحد: الطريقة 1 بتعيد الصندوق والـ Layout، والطريقة 2 بتربط الـ VAO بس.'))
P.append(METHOD_TABLE)
P.append('<h3>البرنامج 2: الطريقتين جنب بعض</h3><p class="what">مربع (رقمين لكل ركن) ومثلث (3 أرقام لكل ركن): Layout مختلف. الشمال بالطريقة 2، واليمين بالطريقة 1. و <code>u_Offset</code> بيزحزح الرسمة شمال أو يمين.</p>'
         + prog(SRC + 'r2_two_methods.cpp', 'two_methods.cpp')
         + res(term(rd(SRC + 'r2_two_methods.txt')) + bigimg('r2_two_methods_1', 'الشمال (VAO لكل حاجة) واليمين (VAO واحد): قارنّاهم بالكمبيوتر بكسل بكسل، ونفس الصورة.'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append('<h3 id="why-vao">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_vao() + '<h3>البرنامج 2</h3>' + WHY.build_methods())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ VAO = الربط بين الـ Buffer والـ Layout، وصندوق الترتيب. مش الـ Shader.</li>
 <li><code>glVertexAttribPointer</code> هو اللي بيعمل الربط، بالصندوق المربوط وقتها.</li>
 <li>Core Profile = لازم VAO. والكارت بيرفض من غير ما يوقّف البرنامج: اسأل بـ <code>glGetError</code>.</li>
 <li>VAO لكل حاجة = أبسط. ولو عايز أسرع: قيس.</li></ul></div>
<div class="try"><b>جرّب بإيدك (تجربة حرة):</b> 1. زوّد شكل تالت (خط بـ <code>GL_LINES</code>) بـ VAO لوحده. 2. في الطريقة 1 بدّل ترتيب رسم المربع والمثلث: الصورة لازم تفضل زي ما هي. 3. اطبع <code>glGetError()</code> بعد كل سطر في الإعداد وشوف مين بيرجّع 1282 قبل الـ VAO.</div></section>''')

# ================================================================== 3 · cross product test
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'اختبر نفسك: الضرب الاتجاهي', 'Khan Academy · Cross product introduction (مراجعة) · <span class="ltr">youtu.be/pJzmiywagfY</span> · khanacademy.org/math/linear-algebra/vectors-and-spaces'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الضرب الاتجاهي بياخد متجهين في 3 أبعاد ويطلّع <b>متجه</b> عمودي على الاتنين. والصف الأوسط في القانون معكوس.</div>
<p class="what">نفس فيديو يوم التلات. النهارده «اختبر نفسك»: البرنامج 1 فيه 7 أسئلة بتصحّح نفسها (PASS أو FAIL)، بإيدنا من غير مكتبات. والبرنامج 2 نفس الكلام بـ NumPy، وأول استخدام حقيقي: الـ Normal بتاع مثلث (الاتجاه اللي «وشه» بيبص له)، اللي هنحتاجه في الإضاءة.</p>''')
P.append(D1.fig(D.x_rows(), 'قانون Khan صف صف على المثال: كل صف بيستخبى فيه عمود، والصف الأوسط بالعكس.'))
P.append(CROSS_TABLE)
P.append('<h3 id="cross-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CROSS_WORDS))
P.append('<h3>البرنامج 1: 7 أسئلة بتصحّح نفسها</h3><p class="what">جاوب كل سؤال في ورقة الأول، وبعدين شغّل.</p>'
         + prog(SRC + 'm1_cross_quiz.py', 'cross_quiz.py') + res(term(rd(SRC + 'm1_cross_quiz.txt'))))
P.append(D1.fig(D.x_hand(), 'شمال: i × j = k (قاعدة الإيد اليمين). يمين: ضلعين من نفس الركن، وضربهم الاتجاهي = Normal المثلث.'))
P.append('<h3>البرنامج 2: NumPy والـ Normal</h3><p class="what">نفس الأرقام في سطر، ومتجهين على نفس الخط، والـ Normal بتاع مثلث على الأرض.</p>'
         + prog(SRC + 'm2_numpy_cross.py', 'numpy_cross.py') + res(term(rd(SRC + 'm2_numpy_cross.txt')) + '<p style="font-size:10pt">الـ Normal = [0, 0, 6]: عمودي على المثلث (لفوق في z). وطوله 6 = مساحة المستطيل اللي ضلعيه 2 و 3.</p>'))
P.append('<h3 id="why-cross">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_cross())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>a × b = [a₂b₃ − a₃b₂, a₃b₁ − a₁b₃, a₁b₂ − a₂b₁]. الأوسط معكوس.</li>
 <li>الناتج عمودي على الاتنين: الضرب النقطي معاهم = 0.</li>
 <li>b × a = ‎−(a × b). ونفس الخط ← صفر. و 3 أبعاد بس.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. احسب [2, 3, 4] × [5, 6, 7] في ورقة، وبعدين زوّده سؤال في البرنامج 1 (الإجابة [‎-3, 6, ‎-3]). 2. اعكس ترتيب الضلعين في الـ Normal: لازم يطلع [0, 0, ‎-6].</div></section>''')

# ================================================================== 4 · git commit
P.append(lec('l4', 'المحاضرة 4 · CAD', 'Commit في Git', 'The Net Ninja · Git &amp; GitHub Tutorial #6: Making Commits · <span class="ltr">youtu.be/Fhgga2s_RmM</span> · git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Commit = نقطة حفظ (Snapshot) للمشروع في لحظة معينة، عليها رسالة بتقول إيه اللي اتغير. تقدر ترجع لأي نقطة بعدين.</div>
<p class="what">هنحط برنامج الـ CAD بتاع امبارح (<code>refactored.cpp</code>) في Git: أول Commit، وبعدين نغيّر سطر واحد ونعمل Commit تاني، ونشوف التاريخ. الجلسة دي اتشغلت فعلاً بـ Git حقيقي. وبعدين برنامج Python صغير بيحسب الـ ID بتاع أول Commit بإيده، ويطلع نفس الرقم.</p>''')
P.append(D1.fig(D.g_areas(), 'التلات صناديق: الفولدر اللي بتعدّل فيه، والـ Staging (اللي هيدخل الـ Commit الجاي)، والمستودع (كل الـ Commits).'))
P.append(GIT_TABLE)
P.append('<h3 id="git-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(GIT_WORDS))
_gs = rd(SRC + 'c1_git_session.txt').split('\n(in the editor')
_g2 = '(in the editor' + _gs[1]
_g2a, _g2b = _g2.split('$ git log\n', 1)
P.append('<h3>الجلسة: أول Commit</h3><p class="what">في الـ Terminal (على Windows: Git Bash أو PowerShell) جوه فولدر المشروع. أول سطرين مرة واحدة بس على الجهاز.</p>' + res(term(_gs[0]), '▶ جلسة حقيقية (Terminal)'))
P.append(SB7.d7_git())
P.append('<h3>الجلسة: نغيّر سطر ونعمل Commit تاني</h3><p class="what">غيّرنا حجم النقطة من 10 لـ 12 في المحرر وحفظنا. <code>git diff</code> بيوري السطر القديم بـ <code>-</code> والجديد بـ <code>+</code>.</p>' + res(term(_g2a), '▶ جلسة حقيقية (Terminal)'))
P.append('<h3>الجلسة: التاريخ</h3>' + res(term('$ git log\n' + _g2b), '▶ جلسة حقيقية (Terminal)') + '<p class="what">الـ ID المختصر في <code>--oneline</code> = أول 7 حروف من الـ ID الكامل. وآخر أمر بيوري الـ Commit من جوه: نص صغير فيه بصمة الفولدر (tree) والاسم والوقت والرسالة.</p>')
P.append(D1.fig(D.g_hash(), 'الـ ID بييجي كده: بصمة الملف (blob)، وبعدين بصمة الفولدر (tree)، وبعدين بصمة نص الـ Commit.'))
P.append('<h3>البرنامج 1: نحسب الـ ID بإيدنا</h3><p class="what">Git بيستخدم SHA-1: دالة بتاخد أي بايتات وتطلّع 40 حرف. نفس البايتات = نفس البصمة دايماً، وأي تغيير صغير = بصمة مختلفة خالص. حط البرنامج جنب <code>refactored.cpp</code> وشغّله.</p>'
         + prog(SRC + 'c1_commit_id.py', 'commit_id.py') + res(term(rd(SRC + 'c1_commit_id.txt')) + '<p style="font-size:10pt"><code>d088e29</code> و <code>bc0094a</code> نفس اللي في سطر <code>index</code> في <code>git diff</code>، و <code>c298df0</code> نفس الـ tree، و <code>84180e1</code> نفس الـ Commit الأول. يعني الـ ID مش عشوائي. (على Windows لو Git بيغيّر نهايات السطور، بصمة الملف هتفرق)</p>'))
P.append('<h3 id="why-git">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_git())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>عدّل ← <code>git add .</code> ← <code>git status</code> (أخضر) ← <code>git commit -m "رسالة"</code> ← <code>git log --oneline</code>.</li>
 <li>الرسالة توصف التغيير: «make points bigger: 10 -> 12 px» مش «fixed things».</li>
 <li>سطر اتغير = 1 insertion + 1 deletion.</li>
 <li>الـ ID = بصمة SHA-1 للمحتوى والاسم والوقت والرسالة.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اعمل نفس الجلسة على فولدر مشروعك. 2. غيّر لون الخطوط في <code>refactored.cpp</code> واعمل Commit برسالة كويسة. 3. شغّل <code>git log --oneline</code> وعد الـ Commits.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>الـ Pointers:</b> كل رقم بنرجعه من OpenGL (<code>&amp;vao</code> و <code>&amp;buffer</code>) بيتكتب من خلال عنوان. ونفس فكرة «عنوان بيشاور على حاجة» هي الـ VAO اللي بيشاور على الـ Buffer.</td></tr>
 <tr><td class="n">2</td><td><b>الـ Vertex Arrays:</b> كل شكل في الـ CAD هيبقى ليه VAO، ونرسمه بسطر ربط واحد.</td></tr>
 <tr><td class="n">3</td><td><b>الضرب الاتجاهي:</b> الـ Normal بتاع كل مثلث، وده أساس الإضاءة بعدين.</td></tr>
 <tr><td class="n">4</td><td><b>Git:</b> من النهارده كل خطوة شغالة في الـ CAD = Commit. لو حاجة باظت، ترجع لآخر نقطة سليمة.</td></tr>
</table>
<h3>بكره (الأحد 1-11): أول يوم في الأسبوع 3 (Classes والـ Textures)</h3>
<ul><li>برمجة: Classes الأساس (The Cherno).</li><li>رسم: Textures النظرية (learnopengl و The Cherno).</li>
<li>رياضيات: المصفوفات، المعنى (3Blue1Brown، فصل 3).</li><li>الـ CAD: B-Rep المفهوم (Wikipedia و Ekeeda).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>POINTERS in C++: <span class="ltr">youtube.com/watch?v=DTxHyVn0ODg</span></li>
 <li>Vertex Arrays in OpenGL: <span class="ltr">youtube.com/watch?v=Bcs56Mm-FJY</span> · <span class="ltr">learnopengl.com</span></li>
 <li>Cross product introduction: <span class="ltr">youtube.com/watch?v=pJzmiywagfY</span></li>
 <li>Git &amp; GitHub Tutorial #6 - Making Commits: <span class="ltr">youtube.com/watch?v=Fhgga2s_RmM</span> · <span class="ltr">git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository</span></li></ul></section>''')

css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q7.DAY7_CARDS, Q7.DAY7_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q7.DAY7_QA))
P = [Q.tag_reference(x) for x in P]
import linenums as LN
if MODE != 'web': P.append(STH.copy_appendix())
P = [jump_numbers(LN.apply(link_words(''.join(P)), ART if MODE != 'web' else ''))]
css += STH.CSS if MODE != 'web' else ''
css += LN.CSS + '''.wlink{color:#2563eb !important;text-decoration:underline;font-weight:bold}
.wline[id]{border:2px solid #f59e0b;border-radius:2mm;padding:1mm}
.jn{display:inline-block;min-width:4mm;margin:0 .8mm;padding:0 1mm;border-radius:2mm;background:#dc2626;color:#fff !important;font-size:7.5pt;line-height:1.5;text-align:center;font-family:"DejaVu Sans",sans-serif}
.jbadge{display:inline-block;margin:0 1mm 0 1mm;padding:.2mm 1.8mm;border-radius:2mm;background:#dc2626;color:#fff;font-size:8.5pt;font-weight:bold;font-family:"DejaVu Sans","CairoAr",sans-serif;direction:ltr;unicode-bidi:isolate}
.wbacks{margin:1mm 0;text-align:right}
.wback{display:inline-block;margin:0 0 1mm 2mm;padding:.6mm 2.5mm;border-radius:3mm;background:#fef3c7;border:1px solid #f59e0b;color:#92400e !important;font-size:9pt;font-weight:bold;text-decoration:none}
tr[id] td.e{background:#fffbeb;box-shadow:inset -3px 0 0 #f59e0b}
@keyframes wglow{0%,100%{box-shadow:0 0 0 0 rgba(245,158,11,0)}15%,70%{box-shadow:0 0 0 6px rgba(245,158,11,.75)}}
.wline:target,tr:target td{animation:wglow 3.5s ease-out 1}'''
if MODE == 'web':
    body = "".join(P)
    body = re.sub(r'src="(img/[^"]+\.png)"', lambda m: 'src="data:image/png;base64,' + base64.b64encode(open(m.group(1), 'rb').read()).decode() + '"', body)
    webcss = open('/home/claude/day1/web.css', encoding='utf-8').read()
    js = open('/home/claude/day1/web.js', encoding='utf-8').read()
    page = ('<title>محاضرات الأسبوع 2 · اليوم السابع</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week2_day7_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 2 - اليوم السابع</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week2_day7.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week2_day7.html', base_url='.').write_pdf('Week2_Day7_Saturday.pdf')
    import fixpdf; fixpdf.fix('Week2_Day7_Saturday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
