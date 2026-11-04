# Week 2 · Day 2 (Monday 26-10): same structure as Day 1. MODE='web' builds the copy page; default builds the PDF.
import html, re, os, base64, sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day2')
import weasyprint
import diagrams as D1
import diag2 as D
from data2 import E
from words2 import C_WORDS, VA_WORDS, VEC_WORDS
from words import TYPES_TABLE
import why_day2 as WHY
import sb as SB

os.chdir('/home/claude/day2')
MODE = globals().get('MODE', 'pdf')
ART = os.environ.get('ART_URL', '').strip()
css = open('final.css', encoding='utf-8').read()
exec(open('hl_src.py', encoding='utf-8').read())
KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4|struct|size_t|auto)\b'

def rd(p): return open(p).read()
def term(t): return '<div class="run"><div class="bar">● ● ●  &nbsp;Terminal — output after Run</div>' + html.escape(t.rstrip('\n')) + '</div>'
def res(body, title='▶ النتيجة لما نعمل Run'): return f'<div class="result"><div class="rh">{title}</div>{body}</div>'
def shot(img, cap): return f'<td><img src="img/{img}.png"><div class="cap">{cap}</div></td>'
def grid(cells, cols):
    rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
    return '<table class="shots">' + ''.join('<tr>' + ''.join(r) + '</tr>' for r in rows) + '</table>'
def bigimg(name, cap, w='80mm'):
    return f'<img src="img/{name}.png" style="width:{w};display:block;margin:2mm auto;border-radius:2mm"><div style="text-align:center;font-size:9.5pt;color:#5b6372;margin-bottom:2mm">{cap}</div>'
LEGEND = ('<div class="legend"><span class="badge b-req">إجباري</span> = من غيره مش هيشتغل · <span class="badge b-imp">مش إجباري، بس مهم جداً</span> = هيشتغل، بس هتتعب · '
          '<span class="badge b-opt">اختياري</span> = تحسين أو مثال</div>')

