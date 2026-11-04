# Week 3 · Day 4 (Wednesday 4-11). Same structure as Week 2. MODE="web" builds the copy page; default builds the PDF.
import html, re, os, base64, sys
for d in ('day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 'day9', 'day10', 'day11'):
    sys.path.insert(0, f'/home/claude/{d}')
import weasyprint
import diagrams as D1
import diag11 as D
from data11 import E, OVER
from words11 import *
import why_day11 as WHY
import sb as SB
import sb11 as SB11
import quick as Q
import quick11 as Q11

os.chdir('/home/claude/day11')
MODE = globals().get('MODE', 'pdf')
ART = os.environ.get('ART_URL', '').strip()
css = open('final.css', encoding='utf-8').read()
exec(open('hl_src.py', encoding='utf-8').read())
KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4|struct|size_t|auto|enum|static|extern|mutable|private|using|namespace|import|as|def|continue|this|sampler2D|unsigned|delete|GLenum|GLint|long|double|try|except|while)\b'

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
STH.setup(['specs_d11'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثالث: الـ Classes والـ Textures</div>
  <h1>اليوم الرابع — الأربع 4 نوفمبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> Stack و Heap — <span style="color:#5b6372">The Cherno (الحلقة 54)</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> Texture wrapping والـ Texture Units — <span style="color:#5b6372">learnopengl و Cem Yuksel (محاضرة 14)</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> جمع وطرح المصفوفات — <span style="color:#5b6372">Khan Academy</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> مقارنة Mesh و B-Rep — <span style="color:#5b6372">Wikipedia و ProAnywhere</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:4mm;background:#fffbeb"><b>النهارده الأربعة مربوطين:</b> الصورة الكبيرة لازم على الـ Heap. وتكرار الـ Texture حساب بسيط على الإحداثيات. ونقل الشكل = جمع مصفوفات. والـ Mesh اللي الكارت بيرسمه تقريب للـ B-Rep.</div>
</section>''')

# ================================================================== 1 · stack vs heap
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'Stack و Heap', 'The Cherno · Stack vs Heap Memory in C++ (الحلقة 54) · <span class="ltr">youtu.be/wJ1L2nSIV1s</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الاتنين في الرام. الـ Stack صغير وسريع وبيترجع لوحده عند الـ <code>}</code>. والـ Heap كبير، بتحجز فيه بـ <code>new</code> وترجّع بـ <code>delete</code>، والحجز فيه أبطأ.</div>
<p class="what">The Cherno عمل نفس الحاجات مرتين: <code>int</code> و <code>int[5]</code> و <code>Vector3</code> على الـ Stack، وبعدين بـ <code>new</code> على الـ Heap، وفتح الـ Memory View وشاف الـ Stack لازق في بعض. البرنامج 1 بيطبع نفس الكلام بالعناوين والمسافات بدل الـ Memory View. والبرنامج 2 بيقيس السرعة، ويحجز صورة 16 MB في دالة وترجع حية لـ main.</p>''')
P.append(D1.fig(D.p_mem(), 'العناوين من التشغيل: الـ Stack لازق في بعض، وكل حاجة على الـ Heap بتاخد 32 بايت (الجزء الغامق = اللي إحنا طلبناه).'))
P.append(STACK_TABLE)
P.append('<h3 id="stack-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(STACK_WORDS))
P.append('<h3>البرنامج 1: نفس الحاجات على الـ Stack والـ Heap</h3><p class="what">قبل ما تشغّل: توقّع العناوين هتبدأ بإيه.</p>'
         + prog(SRC + 'p1_stack_heap.cpp', 'stack_heap.cpp') + res(term(rd(SRC + 'p1_stack_heap.txt')) + '<p style="font-size:10pt">العناوين بتتغير كل تشغيلة، بس المسافات لأ: 12 على الـ Stack (حجم Vector3 بالظبط) و 32 على الـ Heap. والـ ‎-52 معناها إن value تحت array بـ 52 بايت: الـ compiler بيرتّب متغيرات الـ Stack بطريقته، بس اللي ورا بعض بيفضلوا لازقين.</p>'))
P.append(SB11.d11_mem())
P.append('<h3>البرنامج 2: السرعة، وصورة 16 MB</h3><p class="what">توقّع: الـ Heap أبطأ كام مرة؟</p>'
         + prog(SRC + 'p2_speed_size.cpp', 'speed_size.cpp') + res(term(rd(SRC + 'p2_speed_size.txt')) + '<p style="font-size:10pt">مع عدد 100 بس الفرق صغير والأرقام بتتهز كل تشغيلة (أول اللفات أبطأ). جرّبنا مليون في «ليه كتبنا كل ده؟»: الـ Heap طلع أبطأ حوالي 5 مرات.</p>'))
P.append('<h3 id="why-stack">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_stack())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ Stack والـ Heap الاتنين في الرام.</li>
 <li>الـ Stack: حجز = تحريك الـ Stack Pointer، والحاجات لازقة في بعض، وبتموت عند الـ <code>}</code>.</li>
 <li>الـ Heap: <code>new</code> ← malloc بتدوّر في Free List وتسجّل. أبطأ، وكل حتة بتاخد أكتر من حجمها.</li>
 <li>كل <code>new</code> = <code>delete</code>، وكل <code>new[]</code> = <code>delete[]</code>.</li>
 <li>استخدم الـ Stack على قد ما تقدر، والـ Heap للحاجات الكبيرة أو اللي لازم تعيش بعد الدالة.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. غيّر N لمليون وشغّل 3 مرات. 2. شغّل <code>ulimit -s</code> في الـ Terminal: الـ Stack عندك كام؟ 3. زوّد في البرنامج 1 <code>double d = 1.5;</code> على الـ Stack واطبع عنوانه: قريب من مين؟</div></section>''')

# ================================================================== 2 · texture wrapping & units
P.append(lec('l2', 'المحاضرة 2 · رسم', 'Texture wrapping والـ Texture Units', 'learnopengl · Getting started: Textures · Cem Yuksel · Intro to Graphics 14 - Textures on the GPU · <span class="ltr">youtu.be/WULOKMqEGA0</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> التكرار (Wrapping) مش سحر: REPEAT = الجزء العشري، و MIRRORED = سنّة رايحة جاية، و CLAMP = قص. والـ Texture Unit هاردوير بيعمل الحسبة دي والفلترة لوحده، وعدده محدود.</div>
<p class="what">جربنا الأنواع الأربعة يوم 2 من الأسبوع ده. النهارده بنعمل اللي Cem Yuksel شرحه: البرنامج 1 بيرسم الصف اللي فوق والكارت بيكرر، والصف اللي تحت إحنا بنكرر بدالة Wrap في الـ Shader، ونقارن. والبرنامج 2 بيعمل رقعة الشطرنج اللي في المحاضرة كدالة (Procedural)، وجنبها نفس الرقعة من صورة 2 × 2 مكتوبة بإيدنا، ويسأل الكارت عن عدد الـ Texture Units.</p>''')
P.append(D1.fig(D.t_wrap(), 'الـ 3 معادلات اللي في دالة Wrap: الداخل u من ‎-1 لـ 2، والطالع الرقم اللي بيتقرا في الصورة (من 0 لـ 1).'))
P.append(WRAP_TABLE)
P.append('<h3 id="tex-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(TEX_WORDS))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD)، و <code>stb_image.h</code> و <code>stb.cpp</code> جنب الكود، وفولدر <code>res</code> فيه <code>letter.png</code> (حرف F، 8 × 8). الترجمة: <code>g++ wrap_by_hand.cpp stb.cpp</code> + المكتبات. والشباك بيتقفل بـ Esc.</div>' + bigimg('letter_src', 'res/letter.png مكبّرة: ركن أحمر تحت شمال وأخضر فوق يمين، عشان نعرف الاتجاه.', '28mm'))
P.append('<h3>البرنامج 1: الكارت فوق، وإحنا تحت</h3><p class="what">الصف اللي فوق: REPEAT ثم MIRRORED ثم CLAMP من الكارت. اللي تحت: نفس الحاجة بالحساب.</p>'
         + prog(SRC + 't1_wrap_by_hand.cpp', 'wrap_by_hand.cpp')
         + res(term(rd(SRC + 't1_wrap_by_hand.txt')) + bigimg('t1_wrap', 'الشباك الحقيقي: الصفين متطابقين. قارنّا البكسلات: عدد 0 بكسل مختلف من 72,384 في كل عمود.', '150mm'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append(SB11.d11_wrap())
P.append('<h3>البرنامج 2: رقعة شطرنج من دالة ومن صورة</h3><p class="what">نفس المستطيل مرتين، والإحداثيات من 0 لـ 4.</p>'
         + prog(SRC + 't2_procedural.cpp', 'procedural.cpp')
         + res(term(rd(SRC + 't2_procedural.txt')) + bigimg('t2_procedural', 'شمال: الدالة (0 بايت). يمين: الصورة 2 × 2 (12 بايت) والكارت بيكررها. نفس الشكل.', '110mm') + '<p style="font-size:10pt">llvmpipe كارت برمجي (الكارت اللي البرنامج اشتغل عليه عندنا). على كارتك الأرقام ممكن تختلف، بس المعيار بيضمن 16 خانة على الأقل.</p>', '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append('<h3 id="why-tex">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_wrap() + '<h3>البرنامج 2</h3>' + WHY.build_proc())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>REPEAT = <code>u - floor(u)</code>، و MIRRORED = <code>1 - |mod(u, 2) - 1|</code>، و CLAMP = <code>clamp(u, 0, 1)</code>.</li>
 <li>الـ Texture Unit بيعمل التكرار والفلترة في الهاردوير. واحنا بنختار بـ <code>glTexParameteri</code>.</li>
 <li>عدد الخانات: <code>glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS, …)</code>.</li>
 <li>Procedural Texture = دالة في الـ Shader بدل صورة.</li>
 <li>صورة من مصفوفة: لو الصف مش مضاعف 4 بايت، <code>glPixelStorei(GL_UNPACK_ALIGNMENT, 1)</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. في البرنامج 1 خلّي الإحداثيات من ‎-2 لـ 3. 2. اكتب في Wrap طريقة رابعة: REPEAT أفقي و CLAMP رأسي. 3. في البرنامج 2 غيّر الرقعة لـ 3 ألوان.</div></section>''')

# ================================================================== 3 · adding & subtracting matrices
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'جمع وطرح المصفوفات', 'Khan Academy · Adding &amp; subtracting matrices · <span class="ltr">youtu.be/AEqZYsZS6pI</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> نجمع أو نطرح المصفوفتين خانة خانة، بشرط إن المقاس واحد. الجمع الترتيب فيه مش مهم، والطرح الترتيب فيه مهم.</div>
<p class="what">البرنامج 1 بيعمل أمثلة Khan بالظبط: 2 × 3 + 2 × 3، وطرح 2 × 2 بطريقتين، و 3 × 2 + 2 × 2 = Undefined، ومعاهم دالة بتجمع بإيدنا خانة خانة. والبرنامج 2 تمرين في الرسم: نحرّك بيت (6 أركان) بجمع مصفوفة نقل، ونرجّعه بالطرح، ونعمل 4 فريمات. (محتاجين <code>pip install numpy matplotlib</code>)</p>''')
P.append(D1.fig(D.m_add(), 'مثال الفيديو: كل خانة مع اللي قصادها. الخانة الصفرا: 1 + 5 = 6.'))
P.append(MAT_TABLE)
P.append('<h3 id="mat-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(MAT_WORDS))
P.append('<h3>البرنامج 1: أمثلة Khan بالظبط</h3><p class="what">احسب A + B في ورقة الأول.</p>'
         + prog(SRC + 'm1_add_subtract.py', 'add_subtract.py') + res(term(rd(SRC + 'm1_add_subtract.txt')) + '<p style="font-size:10pt">نفس أرقام الفيديو. و D - C طلعت C - D بالسالب.</p>'))
P.append('<h3>البرنامج 2: تمرين: نحرّك بيت بالجمع</h3><p class="what">قبل التشغيل: السقف (1, 3) + (3, 1) = ؟</p>'
         + prog(SRC + 'm2_move_shape.py', 'move_shape.py') + res(term(rd(SRC + 'm2_move_shape.txt')) + bigimg('m2_moves', 'moves.png اللي البرنامج حفظها: البرتقاني الـ 4 فريمات (كل ما يغمق يتأخر)، والأزرق المتقطع البيت بعد ما السقف نزل.', '120mm')))
P.append('<h3 id="why-mat">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_mat())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الجمع والطرح: نفس المقاس، وخانة خانة.</li>
 <li>A + B = B + A، و A - B = A + (‎-1) B، و B - A = ‎-(A - B).</li>
 <li>المقاسات مختلفة = Undefined.</li>
 <li>NumPy بيجمع صف واحد مع مصفوفة (Broadcasting): مريح، بس مش جمع رياضيات.</li>
 <li>في الرسم: الأركان + مصفوفة نقل = الشكل اتحرك.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. احسب في ورقة [[2, ‎-1], [0, 4]] - [[‎-3, 1], [2, 2]] وقارن بالبرنامج. 2. خلّي البيت يتحرك 10 فريمات. 3. اعمل مصفوفة تحرّك الأرضية بس (الصف 0 و 1).</div></section>''')

# ================================================================== 4 · mesh vs B-Rep
P.append(lec('l4', 'المحاضرة 4 · CAD', 'مقارنة Mesh و B-Rep', '<span class="ltr">en.wikipedia.org/wiki/Polygon_mesh</span> · ProAnywhere · Polygon 3D Mesh Explained · <span class="ltr">youtu.be/IiAuqwAJMvo</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Mesh = أركان ووشوش مسطحة، وده اللي الكارت بيرسمه. وهو تقريب: الدايرة بتبقى مضلع. والـ B-Rep بتاع امبارح شايل السطح نفسه بمعادلته، فمظبوط.</div>
<p class="what">ProAnywhere كتب مكعب في ملف OBJ بالـ Notepad (سطور <code>v</code> للأركان و <code>f</code> للوشوش)، وقال إن ترتيب الأركان بيحدد الـ Normal. البرنامج 1 بيكتب نفس الملف، ويقراه تاني، ويحسب Normal كل وش ويتأكد إنه بيبص لبرّه. والبرنامج 2 بيبني أسطوانة امبارح كـ Mesh ويقارنها بالـ B-Rep: العدد، والحجم، والغلط.</p>''')
P.append(D1.fig(D.c_obj(), 'المكعب اللي في cube.obj بأرقام الأركان زي الفيديو. والقاع <code>f 1 4 3 2</code> طلع Normal بتاعه (0, 0, ‎-4) لتحت (من التشغيل).'))
P.append(CAD_TABLE)
P.append('<h3 id="cad-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CAD_WORDS))
P.append('<h3>البرنامج 1: مكعب ProAnywhere في ملف OBJ</h3><p class="what">بعد التشغيل افتح cube.obj بالـ Notepad، أو في Blender: File ← Import ← Wavefront (.obj).</p>'
         + prog(SRC + 'c1_obj_cube.cpp', 'obj_cube.cpp') + res(term(rd(SRC + 'c1_obj_cube.txt')) + '<p style="font-size:10pt">الـ ‎-0 في الوش 2 مش غلط: float عنده صفر بإشارة سالبة، وهو نفس الصفر. والوش 5 (<code>f 1 2 6 5</code>) هو اللي عند x = 1 (الـ Normal (4, 0, 0)).</p>'))
P.append('<h3>البرنامج 2: الأسطوانة Mesh مقابل B-Rep</h3><p class="what">توقّع: كام مثلث عشان أسطوانة 50 مم تبقى بدقة 0.01 مم؟</p>'
         + prog(SRC + 'c2_mesh_vs_brep.cpp', 'mesh_vs_brep.cpp') + res(term(rd(SRC + 'c2_mesh_vs_brep.txt'))))
P.append(D1.fig(D.c_mesh(), 'n = 8: الخط الأحمر هو الغلط بين الدايرة والمضلع. والجدول من التشغيل: كل ما n تكبر × 4، الغلط بيصغر حوالي 16 مرة.'))
P.append('<h3 id="why-cad">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_obj() + '<h3>البرنامج 2</h3>' + WHY.build_mesh())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ Mesh: أركان (x, y, z) + وشوش (أرقام أركان). وملف OBJ نص: <code>v</code> و <code>f</code>، والعد من 1.</li>
 <li>ترتيب أركان الوش = اتجاه الـ Normal (عكس عقارب الساعة = ناحيتك)، ومنه Back Face Culling.</li>
 <li>الـ Mesh تقريب: غلط الدايرة R (1 - cos(ط/n)). عشان تقلل الغلط محتاج مثلثات أكتر بكتير.</li>
 <li>الـ B-Rep مظبوط لأنه شايل المعادلة، وده اللي برامج CAD بتخزنه. والـ Mesh بيتعمل منه وقت الرسم أو التصدير (STL).</li>
 <li>V - E + F = 2 للاتنين لو الشكل مقفول.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. زوّد في cube.obj هرم فوق المكعب (ركن 9 و 4 وشوش). 2. اقلب وش في Blender وفعّل Face Orientation (الأزرق برّه والأحمر جوه). 3. في البرنامج 2 احسب n لدقة 0.001 مم.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>Stack و Heap:</b> الصورة اللي بنحمّلها للـ Texture (16 MB) لازم على الـ Heap، والـ Texture class بتاع امبارح بيرجّعها في الـ Destructor.</td></tr>
 <tr><td class="n">2</td><td><b>Texture wrapping:</b> التكرار حساب على الإحداثيات (الجزء العشري)، والكارت بيعمله في الهاردوير.</td></tr>
 <tr><td class="n">3</td><td><b>جمع المصفوفات:</b> نقل كل أركان الشكل مرة واحدة. وقريب هنعمله في الـ Vertex Shader.</td></tr>
 <tr><td class="n">4</td><td><b>Mesh و B-Rep:</b> الكارت بيرسم Mesh، والـ CAD بيخزن B-Rep، والتحويل بينهم فيه غلط بنتحكم فيه بعدد المثلثات.</td></tr>
</table>
<h3>بكره (الخميس 5-11)</h3>
<ul><li>برمجة: new و delete (The Cherno: The NEW Keyword in C++).</li><li>رسم: Texture filtering (learnopengl).</li>
<li>رياضيات: NumPy والمصفوفات (مراجعة).</li><li>الـ CAD: Mortenson: فصل التمثيل.</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>Stack vs Heap Memory in C++: <span class="ltr">youtube.com/watch?v=wJ1L2nSIV1s</span></li>
 <li>learnopengl Textures: <span class="ltr">learnopengl.com/Getting-started/Textures</span> · Intro to Graphics 14 - Textures on the GPU: <span class="ltr">youtube.com/watch?v=WULOKMqEGA0</span></li>
 <li>Adding &amp; subtracting matrices: <span class="ltr">youtube.com/watch?v=AEqZYsZS6pI</span> · <span class="ltr">khanacademy.org/math/linear-algebra/matrix-transformations</span></li>
 <li>Polygon mesh: <span class="ltr">en.wikipedia.org/wiki/Polygon_mesh</span> · Polygon 3D Mesh Explained: <span class="ltr">youtube.com/watch?v=IiAuqwAJMvo</span></li></ul></section>''')
css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q11.DAY11_CARDS, Q11.DAY11_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q11.DAY11_QA))
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
    page = ('<title>محاضرات الأسبوع 3 · اليوم الرابع</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week3_day4_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 3 - اليوم الرابع</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week3_day4.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week3_day4.html', base_url='.').write_pdf('Week3_Day4_Wednesday.pdf')
    import fixpdf; fixpdf.fix('Week3_Day4_Wednesday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
