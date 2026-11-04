import sys, re
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day7/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def code(n): return rd(X + n + '.out').rsplit('exit=', 1)[1].strip()
def build_err(n):
    return '\n'.join(L.split('/')[-1] for L in rd(X + n + '.build').splitlines() if 'error' in L)
def pyerr(n): return rd(X + n + '.out').split('\nexit=')[0].strip().splitlines()[-1]
def two(a, ca, b, cb): return f'<div class="exrow">{img(a, ca)}{img(b, cb)}</div>'
def gitout(n): return rd(X + n + '.out').rstrip('\n')


def build_pointers():
    S = []
    S.append(step(1, 'int* مش void* عشان نكتب', ['int* intPtr = &var;', '*intPtr = 10;'],
        '<code>void*</code> بيشيل العنوان بس، ومش عارف اللي هناك حجمه كام بايت. عشان نكتب لازم نوع.',
        'req', 'كتبنا <code>*ptr = 10;</code> على الـ <code>void*</code>: الـ compiler رفض يترجم.',
        term(build_err('x_void_deref')), True))
    S.append(step(2, '(void*) قبل buffer في الطباعة', ['std::cout << "buffer = " << (void*)buffer'],
        '<code>std::cout</code> بيتعامل مع <code>char*</code> على إنه نص، فبيطبع الحروف مش العنوان.',
        'imp', 'شيلنا <code>(void*)</code>: اتطبع <code>Hi</code> مكان العنوان. البرنامج ماوقعش، بس الطباعة كدبت علينا.',
        term(out('x_no_cast').splitlines()[3]), True))
    S.append(step(3, 'delete[] مرة واحدة، وبعدها nullptr', ['delete[] buffer;', 'buffer = nullptr;'],
        'العنوان بعد المسح مبقاش بتاعنا. لو مسحناه تاني البرنامج بيبوّظ ذاكرة النظام.',
        'req', 'مسحناه مرتين: البرنامج وقع وطبع رسالة النظام (exit = ' + code('x_double_delete') + ').',
        term(out('x_double_delete').splitlines()[-1]), True))
    return ''.join(S)


def build_quiz():
    S = []
    S.append(step(1, 'Swap بتاخد عناوين', ['void Swap(int* a, int* b)', 'Swap(&a, &b);'],
        'الدالة بتاخد نسخة من أي حاجة بتتبعتلها. لو بعتنا العنوان، النسخة لسه بتشاور على المتغير الأصلي.',
        'req', 'خلّيناها <code>Swap(int a, int b)</code>: بدّلت النسخ جوه الدالة بس، والأصل فضل زي ما هو: FAIL.',
        term(out('q_by_value').splitlines()[0]), True))
    S.append(step(2, 'char** في MakeText', ['void MakeText(char** out, int size)', 'MakeText(&text, 4);'],
        'عايزين الدالة تغيّر <code>text</code> نفسه (العنوان اللي جواه)، فلازم ناخد عنوانه: Pointer لـ Pointer.',
        'req', 'خلّيناها <code>char* out</code>: الدالة حجزت وكتبت xxx في نسختها، و <code>text</code> فضل nullptr: FAIL. والـ 4 بايت اتحجزوا ومحدش هيمسحهم.',
        term(out('q_single_ptr').splitlines()[2]), True))
    S.append(step(3, 'فحص nullptr', ['if (p != nullptr)'],
        'العنوان 0 مش بتاعنا. الكتابة فيه بتوقّع البرنامج.',
        'req', 'شيلنا الفحص: <code>SetToZero(nullptr)</code> وقّع البرنامج (exit = ' + code('q_no_null') + ' = Segmentation fault)، فالاختبارات اللي بعدها ماتنفذتش خالص.',
        term(out('q_no_null')), True))
    S.append(step(4, 'النجمة في Sum', ['total += *(values + i);'],
        '<code>values + i</code> عنوان، و <code>*</code> قبله = الرقم اللي هناك.',
        'req', 'نسينا النجمة: الـ compiler رفض لأنه مينفعش نجمع عنوان على int.', term(build_err('q_no_deref')), True))
    return ''.join(S)


