import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day3/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def pick(p, keep, limit=6):
    o = [l for l in rd(X + p).splitlines() if any(k in l for k in keep)]
    return '\n'.join(o[:limit])
def err(n):
    for l in rd(X + n + '.build').splitlines():
        if 'error' in l or 'warning' in l:
            return l.split('/')[-1]
    return ''
def gl_out(n, skip_src=True):
    keep = [l for l in rd(X + n + '.out').splitlines() if l.strip() and not l.startswith(('#', 'layout', 'void', '{', '}', '    '))]
    return '\n'.join(keep)

def build_ref():
    S = []
    S.append(step(1, 'الـ Reference لازم يتعرّف مع متغير', ['int& ref = a;'],
        'الـ Reference «اسم تاني» لحاجة موجودة. اسم تاني لإيه لو مفيش حاجة؟',
        'req', 'كتبنا <code>int&amp; ref;</code> لوحدها: الـ compiler رفض على طول.',
        term(err('r_no_init')), True))
    S.append(step(2, 'الـ &amp; في تعريف الدالة', ['void Increment(int& value)'],
        'هي اللي بتخلّي الدالة تشتغل على المتغير الأصلي بدل نسخة. ده كل الفرق بين <code>IncrementCopy</code> و <code>IncrementReference</code>.',
        'req', 'شيلناها من برنامج The Cherno: البرنامج اشتغل عادي من غير أي تحذير، بس السطر التاني طبع 2 بدل 3. الزيادة راحت للنسخة.',
        term(out('r_no_amp')), True))
    S.append(step(3, 'الأقواس في (*value)++', ['(*value)++;'],
        'عشان النجمة تشتغل الأول (روح للعنوان)، وبعدين <code>++</code> (زوّد اللي هناك).',
        'req', 'كتبناها <code>*value++</code>: الـ compiler حذّر بس، والبرنامج اشتغل. بس طريقة العنوان طبعت 5، يعني ما زوّدتش حاجة! اللي اتزوّد هو العنوان نفسه.',
        term(err('r_star_pp') + '\n' + out('r_star_pp')), True))
    S.append(step(4, 'ليه Reference مش رقم مباشر؟', ['IncrementReference(a);'],
        'الـ Reference لازم يبقى اسم تاني لـ <b>متغير</b> ليه مكان. الرقم 5 لوحده مالوش مكان تعدّل فيه.',
        'req', 'ندهنا <code>IncrementReference(5)</code>: خطأ. ولما خلّينا المدخل <code>const int&amp;</code> قبل الرقم، بس رفض <code>value++</code> لأن <code>const</code> = ممنوع التعديل.',
        term(err('r_literal') + '\n' + err('r_const_literal')), True))
    S.append(step(5, 'الـ Reference مابيتنقلش لحاجة تانية', ['ref = b;'],
        'ده مش «خلّي ref اسم لـ b». ده «حط قيمة b في a». الـ Reference بيفضل مربوط بأول حاجة اتربط بيها طول عمره.',
        'imp', 'شغّلنا البرنامج 3: بعد <code>ref = b</code> بقى <code>a</code> = 8. ولو عايز تغيّر اللي بتشاور عليه، استخدم Pointer (<code>ptr = &amp;b</code>).',
        term(out('r3_rebind') if False else rd('/home/claude/day3/src/r3_rebind.txt').rstrip()), True))
    S.append(step(6, 'ليه Reference أأمن من Pointer؟', ['IncrementPointer(&a);'],
        'الـ Pointer ممكن يبقى <code>nullptr</code> (مش بيشاور على حاجة). الـ Reference ماينفعش، لازم يتربط بحاجة موجودة.',
        'imp', 'بعتنا <code>IncrementPointer(nullptr)</code>: الترجمة عدّت عادي، والبرنامج وقع وهو شغال (Segmentation fault، كود 139). مع Reference الغلطة دي مش هتترجم أصلاً.',
        term('copy:      a = 5\n[crashed: Segmentation fault, exit code 139]'), True))
    S.append(step(7, 'سطر #define LOG', ['#define LOG(x) std::cout << x << std::endl'],
        'اختصار The Cherno عشان مايكتبش <code>std::cout</code> كل مرة.',
        'opt', 'شيلناه: خطأ في كل سطر فيه <code>LOG</code>. لو شيلته، استبدل كل <code>LOG(a)</code> بـ <code>std::cout &lt;&lt; a &lt;&lt; std::endl</code>.',
        term(err('r_no_define')), True))
    return ''.join(S)

