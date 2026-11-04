# v4: every code is a complete program you can type and run; diagrams for every idea; real run result under each code.
exec(open('build.py', encoding='utf-8').read().split('# ============================================================== content')[0])
from full_data2 import E as EX
import diagrams as D, os, base64
from words import UNIFORM_WORDS, CAMERA_WORDS, TYPES_TABLE
import why as WHY
import why2 as WHY2
import sys as _sb; _sb.path.insert(0, '/home/claude/day2'); import sb as SB
MODE = globals().get('MODE', 'pdf')
ART = os.environ.get('ART_URL', '').strip()

css += WHY.CSS + SB.CSS + '''
.fig { margin:3mm 0 4mm; page-break-inside:avoid; background:#fbfcfe; border:1px solid #e6e9ef; border-radius:3mm; padding:3mm 3mm 2mm; }
.figcap { font-size:9.5pt; color:#5b6372; text-align:center; margin-top:1mm; }
table.cl tr.new td.e { background:#fef9c3; }
table.cl tr.new td.k { box-shadow: inset 4px 0 0 #eab308; }
.what { font-size:10pt; color:#374151; margin:0 0 2mm; }
.copylink { font-size:9.5pt; color:#2563eb; text-decoration:none; margin-right:3mm; font-weight:bold; }
.wline { margin:0 0 4mm; page-break-inside:avoid; }
.wcode { direction:ltr; text-align:left; background:#141a26; color:#e6e9ef; border-radius:2mm 2mm 0 0; padding:1.8mm 3mm; font-size:9pt; }
.chips { direction:ltr; display:flex; flex-wrap:wrap; gap:1.5mm; padding:2mm; background:#f5f7fb; border:1px solid #e2e6ee; border-top:0; border-radius:0 0 2mm 2mm; }
.chip { border:1px solid #c9d1de; background:#fff; border-radius:1.5mm; min-width:18mm; max-width:48mm; flex:0 1 auto; }
.chip .tok { background:#e8ecf3; text-align:center; padding:0.8mm 2mm; font-size:9pt; font-weight:bold; color:#1e3a8a; border-bottom:1px solid #c9d1de; }
.chip .mean { direction:rtl; text-align:center; padding:1mm 2mm; font-size:9pt; line-height:1.45; }
.wnote { font-size:9.5pt; color:#374151; background:#fffbeb; border-right:3px solid #f59e0b; padding:1.5mm 3mm; margin-top:1.5mm; }
table.types { width:100%; border-collapse:collapse; margin:2mm 0 4mm; font-size:10pt; page-break-inside:avoid; }
table.types th { background:#e8ecf3; padding:1.5mm 2.5mm; text-align:right; }
table.types td { border-bottom:1px solid #e2e6ee; padding:1.5mm 2.5mm; }
.setup { background:#f5f3ff; border-radius:3mm; padding:3.5mm 5mm; margin:3mm 0 4mm; font-size:10pt; }
'''

def prog(path, label, new=None):
    """Complete file: every non-empty line + its explanation. Lines in `new` get a yellow highlight."""
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
        e = EX[t.strip()]
        if isnew: e = '<b>★ جديد:</b> ' + e
        e, _rid = JUMP.mark(e, t, label, lnum)
        h.append(f'<tr{cls}{_rid}><td class="k"><i class="ln">{lnum}</i>{hl(t)}</td><td class="e">{e}</td></tr>')
    h.append('</table>')
    return ''.join(h)

def lec(cls, tag, title, meta):
    return f'<section class="lec {cls}"><div class="lec-head"><div class="tag">{tag}</div><h2>{title}</h2><div class="meta">{meta}</div></div>'

