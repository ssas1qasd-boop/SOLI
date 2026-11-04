# Week 2 · Day 5 (Thursday 29-10). Same structure as Days 1-4. MODE="web" builds the copy page; default builds the PDF.
import html, re, os, base64, sys
for d in ('day1', 'day2', 'day3', 'day4', 'day5'):
    sys.path.insert(0, f'/home/claude/{d}')
import weasyprint
import diagrams as D1
import diag5 as D
from data5 import E, OVER
from words5 import *
import why_day5 as WHY
import sb as SB
import sb5 as SB5
import quick as Q
import quick5 as Q5

os.chdir('/home/claude/day5')
MODE = globals().get('MODE', 'pdf')
ART = os.environ.get('ART_URL', '').strip()
css = open('final.css', encoding='utf-8').read()
exec(open('hl_src.py', encoding='utf-8').read())
KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4|struct|size_t|auto|enum|static|extern|mutable|private|using|namespace|import|as)\b'

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
sys.path.insert(0, '/home/claude/steps')
import steps_hook as STH
import jumps as JUMP
STH.setup(['specs_d5'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثاني: المؤشرات والـ Shaders</div>
  <h1>اليوم الخامس — الخميس 29 أكتوبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> تمرين swap بالـ Pointers — <span style="color:#5b6372">C Plus+ و cppreference</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> تعديل الـ Shader — <span style="color:#5b6372">The Cherno و learnopengl</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> dot و cross في Python و NumPy — <span style="color:#5b6372">Keith Galli و NumPy</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> مسح آخر خط (push_back و pop_back) — <span style="color:#5b6372">Engineer4Free و cppreference</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:5mm;background:#fffbeb"><b>النهارده فيه Python:</b> محاضرة الرياضيات بتتكتب بـ Python مش C++. على Windows نزّل Python من python.org (علّم على <b>Add python.exe to PATH</b>)، وبعدين في الـ Terminal: <code>pip install numpy</code>، وشغّل الملف بـ <code>python dot_cross.py</code>. وعلى Windows ممكن <code>dtype</code> تطلع <code>int32</code> بدل <code>int64</code>.</div>
</section>''')

# ================================================================== 1 · swap with pointers
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'تمرين swap بالـ Pointers',
             'C Plus+ · swap two numbers in C++ using pointers · <span class="ltr">youtu.be/ocvBqhMUAOM</span> · cppreference.com/w/cpp/language/pointer'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الدالة العادية بتاخد <b>نسخة</b>، فمهما غيّرت فيها الأصل مش هيحس. لو بعتّلها <b>العنوان</b>، تقدر تروح للصندوق الأصلي وتغيّر اللي جواه.</div>
<p class="what">ده تمرين على كل اللي اتعلمناه في الأسبوع: الـ Pointer (الأحد)، والـ <code>&amp;</code> و <code>*</code>، والـ Reference (التلات). الفيديو بيبدّل رقمين <code>x</code> و <code>y</code> بدالة اسمها <code>swap</code>.</p>''')
P.append(D1.fig(D.p_swap(), '<code>a</code> و <code>b</code> جوه الدالة مش أرقام: دول عناوين بتشاور على <code>x</code> و <code>y</code> اللي في <code>main</code>. و <code>temp</code> صندوق مؤقت.'))
P.append(SWAP_TABLE)
P.append('<h3 id="swap-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(SWAP_WORDS))
P.append('<h3>البرنامج 1: كود الفيديو</h3><p class="what">زي الفيديو بالظبط: الدالة مكتوبة <b>تحت</b> <code>main</code>، فلازم سطر التعريف جوه <code>main</code> قبل النداء.</p>'
         + prog(SRC + 'p1_swap_pointers.cpp', 'swap_pointers.cpp') + res(term(rd(SRC + 'p1_swap_pointers.txt')) + '<p style="font-size:10pt">اتبدلوا: x بقى 20 و y بقى 10.</p>'))
P.append(SB5.d5_swap())
P.append('<h3>البرنامج 2: نفس التبديل بـ 3 طرق، والعناوين قدامك</h3><p class="what">بالقيمة، وبالـ Pointer، وبالـ Reference. كل دالة بتطبع عناوين اللي استلمته، فتشوف بعينك مين نسخة ومين الأصل.</p>'
         + prog(SRC + 'p2_swap_three.cpp', 'swap_three.cpp') + res(term(rd(SRC + 'p2_swap_three.txt')) + '<p style="font-size:10pt">SwapValue استلمت عناوين <b>مختلفة</b> (نسخ)، فماحصلش حاجة. SwapPointer و SwapReference استلموا <b>نفس</b> عناوين x و y، فبدّلوا فعلاً. والأرقام اللي زي <code>0x7ffe...</code> بتتغير كل مرة تشغّل فيها البرنامج.</p>'))
P.append(D1.fig(D.p_three(), 'الـ 3 طرق: النسخ (برتقاني) مالهاش علاقة بالأصل. الـ Pointer شايل العنوان. الـ Reference اسم تاني لنفس الصندوق.'))
P.append('<h3 id="why-swap">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_swap())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>نسخة = الأصل مايتغيرش. عنوان أو Reference = الأصل يتغير.</li>
 <li><code>&amp;x</code> في النداء = عنوان، و <code>*a</code> جوه الدالة = القيمة اللي في العنوان.</li>
 <li><code>temp</code> عشان القيمة الأولى ماتضيعش، وسطر التعريف لو الدالة تحت <code>main</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> اكتب دالة <code>void Increment(int* p)</code> تزوّد الرقم 1، ونادِيها 3 مرات على <code>x</code>. وبعدين اكتبها بالـ Reference. (لازم x يطلع 13)</div></section>''')

# ================================================================== 2 · shader edit
r1 = {l.strip() for l in open(SRC + 'r1_red_triangle.cpp') if l.strip()}
r2new = {l.strip() for l in open(SRC + 'r2_shader_edit.cpp') if l.strip()} - r1
P.append(lec('l2', 'المحاضرة 2 · رسم', 'تعديل الـ Shader', 'قناة The Cherno · Writing a Shader in OpenGL · <span class="ltr">youtu.be/71BLZwRGUJE</span> · learnopengl.com/Getting-started/Shaders'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Shader برنامج صغير بيشتغل جوه كارت الشاشة. لو عدّلت فيه سطر، الشكل واللون يتغيروا من غير ما تلمس أرقام C++. بس لأنه بيتترجم وقت التشغيل، لازم تطبع أخطاءه بنفسك.</div>
<p class="what">في الحلقة دي The Cherno كتب دالتين بالتفصيل (<code>CompileShader</code> و <code>CreateShader</code>) وزوّد فحص الأخطاء، ورسم مثلث أحمر. إحنا هنكتب كوده الأول، وبعدين <b>نعدّل</b> الـ Shader: نكبّر المثلث ونلوّنه حسب المكان.</p>''')
P.append(GLSL_TABLE)
P.append(D1.fig(D.r_vec4(), 'الـ buffer فيه رقمين لكل ركن، والـ Shader طالب <code>vec4</code>: الكارت بيكمّل z = 0 و w = 1.'))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD). الـ Shaders هنا مكتوبة كنص <code>std::string</code> زي الفيديو، مش في ملف.</div>')
P.append('<h3 id="shader-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(SHADER_WORDS))
P.append('<h3>البرنامج 1: كود The Cherno (مثلث أحمر، مع فحص الأخطاء)</h3><p class="what">الجديد في <code>CompileShader</code>: لو الترجمة فشلت، بنسأل عن طول الرسالة، ونجيبها، ونطبعها، ونقول هو Vertex ولا Fragment، ونمسح الـ Shader ونرجّع 0. و <code>CreateShader</code> فيها <code>glValidateProgram</code>.</p>'
         + prog(SRC + 'r1_red_triangle.cpp', 'red_triangle.cpp') + res(bigimg('r1_red_triangle', 'مثلث أحمر'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(COLOR_TABLE)
P.append(D1.fig(D.r_pipeline(), 'البرنامج 2: الـ Vertex بيكبّر ويبعت المكان، والـ Rasterizer بيخلط، والـ Fragment بيلوّن كل بكسل.'))
P.append('<h3>البرنامج 2: تعديل الـ Shader</h3><p class="what">نفس البرنامج بالظبط، والسطور <b>بالأصفر</b> بس هي اللي اتغيرت، وكلها <b>جوه نص الـ Shader</b>: C++ ماتغيرش خالص.</p>'
         + prog(SRC + 'r2_shader_edit.cpp', 'shader_edit.cpp', new=r2new) + res(bigimg('r2_shader_edit', 'المثلث كبر مرة ونص، ولونه بيتدرج حسب المكان'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(SB5.d5_shader())
P.append('<h3 id="why-shader">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_shader())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>افحص <code>GL_COMPILE_STATUS</code> واطبع الرسالة: ده الطريقة الوحيدة تعرف غلطك جوه الـ Shader.</li>
 <li>Vertex: مرة لكل ركن، و <code>gl_Position</code>. Fragment: مرة لكل بكسل، واللون من 0 لـ 1.</li>
 <li><code>out</code> في الـ Vertex و <code>in</code> في الـ Fragment بنفس الاسم = تبعت بيانات بينهم.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. خلّي المثلث أزرق. 2. اقلبه على راسه من الـ Vertex. 3. امسح <code>;</code> من أي سطر في الـ Shader واقرا الرسالة: فيها رقم السطر.</div></section>''')

# ================================================================== 3 · NumPy dot & cross
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'dot و cross في Python و NumPy', 'Keith Galli · Complete Python NumPy Tutorial · <span class="ltr">youtu.be/GB9ByFAIAH4</span> · numpy.org/doc/stable/reference/generated/numpy.dot.html'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> نفس الضرب النقطي والاتجاهي اللي حسبناهم بإيدنا وبـ C++ الأسبوع ده، بس في سطر واحد بمكتبة NumPy. و NumPy سريعة لأنها بتحط الأرقام جنب بعض في الذاكرة زي الـ array في C++.</div>
<p class="what">الفيديو طويل (ساعة) وبيغطي NumPy كلها. إحنا محتاجين منه: إزاي تعمل مصفوفة، وتعرف شكلها، وتوصل لعناصرها، وتحسب عليها، وتحذير النسخ. وبعدين <code>np.dot</code> و <code>np.cross</code>.</p>''')
P.append(D1.fig(D.n_list_vs_np(), 'الـ List في Python: كل رقم object كبير في حتة، والـ List شايلة عناوينهم. NumPy: الأرقام نفسها جنب بعض، 8 بايت لكل واحد.'))
P.append('<h3 id="numpy-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(NUMPY_WORDS))
P.append('<h3>البرنامج 1: أساسيات NumPy</h3><p class="what">من أول جزء في الفيديو: الإنشاء والشكل والنوع والحجم، والوصول للعناصر، والحساب على كل العناصر، وتحذير النسخ.</p>'
         + prog(SRC + 'n1_numpy_basics.py', 'numpy_basics.py') + res(term(rd(SRC + 'n1_numpy_basics.txt')) + '<p style="font-size:10pt">لاحظ آخر سطرين: <code>c = a</code> غيّرت <code>a</code>، و <code>copy()</code> لأ.</p>'))
P.append(D1.fig(D.n_shape(), 'العد من صفر. <code>:</code> معناها «كله».'))
P.append(NUMPY_TABLE)
P.append('<h3>البرنامج 2: dot و cross</h3><p class="what">نفس مثال Khan Academy بتاع امبارح: [1, ‎-7, 1] × [5, 2, 4]. وبعدين الطول والزاوية، و x × y، وكذا متجه مرة واحدة.</p>'
         + prog(SRC + 'n2_dot_cross.py', 'dot_cross.py') + res(term(rd(SRC + 'n2_dot_cross.txt')) + '<p style="font-size:10pt">نفس [‎-30, 1, 37] اللي طلعت امبارح بـ C++ وبإيدنا، والضرب النقطي معاه أصفار. والزاوية بين [3, 4] و [4, 3] = 16.26 درجة.</p>'))
P.append('<h3 id="why-numpy">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_numpy())
P.append('''<div class="sum"><b>الملخص:</b><ul><li><code>np.array</code> + <code>shape</code> و <code>dtype</code> و <code>b[r, c]</code> و <code>b[:, c]</code>.</li>
 <li><code>np.dot</code> = رقم، و <code>np.cross</code> = متجه (3D بس)، و <code>np.linalg.norm</code> = الطول.</li>
 <li><code>c = a</code> اسم تاني، و <code>a.copy()</code> نسخة.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> احسب بـ NumPy الزاوية بين [1, 0, 0] و [1, 1, 0] (الإجابة: 45 درجة)، و [2, 3, 4] × [5, 6, 7] (الإجابة: [‎-3, 6, ‎-3]).</div></section>''')

# ================================================================== 4 · delete last line
P.append(lec('l4', 'المحاضرة 4 · CAD', 'مسح آخر خط (push_back و pop_back)', 'Engineer4Free · Use push_back and pop_back to add or remove elements from vectors · <span class="ltr">youtu.be/opAnlfre-Kw</span> · cppreference.com/w/cpp/container/vector/pop_back'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ vector بيكبر من الآخر بـ <code>push_back</code> ويصغر من الآخر بـ <code>pop_back</code>. ده بالظبط اللي محتاجينه لزرار «تراجع»: آخر خط اترسم هو أول واحد يتمسح.</div>''')
P.append(VECTOR_TABLE)
P.append(D1.fig(D.v_pushpop(), 'مثال الفيديو: كل اسم بيتضاف في الآخر، والـ Q اتضافت هي كمان، فـ <code>pop_back</code> شالتها.'))
P.append('<h3 id="vector-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(VECTOR_WORDS))
c1_term = 'Please enter the names, press Q to quit:\nBraden\nJeff\nKatie\nQ\n' + '\n'.join(rd(SRC + 'c1_out.txt').splitlines()[1:])
P.append('<h3>البرنامج 1: كود الفيديو (أسماء لحد ما تكتب Q)</h3><p class="what">زي الفيديو: <code>using namespace std</code>، و Sentinel اسمه Q، و <code>pop_back</code> بعد اللوب.</p>'
         + prog(SRC + 'c1_names_vector.cpp', 'names_vector.cpp') + res(term(c1_term) + '<p style="font-size:10pt">كتبنا الأربع كلمات في الـ Terminal. البرنامج قال 3 أسماء، لأن <code>pop_back</code> شالت الـ Q.</p>'))
P.append(SB5.d5_names())
c2new = {l.strip() for l in open(SRC + 'c2_delete_last_line.cpp') if l.strip()} - {l.strip() for l in open('/home/claude/day4/src/v2_polylines.cpp') if l.strip()}
P.append(D1.fig(D.c_delete(), 'كل خط في <code>polylines</code> = بداية وعدد، ونقطه في <code>points</code> (رقمين لكل نقطة).'))
P.append('<h3>البرنامج 2 (للـ CAD): Backspace يمسح آخر خط</h3><p class="what">برنامج الـ Polylines بتاع امبارح + زرار Backspace. السطور <b>بالأصفر</b> جديدة: دالة للكيبورد، ورفع النقط بقى في دالة لوحده.</p>'
         + prog(SRC + 'c2_delete_last_line.cpp', 'delete_last_line.cpp', new=c2new)
         + res(term(rd(SRC + 'c2_delete_last_line.txt'))
               + grid([shot('c2_9', 'خطين'), shot('c2_10', 'Backspace: التاني اتمسح'), shot('c2_13', 'خط جديد بـ 3 نقط'), shot('c2_14', 'Backspace: اتمسح'),
                       shot('c2_15', 'Backspace: الأول اتمسح'), shot('c2_17', 'خط جديد من الأول')], 3)
               + '<p style="font-size:10pt">دوسنا بالماوس وبالكيبورد فعلاً، ودي لقطات الشباك بعد كل خطوة.</p>', '▶ النتيجة لما نعمل Run (دوسات حقيقية بالماوس والكيبورد)'))
P.append(SB5.d5_delete())
P.append('<h3 id="why-vector">ليه كتبنا كل ده؟</h3>' + LEGEND + '<h3>البرنامج 1 (الأسماء)</h3>' + WHY.build_vector() + '<h3>البرنامج 2 (مسح آخر خط)</h3>' + WHY.build_delete())
P.append('''<div class="sum"><b>الملخص:</b><ul><li><code>push_back</code> في الآخر، و <code>pop_back</code> من الآخر، و <code>back()</code> تشوف الآخر من غير ما تمسح.</li>
 <li>ماتعملش <code>pop_back</code> على قايمة فاضية: اسأل عن <code>size()</code> الأول.</li>
 <li>مسح خط = <code>pop_back</code> من <code>polylines</code> + (عدد النقط × 2) <code>pop_back</code> من <code>points</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> خلّي زرار <b>Delete</b> (<code>GLFW_KEY_DELETE</code>) يمسح كل الخطوط مرة واحدة: <code>points.clear()</code> و <code>polylines.clear()</code> وبعدين خط فاضي جديد.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>swap بالـ Pointers:</b> نفس فكرة <code>glGenBuffers(1, &amp;buffer)</code>: بنبعت عنوان المتغير عشان الدالة تكتب جواه.</td></tr>
 <tr><td class="n">2</td><td><b>تعديل الـ Shader:</b> الـ Fragment اللي بيلوّن حسب المكان هو أساس أي تأثير بعد كده (إضاءة، Textures).</td></tr>
 <tr><td class="n">3</td><td><b>NumPy:</b> نفس الرياضيات في سطر، عشان تتأكد من حساباتك بسرعة قبل ما تكتبها في C++.</td></tr>
 <tr><td class="n">4</td><td><b>مسح آخر خط:</b> أداة الرسم بقى عندها «تراجع». و <code>pop_back</code> على vector هي نفس فكرة الـ Stack.</td></tr>
</table>
<h3>بكره (الجمعة 30-10)</h3>
<ul><li>برمجة: تمرينين من exercism.</li><li>رسم: ألوان متحركة (مراجعة Uniforms).</li>
<li>رياضيات: مراجعة الضرب النقطي وطول المتجه.</li><li>الـ CAD: تنظيف الكود (Refactoring).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>swap two numbers in C++ using pointers: <span class="ltr">youtube.com/watch?v=ocvBqhMUAOM</span> · <span class="ltr">en.cppreference.com/w/cpp/language/pointer</span></li>
 <li>Writing a Shader in OpenGL: <span class="ltr">youtube.com/watch?v=71BLZwRGUJE</span> · <span class="ltr">learnopengl.com/Getting-started/Shaders</span></li>
 <li>Complete Python NumPy Tutorial: <span class="ltr">youtube.com/watch?v=GB9ByFAIAH4</span> · <span class="ltr">numpy.org/doc/stable/reference/generated/numpy.dot.html</span></li>
 <li>push_back و pop_back: <span class="ltr">youtube.com/watch?v=opAnlfre-Kw</span> · <span class="ltr">en.cppreference.com/w/cpp/container/vector/pop_back</span></li></ul></section>''')

css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q5.DAY5_CARDS, Q5.DAY5_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q5.DAY5_QA))
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
    page = ('<title>محاضرات الأسبوع 2 · اليوم الخامس</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week2_day5_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 2 - اليوم الخامس</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week2_day5.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week2_day5.html', base_url='.').write_pdf('Week2_Day5_Thursday.pdf')
    import fixpdf; fixpdf.fix('Week2_Day5_Thursday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