def build_ham():
    S = []
    S.append(step(1, 'التأكد إن الطولين زي بعض (الحل الأول)', ['if (lhs_length != rhs_length)', '    return -1;'],
        'التمرين بيقول: لو الطولين مختلفين، رجّع ‎-1. وكمان بيحمي اللوب: هو بيلف لحد طول <code>lhs</code>، فلو <code>rhs</code> أقصر هيقرا برا.',
        'req', 'شيلناه وجربنا <code>"AATGC"</code> مع <code>"AAA"</code>: البرنامج قرا بعد آخر <code>"AAA"</code>، وأداة AddressSanitizer مسكته.',
        term(pick('h1_no_len_check.out', ['ERROR: AddressSanitizer', 'READ of size', "is ascii string 'AAA'"], 3)), True))
    S.append(step(2, 'int distance = 0 (مش int distance)', ['int distance = 0;'],
        'الفيديو بيأكد عليها: في C المتغير مابيبدأش بصفر لوحده. بيبدأ بأي حاجة كانت في المكان ده قبله (garbage).',
        'req', 'شيلنا <code>= 0</code>: من غير أي تحذير، أول إجابة طلعت 7 صح، بس التانية طلعت 7 بدل 0! المتغير بدأ بالرقم اللي فضل في الذاكرة من النداء اللي قبله.',
        term(out('h1_no_init')), True))
    S.append(step(3, 'كلمة const', ['int compute(const char* lhs, const char* rhs)'],
        'وعد إن الدالة مش هتغيّر النصوص. الـ compiler بيحرس الوعد ده.',
        'imp', 'جوه الدالة كتبنا <code>lhs[0] = \'X\';</code>: الـ compiler رفض. من غير <code>const</code> كان هيعدّي، والبرنامج يقع لأن النصوص المكتوبة في الكود نفسه للقراية بس.',
        term(err('h1_write_const')), True))
    S.append(step(4, 'التحقق من NULL (الحل التاني)', ['if (!lhs || !rhs)', '    return -1;'],
        'نصيحة الفيديو: «ماتثقش في المدخلات». لو حد بعتلك Pointer فاضي، <code>*lhs</code> هتقرا من العنوان صفر.',
        'imp', 'شيلناه وبعتنا <code>NULL</code>: البرنامج وقع (Segmentation fault). ولاحظ إن حتى الأرقام اللي اتحسبت قبل كده ماظهرتش، لأن البرنامج وقع قبل ما يطبعها على الشاشة.',
        term('[crashed: Segmentation fault, exit code 139, no output]'), True))
    S.append(step(5, 'الشرط *lhs && *rhs', ['for (; *lhs && *rhs; lhs++, rhs++)'],
        'عشان نقف لما <b>أي</b> نص فيهم يخلص، مش الشمال بس.',
        'req', 'خلّينا الشرط <code>*lhs</code> بس: مع <code>"AATGC"</code> و <code>"AAA"</code> الـ Pointer <code>rhs</code> عدّى نهاية <code>"AAA"</code>. نفس الغلطة اللي مسكناها في الحل الأول.',
        term(pick('h2_only_lhs.out', ['ERROR: AddressSanitizer', 'READ of size', "is ascii string 'AAA'"], 3)), True))
    S.append(step(6, 'الـ ? : في الآخر', ['return (*lhs || *rhs) ? -1 : distance;'],
        'بعد اللوب: لو واحد فيهم لسه ماوصلش لآخره، يبقى الطولين مختلفين. الحل التاني مابيحسبش الطول الأول، فده هو المكان الوحيد اللي بيعرف فيه.',
        'req', 'خلّيناها <code>return distance;</code> بس: <code>"AATG"</code> مع <code>"AAA"</code> طلّعوا 1 بدل ‎-1. إجابة غلط من غير أي رسالة.',
        term(out('h2_no_ternary')), True))
    return ''.join(S)