import sys as _sh; _sh.path.insert(0, '/home/claude/steps'); _sh.path.insert(0, '/home/claude/steps')
import steps_hook as STH
import jumps as JUMP
STH.setup(['specs_d1'], MODE, hl)
P = STH.PList()
# ------------------------------------------------------------------ cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثاني: المؤشرات والـ Shaders</div>
  <h1>اليوم الأول — الأحد 25 أكتوبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> المؤشرات (Pointers) في C++ — <span style="color:#5b6372">The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> الـ Uniforms في OpenGL — <span style="color:#5b6372">The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> الضرب النقطي (Dot product) — <span style="color:#5b6372">3Blue1Brown</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> الماوس وكلاس الكاميرا — <span style="color:#5b6372">Victor Gordan</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه 3 حاجات:</b>
    <b>1.</b> رسمة بتوضح الفكرة. <b>2.</b> البرنامج كامل، وكل سطر جنبه شرحه. <b>3.</b> مربع أخضر فيه اللي ظهر على الشاشة لما شغّلناه فعلاً.</div>
  <div class="howto" style="margin-top:5mm;background:#fffbeb"><b>على Windows (Visual Studio) الشكل هيختلف شوية:</b>
    العناوين بتتطبع من غير <code>0x</code> (زي <code>000000A1B2C3D4E0</code>)، والصفر بيتطبع <code>0000000000000000</code>. وأرقام العناوين بتتغير كل مرة تشغّل. ده كله طبيعي.</div>
