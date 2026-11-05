import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day13/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def code(n): return rd(X + n + '.out').split('\nexit=')[1].split('\n')[0] if '\nexit=' in rd(X + n + '.out') else ''
def vg(n, k):
    return '\n'.join(L.split('== ', 1)[-1] for L in rd(X + n + '.out').splitlines() if k in L)
def warn(n): return '\n'.join(L.split('/')[-1] for L in rd(X + n + '.build').splitlines() if 'warning' in L)
def two(a, ca, b, cb, w='75mm'): return f'<div class="exrow">{img(a, ca, w)}{img(b, cb, w)}</div>'
def last(n, k): return '\n'.join(out(n).splitlines()[-k:])


def build_life():
    S = []
    S.append(step(1, 'CreateArray على الـ Heap مش الـ Stack', ['int* array = new int[50];'],
        'المصفوفة لازم تعيش بعد ما CreateArray ترجع.',
        'req', 'خلّيناها <code>int array[50];</code> (غلطة The Cherno): الـ compiler حذّر إننا بنرجّع عنوان متغير محلي، والبرنامج وقع عند أول قراية (exit = ' + code('lf_return_stack') + ' = Segmentation fault). سطر «CreateArray» ماتطبعش.',
        term(warn('lf_return_stack') + '\n' + last('lf_return_stack', 2) + '\nexit=' + code('lf_return_stack')), True))
    S.append(step(2, 'مفيش delete h (عن قصد)', ['Entity* h = new Entity("heap");'],
        'عشان نشوف إن الـ Heap مابيتمسحش لوحده. في برنامج حقيقي لازم delete.',
        'imp', 'زوّدنا <code>delete h;</code> قبل القوس: «Destroyed Entity heap» ظهر في مكانه.',
        term(last('lf_delete_heap', 2)), True))
    return ''.join(S)


def build_scoped():
    S = []
    S.append(step(1, 'delete m_Ptr في الـ Destructor', ['delete m_Ptr;'],
        'ده الشغل كله: الـ ScopedPtr بيموت عند القوس، فيمسح اللي ماسكه.',
        'req', 'شيلناه: «Destroyed Entity» الأولى اختفت، و valgrind لقى حتة ضايعة. (الـ Entity فاضي، و sizeof بتاعه 1 بايت.)',
        term('\n'.join(out('sp_no_delete').splitlines()[:3]) + '\n' + vg('sp_no_delete', 'definitely lost:')), True))
    S.append(step(2, 'ماتنسخش الـ ScopedPtr', ['ScopedPtr e = new Entity();'],
        'لو اتنين ScopedPtr ماسكين نفس العنوان، الاتنين هيعملوا delete.',
        'req', 'زوّدنا <code>ScopedPtr e2 = e;</code>: «Destroyed Entity» مرتين، و double free، والبرنامج وقع (exit = ' + code('sp_copy') + '). ده سبب إن <code>unique_ptr</code> بيمنع النسخ. وده موضوع بكره: Copy Constructors.',
        term(last('sp_copy', 4) + '\nexit=' + code('sp_copy')), True))
    return ''.join(S)


def build_gpu():
    S = []
    S.append(step(1, 'stbi_image_free بعد glTexImage2D', ['glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);', 'stbi_image_free(data);'],
        'الكارت لازم ينسخ الأول. بعد كده بس نمسح.',
        'req', 'مسحنا قبل النسخ: البرنامج ماوقعش ومفيش رسالة، بس الكارت نسخ ذاكرة اترجعت: أول صف (تحت) بقى ألوان عشوائية، وأول بكسل اللي رجع من الكارت مش زي اللي اتحمّل.',
        term('\n'.join(out('g_free_before').splitlines()[:2])) + two('t1_gpu_copy', 'الصح', 'g_free_before', 'free قبل النسخ'), True))
    S.append(step(2, 'glPixelStorei(GL_UNPACK_ALIGNMENT, 1)', ['glPixelStorei(GL_UNPACK_ALIGNMENT, 1);'],
        'عادةً بنحطه مع صور RGB.',
        'opt', 'شيلناه: نفس الصورة بالظبط. ليه؟ الصف هنا 8 × 3 = 24 بايت = مضاعف 4. لو الصورة عرضها 7 مثلاً كان هيبوظ (زي يوم 4).',
        two('t1_gpu_copy', 'الصح', 'g_no_unpack', 'من غيره: زي ما هو'), True))
    return ''.join(S)


