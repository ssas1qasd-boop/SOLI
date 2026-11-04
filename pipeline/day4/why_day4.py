import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day4/exp/'
SRC = '/home/claude/day4/src/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def err(n, k=('error',)):
    for l in rd(X + n + '.build').splitlines():
        if any(w in l for w in k):
            return l.split('/')[-1].replace('tmp/', '')
    return ''
def lerr(n):
    import re
    for l in rd(X + n + '.build').splitlines():
        m = re.search(r"(multiple definition of `[^']+'|undefined reference to `[^']+')", l)
        if m:
            return 'ld: ' + m.group(1)
    return ''

def build_static():
    S = []
    S.append(step(1, 'static على المتغير', ['static int s_Variable = 5;'],
        'عشان المتغير يخص الملف ده بس، فملف تاني يقدر يستخدم نفس الاسم من غير خناقة.',
        'req', 'شيلنا <code>static</code>: كل ملف اترجم لوحده تمام، بس الـ Linker (اللي بيلزق الملفات) رفض، لأن فيه اتنين بنفس الاسم.',
        term(lerr('st_conflict') + '\ncollect2: error: ld returned 1 exit status'), True))
    S.append(step(2, 'static على الدالة', ['static void Function()'],
        'نفس الفكرة بالظبط للدوال.',
        'req', 'شيلناها: نفس خطأ الـ Linker، المرة دي على <code>Function()</code>.',
        term(lerr('st_func_conflict') + '\ncollect2: error: ld returned 1 exit status'), True))
    S.append(step(3, 'extern مع متغير static', ['extern int s_Variable;'],
        '<code>extern</code> بتدوّر على المتغير في ملف تاني. لو هو <code>static</code> هناك، يبقى مخفي عنها.',
        'req', 'خلّينا المتغير في <code>static.cpp</code> يبقى <code>static</code>: الـ Linker قال «مش لاقيه» (undefined reference). ده اللي The Cherno سماه unresolved external symbol في Visual Studio.',
        term(lerr('st_extern_static') + '\ncollect2: error: ld returned 1 exit status'), True))
    S.append(step(4, 'static في ملف header', ['static int s_Counter = 0;   // counter.h'],
        'تحذير الفيديو: كل ملف <code>.cpp</code> بيعمل include للـ header بياخد <b>نسخة لوحده</b>.',
        'imp', 'عملنا <code>counter.h</code> فيه السطر ده، وضمّناه في ملفين، وكل ملف زوّد العدّاد: الاتنين طبعوا 1. يعني اتنين عدّادين منفصلين، مش واحد. مفيش أي خطأ، بس غالباً مش ده اللي إنت عايزه.',
        term(out('st_header')), True))
    return ''.join(S)

def build_const():
    S = []
    S.append(step(1, 'const على متغير', ['const int MAX_AGE = 90;'],
        'وعد إن القيمة مش هتتغير، والـ compiler بيحرسه.',
        'imp', 'كتبنا <code>MAX_AGE = 100;</code>: رفض.', term(err('c_max_age')), True))
    S.append(step(2, 'const قبل النجمة', ['const int* b = a;'],
        'عشان تقرا من العنوان من غير ما حد يغيّر اللي هناك بالغلط.',
        'imp', 'كتبنا <code>*b = 2;</code>: رفض (المحتوى ثابت). وتحريك <code>b</code> نفسه اشتغل عادي في البرنامج.', term(err('c_b_content')), True))
    S.append(step(3, 'const بعد النجمة', ['int* const c = new int(5);'],
        'عشان الـ Pointer يفضل على نفس المكان طول عمره.',
        'imp', 'كتبنا <code>c = nullptr;</code>: رفض (الـ Pointer ثابت). وتغيير المحتوى اشتغل عادي في البرنامج.', term(err('c_c_pointer')), True))
    S.append(step(4, 'const في الحتتين', ['const int* const d = &MAX_AGE;'],
        'قراية بس.', 'imp', 'جربنا الاتنين: خطأين.', term('\n'.join(l.split('/')[-1] for l in rd(X + 'c_d_both.build').splitlines() if 'error' in l)), True))
    S.append(step(5, 'const بعد اسم الدالة', ['int GetX() const'],
        'عشان الدالة تنفع تتنادي على حاجة <code>const</code>، زي <code>const Entity&amp; e</code> في <code>PrintEntity</code>.',
        'req', 'شيلنا <code>const</code> من <code>GetX</code>: <code>PrintEntity</code> مابقتش تترجم، لأن الـ compiler مش ضامن إن <code>GetX</code> مش هتغيّر <code>e</code>.',
        term(err('c_no_const_method')), True))
    S.append(step(6, 'mutable', ['mutable int m_DebugCount = 0;'],
        'استثناء: متغير مسموح يتغيّر حتى جوه دالة <code>const</code>. The Cherno قال إنه بيستخدم للـ debugging زي العدّاد ده.',
        'req', 'شيلنا <code>mutable</code>: رفض الزيادة جوه <code>GetX</code>.', term(err('c_no_mutable')), True))
    return ''.join(S)