</section>''')

# ------------------------------------------------------------------ 1 POINTERS
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'المؤشرات (Pointers) في C++', 'قناة The Cherno · حلقة 16 · <span class="ltr">youtu.be/DTxHyVn0ODg</span>'))
P.append('<div class="idea"><b>الفكرة في سطر:</b> الـ Pointer ورقة مكتوب عليها <b>عنوان</b> مكان في الذاكرة. مش الحاجة نفسها، ده عنوانها بس.</div>')
P.append(D.fig(D.p_street(), 'الذاكرة شارع طويل، وكل بيت = بايت وعليه رقم (عنوان). المتغير <code>var</code> ساكن في البيت <code>0x1000</code>، والـ Pointer ورقة مكتوب عليها الرقم ده.'))
P.append('<table class="grid2"><tr><td><b>علامة &amp;</b><br>«هات رقم البيت» (العنوان).</td><td><b>النجمة قبل الاسم</b><br>«روح البيت ده» واقرا أو غيّر اللي جواه.</td></tr></table>')

pcodes = [
 ('كود 1: Pointer فاضي', 'Pointer قيمته صفر يعني مش بيشاور على أي بيت.', D.p_null(), 'الـ Pointer الفاضي ورقة مكتوب عليها 0: مفيش بيت بالرقم ده، فلو رحت تقرا البرنامج هيقفل.',
  'التلات طرق طلعوا نفس الحاجة: صفر.'),
 ('كود 2: هات عنوان متغير بعلامة &amp;', 'بناخد عنوان متغير ونحطه في Pointer.', D.p_addr(), 'المتغير <code>var</code> جواه 8، و <code>ptr</code> جواه عنوانه.',
  '<code>&amp;var</code> و <code>ptr</code> نفس الرقم بالظبط.'),
 ('كود 3: النوع مش بيغيّر العنوان', 'نفس العنوان بنوعين مختلفين.', D.p_types(), 'الاتنين بيبدأوا من نفس البيت. الفرق إن <code>int*</code> بيقرا 4 بيوت و <code>double*</code> بيقرا 8.',
  'نفس العنوان، والفرق الوحيد حجم اللي هيتقرا: 4 أو 8 بايت.'),
 ('كود 4: روح العنوان وغيّر اللي جواه', 'بنغيّر قيمة متغير من غير ما نكتب اسمه، عن طريق عنوانه.', D.p_deref(), 'النجمة بتخلّي الـ Pointer «يروح» للبيت ويغيّر اللي جواه من 8 لـ 10.',
  'القيمة بقت 10 مع إن السطر اللي غيّرها ما فيهوش اسم <code>var</code>.'),
 ('كود 5: احجز ذاكرة بنفسك (Heap)', 'بنطلب 8 بايت جداد بـ <code>new</code>، ونرجّعهم بـ <code>delete[]</code>.', D.p_heap(), 'المتغيرات العادية في الـ Stack. اللي بتحجزه بـ <code>new</code> بيتعمل في مكان تاني اسمه الـ Heap، والـ Pointer هو الحبل اللي بيوصّلك له.',
  'العنوان بيبدأ بـ <code>0x55…</code> (الـ Heap)، مش <code>0x7ffe…</code> (الـ Stack). والـ 8 بايت كلهم أصفار.'),
 ('كود 6: Pointer شايل عنوان Pointer', 'نجمتين = عنوان لعنوان.', D.p_chain(), 'السلسلة: <code>ptr</code> ← <code>buffer</code> ← البيانات. كل نجمة = خطوة.',
  '<code>ptr</code> = عنوان <code>buffer</code>، و <code>*ptr</code> = اللي جوه <code>buffer</code>، و <code>(*ptr)[0]</code> = البيانات نفسها (0).'),
]
for i, (h, what, sv, cap, after) in enumerate(pcodes, 1):
    P.append(f'<h3>{h}</h3><p class="what">{what}</p>' + D.fig(sv, cap) + prog(f'full/p/p{i}.cpp', f'p{i}.cpp')
             + res(term(rd(f'full/p/p{i}.txt')) + f'<p style="font-size:10pt">{after}</p>'))
    if i in (4, 5, 6):
        P.append({4: SB.d1_deref, 5: SB.d1_heap, 6: SB.d1_chain}[i]())
P.append('<h3 id="why-cpp">ليه كتبنا كل ده؟ الهدف من كل خطوة</h3>'
  '<p class="what">هنا <b>ليه</b> كتبنا كل حاجة في البرامج الست، وهي <b>إجبارية ولا لأ</b>، و<b>إيه اللي يحصل لو شيلتها</b>. وفي غلطات الذاكرة استخدمنا أداة جوه g++ اسمها <b>AddressSanitizer</b>: بتمسك الغلطة لحظة ما تحصل وتقولك اسمها. (تقدر تشغّلها في Visual Studio كمان: Project Properties ← C/C++ ← Enable Address Sanitizer)</p>'
  + '<div class="legend"><span class="badge b-req">إجباري</span> = من غيره مش هيشتغل · <span class="badge b-imp">مش إجباري، بس مهم جداً</span> = هيشتغل، بس هتتعب · <span class="badge b-opt">اختياري</span> = تحسين أو مثال</div>'
  + '<div class="warn" style="font-size:10pt"><b>⚠️ لاحظ:</b> فيه غلطات الـ compiler بيمسكها (أحمر في Visual Studio)، وغلطات بتعدّي من الترجمة عادي وتظهر وإنت بتشغّل بس. التانية أخطر.</div>'
  + WHY2.build_cpp())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ Pointer = عنوان.</li><li>علامة <code>&amp;</code> = هات العنوان، والنجمة = روح للعنوان.</li>
 <li>القيمة <code>nullptr</code> = عنوان فاضي، ماتلمسهوش.</li><li>كل <code>new</code> لازم يقابلها <code>delete</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> في كود 4 غيّر <code>*ptr = 10;</code> لـ <code>*ptr = *ptr * 3;</code>. هيطبع كام؟</div></section>''')