def build_atlas():
    S = []
    S.append(step(1, '(float) قبل القسمة', ['u0 = (float)col / CELLS;', 'v0 = (float)row / CELLS;'],
        'col و CELLS الاتنين int: القسمة هتبقى صحيحة.',
        'req', 'شيلنا <code>(float)</code>: 1 / 4 = 0، و 2 / 4 = 0، و 3 / 4 = 0. الأربع مستطيلات بقوا الخانة 0.',
        term('\n'.join(out('a_int_divide').splitlines()[:4])) + two('t2_atlas', 'الصح: 0 و 5 و 10 و 15', 'a_int_divide', 'كلهم الخانة 0'), True))
    S.append(step(2, 'v من الصف مش العمود', ['v0 = (float)row / CELLS;'],
        'u = أفقي = العمود، و v = رأسي = الصف.',
        'req', 'اخترنا الخانات 1 و 6 و 11 و 12 وكتبنا <code>v0 = col / 4</code>: البرنامج طبع «column 1, row 0» بس رسم الخانة 5، و 12 بقت 0. مفيش أي رسالة.',
        term('\n'.join(out('a_swap_rowcol').splitlines()[:4])) + two('t2_atlas', 'الصح', 'a_swap_rowcol', 'v من العمود'), True))
    return ''.join(S)


def build_mat():
    S = []
    S.append(step(1, 'np.radians', ['t = np.radians(degrees)'],
        'cos و sin في NumPy بياخدوا Radians.',
        'req', 'شيلناه: 90 اتعاملت كـ 90 Radian (حوالي 5157 درجة)، و (1, 0) راح (‎-0.448، 0.894) بدل (0, 1). والغريبة إن «30 @ 60 = 90» لسه True: لأن 30 + 60 = 90 بأي وحدة.',
        term('\n'.join(out('m_no_radians').splitlines()[:2] + [out('m_no_radians').splitlines()[5]])), True))
    S.append(step(2, '÷ (u · u) في مصفوفة الإسقاط', ['P = np.outer(u, u) / (u @ u)'],
        'من غيرها بنضرب في طول u تربيع (5).',
        'req', 'شيلناها: P @ x = (14, 7) = 5 × الصح، و P @ P ≠ P. يعني مابقاش إسقاط.',
        term('\n'.join(out('m_no_divide').splitlines()[-4:-1])), True))
    return ''.join(S)


def build_csg():
    S = []
    S.append(step(1, '&& ! في الـ Difference', ['return InSphere(p) && !InBox(p);'],
        'الفرق = جوه A <b>و</b> برّه B.',
        'req', 'كتبنا <code>||</code>: الـ Difference بقى «جوه الكرة أو برّه الصندوق» = تقريباً الفراغ كله: ‎-1.5 و 2.5 بقوا جوه مع إنهم برّه الاتنين.',
        term(out('c_or_not').splitlines()[0] + '\n' + out('c_or_not').splitlines()[5]), True))
    S.append(step(2, 'p.b > p.a (مش >=)', ['if (p.b > p.a)'],
        'الـ Regularize لازم يشيل الحتت اللي طولها صفر.',
        'req', 'خلّيناها <code>&gt;=</code>: [2, 2] فضلت. في 3D ده وش طاير مالوش حجم، وبيبوّظ الحسابات اللي بعده.',
        term(out('c_keep_zero').splitlines()[2]), True))
    return ''.join(S)
