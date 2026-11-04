# Builds the Week 2 / Day 1 study PDF: every code line sits next to its own simple explanation.
import html, re, weasyprint

css = open('base.css', encoding='utf-8').read() + '''
.fullsec { margin-top:8mm; padding-top:5mm; border-top:3px double #c9d1de; }
.fname { direction:ltr; text-align:left; font-family:"DejaVu Sans Mono",monospace; font-size:9.5pt; font-weight:bold; color:#1d2330; background:#e8ecf3; display:inline-block; padding:1mm 3mm; border-radius:1.5mm; margin:4mm 0 0; }
table.cl { width:100%; border-collapse:collapse; margin:2mm 0 4mm; }
table.cl tr { page-break-inside:avoid; }
table.cl td { vertical-align:top; padding:1.6mm 2.5mm; border-bottom:1px solid #263042; }
table.cl td.k { width:52%; direction:ltr; text-align:left; background:#141a26; color:#e6e9ef;
  font-family:"DejaVu Sans Mono",monospace; font-size:8.3pt; line-height:1.5; white-space:pre-wrap; word-break:break-word; }
table.cl td.e { background:#fbfcfe; border-bottom:1px solid #e6e9ef; font-size:10pt; line-height:1.6; }
table.cl tr.br td.k { color:#6f7a8f; padding-top:0.6mm; padding-bottom:0.6mm; }
table.cl tr.br td.e { color:#8a8f98; font-size:8.8pt; padding-top:0.6mm; padding-bottom:0.6mm; }
table.cl tr:first-child td.k { border-top-left-radius:2.5mm; }
table.cl tr:last-child td.k { border-bottom-left-radius:2.5mm; }
table.cl .cm{color:#8b95a7} table.cl .kw{color:#7fb4ff} table.cl .st{color:#a5e3a0} table.cl .nu{color:#f6b97a}
.note { font-size:9.5pt; color:#5b6372; margin:-2mm 0 3mm; }
.result { border:1.5px solid #16a34a; border-radius:3mm; padding:3.5mm 4.5mm 2mm; margin:4mm 0 5mm; page-break-inside:avoid; }
.result .rh { color:#15803d; font-weight:700; margin-bottom:2mm; }
.run { direction:ltr; text-align:left; background:#0b0f17; color:#b8f2c4; border-radius:2.5mm; padding:0 4mm 3mm;
  font-family:"DejaVu Sans Mono",monospace; font-size:8.4pt; line-height:1.5; white-space:pre-wrap; margin:1mm 0 2.5mm; }
.run .bar { color:#6b7487; font-size:7.5pt; padding:2mm 0 2mm 4mm; border-bottom:1px solid #222a38; margin:0 -4mm 2mm; }
table.shots { width:100%; border-collapse:separate; border-spacing:2mm; margin:0 -2mm; }
table.shots { table-layout:fixed; } table.shots td { text-align:center; vertical-align:top; }
table.shots img { width:100%; border-radius:2mm; display:block; }
table.shots .cap { font-size:9pt; color:#5b6372; margin-top:1mm; line-height:1.45; }
'''

KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4)\b'
def hl(line):
    t = html.escape(line, quote=False)
    m = re.search(r'(//.*$|#\w.*$)', t)
    tail = ''
    if m: t, tail = t[:m.start()], f'<span class="cm">{m.group(0)}</span>'
    parts = re.split(r'("[^"]*")', t)
    out = []
    for p in parts:
        if p.startswith('"'): out.append(f'<span class="st">{p}</span>'); continue
        p = re.sub(KW, r'<span class="kw">\1</span>', p)
        p = re.sub(r'(?<![\w#.])(\d+\.?\d*f?)\b', r'<span class="nu">\1</span>', p)
        out.append(p)
    return ''.join(out) + tail

def code(rows):
    """rows: list of (code_line, explanation). Lines that are only braces get a light style."""
    h = ['<table class="cl">']
    for c, e in rows:
        cls = ' class="br"' if c.strip() in ('{', '}', '};', '{ }') else ''
        h.append(f'<tr{cls}><td class="k">{hl(c)}</td><td class="e">{e}</td></tr>')
    h.append('</table>')
    return '\n'.join(h)

def term(text):
    return '<div class="run"><div class="bar">● ● ●  &nbsp;Terminal — output after Run</div>' + html.escape(text.rstrip('\n')) + '</div>'
def shot(img, cap): return f'<td><img src="img/{img}.png"><div class="cap">{cap}</div></td>'
def grid(cells, cols):
    rows = [cells[i:i+cols] for i in range(0, len(cells), cols)]
    return '<table class="shots">' + ''.join('<tr>' + ''.join(r) + '</tr>' for r in rows) + '</table>'
def rd(p): return open(p).read()
def res(body, title='▶ النتيجة لما نعمل Run'):
    return f'<div class="result"><div class="rh">{title}</div>{body}</div>'
def nores(where):
    return f'<div class="result" style="border-style:dashed"><div class="rh">▶ النتيجة لما نعمل Run</div><p style="font-size:10pt;margin:0 0 2mm">{where}</p></div>'
import re as _re
_pt = open('run/out/pointers.txt').read()
PT = {int(m.group(1)): m.group(0).strip() for m in _re.finditer(r'=== Code (\d).*?(?==== Code|\Z)', _pt, _re.S)}
PT[6] = PT[6].strip()
L = lambda t: f'<span class="ltr">{t}</span>'
B_OPEN, B_CLOSE = 'بداية', 'نهاية'


from full_data import E as _E
def fullfile(path, label):
    rows = []
    for line in open(path):
        t = line.rstrip('\n')
        if not t.strip(): continue
        rows.append((t, _E[t.strip()]))
    return f'<div class="fname"><span class="ltr">{label}</span></div>' + code(rows)
def fullhead(sub):
    return ('<div class="fullsec"><h3 style="border:0;margin-top:0">📄 الكود كامل (جاهز تنسخه وتشغّله)</h3>'
            f'<p style="font-size:10pt;color:#5b6372">{sub}</p>')
FULL = []
FULL.append(fullhead('برنامج واحد فيه كود المحاضرة كله. ضفنا 3 سطور <code>LOG</code> بس عشان نشوف النتيجة.')
  + fullfile('full/1_pointers/main.cpp', 'main.cpp')
  + res(term(rd('full/out1.txt')) + '<p style="font-size:10pt">10 = قيمة <code>var</code> بعد التغيير، وبعدها العنوان، و 0 = أول بايت في الـ buffer، و 1 = «أيوه، ptr2 بيوصّل لـ buffer».</p>') + '</div>')