def build_vao():
    S = []
    S.append(step(1, 'لازم VAO في الـ Core Profile', ['glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, 0);   // before the VAO'],
        'The Cherno: في الـ Core Profile مفيش VAO افتراضي (رقم 0)، فأي ربط من غير VAO بيترفض.',
        'req', 'السطر اللي قبل الـ VAO في برنامجنا هو التجربة نفسها: رجع 1282. عند The Cherno (كارت NVIDIA) الرفض ظهر عند <code>glEnableVertexAttribArray</code>، وعندنا (Mesa) الرفض ظهر عند <code>glVertexAttribPointer</code>. الاتنين نفس القاعدة.',
        term(rd('/home/claude/day7/src/r1_vertex_array.txt').splitlines()[0]), True))
    S.append(step(2, 'glBindVertexArray(vao) في اللوب', ['glBindVertexArray(vao);'],
        'إحنا فكّينا الـ VAO قبل اللوب. من غير ما نربطه تاني، الرسم مالوش أركان.',
        'req', 'شيلناه من اللوب: الشاشة سودا، وكل فريم <code>glGetError</code> = 1282: الكارت رفض الرسم.',
        term('\n'.join(out('v_no_rebind').splitlines()[1:3])) + img('v_no_rebind_1', 'من غير ربط الـ VAO: أسود'), True))
    S.append(step(3, 'glBindBuffer للترتيب في اللوب', ['glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);   // in the loop'],
        'The Cherno كتبه في اللوب. بس الـ VAO بيفتكر صندوق الترتيب من وقت الإعداد.',
        'opt', 'شيلناه: نفس الصورة بالظبط، والخطأ 0. يعني الـ VAO فعلاً فاكره.',
        img('v_no_ibo_1', 'من غيره: نفس الرسمة'), True))
    S.append(step(4, 'ترتيب الفك: الـ VAO الأول', ['glBindVertexArray(0);', 'glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);'],
        'لو فكّينا صندوق الترتيب والـ VAO لسه شغال، الـ VAO هيسجّل «مفيش ترتيب».',
        'req', 'قدّمنا <code>glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)</code> قبل فك الـ VAO، وشيلنا ربط الترتيب من اللوب: البرنامج وقع في أول رسمة (exit = ' + code('v_ibo_first') + ')، لأن الكارت دوّر على الترتيب في العنوان 0.',
        term(out('v_ibo_first')), True))
    return ''.join(S)


def build_methods():
    S = []
    S.append(step(1, 'الطريقتين نفس الصورة', ['glBindVertexArray(squareVao);', 'glBindVertexArray(globalVao);'],
        'الفرق في الكود بس: الطريقة 2 بتربط مرة لكل رسمة، والطريقة 1 بتعيد الصندوق والـ Layout.',
        'imp', 'قارنّا النص الشمال بالنص اليمين في الصورة الحقيقية بالكمبيوتر: نفس البكسلات بالظبط.', '', True))
    S.append(step(2, 'glVertexAttribPointer لكل رسمة في الطريقة 1', ['glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, 0);   // right half'],
        'في الطريقة 1 الـ VAO واحد، فهو لسه فاكر Layout المربع (وصندوق المربع). لازم نقوله الجديد.',
        'req', 'شيلناه من الرسمة اليمين: المثلث اترسم من أركان <b>المربع</b> (أول 3 أركان منه)، فطلع نص مربع أزرق.',
        two('r2_two_methods_1', 'الصح', 'w_no_pointer_1', 'من غيره: المثلث اترسم من المربع'), True))
    S.append(step(3, 'glBindBuffer قبل glVertexAttribPointer', ['glBindBuffer(GL_ARRAY_BUFFER, triangleBuffer);', 'glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, 0);'],
        '<code>glVertexAttribPointer</code> بيربط <b>الصندوق المربوط وقتها</b>. الترتيب هو الربط.',
        'req', 'بدّلنا السطرين: الـ Layout الجديد (3 أرقام) اتربط بصندوق المربع (رقمين)، فالأرقام اتقرت متزحلقة وطلع شكل غريب.',
        two('r2_two_methods_1', 'الصح', 'w_order_1', 'بالعكس: أرقام المربع اتقرت 3 3'), True))
    return ''.join(S)


