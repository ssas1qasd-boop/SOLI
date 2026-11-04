import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day10/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def code(n): return rd(X + n + '.out').split('\nexit=')[1].split('\n')[0] if '\nexit=' in rd(X + n + '.out') else ''
def build_err(n, k=2):
    return '\n'.join([L.split('/')[-1] for L in rd(X + n + '.build').splitlines() if 'error' in L][:k])
def vg(n, k):
    return '\n'.join(L.split('== ', 1)[-1] for L in rd(X + n + '.out').splitlines() if k in L)
def two(a, ca, b, cb): return f'<div class="exrow">{img(a, ca)}{img(b, cb)}</div>'


def build_ctor():
    S = []
    S.append(step(1, 'Entity() (الـ Constructor الفاضي)', ['Entity()', '{', 'x = 0.0f;', 'y = 0.0f;'],
        '<code>Entity e1;</code> من غير قوسين محتاج Constructor مابياخدش حاجة. ولما كتبنا أي Constructor تاني، C++ بطّل يعمل الفاضي لوحده.',
        'req', 'شيلنا <code>Entity()</code> وسبنا اللي بياخد رقمين: الـ compiler رفض <code>Entity e1;</code>.',
        term(build_err('x_no_default', 1)), True))
    S.append(step(2, 'this->x مش x', ['this->x = x;', 'this->y = y;'],
        'اسم الـ parameter نفس اسم المتغير. <code>this-&gt;</code> بيقول «بتاع الـ object».',
        'req', 'كتبنا <code>x = x;</code>: اترجم من غير أي خطأ، و e2 طبع أرقام عجيبة بدل 10, 5. الرقم اتحط في نفسه، والـ object فضل مش متهيّأ.',
        term('\n'.join(out('x_no_this').splitlines()[3:5])), True))
    S.append(step(3, 'Log() = delete', ['Log() = delete;'],
        'عشان محدش يعمل object من class كله static.',
        'imp', 'زوّدنا <code>Log l;</code> في main: الـ compiler رفض، و <code>Log::Write</code> فضلت شغالة. لو شيلنا السطر، <code>Log l;</code> هتترجم عادي ومش هتعمل حاجة مفيدة.',
        term(build_err('x_log_object', 1)), True))
    return ''.join(S)


def build_dtor():
    S = []
    S.append(step(1, 'delete heap', ['delete heap;'],
        'الـ object اللي على الـ Heap مابيموتش لوحده. <code>delete</code> هو اللي بينادي الـ Destructor.',
        'req', 'شيلنا السطر: «Destroyed Entity!» اتطبعت مرة واحدة بس بدل مرتين، و valgrind (أداة بتراقب الذاكرة) قال 8 بايت ضايعين (الـ Entity = رقمين float).',
        term('\n'.join(out('d_no_delete').splitlines()[0:7]) + '\n' + vg('d_no_delete', 'definitely lost:')), True))
    S.append(step(2, 'delete[] data في ~Buffer', ['delete[] data;'],
        'الـ Constructor حجز 16 رقم بـ <code>new[]</code>، والـ Destructor لازم يرجّعهم.',
        'req', 'شيلنا السطر: البرنامج طبع نفس الكلام بالظبط (مفيش أي علامة!)، بس valgrind لقى 64 بايت ضايعين = 16 × 4. وفي البرنامج الأصلي valgrind قال 0.',
        term(vg('d_no_delete_arr', 'definitely lost:') + '\n' + 'original: ' + vg('d_ok_valgrind', 'in use at exit:')), True))
    return ''.join(S)


def build_crate():
    S = []
    S.append(step(1, 'format حسب عدد القنوات', ['GLenum format = (channels == 4) ? GL_RGBA : GL_RGB;'],
        'crate.png فيها 3 قنوات بس (مفيش شفافية).',
        'req', 'كتبنا <code>GL_RGBA</code> على طول: الكارت قرا كل 4 بايت كبكسل، والصندوق بقى ألوان عشوائية وشرايط.',
        two('t1_crate', 'الصح (RGB)', 't_rgba_for_rgb', 'RGBA لملف 3 قنوات'), True))
    S.append(step(2, 'الـ { } حوالين الـ Texture', ['Texture crate("res/crate.png");', 'std::cout << "loop ended (Escape)" << std::endl;'],
        'الـ Destructor بينادي <code>glDeleteTextures</code>، وده محتاج الشباك (الـ Context) لسه موجود.',
        'req', 'شيلنا الـ { }: الـ Texture مات بعد <code>glfwTerminate</code> عند <code>return 0</code>. البرنامج وقع (exit = ' + code('t_no_scope') + ' = Segmentation fault)، وسطر «~Texture()» ماتطبعش خالص.',
        term(out('t_no_scope') + '\nexit=' + code('t_no_scope')), True))
    S.append(step(3, '× vec4(color, 1.0)', ['"    FragColor = texture(tex0, texCoord) * vec4(color, 1.0);\\n"'],
        'طريقة learnopengl تخلط لون الركن مع الصورة.',
        'opt', 'شيلنا الضرب: الصندوق رجع بلونه الأصلي. يعني الألوان دي زيادة للتجربة بس.',
        two('t1_crate', 'مع لون الأركان', 't_no_tint', 'الصورة لوحدها'), True))
    return ''.join(S)


