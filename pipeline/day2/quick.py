# "20 minutes only" page + self-test questions, for Day 1 and Day 2. Also tags reference-only sections.
import html, re

exec(open('/home/claude/day2/hl_src.py', encoding='utf-8').read())
KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4|struct|size_t|auto)\b'

CSS = '''
.quick { page-break-after: always; }
.quick h2 { font-size: 18pt; margin: 0 0 1mm; }
.quick .qsub { color:#5b6372; font-size:10.5pt; margin:0 0 4mm; }
.method { background:#f0fdf4; border:1px solid #bbf7d0; border-radius:3mm; padding:3mm 5mm; margin:0 0 5mm; font-size:10pt; }
.method ol { margin:1mm 0 0; }
.qcard { border:1px solid #e2e6ee; border-radius:3mm; margin:0 0 4mm; page-break-inside:avoid; overflow:hidden; }
.qcard .qh { padding:2mm 4mm; color:#fff; font-weight:bold; font-size:11pt; }
.qcard .qb { padding:2.5mm 4mm 3mm; font-size:10pt; }
.qcard ul { margin:0 0 2mm; padding-right:5mm; }
.qcard li { margin-bottom:0.6mm; }
.qcard .code { margin:1.5mm 0 2mm; font-size:8.6pt; }
.qrow { margin:1mm 0; }
.qrow b { color:#b91c1c; }
.qrow.qrun b { color:#15803d; }
.selftest { page-break-inside:auto; }
.selftest h3 { margin-top:5mm; }
.qa { border-bottom:1px dashed #d1d5db; padding:1.5mm 0; font-size:10pt; page-break-inside:avoid; }
.qa .q { font-weight:bold; }
.qa summary { cursor:pointer; font-weight:bold; list-style:none; }
.qa summary::-webkit-details-marker { display:none; }
.qa summary::before { content:"❓ "; }
.qa details[open] summary::before { content:"✅ "; }
.qa .a { color:#15803d; margin-top:1mm; }
.answers { page-break-before: always; }
.tag-ref { display:inline-block; font-size:8.8pt; font-weight:bold; color:#475569; background:#e2e8f0; border-radius:10mm; padding:0.3mm 2.5mm; margin-right:2mm; vertical-align:middle; }
'''

def codeblock(lines):
    return '<div class="code">' + '\n'.join(f'<i class="ln">{i}</i>' + hl(l) for i, l in enumerate(lines, 1)) + '</div>'

def card(color, title, remember, pattern, mistake, run):
    return (f'<div class="qcard"><div class="qh" style="background:{color}">{title}</div><div class="qb">'
            '<b>ثبّت دول:</b><ul>' + ''.join(f'<li>{r}</li>' for r in remember) + '</ul>'
            '<b>النمط اللي هتكرره:</b>' + codeblock(pattern)
            + f'<div class="qrow"><b>⚠️ أشهر غلطة:</b> {mistake}</div>'
            + f'<div class="qrow qrun"><b>▶ شغّل ده بس:</b> {run}</div></div></div>')

METHOD = '''<div class="method"><b>كل جلسة في 30-40 دقيقة:</b><ol>
<li>شوف الفيديو بسرعة 1.5×.</li><li>اقرا الكارت بتاع المحاضرة في الصفحة دي.</li>
<li>شغّل البرنامج اللي مكتوب في «شغّل ده بس»، وغيّر فيه حاجة واحدة من «جرّب بإيدك».</li>
<li>جاوب «اختبر نفسك» من غير ما تبص، وبعدين شوف الإجابات.</li></ol>
باقي الملف مرجع: ارجعله لما تحتاج تفهم سطر معين. الأقسام المعلّمة <span class="tag-ref">📚 مرجع</span> مش لازم تتقري كل يوم.</div>'''

