# Week 2 · Day 4 (Wednesday 28-10). Same structure as Days 1-3. MODE="web" builds the copy page; default builds the PDF.
import html, re, os, base64, sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day2')
sys.path.insert(0, '/home/claude/day3')
sys.path.insert(0, '/home/claude/day4')
import weasyprint
import diagrams as D1
import diag4 as D
from data4 import E, OVER
from words4 import *
import why_day4 as WHY
import sb as SB
import sb4 as SB4
import quick as Q
import quick4 as Q4

os.chdir('/home/claude/day4')
MODE = globals().get('MODE', 'pdf')
ART = os.environ.get('ART_URL', '').strip()
css = open('final.css', encoding='utf-8').read()
exec(open('hl_src.py', encoding='utf-8').read())
KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4|struct|size_t|auto|enum|static|extern|mutable|private)\b'

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
        e = over.get(t.strip(), E[t.strip()])
        if isnew: e = '<b>★ جديد:</b> ' + e
        e, _rid = JUMP.mark(e, t, label, lnum)
        h.append(f'<tr{cls}{_rid}><td class="k"><i class="ln">{lnum}</i>{hl(t)}</td><td class="e">{e}</td></tr>')
    h.append('</table>')
    return ''.join(h)

def lec(cls, tag, title, meta):
    return f'<section class="lec {cls}"><div class="lec-head"><div class="tag">{tag}</div><h2>{title}</h2><div class="meta">{meta}</div></div>'

