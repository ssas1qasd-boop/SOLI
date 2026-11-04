# Week 2 · Day 6 (Friday 30-10). Same structure as Days 1-5. MODE="web" builds the copy page; default builds the PDF.
import html, re, os, base64, sys
for d in ('day1', 'day2', 'day3', 'day4', 'day5', 'day6'):
    sys.path.insert(0, f'/home/claude/{d}')
import weasyprint
import diagrams as D1
import diag6 as D
from data6 import E, OVER
from words6 import *
import why_day6 as WHY
import sb as SB
import sb6 as SB6
import quick as Q
import quick6 as Q6

os.chdir('/home/claude/day6')
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
STH.setup(['specs_d6'], MODE, hl)
P = STH.PList()
# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثاني: المؤشرات والـ Shaders</div>
  <h1>اليوم السادس — الجمعة 30 أكتوبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> تمرينين exercism + بناء Compiler من الصفر — <span style="color:#5b6372">Erik Schierboom (NDC Oslo 2026) و exercism</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> ألوان متحركة (مراجعة Uniforms) — <span style="color:#5b6372">The Cherno و learnopengl</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> مراجعة الضرب النقطي وطول المتجه — <span style="color:#5b6372">Khan Academy</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> تنظيف الكود (Refactoring) — <span style="color:#5b6372">IoTIoT و Wikipedia</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:5mm;background:#fffbeb"><b>النهارده يوم مراجعة وتطبيق:</b> الرسم والرياضيات مراجعة لمحاضرات الأحد والإتنين بكود جديد. والـ CAD هيرجع لبرنامج امبارح وينضّفه من غير ما يغيّر سلوكه، وهنثبت ده بمقارنة الصور بكسل بكسل. ومحاضرة الرياضيات بـ Python زي امبارح.</div>