DAY1_CARDS = [
 card('#2563eb', 'البرمجة: Pointers', [
   'الـ Pointer = عنوان مكان في الذاكرة.',
   'علامة <code>&amp;x</code> = هات العنوان، و <code>*p</code> = روح للعنوان.',
   'القيمة <code>nullptr</code> = عنوان فاضي، ماتقراش منه.',
   'كل <code>new</code> ليها <code>delete</code>، و <code>new[]</code> ليها <code>delete[]</code>.'],
   ['int x = 8;', 'int* p = &x;   // p = address of x', '*p = 10;       // now x = 10'],
   'تقرا من <code>nullptr</code> أو بعد <code>delete</code> = البرنامج يقع.', 'كود 4 (<code>p4.cpp</code>).'),
 card('#0d9488', 'الرسم: Uniforms', [
   'الـ Uniform = خانة في الـ Shader بتملاها من الـ C++، وقيمتها واحدة لكل البكسلات.',
   'أي برنامج OpenGL = تجهيز ← لوب (امسح، ارسم، اعرض، اقرا الأحداث) ← تنضيف.',
   'الـ Shader بيتكتب بلغة GLSL، و <code>vec4</code> = 4 أرقام مع بعض.'],
   ['uniform vec4 u_Color;                              // shader', 'int loc = glGetUniformLocation(shader, "u_Color");  // C++', 'glUniform4f(loc, 0.2f, 0.3f, 0.8f, 1.0f);'],
   'اسم الخانة غلط (يرجع ‎-1)، أو نسيت <code>glUseProgram</code>: شاشة سودا من غير رسالة.', 'البرنامج 2 (اللون المتحرك).'),
 card('#c2410c', 'الرياضيات: الضرب النقطي', [
   'اضرب المتقابلين واجمع = رقم واحد.',
   'الإشارة: موجب = نفس الناحية، صفر = متعامدين، سالب = عكس بعض.',
   'المعنى: طول الضل × الطول.'],
   ['[1, 2] . [3, 4] = 1*3 + 2*4 = 11'],
   'تفتكر إن النتيجة متجه: هي رقم.', '<code>dot.cpp</code>.'),
 card('#7c3aed', 'الـ CAD: الكاميرا', [
   'الكاميرا = Position (فين) + Orientation (بتبص فين) + Up (فين فوق).',
   'الكيبورد بيغيّر Position، والماوس بيلف Orientation.',
   'المصفوفة = projection × view، وبتتبعت كـ Uniform كل فريم.'],
   ['view = glm::lookAt(Position, Position + Orientation, Up);', 'projection = glm::perspective(glm::radians(45.0f), (float)width / height, 0.1f, 100.0f);', 'if (W pressed) Position += speed * Orientation;'],
   'ترتيب الضرب معكوس، أو نسيت <code>glEnable(GL_DEPTH_TEST)</code>.', 'مشروع الكاميرا (5 ملفات) مرة واحدة، وجرّب WASD والماوس.'),
]

DAY1_QA = [
 ('البرمجة: Pointers', [
   ('بعد <code>int x = 5; int* p = &amp;x; *p = 7;</code> قيمة <code>x</code> بقت كام؟', 'بقت 7، لأن <code>*p</code> راح لعنوان x وغيّره.'),
   ('إيه الفرق بين النجمة في <code>int* p</code> وفي <code>*p = 7</code>؟', 'الأولى بتعرّف Pointer. التانية معناها «روح للعنوان».'),
   ('إيه اللي يحصل لو قريت من <code>nullptr</code>؟', 'البرنامج يقع (crash).'),
   ('حجزت بـ <code>new char[8]</code>. ترجّعها إزاي؟', 'بـ <code>delete[]</code> بالأقواس.')]),
 ('الرسم: Uniforms', [
   ('الفرق بين Attribute و Uniform؟', 'الـ Attribute قيمته مختلفة لكل ركن. الـ Uniform قيمة واحدة لكل الأركان والبكسلات.'),
   ('إيه الـ 3 خطوات عشان تبعت Uniform؟', 'تعرّفه في الـ Shader، تجيب رقمه بـ <code>glGetUniformLocation</code>، تبعت القيمة بـ <code>glUniform…</code>.'),
   ('لو <code>glGetUniformLocation</code> رجّعت ‎-1، معناها إيه؟', 'مش لاقية الخانة: الاسم غلط، أو الخانة مش مستخدمة في الـ Shader.'),
   ('لازم تعمل إيه قبل <code>glUniform4f</code>؟', 'لازم <code>glUseProgram(shader)</code> الأول.')]),
 ('الرياضيات: الضرب النقطي', [
   ('كام ناتج <code>[1, 2] · [3, 4]</code>؟', 'الناتج 11.'),
   ('الضرب النقطي طلع صفر. ده معناه إيه؟', 'المتجهين متعامدين (90°).'),
   ('نتيجة الضرب النقطي متجه ولا رقم؟', 'رقم.')]),
 ('الـ CAD: الكاميرا', [
   ('إيه الـ 3 متجهات اللي بتوصف الكاميرا؟', 'هما Position و Orientation و Up.'),
   ('ليه بنكتب <code>Position + Orientation</code> في <code>lookAt</code>؟', 'لأن <code>lookAt</code> عايزة نقطة تبصلها، فبناخد نقطة قدامك بخطوة.'),
   ('زرار W بيعمل إيه في الكود؟', 'السطر <code>Position += speed * Orientation;</code> يعني خطوة لقدام.'),
   ('ليه بنرجّع الماوس لنص الشاشة كل فريم؟', 'عشان نقيس الحركة الجديدة بس. لو ما رجعش، الكاميرا هتفضل تلف لوحدها.')]),
]