FULL.append(fullhead('البرنامج كامل في ملف واحد. نفس فكرة The Cherno، بس بـ GLAD زي ما ركبتها في الأسبوع الأول، والـ Shader مكتوب جوه الكود بدل ملف منفصل.')
  + fullfile('full/2_uniforms/main.cpp', 'main.cpp')
  + res(term(rd('full/out2.txt')) + grid([shot(f'full_u{i}', f'لقطة {i}') for i in range(1,7)] + ['<td></td>','<td></td>'], 4)
        + '<p style="font-size:10pt">لقطات من الشباك الحقيقي وهو شغال، كل لقطة بعد حوالي 0.12 ثانية: اللون رايح جاي بين الأزرق والوردي.</p>',
        '▶ النتيجة لما نعمل Run (الشباك الحقيقي)') + '</div>')
FULL.append(fullhead('برنامج كامل يجرّب الأمثلة.')
  + fullfile('full/3_dot/main.cpp', 'main.cpp')
  + res(term(rd('full/out3.txt'))) + '</div>')
camshots = [('c_start','أول ما يشتغل'),('c_w','دسنا <b>W</b> ربع ثانية'),('c_s','دسنا <b>S</b> نص ثانية'),('c_d','دسنا <b>D</b>'),
            ('c_a','دسنا <b>A</b> (رجعنا)'),('c_space','دسنا <b>Space</b>'),('c_mousedown','سحبنا الماوس لتحت'),('c_mouseright','سحبنا الماوس يمين')]
FULL.append(fullhead('5 ملفات. حطهم كلهم في نفس المشروع في Visual Studio. شكل الكلاسات زي Victor Gordan، بس الـ Shader بياخد النص مباشرة بدل ما يقرا ملفات، والهرم ملوّن بدل صورة الطوب.')
  + fullfile('full/4_camera/shaderClass.h', 'shaderClass.h')
  + fullfile('full/4_camera/shaderClass.cpp', 'shaderClass.cpp')
  + fullfile('full/4_camera/Camera.h', 'Camera.h')
  + fullfile('full/4_camera/Camera.cpp', 'Camera.cpp')
  + fullfile('full/4_camera/main.cpp', 'main.cpp')
  + res(grid([shot('full_'+n, c) for n, c in camshots], 4)
        + '<p style="font-size:10pt">ده الشباك الحقيقي وإحنا بندوس أزرار ونحرك الماوس فعلاً، بالترتيب ده في نفس الجلسة: كل لقطة بتكمّل من اللي قبلها.</p>'
        + '<p style="font-size:10pt"><b>ملاحظة مهمة اكتشفناها:</b> لما شغّلنا البرنامج من غير ما نحدد سرعة الشاشة، الكاميرا طارت بعيد جداً. السبب إن <code>speed = 0.1</code> بتتضاف <b>كل فريم</b>، فلو جهازك بيرسم 1000 فريم في الثانية هتتحرك أسرع 16 مرة من جهاز بيرسم 60. اللقطات دي على 60 فريم في الثانية زي الشاشة العادية. والحل اللي هتشوفه قدام (learnopengl): تضرب السرعة في الوقت اللي عدّى بين الفريمات (deltaTime).</p>',
        '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبندوس أزرار بجد)') + '</div>')

# ============================================================== content
P = []
P.append('''
<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثاني: المؤشرات والـ Shaders</div>
  <h1>اليوم الأول — الأحد 25 أكتوبر</h1>
  <div class="sub">أربع محاضرات، وكل سطر كود جنبه شرحه بأبسط كلام</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> المؤشرات (Pointers) في C++ — <span style="color:#5b6372">The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> الـ Uniforms في OpenGL — <span style="color:#5b6372">The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> الضرب النقطي (Dot product) — <span style="color:#5b6372">3Blue1Brown</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> الماوس وكلاس الكاميرا — <span style="color:#5b6372">Victor Gordan</span></td></tr>
  </table>
  <div class="howto">
    <b>إزاي تقرا الملف؟</b>
    كل كود متحط في جدول: السطر على اليمين، وشرحه على الشمال قصاده. مفيش ولا سطر من غير شرح، حتى الأقواس.
  </div>
  <div class="howto" style="margin-top:5mm;background:#f0fdf4">
    <b>تحت كل كود: «النتيجة لما نعمل Run»</b>
    كل كود اتشغل بجد، والمربع الأخضر تحته فيه اللي ظهر على الشاشة فعلاً. ولو كود مالوش شكل لوحده (زي ملف header)، المربع المتقطع بيقولك نتيجته هتبان فين. أرقام العناوين هتختلف عندك، وده طبيعي.
  </div>
</section>''')

# ---------------------------------------------------------- 1 POINTERS
P.append('<section class="lec l1"><div class="lec-head"><div class="tag">المحاضرة 1 · برمجة</div><h2>المؤشرات (Pointers) في C++</h2>'
         '<div class="meta">قناة The Cherno · حلقة 16 · <span class="ltr">youtu.be/DTxHyVn0ODg</span></div></div>')
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Pointer ورقة مكتوب عليها <b>عنوان</b> مكان في الذاكرة. مش الحاجة نفسها، ده عنوانها بس.</div>
<h3>تشبيه بسيط</h3>
<p>الذاكرة شارع طويل فيه بيوت. كل بيت عليه رقم. المتغير = بيت جواه حاجة. الـ Pointer = ورقة عليها رقم البيت.</p>
<table class="grid2"><tr>
 <td><b>علامة &amp;</b><br>«هات رقم البيت» (العنوان).</td>
 <td><b>النجمة قبل الاسم</b><br>«روح البيت ده» واقرا أو غيّر اللي جواه.</td>