def build_two():
    S = []
    S.append(step(1, 'tex1 = الخانة 1', ['glUniform1i(glGetUniformLocation(shaderProgram, "tex1"), 1);'],
        'كل sampler في الـ Shader بيبدأ بـ 0. لازم نقول لـ tex1 «اقرا من 1».',
        'req', 'شيلنا السطر: الاتنين قروا من الخانة 0، فاتخلط الصندوق مع نفسه (متكرر 2 × 2) والوش اختفى.',
        two('t2_two_textures', 'الصح', 't_no_unit1', 'tex1 من الخانة 0'), True))
    S.append(step(2, 'face.a في الـ mix', ['"    FragColor = mix(texture(tex0, texCoord), face, face.a * amount);\\n"'],
        'الوش خلفيته شفافة. من غير <code>face.a</code> الشفاف هيتحسب لون (أسود).',
        'imp', 'خلّيناها <code>mix(texture(tex0, texCoord), face, amount)</code> بـ 1.0: الصندوق اختفى وكل الأماكن الشفافة بقت سودا.',
        two('t2_two_textures', 'بـ face.a', 't_amount1', 'من غير الشفافية'), True))
    return ''.join(S)


def build_mat():
    S = []
    S.append(step(1, 'column_stack (أعمدة)', ['A = np.column_stack([T(e1), T(e2)])'],
        'T(e₁) و T(e₂) لازم يبقوا <b>أعمدة</b>: العمود رقم j = e_j راح فين.',
        'req', 'خلّيناهم صفوف (<code>np.vstack</code>): A بقت 2 × 3، و A @ v رفض يشتغل.',
        term('\n'.join(out('m_rows').splitlines()[7:10]) + '\n' + out('m_rows').splitlines()[-1]), True))
    S.append(step(2, 'A @ F.T (مش A.T)', ['moved = (A @ F.T).T'],
        'نفس الكلام في البرنامج 2: لو قلبنا A، الأعمدة بقت صفوف.',
        'req', 'كتبنا <code>A.T</code>: التكبير والمراية زي ما هما (متماثلين)، بس اللف بقى ‎-90 والميل بقى لفوق. الغلطة دي مش بتطلّع أي خطأ.',
        img('m_transposed', 'A.T: اللف والميل غلط', '150mm'), True))
    return ''.join(S)


def build_cyl():
    return step(1, 'اللحام مرتين في حلقة الجنب', ['{ { { 0, true }, { 1, false }, { 2, false }, { 1, true } } },'],
        'الجنب مستطيل ملفوف: حرفه الشمال ويمين هما نفس خط اللحام. فالحلقة لازم تعدي عليه رايح وجاي.',
        'req', 'شيلنا آخر <code>{ 1, true }</code>: أويلر لسه 2 (مابيعدش الاستخدامات)، بس العد قال ضلع 1 متلمس مرة واحدة: الشكل مفتوح.',
        term('\n'.join(L for L in out('b_no_seam_back').splitlines() if 'loop:' in L and 'face 1' in L or 'used' in L)), True)


def build_hole():
    return step(1, 'حلقة الخرم في الغطا والقاع', ['{ { { 0, 3, 2, 1 }, { 8, 9, 10, 11 } } },', '{ { { 4, 5, 6, 7 }, { 12, 15, 14, 13 } } },'],
        'حيطان الخرم بتلمس الغطا والقاع عند حدود الخرم. الحلقة التانية هي اللي بتقفل الحدود دي.',
        'req', 'شيلنا الحلقتين: الأرقام زي ما هي تقريباً، بس 8 أضلاع بقوا متلمسين مرة واحدة: الشكل فيه فتحة.',
        term('\n'.join(out('h_no_inner').splitlines()[0:11])), True)