def build_shader():
    S = []
    S.append(step(1, 'المسار والـ Working Directory', ['ParseShader("res/shaders/Basic.shader");'],
        'المسار ده «نسبي»: بيتحسب من المجلد اللي البرنامج شغال منه. في Visual Studio ده مجلد المشروع (<code>$(ProjectDir)</code>)، ولو شغّلت الـ .exe لوحده يبقى مجلد الـ .exe.',
        'req', 'غلّطنا حرف في المسار (<code>shader</code> بدل <code>shaders</code>): ولا رسالة إن الملف مش موجود! النصين طلعوا فاضيين، فالـ Shaderين فشلوا، والشباك أسود.',
        term(gl_out('s_wrong_path')) + img('s_wrong_path', 'الشباك: أسود'), True))
    S.append(step(2, "الـ '\\n' بعد كل سطر", ["ss[(int)type] << line << '\\n';"],
        '<code>getline</code> بتقرا السطر من غير علامة النزول. لازم نرجّعها، وإلا كل الـ Shader هيبقى سطر واحد.',
        'req', 'شيلناها: <code>#version</code> اتلزق في اللي بعده، والـ Shaderين فشلوا.',
        term(gl_out('s_no_newline')), True))
    S.append(step(3, 'الـ (int) قبل type', ["ss[(int)type] << line << '\\n';"],
        '<code>enum class</code> محمية: مابتتحولش لرقم لوحدها. لازم تقول صراحةً «اعتبرها int».',
        'req', 'شيلنا <code>(int)</code>: ماترجمش.',
        term(err('s_no_cast')), True))
    S.append(step(4, 'سطر #shader vertex في الملف', ['#shader vertex'],
        'هو اللي بيغيّر <code>type</code> من NONE لـ VERTEX. من غيره، أول سطور هتتكتب في <code>ss[-1]</code>، وده مكان مش موجود.',
        'req', 'شيلناه من الملف: البرنامج وقع على طول (Segmentation fault). الكود ده بيثق إن الملف مكتوب صح؛ في مشروع حقيقي تتأكد إن <code>type</code> مش NONE قبل ما تكتب.',
        term('[crashed: Segmentation fault, exit code 139]'), True))
    S.append(step(5, 'طباعة رسالة الخطأ', ['glGetShaderInfoLog(id, 512, nullptr, message);', 'std::cout << message << std::endl;'],
        'كارت الشاشة بيقولك الغلطة فين بالظبط. من غير الطباعة دي، كل غلطة في الـ Shader = شاشة سودا وخلاص.',
        'imp', 'كتبنا <code>gl_position</code> بحرف p صغير في الملف: الرسالة قالت السطر 7، والكلمة الغلط. الشباك أسود، بس عرفنا السبب في ثانية.',
        term(gl_out('s_typo')) + img('s_typo', 'الشباك: أسود'), True))
    S.append(step(6, 'glDeleteProgram مش glDeleteShader', ['glDeleteProgram(shader);'],
        'الحاجة اللي اسمها <code>shader</code> في <code>main</code> هي Program (فيها Shaderين)، فبنمسحها بدالة الـ Program. ده التصحيح اللي The Cherno قاله في الحلقة.',
        'imp', 'كتبنا <code>glDeleteShader(shader)</code>: البرنامج ماوقعش، بس OpenGL رجّع خطأ رقم 1282 (GL_INVALID_OPERATION)، يعني ما مسحش حاجة.',
        term(rd(X + 's_delete_shader.out').strip().splitlines()[-1]), True))
    S.append(step(7, 'ليه ملف واحد للـ Shaders؟', ['#shader vertex', '#shader fragment'],
        'عشان تكتب الـ Shader من غير علامات تنصيص ومن غير <code>\\n</code> في كل سطر، وتغيّر اللون من غير ما تعيد ترجمة الـ C++. <code>#shader</code> علامة إحنا اخترعناها، والـ GPU عمره ما بيشوفها.',
        'opt', 'الطريقة القديمة (النص جوه الكود) شغالة عادي، وده اللي عملناه امبارح. دي بس طريقة أريح لما الـ Shaders تكبر.'))
    return ''.join(S)