</tr></table>''')

P.append('<h3>كود 1: Pointer فاضي</h3>' + code([
    ('void* ptr = 0;', 'عملنا Pointer «من غير نوع» وقيمته صفر، يعني مش بيشاور على أي بيت.'),
    ('void* ptr = NULL;', 'نفس اللي فوق بالظبط. كلمة <code>NULL</code> اسم قديم للصفر.'),
    ('void* ptr = nullptr;', 'برضه نفس المعنى، بس دي الطريقة الحديثة. استخدمها دايماً.'),
]) + res(term(PT[1]) + '<p style="font-size:10pt">الـ Pointer الفاضي قيمته 0، يعني مش بيشاور على أي حاجة.</p>') + '<p class="note">التلات سطور دول بدائل لبعض، مش بيتكتبوا مع بعض. ولو حاولت تقرا من Pointer فاضي البرنامج هيقفل.</p>')

P.append('<h3>كود 2: هات عنوان متغير</h3>' + code([
    ('int var = 8;', 'بيت اسمه <code>var</code> وجواه الرقم 8.'),
    ('void* ptr = &var;', 'علامة <code>&amp;</code> يعني «هات العنوان». فالمتغير <code>ptr</code> بقى شايل عنوان <code>var</code>.'),
]) + res(term(PT[2]) + '<p style="font-size:10pt">العنوان رقم طويل بالـ hex. و <code>&amp;var</code> و <code>ptr</code> نفس الرقم بالظبط.</p>'))

P.append('<h3>كود 3: النوع مش بيغيّر العنوان</h3>' + code([
    ('int* ptr = &var;', 'نفس العنوان، بس قلنا للـ compiler: «اللي هناك رقم صحيح، 4 بايت».'),
    ('double* ptr2 = (double*)&var;', 'غيّرنا النوع بالعافية لـ <code>double</code>. العنوان نفسه ما اتغيرش، اللي اتغير بس عدد البايتات اللي هيقراها (8).'),
]) + res(term(PT[3]) + '<p style="font-size:10pt">النوعين طلعوا نفس العنوان. الفرق الوحيد حجم اللي هيتقرا: 4 بايت أو 8.</p>'))

P.append('<h3>كود 4: روح العنوان وغيّر اللي جواه</h3>' + code([
    ('int var = 8;', 'بيت جواه 8.'),
    ('int* ptr = &var;', 'الـ Pointer شايل عنوانه.'),
    ('*ptr = 10;', 'النجمة = «روح للعنوان». رحنا البيت وحطينا 10 مكان 8.'),
    ('std::cout << var;', 'اطبع <code>var</code>: هيطلع 10، لأننا غيرنا نفس البيت.'),
]) + res(term(PT[4]) + '<p style="font-size:10pt">القيمة اتغيرت من 8 لـ 10 من غير ما نلمس <code>var</code> بإيدنا، غيرناها عن طريق العنوان.</p>') + '<p class="note">ليه مينفعش النجمة مع <code>void*</code>؟ لأن الـ compiler مش عارف يكتب كام بايت، فلازم نديله نوع.</p>')

P.append('<h3>كود 5: احجز ذاكرة بنفسك (Heap)</h3>' + code([
    ('char* buffer = new char[8];', 'كلمة <code>new</code> = «احجزلي 8 بايت جداد». وهي بترجع عنوانهم، فبنحفظه في <code>buffer</code>.'),
    ('memset(buffer, 0, 8);', 'املا الـ 8 بايت دول أصفار. (محتاجة <code>#include &lt;cstring&gt;</code>)'),
    ('// ... use buffer ...', 'هنا بتستخدم الذاكرة دي في شغلك.'),
    ('delete[] buffer;', 'رجّع الذاكرة لما تخلص. لو نسيت تحصل مشكلة اسمها «تسريب ذاكرة».'),
]) + res(term(PT[5]) + '<p style="font-size:10pt">العنوان هنا بيبدأ بـ <code>0x55…</code> (منطقة الـ Heap)، مش <code>0x7ffe…</code> زي المتغيرات العادية (الـ Stack). والـ 8 بايت كلهم أصفار بسبب <code>memset</code>.</p>') + '<p class="note">القاعدة: <code>new</code> معاها <code>delete</code>، و <code>new[]</code> معاها <code>delete[]</code>.</p>')

P.append('<h3>كود 6: Pointer شايل عنوان Pointer</h3>' + code([
    ('char* buffer = new char[8];', 'المتغير <code>buffer</code> شايل عنوان الـ 8 بايت.'),
    ('char** ptr = &buffer;', 'نجمتين = «عنوان لعنوان». المتغير <code>ptr</code> شايل عنوان <code>buffer</code> نفسه.'),
]) + res(term(PT[6]) + '<p style="font-size:10pt">سلسلة من 3 خطوات: <code>pp</code> فيه عنوان <code>buffer</code> ← وده فيه عنوان البيانات ← واللي هناك هو البيانات نفسها (0).</p>'))


P.append('''<div class="sum"><b>الملخص:</b><ul>
 <li>الـ Pointer = عنوان.</li><li>علامة <code>&amp;</code> = هات العنوان، والنجمة = روح للعنوان.</li>
 <li>القيمة <code>nullptr</code> = عنوان فاضي، ماتلمسهوش.</li><li>كل <code>new</code> لازم يقابلها <code>delete</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> اكتب <code>int a = 5; int* p = &amp;a;</code> واطبع <code>p</code> و <code>*p</code> و <code>&amp;a</code>. هتلاقي <code>p</code> = <code>&amp;a</code>، و <code>*p</code> = 5.</div>''' + FULL[0] + '</section>')

# ---------------------------------------------------------- 2 UNIFORMS
P.append('<section class="lec l2"><div class="lec-head"><div class="tag">المحاضرة 2 · رسم</div><h2>الـ Uniforms في OpenGL</h2>'
         '<div class="meta">قناة The Cherno · سلسلة OpenGL · <span class="ltr">youtu.be/DE6Xlx_kbo0</span></div></div>')
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Uniform «خانة» جوه الـ Shader (اللي شغال على كارت الشاشة)، وإحنا بنملاها من كود الـ C++.</div>
<table class="grid2"><tr>
 <td><b>القيمة المتغيرة (Attribute)</b><br>مختلفة لكل نقطة، زي اسم كل طالب.</td>
 <td><b>القيمة الموحدة (Uniform)</b><br>واحدة لكل النقط، زي رقم الفصل.</td>
</tr></table>
<p>الخطوات دايماً 3: <b>عرّف</b> الخانة في الـ Shader ← <b>هات رقمها</b> من الـ C++ ← <b>ابعت</b> القيمة.</p>''')