def build_cross():
    S = []
    S.append(step(1, 'الصف التاني معكوس', ['a[2] * b[0] - a[0] * b[2],'],
        'Khan: الصف الأوسط بيتكتب بالعكس (a₃b₁ − a₁b₃). ده أشهر غلط.',
        'req', 'كتبناه زي الصفين التانيين (a₁b₃ − a₃b₁): العنصر التاني طلع ‎-1 بدل 1، والناتج بطّل يبقى عمودي، والـ check مسك 4 أسئلة.',
        term('\n'.join(out('c_not_reversed').splitlines()[:3])), True))
    S.append(step(2, '3 أبعاد بس', ['def cross(a, b):'],
        'الضرب الاتجاهي متعرّف في R³ بس.',
        'req', 'بعتنا متجهين 2D: Python وقعت لأن مفيش عنصر رقم 2.', term(pyerr('c_2d')), True))
    S.append(step(3, 'الترتيب بيفرق', ['check("b x a", cross(b, a), [30, -1, -37])'],
        'عكس الضرب النقطي: a × b = ‎−(b × a).',
        'imp', 'البرنامج نفسه أثبتها: نفس الأرقام بإشارة عكس. ولما بتحسب Normal لمثلث، الترتيب الغلط بيقلب الوش للناحية التانية.', '', True))
    return ''.join(S)


def build_git():
    S = []
    S.append(step(1, 'git config مرة واحدة', ['git config --global user.name "Student"', 'git config --global user.email "student@example.com"'],
        'كل Commit عليه اسم وإيميل. Git لازم يعرف إنت مين.',
        'req', 'جربنا Commit على جهاز مافيهوش الاسم: Git رفض وقال «Please tell me who you are». (اسم الجهاز في السطر الأخير هيختلف عندك)',
        term(gitout('g_no_name').split('\n\n', 2)[2].split('$ git commit -m "add refactored polyline tool"\n', 1)[1]), True))
    S.append(step(2, 'git add قبل git commit', ['git add .'],
        'الـ Commit بياخد اللي في الـ Staging بس.',
        'req', 'عملنا commit من غير add: مفيش Commit اتعمل، و Git قالنا نعمل add.',
        term(gitout('g_no_add').split('$ git commit -m "add refactored polyline tool"\n', 1)[1]), True))
    S.append(step(3, 'رسالة بتوصف التغيير', ['git commit -m "make points bigger: 10 -> 12 px"'],
        'بعد أسبوعين مش هتفتكر عملت إيه. الرسالة هي اللي هتقولك.',
        'imp', 'نفس التغيير برسايل وحشة: الـ log بقى مالوش معنى.',
        term(gitout('g_bad_msg').split('$ git log --oneline\n', 1)[1]) + term('ed785af make points bigger: 10 -> 12 px\n84180e1 add refactored polyline tool'), True))
    S.append(step(4, 'الـ ID جاي من المحتوى والوقت', ['who = "Student <student@example.com> 1793458800 +0200"'],
        'الـ ID مش رقم عشوائي: بصمة لكل حاجة في الـ Commit.',
        'imp', 'زوّدنا الوقت ثانية واحدة بس: الـ ID اتغير كله. عشان كده الـ ID بتاعك هيطلع غير اللي هنا (اسمك ووقتك غير).',
        term('\n'.join(L for L in out('g_one_second').splitlines() if L.startswith(('commit', 'short')))), True))
    return ''.join(S)