SRC = 'src/'
import sys as _sh; _sh.path.insert(0, '/home/claude/steps'); _sh.path.insert(0, '/home/claude/steps')
import steps_hook as STH
import jumps as JUMP
STH.setup(['specs_d4'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثاني: المؤشرات والـ Shaders</div>
  <h1>اليوم الرابع — الأربعاء 28 أكتوبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> Static و Const في C++ — <span style="color:#5b6372">The Cherno (حلقة 21 و 34)</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> الـ Index Buffer (EBO): رسم مستطيل — <span style="color:#5b6372">The Cherno و learnopengl</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> الضرب الاتجاهي: تمارين — <span style="color:#5b6372">Khan Academy</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> رسم عدة خطوط (Vertex Arrays) — <span style="color:#5b6372">The Cherno و learnopengl</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:5mm;background:#fffbeb"><b>على Windows (Visual Studio):</b> برامج Static فيها ملفين: ضيف الاتنين لنفس المشروع (Add → Existing Item)، و Visual Studio هيترجمهم ويربطهم لوحده. ورسايل الـ Linker عندك بتبدأ بـ <code>LNK2005</code> و <code>LNK2001</code> بدل <code>ld</code>.</div>
</section>''')

# ================================================================== 1 · Static + Const
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'Static و Const في C++',
             'The Cherno · حلقة 21: Static · <span class="ltr">youtu.be/f3FVU-iwNuA</span> · حلقة 34: CONST · <span class="ltr">youtu.be/4fJBrditnJU</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> <code>static</code> (برا الكلاس) = «الاسم ده للملف ده بس». و <code>const</code> = «وعد إن الحاجة دي مش هتتغير»، والـ compiler بيحرس الوعد.</div>
<h3>الجزء الأول: Static (برا الكلاس)</h3>
<p class="what">The Cherno قال إن <code>static</code> ليها معنيين: <b>برا</b> الكلاس (موضوع الحلقة دي) و<b>جوه</b> الكلاس (حلقة تانية). كل ملف <code>.cpp</code> بيترجم لوحده (اسمه Translation Unit)، وبعدين الـ Linker بيربطهم.</p>''')
P.append(D1.fig(D.s_linker(), 'الـ Linker بيشوف الأسماء العادية (أزرق) بس. الأسماء الـ <code>static</code> (أحمر بقفل) مخفية عنه، فمفيش خناقة لو اتكرر الاسم.'))
P.append(LINK_TABLE)
P.append('<h3 id="static-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(STATIC_WORDS))
P.append('<h3>البرنامج 1: static بيمنع الخناقة (ملفين)</h3><p class="what">نفس الاسم <code>s_Variable</code> ونفس الدالة <code>Function</code> في الملفين. اللي في <code>static.cpp</code> عليهم <code>static</code>.</p>'
         + prog(SRC + 'st1/static.cpp', '1_static/static.cpp') + prog(SRC + 'st1/main.cpp', '1_static/main.cpp')
         + res(term(rd(SRC + 'st1.txt')) + '<p style="font-size:10pt">كل ملف شاف النسخة بتاعته: main.cpp شاف 10، و static.cpp شاف 5. وكل واحد نادى <code>Function</code> بتاعته.</p>'))
P.append(SB4.d4_static())
P.append('<h3>البرنامج 2: extern بيجيب المتغير من ملف تاني (ملفين)</h3><p class="what">هنا العكس: <code>static.cpp</code> فيه متغير عادي، و <code>main.cpp</code> بيستخدمه بـ <code>extern</code>.</p>'
         + prog(SRC + 'st2/static.cpp', '2_extern/static.cpp') + prog(SRC + 'st2/main.cpp', '2_extern/main.cpp')
         + res(term(rd(SRC + 'st2.txt')) + '<p style="font-size:10pt">طبع 5: القيمة اللي في <code>static.cpp</code>.</p>'))
P.append('<div class="ok"><b>نصيحة The Cherno:</b> خلّي أي متغير أو دالة عامة <code>static</code>، إلا لو محتاج ملف تاني يشوفها. ده بيمنع خناقات الأسماء. (وإنت شفت <code>static</code> قبل كده على <code>CompileShader</code> و <code>ParseShader</code>!)</div>')
P.append('<h3>الجزء التاني: Const</h3><p class="what">زي <code>private</code>: مابيغيّرش الكود اللي بيشتغل، بس بيفرض قواعد على اللي بيكتب. و The Cherno قال إن الوعد ممكن يتكسر بحيل، بس ماتعملش كده.</p>')
P.append(D1.fig(D.c_const4(), 'الأربع حالات. القفل على الـ Pointer = مايتحركش. القفل على الرقم = مايتغيرش من خلاله.'))
P.append(CONST_TABLE)
P.append('<h3 id="const-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CONST_WORDS))
P.append('<h3>البرنامج 3: const مع المتغيرات والـ Pointers</h3><p class="what">البرنامج بيعمل الحاجات <b>المسموحة</b> بس في كل حالة. الحاجات الممنوعة جربناها في قسم «ليه» وطلّعت أخطاء.</p>'
         + prog(SRC + 'c1_const_pointers.cpp', 'const_pointers.cpp') + res(term(rd(SRC + 'c1_const_pointers.txt'))))
P.append('<h3>البرنامج 4: const مع الدوال، و mutable</h3><p class="what">مثال The Cherno: <code>GetX</code> وعدت إنها مش هتغيّر حاجة، عشان كده ينفع تتنادي من <code>PrintEntity</code> اللي واخدة <code>const Entity&amp;</code>. و <code>mutable</code> بيسمح بعدّاد للـ debugging.</p>'
         + prog(SRC + 'c2_const_method.cpp', 'const_method.cpp') + res(term(rd(SRC + 'c2_const_method.txt')) + '<p style="font-size:10pt">العدّاد زاد مرتين جوه دالة <code>const</code>، بفضل <code>mutable</code>.</p>'))
P.append('<h3 id="why-prog">ليه كتبنا كل ده؟ الهدف من كل خطوة</h3><p class="what">لكل خطوة: <b>ليه</b>، وهي <b>إجبارية ولا لأ</b>، و<b>إيه اللي يحصل لو شيلتها</b> (جربناها فعلاً).</p>'
         + LEGEND + '<div class="warn" style="font-size:10pt"><b>⚠️ لاحظ:</b> أخطاء الـ <code>static</code> مش بتطلع من الـ compiler، بتطلع من الـ <b>Linker</b> في الآخر. كل ملف لوحده سليم، والمشكلة بتظهر لما يتلزقوا.</div>'
         + '<h3>Static</h3>' + WHY.build_static() + '<h3>Const</h3>' + WHY.build_const())
P.append('''<div class="sum"><b>الملخص:</b><ul><li><code>static</code> برا الكلاس = للملف ده بس، و <code>extern</code> = من ملف تاني.</li>
 <li>اسمين عامين زي بعض = خطأ Linker. و <code>static</code> في header = نسخة لكل ملف.</li>
 <li><code>const</code> قبل النجمة = المحتوى، بعدها = الـ Pointer، وبعد الدالة = مش هتغيّر الكلاس.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b><br>1. في البرنامج 2 خلّي <code>static.cpp</code> فيه دالة <code>int GetValue()</code> عادية، ونادِيها من <code>main.cpp</code> بسطر تعريف بس.<br>
2. ضيف لـ Entity دالة <code>int GetY() const</code>، وجرّب تكتب جواها <code>m_X = 5;</code>. إيه الخطأ؟</div></section>''')

# ================================================================== 2 · EBO
e1 = {l.strip() for l in open(SRC + 'e1_rect_arrays.cpp') if l.strip()}
e2new = {l.strip() for l in open(SRC + 'e2_rect_indices.cpp') if l.strip()} - e1
P.append(lec('l2', 'المحاضرة 2 · رسم', 'الـ Index Buffer (EBO): رسم مستطيل', 'قناة The Cherno · Index Buffers in OpenGL · <span class="ltr">youtu.be/MXNMC1YAxVQ</span> · learnopengl.com/Getting-started/Hello-Triangle'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> كارت الشاشة بيرسم مثلثات بس، فالمستطيل = مثلثين. بدل ما تكتب الركن المشترك مرتين، اكتب كل ركن مرة، وقول بالأرقام مين بيعمل كل مثلث.</div>
<p class="note">learnopengl بيسمّيه <b>EBO</b> (Element Buffer Object)، و The Cherno بيسمّيه <b>IBO</b> (Index Buffer Object). نفس الحاجة.</p>''')
P.append(D1.fig(D.e_dup(), 'شمال: 6 أركان، منهم 2 مكررين (أحمر). يمين: 4 أركان بس، وأرقام بتقول الترتيب.'))
P.append(D1.fig(D.e_indices(), 'الأرقام 0 و 1 و 2 = المثلث الأزرق، و 2 و 3 و 0 = المثلث الأخضر.'))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم. الـ Shader هنا نفس Shader الخطوط امبارح (لون من <code>u_Color</code>).</div>')
P.append('<h3 id="ebo-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(EBO_WORDS))
P.append('<h3>البرنامج 1: مستطيل من غير Index Buffer (6 أركان)</h3><p class="what">الطريقة الأولى في الحلقة: مثلثين، كل واحد 3 أركان، والركنين المشتركين مكتوبين مرتين.</p>'
         + prog(SRC + 'e1_rect_arrays.cpp', 'rect_arrays.cpp') + res(bigimg('e1_rect_arrays', 'مستطيل أزرق'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append('<h3>البرنامج 2: نفس المستطيل بالـ Index Buffer (4 أركان)</h3><p class="what">السطور <b>بالأصفر</b> هي اللي اتغيرت: 4 أركان بدل 6، ومصفوفة <code>indices</code>، و buffer تاني، و <code>glDrawElements</code>.</p>'
         + prog(SRC + 'e2_rect_indices.cpp', 'rect_indices.cpp', new=e2new) + res(bigimg('e2_rect_indices', 'نفس المستطيل بالظبط'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(SB4.d4_ebo())
P.append('''<table class="types"><tr><th>نوع الـ index</th><th>الحجم</th><th>أكبر رقم</th><th>في glDrawElements</th></tr>
<tr><td><code>unsigned char</code></td><td>1 بايت</td><td>255</td><td><code>GL_UNSIGNED_BYTE</code></td></tr>
<tr><td><code>unsigned short</code></td><td>2 بايت</td><td>65,535</td><td><code>GL_UNSIGNED_SHORT</code></td></tr>
<tr><td><code>unsigned int</code></td><td>4 بايت</td><td>أكتر من 4 مليار</td><td><code>GL_UNSIGNED_INT</code></td></tr></table>''')
P.append('<h3 id="why-ebo">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_ebo())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Index Buffer = أرقام الأركان بالترتيب، 3 لكل مثلث.</li>
 <li><code>GL_ELEMENT_ARRAY_BUFFER</code> + <code>glDrawElements(mode, عدد الـ indices, GL_UNSIGNED_INT, nullptr)</code>.</li>
 <li>لازم unsigned، والـ VAO بيفتكر الـ IBO، فماتفكّوش وهو شغال.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> ارسم شكل سداسي (6 أركان + ركن في النص = 7) بـ 6 مثلثات: كام index هتحتاج؟ (الإجابة: 18)</div></section>''')

# ================================================================== 3 · Cross (Khan)
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'الضرب الاتجاهي: تمارين', 'Khan Academy · Cross product introduction · <span class="ltr">youtu.be/pJzmiywagfY</span> · تمارين: khanacademy.org/math/linear-algebra'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> نفس الضرب الاتجاهي بتاع امبارح، بس بطريقة حساب Khan Academy: لكل صف، غطي رقمه واضرب الباقي على الصليب. والصف الأوسط معكوس.</div>
<table class="types"><tr><th></th><th>Dot product</th><th>Cross product</th></tr>
<tr><td>موجود في</td><td>أي عدد أبعاد</td><td><b>3D بس</b></td></tr><tr><td>الناتج</td><td>رقم</td><td><b>متجه</b></td></tr><tr><td>الرمز</td><td>a · b</td><td>a × b</td></tr></table>
<div class="formula">a × b = [ a<sub>2</sub>b<sub>3</sub> − a<sub>3</sub>b<sub>2</sub> ,  a<sub>3</sub>b<sub>1</sub> − a<sub>1</sub>b<sub>3</sub> ,  a<sub>1</sub>b<sub>2</sub> − a<sub>2</sub>b<sub>1</sub> ]</div>''')
P.append(D1.fig(D.x_khan(), 'مثال الفيديو خطوة خطوة: كل صف بنغطي رقمه (الخط الرمادي)، والصف الأوسط بس اللي بيتعكس.'))
P.append('''<div class="ok"><b>الخاصية المهمة:</b> (a × b) · a = 0 و (a × b) · b = 0. يعني الناتج <b>عمودي</b> (orthogonal) على الاتنين. واتجاهه بقاعدة الإيد اليمين: السبابة a، والوسطى b، والإبهام a × b.</div>
<p class="note"><b>Orthogonal مقابل Perpendicular:</b> الاتنين معناهم متعامدين، بس orthogonal بتشمل متجه الصفر كمان (لأن صفر · أي حاجة = 0).</p>''')
P.append('<h3>الكود: مثال الفيديو + 4 تمارين</h3><p class="what">نفس دالة <code>cross</code> بتاعة امبارح، ودالة <code>check</code> بتطبع الناتج وتتأكد إنه عمودي. حل التمارين بإيدك الأول، وبعدين قارن.</p>'
         + prog(SRC + 'x1_cross_khan.cpp', 'cross_khan.cpp') + res(term(rd(SRC + 'x1_cross_khan.txt')) + '<p style="font-size:10pt">مثال الفيديو طلع [‎-30, 1, 37] بالظبط. وكل الضرب النقطي أصفار. ولاحظ x × y = z بس y × x = ‎-z.</p>'))
P.append('<h3 id="why-cross">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_cross())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>3D بس، والناتج متجه عمودي على الاتنين.</li><li>غطي رقم الصف واضرب على الصليب، والأوسط معكوس.</li><li>اتأكد بالضرب النقطي = 0.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> احسب بإيدك [1, 2, 3] × [4, 5, 6] (الإجابة: [‎-3, 6, ‎-3])، وبعدين حل تمارين Khan Academy في الصفحة اللي في الخطة.</div></section>''')

# ================================================================== 4 · VAO + multiple lines
v1 = {l.strip() for l in open(SRC + 'v1_two_vaos.cpp') if l.strip()}
P.append(lec('l4', 'المحاضرة 4 · CAD', 'رسم عدة خطوط (Vertex Arrays)', 'قناة The Cherno · Vertex Arrays in OpenGL · <span class="ltr">youtu.be/Bcs56Mm-FJY</span> · learnopengl.com/Getting-started/Hello-Triangle'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ VAO (Vertex Array Object) = «دفتر» بيفتكر الـ buffer وإعداداته. لما يبقى عندك كذا شكل، كل شكل ليه دفتر، وقبل ما ترسمه تفتح دفتره بسطر واحد.</div>
<table class="types"><tr><th></th><th>من غير VAO (Compatibility)</th><th>مع VAO</th></tr>
<tr><td>قبل كل رسمة</td><td>bind الـ buffer + <code>glVertexAttribPointer</code> تاني</td><td><code>glBindVertexArray</code> بس</td></tr>
<tr><td>في الـ Core Profile</td><td>مش هيشتغل (1282)</td><td>لازم</td></tr></table>
<p class="note">The Cherno سأل: VAO واحد لكل حاجة ولا VAO لكل شكل؟ وقال: «حسب الحالة، اعمل benchmark». ووثائق OpenGL بتنصح بـ VAO لكل شكل، وده اللي هنعمله.</p>''')
P.append(D1.fig(D.v_vao(), 'كل شكل ليه VAO فاكر الـ buffer بتاعه. في اللوب: bind ثم رسم، لكل شكل.'))
P.append(MODES_TABLE)
P.append('<h3 id="vao-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(VAO_WORDS))
P.append('<h3>البرنامج 3: شكلين، كل واحد ليه VAO</h3><p class="what">بيت (6 خطوط) وشمس (خطين)، كل واحد في buffer لوحده و VAO لوحده. وفي اللوب بنبدّل بينهم.</p>'
         + prog(SRC + 'v1_two_vaos.cpp', 'two_vaos.cpp') + res(bigimg('v1_two_vaos', 'البيت أبيض والشمس صفرا: شكلين من VAOين'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(SB4.d4_vao())
v2new = {l.strip() for l in open(SRC + 'v2_polylines.cpp') if l.strip()} - v1 - {l.strip() for l in open('/home/claude/day3/src/l2_click_lines.cpp') if l.strip()}
P.append('<h3>البرنامج 4 (للـ CAD): خطوط متصلة بالماوس (Polylines)</h3><p class="what">زي أداة Polyline في AutoCAD: الزرار الشمال يضيف نقطة للخط الحالي، واليمين يخلّصه ويبدأ خط جديد. كل الخطوط في buffer واحد، ولكل خط بداية وعدد. السطور <b>بالأصفر</b> جديدة عن برنامج الماوس بتاع امبارح.</p>'
         + prog(SRC + 'v2_polylines.cpp', 'polylines.cpp', new=v2new)
         + res(term(rd(SRC + 'v2_polylines.txt'))
               + grid([shot('v2_4', '4 دوسات شمال'), shot('v2_5', 'يمين: خلص'), shot('v2_8', '3 دوسات: خط تاني'), shot('v2_10', 'يمين، ونقطة جديدة')], 4)
               + '<p style="font-size:10pt">دوسنا بالماوس فعلاً (شمال ويمين)، ودي لقطات الشباك.</p>', '▶ النتيجة لما نعمل Run (دوسات حقيقية بالماوس)'))
P.append(SB4.d4_poly())
P.append('<h3 id="why-vao">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_vao())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>VAO = دفتر بيفتكر الـ buffer والـ layout. واحد لكل شكل.</li>
 <li>في الـ Core Profile لازم، وفي الـ Compatibility فيه VAO 0 افتراضي.</li><li>OpenGL بيرسم بآخر حاجة اتعملها bind.</li>
 <li><code>GL_LINE_STRIP</code> + (بداية، عدد) لكل خط = عدة خطوط في buffer واحد.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> في البرنامج 4 خلّي زرار <b>Backspace</b> يمسح آخر نقطة (<code>points.pop_back()</code> مرتين، و <code>count--</code>). ده تمرين بكره «مسح آخر خط».</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>Static و Const:</b> <code>static</code> اللي على <code>CompileShader</code> من أول يوم معناها «للملف ده بس». و <code>const std::string&amp;</code> في <code>ParseShader</code> = Reference امبارح + Const النهارده.</td></tr>
 <tr><td class="n">2</td><td><b>Index Buffer:</b> كل الأشكال المعقدة (مكعبات، موديلات) بتترسم كده، وهتحتاجه في الـ CAD لما ترسم مستطيلات ومضلعات.</td></tr>
 <tr><td class="n">3</td><td><b>الضرب الاتجاهي:</b> هيديك الاتجاه العمودي على أي سطح (normal)، وده أساس الإضاءة بعدين.</td></tr>
 <tr><td class="n">4</td><td><b>الـ VAO والخطوط:</b> برنامج الـ Polylines ده بداية أداة رسم حقيقية في الـ CAD.</td></tr>
</table>
<h3>بكره (الخميس 29-10)</h3>
<ul><li>برمجة: تمرين swap بالـ Pointers.</li><li>رسم: تعديل الـ Shader (Writing a Shader in OpenGL).</li>
<li>رياضيات: dot و cross في Python و NumPy.</li><li>الـ CAD: مسح آخر خط (<code>push_back</code> و <code>pop_back</code>).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>Static: <span class="ltr">youtube.com/watch?v=f3FVU-iwNuA</span> · CONST: <span class="ltr">youtube.com/watch?v=4fJBrditnJU</span></li>
 <li>Index Buffers: <span class="ltr">youtube.com/watch?v=MXNMC1YAxVQ</span> · <span class="ltr">learnopengl.com/Getting-started/Hello-Triangle</span></li>
 <li>Cross product introduction: <span class="ltr">youtube.com/watch?v=pJzmiywagfY</span></li>
 <li>Vertex Arrays: <span class="ltr">youtube.com/watch?v=Bcs56Mm-FJY</span></li></ul></section>''')

css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q4.DAY4_CARDS, Q4.DAY4_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q4.DAY4_QA))
P = [Q.tag_reference(x) for x in P]
import linenums as LN
if MODE != 'web': P.append(STH.copy_appendix())
import jumps as JUMP
P = [JUMP.apply(''.join(P), LN, ART if MODE != 'web' else '')]
css += STH.CSS if MODE != 'web' else ''
css += LN.CSS + JUMP.CSS
if MODE == 'web':
    body = "".join(P)
    body = re.sub(r'src="(img/[^"]+\.png)"', lambda m: 'src="data:image/png;base64,' + base64.b64encode(open(m.group(1), 'rb').read()).decode() + '"', body)
    webcss = open('/home/claude/day1/web.css', encoding='utf-8').read()
    js = open('/home/claude/day1/web.js', encoding='utf-8').read()
    page = ('<title>محاضرات الأسبوع 2 · اليوم الرابع</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week2_day4_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 2 - اليوم الرابع</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week2_day4.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week2_day4.html', base_url='.').write_pdf('Week2_Day4_Wednesday.pdf')
    import fixpdf; fixpdf.fix('Week2_Day4_Wednesday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
