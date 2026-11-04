import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day11/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def code(n): return rd(X + n + '.out').split('\nexit=')[1].split('\n')[0] if '\nexit=' in rd(X + n + '.out') else ''
def build_warn(n, k=1):
    return '\n'.join([L.split('/')[-1] for L in rd(X + n + '.build').splitlines() if 'warning' in L][:k])
def vg(n, k):
    return '\n'.join(L.split('== ', 1)[-1] for L in rd(X + n + '.out').splitlines() if k in L)
def two(a, ca, b, cb, w='75mm'): return f'<div class="exrow">{img(a, ca, w)}{img(b, cb, w)}</div>'
DIFF = {'t1_wrap': (0, 0, 0), 'w_int_floor': (21385, 0, 0), 'w_mirror_no_one': (0, 31668, 0), 'w_repeat_sampler': (0, 0, 28106)}
TOTAL = 72384


def build_stack():
    S = []
    S.append(step(1, 'delete[] harray (مش delete بس)', ['delete[] harray;'],
        'اللي اتحجز بـ <code>new int[5]</code> لازم يترجع بـ <code>delete[]</code>.',
        'req', 'شيلنا السطر: البرنامج طبع نفس الكلام بالظبط، بس valgrind (أداة بتراقب الذاكرة) لقى 20 بايت ضايعين = 5 × 4. ولما كتبنا <code>delete harray;</code> من غير [ ]: valgrind قال Mismatched (مش متطابق) وعدد 2 أخطاء.',
        term(vg('x_no_delete_arr', 'definitely lost:') + '\n' + vg('x_delete_not_arr', 'Mismatched free') + '\n' + vg('x_delete_not_arr', 'ERROR SUMMARY') + '\noriginal: ' + vg('x_ok_valgrind', 'in use at exit:')), True))
    S.append(step(2, 'delete v جوه اللوب', ['delete v;'],
        'كل لفة بتعمل Vector3 جديد على الـ Heap. لو مارجعناهوش في نفس اللفة، العنوان بيضيع مع اللفة اللي بعدها.',
        'req', 'شيلنا السطر: valgrind لقى 1,200 بايت ضايعين في عدد 100 حتة = 100 × 12. ده اسمه Memory Leak: البرنامج شغال عادي وبياكل رام في السكوت.',
        term(vg('s_no_delete_loop', 'in use at exit:') + '\n' + vg('s_no_delete_loop', 'definitely lost in loss record')), True))
    S.append(step(3, 'الصورة على الـ Heap (new) مش الـ Stack', ['unsigned char* pixels = new unsigned char[width * height * 4];'],
        'الـ Stack هنا 8 MB بس (<code>ulimit -s</code> = 8192)، والصورة 16 MB. وكمان لازم تعيش بعد ما LoadTexture ترجع.',
        'req', 'خلّيناها <code>unsigned char pixels[2048 * 2048 * 4];</code>: الـ compiler حذّر إننا بنرجّع عنوان متغير محلي، والبرنامج وقع أول ما دخل LoadTexture (exit = ' + code('s_stack_texture') + ' = Segmentation fault). سطر «LoadTexture: 16 MB» ماتطبعش خالص.',
        term(build_warn('s_stack_texture') + '\n' + out('s_stack_texture') + '\nexit=' + code('s_stack_texture')), True))
    S.append(step(4, 'N = 100 بس', ['const int N = 100;'],
        'عدد صغير عشان البنش يمشي على كل لفة. بس الأرقام مع 100 بتتهز (أول لفات أبطأ).',
        'opt', 'خلّيناه مليون: الـ Stack حوالي 3 ns والـ Heap حوالي 16 ns. يعني أبطأ 5 مرات تقريباً، زي كلام The Cherno.',
        term(out('s_million').splitlines()[0] + '\n' + out('s_million').splitlines()[1] + '\n' + out('s_million').splitlines()[2]), True))
    return ''.join(S)


def build_wrap():
    S = []
    S.append(step(1, 'floor مش تقريب لـ int', ['"        return uv - floor(uv);\\n"'],
        '<code>floor(‎-0.3)</code> = ‎-1، فالجزء العشري 0.7 (صح). لكن <code>int(‎-0.3)</code> = 0 لأنه بيشيل الكسر بس.',
        'req', f'كتبنا <code>uv - vec2(ivec2(uv))</code>: الحتة اللي u أو v فيها سالب بقت أرقام سالبة، والكارت قصّها على الحرف. عدد {DIFF["w_int_floor"][0]:,} بكسل من {TOTAL:,} اختلفوا عن الصف اللي فوق.',
        two('t1_wrap', 'الصح: الصفين زي بعض', 'w_int_floor', 'int: الشمال تحت باظ'), True))
    S.append(step(2, '1.0 - في المراية', ['"        return 1.0 - abs(mod(uv, 2.0) - 1.0);\\n"'],
        'من غير <code>1.0 -</code> المراية بتبدأ مقلوبة: 0 بيبقى 1.',
        'req', f'شيلناها: الحرف اتقلب في كل الخانات (مراية بس من الناحية الغلط). عدد {DIFF["w_mirror_no_one"][1]:,} بكسل اختلفوا.',
        two('t1_wrap', 'الصح', 'w_mirror_no_one', 'من غير 1.0 -'), True))
    S.append(step(3, 'CLAMP_TO_EDGE للصف اللي تحت', ['letter.SetWrap(GL_CLAMP_TO_EDGE);'],
        'دالتنا بتطلّع أرقام من 0 لـ 1 بالظبط. الـ 1.0 مع REPEAT بترجع لأول الصورة.',
        'imp', f'خلّيناها <code>GL_REPEAT</code>: REPEAT والمراية فضلوا صح، بس الـ CLAMP بقى فيه ألوان من الناحية التانية في الأركان (الكارت كرر تاني فوق اللي إحنا قصيناه). عدد {DIFF["w_repeat_sampler"][2]:,} بكسل اختلفوا.',
        two('t1_wrap', 'الصح', 'w_repeat_sampler', 'REPEAT تحت'), True))
    return ''.join(S)