DAY2_CARDS = [
 card('#2563eb', 'البرمجة: C والـ Pointers', [
   'لغة C هي أصل C++ (من 1972)، صغيرة وسريعة، والذاكرة بإيدك.',
   'الأمر <code>p++</code> = العنصر اللي بعده (مش البايت اللي بعده).',
   'عشان دالة تغيّر متغيرك: ابعتلها عنوانه.'],
   ['printf("%d\\n", x);                       // = std::cout << x', 'int* a = malloc(5 * sizeof(int));  free(a);   // = new int[5]; delete[] a;', 'void doubleIt(int* n) { *n = *n * 2; }    doubleIt(&score);'],
   '<code>malloc</code> من غير <code>sizeof</code>، أو نسيت <code>free</code>.', 'برنامج 4 (<code>double_it.cpp</code>).'),
 card('#0d9488', 'الرسم: Vertex Attributes', [
   'الـ Vertex = ركن بكل بياناته (مكان، لون…)، وكل بيان اسمه Attribute.',
   'الـ size = كام رقم، والـ stride = طول الركن كله بالبايت، والـ offset = البيان بيبدأ فين جوه الركن.',
   'رقم الـ Attribute لازم يطابق <code>layout(location = …)</code>.'],
   ['// vertex = x, y, r, g, b   (5 floats = 20 bytes)', 'glEnableVertexAttribArray(1);', 'glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 5, (void*)(sizeof(float) * 2));'],
   'stride أو offset غلط: الشكل أو الألوان تبوظ من غير أي رسالة.', 'البرنامج 2 (<code>triangle_colors.cpp</code>).'),
 card('#c2410c', 'الرياضيات: الطول', [
   'الطول = جذر (المتجه · نفسه).', 'في 2D ده فيثاغورس بالظبط.'],
   ['length = sqrt(a . a)        // |[2,5]| = sqrt(4 + 25) = sqrt(29)'],
   'تنسى الجذر (هيطلع مربع الطول).', '<code>dot_length.cpp</code>.'),
 card('#7c3aed', 'الـ CAD: std::vector', [
   'قايمة بتكبر لوحدها وعارفة حجمها.',
   'علامة <code>&amp;</code> في اللوب والدوال لو هتعدّل، و <code>const&amp;</code> لو هتقرا بس.',
   'لما بتكبر بتتنقل، فماتحتفظش بعنوان عنصر جواها.'],
   ['std::vector<Point> points;', 'points.push_back({ 100, 50 });', 'for (const Point& p : points) { ... }'],
   'تشيل عنوان عنصر وبعدين تعمل <code>push_back</code>.', 'برنامج 4 (<code>cad_points.cpp</code>).'),
]