def prog(path, label, new=None):
    STH.seen(path)
    aid = re.sub(r'[^A-Za-z0-9_-]', '-', label)
    raw = open(path).read().rstrip('\n') + '\n'
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
        e = E[t.strip()]
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
STH.setup(['specs_d2'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثاني: المؤشرات والـ Shaders</div>
  <h1>اليوم التاني — الإثنين 26 أكتوبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> مقدمة لغة C (الجزء 1) + تمارين Pointers — <span style="color:#5b6372">Exercism</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> Vertex Attributes و Layouts — <span style="color:#5b6372">The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> الضرب النقطي وطول المتجه — <span style="color:#5b6372">Khan Academy</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> تخزين النقط في std::vector — <span style="color:#5b6372">The Cherno</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:5mm;background:#fffbeb"><b>على Windows (Visual Studio):</b> العناوين بتتطبع من غير <code>0x</code>، وأرقامها بتتغير كل مرة. وفي برنامج نمو الـ vector الأرقام هتختلف (Visual Studio بيكبّر ×1.5 مش ×2). الفكرة هي هي.</div>
</section>''')

# ================================================================== 1 · C
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'مقدمة لغة C (الجزء 1) + تمارين Pointers',
             'قناة Exercism · A Brief Introduction to C · من البداية لحد 7:26 · <span class="ltr">youtu.be/SVthw_d9nwE</span> · التمارين: <span class="ltr">exercism.org/tracks/cpp</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> C هي «الجدة» اللي C++ اتولدت منها: لغة صغيرة وسريعة، وإنت اللي بتمسك الذاكرة بإيدك. وكل اللي اتعلمته في الـ Pointers جاي منها.</div>
<p class="note" style="margin:0 0 3mm">الخطة بتقول الجزء الأول بس (تاريخ C ومميزاتها، لحد 7:26). جزء حل تمرين Hamming (من 7:26) يوم الثلاثاء.</p>''')
P.append(D1.fig(D.c_family(), 'C اتعملت سنة 1972 في Bell Labs عشان يكتبوا بيها Unix. ولغات كتير اتبنت على شكلها، منهم C++ اللي إنت بتتعلمها.'))
P.append('''<h3>اللي الفيديو قاله عن C، باختصار</h3>
<table class="types"><tr><th>الميزة</th><th>معناها</th><th>هتشوفها في</th></tr>
<tr><td>لغة صغيرة</td><td>كلمات قليلة، فتتعلمها بسرعة</td><td>كل البرامج تحت قصيرة</td></tr>
<tr><td>سريعة وقريبة من الجهاز</td><td>بتتحول لأوامر المعالج مباشرة</td><td>برنامج 3: <code>p++</code></td></tr>
<tr><td>إدارة الذاكرة يدوي</td><td>إنت اللي بتحجز وإنت اللي بترجّع، ومفيش حد بينضّف وراك</td><td>برنامج 2: <code>malloc</code> و <code>free</code></td></tr>
<tr><td>بتشتغل على أي جهاز</td><td>تقريباً كل جهاز في الدنيا ليه compiler لـ C</td><td>—</td></tr></table>
<h3>C مقابل C++ في حاجات هتقابلها</h3>
<table class="types"><tr><th>الحاجة</th><th>في C</th><th>في C++</th></tr>
<tr><td>الطباعة</td><td><code>printf</code> من <code>stdio.h</code></td><td><code>std::cout</code> من <code>iostream</code></td></tr>
<tr><td>حجز ذاكرة</td><td><code>malloc</code> و <code>free</code></td><td><code>new</code> و <code>delete</code></td></tr>
<tr><td>Pointer فاضي</td><td><code>NULL</code></td><td><code>nullptr</code></td></tr>
<tr><td>امتداد الملف</td><td><code>.c</code></td><td><code>.cpp</code></td></tr></table>
<div class="setup"><b>إزاي تشغّل برنامج C في Visual Studio:</b> اعمل مشروع C++ عادي (Console App)، وسمّي الملف بامتداد <code>.c</code> بدل <code>.cpp</code>. Visual Studio بيترجم أي ملف <code>.c</code> كلغة C لوحده.</div>''')
P.append('<h3 id="c-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(C_WORDS))
P.append('<h3>برنامج 1: أول برنامج C</h3><p class="what">نفس فكرة Hello World، بس بلغة C و <code>printf</code>.</p>'
         + prog(SRC + 'c1_hello.c', 'hello.c') + res(term(rd(SRC + 'c1_hello.txt')) + '<p style="font-size:10pt">مكان <code>%d</code> اتحط 1972.</p>'))
P.append('<h3>برنامج 2: الذاكرة بإيدك (malloc و free)</h3><p class="what">ده اللي الفيديو سماه Manual Memory Management: بنحجز مكان لـ 5 أرقام على الـ Heap ونرجّعه في الآخر.</p>'
         + D1.fig(D1.p_heap(), 'نفس رسمة امبارح: <code>malloc</code> بتحجز في الـ Heap زي <code>new</code> بالظبط، والـ Pointer هو الحبل اللي بيوصّلك له.')
         + prog(SRC + 'c2_malloc.c', 'malloc.c') + res(term(rd(SRC + 'c2_malloc.txt'))))
P.append(SB.d2_malloc())
P.append('<h3>برنامج 3: حساب الـ Pointers (p++)</h3><p class="what">من مميزات C في الفيديو. بنمشي على مصفوفة بزق الـ Pointer خطوة خطوة.</p>'
         + D1.fig(D.c_arith(), 'كل <code>p++</code> بيحرّك العنوان 4 بايت (حجم الـ int)، فبيوصل للرقم اللي بعده على طول.')
         + prog(SRC + 'c3_ptr_arith.c', 'pointer_arithmetic.c')
         + res(term(rd(SRC + 'c3_ptr_arith.txt')) + '<p style="font-size:10pt">بص على آخر رقمين في العنوان: e40 ثم e44 ثم e48 ثم e4c. كل خطوة +4 بالظبط.</p>'))
P.append(SB.d2_arith())
P.append('<h3>برنامج 4 (تمرين Pointers): دالة بتغيّر متغير مش بتاعها</h3><p class="what">ده أهم استخدام للـ Pointers في الحياة العملية، وده اللي هتقابله في تمارين Exercism.</p>'
         + D1.fig(D.c_byvalue(), 'شمال: الدالة خدت نسخة، فالأصل ما اتغيرش. يمين: الدالة خدت العنوان، فراحت غيّرت الأصل.')
         + prog(SRC + 'c4_double_it.cpp', 'double_it.cpp') + res(term(rd(SRC + 'c4_double_it.txt'))))
P.append(SB.d2_double())
P.append('<h3 id="why-c">ليه كتبنا كل ده؟ الهدف من كل خطوة</h3><p class="what">زي امبارح: لكل خطوة <b>ليه</b>، وهي <b>إجبارية ولا لأ</b>، و<b>إيه اللي يحصل لو شيلتها</b> (جربناها فعلاً). ولغلطات الذاكرة استخدمنا أداة AddressSanitizer.</p>'
         + LEGEND + '<div class="warn" style="font-size:10pt"><b>⚠️ لاحظ:</b> C أكثر تساهلاً من C++. حاجات كتير الـ C++ بترفضها، C بتطلّع عليها تحذير بس وتكمّل. اقرا التحذيرات دايماً.</div>' + WHY.build_c())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>C = لغة 1972، صغيرة وسريعة، و C++ مبنية عليها.</li>
 <li><code>printf</code> بعلامات <code>%d</code> و <code>%p</code>، و <code>malloc</code> بالبايت و <code>free</code> إجباري.</li>
 <li><code>p++</code> بيروح للعنصر اللي بعده (مش البايت).</li><li>عشان دالة تغيّر متغيرك: ابعتلها عنوانه.</li></ul></div>
<div class="try"><b>تمارين (Pointers):</b><br>1. اكتب دالة <code>void swap(int* a, int* b)</code> تبدّل قيمتين. (هتحلها بالتفصيل يوم الخميس)<br>
2. في برنامج 3، خلّي اللوب يطبع المصفوفة بالعكس: ابدأ بـ <code>p = arr + 3</code> واستخدم <code>p--</code>.<br>
3. على exercism.org/tracks/cpp حل أول تمرينين في الـ track.</div></section>''')

# ================================================================== 2 · Vertex Attributes
va1 = {l.strip() for l in open(SRC + 'va1_positions.cpp') if l.strip()}
va2new = {l.strip() for l in open(SRC + 'va2_colors.cpp') if l.strip()} - va1
P.append(lec('l2', 'المحاضرة 2 · رسم', 'Vertex Attributes و Layouts في OpenGL', 'قناة The Cherno · سلسلة OpenGL · <span class="ltr">youtu.be/x0H--CL2tUI</span> · مرجع: learnopengl.com/Getting-started/Shaders'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> كارت الشاشة شايف الـ buffer مجرد bytes ورا بعض. <code>glVertexAttribPointer</code> هي اللي بتقوله: «كل ركن طوله كذا، وجواه مكان من هنا لهنا، ولون من هنا لهنا».</div>
<table class="grid2"><tr><td><b>غلطة شائعة</b><br>إن الـ Vertex = المكان بس.</td><td><b>الصح</b><br>الـ Vertex = ركن، وجواه حاجات كتير: مكان، لون، إحداثيات صورة… كل واحدة اسمها Attribute.</td></tr></table>''')
P.append(D1.fig(D.va_layout(), 'الـ buffer في البرنامج 2: كل ركن 5 أرقام. <b>stride</b> = تنط قد إيه للركن اللي بعده (20 بايت). <b>offset</b> = اللون بيبدأ فين جوه الركن (بعد 8 بايت).'))
P.append(D1.fig(D.va_slots(), 'كل مدخل في الـ C++ ليه رقم، ولازم يقابله نفس الرقم في الـ Shader (<code>layout(location = …)</code>).'))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> GLFW و GLAD متركبين زي الأسبوع الأول، و <code>glad.c</code> مضاف للمشروع. والشكل العام للبرنامج (الشباك، الـ Shader، اللوب) هو هو برنامج امبارح، وشرح «ليه» كل خطوة فيه موجود في ملف امبارح (قسم الـ Uniforms). هنا بنركز على الجديد.</div>')
P.append('<h3 id="va-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(VA_WORDS))
P.append('<h3>البرنامج 1: مثلث بالأماكن بس</h3><p class="what">زي حلقة The Cherno: كل ركن رقمين (x, y)، ومدخل واحد بس.</p>'
         + prog(SRC + 'va1_positions.cpp', 'triangle_positions.cpp')
         + res(bigimg('va1_positions', 'مثلث برتقاني: اللون ثابت في الـ Shader، والأماكن جاية من الـ buffer'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append('<h3>البرنامج 2: كل ركن ليه لون (مدخلين)</h3><p class="what">نفس البرنامج 1، والسطور المتعلّمة <b>بالأصفر</b> هي اللي اتغيرت: ضفنا لون لكل ركن، ومدخل تاني، وغيّرنا الـ stride.</p>'
         + prog(SRC + 'va2_colors.cpp', 'triangle_colors.cpp', new=va2new)
         + res(bigimg('va2_colors', 'الركن الأحمر تحت شمال، والأخضر فوق، والأزرق تحت يمين، وكل اللي في النص خليط منهم')
               + '<p style="font-size:10pt"><b>ليه طلع تدرّج؟</b> إحنا ادينا لون لـ 3 أركان بس، بس كارت الشاشة بيلوّن كل بكسل جوه المثلث. فبيحسب لكل بكسل خليط من ألوان الأركان حسب قربه من كل ركن. ده اسمه interpolation.</p>',
               '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(SB.d2_va())
P.append('<h3 id="why-va">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت في رقم؟</h3><p class="what">كل تجربة هنا غيّرنا فيها رقم واحد بس في البرنامج 2، وشغّلناه وصوّرنا الشباك.</p>'
         + LEGEND + '<div class="warn" style="font-size:10pt"><b>⚠️ لاحظ:</b> ولا غلطة من دول طلّعت رسالة خطأ (ماعدا واحدة). كلهم اشتغلوا وطلّعوا رسمة غلط أو مفيش رسمة. عشان كده لازم تفهم كل رقم في <code>glVertexAttribPointer</code>.</div>'
         + WHY.build_va())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ Vertex = ركن بكل بياناته، مش المكان بس.</li>
 <li>لكل Attribute: <code>glEnableVertexAttribArray</code> + <code>glVertexAttribPointer</code>.</li>
 <li>الـ size = عدد الأرقام، والـ stride = طول الركن كله بالبايت، والـ offset = بداية المدخل جوه الركن.</li>
 <li>رقم المدخل لازم يطابق <code>layout(location)</code>، واسم <code>out</code> لازم يطابق اسم <code>in</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> في البرنامج 2 خلّي الركن الفوقاني أبيض (1, 1, 1). وبعدين زوّد لكل ركن رقم شفافية (يبقى 6 أرقام): غيّر الـ stride، والـ size بتاع اللون لـ 4، و <code>vec3</code> لـ <code>vec4</code>.</div></section>''')

# ================================================================== 3 · Math
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'الضرب النقطي وطول المتجه', 'Khan Academy · Vectors and Spaces · <span class="ltr">youtu.be/WNuIhXo39_k</span> · تمارين: khanacademy.org/math/linear-algebra'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الضرب النقطي = اضرب المتقابلين واجمع (النتيجة رقم). والطول = جذر الضرب النقطي في نفسه.</div>
<h3>مراجعة: العمليتين اللي فاتوا</h3>
<div class="formula">a + b = [a<sub>1</sub>+b<sub>1</sub>, a<sub>2</sub>+b<sub>2</sub>, …]   ← متجه</div>
<div class="formula">c · a = [c·a<sub>1</sub>, c·a<sub>2</sub>, …]   ← متجه</div>
<h3>الضرب النقطي ← رقم واحد</h3>
<div class="formula">a · b = a<sub>1</sub>b<sub>1</sub> + a<sub>2</sub>b<sub>2</sub> + … + a<sub>n</sub>b<sub>n</sub></div>
<div class="formula">[2, 5] · [7, 1] = 14 + 5 = <b>19</b></div>
<div class="formula">[1, 2, 3] · [−2, 0, 5] = −2 + 0 + 15 = <b>13</b></div>
<h3>طول المتجه</h3>
<div class="formula">‖a‖ = √(a<sub>1</sub>² + a<sub>2</sub>² + … + a<sub>n</sub>²)</div>
<p>ليه نعرّفه بالشكل ده؟ لأن المتجه ممكن يبقى فيه 50 رقم ومش هتقدر ترسمه. بس في 2D الطريقة دي هي فيثاغورس بالظبط:</p>''')
P.append(D1.fig(D.m_pyth(), 'المتجه [2, 5] وتر في مثلث قائم ضلعيه 2 و 5، فطوله √29. ولاحظ إن 29 هو نفسه [2,5]·[2,5].'))
P.append('<div class="ok"><b>العلاقة المهمة:</b> ‖a‖² = a · a ، يعني الطول = √(a · a). وده اللي هنكتبه في الكود حرفياً.</div>')
P.append('<h3>الكود: الضرب النقطي والطول</h3><p class="what">برنامج كامل يحسب أمثلة الفيديو.</p>'
         + prog(SRC + 'd1_dot_length.cpp', 'dot_length.cpp')
         + res(term(rd(SRC + 'd1_dot_length.txt')) + '<p style="font-size:10pt">نفس أرقام الفيديو: 19 و 13. و [2,5]·[2,5] = 29، وجذره = الطول بالظبط.</p>'))
P.append(SB.d2_length())
P.append('<h3 id="why-math">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_math())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>جمع وضرب في رقم ← متجه. الضرب النقطي ← رقم.</li><li>‖a‖ = √(a · a)، وفي 2D ده فيثاغورس.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> احسب بإيدك طول [3, 4] (لازم يطلع رقم صحيح!)، وبعدين ضيفه للبرنامج وتأكد. وحل تمارين Khan Academy في الصفحة اللي في الخطة.</div></section>''')

# ================================================================== 4 · vector
P.append(lec('l4', 'المحاضرة 4 · CAD', 'تخزين النقط في std::vector', 'قناة The Cherno · Dynamic Arrays in C++ · <span class="ltr">youtu.be/PocJ5jXv8No</span> · مرجع: en.cppreference.com/w/cpp/container/vector'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> <code>std::vector</code> = قايمة بتكبر لوحدها. في الـ CAD هي اللي هتشيل كل النقط والخطوط اللي المستخدم بيرسمها.</div>
<table class="types"><tr><th></th><th>مصفوفة عادية</th><th>std::vector</th></tr>
<tr><td>الحجم</td><td>ثابت</td><td>بيكبر لما تضيف</td></tr>
<tr><td>لازم تعرف الحجم من الأول؟</td><td>أيوه</td><td>لأ</td></tr>
<tr><td>عارف حجمه؟</td><td>لأ</td><td>أيوه: <code>.size()</code></td></tr>
<tr><td>رجوع الذاكرة</td><td>بإيدك (لو <code>new</code>)</td><td>لوحده</td></tr></table>''')
P.append('<h3 id="vec-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(VEC_WORDS))
P.append('<h3>برنامج 1: إنشاء وإضافة وقراية</h3>' + prog(SRC + 'v1_basics.cpp', 'vector_basics.cpp') + res(term(rd(SRC + 'v1_basics.txt'))))
P.append('<h3>برنامج 2: اللف على العناصر</h3><p class="what">طريقتين للف، وإزاي تعدّل وإنت بتلف.</p>' + prog(SRC + 'v2_loops.cpp', 'vector_loops.cpp') + res(term(rd(SRC + 'v2_loops.txt'))))
P.append('<h3>برنامج 3: كود The Cherno كامل (طباعة، مسح عنصر، مسح الكل)</h3>' + prog(SRC + 'v3_full.cpp', 'vector_full.cpp') + res(term(rd(SRC + 'v3_full.txt'))))
P.append(SB.d2_erase())
P.append('<h3>برنامج 4 (للـ CAD): قايمة نقط ودوال بتتعامل معاها</h3><p class="what">ده بالظبط اللي هتحتاجه في الـ CAD: كل ما المستخدم يدوس، نضيف نقطة. والدوال بتاخد القايمة بـ <code>&amp;</code> أو <code>const&amp;</code>.</p>'
         + prog(SRC + 'v4_cad_points.cpp', 'cad_points.cpp') + res(term(rd(SRC + 'v4_cad_points.txt'))))
P.append('<h3>برنامج 5: إزاي الـ vector بيكبر من جوه</h3><p class="what">الفيديو قال: لما المكان يخلص، بيحجز مكان أكبر وينقل كل حاجة. البرنامج ده بيوريك ده بيحصل امتى.</p>'
         + D1.fig(D.v_growth(), 'الـ capacity بتتضاعف (في g++). كل مرة تتملي، الـ vector بيتنقل لمكان جديد أكبر.')
         + prog(SRC + 'v5_growth.cpp', 'vector_growth.cpp')
         + res(term(rd(SRC + 'v5_growth.txt')) + '<p style="font-size:10pt">الـ vector اتنقل 5 مرات بس في 9 إضافات، لأنه كل مرة بيحجز ضعف اللي محتاجه. ولو عارف العدد من الأول، <code>reserve()</code> بتمنع النقل خالص (ده موضوع حلقة The Cherno الجاية: Optimizing std::vector).</p>'))
P.append(SB.d2_growth())
P.append('<h3 id="why-vec">ليه كتبنا كل ده؟</h3>' + LEGEND
         + D1.fig(D.v_dangling(), 'أخطر حاجة في الـ vector: لو شايل عنوان عنصر جواه وعملت <code>push_back</code> والـ vector اتنقل، العنوان ده بقى بيشاور على مكان اترجع.')
         + SB.d2_dangling() + WHY.build_vec())
P.append('''<div class="sum"><b>الملخص:</b><ul><li><code>push_back</code> يضيف، <code>size</code> العدد، <code>[]</code> أو <code>at</code> للقراية، <code>erase</code> و <code>clear</code> و <code>pop_back</code> للمسح.</li>
 <li>في اللوب وفي مدخل الدالة: <code>&amp;</code> لو هتعدّل، و <code>const&amp;</code> لو هتقرا بس.</li>
 <li>الـ vector بيتنقل وهو بيكبر، فماتحتفظش بعناوين عناصره.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> في برنامج 4 ضيف دالة <code>float totalLength(const std::vector&lt;Point&gt;&amp; points)</code> تحسب طول الخط اللي بيوصل النقط ببعض، واستخدم قانون الطول من محاضرة الرياضيات. (الإجابة للنقط الـ 3: 100 + 50 = 150)</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>C والـ Pointers:</b> آخر مدخل في <code>glVertexAttribPointer</code> نوعه <code>void*</code> لأن OpenGL مكتوب بأسلوب C. و <code>malloc</code>/<code>free</code> هي أصل <code>new</code>/<code>delete</code> اللي جوه الـ vector.</td></tr>
 <tr><td class="n">2</td><td><b>Vertex Attributes:</b> بيانات الأركان في الآخر هتيجي من <code>std::vector&lt;Vertex&gt;</code> بدل مصفوفة ثابتة، وهتبعتها بـ <code>vertices.data()</code>.</td></tr>
 <tr><td class="n">3</td><td><b>الطول:</b> هتحتاجه في الـ CAD عشان تحسب طول الخطوط، وفي <code>normalize</code> اللي في الكاميرا (normalize = اقسم على الطول).</td></tr>
 <tr><td class="n">4</td><td><b>الـ vector:</b> مكان تخزين النقط والخطوط في برنامجك.</td></tr>
</table>
<h3>بكره (الثلاثاء 27-10)</h3>
<ul><li>برمجة: References في C++ (The Cherno حلقة 17) + الجزء 2 من فيديو C (حل Hamming من 7:26).</li>
<li>رسم: مراجعة الـ Shaders (How I Deal with Shaders).</li>
<li>رياضيات: الضرب الاتجاهي Cross product (3Blue1Brown فصل 10).</li>
<li>الـ CAD: رسم خط بين نقطتين.</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>مقدمة C: <span class="ltr">youtube.com/watch?v=SVthw_d9nwE</span></li>
 <li>Vertex Attributes: <span class="ltr">youtube.com/watch?v=x0H--CL2tUI</span></li>
 <li>الضرب النقطي والطول: <span class="ltr">youtube.com/watch?v=WNuIhXo39_k</span></li>
 <li>std::vector: <span class="ltr">youtube.com/watch?v=PocJ5jXv8No</span></li></ul></section>''')


import sys as _s; _s.path.insert(0, '/home/claude/day2')
import quick as Q
css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q.DAY2_CARDS, Q.DAY2_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q.DAY2_QA))
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
    page = ('<title>محاضرات الأسبوع 2 · اليوم التاني</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week2_day2_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 2 - اليوم التاني</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week2_day2.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week2_day2.html', base_url='.').write_pdf('Week2_Day2_Monday.pdf')
    import fixpdf; fixpdf.fix('Week2_Day2_Monday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