P.append('<h3>كود 1: تعريف الخانة في الـ Shader</h3>' + code([
    ('#shader fragment', 'علامة من The Cherno عشان برنامجه يعرف إن اللي جاي ده Fragment Shader. مش جزء من لغة GLSL.'),
    ('#version 330 core', 'بنكتب بلغة GLSL نسخة 3.3.'),
    ('layout(location = 0) out vec4 color;', 'ده اللون اللي هيطلع لكل بكسل. النوع <code>vec4</code> يعني 4 أرقام: أحمر، أخضر، أزرق، شفافية.'),
    ('uniform vec4 u_Color;', 'خانة لون فاضية اسمها <code>u_Color</code>، هنملاها من الـ C++. حرف <code>u_</code> عادة عشان تعرف إنها Uniform.'),
    ('void main()', 'الدالة اللي بتشتغل مرة لكل بكسل.'),
    ('{', f'{B_OPEN} الدالة.'),
    ('    color = u_Color;', 'لون البكسل = اللون اللي جه في الخانة. فالشكل كله لون واحد.'),
    ('};', f'{B_CLOSE} الدالة.'),
]) + nores('الـ Shader لوحده مش بيطلّع حاجة على الشاشة؛ ده «وصفة» بيستخدمها كارت الشاشة. نتيجته هتبان لما نبعتله لون في <b>كود 3</b> تحت (المربع الأزرق).'))

P.append('<h3>كود 2: هات رقم الخانة</h3>' + code([
    ('glUseProgram(shader);', 'شغّل الـ Shader ده. لازم يكون شغال قبل ما تبعتله أي قيمة.'),
    ('int location = glGetUniformLocation(shader, "u_Color");', 'اسأل كارت الشاشة: «الخانة اللي اسمها <code>u_Color</code> رقمها كام؟» واحفظ الرقم.'),
    ('ASSERT(location != -1);', 'لو الرقم طلع ‎-1 وقّف البرنامج. معناه إن الاسم غلط، أو الخانة مش مستخدمة.'),
]))
P.append('<div class="result"><div class="rh">▶ النتيجة لما نعمل Run</div>' +
         term('\n'.join(rd('run/out/uniforms.txt').split('\n')[:2])) +
         '<p style="font-size:10pt">الاسم الصح رجّع 0 (رقم صالح)، والاسم اللي فيه غلطة رجّع ‎-1.</p></div>')

P.append('<h3>كود 3: ابعت اللون</h3>' + code([
    ('glUniform4f(location, 0.2f, 0.3f, 0.8f, 1.0f);', 'ابعت 4 أرقام عشرية للخانة: أحمر قليل، أخضر قليل، أزرق كتير، ومش شفاف. النتيجة: أزرق.'),
]) + '<p class="note">اسم الدالة بيتقرا كده: Uniform + 4 أرقام + f يعني float. وأخواتها: <code>glUniform1f</code> لرقم واحد، و <code>glUniformMatrix4fv</code> لمصفوفة (هتشوفها في الكاميرا).</p>')
P.append('<div class="result"><div class="rh">▶ النتيجة لما نعمل Run</div>' +
         '<img src="img/uni_fixed.png" style="width:70mm;display:block;margin:0 auto;border-radius:2mm">' +
         f'<div style="text-align:center;font-size:9pt;color:#5b6372;margin:1.5mm 0 2mm">{L("(0.2, 0.3, 0.8, 1.0)")} = مربع أزرق</div></div>')

P.append('<h3>كود 4: لون بيتغير لوحده (Animation)</h3>' + code([
    ('float r = 0.0f;', 'كمية الأحمر. بتبدأ من صفر.'),
    ('float increment = 0.05f;', 'هنزوّد الأحمر قد إيه كل مرة.'),
    ('while (!glfwWindowShouldClose(window))', 'كرر طول ما الشباك مفتوح. كل لفة = صورة واحدة (فريم).'),
    ('{', f'{B_OPEN} اللوب.'),
    ('    glClear(GL_COLOR_BUFFER_BIT);', 'امسح الشاشة.'),
    ('    glUniform4f(location, r, 0.3f, 0.8f, 1.0f);', 'ابعت اللون بكمية الأحمر الحالية.'),
    ('    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);', 'ارسم مثلثين (6 نقط) = مربع.'),
    ('    if (r > 1.0f)', 'لو الأحمر عدّى 1 (الأقصى)…'),
    ('        increment = -0.05f;', '…ابدأ نقّص.'),
    ('    else if (r < 0.0f)', 'ولو نزل تحت 0…'),
    ('        increment = 0.05f;', '…ارجع زوّد. زي البندول رايح جاي.'),
    ('    r += increment;', 'غيّر الأحمر خطوة.'),
    ('    glfwSwapBuffers(window);', 'اعرض الصورة اللي رسمناها على الشاشة.'),
    ('    glfwPollEvents();', 'شوف لو المستخدم داس على حاجة أو قفل الشباك.'),
    ('}', f'{B_CLOSE} اللوب، ويرجع يبدأ تاني.'),
]))
frames = [(0,'0.00'),(7,'0.35'),(14,'0.70'),(21,'0.95'),(28,'0.60'),(35,'0.25'),(42,'0.10')]
P.append('<div class="result"><div class="rh">▶ النتيجة لما نعمل Run: لقطات من الـ Animation (كل 7 فريمات)</div>' +
         grid([shot(f'uni_f{k:02d}', f'فريم {k}<br>{L("r = "+r)}') for k, r in frames] + ['<td></td>'], 4) +
         '<p style="font-size:10pt">الأحمر بيزيد فاللون يقلب وردي، وبعدين يقل فيرجع أزرق، وهكذا على طول.</p></div>')
P.append('''<div class="sum"><b>الملخص:</b><ul>
 <li>الـ Uniform = خانة في الـ Shader بنملاها من الـ C++.</li>
 <li>الخطوات: عرّفها، هات رقمها، ابعت القيمة.</li><li>لازم <code>glUseProgram</code> الأول، والرقم ‎-1 = مش لاقيها.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> خلي الأخضر هو اللي بيتغير بدل الأحمر، وبعدين خلي <code>increment</code> = 0.01 وشوف الفرق.</div>''' + FULL[1] + '</section>')

