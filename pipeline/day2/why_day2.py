import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day2/exp/'
def rd(p): return open(p).read()
def pick(p, keep, limit=6):
    out = [l for l in rd(p).splitlines() if any(k in l for k in keep)]
    return '\n'.join(out[:limit])
def first_err(p):
    for l in rd(p).splitlines():
        if 'error' in l or 'warning' in l:
            return l.split('/')[-1]
    return ''

def build_c():
    S = []
    S.append(step(1, 'سطر #include <stdio.h>', ['#include <stdio.h>'],
        'فيه تعريف <code>printf</code>. القاعدة زي C++: ضم المكتبة اللي فيها الحاجة اللي بتستخدمها.',
        'req', 'شيلناه: في C (مش C++) الـ compiler بيطلّع <b>تحذير</b> بس ويكمّل، والبرنامج اشتغل. ده فرق مهم: C أكثر تساهلاً، وفي compilers أحدث (GCC 14 مثلاً) نفس الحالة بقت خطأ. ماتعتمدش على التساهل ده.',
        term('\n'.join(rd(X + 'c_no_stdio.build').splitlines()[:1]).split('/')[-1] + '\nC was born in 1972\nHello from C!'), True))
    S.append(step(2, 'int main(void) و return 0', ['int main(void)', 'return 0;'],
        'البداية زي C++. <code>return 0</code> بتقول لنظام التشغيل «خلصت من غير مشاكل»، وأي رقم تاني معناه «في مشكلة». ده اللي بيستخدمه البرنامج اللي شغّلك (زي Visual Studio) عشان يعرف النتيجة.',
        'imp', 'في <code>main</code> بالذات، لو نسيتها الـ compiler بيعتبرها 0 لوحده (من C99). في أي دالة تانية بترجّع رقم، لازم تكتب <code>return</code>.'))
    S.append(step(3, 'علامات % في printf', ['printf("C was born in %d\\n", year);'],
        '<code>printf</code> مش بتعرف نوع المتغير لوحدها (عكس <code>cout</code>). إنت اللي بتقولها: <code>%d</code> رقم صحيح، <code>%f</code> عشري، <code>%p</code> عنوان.',
        'req', 'خلينا <code>year</code> نوعها <code>float</code> وسبنا <code>%d</code>: الـ compiler حذّر، والبرنامج طبع رقم ملوش علاقة بـ 1972.',
        term(first_err(X + 'c_wrong_format.build') + '\n' + pick(X + 'c_wrong_format.out', ['born'])), True))
    S.append(step(4, '\\n في آخر النص', ['printf("Hello from C!\\n");'],
        '<code>printf</code> مش بتنزل سطر لوحدها (عكس <code>std::endl</code>). <code>\\n</code> هو «انزل سطر».',
        'imp', 'شيلناها: الجملتين لزقوا في بعض في سطر واحد.',
        term(rd(X + 'c_no_newline.out').split('exit=')[0]), True))
    S.append(step(5, 'malloc بـ sizeof', ['int* numbers = malloc(count * sizeof(int));'],
        'زي <code>new</code>: بتحجز ذاكرة على الـ Heap. الفرق إن <code>malloc</code> بتحسب <b>بالبايت</b>، فلازم تقولها 5 أرقام × 4 بايت. ده معنى «Manual Memory Management» في الفيديو: إنت اللي بتحسب.',
        'req', 'كتبنا <code>malloc(count)</code> من غير <code>sizeof</code>: اتحجز 5 بايت بس بدل 20. البرنامج كتب برا المساحة، وأداة كشف أخطاء الذاكرة مسكته فوراً.',
        term(pick(X + 'c_no_sizeof.out', ['heap-buffer-overflow on', 'WRITE of size', 'located 0 bytes after'])), True))
    S.append(step(6, 'سطر #include <stdlib.h>', ['#include <stdlib.h>'],
        'فيه تعريف <code>malloc</code> و <code>free</code>.',
        'req', 'شيلناه: تحذير بس واشتغل، زي <code>stdio.h</code>. بس هنا الموضوع أخطر: من غير التعريف، الـ compiler ممكن يفترض نوع غلط للعنوان اللي راجع. اكتبه دايماً.',
        term(first_err(X + 'c_no_stdlib.build')), True))
    S.append(step(7, 'التأكد من NULL', ['if (numbers == NULL)', '    return 1;'],
        'لو الجهاز ما فيهوش ذاكرة كفاية، <code>malloc</code> بترجع <code>NULL</code> بدل عنوان. لو كملت واستخدمته، يبقى Pointer فاضي = crash (فاكر محاضرة امبارح؟).',
        'imp', 'في البرامج الصغيرة مش هتلاحظ حاجة، لأن الحجز تقريباً عمره ما بيفشل. بس الفيديو قال «ماتثقش في أي حاجة»، وده مثال عليها.'))
    S.append(step(8, 'شرط اللوب i < count', ['for (int i = 0; i < count; i++)'],
        'الخانات من 0 لـ 4 (5 خانات). آخر رقم صالح = <code>count - 1</code>.',
        'req', 'كتبنا <code>i &lt;= count</code>: اللوب كتب في خانة رقم 5 اللي مش بتاعتنا. C مش بتمنعك؛ الأداة هي اللي مسكتها.',
        term(pick(X + 'c_loop_equal.out', ['heap-buffer-overflow on', 'WRITE of size', 'located 0 bytes after'])), True))
    S.append(step(9, 'free', ['free(numbers);'],
        'رجوع الذاكرة إنت المسؤول عنه، مفيش حد هيعملها بدالك (مفيش Garbage Collector زي Java). ده الجزء التاني من «Manual Memory Management».',
        'imp', 'شيلناه: البرنامج اشتغل عادي وطبع كل حاجة، بس الأداة قالت في الآخر «20 بايت ضاعوا».',
        term(pick(X + 'c_no_free.out', ['LeakSanitizer', 'Direct leak', 'SUMMARY'])), True))
    S.append(step(10, 'p++ (حساب الـ Pointers)', ['p++;'],
        'أسرع طريقة تمشي بيها على مصفوفة: بدل ما تحسب مكان كل خانة، بتزق الـ Pointer خطوة. والخطوة = حجم النوع، فـ C بتحسبها لوحدها.',
        'req', 'خلينا اللوب يلف 5 مرات على مصفوفة فيها 4: الـ Pointer عدّى آخرها وقرا ذاكرة مش بتاعته. الأداة مسكتها.',
        term(pick(X + 'c_arith_past_end.out', ['p = ', 'stack-buffer-overflow on', 'READ of size'], 7)), True))
    S.append(step(11, 'الدالة بتاخد عنوان (int*) مش رقم', ['void doubleIt(int* number)', 'doubleIt(&score);'],
        'لما تبعت متغير عادي لدالة، الدالة بتاخد <b>نسخة</b> منه. أي تعديل بيحصل في النسخة بس. عشان الدالة تغيّر الأصل، لازم تبعتلها عنوانه.',
        'req', 'خلينا الدالة تاخد <code>int</code> عادي: اشتغلت من غير أخطاء، بس <code>score</code> فضل 21، لأن اللي اتضاعف كان النسخة. وجربنا كمان نبعت <code>score</code> لدالة عايزة عنوان من غير <code>&amp;</code>: الـ compiler رفض.',
        term(rd(X + 'c_by_value.out').split('exit=')[0].strip() + '\n\n(without &):  ' + first_err(X + 'c_no_ampersand.build')), True))
    return ''.join(S)