# ------------------------------------------------------------------ 2 UNIFORMS
u1 = {l.strip() for l in open('full/u/u1.cpp') if l.strip()}
u2new = {l.strip() for l in open('full/u/u2.cpp') if l.strip()} - u1
P.append(lec('l2', 'المحاضرة 2 · رسم', 'الـ Uniforms في OpenGL', 'قناة The Cherno · سلسلة OpenGL · <span class="ltr">youtu.be/DE6Xlx_kbo0</span>'))
P.append('<div class="idea"><b>الفكرة في سطر:</b> الـ Uniform «خانة» جوه الـ Shader (اللي شغال على كارت الشاشة)، وإحنا بنملاها من كود الـ C++.</div>')
P.append(D.fig(D.u_flow(), 'الـ C++ بيبعت 4 أرقام بـ <code>glUniform4f</code> ← بيتحطوا في خانة <code>u_Color</code> جوه الـ Shader ← كل بكسل بياخد اللون ده.'))
P.append(D.fig(D.u_attr(), 'الـ Attribute: كل ركن ليه قيمته (فبيطلع تدرّج). الـ Uniform: قيمة واحدة لكل الأركان (لون واحد).'))
P.append('''<div class="setup"><b>قبل ما تشغّل:</b> البرنامج محتاج GLFW و GLAD متركبين في المشروع زي ما عملت في الأسبوع الأول (learnopengl: Hello Window). ضيف ملف <code>glad.c</code> للمشروع.
الشكل نفس فكرة The Cherno، بس هو بيستخدم GLEW وبيقرا الـ Shader من ملف؛ هنا GLAD والـ Shader مكتوب جوه الكود عشان الملف يبقى واحد.</div>''')
P.append('<h3 id="glsl">قبل الكود: كلمات الـ Shader كلمة كلمة</h3>'
  '<p class="what">الـ Shader مكتوب بلغة تانية اسمها <b>GLSL</b>، شبه C++ بس فيها كلمات جديدة. أهمهم <code>vec4</code>.</p>'
  + D.fig(D.u_vec4(), '<code>vec4</code> = علبة فيها 4 أرقام عشرية. لو مكان: x, y, z, w. لو لون: r, g, b, a (أحمر، أخضر، أزرق، شفافية). وتقدر توصل لكل رقم بالنقطة: <code>.x</code> أو <code>.r</code>.')
  + TYPES_TABLE
  + D.fig(D.u_slot(), 'إحنا بنبعت من الـ C++ رقمين بس لكل ركن، بيدخلوا الخانة 0، والـ Shader بيستلمهم كـ <code>vec4</code>. الرقمين الناقصين بيتملوا لوحدهم: z = 0 و w = 1.')
  + D.fig(D.u_screen(), 'الشاشة في OpenGL من ‎-1 لـ +1 في الاتجاهين، والنص هو (0, 0). عشان كده المربع اللي أركانه ±0.5 بياخد نص الشاشة.')
  + '<h3>كل سطر في الـ Shader، كلمة كلمة</h3>' + ''.join(UNIFORM_WORDS))
P.append('<h3>البرنامج 1: مربع بلون ثابت (كود 1 + 2 + 3 مع بعض)</h3><p class="what">الـ Shader لوحده مش بيشتغل، محتاج برنامج يفتح شباك ويرسم. ده أصغر برنامج كامل فيه: تعريف الخانة، وجيب رقمها، وابعتلها لون.</p><p class="what" style="color:#0f766e">عايز تعرف <b>ليه</b> كتبنا كل خطوة، وهي إجبارية ولا لأ؟ شوف قسم «ليه كتبنا كل ده؟» بعد البرنامج 2.</p>'
         + prog('full/u/u1.cpp', 'uniform_fixed.cpp')
         + res(term(rd('full/u/u1.txt')) + '<img src="img/full_u1fixed.png" style="width:80mm;display:block;margin:2mm auto;border-radius:2mm">'
               + '<p style="font-size:10pt">الشباك فيه مربع أزرق ثابت. والـ Terminal: الاسم الصح رقمه 0، والاسم الغلط ‎-1.</p>'))