def build_cross():
    S = []
    S.append(step(1, 'الترتيب بيفرق', ['cross2D(-3, 1, 2, 1)', 'cross2D(2, 1, -3, 1)'],
        'v × w = −(w × v). الإشارة بتقولك v على يمين w ولا شمالها.',
        'req', 'البرنامج نفسه بيوريك: ‎-5 بعدين 5.',
        term('\n'.join(rd('/home/claude/day3/src/x1_cross.txt').splitlines()[:2])), True))
    S.append(step(2, 'السالب في الرقم التاني', ['v.z * w.x - v.x * w.z,'],
        'في الفيديو الرقم التاني عليه سالب: −(v₁w₃ − v₃w₁). إحنا كتبناه مقلوب (v₃w₁ − v₁w₃) وده نفس الحاجة.',
        'req', 'بدّلنا الطرفين (نسينا السالب) وجربنا على (1,2,3) × (4,5,6): الناتج طلع (‎-3, ‎-6, ‎-3) بدل (‎-3, 6, ‎-3)، والتأكيد بالضرب النقطي كشفه: مابقاش صفر.',
        term('wrong:  ' + pick('x_wrong_sign.out', ['3D'], 1) + '\n        ' + pick('x_wrong_sign.out', ['c . v'], 1)
             + '\nright:  ' + pick('x_right_123.out', ['3D'], 1) + '\n        ' + pick('x_right_123.out', ['c . v'], 1)), True))
    S.append(step(3, 'لو المتجهين في نفس الاتجاه', ['Vec3 w = { 0, 0, 5 };'],
        'متوازي الأضلاع بيفطس (مساحته صفر)، فالناتج متجه صفر. ومفيش اتجاه «عمودي» واحد.',
        'imp', 'خلّينا w في نفس اتجاه v: الناتج (0, 0, 0). وده بالظبط سبب شرط الـ 5° في الكاميرا يوم الأحد: لو بصّيت لفوق خالص، <code>cross(Orientation, Up)</code> = صفر، والكاميرا تتلخبط.',
        term(pick('x_parallel.out', ['3D'], 1)), True))
    S.append(step(4, 'ليه نكتبها بإيدنا لو GLM فيها cross؟', ['Vec3 cross(Vec3 v, Vec3 w)'],
        'عشان تفهم الأرقام. في الشغل الحقيقي استخدم <code>glm::cross</code>.',
        'opt', 'قارنّا بـ GLM: نفس النتايج بالظبط. وفي الكاميرا <code>cross(Orientation, Up)</code> = (1, 0, 0) يعني «يمين»، وده اللي زرار D بيمشي فيه.',
        term(rd(X + 'x_glm.out').strip()), True))
    return ''.join(S)