# ---------------------------------------------------------- 3 DOT
P.append('<section class="lec l3"><div class="lec-head"><div class="tag">المحاضرة 3 · رياضيات</div><h2>الضرب النقطي (Dot product)</h2>'
         '<div class="meta">قناة 3Blue1Brown · فصل 9 · <span class="ltr">youtu.be/LyGKycYT2v0</span></div></div>')
P.append('''<div class="idea"><b>الفكرة في سطر:</b> بتاخد متجهين وتطلّع رقم واحد، الرقم ده بيقولك هما «متفقين في الاتجاه» قد إيه.</div>
<h3>الحساب: اضرب المتقابلين واجمع</h3>
<div class="formula">[1, 2] · [3, 4] = 1×3 + 2×4 = <b>11</b></div>
<div class="formula">[6, 2, 8, 3] · [1, 8, 5, 3] = 6 + 16 + 40 + 9 = <b>71</b></div>
<h3>المعنى: الضل</h3>
<p>نوّر كشاف على <b>w</b> فيقع ضله على خط <b>v</b>. طول الضل × طول <b>v</b> = الضرب النقطي.</p>
<svg width="100%" viewBox="0 0 640 150" xmlns="http://www.w3.org/2000/svg">
 <defs><marker id="ao" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#c2410c"/></marker>
 <marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#2563eb"/></marker></defs>
 <g font-size="13"><line x1="60" y1="120" x2="420" y2="120" stroke="#c2410c" stroke-width="3" marker-end="url(#ao)"/><text x="425" y="125" fill="#c2410c" font-weight="bold">v</text>
 <line x1="60" y1="120" x2="260" y2="25" stroke="#2563eb" stroke-width="3" marker-end="url(#ab)"/><text x="265" y="25" fill="#2563eb" font-weight="bold">w</text>
 <line x1="260" y1="29" x2="260" y2="120" stroke="#8a8f98" stroke-dasharray="5 4"/>
 <line x1="60" y1="132" x2="260" y2="132" stroke="#0d9488" stroke-width="4"/><text x="160" y="148" text-anchor="middle" fill="#0d9488">shadow</text></g></svg>
<table class="grid2"><tr><td><b>موجب</b><br>نفس الناحية تقريباً.</td><td><b>صفر</b><br>متعامدين (90°)، مفيش ضل.</td></tr></table>
<table class="grid2"><tr><td><b>سالب</b><br>عكس بعض.</td><td><b>الترتيب مش مهم</b><br><code>v·w = w·v</code> دايماً.</td></tr></table>
<h3>الفكرة العميقة (الازدواجية) بكلمتين</h3>
<p>أي متجه تقدر تشوفه بطريقتين: <b>سهم</b>، أو <b>آلة</b> بتاخد أي متجه تاني وتطلّع رقم (وده بالظبط الضرب النقطي معاه). مثال: المصفوفة <code>[1 −2]</code> لما تضربها في <code>[4, 3]</code> تطلع ‎-2، ودي نفسها <code>[1, −2] · [4, 3]</code>.</p>
<p>ولو المتجه طوله 1 (اسمه متجه وحدة)، الضرب النقطي معاه = طول الضل بالظبط. عشان كده بنستخدم <code>normalize</code> كتير في الجرافيكس.</p>''')

P.append('<h3>كود: الضرب النقطي في C++</h3>' + code([
    ('float dot(const float* v, const float* w, int n)', 'دالة بتاخد متجهين (كعنوان أول رقم في كل واحد، محاضرة 1!) وعدد الأرقام <code>n</code>.'),
    ('{', f'{B_OPEN} الدالة.'),
    ('    float sum = 0.0f;', 'المجموع يبدأ من صفر.'),
    ('    for (int i = 0; i < n; i++)', 'لف على الأرقام واحد واحد.'),
    ('        sum += v[i] * w[i];', 'اضرب الرقمين اللي قصاد بعض وزوّدهم على المجموع.'),
    ('    return sum;', 'رجّع النتيجة.'),
    ('}', f'{B_CLOSE} الدالة.'),
    ('// glm version: float d = glm::dot(a, b);', 'مكتبة GLM بتعمل نفس الحكاية في سطر واحد، وهنستخدمها في الكاميرا.'),
]))
P.append('<div class="result"><div class="rh">▶ النتيجة لما نعمل Run</div>' + term(rd('run/out/dot.txt')) +
         '<p style="font-size:10pt">نفس أرقام الفيديو (11 و 71 و ‎-2). والإشارة طلعت موجب ثم صفر ثم سالب، والترتيب ما فرقش.</p></div>')
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الحساب: اضرب المتقابلين واجمع.</li>
 <li>المعنى: الضل × الطول. والإشارة بتقول نفس الاتجاه ولا عكسه ولا متعامدين.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> احسب <code>[3, 4] · [4, −3]</code>. طلع صفر؟ يبقى العلاقة بينهم إيه؟</div>''' + FULL[2] + '</section>')

# ---------------------------------------------------------- 4 CAMERA
P.append('<section class="lec l4"><div class="lec-head"><div class="tag">المحاضرة 4 · CAD</div><h2>الماوس وكلاس الكاميرا</h2>'
         '<div class="meta">قناة Victor Gordan · OpenGL Tutorial 8 · <span class="ltr">youtu.be/86_pQCKOIPk</span></div></div>')
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الكاميرا = 3 حاجات: <b>إنت فين</b> (Position)، <b>بتبص فين</b> (Orientation)، و<b>فين فوق</b> (Up). الكيبورد بيحرّكك، والماوس بيلف راسك.</div>''')

