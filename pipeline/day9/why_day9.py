import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day9/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def build_err(n, k=2):
    return '\n'.join([L.split('/')[-1] for L in rd(X + n + '.build').splitlines() if 'error' in L][:k])
def two(a, ca, b, cb): return f'<div class="exrow">{img(a, ca)}{img(b, cb)}</div>'


def build_struct():
    S = []
    S.append(step(1, 'public: في الـ class', ['class PlayerC', '{', 'public:'],
        'الـ class بيخلّي كل حاجة <code>private</code> لوحده. من غير <code>public:</code>، main مش هتقدر تكتب <code>c.x = 0</code>.',
        'req', 'شيلنا <code>public:</code>: الـ compiler رفض يترجم.',
        term(build_err('x_class_no_public')), True))
    S.append(step(2, 'الـ struct مش محتاج public:', ['struct PlayerS'],
        'ده الفرق الوحيد اللي The Cherno قاله. وعشان نتأكد إن الفرق في «الافتراضي» بس، عملنا العكس: كتبنا <code>private:</code> في الـ struct.',
        'imp', 'كتبنا <code>private:</code> أول الـ struct: نفس الخطأ بالظبط. يعني الـ struct والـ class نفس الحاجة لما نكتب الكلمة بإيدنا.',
        term(build_err('x_struct_private')), True))
    S.append(step(3, 'Vec2 بقيم أولية { }', ['Vec2 position = { 1.0f, 2.0f };'],
        'طريقة سريعة نحط بيها القيم بالترتيب. شغالة مع الـ struct البسيط اللي كله public.',
        'opt', 'ممكن بدلها <code>position.x = 1.0f; position.y = 2.0f;</code>: نفس النتيجة.'))
    return ''.join(S)


def build_vertex():
    S = []
    S.append(step(1, 'float مش double', ['float x, y;', 'float u, v;'],
        'الكارت بيستنى كل رقم 4 بايت (<code>GL_FLOAT</code>). و <code>numbers</code> نوعه <code>float*</code>.',
        'req', 'غيّرنا لـ <code>double</code>: الـ compiler رفض يحط عنوان double في <code>float*</code>. ولو في برنامج OpenGL، كان الكارت هيقرا البايتات غلط.',
        term(build_err('x_vertex_double', 1)), True))
    S.append(step(2, 'الـ struct = الـ stride', ['std::cout << "sizeof(Vertex) = " << sizeof(Vertex) << " bytes  (the stride)" << std::endl;'],
        'أي متغير نزوّده في الـ struct بيكبّر الركن، فلازم الـ stride يتغير معاه.',
        'imp', 'زوّدنا <code>int id;</code>: الركن بقى 20 بايت، و numbers[10] بقى 0.5 (x بتاع ركن 2) بدل u. لو الـ stride فضل 16 في <code>glVertexAttribPointer</code>، الكارت هيقرا أركان غلط.',
        term('\n'.join(out('x_vertex_extra').splitlines()[i] for i in (0, 3, 5))), True))
    return ''.join(S)


def build_cat():
    S = []
    S.append(step(1, 'glGenerateMipmap', ['glGenerateMipmap(GL_TEXTURE_2D);'],
        'الـ MIN_FILTER بتاعنا فيه MIPMAP، يعني بيطلب نسخ مصغّرة.',
        'req', 'شيلنا السطر: المربع أسود، و <code>glGetError()</code> = 0. نفس مشكلة امبارح بالظبط بشكل تاني.',
        img('t_no_mipmap', 'من غير glGenerateMipmap: أسود'), True))
    S.append(step(2, 'GL_RGBA = عدد القنوات في الملف', ['glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, widthImg, heightImg, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes);'],
        'إحنا طلبنا من stbi_load «زي الملف» (0)، والملف 4 قنوات. فلازم نقول للكارت 4.',
        'req', 'كتبنا <code>GL_RGB</code>: الكارت قرا كل 3 بايت كبكسل، فالألوان والصفوف اتزحلقت.',
        img('t_rgb', 'GL_RGB مع ملف 4 قنوات: بايظة'), True))
    S.append(step(3, 'stbi_set_flip_vertically_on_load(true)', ['stbi_set_flip_vertically_on_load(true);'],
        'نفس سبب امبارح: الملف بيبدأ من فوق، و OpenGL من تحت.',
        'req', 'خلّيناها false: القطة اتقلبت.',
        two('t1_pixel_cat', 'الصح', 't_no_flip', 'من غير القلب'), True))
    S.append(step(4, 'MAG_FILTER = GL_NEAREST', ['glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);'],
        'الصورة 16 × 16 بتتكبّر لمئات البكسلات. NEAREST بيحافظ على المربعات (Pixel Art).',
        'opt', 'خلّيناها GL_LINEAR: اشتغلت، بس القطة بقت مغبّشة.',
        img('t_linear', 'LINEAR: مغبّشة'), True))
    return ''.join(S)