def build_cross():
    S = []
    S.append(step(1, 'الصف الأوسط معكوس', ['a.z * b.x - a.x * b.z,'],
        'دي طريقة الحفظ في الفيديو: الأول والتالت بنفس الترتيب، والأوسط معكوس.',
        'req', 'كتبناه بنفس ترتيب الباقيين (مش معكوس): مثال الفيديو طلع [‎-30, ‎-1, 37] بدل [‎-30, 1, 37]، والضرب النقطي مابقاش صفر.',
        term(rd(X + 'x_middle_not_reversed.out').splitlines()[0]), True))
    S.append(step(2, 'التأكيد بالضرب النقطي', ['<< "    c.a = " << dot(c, a) << "  c.b = " << dot(c, b) << std::endl;'],
        'خاصية Khan Academy: الناتج عمودي على الاتنين، يعني الضرب النقطي معاهم = 0. أسهل طريقة تكشف بيها غلطة حساب.',
        'opt', 'كل التمارين في البرنامج طلّعت 0 و 0. ولو طلع أي رقم غير صفر، يبقى فيه غلطة في الحساب.'))
    return ''.join(S)

def build_ebo():
    S = []
    S.append(step(1, 'GL_UNSIGNED_INT', ['glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);'],
        'لازم يطابق نوع مصفوفة <code>indices</code>، ولازم يبقى unsigned.',
        'req', 'كتبناه <code>GL_INT</code> زي تحذير The Cherno: شاشة سودا، ومفيش أي رسالة. بس لما سألنا <code>glGetError</code> رجّع 1280 (GL_INVALID_ENUM).',
        term(out('e_gl_int')) + img('e_gl_int', 'GL_INT: أسود'), True))
    S.append(step(2, 'العدد = عدد الـ indices', ['glDrawElements(GL_TRIANGLES, 6, …)'],
        '6 = عدد أرقام الترتيب (مثلثين × 3)، مش عدد الأركان (4).',
        'req', 'كتبنا 3: اترسم أول مثلث بس.', img('e_count3', 'العدد 3: نص المستطيل'), True))
    S.append(step(3, 'الترتيب الصح', ['2, 3, 0'],
        'كل 3 أرقام = مثلث. لو غلطت في رقم، المثلث هيوصل أركان غلط.',
        'req', 'غيّرنا التاني لـ <code>2, 3, 1</code>: طلع شكل غريب بدل المستطيل.', img('e_wrong_indices', '2, 3, 1 بدل 2, 3, 0'), True))
    S.append(step(4, 'ماتفكّش الـ IBO والـ VAO شغال', ['glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);'],
        'الـ VAO بيفتكر الـ Index Buffer المربوط وهو شغال. لو فكّيته (<code>glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)</code>) والـ VAO لسه مربوط، الـ VAO بينساه.',
        'req', 'ضفنا سطر الفك بعد التجهيز: البرنامج <b>وقع</b> أول ما رسم (Segmentation fault). من غير IBO، <code>nullptr</code> بقت معناها «اقرا الأرقام من العنوان صفر».',
        term('[crashed: Segmentation fault, exit code 139]'), True))
    S.append(step(5, 'فك الـ Vertex Buffer عادي', ['glBindBuffer(GL_ARRAY_BUFFER, 0);'],
        'عكس اللي فات: الـ Vertex Buffer اتسجل في الـ VAO لحظة <code>glVertexAttribPointer</code>، فبعدها تفكه براحتك.',
        'opt', 'فكّيناه قبل عمل الـ IBO: المستطيل اترسم عادي.', img('e_unbind_vbo', 'فك الـ VBO: سليم'), True))
    S.append(step(6, 'ليه Index Buffer أصلاً؟', ['float positions[8]', 'unsigned int indices[6]'],
        'عشان مانكررش الأركان. The Cherno قال: استخدمه في 90% من الحالات.',
        'imp', 'للأمانة، حسبناها: في مستطيلنا (ركن = رقمين = 8 بايت) من غير IBO = 6 × 8 = 48 بايت، ومع IBO = 4 × 8 + 6 × 4 = 56 بايت، يعني أكبر شوية! بس لما الركن يبقى فيه مكان ولون وإحداثيات صورة (32 بايت مثلاً): 192 بايت من غير IBO مقابل 152 مع IBO. وكل ما الشكل يكبر، التوفير يكبر.'))
    return ''.join(S)