P.append('<h3>كود 1: ملف camera.h</h3>' + code([
    ('#ifndef CAMERA_CLASS_H', 'حماية: لو الملف ده اتضم قبل كده، اتخطاه.'),
    ('#define CAMERA_CLASS_H', 'علّم إن الملف اتضم خلاص.'),
    ('#include <glad/glad.h>', 'دوال OpenGL.'),
    ('#include <GLFW/glfw3.h>', 'الشباك والكيبورد والماوس.'),
    ('#include <glm/glm.hpp>', 'مكتبة الرياضيات: متجهات ومصفوفات.'),
    ('#include <glm/gtc/matrix_transform.hpp>', 'فيها <code>lookAt</code> و <code>perspective</code>.'),
    ('#include <glm/gtc/type_ptr.hpp>', 'فيها <code>value_ptr</code> (بتطلّع عنوان المصفوفة).'),
    ('#include <glm/gtx/rotate_vector.hpp>', 'فيها <code>rotate</code> (لف متجه).'),
    ('#include <glm/gtx/vector_angle.hpp>', 'فيها <code>angle</code> (الزاوية بين متجهين).'),
    ('#include "shaderClass.h"', 'كلاس الـ Shader من الدروس اللي فاتت.'),
    ('class Camera', 'بنعرّف كلاس اسمه Camera.'),
    ('{', f'{B_OPEN} الكلاس.'),
    ('public:', 'كل اللي جاي ينفع نستخدمه من برا الكلاس.'),
    ('    glm::vec3 Position;', 'مكان الكاميرا (x, y, z).'),
    ('    glm::vec3 Orientation = glm::vec3(0.0f, 0.0f, -1.0f);', 'بتبص فين: لقدام. في OpenGL «قدام» = سالب z.'),
    ('    glm::vec3 Up = glm::vec3(0.0f, 1.0f, 0.0f);', 'فين فوق: محور y.'),
    ('    int width;', 'عرض الشباك.'),
    ('    int height;', 'طول الشباك.'),
    ('    float speed = 0.1f;', 'سرعة المشي.'),
    ('    float sensitivity = 100.0f;', 'قد إيه حركة الماوس بتلف الكاميرا.'),
    ('    bool firstClick = true;', 'دي أول ضغطة ماوس؟ (عشان الكاميرا ما تنطش).'),
    ('    Camera(int width, int height, glm::vec3 position);', 'الـ Constructor: بيجهّز الكاميرا أول ما تتعمل.'),
    ('    void Matrix(float FOVdeg, float nearPlane, float farPlane, Shader& shader, const char* uniform);', 'دالة بتعمل مصفوفة الكاميرا وتبعتها للـ Shader.'),
    ('    void Inputs(GLFWwindow* window);', 'دالة بتقرا الكيبورد والماوس.'),
    ('};', f'{B_CLOSE} الكلاس.'),
    ('#endif', f'{B_CLOSE} الحماية اللي في أول الملف.'),
]) + nores('ملف الـ header مجرد «تعريف»: بيقول الكاميرا فيها إيه، ومش بيرسم حاجة لوحده. أول صورة هتظهر بعد <b>كود 5</b>.'))

P.append('<h3>كود 2: الـ Constructor</h3>' + code([
    ('Camera::Camera(int width, int height, glm::vec3 position)', 'بياخد عرض وطول الشباك، ومكان البداية.'),
    ('{', f'{B_OPEN} الدالة.'),
    ('    Camera::width = width;', 'احفظ العرض جوه الكاميرا. كتبنا <code>Camera::</code> عشان نفرّقه عن اللي داخل بنفس الاسم.'),
    ('    Camera::height = height;', 'احفظ الطول.'),
    ('    Position = position;', 'حط الكاميرا في مكان البداية.'),
    ('}', f'{B_CLOSE} الدالة.'),
]) + nores('مفيش حاجة بتترسم هنا. الـ Constructor بس بيحفظ الأرقام: الكاميرا بقت في المكان (0, 0, 2) وبتبص لقدام.'))

P.append('<h3>كود 3: دالة Matrix</h3>' + code([
    ('void Camera::Matrix(float FOVdeg, float nearPlane, float farPlane, Shader& shader, const char* uniform)', 'بتاخد: زاوية الرؤية، أقرب وأبعد مسافة، الـ Shader، واسم الخانة.'),
    ('{', f'{B_OPEN} الدالة.'),
    ('    glm::mat4 view = glm::mat4(1.0f);', 'مصفوفة «محايدة» (ما بتغيرش حاجة) هنحط فيها الـ View.'),
    ('    glm::mat4 projection = glm::mat4(1.0f);', 'ونفس الكلام للـ Projection.'),
    ('    view = glm::lookAt(Position, Position + Orientation, Up);', '«أنا واقف هنا، باصص على النقطة اللي قدامي، وراسي لفوق».'),
    ('    projection = glm::perspective(glm::radians(FOVdeg), (float)width / height, nearPlane, farPlane);', 'بتخلي البعيد يبان صغير. محتاجة: الزاوية بالـ radians، نسبة العرض للطول، أقرب وأبعد مسافة.'),
    ('    glUniformMatrix4fv(glGetUniformLocation(shader.ID, uniform), 1, GL_FALSE, glm::value_ptr(projection * view));', 'اضرب المصفوفتين وابعت النتيجة لخانة الـ Shader. نفس خطوات محاضرة 2 بالظبط، بس مصفوفة بدل لون.'),
    ('}', f'{B_CLOSE} الدالة.'),
]) + nores('الدالة دي بتحسب أرقام المصفوفة وتبعتها، والرسم نفسه بيحصل لما الأكواد 3 و 4 و 5 يشتغلوا مع بعض. النتيجة بعد <b>كود 5</b>.'))

P.append('<h3>كود 4: الاستخدام في main</h3>' + code([
    ('#include "Camera.h"', 'ضم ملف الكاميرا.'),
    ('Camera camera(width, height, glm::vec3(0.0f, 0.0f, 2.0f));', 'اعمل كاميرا، وحطها ورا الشكل بمسافة 2.'),
    ('glEnable(GL_DEPTH_TEST);', 'خلي اللي قدام يغطي اللي ورا.'),
    ('while (!glfwWindowShouldClose(window))', 'اللوب الرئيسي. كل لفة = فريم.'),
    ('{', f'{B_OPEN} اللوب.'),
    ('    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);', 'لون الخلفية: كحلي غامق.'),
    ('    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);', 'امسح الألوان والعمق من الفريم اللي فات.'),
    ('    shaderProgram.Activate();', 'شغّل الـ Shader.'),
    ('    camera.Inputs(window);', 'اقرا الأزرار وحرّك الكاميرا.'),
    ('    camera.Matrix(45.0f, 0.1f, 100.0f, shaderProgram, "camMatrix");', 'ابني المصفوفة (زاوية 45°، تشوف من 0.1 لـ 100) وابعتها لخانة <code>camMatrix</code>.'),
    ('    // ... draw ...', 'هنا بنرسم الأشكال.'),
    ('}', f'{B_CLOSE} اللوب.'),
]) + nores('اللوب جاهز ومستني الـ Vertex Shader اللي في <b>كود 5</b> عشان يعرف يستخدم المصفوفة. النتيجة تحته.'))