DAY2_QA = [
 ('البرمجة: C والـ Pointers', [
   ('علامة <code>%d</code> في <code>printf</code> معناها إيه؟', 'مكان لرقم صحيح.'),
   ('الأمر <code>malloc(5)</code> بيحجز كام؟', 'بيحجز 5 بايت بس، مش 5 أرقام. عشان 5 أرقام: <code>malloc(5 * sizeof(int))</code>.'),
   ('لو <code>p</code> بيشاور على <code>arr[0]</code>، بعد <code>p++</code> بيشاور على إيه؟', 'على <code>arr[1]</code>، والعنوان زاد 4 بايت.'),
   ('ليه <code>doubleIt</code> بتاخد <code>int*</code> مش <code>int</code>؟', 'عشان تغيّر الأصل. لو أخدت <code>int</code> هتاخد نسخة.')]),
 ('الرسم: Vertex Attributes', [
   ('الـ Vertex = المكان بس؟', 'لأ. الـ Vertex = ركن بكل بياناته.'),
   ('ركن فيه x, y, r, g, b (float). الـ stride كام بايت؟ والـ offset بتاع اللون كام؟', 'الـ stride = 20 بايت، والـ offset = 8 بايت.'),
   ('نسيت <code>glEnableVertexAttribArray(1)</code>. هيحصل إيه؟', 'اللون هياخد القيمة الافتراضية (أسود)، ومن غير رسالة خطأ.'),
   ('ليه المثلث طلع متدرّج؟', 'كارت الشاشة بيخلط ألوان الأركان لكل بكسل (interpolation).')]),
 ('الرياضيات: الطول', [
   ('كام ناتج <code>[2, 5] · [7, 1]</code>؟', 'الناتج 19.'),
   ('طول <code>[3, 4]</code> = ؟', 'الطول 5 (لأن √(9 + 16) = √25).'),
   ('الضرب <code>a · a</code> بيساوي إيه؟', 'مربع طول a.')]),
 ('الـ CAD: std::vector', [
   ('إزاي تضيف عنصر في الآخر؟', 'بـ <code>push_back</code>.'),
   ('الفرق بين <code>v[5]</code> و <code>v.at(5)</code>؟', 'الدالة <code>at</code> بتتأكد من الرقم وبتوقف برسالة واضحة، والأقواس <code>[]</code> مش بتتأكد.'),
   ('ليه <code>printPoints</code> بتاخد <code>const&amp;</code>؟', 'من غير نسخ القايمة، ومن غير ما تعدّل فيها.'),
   ('ليه خطر تحتفظ بعنوان عنصر جوه vector؟', 'لأن <code>push_back</code> ممكن ينقله لمكان جديد، والعنوان القديم يبوظ.')]),
]

def quick_section(cards, qa, mode):
    h = ['<section class="quick"><h2>⭐ لو معاك 20 دقيقة بس</h2><div class="qsub">ده أهم حاجة في اليوم. ذاكر الصفحة دي، والباقي ارجعله لما تحتاجه.</div>', METHOD]
    h += cards
    h.append('</section><section class="selftest"><h2>❓ اختبر نفسك</h2>')
    h.append('<div class="qsub">' + ('دوس على السؤال عشان تشوف الإجابة. جاوب في دماغك الأول.' if mode == 'web' else 'جاوب في دماغك الأول، والإجابات في آخر صفحة في الملف.') + '</div>')
    n = 0
    for title, items in qa:
        h.append(f'<h3>{title}</h3>')
        for q, a in items:
            n += 1
            if mode == 'web':
                h.append(f'<div class="qa"><details><summary>{n}. {q}</summary><div class="a">{a}</div></details></div>')
            else:
                h.append(f'<div class="qa"><span class="q">{n}.</span> {q}</div>')
    h.append('</section>')
    return ''.join(h)

def answers_section(qa):
    h = ['<section class="answers"><h2>✅ إجابات «اختبر نفسك»</h2>']
    n = 0
    for title, items in qa:
        h.append(f'<h3>{title}</h3>')
        for q, a in items:
            n += 1
            h.append(f'<div class="qa"><span class="q">{n}.</span> <span class="a">{a}</span></div>')
    h.append('</section>')
    return ''.join(h)

REF_KEYS = ('كلمة كلمة', 'ليه كتبنا', 'إيه اللي يحصل لو غلطت')
def tag_reference(doc):
    def f(m):
        if any(k in m.group(2) for k in REF_KEYS):
            return m.group(1) + m.group(2) + ' <span class="tag-ref">📚 مرجع</span></h3>'
        return m.group(0)
    return re.sub(r'(<h3[^>]*>)(.*?)</h3>', f, doc)