def build_va():
    S = []
    S.append(step(1, 'glEnableVertexAttribArray', ['glEnableVertexAttribArray(1);'],
        'كل مدخل لازم يتفعّل. التفعيل بيقول «اقرا المدخل ده من الـ buffer»، ومن غيره كارت الشاشة بيستخدم قيمة ثابتة افتراضية.',
        'req', 'شيلنا تفعيل المدخل 1 (اللون): كل الأركان أخدت اللون الافتراضي (0, 0, 0) = أسود، فالمثلث اختفى في الخلفية السودا. ومفيش ولا رسالة خطأ.',
        '<div class="exrow">' + img('x_ok', 'الطبيعي', '34mm') + img('x_no_enable1', 'من غير تفعيل اللون', '34mm') + '</div>', True))
    S.append(step(2, 'الـ index (أول مدخل)', ['glVertexAttribPointer(1, …)', 'layout(location = 1) in vec3 aColor;'],
        'الرقم ده هو اللي بيربط الـ C++ بالـ Shader. لازم يبقى نفس رقم <code>location</code>.',
        'req', 'غيّرناه لـ 2 في الـ C++ وسبنا الـ Shader 1: الـ Shader دوّر على المدخل 1 فلقاه مش متفعل، فأسود تاني.',
        '<div class="exrow">' + img('x_ok', 'الطبيعي', '34mm') + img('x_wrong_index', 'index مش متطابق', '34mm') + '</div>', True))
    S.append(step(3, 'الـ size (تاني مدخل)', ['glVertexAttribPointer(0, 2, …)'],
        'كام رقم في المدخل ده. المكان رقمين (x, y)، واللون 3. ده عدد الأرقام، <b>مش</b> عدد البايتات.',
        'imp', 'خليناه 3 للمكان: ولا حاجة اتغيرت! لأن الـ Shader بيستلم <code>vec2</code>، فرمى الرقم التالت. يعني الغلطة دي ممكن تستخبى، وتظهر بعدين لما تغيّر الـ Shader. خليه يطابق نوع المتغير في الـ Shader دايماً.',
        '<div class="exrow">' + img('x_ok', 'الطبيعي', '34mm') + img('x_size3', 'size = 3 بدل 2', '34mm') + '</div>', True))
    S.append(step(4, 'الـ stride (خامس مدخل)', ['sizeof(float) * 5'],
        'كام بايت من أول ركن لأول الركن اللي بعده. لما ضفنا اللون، الركن بقى 5 أرقام بدل 2، فلازم الـ stride يتغير.',
        'req', 'سبناه رقمين (8 بايت) زي البرنامج الأول: كارت الشاشة قرا أرقام اللون على إنها أماكن، والشكل اتشوّه.',
        '<div class="exrow">' + img('x_ok', 'الطبيعي', '34mm') + img('x_wrong_stride', 'stride غلط', '34mm') + '</div>', True))
    S.append(step(5, 'الـ offset (آخر مدخل)', ['(void*)(sizeof(float) * 2)'],
        'جوه الركن الواحد، اللون بيبدأ بعد أول رقمين (8 بايت). والـ <code>(void*)</code> لأن OpenGL كاتب المدخل ده كعنوان (من أيام قديمة)، فلازم نحوّل الرقم.',
        'req', 'خليناه 0: اللون اتقرا من أول الركن، يعني من أرقام المكان، فالألوان طلعت غلط. ولما كتبناه <code>8</code> من غير <code>(void*)</code>: الـ compiler رفض.',
        '<div class="exrow">' + img('x_ok', 'الطبيعي', '34mm') + img('x_wrong_offset', 'offset = 0', '34mm') + '</div>'
        + term("int_offset.cpp: error: invalid conversion from 'int' to 'const void*'"), True))
    S.append(step(6, 'حجم الـ buffer في glBufferData', ['glBufferData(GL_ARRAY_BUFFER, 15 * sizeof(float), vertices, GL_STATIC_DRAW);'],
        'كام بايت ينسخ لكارت الشاشة. لازم يبقى الـ 15 رقم كلهم.',
        'req', 'كتبنا 10 بدل 15: آخر ركن ما اتنسخش، فالمثلث اتقطع.',
        '<div class="exrow">' + img('x_ok', 'الطبيعي', '34mm') + img('x_short_buffer', '10 أرقام بس', '34mm') + '</div>', True))
    S.append(step(7, 'out و in بنفس الاسم', ['out vec3 vertexColor;   // vertex shader', 'in vec3 vertexColor;    // fragment shader'],
        'ده الطريق اللي اللون بيعدّي فيه من الـ Vertex Shader للـ Fragment Shader. والربط بيحصل <b>بالاسم</b>، فلازم الاتنين يتكتبوا بالحرف.',
        'req', 'غيّرنا الاسم في الـ Fragment بس: الربط فشل ومفيش حاجة اترسمت. ودالة <code>CompileShader</code> ما طبعتش حاجة، لأن كل Shader لوحده سليم؛ الغلطة في الربط بينهم.',
        '<div class="exrow">' + img('x_ok', 'الطبيعي', '34mm') + img('x_name_mismatch', 'اسم مختلف', '34mm') + '</div>', True))
    S.append(step(8, 'glDrawArrays بدل glDrawElements', ['glDrawArrays(GL_TRIANGLES, 0, 3);'],
        'هنا كل ركن مكتوب مرة واحدة ومش متكرر، فمش محتاجين index buffer. <code>glDrawArrays</code> بتاخد الأركان بالترتيب.',
        'opt', 'تقدر تستخدم <code>glDrawElements</code> مع index buffer زي امبارح، بس في مثلث واحد مالوش لازمة.'))
    return ''.join(S)