P.append('<h3>كود 5: الـ Vertex Shader</h3>' + code([
    ('#version 330 core', 'لغة GLSL نسخة 3.3.'),
    ('layout (location = 0) in vec3 aPos;', 'مكان كل نقطة.'),
    ('layout (location = 1) in vec3 aColor;', 'لون كل نقطة.'),
    ('layout (location = 2) in vec2 aTex;', 'إحداثيات الصورة (texture) على كل نقطة.'),
    ('out vec3 color;', 'هنبعت اللون للـ Fragment Shader.'),
    ('out vec2 texCoord;', 'وإحداثيات الصورة كمان.'),
    ('uniform mat4 camMatrix;', 'خانة مصفوفة الكاميرا، جاية من الـ C++.'),
    ('void main()', 'بتشتغل مرة لكل نقطة.'),
    ('{', f'{B_OPEN} الدالة.'),
    ('    gl_Position = camMatrix * vec4(aPos, 1.0);', 'مكان النقطة على الشاشة = المصفوفة × مكانها. والـ 1.0 رقم رابع لازم عشان الضرب في 4×4.'),
    ('    color = aColor;', 'عدّي اللون زي ما هو.'),
    ('    texCoord = aTex;', 'عدّي إحداثيات الصورة زي ما هي.'),
    ('}', f'{B_CLOSE} الدالة.'),
]) + res('<img src="img/cam_start.png" style="width:75mm;display:block;margin:0 auto;border-radius:2mm"><div style="text-align:center;font-size:9pt;color:#5b6372;margin:1.5mm 0 2mm">أول ما البرنامج يشتغل: الكاميرا في (0, 0, 2) وبتبص على الهرم، والأرضية بالمنظور (البعيد أصغر)</div>', '▶ النتيجة لما نعمل Run (الأكواد 1 لـ 5 مع بعض)'))

P.append('<h3>كود 6: الكيبورد</h3>' + code([
    ('void Camera::Inputs(GLFWwindow* window)', 'دالة قراءة الأزرار.'),
    ('{', f'{B_OPEN} الدالة.'),
    ('    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)', 'هل زرار W مضغوط؟'),
    ('        Position += speed * Orientation;', 'امشي خطوة لقدام في اتجاه نظرك.'),
    ('    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)', 'هل A مضغوط؟'),
    ('        Position += speed * -glm::normalize(glm::cross(Orientation, Up));', 'امشي شمال. الدالة <code>cross</code> بتدّي اتجاه يمينك، والسالب = شمالك.'),
    ('    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)', 'هل S مضغوط؟'),
    ('        Position += speed * -Orientation;', 'امشي لورا.'),
    ('    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)', 'هل D مضغوط؟'),
    ('        Position += speed * glm::normalize(glm::cross(Orientation, Up));', 'امشي يمين. و <code>normalize</code> بتخلي الطول 1 عشان السرعة تفضل ثابتة.'),
    ('    if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS)', 'هل Space مضغوط؟'),
    ('        Position += speed * Up;', 'اطلع لفوق.'),
    ('    if (glfwGetKey(window, GLFW_KEY_LEFT_CONTROL) == GLFW_PRESS)', 'هل Ctrl مضغوط؟'),
    ('        Position += speed * -Up;', 'انزل لتحت.'),
    ('    if (glfwGetKey(window, GLFW_KEY_LEFT_SHIFT) == GLFW_PRESS)', 'هل Shift مضغوط؟'),
    ('        speed = 0.4f;', 'اجري: السرعة 4 أضعاف.'),
    ('    else if (glfwGetKey(window, GLFW_KEY_LEFT_SHIFT) == GLFW_RELEASE)', 'لو سبت Shift…'),
    ('        speed = 0.1f;', '…ارجع للسرعة العادية.'),
]) + '<p class="note">كل زرار ليه <code>if</code> لوحده (مش <code>else if</code>) عشان تقدر تدوس W و D مع بعض وتمشي بالورب.</p>')

cam1 = [shot('cam_start', 'البداية<br>' + L('Position (0, 0, 2)')),
        shot('cam_W', '<b>W</b> × 10 فريم<br>قرّبنا'),
        shot('cam_S', '<b>S</b> × 10 فريم<br>بعدنا'),
        shot('cam_D', '<b>D</b> × 10 فريم<br>إحنا رحنا يمين، فالهرم بان شمال'),
        shot('cam_Space', '<b>Space</b> × 8 فريم<br>طلعنا لفوق'),
        shot('cam_WD', '<b>W + D</b> مع بعض<br>مشي بالورب')]
P.append('<div class="result"><div class="rh">▶ النتيجة لما نعمل Run ونضغط كل زرار</div>' + grid(cam1, 3) +
         '<p style="font-size:10pt">كل فريم الكاميرا بتتحرك 0.1، فـ 10 فريمات = وحدة كاملة. (الهرم هنا ملوّن بدل صورة الطوب اللي في الفيديو عشان الحركة تبان أوضح.)</p></div>')

