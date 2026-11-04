# Week 2 · Day 3 (Tuesday 27-10). Same structure as Day 1/2. MODE='web' builds the copy page; default builds the PDF.
import html, re, os, base64, sys
sys.path.insert(0, '/home/claude/day1')
sys.path.insert(0, '/home/claude/day2')
sys.path.insert(0, '/home/claude/day3')
import weasyprint
import diagrams as D1
import diag3 as D
from data3 import E, OVER
from words3 import REF_WORDS, AMP_TABLE, HAM_WORDS, SHADER_WORDS, CROSS_WORDS, CAD_WORDS
import why_day3 as WHY
import sb as SB
import sb3 as SB3
import quick as Q
import quick3 as Q3

os.chdir('/home/claude/day3')
MODE = globals().get('MODE', 'pdf')
ART = os.environ.get('ART_URL', '').strip()
css = open('final.css', encoding='utf-8').read()
exec(open('hl_src.py', encoding='utf-8').read())
KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4|struct|size_t|auto|enum|static)\b'

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
STH.setup(['specs_d3'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثاني: المؤشرات والـ Shaders</div>
  <h1>اليوم التالت — الثلاثاء 27 أكتوبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> الـ References في C++ + تمرين Hamming في C — <span style="color:#5b6372">The Cherno و Exercism</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> مراجعة الـ Shaders + الـ Shaders في ملف — <span style="color:#5b6372">learnopengl و The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> الضرب الاتجاهي (Cross product) — <span style="color:#5b6372">3Blue1Brown</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> رسم خط بين نقطتين — <span style="color:#5b6372">learnopengl و The Cherno</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:5mm;background:#fffbeb"><b>على Windows (Visual Studio):</b> العناوين بتتطبع من غير <code>0x</code>، وأرقامها بتتغير كل مرة. وفي برنامج الـ Shader، ملف <code>Basic.shader</code> لازم يبقى في <code>res/shaders/</code> جوه مجلد المشروع (اللي فيه ملف <code>.vcxproj</code>).</div>
</section>''')

# ================================================================== 1 · References + Hamming
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'الـ References في C++ + تمرين Hamming',
             'The Cherno · حلقة 17 · <span class="ltr">youtu.be/IzoFn3dfsPA</span> · Exercism · A Brief Introduction to C (من 7:26) · <span class="ltr">youtu.be/SVthw_d9nwE?t=446</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Reference = <b>اسم تاني</b> لمتغير موجود. أي حاجة تعملها في الاسم التاني بتحصل في الأصل.</div>
<p class="note" style="margin:0 0 3mm">The Cherno بيقول إن الـ References هي Pointers «متنكرة»: الـ compiler بيعمل نفس الشغل من جوه، بس إنت بتكتب من غير <code>*</code> و <code>&amp;</code> في كل حتة.</p>''')
P.append(D1.fig(D.r_alias(), 'شمال: الـ Reference مش صندوق جديد، ده اسم تاني على نفس الصندوق. يمين: الـ Pointer صندوق تاني جواه العنوان.'))
P.append('<h3>علامة &amp; ليها معنيين، والنجمة ليها معنيين</h3><p class="what">نفس القاعدة اللي اتكلمنا فيها: <b>لازقة في نوع</b> = جزء من النوع. <b>قبل اسم متغير</b> = أمر.</p>' + AMP_TABLE)
P.append('<h3 id="ref-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(REF_WORDS))
P.append('<h3>البرنامج 1: اسم تاني لنفس الصندوق</h3><p class="what">بنعمل Reference ونغيّر عن طريقه، وبنطبع العنوانين عشان نتأكد إنهم صندوق واحد.</p>'
         + prog(SRC + 'r1_reference.cpp', 'reference.cpp') + res(term(rd(SRC + 'r1_reference.txt')) + '<p style="font-size:10pt">‏<code>a</code> بقى 2، والعنوانين نفس الرقم بالظبط.</p>'))
P.append(SB3.d3_ref())
P.append('<h3>البرنامج 2: 3 طرق لدالة تزوّد رقم</h3><p class="what">ده المثال الأساسي في الحلقة: نسخة (مش شغالة)، وعنوان (شغالة بس فيها نجوم)، و Reference (شغالة ونضيفة).</p>'
         + D1.fig(D.r_three(), 'النسخة صندوق جديد، فالأصل مابيتغيرش. الـ Pointer بيمسك العنوان. الـ Reference اسم تاني لنفس الصندوق.')
         + prog(SRC + 'r2_increment.cpp', 'increment.cpp') + res(term(rd(SRC + 'r2_increment.txt')) + '<p style="font-size:10pt">النسخة ما غيّرتش حاجة (5). العنوان زوّد (6). الـ Reference زوّد (7).</p>'))
P.append('<h3>البرنامج 3: الـ Reference مابيتنقلش</h3><p class="what">أهم قاعدة في الحلقة: بعد ما الـ Reference يتربط، مش هيتربط بحاجة تانية أبداً.</p>'
         + prog(SRC + 'r3_rebind.cpp', 'rebind.cpp') + res(term(rd(SRC + 'r3_rebind.txt'))))
P.append(SB3.d3_rebind())
P.append('<h3>البرنامج 4: كود The Cherno كامل</h3>' + prog(SRC + 'r4_cherno.cpp', 'references_cherno.cpp') + res(term(rd(SRC + 'r4_cherno.txt')) + '<p style="font-size:10pt">نفس أرقام الفيديو: 2 ثم 3 ثم 2 ثم 1.</p>'))
P.append('''<h3>Reference ولا Pointer؟</h3><table class="types"><tr><th></th><th>Reference</th><th>Pointer</th></tr>
<tr><td>ممكن يبقى فاضي؟</td><td>لأ، لازم يتربط بحاجة</td><td>أيوه: <code>nullptr</code></td></tr>
<tr><td>ممكن يتنقل لحاجة تانية؟</td><td>لأ</td><td>أيوه: <code>ptr = &amp;b</code></td></tr>
<tr><td>بتكتب نجمة عشان توصل للقيمة؟</td><td>لأ</td><td>أيوه: <code>*ptr</code></td></tr>
<tr><td>استخدمه لما</td><td>مدخل دالة هتعدّله، أو <code>const&amp;</code> عشان ماتنسخش</td><td>محتاج «فاضي» أو تتنقل</td></tr></table>
<div class="ok"><b>هتشوفه فين النهارده؟</b> في محاضرة الرسم: <code>ParseShader(const std::string&amp; filepath)</code>. ويوم الإتنين في الـ vector: <code>for (const Vertex&amp; v : vertices)</code>. كلهم نفس الفكرة.</div>''')

P.append('<h3 id="hamming">تمرين Hamming (Exercism، الجزء 2 من فيديو C: من 7:26)</h3>'
         '<p class="what">المطلوب: عندك سلسلتين DNA (حروف A و C و G و T)، احسب كام مكان الحرف فيه مختلف. لو الطولين مختلفين رجّع ‎-1. ده اسمه «Hamming distance». الفيديو حلّه بطريقتين، والاتنين هنا.</p>')
P.append(D1.fig(D.h_strands(), 'مثال الفيديو: قارن حرف بحرف. الأحمر = مختلف، والعدد 7. والـ <code>\\0</code> في الآخر علامة نهاية النص في C.'))
P.append('''<div class="note"><b>النصوص في C (من الفيديو):</b> مفيش نوع اسمه String في C. النص = صف حروف ورا بعض، وفي آخره حرف خفي <code>'\\0'</code> (Null Terminator). فـ <code>"Hamming"</code> في الذاكرة 8 خانات: H a m m i n g \\0.</div>''')
P.append('<h3 id="ham-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(HAM_WORDS))
P.append('<h3>البرنامج 5: الحل الأول من الفيديو (strlen و for)</h3><p class="what">احسب الطولين الأول؛ لو مختلفين ارجع ‎-1. بعدين لف بـ <code>i</code> وعدّ الاختلافات.</p>'
         + prog(SRC + 'h1_hamming_strlen.c', 'hamming_strlen.c') + res(term(rd(SRC + 'h1_hamming_strlen.txt')) + '<p style="font-size:10pt">‏7 اختلافات (زي الفيديو)، وبعدين 0 (زي بعض)، وبعدين ‎-1 (طولين مختلفين).</p>'))
h1 = {l.strip() for l in open(SRC + 'h1_hamming_strlen.c') if l.strip()}
h2new = {l.strip() for l in open(SRC + 'h2_hamming_pointers.c') if l.strip()} - h1
P.append('<h3>البرنامج 6: الحل المتقدم من الفيديو (Pointer Arithmetic)</h3><p class="what">من غير <code>strlen</code> ومن غير <code>i</code>: الـ Pointerين نفسهم بيمشوا على الحروف (<code>lhs++</code>). ده نفس <code>p++</code> بتاع امبارح. السطور <b>بالأصفر</b> هي اللي اختلفت عن الحل الأول.</p>'
         + prog(SRC + 'h2_hamming_pointers.c', 'hamming_pointers.c', new=h2new) + res(term(rd(SRC + 'h2_hamming_pointers.txt')) + '<p style="font-size:10pt">نفس النتايج، وزيادة: لما بعتنا <code>NULL</code> رجّع ‎-1 من غير ما البرنامج يقع.</p>'))
P.append(SB3.d3_hamming())
P.append('''<table class="types"><tr><th></th><th>الحل الأول</th><th>الحل التاني</th></tr>
<tr><td>بيعرف الطول إزاي؟</td><td><code>strlen</code> قبل اللوب</td><td>بيشوف مين خلص الأول بعد اللوب</td></tr>
<tr><td>بيمشي على الحروف بـ</td><td>رقم <code>i</code> و <code>lhs[i]</code></td><td>الـ Pointer نفسه <code>lhs++</code> و <code>*lhs</code></td></tr>
<tr><td>بيتحقق من NULL؟</td><td>لأ</td><td>أيوه</td></tr>
<tr><td>أسهل في القراية</td><td>✓</td><td></td></tr></table>
<div class="note"><b>Idioms في C من الفيديو:</b> <code>*lhs</code> بدل <code>*lhs != '\\0'</code>، و <code>!ptr</code> بدل <code>ptr == NULL</code>، و <code>? :</code> للاختصار.</div>''')
P.append('<div class="setup"><b>على Exercism (زي الفيديو):</b> الملفات جاهزة: <code>hamming.h</code> فيه سطر التعريف <code>int compute(const char *lhs, const char *rhs);</code>، وإنت بتكتب الدالة بس في <code>hamming.c</code> وأوله <code>#include "hamming.h"</code>، ومن غير <code>main</code>، لأن الموقع عنده اختبارات بتناديها هي. البرامج هنا فيها <code>main</code> عشان تشغّلها لوحدها.</div>')
P.append('<h3 id="why-ref">ليه كتبنا كل ده؟ الهدف من كل خطوة</h3><p class="what">لكل خطوة: <b>ليه</b>، وهي <b>إجبارية ولا لأ</b>، و<b>إيه اللي يحصل لو شيلتها</b> (جربناها فعلاً).</p>'
         + LEGEND + '<h3>الـ References</h3>' + WHY.build_ref() + '<h3>تمرين Hamming</h3>' + WHY.build_ham())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ Reference = اسم تاني، والعنوان واحد.</li>
 <li>علامة <code>&amp;</code> لازقة في نوع = Reference. قبل متغير = عنوان.</li>
 <li>لازم يتربط وهو بيتعمل، ومابيتنقلش، ومايبقاش فاضي.</li>
 <li>في C النص بيخلص بـ <code>'\\0'</code>، وأي لوب على نصين لازم يقف لما أي واحد فيهم يخلص.</li>\n <li>في C ابدأ أي متغير بقيمة (<code>int distance = 0</code>)، وماتثقش في المدخلات (اتحقق من NULL).</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b><br>1. اكتب <code>void Swap(int&amp; a, int&amp; b)</code> تبدّل قيمتين، وجربها.<br>
2. في Hamming: خلّي الحل التاني يرجّع ‎-1 كمان لو أي نص فيه حرف غير A و C و G و T.<br>3. حل التمرين على exercism.org/tracks/c بنفسك بأي طريقة من الاتنين.</div></section>''')

# ================================================================== 2 · Shaders
P.append(lec('l2', 'المحاضرة 2 · رسم', 'مراجعة الـ Shaders + الـ Shaders في ملف', 'قناة The Cherno · How I Deal with Shaders in OpenGL · <span class="ltr">youtu.be/2pv0Fbo-7ms</span> · مراجعة: learnopengl.com/Getting-started/Shaders'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> بدل ما الـ Shader يبقى نص جوه الـ C++ بعلامات تنصيص و <code>\\n</code>، نحطه في ملف لوحده، ونكتب دالة تقراه وتقسمه لنصين.</div>
<h3>مراجعة سريعة (learnopengl)</h3>
<table class="types"><tr><th>الكلمة</th><th>معناها</th><th>شفناها فين</th></tr>
<tr><td><code>in</code></td><td>مدخل: جاي من الـ buffer أو من الـ Shader اللي قبله</td><td>امبارح: <code>aPosition</code> و <code>aColor</code></td></tr>
<tr><td><code>out</code></td><td>مخرج: رايح للـ Shader اللي بعده أو للشاشة</td><td>امبارح: <code>vertexColor</code></td></tr>
<tr><td><code>uniform</code></td><td>قيمة واحدة لكل الأركان، بتيجي من الـ C++</td><td>الأحد: <code>u_Color</code></td></tr>
<tr><td><code>gl_Position</code></td><td>مكان الركن النهائي (لازم يتملي)</td><td>كل البرامج</td></tr></table>''')
P.append(D1.fig(D.s_split(), 'ملف واحد فيه الاتنين. <code>ParseShader</code> بتقرا سطر سطر: سطر <code>#shader</code> بيغيّر «إحنا فين»، وأي سطر تاني بيتكتب في النص المناسب.'))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> GLFW و GLAD متركبين زي كل يوم. واعمل مجلد <code>res/shaders</code> جوه مجلد المشروع، وحط فيه الملف <code>Basic.shader</code> اللي تحت. The Cherno بيستخدم GLEW؛ هنا GLAD، والفرق في سطر التحميل بس.</div>')
P.append('<h3 id="shader-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(SHADER_WORDS))
P.append('<h3>الملف 1: Basic.shader</h3><p class="what">ده ملف نص عادي (مش C++). احفظه في <code>res/shaders/Basic.shader</code>.</p>'
         + prog(SRC + 'res/shaders/Basic.shader', 'Basic.shader'))
P.append('<h3>البرنامج 1: يقرا الملف ويرسم</h3><p class="what">كود The Cherno كامل: <code>ParseShader</code> و <code>CompileShader</code> و <code>CreateShader</code>، وبيطبع النصين عشان نتأكد إن التقسيم صح.</p>'
         + prog(SRC + 's1_shader_file.cpp', 'shader_file.cpp')
         + res(term(rd(SRC + 's1_shader_file.txt')) + bigimg('s1_shader_file', 'المثلث بقى أزرق: اللون جاي من الملف، مش من الـ C++'),
               '▶ النتيجة لما نعمل Run (الـ Terminal والشباك الحقيقي)'))
P.append(SB3.d3_parse())
P.append('<div class="ok"><b>جرّب التغيير السريع:</b> غيّر <code>vec4(0.2, 0.3, 0.8, 1.0)</code> في الملف لأي لون، وشغّل تاني. من غير ما تعيد ترجمة الـ C++، لأن الملف بيتقرا وقت التشغيل.</div>')
P.append('<h3 id="why-shader">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND
         + '<div class="warn" style="font-size:10pt"><b>⚠️ لاحظ:</b> غلطات الـ Shader مابتظهرش وإنت بتترجم الـ C++. بتظهر وقت التشغيل بس، عشان كده طباعة رسالة الخطأ مهمة جداً.</div>'
         + WHY.build_shader())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>ملف واحد فيه الـ Shaderين، وعلامة <code>#shader</code> بتفصلهم.</li>
 <li><code>ParseShader</code>: <code>ifstream</code> + <code>getline</code> + <code>stringstream</code>.</li>
 <li>المسار نسبي، ولو غلط مفيش رسالة: شاشة سودا.</li><li>امسح البرنامج بـ <code>glDeleteProgram</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> خلّي <code>ParseShader</code> تطبع «Could not open file» لو الملف مافتحش. (تلميح: <code>if (!stream.is_open())</code>)</div></section>''')

# ================================================================== 3 · Cross
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'الضرب الاتجاهي (Cross product)', '3Blue1Brown · Essence of Linear Algebra · فصل 10 · <span class="ltr">youtu.be/eu6i7WJeinw</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الضرب النقطي بيقولك المتجهين «متفقين» قد إيه. الضرب الاتجاهي بيقولك المساحة اللي بينهم، وفي 3D بيديك متجه عمودي على الاتنين.</div>
<h3>في 2D: مساحة بإشارة</h3>
<div class="formula">v × w = v<sub>1</sub>w<sub>2</sub> − v<sub>2</sub>w<sub>1</sub>   (المحدد)</div>''')
P.append(D1.fig(D.x_parallelogram(), 'مثال الفيديو: v = (‎-3, 1) و w = (2, 1). المساحة 5، والإشارة سالبة لأن v على شمال w.'))
P.append('''<table class="types"><tr><th>القاعدة</th><th>معناها</th></tr>
<tr><td>v × w = −(w × v)</td><td>الترتيب بيقلب الإشارة</td></tr>
<tr><td>(3v) × w = 3(v × w)</td><td>كبّر متجه 3 مرات، المساحة تكبر 3 مرات</td></tr>
<tr><td>متعامدين</td><td>أكبر مساحة</td></tr><tr><td>نفس الاتجاه</td><td>صفر (مفيش مساحة)</td></tr></table>
<div class="note">3Blue1Brown بيقول إن نسخة الـ 2D دي مش «الضرب الاتجاهي الحقيقي». الحقيقي في 3D وبيطلّع متجه.</div>
<h3>في 3D: متجه</h3>''')
P.append(D1.fig(D.x_3d(), 'مثال الفيديو: v في اتجاه z و w في اتجاه y. المربع مساحته 4، فالناتج طوله 4، واتجاهه ناحية ‎-x بقاعدة الإيد اليمين.'))
P.append('<div class="formula">v × w = ( v<sub>2</sub>w<sub>3</sub> − v<sub>3</sub>w<sub>2</sub> ,  −(v<sub>1</sub>w<sub>3</sub> − v<sub>3</sub>w<sub>1</sub>) ,  v<sub>1</sub>w<sub>2</sub> − v<sub>2</sub>w<sub>1</sub> )</div>'
         + '<p class="note">الفيديو بيحسبها بمحدد 3×3 فيه î و ĵ و k̂، وده بيطلّع نفس الـ 3 أرقام دول.</p>')
P.append('<h3 id="cross-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CROSS_WORDS))
P.append('<h3>الكود: أمثلة الفيديو بالكمبيوتر</h3><p class="what">برنامج كامل من غير أي مكتبات.</p>'
         + prog(SRC + 'x1_cross.cpp', 'cross.cpp') + res(term(rd(SRC + 'x1_cross.txt')) + '<p style="font-size:10pt">نفس أرقام الفيديو: ‎-5، والترتيب بيقلبها، و ×3 بتضربها في 3، و (‎-4, 0, 0) في 3D. والضرب النقطي = 0 بيأكد إن الناتج عمودي.</p>'))
P.append('<div class="ok"><b>شفته قبل كده!</b> في الكاميرا يوم الأحد: <code>glm::normalize(glm::cross(Orientation, Up))</code> = اتجاه «اليمين». ده الضرب الاتجاهي: عمودي على اتجاه النظر وعلى فوق.</div>')
P.append('<h3 id="why-cross">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_cross())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>2D: رقم = v₁w₂ − v₂w₁ (مساحة بإشارة).</li><li>3D: متجه، طوله المساحة، واتجاهه عمودي (الإيد اليمين).</li>
 <li>الترتيب بيقلب الإشارة، ونفس الاتجاه = صفر.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> احسب بإيدك (1, 0, 0) × (0, 1, 0). لازم يطلع (0, 0, 1). وبعدين بدّل الترتيب وشوف الإشارة.</div></section>''')

# ================================================================== 4 · CAD
P.append(lec('l4', 'المحاضرة 4 · CAD', 'رسم خط بين نقطتين', 'قناة The Cherno · Vertex Buffers and Drawing a Triangle · <span class="ltr">youtu.be/0p9VxImr7Y0</span> · learnopengl.com/Getting-started/Hello-Triangle · التوثيق: docs.gl'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> نفس خطوات رسم المثلث بالظبط (buffer ← bind ← البيانات ← الرسم)، بس بنقطتين و <code>GL_LINES</code>. ودي أول أداة في برنامج الـ CAD بتاعك.</div>
<h3>الخطوات من الحلقة</h3>
<table class="types"><tr><th>الخطوة</th><th>الدالة</th><th>معناها</th></tr>
<tr><td>1. اعمل buffer</td><td><code>glGenBuffers(1, &amp;buffer)</code></td><td>هات رقم (ID) لـ buffer جديد</td></tr>
<tr><td>2. اختاره</td><td><code>glBindBuffer(GL_ARRAY_BUFFER, buffer)</code></td><td>Bind = اختار. أي أمر بعد كده هيشتغل عليه</td></tr>
<tr><td>3. ابعت البيانات</td><td><code>glBufferData(…)</code></td><td>انسخ الأرقام لذاكرة كارت الشاشة (VRAM)</td></tr>
<tr><td>4. ارسم</td><td><code>glDrawArrays(mode, first, count)</code></td><td>Draw Call: ارسم من الـ buffer المختار</td></tr></table>
<div class="note"><b>OpenGL = State Machine:</b> زي Photoshop، لازم تختار الـ layer الأول وبعدين ترسم. OpenGL بيرسم بالحاجات «المختارة» دلوقتي.</div>
<table class="types"><tr><th>نوع الرسم (mode)</th><th>بيعمل إيه</th></tr>
<tr><td><code>GL_POINTS</code></td><td>كل نقطة لوحدها</td></tr><tr><td><code>GL_LINES</code></td><td>كل نقطتين = خط</td></tr>
<tr><td><code>GL_LINE_STRIP</code></td><td>خط متصل بيعدّي على كل النقط</td></tr><tr><td><code>GL_TRIANGLES</code></td><td>كل 3 نقط = مثلث</td></tr></table>
<table class="types"><tr><th>التلميح (usage)</th><th>معناه</th></tr>
<tr><td><code>GL_STATIC_DRAW</code></td><td>البيانات هتتحط مرة وتترسم كتير</td></tr>
<tr><td><code>GL_DYNAMIC_DRAW</code></td><td>هتتغير كتير وتترسم كتير</td></tr>
<tr><td><code>GL_STREAM_DRAW</code></td><td>هتتحط مرة وتترسم مرات قليلة</td></tr></table>''')
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD). و The Cherno في الحلقة قال الكود «مش هيظهر حاجة لسه» لأن ناقصه Shader و Attribute. البرامج هنا كاملة، وجربنا كود الحلقة زي ما هو في قسم «ليه».</div>')
P.append('<h3 id="cad-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CAD_WORDS))
P.append('<h3>البرنامج 1: خط بين نقطتين ثابتين</h3><p class="what">نقطتين في مصفوفة، ونرسمهم مرتين: مرة كخط أبيض، ومرة كنقط برتقاني.</p>'
         + prog(SRC + 'l1_line.cpp', 'line.cpp')
         + res(bigimg('l1_line', 'خط أبيض بين نقطتين برتقاني'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
l1 = {l.strip() for l in open(SRC + 'l1_line.cpp') if l.strip()}
l2new = {l.strip() for l in open(SRC + 'l2_click_lines.cpp') if l.strip()} - l1
P.append('<h3>البرنامج 2 (للـ CAD): ارسم بالماوس</h3><p class="what">كل دوستين = خط. النقط بتتخزن في <code>std::vector</code> (محاضرة امبارح)، وبتتبعت لكارت الشاشة مع كل دوسة. السطور المتعلّمة <b>بالأصفر</b> هي الجديدة عن البرنامج 1.</p>'
         + D1.fig(D.l_pixels(), 'الماوس بيدّيك بكسل (0 فوق شمال)، و OpenGL عايز من ‎-1 لـ +1 (و +1 فوق). عشان كده بنحوّل ونقلب y.')
         + D1.fig(D.l_pipeline(), 'اللي بيحصل مع كل دوسة.')
         + prog(SRC + 'l2_click_lines.cpp', 'click_lines.cpp', new=l2new)
         + res(term(rd(SRC + 'l2_click_lines.txt'))
               + grid([shot('l2_1', 'دوسة 1'), shot('l2_2', 'دوسة 2: خط'), shot('l2_3', 'دوسة 3'), shot('l2_4', 'دوسة 4: خط تاني'), shot('l2_5', 'دوسة 5')], 5)
               + '<p style="font-size:10pt">دوسنا بالماوس فعلاً 5 مرات في الشباك. كل دوستين بقوا خط.</p>', '▶ النتيجة لما نعمل Run (دوسات حقيقية بالماوس)'))
P.append(SB3.d3_click())
P.append('<h3 id="why-cad">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_cad())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>buffer ← bind ← <code>glBufferData</code> (بالبايت) ← <code>glDrawArrays</code>.</li>
 <li><code>GL_LINES</code> = كل نقطتين خط.</li><li>البكسل ← OpenGL: <code>2*px/width - 1</code> و <code>1 - 2*py/height</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> في البرنامج 2 غيّر <code>GL_LINES</code> لـ <code>GL_LINE_STRIP</code>: كل النقط هتتوصل بخط واحد متصل (زي أداة Polyline في AutoCAD). وبعدين خلّي الزرار اليمين يمسح كل النقط (<code>points.clear()</code>).</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>الـ References:</b> <code>ParseShader(const std::string&amp; filepath)</code> في محاضرة الرسم بتاخد Reference عشان ماتنسخش النص.</td></tr>
 <tr><td class="n">2</td><td><b>ملف الـ Shader:</b> هتستخدم نفس <code>ParseShader</code> في الـ CAD لما الـ Shaders تكتر (خطوط، نقط، اختيار…).</td></tr>
 <tr><td class="n">3</td><td><b>الضرب الاتجاهي:</b> هو اللي بيدّي الكاميرا اتجاه «اليمين»، وهتحتاجه في الـ CAD عشان تعرف النقطة على يمين الخط ولا شماله.</td></tr>
 <tr><td class="n">4</td><td><b>رسم الخط:</b> أول أداة رسم حقيقية في برنامجك، وبتجمع كل اللي فات: vector + buffer + Shader + Uniform.</td></tr>
</table>
<h3>بكره (الأربعاء 28-10)</h3>
<ul><li>برمجة: Const و Static (The Cherno).</li><li>رسم: Index Buffers (EBO) ورسم مستطيل.</li>
<li>رياضيات: الضرب الاتجاهي (Khan Academy).</li><li>الـ CAD: رسم عدة خطوط.</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>References: <span class="ltr">youtube.com/watch?v=IzoFn3dfsPA</span></li>
 <li>مقدمة C (Hamming من 7:26 لـ 21:43): <span class="ltr">youtube.com/watch?v=SVthw_d9nwE&amp;t=446s</span> · <span class="ltr">exercism.org/tracks/c</span></li>
 <li>How I Deal with Shaders: <span class="ltr">youtube.com/watch?v=2pv0Fbo-7ms</span> · <span class="ltr">learnopengl.com/Getting-started/Shaders</span></li>
 <li>Cross products: <span class="ltr">youtube.com/watch?v=eu6i7WJeinw</span></li>
 <li>Vertex Buffers: <span class="ltr">youtube.com/watch?v=0p9VxImr7Y0</span> · <span class="ltr">learnopengl.com/Getting-started/Hello-Triangle</span> · <span class="ltr">docs.gl</span></li></ul></section>''')

css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q3.DAY3_CARDS, Q3.DAY3_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q3.DAY3_QA))
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
    page = ('<title>محاضرات الأسبوع 2 · اليوم التالت</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week2_day3_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 2 - اليوم التالت</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week2_day3.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week2_day3.html', base_url='.').write_pdf('Week2_Day3_Tuesday.pdf')
    import fixpdf; fixpdf.fix('Week2_Day3_Tuesday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