def build_math():
    S = []
    S.append(step(1, 'std::sqrt في دالة الطول', ['return std::sqrt(dot(a, a, n));'],
        'الطول = جذر مجموع المربعات. ومجموع المربعات هو بالظبط الضرب النقطي في نفسه.',
        'req', 'شيلنا الجذر: الطول طلع 29 بدل 5.385. ده «مربع الطول»؛ وبالمناسبة ساعات بيستخدموه عن قصد لما يقارنوا أطوال، لأنه أسرع (من غير جذر).',
        term(pick(X + 'd_no_sqrt.out', ['length'])), True))
    S.append(step(2, 'نوع الطول float مش int', ['float length(const float* a, int n)'],
        'الطول غالباً كسر (√29 = 5.385). الـ <code>int</code> بيرمي الكسر.',
        'req', 'خلينا الدالة ترجّع <code>int</code>: الطول طلع 5 بدل 5.385، والـ compiler ما قالش ولا كلمة.',
        term(pick(X + 'd_int_length.out', ['length'])), True))
    S.append(step(3, 'عدد الأرقام n', ['dot(c, d, 3)'],
        'الدالة مش عارفة المتجه طوله كام (بتاخد عنوان أول رقم بس، زي محاضرة امبارح). إنت اللي بتقولها.',
        'req', 'بعتنا 2 لمتجه فيه 3: الدالة حسبت أول رقمين بس، فالنتيجة طلعت ‎-2 بدل 13. ومفيش أي تحذير. (<code>std::vector</code> بيحل المشكلة دي لأنه عارف حجمه)',
        term(pick(X + 'd_wrong_n.out', ['[1,2,3]'])), True))
    return ''.join(S)