def build_vao():
    S = []
    S.append(step(1, 'الـ VAO في الـ Core Profile', ['glGenVertexArrays(1, &vao);', 'glBindVertexArray(vao);'],
        'الـ Core Profile (اللي بنستخدمه) مافيهوش VAO افتراضي. لازم تعمله بنفسك.',
        'req', 'شيلنا سطرين الـ VAO من برنامج المستطيل: شاشة سودا، و <code>glGetError</code> = 1282 (GL_INVALID_OPERATION)، نفس الرقم اللي The Cherno قاله.',
        term(out('v_no_vao_core')) + img('v_no_vao_core', 'Core من غير VAO: أسود'), True))
    S.append(step(2, 'ليه كان شغال قبل كده من غيره؟', ['glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);'],
        'في الـ Compatibility Profile، OpenGL بيعمل VAO رقم 0 لوحده.',
        'opt', 'شيلنا سطور الـ Core و الـ VAO مع بعض: المستطيل اترسم، و <code>glGetError</code> = 0. ده اللي كان بيحصل في أول حلقات The Cherno.',
        term(out('v_no_vao_compat')) + img('v_no_vao_compat', 'Compatibility من غير VAO: شغال'), True))
    S.append(step(3, 'Bind قبل كل رسمة', ['glBindVertexArray(sunVao);'],
        'OpenGL = State Machine: بيرسم بآخر حاجة اتعملها bind.',
        'req', 'شيلنا bind الشمس من اللوب: الشمس اختفت، وأول خطين من البيت (الأرض والحيطة اليمين) اترسموا أصفر! أمر رسم الشمس اشتغل على VAO البيت.',
        img('v_no_sun_bind', 'من غير bind الشمس'), True))
    S.append(step(4, 'GL_LINE_STRIP مش GL_LINES', ['glDrawArrays(GL_LINE_STRIP, line.first, line.count);'],
        'عشان كل نقطة تتوصل باللي بعدها (خط متصل).',
        'req', 'غيّرناها لـ <code>GL_LINES</code>: الخطوط بقت حتت منفصلة (كل نقطتين لوحدهم)، والنقطة الأخيرة في الخط التاني اتسابت لوحدها.',
        img('p_lines_not_strip_8', 'GL_LINES: حتت منفصلة') + img('v2_8', 'GL_LINE_STRIP: متصل'), True))
    S.append(step(5, 'أول Polyline فاضي', ['polylines.push_back({ 0, 0 });'],
        'أول دوسة بتعمل <code>polylines.back().count++</code>، ولازم يكون فيه خط موجود.',
        'req', 'شيلناه: البرنامج وقع أول ما دوسنا. <code>back()</code> على قايمة فاضية = قراية من مكان مش موجود.',
        term('[crashed on the first click]'), True))
    return ''.join(S)