P.append('<h3>البرنامج 2: لون بيتغير لوحده (Animation)</h3><p class="what">نفس البرنامج 1 بالظبط، والسطور المتعلّمة <b>بالأصفر</b> هي بس اللي اتغيرت. انسخه كله وشغّله.</p>'
         + D.fig(D.u_wave(), 'قيمة الأحمر <code>r</code> مع الوقت: بتطلع لحد 1 فتنزل، وتوصل 0 فتطلع. والمربع بيتنقل بين أزرق ووردي.')
         + prog('full/u/u2.cpp', 'uniform_animation.cpp', new=u2new)
         + res(term(rd('full/out2.txt')) + grid([shot(f'full_u{i}', f'لقطة {i}') for i in range(1, 7)] + ['<td></td>', '<td></td>'], 4)
               + '<p style="font-size:10pt">لقطات من الشباك الحقيقي وهو شغال، كل واحدة بعد حوالي 0.12 ثانية.</p>', '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(SB.d1_gpu())
P.append('<h3 id="why">ليه كتبنا كل ده؟ الهدف من كل خطوة</h3>'
  '<p class="what">جدول الكود فوق بيقولك كل سطر <b>بيعمل إيه</b>. هنا بنقولك <b>ليه</b> كتبناه، وهو <b>إجباري ولا لأ</b>، و<b>إيه اللي يحصل لو شيلته</b>. واللي عليه «✓ جربناها فعلاً» شيلنا السطر ده من البرنامج وشغّلناه، والنتيجة اللي قدامك حقيقية.</p>'
  + D.fig(D.w_three_mains(), '<b>ليه 3 دوال main؟</b> هما 3 برامج منفصلين: واحد C++ على المعالج بيشتغل مرة، واتنين على كارت الشاشة. والاسم <code>main</code> مش اختيار: هو قاعدة في اللغتين إن البداية اسمها كده.')
  + D.fig(D.w_timeline(), '<b>شكل أي برنامج OpenGL:</b> تجهيز مرة واحدة، بعدها لوب بيرسم كل فريم، وفي الآخر تنضيف. أي سطر في البرنامج بيقع في واحدة من التلاتة دول.')
  + '<div class="legend"><span class="badge b-req">إجباري</span> = من غيره البرنامج مش هيرسم أو مش هيشتغل · <span class="badge b-imp">مش إجباري، بس مهم جداً</span> = هيشتغل، بس هتتعب · <span class="badge b-opt">اختياري</span> = تحسين أو مثال</div>'
  + '<div class="warn" style="font-size:10pt"><b>⚠️ لاحظ:</b> كل البرامج المكسورة في التجارب دي اتعملها compile <b>من غير ولا خطأ</b>. يعني الـ compiler مش هيقولك إنك نسيت خطوة؛ هتشوف شاشة سودا بس. عشان كده لازم تعرف كل خطوة بتعمل إيه.</div>'
  + WHY.build(rd))
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ Uniform = خانة في الـ Shader بنملاها من الـ C++.</li>
 <li>الخطوات: عرّفها، هات رقمها، ابعت القيمة.</li><li>لازم <code>glUseProgram</code> الأول، والرقم ‎-1 = مش لاقيها.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> في البرنامج 2 خلي الأخضر هو اللي بيتغير بدل الأحمر.</div></section>''')

# ------------------------------------------------------------------ 3 DOT
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'الضرب النقطي (Dot product)', 'قناة 3Blue1Brown · فصل 9 · <span class="ltr">youtu.be/LyGKycYT2v0</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> بتاخد متجهين وتطلّع رقم واحد، بيقولك هما «متفقين في الاتجاه» قد إيه.</div>
<h3>الحساب: اضرب المتقابلين واجمع</h3>
<div class="formula">[1, 2] · [3, 4] = 1×3 + 2×4 = <b>11</b></div>
<div class="formula">[6, 2, 8, 3] · [1, 8, 5, 3] = 6 + 16 + 40 + 9 = <b>71</b></div>
''' + SB.d1_dot() + '<h3>المعنى: الضل</h3>')
P.append(D.fig(D.d_proj(), 'نوّر كشاف على <b>w</b> فيقع ضله على خط <b>v</b>. طول الضل × طول <b>v</b> = الضرب النقطي.'))
P.append(D.fig(D.d_signs(), 'الإشارة بتقولك العلاقة: موجب = نفس الناحية، صفر = متعامدين (مفيش ضل)، سالب = عكس بعض.'))
P.append('<h3>الفكرة العميقة (الازدواجية) بكلمتين</h3><p>أي متجه تقدر تشوفه كـ <b>سهم</b>، أو كـ <b>آلة</b> بتاخد أي متجه وتطلّع رقم، والرقم ده هو الضرب النقطي معاه.</p>')
P.append(D.fig(D.d_machine(), 'المتجه [1, −2] كآلة: دخّلت [4, 3] طلع ‎-2. ودي نفسها حسبة المصفوفة <code>[1 −2]</code> × <code>[4, 3]</code>.'))
P.append('<p>ولو المتجه طوله 1، الضرب النقطي معاه = طول الضل بالظبط. عشان كده بنستخدم <code>normalize</code> كتير في الجرافيكس.</p>')
P.append('<h3>الكود: نحسب الأمثلة دي بالكمبيوتر</h3><p class="what">برنامج كامل. محتاج مكتبة GLM بس (هتركبها في الأسبوع 4، أو امسح سطور <code>glm</code> لو لسه مش متركبة).</p>'
         + prog('full/3_dot/main.cpp', 'dot.cpp') + res(term(rd('full/out3.txt')) + '<p style="font-size:10pt">نفس أرقام الفيديو: 11 و 71. والإشارة: موجب ثم صفر ثم سالب.</p>'))
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الحساب: اضرب المتقابلين واجمع.</li><li>المعنى: الضل × الطول. والإشارة بتقول نفس الاتجاه ولا عكسه ولا متعامدين.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> ضيف للبرنامج سطر يحسب <code>[3, 4] · [4, −3]</code>. طلع صفر؟ يبقى العلاقة إيه؟</div></section>''')

# ------------------------------------------------------------------ 4 CAMERA
P.append(lec('l4', 'المحاضرة 4 · CAD', 'الماوس وكلاس الكاميرا', 'قناة Victor Gordan · OpenGL Tutorial 8 · <span class="ltr">youtu.be/86_pQCKOIPk</span>'))
P.append('<div class="idea"><b>الفكرة في سطر:</b> الكاميرا = 3 حاجات: <b>إنت فين</b> (Position)، <b>بتبص فين</b> (Orientation)، و<b>فين فوق</b> (Up). الكيبورد بيحرّكك، والماوس بيلف راسك.</div>')
P.append(D.fig(D.c_vectors(), 'الـ 3 متجهات، ومنهم بنطلّع رابع: «اليمين» = الضرب الاتجاهي (cross) بين اتجاه النظر وفوق.'))
P.append('''<div class="setup"><b>الكاميرا مش برنامج ملف واحد:</b> الكلاسات متقسمة على <b>5 ملفات</b>، ومش هتشتغل غير لما تحطهم كلهم في <b>نفس المشروع</b> في Visual Studio
(ومعاهم <code>glad.c</code>، ومكتبات GLFW و GLM). الأكواد 1 لـ 5 تحت هما الـ 5 ملفات كاملين. اكتبهم زي ما هما، واعمل Run على المشروع.</div>''')
P.append('<h3>كود 1: ملف shaderClass.h</h3><p class="what">تعريف كلاس الـ Shader: «فيه إيه» من غير التفاصيل.</p>' + prog('full/4_camera/shaderClass.h', 'shaderClass.h')
         + nores('ملف تعريف بس، مش بيرسم حاجة لوحده. النتيجة بعد كود 5.'))
P.append('<h3>كود 2: ملف shaderClass.cpp</h3><p class="what">تفاصيل الكلاس: إزاي بيبني الـ Shader ويشغّله.</p>' + prog('full/4_camera/shaderClass.cpp', 'shaderClass.cpp')
         + nores('ده «شغل جوه الكلاس». بيتنفّذ لما <code>main.cpp</code> يعمل Shader. النتيجة بعد كود 5.'))
P.append('<h3>كود 3: ملف Camera.h</h3><p class="what">تعريف كلاس الكاميرا: المتغيرات والدوال.</p>' + prog('full/4_camera/Camera.h', 'Camera.h')
         + nores('ملف تعريف بس. النتيجة بعد كود 5.'))
P.append('<h3>كود 4: ملف Camera.cpp</h3><p class="what">قلب المحاضرة: إزاي الكاميرا بتعمل المصفوفة، وبتتحرك بالكيبورد، وبتلف بالماوس.</p>'
         + D.fig(D.c_fov(), 'زاوية الرؤية (FOV) في دالة <code>perspective</code>: 45° = بتشوف حتة صغيرة فالحاجات كبيرة، و 90° = بتشوف أكتر والحاجات أصغر.')
         + D.fig(D.c_wasd(), 'من فوق: W و S على اتجاه النظر، و A و D على «اليمين». وكل فريم بتتحرك <code>speed</code> = 0.1.')
         + D.fig(D.c_pitch(), 'شرط الـ 5°: لو البص هيقرب أوي من فوق خالص أو تحت خالص (المنطقة الحمرا)، الكاميرا ترفض اللفة دي عشان ما تتقلبش.')
         + prog('full/4_camera/Camera.cpp', 'Camera.cpp')
         + nores('الدوال دي بتشتغل كل فريم لما <code>main.cpp</code> ينده عليها. النتيجة بعد كود 5.'))
camshots = [('c_start', 'أول ما يشتغل'), ('c_w', 'دسنا <b>W</b> ربع ثانية'), ('c_s', 'دسنا <b>S</b> نص ثانية'), ('c_d', 'دسنا <b>D</b>'),
            ('c_a', 'دسنا <b>A</b> (رجعنا)'), ('c_space', 'دسنا <b>Space</b>'), ('c_mousedown', 'سحبنا الماوس لتحت'), ('c_mouseright', 'سحبنا الماوس يمين')]
ct = rd('run/out/camera.txt').split('\n')
i1 = [i for i, l in enumerate(ct) if 'normal drag' in l][0]; i2 = [i for i, l in enumerate(ct) if 'very fast' in l][0]
P.append('<h3>قبل كود 5: سطور الـ Shader الجديدة كلمة كلمة</h3><p class="what">الـ Shader هنا فيه كلمات جديدة عن محاضرة الـ Uniforms: <code>vec3</code> و <code>mat4</code>.</p>' + ''.join(CAMERA_WORDS))
P.append('<h3>كود 5: ملف main.cpp</h3><p class="what">البرنامج الرئيسي: بيفتح الشباك، ويعمل الهرم، ويشغّل الكاميرا كل فريم.</p>' + prog('full/4_camera/main.cpp', 'main.cpp')
         + res(grid([shot('full_' + n, c) for n, c in camshots], 4)
               + '<p style="font-size:10pt">ده الشباك الحقيقي وإحنا بندوس أزرار ونحرك الماوس فعلاً، بالترتيب ده في نفس الجلسة: كل لقطة بتكمّل من اللي قبلها.</p>',
               '▶ النتيجة لما نعمل Run للمشروع كله (الأكواد 1 لـ 5)'))
P.append(res(term('\n'.join(ct[i1:i1 + 15])) + '<p style="font-size:10pt">مع سحب عادي للماوس لفوق، الزاوية بتقف عند 10° ومش بتتقلب. الشرط شغال.</p>'
             + term('\n'.join(ct[i2:i2 + 5])) + '<p style="font-size:10pt">بس لو الماوس اتحرك بسرعة جداً في فريم واحد، الخطوة بتنط فوق المنطقة الحمرا والكاميرا تتقلب. ده عيب في كود الفيديو.</p>',
             '▶ تجربة إضافية: شرط الـ 5°'))
P.append('''<div class="warn"><b>⚠️ اكتشفناها وإحنا بنشغّل:</b> سرعة الكاميرا بتعتمد على سرعة جهازك! <code>speed = 0.1</code> بتتضاف <b>كل فريم</b>،
فلو جهازك بيرسم 1000 فريم في الثانية الكاميرا هتطير. اللقطات فوق على 60 فريم زي الشاشة العادية. والحل اللي هتتعلمه قدام (learnopengl): تضرب السرعة في الوقت اللي عدّى بين فريمين (deltaTime).</div>''')
P.append(SB.d1_camera())
P.append('<h3 id="why-cam">ليه كتبنا كل ده؟ الهدف من كل خطوة</h3>'
  '<p class="what">خطوات تجهيز OpenGL نفسها (الشباك، GLAD، VAO، VBO، اللوب…) شرحناها في قسم «ليه؟» في محاضرة الـ Uniforms، ونفس الكلام هنا بالظبط. هنا الخطوات الخاصة بالكاميرا. وفي التجارب شلنا أو غيّرنا حاجة واحدة بس، ودوسنا أزرار وحركنا الماوس فعلاً.</p>'
  + '<div class="legend"><span class="badge b-req">إجباري</span> = من غيره مش هيشتغل · <span class="badge b-imp">مش إجباري، بس مهم جداً</span> = هيشتغل، بس هتتعب · <span class="badge b-opt">اختياري</span> = تحسين أو مثال</div>'
  + WHY2.build_cam())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الكاميرا = مكان + بتبص فين + فين فوق.</li>
 <li>دالة <code>lookAt</code> + دالة <code>perspective</code> = مصفوفة، بتتبعت كـ Uniform.</li><li>الكيبورد بيغيّر المكان، والماوس بيغيّر الاتجاه.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> في <code>main.cpp</code> غيّر <code>45.0f</code> لـ <code>90.0f</code>، وفي <code>Camera.h</code> غيّر <code>sensitivity</code> لـ 50.</div></section>''')