</section>''')

# ================================================================== 1 · compiler + exercism
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'بناء Compiler من الصفر + تمرينين exercism',
             'Erik Schierboom · Writing a compiler from scratch (NDC Oslo 2026) · <span class="ltr">youtu.be/tYFljFUaAw0</span> · exercism.org/tracks/cpp'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Compiler برنامج بيترجم كود من شكل لشكل. بيقرا الحروف ويقطّعها كلمات (Tokens)، ويرتب الكلمات في شجرة بتقول مين يتحسب الأول، ويحوّل الشجرة لأوامر صغيرة تشتغل على Stack.</div>
<p class="what">Erik (نفس اللي شرح Hamming يوم التلات) بنى لغة صغيرة فيها أرقام وجمع وضرب ومتغيرات. إحنا هنبني نفس الفكرة في ملف C++ واحد، ونطبع كل مرحلة عشان تشوفها بعينك. وبعدين تمرينين من exercism: <b>Leap</b> و <b>Raindrops</b>.</p>''')
P.append(D1.fig(D.k_pipeline(), 'الـ 4 مراحل: كل مرحلة بتاخد شكل البرنامج وتطلّع الشكل اللي بعده. والـ VM في الآخر بتنفذ.'))
P.append(COMPILER_TABLE)
P.append('<h3 id="compiler-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(COMPILER_WORDS))
P.append(D1.fig(D.k_trees(), 'شمال: الجمع بينده الضرب، فـ 2 × 3 بقت فرع لوحدها والنتيجة 7. يمين: لو بدّلنا المستويين (جربناها تحت) تطلع 9.'))
P.append('<h3>البرنامج 1: Compiler صغير</h3><p class="what">الكود: <code>var x = 1 + 2 * 3; x * 2;</code>. البرنامج بيطبع الـ Tokens، والشجرة، والـ Bytecode، وكل أمر وهو بيتنفذ مع الـ Stack بعده.</p>'
         + prog(SRC + 'p1_tiny_compiler.cpp', 'tiny_compiler.cpp') + res(term(rd(SRC + 'p1_tiny_compiler.txt')) + '<p style="font-size:10pt">1 + 2 × 3 = 7 اتخزنت في <code>x</code> (الخانة 0)، وبعدين x × 2 = 14 اتطبعت.</p>'))
P.append(SB6.d6_scan())
P.append(SB6.d6_parse())
P.append(BYTECODE_TABLE)
P.append(D1.fig(D.k_stack(), 'الـ Stack وهو بيحسب 1 + 2 × 3: كل LOAD بيحط فوق، والعملية بتشيل رقمين وتحط واحد.'))
P.append(SB6.d6_vm())
P.append('<h3 id="exercism-words">تمرينين exercism</h3><p class="what">في exercism بتكتب الدالة بس، والموقع بيشغّل اختبارات جاهزة ويقولك PASS أو FAIL. إحنا عملنا دالة <code>check</code> صغيرة بنفس الفكرة عشان تجرب على جهازك.</p>' + ''.join(EXERCISM_WORDS))
P.append('<h3>البرنامج 2: Leap (السنة الكبيسة)</h3><p class="what">السنة كبيسة لو بتقبل القسمة على 4، إلا لو بتقبل على 100، إلا لو بتقبل على 400.</p>'
         + prog(SRC + 'p2_leap.cpp', 'leap.cpp') + res(term(rd(SRC + 'p2_leap.txt'))))
P.append('<h3>البرنامج 3: Raindrops</h3><p class="what">3 = Pling، و 5 = Plang، و 7 = Plong. لو مفيش ولا واحد، رجّع الرقم نفسه.</p>'
         + prog(SRC + 'p3_raindrops.cpp', 'raindrops.cpp') + res(term(rd(SRC + 'p3_raindrops.txt'))))
P.append('<h3 id="why-compiler">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1 (الـ Compiler)</h3>' + WHY.build_compiler() + '<h3>البرنامج 2 و 3 (exercism)</h3>' + WHY.build_exercism())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Scanner: حروف ← Tokens. Parser: Tokens ← شجرة. Compiler: شجرة ← Bytecode. VM: تنفيذ على Stack.</li>
 <li>الأولوية من ترتيب الدوال: الأضعف (الجمع) بينده الأقوى (الضرب).</li>
 <li>الشجرة كلها <code>Node*</code>: نفس الـ Pointers بتاعة الأسبوع ده.</li>
 <li>exercism: الاختبار بيقولك الغلطة في ثانية. <code>&amp;&amp;</code> أقوى من <code>||</code>، بس الأقواس بتوضح.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. غيّر الكود لـ <code>var y = 2 * 3 + 4; y * y;</code> (لازم يطلع 100). 2. زوّد الطرح: Token <code>Minus</code> وأمر <code>SUBTRACT</code> في نفس مستوى الجمع. 3. في Raindrops: زوّد 11 = Plunk.</div></section>''')

# ================================================================== 2 · uniforms review
r1 = {l.strip() for l in open(SRC + 'r1_animated_color.cpp') if l.strip()}
r2new = {l.strip() for l in open(SRC + 'r2_time_colors.cpp') if l.strip()} - r1
P.append(lec('l2', 'المحاضرة 2 · رسم', 'ألوان متحركة (مراجعة Uniforms)', 'قناة The Cherno · Uniforms in OpenGL (مراجعة) · <span class="ltr">youtu.be/DE6Xlx_kbo0</span> · learnopengl.com/Getting-started/Shaders'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ uniform رقم (أو كذا رقم) بيبعته الـ CPU للـ Shader قبل الرسم، وبيبقى واحد لكل الرسمة. لو غيّرته كل فريم، الرسمة بتتحرك من غير ما تلمس الأركان.</div>
<p class="what">ده نفس فيديو يوم الأحد. البرنامج 1 هو كود The Cherno كامل مع فحص الاسم زي الـ ASSERT بتاعه. والبرنامج 2 خطوة لقدام: بنبعت <b>الوقت</b> بس، والـ Fragment Shader هو اللي يحسب لون مختلف لكل بكسل.</p>''')
P.append(UNIFORM_TABLE)
P.append(D1.fig(D.u_one_vs_many(), 'شمال: كل ركن ليه مكانه من الصندوق (attribute). يمين: لون واحد للمستطيل كله (uniform).'))
P.append('<h3 id="uniform-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(UNIFORM_WORDS))
P.append(GLUNIFORM_TABLE)
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD). الـ Shaders مكتوبة كنص <code>std::string</code> زي يوم الخميس.</div>')
P.append('<h3>البرنامج 1: كود The Cherno (الأحمر بيطلع وينزل)</h3><p class="what">مستطيل بـ Index Buffer، ولونه من <code>u_Color</code>، والأحمر بيتغير 0.05 كل فريم ويرجع عند 0 و 1. وبنطبع الأحمر كل 10 فريمات.</p>'
         + prog(SRC + 'r1_animated_color.cpp', 'animated_color.cpp')
         + res(term('\n'.join(rd(SRC + 'r1_animated_color.txt').splitlines()[:6]))
               + grid([shot('r1_animated_color_3', 'r قليل'), shot('r1_animated_color_1', 'r في النص'), shot('r1_animated_color_5', 'r قرب من 1')], 3)
               + '<p style="font-size:10pt">3 لقطات حقيقية من نفس التشغيل في أوقات مختلفة.</p>', '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(D1.fig(D.u_zigzag(), 'الأحمر مع الفريمات: بالـ if بيطلع وينزل (أزرق). من غيرها بيكبر للأبد، والكارت بيقصه عند 1 فاللون بيقف (أحمر متقطع).'))
P.append(SB6.d6_anim())
P.append(D1.fig(D.u_time_flow(), 'البرنامج 2: الـ CPU بيبعت رقم واحد كل فريم، والكارت بيحسب لون لكل بكسل.'))
P.append('<h3>البرنامج 2: ألوان بالوقت</h3><p class="what">نفس البرنامج، والسطور <b>بالأصفر</b> هي اللي اتغيرت: بدل <code>u_Color</code> بقى فيه <code>u_Time</code> (float واحد) بنبعته بـ <code>glUniform1f</code>، والـ Fragment بيحسب الألوان بـ <code>sin</code>.</p>'
         + prog(SRC + 'r2_time_colors.cpp', 'time_colors.cpp', new=r2new)
         + res(term('\n'.join(rd(SRC + 'r2_time_colors.txt').splitlines()[:5]))
               + grid([shot('r2_time_colors_1', 'بعد نص ثانية تقريباً'), shot('r2_time_colors_4', 'بعدها بثانية'), shot('r2_time_colors_6', 'بعدها كمان')], 3), '▶ النتيجة لما نعمل Run (الشباك الحقيقي)'))
P.append(SB6.d6_time())
P.append('<h3 id="why-uniform">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_uniform() + '<h3>البرنامج 2</h3>' + WHY.build_time())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>uniform = قيمة واحدة لكل الرسمة من الـ CPU. attribute = قيمة لكل ركن من الصندوق.</li>
 <li><code>glUseProgram</code> ← <code>glGetUniformLocation</code> مرة واحدة ← <code>glUniform4f</code> أو <code>glUniform1f</code> كل فريم.</li>
 <li>‎-1 = اسم غلط أو uniform مش مستخدم. والنوع لازم يطابق (<code>1f</code> للـ float).</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. في البرنامج 1 حرّك الأخضر كمان بـ <code>increment</code> تاني. 2. في البرنامج 2 زوّد <code>uniform float u_Speed;</code> وابعته بـ <code>glUniform1f</code>، واضرب الوقت فيه.</div></section>''')

# ================================================================== 3 · dot & length review
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'مراجعة الضرب النقطي وطول المتجه', 'Khan Academy · Vector dot product and vector length (مراجعة) · <span class="ltr">youtu.be/WNuIhXo39_k</span> · khanacademy.org/math/linear-algebra/vectors-and-spaces'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الضرب النقطي = اضرب المتقابلين واجمع، والنتيجة رقم. والطول = جذر الضرب النقطي للمتجه في نفسه. ده فيثاغورس بالظبط، وشغال لأي عدد أرقام.</div>
<p class="what">نفس فيديو يوم الإتنين. المرة دي بـ Python: الأول بإيدنا من غير مكتبات (عشان القانون يبان)، وبعدين بـ NumPy زي امبارح، ونجرب خصائص الضرب النقطي بأرقام.</p>''')
P.append(D1.fig(D.m_pythagoras(), 'المتجه [2, 5]: ضلعين 2 و 5، والوتر = الطول = √29. ونفس الرقم 29 = a · a.'))
P.append('<h3 id="math-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(MATH_WORDS))
P.append('<h3>البرنامج 1: بإيدنا (Python من غير مكتبات)</h3><p class="what">دالتين: <code>dot</code> بلوب، و <code>length</code> بتستخدم <code>dot</code>. ونفس أمثلة Khan.</p>'
         + prog(SRC + 'm1_dot_length.py', 'dot_length.py') + res(term(rd(SRC + 'm1_dot_length.txt')) + '<p style="font-size:10pt">19 و 13 زي Khan بالظبط، و |[2, 5]| = √29، و 50 واحد طولهم √50.</p>'))
P.append('<h3>البرنامج 2: بـ NumPy، والخصائص</h3><p class="what">نفس الأرقام في سطر، وبعدين 3 خصائص بنتأكد منها بأرقام، ومتجه طوله 1.</p>'
         + prog(SRC + 'm2_numpy_review.py', 'numpy_review.py') + res(term(rd(SRC + 'm2_numpy_review.txt'))))
P.append(MATH_TABLE)
P.append('<h3 id="why-math">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_math())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>a · b = مجموع (aᵢ × bᵢ): رقم. لازم نفس الطول.</li>
 <li>‖a‖ = √(a · a). وقسمة المتجه على طوله = متجه طوله 1.</li>
 <li>c · d = d · c، والتوزيع، والرقم يطلع برا.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. طول [1, 2, 2]؟ (3). 2. [1, 1] · [‎-1, 1]؟ (0: المتجهين متعامدين). 3. اكتب دالة <code>normalize(a)</code> بإيدك من غير NumPy.</div></section>''')

# ================================================================== 4 · refactoring
c0 = {l.strip() for l in open('/home/claude/day5/src/c2_delete_last_line.cpp') if l.strip()}
c1new = {l.strip() for l in open(SRC + 'c1_refactored.cpp') if l.strip()} - c0
P.append(lec('l4', 'المحاضرة 4 · CAD', 'تنظيف الكود (Refactoring)', 'IoTIoT · Code Refactoring Introduction for Beginners · <span class="ltr">youtu.be/7Xojr8J9Rso</span> · en.wikipedia.org/wiki/Code_refactoring'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> «Refactoring = إعادة ترتيب الكود من جوه من غير ما سلوكه من برا يتغير» (Martin Fowler). الهدف كود أسهل في القراية والتعديل، والبرنامج يفضل يعمل نفس الحاجة بالظبط.</div>
<p class="what">الفيديو مقدمة: إيه هو الـ Refactoring، وإيه الـ Coding Standards، وإيه اللي بيحصل لو مااتعملش (Code smells، صعوبة الصيانة، وقت أطول في الـ Debugging). إحنا هنطبّق على برنامج امبارح (مسح آخر خط): نفس السلوك، كود أنضف. وبعدين <b>نثبت</b> إن السلوك ما اتغيرش.</p>''')
P.append(REFACTOR_TABLE)
P.append(D1.fig(D.c_layers(), 'شمال: امبارح، الـ Callbacks شايلين كل الشغل. يمين: النهارده، الـ Callback بيترجم الضغطة لفعل له اسم، والأفعال بتستخدم دوال صغيرة.'))
P.append('<h3 id="refactor-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(REFACTOR_WORDS))
P.append('<h3>البرنامج 1: برنامج امبارح بعد التنظيف</h3><p class="what">السطور <b>بالأصفر</b> جديدة أو اتغيرت عن امبارح. باقي السطور (الـ Shaders وإعداد الشباك) زي ما هي.</p>'
         + prog(SRC + 'c1_refactored.cpp', 'refactored.cpp', new=c1new)
         + res(term(rd(SRC + 'c1_refactored.txt'))
               + grid([shot('c1_9', 'خطين'), shot('c1_10', 'Backspace'), shot('c1_13', 'خط جديد بـ 3 نقط'), shot('c1_15', 'Backspace مرتين'), shot('c1_17', 'نقطتين جداد')], 3)
               + '<p style="font-size:10pt">17 دوسة حقيقية بالماوس والكيبورد. شغّلنا برنامج امبارح بنفس الـ 17 دوسة: الـ Terminal نفس الكلام بالحرف، والـ 17 صورة نفس البكسلات بالظبط.</p>', '▶ النتيجة لما نعمل Run (دوسات حقيقية بالماوس والكيبورد)'))
P.append(SB6.d6_same())
P.append('<h3 id="why-refactor">ليه كتبنا كل ده؟ وإزاي نعرف إننا ما بوّظناش حاجة؟</h3>' + LEGEND + WHY.build_refactor())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Refactoring: الكود من جوه يتغير، والسلوك من برا لأ.</li>
 <li>أرقام سحرية ← ثوابت. كود متكرر ← دالة. دالة كبيرة ← دوال صغيرة أسماءها أفعال.</li>
 <li>بعد كل خطوة: شغّل بنفس الدخل وقارن الكلام <b>والصورة</b>. غلطة واحدة ممكن تبان في واحد بس منهم.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. خلّي لون الخطوط أخضر بتغيير سطر واحد بس. 2. اعمل <code>ClearAll()</code> لزرار Delete، واستخدم فيها <code>StartNewLine()</code>.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>الـ Compiler:</b> نفس اللي بيحصل للـ Shader لما تنده <code>glCompileShader</code>: نص بيتقطّع ويتحوّل لأوامر الكارت. ونفس الـ <code>g++</code> اللي بنستخدمه كل يوم.</td></tr>
 <tr><td class="n">2</td><td><b>الـ Uniforms:</b> قيمة واحدة من الـ CPU لكل البكسلات. بعدين هنبعت بيها مصفوفة الكاميرا.</td></tr>
 <tr><td class="n">3</td><td><b>الضرب النقطي والطول:</b> الـ Unit vector هو اللي هنستخدمه في الإضاءة: الضوء بيتحسب بـ dot بين متجهين طولهم 1.</td></tr>
 <tr><td class="n">4</td><td><b>الـ Refactoring:</b> كل ما الأداة تكبر، الكود لازم يفضل نضيف عشان نقدر نزوّد عليه.</td></tr>
</table>
<h3>بكره (السبت 31-10)</h3>
<ul><li>برمجة: مراجعة الأسبوع (Pointers).</li><li>رسم: تجربة حرة (Vertex Arrays).</li>
<li>رياضيات: اختبر نفسك (Cross product).</li><li>الـ CAD: Commit في Git.</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>Writing a compiler from scratch (NDC Oslo 2026): <span class="ltr">youtube.com/watch?v=tYFljFUaAw0</span> · <span class="ltr">exercism.org/tracks/cpp</span> · <span class="ltr">craftinginterpreters.com</span></li>
 <li>Uniforms in OpenGL: <span class="ltr">youtube.com/watch?v=DE6Xlx_kbo0</span> · <span class="ltr">learnopengl.com/Getting-started/Shaders</span></li>
 <li>Vector dot product and vector length: <span class="ltr">youtube.com/watch?v=WNuIhXo39_k</span></li>
 <li>Code Refactoring Introduction for Beginners: <span class="ltr">youtube.com/watch?v=7Xojr8J9Rso</span> · <span class="ltr">en.wikipedia.org/wiki/Code_refactoring</span></li></ul></section>''')

css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q6.DAY6_CARDS, Q6.DAY6_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q6.DAY6_QA))
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
    page = ('<title>محاضرات الأسبوع 2 · اليوم السادس</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week2_day6_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 2 - اليوم السادس</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week2_day6.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week2_day6.html', base_url='.').write_pdf('Week2_Day6_Friday.pdf')
    import fixpdf; fixpdf.fix('Week2_Day6_Friday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