def build_cad():
    S = []
    S.append(step(1, 'كود الفيديو زي ما هو', ['glBufferData(GL_ARRAY_BUFFER, 6 * sizeof(float), positions, GL_STATIC_DRAW);', 'glDrawArrays(GL_TRIANGLES, 0, 3);'],
        'الحلقة بتعمل الـ buffer وأمر الرسم بس، و The Cherno قال «مش هيظهر حاجة لسه».',
        'req', 'شغّلنا كود الحلقة بالظبط: شباك أسود فعلاً. ولما ضفنا سطرين بتوع الحلقة الجاية (<code>glEnableVertexAttribArray</code> و <code>glVertexAttribPointer</code>) من غير Shader، طلع مثلث أبيض، زي ما حصل عند The Cherno. ده بيشتغل في الـ Compatibility profile بس؛ في الـ Core (اللي بنستخدمه) لازم VAO و Shader.',
        img('c_cherno_raw', 'كود الحلقة: أسود') + img('c_cherno_attrib', '+ سطرين الـ Attribute: أبيض'), True))
    S.append(step(2, 'قلب y في تحويل الماوس', ['float y = (float)(1.0 - 2.0 * py / height);'],
        'البكسل بيتعد من فوق، و OpenGL بيعد من تحت.',
        'req', 'شيلنا القلب ودوسنا نفس النقطتين: الخط اترسم مقلوب (المكان اللي دوسنا فوقه اترسم تحت).',
        img('l_no_flip_2', 'من غير قلب: الخط مقلوب') + img('l2_2', 'الصح'), True))
    S.append(step(3, 'sizeof(float) في glBufferData', ['glBufferData(GL_ARRAY_BUFFER, points.size() * sizeof(float), points.data(), GL_DYNAMIC_DRAW);'],
        'الحجم بالبايت. نقطتين = 4 أرقام × 4 بايت = 16 بايت.',
        'req', 'كتبنا <code>points.size()</code> بس (4 بايت): اتبعت رقم واحد بس من الأربعة، فاترسمت نقطة واحدة في مكان غلط ومفيش خط. ومن غير ولا رسالة خطأ.',
        img('l_no_sizeof_2', 'من غير sizeof'), True))
    S.append(step(4, 'GL_DYNAMIC_DRAW', ['GL_DYNAMIC_DRAW'],
        'تلميح لكارت الشاشة إن البيانات هتتغير كتير، فيحطها في مكان أسرع للتعديل.',
        'opt', 'غيّرناها لـ <code>GL_STATIC_DRAW</code>: اشتغل بالظبط نفس الشكل. ده اللي الحلقة قالته: مجرد تلميح، لو غلطت ممكن يبقى أبطأ بس.',
        img('l_static_2', 'GL_STATIC_DRAW: نفس النتيجة'), True))
    S.append(step(5, 'glPointSize', ['glPointSize(12.0f);'],
        'من غيرها النقطة بكسل واحد.',
        'opt', 'شيلناها: النقط اختفت تقريباً.',
        img('l_no_pointsize', 'من غير glPointSize'), True))
    S.append(step(6, 'سُمك الخط', ['glLineWidth(5.0f);'],
        'الخط بكسل واحد افتراضياً. <code>glLineWidth</code> بتتخنه.',
        'opt', 'ضفناها: اشتغلت على الجهاز اللي جربنا عليه. بس خلّي بالك: في الـ Core profile كروت كتير بتدعم 1 بس. عشان كده برامج الـ CAD الحقيقية بترسم الخط التخين كمستطيل (مثلثين).',
        img('l_width', 'glLineWidth(5)'), True))
    S.append(step(7, 'GL_LINES بتاخد كل نقطتين', ['glDrawArrays(GL_LINES, 0, count);'],
        'نقطة 0 مع 1 = خط، و 2 مع 3 = خط، وهكذا. ده اللي بيخلّي كل دوستين = خط في البرنامج 2.',
        'req', 'في التشغيل دوسنا 5 مرات: اترسم خطين، والنقطة الخامسة لوحدها (لسه مستنية شريكها).',
        img('l2_5', '5 دوسات = خطين + نقطة'), True))
    return ''.join(S)
