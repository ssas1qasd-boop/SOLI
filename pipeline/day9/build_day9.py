# Week 3 · Day 2 (Monday 2-11). Same structure as Week 2. MODE="web" builds the copy page; default builds the PDF.
import html, re, os, base64, sys
for d in ('day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 'day9'):
    sys.path.insert(0, f'/home/claude/{d}')
import weasyprint
import diagrams as D1
import diag9 as D
from data9 import E, OVER
from words9 import *
import why_day9 as WHY
import sb as SB
import sb9 as SB9
import quick as Q
import quick9 as Q9

os.chdir('/home/claude/day9')
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
STH.setup(['specs_d9'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثالث: الـ Classes والـ Textures</div>
  <h1>اليوم التاني — الإتنين 2 نوفمبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> Class مقابل Struct — <span style="color:#5b6372">The Cherno (الحلقة 19)</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> تحميل صورة بـ stb_image — <span style="color:#5b6372">Victor Gordan و Sean Barrett</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> التحويلات الخطية — <span style="color:#5b6372">Khan Academy</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> vertex و edge و face — <span style="color:#5b6372">Cem Yuksel (محاضرة 12) و Wikipedia</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:4mm;background:#fffbeb"><b>النهارده الأربعة مربوطين:</b> الـ struct هو الركن (Vertex)، والركن بيشيل إحداثيات الـ Texture، والإسقاط بتاع امبارح طلع تحويل خطي، والمثلث بيلوّن البكسلات بالـ Barycentric.</div>
  <div class="howto" style="margin-top:4mm"><b>برامج الـ Texture</b> محتاجة <code>stb_image.h</code> و <code>stb.cpp</code> وفولدر <code>res</code> جنبها (كله في ملف الكود المضغوط). وبرنامج الإسقاط محتاج <code>pip install numpy matplotlib</code>.</div>
</section>''')

# ================================================================== 1 · struct vs class
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'Class مقابل Struct', 'The Cherno · CLASSES vs STRUCTS in C++ (الحلقة 19) · <span class="ltr">youtu.be/fLgTtaqqJp0</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> مفيش فرق تقريباً. الـ struct كل حاجة فيه <code>public</code> لوحدها، والـ class كل حاجة فيه <code>private</code> لوحدها. والـ struct موجود في C++ عشان الكود المكتوب بلغة C يفضل شغال (The Cherno).</div>
<p class="what">البرنامج 1 بيكتب لاعب امبارح مرتين: مرة struct ومرة class، ويوري إن النتيجة والحجم واحد. وبعدين <code>Vec2</code> مثال The Cherno للـ struct: «بيانات بسيطة» (POD = Plain Old Data). والبرنامج 2 بيوري ليه الـ struct مهم في الرسم: ركن الـ Texture كـ struct، وحجمه هو الـ stride.</p>''')
P.append(D1.fig(D.s_visibility(), 'نفس المتغيرات ونفس الدالة. الفرق في الكلمة اللي بتتكتب لوحدها لو ماكتبناش حاجة. والحجم 12 بايت في الاتنين (من التشغيل).'))
P.append(STRUCT_TABLE)
P.append('<h3 id="struct-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(STRUCT_WORDS))
P.append('<h3>البرنامج 1: نفس اللاعب بـ struct و class</h3><p class="what">قبل ما تشغّل: توقّع الـ <code>sizeof</code> بتاع الاتنين.</p>'
         + prog(SRC + 'p1_struct_class.cpp', 'struct_class.cpp') + res(term(rd(SRC + 'p1_struct_class.txt')) + '<p style="font-size:10pt">نفس الأرقام ونفس الحجم. و Vec2 = رقمين float = 8 بايت.</p>'))
P.append(SB9.d9_struct())
P.append('<h3>البرنامج 2: الركن struct (اللي بنبعته للكارت)</h3><p class="what">نفس مربع امبارح (x و y و u و v)، بس كل ركن struct ليه أسماء بدل 16 رقم ورا بعض.</p>'
         + prog(SRC + 'p2_vertex_struct.cpp', 'vertex_struct.cpp') + res(term(rd(SRC + 'p2_vertex_struct.txt')) + '<p style="font-size:10pt">16 = الـ stride، و 8 = الـ offset بتاع u، و 64 = الحجم اللي <code>glBufferData</code> بينسخه. والرقم رقم 10 في الصف هو نفسه <code>square[2].u</code>.</p>'))
P.append(D1.fig(D.v_layout(), 'الـ 4 أركان في الرام: 16 رقم float ورا بعض. كل ركن 16 بايت، و u بيبدأ بعد 8. الكارت مش شايف الأسماء، شايف البايتات بس.'))
P.append('<h3 id="why-struct">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_struct() + '<h3>البرنامج 2</h3>' + WHY.build_vertex())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>struct = class، بس الافتراضي <code>public</code>.</li>
 <li>الاتنين فيهم متغيرات ودوال ونفس الحجم.</li>
 <li>The Cherno: struct للبيانات البسيطة، و class للحاجات الكبيرة اللي فيها منطق. وماتورّثش struct من class (Inheritance) لأن بعض الـ compilers بتطلّع تحذير.</li>
 <li><code>sizeof</code> الركن = الـ stride، و <code>offsetof</code> = الـ offset.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. زوّد في Vec2 دالة <code>Scale(float k)</code>. 2. اعمل <code>struct Color { float r, g, b; };</code> واطبع حجمه (لازم 12). 3. زوّد z في Vertex وشوف الـ stride والـ offset بتاع u بقوا كام.</div></section>''')

# ================================================================== 2 · stb_image (Victor Gordan)
P.append(lec('l2', 'المحاضرة 2 · رسم', 'تحميل صورة بـ stb_image', 'Victor Gordan · OpenGL Tutorial 6 - Textures · <span class="ltr">youtu.be/u-00hjlfMKc</span> · Sean Barrett · <span class="ltr">github.com/nothings/stb</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> نفس اللي عملناه امبارح بطريقة Victor Gordan: صورة Pixel Art صغيرة، و Mipmaps (نسخ مصغّرة)، و NEAREST عشان المربعات تفضل حادة، والأنواع الأربعة للتكرار (WRAP).</div>
<p class="what">مكتبة stb_image بتاعة Sean Barrett ملف واحد (<code>stb_image.h</code>). بنحط الكود بتاعها في ملف لوحده (<code>stb.cpp</code>)، وأي ملف تاني يعمل <code>#include</code> للتعريفات بس. البرنامج 1 بيرسم قطة 16 × 16 على مستطيل. والبرنامج 2 بيعمل 4 Textures من صورة السهم بتاعة امبارح، كل واحدة بنوع WRAP، وبيوسّع الإحداثيات لحد ‎-0.5 و 1.5 عشان نشوف اللي برّه الصورة.</p>''')
P.append(D1.fig(D.t_pipeline(), 'الصورة من الملف لحد الكارت: 1024 بايت في الرام، ثم المستوى 0 في الكارت، ثم النسخ المصغّرة 8 و 4 و 2 و 1.'))
P.append(TEX_TABLE)
P.append('<h3 id="tex-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(TEX_WORDS))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD). وحط جنب الكود <code>stb_image.h</code> و <code>stb.cpp</code> (تحت)، وفولدر <code>res</code> فيه <code>pixel_cat.png</code> (16 × 16، الخلفية شفافة) و <code>logo.png</code> بتاعة امبارح. وفي الترجمة لازم الملفين: <code>g++ pixel_cat.cpp stb.cpp …</code>.</div>' + bigimg('pixel_cat_src', 'res/pixel_cat.png مكبّرة (الخلفية المربعات = شفاف)', '28mm'))
P.append('<h3>stb.cpp: كود المكتبة في ملف لوحده</h3>' + prog(SRC + 'stb.cpp', 'stb.cpp'))
P.append('<h3>البرنامج 1: قطة Pixel Art (أسلوب Victor Gordan)</h3><p class="what">الأركان 5 أرقام (x و y و z و u و v)، و EBO، و Mipmaps.</p>'
         + prog(SRC + 't1_pixel_cat.cpp', 'pixel_cat.cpp')
         + res(term(rd(SRC + 't1_pixel_cat.txt')) + bigimg('t1_pixel_cat', 'القطة بمربعات حادة (NEAREST)، والخلفية الكحلي باينة من الأماكن الشفافة.'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(SB9.d9_texture())
P.append('<h3>البرنامج 2: الأنواع الأربعة للتكرار (WRAP)</h3><p class="what">صورة واحدة في 4 Textures. كل مربع بيقرا من ‎-0.5 لـ 1.5، فالنص هو الصورة، واللي حواليها بيقرره WRAP.</p>'
         + prog(SRC + 't2_wrap_modes.cpp', 'wrap_modes.cpp')
         + res(term(rd(SRC + 't2_wrap_modes.txt')) + bigimg('t2_wrap_modes', 'فوق شمال: REPEAT. فوق يمين: MIRRORED_REPEAT (معكوسة). تحت شمال: CLAMP_TO_EDGE (الحافة الشفافة اتمدت). تحت يمين: CLAMP_TO_BORDER (أحمر).'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(D1.fig(D.t_wrap(), 'الإحداثيات من ‎-0.5 لـ 1.5: المربع البرتقاني هو الصورة (0..1)، والحلقة الرمادي برّه الصورة، ولونها حسب WRAP.'))
P.append('<h3 id="why-tex">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_cat() + '<h3>البرنامج 2</h3>' + WHY.build_wrap())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>stb_image: <code>#define STB_IMAGE_IMPLEMENTATION</code> في ملف واحد بس (<code>stb.cpp</code>).</li>
 <li><code>stbi_load(…, 0)</code> = زي الملف، فـ <code>glTexImage2D</code> لازم يطابق عدد القنوات.</li>
 <li>MIPMAP في MIN_FILTER محتاج <code>glGenerateMipmap</code>، وإلا أسود.</li>
 <li>NEAREST للـ Pixel Art، و LINEAR للصور العادية.</li>
 <li>WRAP: REPEAT و MIRRORED_REPEAT و CLAMP_TO_EDGE و CLAMP_TO_BORDER (+ <code>glTexParameterfv</code> للون).</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. ارسم Pixel Art بتاعتك 8 × 8 في أي برنامج رسم وحطها مكان القطة. 2. صغّر المستطيل لـ 0.1 وجرّب <code>GL_LINEAR_MIPMAP_LINEAR</code>. 3. غيّر لون الحدود لأخضر.</div></section>''')

# ================================================================== 3 · transformations
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'التحويلات الخطية', 'Khan Academy · Vector transformations · <span class="ltr">youtu.be/gAbadNuQEjI</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الدالة بتربط حاجة من مجموعة بحاجة في مجموعة تانية. ولما الحاجات دي متجهات، اسمها «تحويل» (Transformation) ونكتبها <bdi dir="ltr">T: ℝⁿ → ℝᵐ</bdi>: داخل n رقم وطالع m رقم.</div>
<p class="what"><b>ℝⁿ</b> (تتقري R n) = كل المتجهات اللي فيها n رقم حقيقي: ℝ² = (x, y) و ℝ³ = (x, y, z). البرنامج 1 بيكتب مثال Khan بالظبط كدالة Python، وبعدين نفس الدالة كمصفوفة 2 × 3، وتحويل تاني مش خطي للمقارنة. والبرنامج 2 بياخد الإسقاط بتاع المكعب من امبارح ويكتبه مصفوفة بـ NumPy: طلع تحويل من ℝ³ لـ ℝ².</p>''')
P.append(D1.fig(D.m_mapping(), 'مثال Khan: كل متجه في ℝ³ بيروح لمتجه في ℝ². والمصفوفة A بتعمل نفس الشغل: صفين (رقمين طالعين) و 3 أعمدة (3 داخلين).'))
P.append(TRANS_TABLE)
P.append('<h3 id="trans-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(TRANS_WORDS))
P.append('<h3>البرنامج 1: مثال Khan بالظبط</h3><p class="what">احسب T(1, 1, 1) و T(2, 4, 1) في ورقة الأول.</p>'
         + prog(SRC + 'm1_transform.py', 'transform.py') + res(term(rd(SRC + 'm1_transform.txt')) + '<p style="font-size:10pt">الدالة والمصفوفة نفس النتيجة في التلاتة. و S مش خطي: الصفر راح (0, 1)، والضعف مش بيدّي ضعف.</p>'))
P.append('<h3>البرنامج 2: إسقاط المكعب مصفوفة</h3><p class="what">في <code>wireframe.cpp</code> امبارح حسبنا x و y على الشاشة بمعادلة. هنا نفس المعادلة مصفوفة P مقاسها 2 × 3.</p>'
         + prog(SRC + 'm2_projection.py', 'projection.py') + res(term(rd(SRC + 'm2_projection.txt')) + bigimg('m2_projection', 'projection.png اللي البرنامج حفظها: نفس المكعب بتاع امبارح.', '80mm')))
P.append('<h3 id="why-trans">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_transform())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>التحويل = دالة على المتجهات: <bdi dir="ltr">T: ℝⁿ → ℝᵐ</bdi>.</li>
 <li>T(x₁, x₂, x₃) = (x₁ + 2x₂, 3x₃): ‏(1, 1, 1) ← (3, 3) و (2, 4, 1) ← (10, 3).</li>
 <li>التحويل الخطي ممكن يتكتب مصفوفة m × n.</li>
 <li>الخطي: الأصل مايتحركش، و T(a + b) = T(a) + T(b).</li>
 <li>استخدامه في الألعاب: لف، تكبير، تحريك الكاميرا، والإسقاط على الشاشة.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اكتب T(x, y) = (2x, x + y) كدالة ومصفوفة 2 × 2. 2. جرّب T(x, y) = (x + 1, y): خطي؟ 3. غيّر P في البرنامج 2 لـ [[1, 0, 0], [0, 0, 1]] (منظر من قدام) وشوف الصورة.</div></section>''')

# ================================================================== 4 · triangular meshes
P.append(lec('l4', 'المحاضرة 4 · CAD', 'vertex و edge و face: الشبكات المثلثية', 'Cem Yuksel · Lecture 12: Triangular Meshes · <span class="ltr">youtu.be/HV2dKIQcp6k</span> · <span class="ltr">en.wikipedia.org/wiki/Polygon_mesh</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> أي سطح بنرسمه = مثلثات. 3 نقط دايماً على مستوى واحد، فالمثلث دايماً مسطح. وأي نقطة على المثلث = خليط من أركانه التلاتة بالأوزان α و β و γ (Barycentric)، ومجموعهم 1.</div>
<p class="what">الـ Mesh = أركان (Vertices) + أضلاع (Edges) + وشوش (Faces). أحسن طريقة نخزّنها: الأركان مرة واحدة، وكل مثلث 3 أرقام (Indexed Face List). البرنامج 1 بيعمل مكعب امبارح من 12 مثلث، ويقارن المساحة، ويعد الأضلاع، ويحسب α و β و γ لأربع نقط. والبرنامج 2 بيرسم مثلث أحمر وأخضر وأزرق، ويحسب لون بكسلات بإيدنا ويقارنه باللي الكارت رسمه.</p>''')
P.append(D1.fig(D.c_indexed(), 'المكعب بطريقتين (من التشغيل): 432 بايت لو كل مثلث شايل أركانه، و 240 لو بالأرقام. وكل ضلع داخلي مشترك بين مثلثين.'))
P.append(D1.fig(D.c_bary(), 'المثلث (0,0) و (4,0) و (0,4) والنقطة (1,1): المثلث اللي قصاد كل ركن، ومساحته ÷ الكل = وزن الركن ده.'))
P.append(MESH_TABLE)
P.append('<h3 id="mesh-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(MESH_WORDS))
P.append('<h3>البرنامج 1: المكعب مثلثات و Barycentric</h3><p class="what">توقّع: المكعب فيه كام ضلع لما يبقى مثلثات؟</p>'
         + prog(SRC + 'c1_mesh.cpp', 'mesh.cpp') + res(term(rd(SRC + 'c1_mesh.txt'))))
P.append(SB9.d9_mesh())
P.append('<h3>البرنامج 2: الكارت بيلوّن بالـ Barycentric</h3><p class="what">نفس الحساب بتاع البرنامج 1 بإحداثيات الشاشة، وبعدين <code>glReadPixels</code> بيقرا اللون اللي الكارت رسمه.</p>'
         + prog(SRC + 'c2_barycentric.cpp', 'barycentric.cpp')
         + res(term(rd(SRC + 'c2_barycentric.txt')) + bigimg('c2_barycentric', 'كل بكسل لونه = α أحمر + β أخضر + γ أزرق. وحسابنا طابق الكارت في البكسلين اللي جوه.'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append('<h3 id="why-mesh">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_mesh() + '<h3>البرنامج 2</h3>' + WHY.build_bary())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Mesh = Vertices + Edges + Faces، وفي الرسم الوشوش مثلثات.</li>
 <li>المثلث دايماً مسطح. الشكل الرباعي ممكن ركنه الرابع يطلع برّه المستوى.</li>
 <li>Indexed Face List = الأركان مرة واحدة + أرقام (زي الـ EBO).</li>
 <li>P = αP₀ + βP₁ + γP₂، والمجموع 1. سالبة = برّه.</li>
 <li>الكارت بيحسب α و β و γ لكل بكسل ويخلط بيها أي حاجة: لون، إحداثيات Texture، إلخ.</li>
 <li>الفنانين بيرسموا بأشكال رباعية (Quads) لأنها أسهل في التعديل، وقبل الرسم بتتحول لمثلثات (Cem Yuksel).</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اعمل الهرم بتاع امبارح مثلثات (القاعدة مثلثين): V و E و F كام؟ 2. اسأل <code>Barycentric(0, 2)</code> و <code>Barycentric(-1, 1)</code>. 3. في البرنامج 2 اقرا بكسل قريب من الركن الأخضر.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>struct:</b> الركن (<code>Vertex</code> و <code>Corner</code>) والمثلث (<code>Triangle</code>) كلهم struct بسيط. وحجمه هو الـ stride اللي بنكتبه لـ OpenGL.</td></tr>
 <tr><td class="n">2</td><td><b>stb_image:</b> كل ركن بيشيل (u, v)، والكارت بيخلطها لكل بكسل بنفس الـ Barycentric بتاع المحاضرة 4.</td></tr>
 <tr><td class="n">3</td><td><b>التحويلات:</b> الإسقاط بتاع المكعب طلع مصفوفة 2 × 3. والخطوة الجاية نكتبها في الـ Shader.</td></tr>
 <tr><td class="n">4</td><td><b>الشبكات المثلثية:</b> نفس المكعب بتاع الـ B-Rep اتقسم 12 مثلث، وأويلر لسه 2.</td></tr>
</table>
<h3>بكره (التلات 3-11)</h3>
<ul><li>برمجة: Constructors و Destructors (The Cherno، الحلقة 25 و 26).</li><li>رسم: Texture على مستطيل (learnopengl، و Cem Yuksel محاضرة 13: Textures).</li>
<li>رياضيات: تمارين Khan: التحويلات الخطية كضرب مصفوفة في متجه.</li><li>الـ CAD: رسم مخطط B-Rep بإيدك (Wikipedia).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>CLASSES vs STRUCTS in C++: <span class="ltr">youtube.com/watch?v=fLgTtaqqJp0</span></li>
 <li>OpenGL Tutorial 6 - Textures: <span class="ltr">youtube.com/watch?v=u-00hjlfMKc</span> · <span class="ltr">github.com/nothings/stb</span></li>
 <li>Vector transformations: <span class="ltr">youtube.com/watch?v=gAbadNuQEjI</span></li>
 <li>Lecture 12: Triangular Meshes: <span class="ltr">youtube.com/watch?v=HV2dKIQcp6k</span> · <span class="ltr">en.wikipedia.org/wiki/Polygon_mesh</span></li></ul></section>''')

css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q9.DAY9_CARDS, Q9.DAY9_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q9.DAY9_QA))
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
    page = ('<title>محاضرات الأسبوع 3 · اليوم الثاني</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week3_day2_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 3 - اليوم الثاني</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week3_day2.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week3_day2.html', base_url='.').write_pdf('Week3_Day2_Monday.pdf')
    import fixpdf; fixpdf.fix('Week3_Day2_Monday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