def build_proc():
    S = []
    S.append(step(1, 'glPixelStorei(GL_UNPACK_ALIGNMENT, 1)', ['glPixelStorei(GL_UNPACK_ALIGNMENT, 1);'],
        'الصف 6 بايت. الكارت بيفترض إن كل صف بيبدأ عند مضاعف 4.',
        'req', 'شيلناه: الكارت قرا أول صف صح، وبعدين نط بايتين قبل التاني. الألوان بقت أصفر وكحلي، والرقعة مش زي الدالة.',
        two('t2_procedural', 'الصح', 'p_no_unpack', 'من غير glPixelStorei'), True))
    S.append(step(2, 'NEAREST للتكبير', ['glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);'],
        'الـ 2 × 2 بتتكبر لـ 312 × 312 بكسل. NEAREST = كل بكسل ياخد لون أقرب بكسل في الصورة.',
        'req', 'خلّيناه <code>GL_LINEAR</code>: الكارت خلط الألوان الأربعة، والرقعة بقت بنفسجي ضبابي. الدالة مافيهاش المشكلة دي: بتحسب اللون بالظبط في كل بكسل.',
        two('t2_procedural', 'NEAREST', 'p_linear', 'LINEAR'), True))
    return ''.join(S)


def build_mat():
    S = []
    S.append(step(1, 'المقاسات لازم تتساوى', ['if X.shape != Y.shape:'],
        'Khan: الجمع متعرّف بس لنفس المقاس.',
        'req', 'غيّرنا F لصف واحد <code>[[5, 7]]</code> (1 × 2): دالتنا قالت undefined، لكن NumPy جمعها عادي! NumPy بيكرر الصف على كل الصفوف (Broadcasting). مريح في الكود، بس مش جمع مصفوفات بتاع الرياضيات.',
        term('\n'.join(out('m_broadcast').splitlines()[-4:])), True))
    S.append(step(2, '[[3, 1]] * 6 (صفوف)', ['move = np.array([[3, 1]] * 6, dtype=float)'],
        'مصفوفة النقل لازم 6 × 2 زي البيت.',
        'req', 'كتبنا <code>[3, 1] * 6</code>: بقت 12 رقم في صف واحد، و NumPy رفض.',
        term(out('m_flat_move').splitlines()[-1]), True))
    return ''.join(S)


def build_obj():
    S = []
    S.append(step(1, 'ترتيب الأركان في f', ['obj << "f 1 4 3 2\\nf 5 6 7 8\\nf 1 5 8 4\\nf 2 3 7 6\\nf 1 2 6 5\\nf 4 8 7 3\\n";'],
        'الترتيب بيحدد اتجاه الـ Normal.',
        'req', 'غيّرنا القاع لـ <code>f 1 2 3 4</code> (عكس الفيديو): الـ Normal بقى (0, 0, 4) لفوق، يعني جوه المكعب. والعدد وأويلر ماتغيّروش! الغلطة دي مش بتبان غير في الـ Normal (والكارت هيشيل الوش ده مع Back Face Culling).',
        term('\n'.join(out('o_flip_bottom').splitlines()[1:3]) + '\n' + out('o_flip_bottom').splitlines()[-1]), True))
    S.append(step(2, 'index - 1', ['f.push_back(index - 1);'],
        'OBJ بيعد من 1.',
        'req', 'شيلنا الـ - 1: الوش الأول طلع Normal عجيب (4, ‎-4, ‎-4)، وفي الوش التاني البرنامج حاول يقرا الركن رقم 8 (والأركان من 0 لـ 7) فوقف (exit = ' + code('o_one_based') + '). شغّلناه بـ <code>-D_GLIBCXX_ASSERTIONS</code> عشان الـ vector يفحص الأرقام.',
        term(out('o_one_based').splitlines()[1] + '\n' + out('o_one_based').splitlines()[2].split(': ')[-1] + '\nexit=' + code('o_one_based')), True))
    return ''.join(S)


def build_mesh():
    return step(1, '% n في الجنب', ['int j = (i + 1) % n;'],
        'الدايرة لازم تقفل: بعد الركن 7 ييجي 0.',
        'req', 'شيلنا الـ % n: البرنامج ماوقعش ولا طلّع خطأ، بس E بقت 45 بدل 42 وأويلر ‎-1 بدل 2. أويلر هو اللي كشف إن الشكل مش مقفول.',
        term(out('b_no_modulo').splitlines()[0]), True)