def build_wrap():
    return step(1, 'لون الحدود', ['glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border);'],
        'CLAMP_TO_BORDER بياخد اللون ده لكل حاجة برّه الصورة. الافتراضي 0 0 0 0 (شفاف).',
        'opt', 'شيلنا السطر: الحدود الحمرا اختفت (بقت شفافة)، والتلاتة التانيين زي ما هما.',
        two('t2_wrap_modes', 'بلون الحدود', 'w_no_border', 'من غير لون: شفاف'), True)


def build_transform():
    S = []
    S.append(step(1, 'المصفوفة = الدالة', ['A = [[1, 2, 0],', '[0, 0, 3]]'],
        'كل صف = معادلة رقم طالع. الصف الأول (1, 2, 0) = x₁ + 2x₂ + 0x₃.',
        'req', 'لخبطنا الأعمدة (‏[[1, 0, 2], [0, 3, 0]]): (1, 1, 1) لسه (3, 3) بالصدفة، بس (2, 4, 1) طلع (4, 12) بدل (10, 3). يعني مثال واحد مش كفاية عشان نتأكد.',
        term('\n'.join(out('m_wrong_matrix').splitlines()[3:5])), True))
    S.append(step(2, 'P @ مش P.T @', ['screen = (P @ centered.T).T'],
        'P مقاسها 2 × 3: بتاخد 3 أرقام. لو قلبناها بقت 3 × 2 وعايزة رقمين.',
        'req', 'كتبنا <code>P.T</code>: NumPy رفض لأن المقاسات مش راكبة على بعض.',
        term(out('m_shape').splitlines()[-1].split(': ', 1)[0] + ': matmul: Input operand 1 has a mismatch in its core dimension 0 … (size 3 is different from 2)'), True))
    return ''.join(S)


def build_mesh():
    S = []
    S.append(step(1, 'std::set مش std::vector', ['std::set<std::pair<unsigned int, unsigned int>> edges;', 'edges.insert({ std::min(p, q), std::max(p, q) });'],
        'كل ضلع بين مثلثين، فبيتزوّد مرتين. الـ set بيشيل التكرار.',
        'req', 'استخدمنا vector: E طلع 36 بدل 18، وأويلر ‎-16 بدل 2.',
        term(out('b_no_set').splitlines()[2]), True))
    S.append(step(2, 'std::min و std::max', ['edges.insert({ std::min(p, q), std::max(p, q) });'],
        'الضلع (1, 2) هو نفسه (2, 1). لو ماخدناش الصغير الأول، الـ set هيشوفهم ضلعين.',
        'imp', 'جرّبها بإيدك: اكتب <code>{ p, q }</code> وشوف E بقى كام.'))
    return ''.join(S)


def build_bary():
    return step(1, 'out vec3 color (من غير flat)', ['"out vec3 color;\\n"', '"in vec3 color;\\n"'],
        'من غير <code>flat</code> الكارت بيخلط ألوان الأركان التلاتة بـ α و β و γ لكل بكسل (اللي حسبناه بإيدنا).',
        'req', 'كتبنا <code>flat</code>: المثلث كله أزرق (لون آخر ركن)، والكارت بقى بيقول 0 0 255 وحسابنا 63 64 128.',
        two('c2_barycentric', 'Interpolation', 'b_flat', 'flat: لون واحد') + term(out('b_flat').splitlines()[1]), True)
