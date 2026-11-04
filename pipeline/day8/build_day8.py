# Week 3 · Day 1 (Sunday 1-11). Same structure as Week 2. MODE="web" builds the copy page; default builds the PDF.
import html, re, os, base64, sys
for d in ('day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8'):
    sys.path.insert(0, f'/home/claude/{d}')
import weasyprint
import diagrams as D1
import diag8 as D
from data8 import E, OVER
from words8 import *
import why_day8 as WHY
import sb as SB
import sb8 as SB8
import quick as Q
import quick8 as Q8

os.chdir('/home/claude/day8')
MODE = globals().get('MODE', 'pdf')
ART = os.environ.get('ART_URL', '').strip()
css = open('final.css', encoding='utf-8').read()
exec(open('hl_src.py', encoding='utf-8').read())
KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4|struct|size_t|auto|enum|static|extern|mutable|private|using|namespace|import|as|def|continue|this|sampler2D|unsigned)\b'

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
STH.setup(['specs_d8'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثالث: الـ Classes والـ Textures</div>
  <h1>اليوم الأول — الأحد 1 نوفمبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> الـ Classes (الأساس) — <span style="color:#5b6372">The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> الـ Textures (النظرية) — <span style="color:#5b6372">learnopengl و The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> المصفوفات (المعنى) — <span style="color:#5b6372">3Blue1Brown (الفصل التالت)</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> الـ B-Rep (المفهوم) — <span style="color:#5b6372">Wikipedia و Ekeeda</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:4mm;background:#fffbeb"><b>النهارده الأربعة مربوطين:</b> الـ Class في الـ Texture والـ B-Rep، والمصفوفة هتحرّك الـ Wireframe بعدين.</div>
  <div class="howto" style="margin-top:4mm"><b>على Windows:</b> العناوين من غير <code>0x</code>. وبرنامج الـ Texture محتاج <code>stb_image.h</code> و <code>res/logo.png</code> جنبه (في ملف الكود المضغوط).</div>
</section>''')

# ================================================================== 1 · classes
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'الـ Classes: الأساس', 'The Cherno · CLASSES in C++ (الحلقة 18) · <span class="ltr">youtu.be/2BP8NhxjrO0</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Class = طريقة نجمع بيها البيانات والدوال اللي بتشتغل عليها في حتة واحدة. مش بيضيف حاجة C مش قادرة تعملها، بس بيخلّي الكود أنظف (The Cherno).</div>
<p class="what">البرنامج 1 هو مثال The Cherno: لاعب ليه مكان وسرعة ودالة <code>Move</code>. هنكتب الحركة مرة كـ Method جوه الكلاس ومرة كدالة برّه، ونشوف إنهم نفس الشغل. وبعدين نطبع الـ Object في الرام. والبرنامج 2 عداد <code>private</code>: الكلاس بيحمي بياناته، وبنطبع <code>this</code>.</p>''')
P.append(D1.fig(D.c_objects(), 'الكلاس قالب، والـ Object نسخة حقيقية في الرام. الأرقام من تشغيلة حقيقية: <code>player</code> 12 بايت، و x و y و speed جنب بعض كل 4 بايت.'))
P.append(CLASS_TABLE)
P.append('<h3 id="class-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CLASS_WORDS))
P.append('<h3>البرنامج 1: اللاعب (مثال The Cherno)</h3><p class="what">نفس الحركة بطريقتين، و Object تاني، والـ Object في الرام.</p>'
         + prog(SRC + 'p1_player.cpp', 'player.cpp') + res(term(rd(SRC + 'p1_player.txt')) + '<p style="font-size:10pt">السطر التاني والتالت: نفس الزيادة بالظبط. و <code>&amp;player</code> = <code>&amp;player.x</code>، و y بعده بـ 4 و speed بعده بـ 4. العناوين هتختلف عندك.</p>'))
P.append(SB8.d8_player())
P.append('<h3>البرنامج 2: عداد بيحمي نفسه (private و this)</h3><p class="what">قبل ما تشغّل: توقّع العداد هيبقى كام بعد <code>Add(3)</code> و <code>Add(4)</code> و <code>Add(-100)</code>.</p>'
         + prog(SRC + 'p2_counter.cpp', 'counter.cpp') + res(term(rd(SRC + 'p2_counter.txt')) + '<p style="font-size:10pt">7 مش ‎-93: الكلاس رفض السالب. و <code>this</code> جوه الدالة = <code>&amp;clicks</code> مرة و <code>&amp;other</code> مرة.</p>'))
P.append('<h3 id="why-classes">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_player() + '<h3>البرنامج 2</h3>' + WHY.build_counter())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Class = قالب، و Object = نسخة في الرام حجمها = متغيراتها.</li>
 <li>الافتراضي <code>private</code>. <code>public:</code> عشان توصل من برّه.</li>
 <li>Method = دالة جوه الكلاس، بتشتغل على الـ Object اللي اتنادت عليه (<code>this</code>).</li>
 <li>المتغيرات مش بتبدأ بصفر لوحدها: حط قيمة قبل ما تستخدم.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. زوّد <code>void Print()</code> في Player تطبع x و y. 2. زوّد Method في Counter اسمها <code>Remove(int n)</code> ماتخليش العداد ينزل تحت 0. 3. اطبع <code>sizeof(Counter)</code> (لازم 4).</div></section>''')

# ================================================================== 2 · textures
t1n = {l.strip() for l in open(SRC + 't1_texture.cpp') if l.strip()} - {l.strip() for l in open('/home/claude/day7/src/r1_vertex_array.cpp') if l.strip()}
P.append(lec('l2', 'المحاضرة 2 · رسم', 'الـ Textures: النظرية', 'The Cherno · Textures in OpenGL · <span class="ltr">youtu.be/n4k7ANAFsIQ</span> · <span class="ltr">learnopengl.com/Getting-started/Textures</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Texture = صورة بنحمّلها على الكارت. كل ركن بيقول «أنا عند النقطة دي في الصورة» (u, v)، والكارت بيلوّن كل بكسل في النص من الصورة.</div>
<p class="what">البرنامج 1 كود The Cherno في ملف واحد: بنقرا صورة PNG بـ stb_image، ونبعتها للكارت، ونرسمها على مربع بشفافية. وعملنا كلاس صغير <code>Texture</code> زي The Cherno (من غير Constructor لسه). والبرنامج 2 بيرسم نفس الصورة الصغيرة 4 مرات بإعدادات مختلفة جنب بعض.</p>''')
P.append(D1.fig(D.t_uv(), 'كل ركن في المربع ليه نقطة في الصورة (u, v). الـ Texture في خانة (Slot)، والـ Shader بيعرف الخانة من <code>u_Texture</code>.'))
P.append(TEX_TABLE)
P.append('<h3 id="tex-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(TEX_WORDS))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD). وحط جنب الكود: <code>stb_image.h</code> (من <span class="ltr">github.com/nothings/stb</span>) وفولدر <code>res</code> فيه <code>logo.png</code>. الصورة اللي استخدمناها 128 × 128، فيها دايرة برتقاني وسهم لفوق ومربع أزرق فوق شمال، والباقي شفاف:</div>' + bigimg('logo_src', 'res/logo.png (الخلفية المربعات = شفاف)', '28mm'))
P.append('<h3>البرنامج 1: صورة على مربع (كود The Cherno)</h3><p class="what">السطور <b>بالأصفر</b> جديدة عن برنامج يوم السبت (vertex_array.cpp).</p>'
         + prog(SRC + 't1_texture.cpp', 'texture.cpp', new=t1n)
         + res(term(rd(SRC + 't1_texture.txt')) + bigimg('t1_texture', 'الصورة على المربع، والخلفية الزرقا باينة من الأماكن الشفافة. المربع اتمط لأن الشباك 640 × 480.'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(SB8.d8_texture())
P.append('<h3>البرنامج 2: الإعدادات الأربعة جنب بعض</h3><p class="what">صورة 4 × 4 بنعملها بإيدنا، في Textureين بإعدادات مختلفة، كل واحدة في خانة. والـ Shader بيضرب الإحداثيات في <code>u_Repeat</code>.</p>'
         + prog(SRC + 't2_settings.cpp', 'texture_settings.cpp')
         + res(term(rd(SRC + 't2_settings.txt')) + bigimg('t2_settings', 'فوق شمال: NEAREST (حاد). فوق يمين: LINEAR (ناعم). تحت شمال: REPEAT مع 0..2 (اتكررت). تحت يمين: CLAMP_TO_EDGE مع 0..2 (الحافة اتمدت).'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append('<h3 id="why-tex">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_texture() + '<h3>البرنامج 2</h3>' + WHY.build_settings())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>اقرا (stb_image) ← اعمل واربط ← 4 إعدادات ← <code>glTexImage2D</code> ← خانة ← <code>glUniform1i</code>.</li>
 <li>كل ركن ليه (u, v) من 0 لـ 1، و (0, 0) تحت شمال: عشان كده بنقلب الصورة.</li>
 <li>من غير MIN_FILTER: أسود من غير أي خطأ. ومن غير Blending: الشفاف أسود.</li>
 <li>NEAREST حاد و LINEAR ناعم. REPEAT بيكرر و CLAMP بيمد الحافة.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. حط صورة بتاعتك مكان logo.png. 2. خلّي الإحداثيات تروح لـ 3 في البرنامج 1 وغيّر WRAP لـ REPEAT. 3. ارسم الصورة مرتين: مرة بالخانة 0 ومرة بالخانة 1.</div></section>''')

# ================================================================== 3 · matrices
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'المصفوفات: المعنى', '3Blue1Brown · Linear transformations and matrices (فصل 3) · <span class="ltr">youtu.be/kYB8IZa5AuE</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> المصفوفة = وصف لتحويل الفراغ. عمودها الأول = المكان اللي î بيروحله، والتاني = المكان اللي ĵ بيروحله. واعرف دول، تعرف أي متجه بيروح فين.</div>
<p class="what">التحويل الخطي: الخطوط تفضل خطوط (ماتتنيش)، ونقطة الأصل (0, 0) ماتتحركش. البرنامج 1 بإيدنا من غير مكتبات: الضرب عمود عمود، ومثال الفيديو، والدوران، والقص، ومصفوفة بتكبس المستوى على خط. والبرنامج 2 نفس الكلام بـ NumPy، وبيرسم الشبكة قبل وبعد.</p>''')
P.append(D1.fig(D.m_columns(), 'مثال 3Blue1Brown: î بيروح (1, ‎-2) و ĵ بيروح (3, 0). فالمتجه (‎-1, 2) = ‎-1 مرة من الأول + 2 مرة من التاني = (5, 2).'))
P.append(MAT_TABLE)
P.append('<h3 id="mat-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(MAT_WORDS))
P.append('<h3>البرنامج 1: الأعمدة بإيدنا</h3><p class="what">احسب كل سطر في ورقة قبل ما تشغّل.</p>'
         + prog(SRC + 'm1_matrix_columns.py', 'matrix_columns.py') + res(term(rd(SRC + 'm1_matrix_columns.txt')) + '<p style="font-size:10pt">آخر 4 سطور: كل النتايج مضاعفات (2, 1). يعني المستوى كله اتكبس على خط واحد، لأن العمودين على نفس الخط.</p>'))
P.append('<h3>البرنامج 2: NumPy والشبكة</h3><p class="what">الشبكة الرمادي = خطوط الفراغ بعد التحويل. السهم الأخضر = î الجديد، والأحمر = ĵ الجديد.</p>'
         + prog(SRC + 'm2_numpy_grid.py', 'numpy_grid.py') + res(term(rd(SRC + 'm2_numpy_grid.txt')) + bigimg('m2_grids', 'الصورة اللي البرنامج حفظها (grids.png): الخطوط فضلت مستقيمة ومتوازية، والأصل مكانه.', '170mm')))
P.append('<h3 id="why-mat">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_matrix())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>المصفوفة = تحويل. العمود الأول = î′ والتاني = ĵ′.</li>
 <li>M v = x × العمود الأول + y × العمود التاني.</li>
 <li>في NumPy: <code>M @ v</code> (مش <code>*</code>). و <code>M[:, 0]</code> = العمود الأول.</li>
 <li>تحويلين ورا بعض = ضرب مصفوفتين، والترتيب بيفرق.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اكتب مصفوفة دوران 90 مع عقارب الساعة (î ← (0, ‎-1)) وجرّبها. 2. مصفوفة بتكبّر الضعف: [[2, 0], [0, 2]]. 3. ارسمها في البرنامج 2.</div></section>''')

# ================================================================== 4 · b-rep
P.append(lec('l4', 'المحاضرة 4 · CAD', 'الـ B-Rep: المفهوم', 'Ekeeda · Boundary Representation (B-Rep) · <span class="ltr">youtu.be/aafsBz50O-Q</span> · <span class="ltr">en.wikipedia.org/wiki/Boundary_representation</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ B-Rep (Boundary Representation) = بنوصف الجسم المصمت بحدوده: وشوش (Faces) حواليها أضلاع (Edges) في أطرافها أركان (Vertices). وده اللي برامج الـ CAD الحقيقية بتخزّنه.</div>
<p class="what">جزئين: <b>Geometry</b> = الأماكن (كل ركن فين)، و <b>Topology</b> = مين متوصل بمين (الوش ده حواليه أنهي أضلاع). البرنامج 1 بيعمل المكعب والهرم بكلاسات (زي المحاضرة 1) ويفحصهم بقانون أويلر وبعد الأضلاع المكشوفة. والبرنامج 2 بيرسم المكعب Wireframe من نفس الـ B-Rep.</p>''')
P.append(D1.fig(D.b_cube(), 'المكعب بأرقام الأركان (أزرق) والأضلاع (مربعات). الوش القدام = الأضلاع 0 و 9 و 4 و 8. نفس الإسقاط اللي في wireframe.cpp.'))
P.append(BREP_TABLE)
P.append('<h3 id="brep-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(BREP_WORDS))
P.append('<h3>البرنامج 1: المكعب والهرم وفحصهم</h3><p class="what">أويلر لجسم مقفول من غير خروم: F − E + V = 2. وكل ضلع لازم يبقى بين وشين بالظبط.</p>'
         + prog(SRC + 'c1_brep.cpp', 'brep.cpp') + res(term(rd(SRC + 'c1_brep.txt'))))
P.append(SB8.d8_brep())
P.append('<h3>البرنامج 2: من الـ B-Rep لـ Wireframe</h3><p class="what">نفس البيانات. قايمة الأضلاع بقت ترتيب رسم <code>GL_LINES</code> على طول، والوش القدام اترسم برتقاني من الأضلاع اللي حواليه.</p>'
         + prog(SRC + 'c2_wireframe.cpp', 'wireframe.cpp')
         + res(term(rd(SRC + 'c2_wireframe.txt')) + bigimg('c2_wireframe', 'الـ 12 ضلع خطوط رمادي، والـ 8 أركان نقط زرقا، والوش القدام برتقاني.'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append('<h3 id="why-brep">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_brep())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>B-Rep = Faces ← Edges ← Vertices، و Geometry + Topology.</li>
 <li>أويلر: F − E + V = 2 (مكعب 6 − 12 + 8، هرم 5 − 8 + 5).</li>
 <li>جسم مقفول = كل ضلع بين وشين. أويلر لوحده مش كفاية.</li>
 <li>B-Rep ← Wireframe سهل: الأضلاع = <code>GL_LINES</code>.</li>
 <li>قصاده الـ CSG (أشكال جاهزة بتتجمع وتتطرح): أصغر في التخزين، بس الـ B-Rep أسرع في الرسم وأنسب للأشكال المعقدة (Ekeeda).</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اعمل منشور تلاتي (Triangular prism): V = 6 و E = 9 و F = 5، واتأكد إن أويلر 2. 2. ارسمه في البرنامج 2. 3. غيّر الوش البرتقاني للوش اللي فوق (رقم 1).</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>الـ Classes:</b> استخدمناها في <code>Texture</code> (الصورة ورقمها ودوالها) وفي <code>Body</code> (الأركان والأضلاع والوشوش ودوال الفحص). كل حاجة في الـ CAD بعد كده هتبقى كلاس.</td></tr>
 <tr><td class="n">2</td><td><b>الـ Textures:</b> نفس فكرة الـ Buffer بس للصور: <code>glTexImage2D</code> زي <code>glBufferData</code>، والخانة زي الـ Uniform.</td></tr>
 <tr><td class="n">3</td><td><b>المصفوفات:</b> الإسقاط اللي عملناه بإيدنا في wireframe.cpp (x و y من x و y و z) هو تحويل. قريب هنكتبه مصفوفة ونبعته للـ Shader عشان نلف المكعب.</td></tr>
 <tr><td class="n">4</td><td><b>الـ B-Rep:</b> البيانات الحقيقية لأي جسم في الـ CAD، ومنها بنطلّع الـ Wireframe (والوشوش مثلثات بعدين).</td></tr>
</table>
<h3>بكره (الإتنين 2-11)</h3>
<ul><li>برمجة: Struct مقابل Class (The Cherno، الحلقة 19).</li><li>رسم: تحميل صورة بـ stb_image (Victor Gordan، OpenGL Tutorial 6).</li>
<li>رياضيات: التحويلات الخطية (Khan Academy).</li><li>الـ CAD: vertex و edge و face (Cem Yuksel، محاضرة 12).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>CLASSES in C++: <span class="ltr">youtube.com/watch?v=2BP8NhxjrO0</span></li>
 <li>Textures in OpenGL: <span class="ltr">youtube.com/watch?v=n4k7ANAFsIQ</span> · <span class="ltr">learnopengl.com/Getting-started/Textures</span> · <span class="ltr">github.com/nothings/stb</span></li>
 <li>Linear transformations and matrices: <span class="ltr">youtube.com/watch?v=kYB8IZa5AuE</span></li>
 <li>Boundary Representation (B-Rep): <span class="ltr">youtube.com/watch?v=aafsBz50O-Q</span> · <span class="ltr">en.wikipedia.org/wiki/Boundary_representation</span></li></ul></section>''')

css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q8.DAY8_CARDS, Q8.DAY8_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q8.DAY8_QA))
P = [Q.tag_reference(x) for x in P]
import linenums as LN
if MODE != 'web': P.append(STH.copy_appendix())
P = [JUMP.apply(''.join(P), LN, ART if MODE != 'web' else '')]
css += STH.CSS if MODE != 'web' else ''
css += LN.CSS + JUMP.CSS
if MODE == 'web':
    body = "".join(P)
    body = re.sub(r'src="(img/[^"]+\.png)"', lambda m: 'src="data:image/png;base64,' + base64.b64encode(open(m.group(1), 'rb').read()).decode() + '"', body)
    webcss = open('/home/claude/day1/web.css', encoding='utf-8').read()
    js = open('/home/claude/day1/web.js', encoding='utf-8').read()
    page = ('<title>محاضرات الأسبوع 3 · اليوم الأول</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week3_day1_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 3 - اليوم الأول</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week3_day1.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week3_day1.html', base_url='.').write_pdf('Week3_Day1_Sunday.pdf')
    import fixpdf; fixpdf.fix('Week3_Day1_Sunday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