P.append('<h3>كود 7: الماوس (تكملة دالة Inputs)</h3>' + code([
    ('    if (glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS)', 'هل زرار الماوس الشمال مضغوط؟'),
    ('    {', f'{B_OPEN} «لو مضغوط».'),
    ('        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN);', 'اخفي سهم الماوس.'),
    ('        if (firstClick)', 'لو دي أول ضغطة…'),
    ('        {', f'{B_OPEN}.'),
    ('            glfwSetCursorPos(window, (width / 2), (height / 2));', '…حط الماوس في نص الشاشة الأول، عشان الكاميرا ما تنطش.'),
    ('            firstClick = false;', 'وعلّم إن أول ضغطة خلصت.'),
    ('        }', f'{B_CLOSE}.'),
    ('        double mouseX;', 'متغير لمكان الماوس الأفقي.'),
    ('        double mouseY;', 'متغير لمكانه الرأسي.'),
    ('        glfwGetCursorPos(window, &mouseX, &mouseY);', 'هات مكان الماوس. بنبعت العناوين بـ <code>&amp;</code> عشان الدالة تكتب فيهم (محاضرة 1!).'),
    ('        float rotX = sensitivity * (float)(mouseY - (height / 2)) / height;', 'الماوس بعد عن النص رأسياً قد إيه = هنبص لفوق/تحت قد إيه.'),
    ('        float rotY = sensitivity * (float)(mouseX - (width / 2)) / width;', 'وبعد أفقياً قد إيه = هنبص يمين/شمال قد إيه.'),
    ('        glm::vec3 newOrientation = glm::rotate(Orientation, glm::radians(-rotX), glm::normalize(glm::cross(Orientation, Up)));', 'جرّب تلف النظر لفوق/تحت حوالين محور يمينك، وحط النتيجة في متغير مؤقت.'),
    ('        if (!(glm::angle(newOrientation, Up) <= glm::radians(5.0f) || glm::angle(newOrientation, -Up) <= glm::radians(5.0f)))', 'لو الاتجاه الجديد <b>مش</b> قريب أوي (أقل من 5°) من فوق خالص أو تحت خالص…'),
    ('            Orientation = newOrientation;', '…اقبله. كده الكاميرا عمرها ما تتقلب على ضهرها.'),
    ('        Orientation = glm::rotate(Orientation, glm::radians(-rotY), Up);', 'لف يمين/شمال حوالين محور فوق، من غير شروط.'),
    ('        glfwSetCursorPos(window, (width / 2), (height / 2));', 'رجّع الماوس للنص عشان نقيس الحركة الجاية من الصفر.'),
    ('    }', f'{B_CLOSE} «لو مضغوط».'),
    ('    else if (glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_RELEASE)', 'لو سبت زرار الماوس…'),
    ('    {', f'{B_OPEN}.'),
    ('        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL);', 'رجّع السهم يظهر.'),
    ('        firstClick = true;', 'جهّز «أول ضغطة» للمرة الجاية.'),
    ('    }', f'{B_CLOSE}.'),
    ('}', f'{B_CLOSE} دالة Inputs كلها.'),
]))

cam2 = [shot('cam_mouseR', 'الماوس يمين<br>لفّينا 25° يمين'),
        shot('cam_mouseDown', 'طلعنا لفوق وبصينا لتحت<br>شايفين الهرم من فوق'),
        shot('cam_start', L('FOV = 45°') + '<br>الطبيعي'),
        shot('cam_fov90', L('FOV = 90°') + '<br>المشهد أوسع والهرم أصغر')]
ct = rd('run/out/camera.txt').split('\n')
i1 = [i for i, l in enumerate(ct) if 'normal drag' in l][0]
i2 = [i for i, l in enumerate(ct) if 'very fast' in l][0]
P.append('<div class="result"><div class="rh">▶ النتيجة لما نعمل Run ونحرك الماوس</div>' + grid(cam2, 2) + '</div>')
P.append('<div class="result"><div class="rh">▶ تجربة شرط الـ 5° (سحب الماوس لفوق على طول)</div>' + term('\n'.join(ct[i1:i1+15])) +
         '<p style="font-size:10pt">مع سحب عادي، الزاوية مع <code>Up</code> بتنزل لحد 10° وتقف. الشرط شغال.</p>' +
         term('\n'.join(ct[i2:i2+5])) +
         '<p style="font-size:10pt"><b>اكتشاف من التشغيل:</b> لو الماوس اتحرك بسرعة جداً في فريم واحد، الخطوة بتنط فوق منطقة الـ 5° والكاميرا تتقلب. ده عيب في كود الفيديو، ومش هتلاحظه غالباً مع حركة الإيد العادية. الحل الأأمن (زي learnopengl): تخزّن زاوية البص لفوق كرقم وتحصرها بين ‎-89° و 89°.</p></div>')
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الكاميرا = مكان + بتبص فين + فين فوق.</li>
 <li>دالة <code>lookAt</code> + دالة <code>perspective</code> = مصفوفة، بتتبعت كـ Uniform.</li>
 <li>الكيبورد بيغيّر المكان، والماوس بيغيّر الاتجاه.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> غيّر <code>sensitivity</code> لـ 50 ثم 200، وغيّر الـ FOV من 45 لـ 90.</div>''' + FULL[3] + '</section>')

# ---------------------------------------------------------- links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<p style="color:#5b6372">كود الكاميرا لوحده فيه الأربع محاضرات:</p>
<table class="flow">
 <tr><td class="n">1</td><td><b>المؤشرات:</b> الدالة <code>glfwGetCursorPos</code> بتاخد عناوين بـ <code>&amp;</code>، والدالة <code>value_ptr</code> بترجّع عنوان.</td></tr>
 <tr><td class="n">2</td><td><b>الـ Uniforms:</b> مصفوفة الكاميرا بتتبعت بنفس الـ 3 خطوات بتوع اللون.</td></tr>
 <tr><td class="n">3</td><td><b>الضرب النقطي:</b> جوه <code>glm::angle</code> اللي بتمنع الكاميرا تتقلب، وجوه <code>lookAt</code>.</td></tr>
 <tr><td class="n">4</td><td><b>الكاميرا:</b> بتجمع ده كله، وده أساس أداة الـ CAD بتاعتك.</td></tr>
</table>
<h3>بكره (الإثنين 26-10)</h3>
<ul><li>برمجة: تمارين Pointers من Exercism.</li><li>رسم: ألوان لكل نقطة (Vertex Attributes).</li>
<li>رياضيات: تمارين الضرب النقطي من Khan Academy.</li><li>الـ CAD: تخزين النقط في <code>std::vector</code>.</li></ul>
<h3>المصادر</h3>
<ul style="font-size:10pt">
 <li>المؤشرات: <span class="ltr">youtube.com/watch?v=DTxHyVn0ODg</span></li>
 <li>الـ Uniforms: <span class="ltr">youtube.com/watch?v=DE6Xlx_kbo0</span></li>
 <li>الضرب النقطي: <span class="ltr">youtube.com/watch?v=LyGKycYT2v0</span></li>
 <li>الكاميرا: <span class="ltr">youtube.com/watch?v=86_pQCKOIPk</span></li>
</ul></section>''')

doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 2 - اليوم الأول</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
open('week2_day1_v3.html', 'w', encoding='utf-8').write(doc)
weasyprint.HTML('week2_day1_v3.html', base_url='.').write_pdf('Week2_Day1_Sunday.pdf')
print('built')
