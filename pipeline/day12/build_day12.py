# Week 3 · Day 5 (Thursday 5-11). Same structure as Week 2. MODE="web" builds the copy page; default builds the PDF.
import html, re, os, base64, sys
for d in ('day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 'day9', 'day10', 'day11', 'day12'):
    sys.path.insert(0, f'/home/claude/{d}')
import weasyprint
import diagrams as D1
import diag12 as D
from data12 import E, OVER
from words12 import *
import why_day12 as WHY
import sb as SB
import sb12 as SB12
import quick as Q
import quick12 as Q12

os.chdir('/home/claude/day12')
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
STH.setup(['specs_d12'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثالث: الـ Classes والـ Textures</div>
  <h1>اليوم الخامس — الخميس 5 نوفمبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> كلمة new — <span style="color:#5b6372">The Cherno (The NEW Keyword in C++)</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> Texture filtering: الـ Mipmaps والـ Anisotropy — <span style="color:#5b6372">learnopengl وفيديو Mipmaps and Anisotropic Filtering</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> NumPy والمصفوفات (مراجعة) — <span style="color:#5b6372">NumPy docs و Keith Galli</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> التمثيل: Wireframe و Surface و Solid — <span style="color:#5b6372">Mortenson و Dr. Suyog Patil</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:4mm;background:#fffbeb"><b>النهارده الأربعة مربوطين:</b> <code>new</code> بتحجز وتنادي الـ Constructor. والـ Mipmaps نسخ أصغر بنحجزها للصورة (ثلث زيادة). و NumPy بيورّينا الأحجام بالبايت ويضرب المصفوفات. والـ Solid هو التمثيل الوحيد اللي يعرف الحجم.</div>
</section>''')

# ================================================================== 1 · new
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'كلمة new', 'The Cherno · The NEW Keyword in C++ · <span class="ltr">youtu.be/NUZdUSqsCs4</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> <code>new</code> = تحجز مكان على الـ Heap (بتنادي <code>malloc</code>) + تنادي الـ Constructor. و <code>delete</code> = تنادي الـ Destructor + ترجّع المكان (<code>free</code>).</div>
<p class="what">The Cherno قال إن <code>new</code> Operator عادي، وإن اللي بيفرّقها عن <code>malloc</code> هو الـ Constructor، وذكر Placement new في الآخر. البرنامج 1 بيكتب <code>operator new</code> بنفسه عشان يطبع كل <code>new</code> طلبت كام بايت، ويقارن بـ <code>malloc</code>. والبرنامج 2 بيعمل Placement new: Constructor على ذاكرة محجوزة قبل كده.</p>''')
P.append(D1.fig(D.p_new(), 'الطرق التلاتة، و <code>new Entity[3]</code> بالأحجام اللي طلعت من التشغيل: 8 بايت للعدد + 3 × 32.'))
P.append(NEW_TABLE)
P.append('<h3 id="new-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(NEW_WORDS))
P.append('<h3>البرنامج 1: new بتطلب كام بايت؟</h3><p class="what">قبل ما تشغّل: توقّع <code>new Entity[3]</code> هتطلب كام.</p>'
         + prog(SRC + 'p1_new.cpp', 'new_operator.cpp') + res(term(rd(SRC + 'p1_new.txt')) + '<p style="font-size:10pt">sizeof(Entity) = 32 لأن جواه <code>std::string</code> واحد (حجمه 32 هنا). والـ 104 = 3 × 32 + 8: الـ compiler بيطلب 8 زيادة لأن الـ Entity عنده Destructor (بتاع الـ string)، فلازم يفتكر العدد.</p>'))
P.append(SB12.d12_new())
P.append('<h3>البرنامج 2: Placement new</h3><p class="what">توقّع: عنوان v هيبقى قد إيه من b؟</p>'
         + prog(SRC + 'p2_placement.cpp', 'placement_new.cpp') + res(term(rd(SRC + 'p2_placement.txt')) + '<p style="font-size:10pt">العناوين بتتغير كل تشغيلة، بس v = b دايماً. و h في عنوان تاني لأن <code>new</code> العادية حجزت مكان جديد.</p>'))
P.append(SB12.d12_place())
P.append('<h3 id="why-new">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_new() + '<h3>البرنامج 2</h3>' + WHY.build_place())
P.append('''<div class="sum"><b>الملخص:</b><ul><li><code>new T()</code> = malloc(sizeof(T)) + Constructor. و <code>delete</code> = Destructor + free.</li>
 <li><code>malloc</code> مابتنادي Constructor، فـ C++ بتستخدم <code>new</code>.</li>
 <li><code>new T[n]</code> ممكن تطلب أكتر من n × sizeof(T): العدد بيتحفظ قبل المصفوفة لـ <code>delete[]</code>.</li>
 <li>اللي بـ <code>new[]</code> يترجع بـ <code>delete[]</code>، واللي بـ malloc بـ free.</li>
 <li>Placement new: <code>new (address) T(...)</code>، ومعاها Destructor بإيدك بس.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. زوّد في Entity متغير <code>int age;</code> واتوقّع sizeof قبل ما تشغّل. 2. اعمل <code>new int[3]</code>: فيه 8 زيادة؟ (int مالوش Destructor). 3. في البرنامج 2 حط Vector3 تاني عند <code>b + 3</code>.</div></section>''')

# ================================================================== 2 · mipmaps & anisotropic filtering
P.append(lec('l2', 'المحاضرة 2 · رسم', 'Texture filtering: الـ Mipmaps والـ Anisotropy', 'learnopengl · Getting started: Textures (Texture filtering و Mipmaps) · Mipmaps and Anisotropic Filtering · <span class="ltr">youtu.be/q-M2iTIY7Tk</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> لما الصورة تتصغّر (أرضية بعيدة)، بكسل الشاشة بيغطي بكسلات كتير من الصورة. الـ Mipmaps نسخ أصغر جاهزة يقرا منها، والـ Anisotropy بياخد عينات أكتر لما الزاوية حادة.</div>
<p class="what">جربنا NEAREST و LINEAR يوم 2 من الأسبوع ده على صورة <b>بتتكبر</b>. النهارده الصورة <b>بتتصغّر</b>. الفيديو مافيهوش كلام: بيورّي أرضية شطرنج بتبعد، ويقارن الفلاتر (0:19)، ويورّي إن الـ Mipmap لوحده بيخلّي البعيد رمادي في الزوايا الحادة (0:47)، وإن الـ Anisotropic بيصلّحها (1:20)، وفي الآخر فلاتر التكبير (2:13). البرنامج 1 بيعمل نفس الأرضية بـ 4 فلاتر. والبرنامج 2 بيلوّن كل مستوى بلون عشان نشوف الكارت بيقرا من أنهي واحد.</p>''')
P.append(D1.fig(D.t_mip(), 'المستويات التسعة بالمقاسات اللي الكارت طبعها، وبالألوان اللي حطيناها في البرنامج 2.'))
P.append(D1.fig(D.t_aniso(), 'ليه الـ Mipmap لوحده بيبقى رمادي: البكسل البعيد بيغطي حتة طويلة رفيعة.'))
P.append(MIP_TABLE)
P.append('<h3 id="mip-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(MIP_WORDS))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD). مفيش صور: الرقعة والألوان بنعملهم في الكود. الترجمة: <code>g++ mipmaps.cpp</code> + المكتبات. والشباك بيتقفل بـ Esc.</div>')
P.append('<h3>البرنامج 1: أرضية بـ 4 فلاتر</h3><p class="what">فوق: NEAREST و LINEAR. تحت: Trilinear، و Trilinear + Anisotropy 16.</p>'
         + prog(SRC + 't1_mipmaps.cpp', 'mipmaps.cpp')
         + res(term(rd(SRC + 't1_mipmaps.txt')) + bigimg('t1_mipmaps', 'الشباك الحقيقي. قسنا التباين (الانحراف المعياري للرمادي) في الحتة البعيدة: NEAREST عدد 110 و LINEAR عدد 106 (تموّج)، و Trilinear عدد 32 (رمادي)، ومع Anisotropy عدد 57 (المربعات لسه باينة).', '150mm'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append('<h3>البرنامج 2: كل مستوى بلون</h3><p class="what">توقّع: الأرضية القريبة هتبقى لون أنهي مستوى؟</p>'
         + prog(SRC + 't2_mip_levels.cpp', 'mip_levels.cpp')
         + res(term(rd(SRC + 't2_mip_levels.txt')) + bigimg('t2_mip_levels', 'شمال من غير Anisotropy: القريب برتقاني (المستوى 1) وبعدين أصفر وأخضر لحد البنفسجي. يمين مع 16: الأحمر (المستوى 0) ظهر، وكل لون اتزق لبعيد.', '150mm') + '<p style="font-size:10pt">llvmpipe كارت برمجي (اللي البرنامج اشتغل عليه عندنا). على كارتك الحدود بين الألوان ممكن تتحرك شوية، بس الترتيب نفسه.</p>', '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append(SB12.d12_mip())
P.append('<h3 id="why-mip">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_mip() + '<h3>البرنامج 2</h3>' + WHY.build_levels())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>التصغير (MIN): NEAREST و LINEAR بيقروا من الأصل فبيعملوا Moiré.</li>
 <li>الـ Mipmaps: <code>glGenerateMipmap</code> بيعمل 256 ← 128 ← … ← 1، والكل 1.333 × الأصل.</li>
 <li><code>LINEAR_MIPMAP_LINEAR</code> = Trilinear: LINEAR في مستويين وخلط بينهم.</li>
 <li>الـ Mipmap للـ MIN بس. الـ MAG = NEAREST (حاد) أو LINEAR (ناعم).</li>
 <li>فلتر MIPMAP ومستويات ناقصة = Texture أسود.</li>
 <li><code>GL_TEXTURE_MAX_ANISOTROPY</code> (لحد 16) للأرضيات والزوايا الحادة.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. في البرنامج 1 خلّي الـ Anisotropy 2 و 4 و 8 وقارن. 2. خلّي الرقعة 512 بدل 256: كام مستوى؟ 3. في البرنامج 2 غيّر الفلتر لـ <code>GL_LINEAR_MIPMAP_LINEAR</code>: الحدود بين الألوان بقت إيه؟</div></section>''')

# ================================================================== 3 · numpy
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'NumPy والمصفوفات (مراجعة)', '<span class="ltr">numpy.org/doc/stable/user/absolute_beginners.html</span> · Keith Galli · Complete Python NumPy Tutorial · <span class="ltr">youtu.be/GB9ByFAIAH4</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> مصفوفة NumPy = بايتات ورا بعض بنوع واحد (زي مصفوفة C++). منها بناخد خانة أو صف أو عمود أو حتة، ونعمل حساب على الكل مرة واحدة.</div>
<p class="what">استخدمنا NumPy قبل كده في الجمع والطرح. النهارده مراجعة اللي Keith Galli عمله في الفيديو: البرنامج 1 الأبعاد والنوع والحجم بالبايت، والوصول للخانات، وتمرينه (5 × 5)، ونسخ المصفوفة. والبرنامج 2 العمليات، وضرب المصفوفات (<code>matmul</code>)، والإحصاء، وتغيير الشكل، والفلترة.</p>''')
P.append(D1.fig(D.m_slice(), 'مصفوفة Keith (2 × 7): الأصفر خانة، والتيل عمود، والأزرق حتة بخطوة 2.'))
P.append(NP_TABLE)
P.append('<h3 id="np-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(NP_WORDS))
P.append('<h3>البرنامج 1: المصفوفة نفسها</h3><p class="what">قبل التشغيل: <code>m[0, 1:6:2]</code> = ؟</p>'
         + prog(SRC + 'm1_numpy_arrays.py', 'numpy_arrays.py') + res(term(rd(SRC + 'm1_numpy_arrays.txt'))))
P.append('<h3>البرنامج 2: الحساب</h3><p class="what">احسب في ورقة: خانة واحدة من <code>matmul(ones, twos)</code>.</p>'
         + prog(SRC + 'm2_numpy_math.py', 'numpy_math.py') + res(term(rd(SRC + 'm2_numpy_math.txt')) + '<p style="font-size:10pt">reshape (2, 3) اترفض والبرنامج ماوقفش لأننا مسكنا الغلط بـ <code>try</code> و <code>except</code>.</p>'))
P.append('<h3 id="why-np">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_np())
P.append('''<div class="sum"><b>الملخص:</b><ul><li><code>shape</code> و <code>ndim</code> و <code>dtype</code> و <code>itemsize</code> و <code>nbytes</code>.</li>
 <li><code>m[i, j]</code> و <code>m[i, :]</code> و <code>m[:, j]</code> و <code>m[0, 1:6:2]</code>، والسالب من الآخر.</li>
 <li><code>y = x</code> اسم تاني، و <code>copy()</code> نسخة.</li>
 <li><code>+ - * **</code> خانة خانة، و <code>np.matmul</code> ضرب مصفوفات (الداخلي لازم يتساوى).</li>
 <li><code>min</code> و <code>max</code> و <code>sum</code> مع <code>axis</code>، و <code>reshape</code> بنفس العدد، و <code>vstack</code> و <code>hstack</code>، و <code>a[a &gt; 50]</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اعمل تمرين Keith التاني: 6 × 5 فيها 1 لـ 30، وهات منها [[11, 12], [16, 17]]. 2. اعمل مصفوفة float32: itemsize كام؟ 3. اضرب 3 × 2 في 2 × 4: النتيجة مقاسها إيه؟</div></section>''')

# ================================================================== 4 · CAD representation
P.append(lec('l4', 'المحاضرة 4 · CAD', 'التمثيل: Wireframe و Surface و Solid', 'Mortenson · Geometric Modeling (فصل التمثيل) · Dr. Suyog Patil · Geometric Modelling in CAD · <span class="ltr">youtu.be/aG4ex0ANCJM</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> نفس الشكل ممكن يتخزن 3 طرق: خطوط (Wireframe)، أو وشوش (Surface)، أو جسم مقفول يعرف جوه وبرّه (Solid). وكل ما التمثيل يكمل، تقدر تسأله أسئلة أكتر.</div>
<p class="what">Dr. Patil بدأ بالتمثيل البارامتري: x = R sinθ، و y = R cosθ، و z = H، وورّى إن نفس المعادلة بتدي نقطة أو دايرة أو أسطوانة أو جسم حسب كام بارامتر بيتغير. وبعدين قارن الـ Wireframe والـ Surface والـ Solid. البرنامج 1 بيعمل جدول البارامترات. والبرنامج 2 بيبني نفس المكعب بالطرق التلاتة ويسأل كل واحد عن الطول والمساحة والحجم.</p>''')
P.append(D1.fig(D.c_param(), 'جدول Dr. Patil: نفس المعادلة، والفرق في عدد البارامترات الحرة. عدد النقط من التشغيل.'))
P.append(D1.fig(D.c_three(), 'نفس المكعب (ضلعه 2) بالطرق التلاتة، والأرقام من التشغيل.'))
P.append(CAD_TABLE)
P.append('<h3 id="cad-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CAD_WORDS))
P.append('<h3>البرنامج 1: البارامترات الحرة</h3><p class="what">توقّع: R من 0 لـ 10 و θ بس حرين: الشكل إيه؟</p>'
         + prog(SRC + 'c1_parametric.cpp', 'parametric.cpp') + res(term(rd(SRC + 'c1_parametric.txt')) + '<p style="font-size:10pt">max r = 10 في كل الأشكال: ولا نقطة عدّت نص القطر. وعدد النقط 3 أُس عدد البارامترات الحرة (3 عينات لكل واحد).</p>'))
P.append('<h3>البرنامج 2: المكعب 3 مرات</h3><p class="what">توقّع: أنهي تمثيل هيعرف الحجم؟</p>'
         + prog(SRC + 'c2_three_models.cpp', 'three_models.cpp') + res(term(rd(SRC + 'c2_three_models.txt')) + '<p style="font-size:10pt">الحجم من 8 خلايا × 1 = 8 = 2³ بالظبط لأن المكعب ماشي مع حدود الخلايا. في شكل مدوّر لازم خلايا أصغر عشان الرقم يقرب.</p>'))
P.append('<h3 id="why-cad">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_cad())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Parametric: كل إحداثي دالة في بارامترات. الأسطوانة: x = R sinθ، و y = R cosθ، و z = H.</li>
 <li>عدد البارامترات الحرة: 0 نقطة، 1 منحنى، 2 سطح، 3 جسم.</li>
 <li>Wireframe = أركان وخطوط: خفيف، بس غامض ومايعرفش مساحة ولا حجم.</li>
 <li>Surface = وشوش: مساحة وشكل للرسم، بس مايعرفش الجوه.</li>
 <li>Solid = جوه وبرّه: حجم وكتلة ومركز ثقل. ده اللي برامج CAD بتعمله (B-Rep مقفول أو CSG).</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. في البرنامج 1 زوّد مخروط: R من 0 لـ 10 بيتغير مع H (لازم تعدّل At). 2. في البرنامج 2 خلّي الخلايا 0.5: الحجم لسه 8؟ 3. اكتب Inside لكرة نص قطرها 1 واحسب حجمها بالخلايا.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>new:</b> حجز + Constructor. والـ <code>std::vector</code> اللي شايل بكسلات الـ Texture بيعمل <code>new[]</code> و <code>delete[]</code> لوحده.</td></tr>
 <tr><td class="n">2</td><td><b>Mipmaps:</b> ذاكرة زيادة (الثلث) عشان الرسم البعيد يبقى نضيف، والـ Anisotropy عينات أكتر في الزوايا الحادة.</td></tr>
 <tr><td class="n">3</td><td><b>NumPy:</b> nbytes زي sizeof، و matmul هو الضرب اللي هنستخدمه في التحويلات بكره.</td></tr>
 <tr><td class="n">4</td><td><b>التمثيل:</b> الكارت بيرسم وشوش (Surface)، لكن الـ CAD محتاج Solid عشان يعرف الحجم.</td></tr>
</table>
<h3>بكره (الجمعة 6-11)</h3>
<ul><li>برمجة: عمر الـ Object (cppreference و The Cherno: Object Lifetime in C++).</li><li>رسم: Textures (learnopengl و Basic OpenGL Textures Explained).</li>
<li>رياضيات: Matrix transformations (Khan Academy).</li><li>الـ CAD: Solid modeling و CSG (Wikipedia و Constructive Solid Geometry - Friday Minis 142).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>The NEW Keyword in C++: <span class="ltr">youtube.com/watch?v=NUZdUSqsCs4</span></li>
 <li>learnopengl Textures: <span class="ltr">learnopengl.com/Getting-started/Textures</span> · Mipmaps and Anisotropic Filtering: <span class="ltr">youtube.com/watch?v=q-M2iTIY7Tk</span></li>
 <li>NumPy absolute beginners: <span class="ltr">numpy.org/doc/stable/user/absolute_beginners.html</span> · Complete Python NumPy Tutorial: <span class="ltr">youtube.com/watch?v=GB9ByFAIAH4</span></li>
 <li>Mortenson · Geometric Modeling · Geometric Modelling in CAD: <span class="ltr">youtube.com/watch?v=aG4ex0ANCJM</span></li></ul></section>''')
css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q12.DAY12_CARDS, Q12.DAY12_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q12.DAY12_QA))
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
    page = ('<title>محاضرات الأسبوع 3 · اليوم الخامس</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week3_day5_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 3 - اليوم الخامس</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week3_day5.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week3_day5.html', base_url='.').write_pdf('Week3_Day5_Thursday.pdf')
    import fixpdf; fixpdf.fix('Week3_Day5_Thursday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