def build_vec():
    S = []
    S.append(step(1, 'سطر #include <vector>', ['#include <vector>'], 'فيه تعريف <code>std::vector</code>.',
        'req', 'شيلناه: الترجمة فشلت.', term(first_err(X + 'v_no_include.build')), True))
    S.append(step(2, 'ليه vector بدل مصفوفة عادية؟', ['std::vector<Vertex> vertices;'],
        'المصفوفة العادية حجمها ثابت ولازم تعرفه من الأول. في برنامج CAD مش هتعرف المستخدم هيرسم كام نقطة. الـ vector بيكبر لوحده، وعارف حجمه (<code>size()</code>)، وبيرجّع ذاكرته لوحده.',
        'req', 'تقدر تعملها بـ <code>new</code> و <code>delete</code> زي امبارح، بس هتكتب كل حاجة بإيدك وهتنسى. الـ vector بيعمل الشغل ده.'))
    S.append(step(3, '[] مقابل at()', ['vertices[0].x', 'vertices.at(1).y'],
        'الاتنين بيجيبوا عنصر برقمه. <code>[]</code> أسرع ومش بتتأكد. <code>at()</code> بتتأكد إن الرقم جوه القايمة.',
        'imp', 'طلبنا العنصر رقم 5 من قايمة فيها 3. بـ <code>at(5)</code> البرنامج وقف ورسالته بتقول بالظبط الغلطة فين. وبـ <code>[5]</code> قرا ذاكرة مش بتاعته من غير ولا رسالة؛ الأداة بس اللي مسكتها.',
        term(pick(X + 'v_at_out.out', ['terminate', 'what()']) + '\n\n[5]:  ' + pick(X + 'v_index_out.out', ['heap-buffer-overflow on'], 1).split('ERROR: ')[-1][:60]), True))
    S.append(step(4, 'الـ & في اللوب', ['for (const Vertex& v : vertices)', 'for (Vertex& v : vertices)'],
        'من غير <code>&amp;</code> كل لفة بتعمل <b>نسخة</b> من العنصر. ده بطء على الفاضي، والأخطر إن التعديل بيروح للنسخة.',
        'req', 'شيلنا <code>&amp;</code> من لوب التعديل: اشتغل من غير أخطاء، بس x فضلت 1 و 4، لأن اللي اتضرب في 10 كان النسخ.',
        term(pick(X + 'v_loop_copy.out', ['after x'])), True))
    S.append(step(5, 'size_t مش int في اللوب', ['for (size_t i = 0; i < vertices.size(); i++)'],
        '<code>size()</code> بترجّع نوع اسمه <code>size_t</code> (رقم موجب بس). مقارنته بـ <code>int</code> (ممكن يبقى سالب) ممكن تعمل مشاكل في حالات نادرة.',
        'imp', 'كتبناها <code>int</code> زي The Cherno: اشتغلت، بس الـ compiler حذّر إن النوعين مختلفين.',
        term(first_err(X + 'v_int_loop.build')[:150]), True))
    S.append(step(6, 'الـ & في مدخل الدالة', ['void addPoint(std::vector<Point>& points, …)', 'void printPoints(const std::vector<Point>& points)'],
        'نفس فكرة <code>doubleIt</code> في محاضرة البرمجة: من غير <code>&amp;</code> الدالة بتاخد نسخة من القايمة كلها. لو هتعدّل: <code>&amp;</code>. لو هتقرا بس: <code>const&amp;</code> (من غير نسخ ومن غير تعديل).',
        'req', 'شيلنا <code>&amp;</code> من <code>addPoint</code>: النقط اتضافت لنسخة واتمسحت، والقايمة الأصلية فضلت 0 نقط.',
        term(pick(X + 'v_by_value.out', ['points:'], 1)), True))
    S.append(step(7, 'الـ vector بيتنقل وهو بيكبر', ['numbers.push_back(i);'],
        'لما المكان المحجوز (capacity) يخلص، الـ vector بيحجز مكان أكبر، وينقل كل حاجة، ويرجّع القديم. ده اللي شفناه في البرنامج 5.',
        'req', 'خلّي بالك: أي Pointer لعنصر جوه الـ vector بيبوظ بعد النقل. جربناها: أخدنا عنوان أول نقطة، عملنا <code>push_back</code>، وقرينا من العنوان القديم. الأداة قالت «استخدام بعد الإرجاع»، نفس غلطة امبارح بالظبط.',
        term(pick(X + 'v_dangling.out', ['heap-use-after-free on', 'READ of size'])), True))
    S.append(step(8, 'operator<<', ['std::ostream& operator<<(std::ostream& stream, const Vertex& vertex)'],
        '<code>cout</code> مش عارف يطبع نوع إنت اللي عامله. الدالة دي بتعلّمه.',
        'opt', 'تقدر تطبع <code>v.x</code> و <code>v.y</code> و <code>v.z</code> بإيدك كل مرة. بس لو هتطبع نقط كتير، الدالة بتوفر كتابة.'))
    return ''.join(S)