# ------------------------------------------------------------------ links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>المؤشرات:</b> الدالة <code>glfwGetCursorPos</code> بتاخد عناوين بـ <code>&amp;</code>، والدالة <code>value_ptr</code> بترجّع عنوان.</td></tr>
 <tr><td class="n">2</td><td><b>الـ Uniforms:</b> مصفوفة الكاميرا بتتبعت بنفس الـ 3 خطوات بتوع اللون.</td></tr>
 <tr><td class="n">3</td><td><b>الضرب النقطي:</b> جوه <code>glm::angle</code> اللي بتمنع الكاميرا تتقلب، وجوه <code>lookAt</code>.</td></tr>
 <tr><td class="n">4</td><td><b>الكاميرا:</b> بتجمع ده كله، وده أساس أداة الـ CAD بتاعتك.</td></tr>
</table>
<h3>بكره (الإثنين 26-10)</h3>
<ul><li>برمجة: تمارين Pointers من Exercism.</li><li>رسم: ألوان لكل نقطة (Vertex Attributes).</li>
<li>رياضيات: تمارين الضرب النقطي من Khan Academy.</li><li>الـ CAD: تخزين النقط في <code>std::vector</code>.</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>المؤشرات: <span class="ltr">youtube.com/watch?v=DTxHyVn0ODg</span></li><li>الـ Uniforms: <span class="ltr">youtube.com/watch?v=DE6Xlx_kbo0</span></li>
 <li>الضرب النقطي: <span class="ltr">youtube.com/watch?v=LyGKycYT2v0</span></li><li>الكاميرا: <span class="ltr">youtube.com/watch?v=86_pQCKOIPk</span></li></ul></section>''')


import sys as _s; _s.path.insert(0, '/home/claude/day2')
import quick as Q
css += STH.CSS
css += Q.CSS
P.insert(1, Q.quick_section(Q.DAY1_CARDS, Q.DAY1_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q.DAY1_QA))
P = [Q.tag_reference(x) for x in P]
import linenums as LN
if MODE != 'web': P.append(STH.copy_appendix())
import jumps as JUMP
P = [JUMP.apply(''.join(P), LN, ART if MODE != 'web' else '')]
css += STH.CSS if MODE != 'web' else ''
css += LN.CSS + JUMP.CSS
if MODE == 'web':
    body = "".join(P)
    def datauri(m):
        b = base64.b64encode(open(m.group(1), 'rb').read()).decode()
        return f'src="data:image/png;base64,{b}"'
    body = re.sub(r'src="(img/[^"]+\.png)"', datauri, body)
    webcss = open('web.css', encoding='utf-8').read()
    js = open('web.js', encoding='utf-8').read()
    page = ('<title>محاضرات الأسبوع 2 · اليوم الأول</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week2_day1_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 2 - اليوم الأول</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week2_day1_v4.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week2_day1_v4.html', base_url='.').write_pdf('Week2_Day1_Sunday.pdf')
    import fixpdf; fixpdf.fix('Week2_Day1_Sunday.pdf')
    print('built v4')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
