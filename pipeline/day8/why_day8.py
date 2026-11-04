import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day8/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def build_err(n, k=2):
    return '\n'.join([L.split('/')[-1] for L in rd(X + n + '.build').splitlines() if 'error' in L][:k])
def two(a, ca, b, cb): return f'<div class="exrow">{img(a, ca)}{img(b, cb)}</div>'


def build_player():
    S = []
    S.append(step(1, 'public:', ['class Player', '{', 'public:'],
        'الكلاس بيخلّي كل حاجة <code>private</code> لوحده. من غير <code>public:</code> محدش برّه الكلاس يقدر يقرا أو يكتب x و y.',
        'req', 'شيلنا <code>public:</code>: الـ compiler رفض يترجم، حتى الدالة اللي برّه الكلاس مش قادرة توصل لـ x.',
        term(build_err('x_no_public')), True))
    S.append(step(2, 'الـ & في الدالة اللي برّه', ['void Move(Player& player, int xa, int ya)'],
        'من غير <code>&amp;</code> الدالة بتاخد نسخة من اللاعب وتحرّك النسخة. الـ Method مش محتاجة كده لأنها شغالة على الأصل (من خلال <code>this</code>).',
        'req', 'شيلنا الـ <code>&amp;</code>: السطر التالت فضل 2 و ‎-2 بدل 4 و ‎-4. البرنامج ماوقعش، بس الحركة ضاعت.',
        term('\n'.join(out('x_by_value').splitlines()[1:3])), True))
    S.append(step(3, 'نحط قيمة لكل متغير', ['player.speed = 2;'],
        'متغيرات الـ Object مش بتبدأ بصفر لوحدها: بيبقى فيها أي حاجة كانت في الرام. (الـ Constructor اللي هييجي في حلقة جاية بيحل ده.)',
        'req', 'شيلنا سطر السرعة: x طلع رقم عشوائي ضخم.',
        term('\n'.join(out('x_no_speed').splitlines()[1:3])), True))
    S.append(step(4, 'sizeof والعناوين', ['std::cout << "sizeof(Player) = " << sizeof(Player)', 'std::cout << "&player.x     = " << &player.x'],
        'مش جزء من الحركة: بيورّينا إن الـ Object = متغيراته جنب بعض في الرام (12 بايت)، والـ Method مش بتاخد مكان جوه.',
        'opt', 'شيلهم: الحركة مش هتتأثر.'))
    return ''.join(S)


def build_counter():
    S = []
    S.append(step(1, 'private: count', ['private:', 'int count;'],
        'الكلاس عايز يضمن إن العداد عمره ما ينقص. لو count مكشوف، أي حد يكتب <code>clicks.count = -5</code>.',
        'imp', 'كتبنا <code>clicks.count = 3;</code> في main: الـ compiler رفض.',
        term(build_err('x_touch_private', 1)), True))
    S.append(step(2, 'Reset() قبل الاستخدام', ['clicks.Reset();'],
        'نفس مشكلة السرعة: count بيبدأ بأي حاجة. Reset بتحط 0.',
        'req', 'شيلنا <code>clicks.Reset();</code>: العداد طلع رقم سالب غريب بدل 7.',
        term(out('x_no_reset').splitlines()[0]), True))
    S.append(step(3, 'Where() و this', ['clicks.Where();', 'std::cout << "inside Where(): this = " << this << std::endl;'],
        'بيثبت إن الـ Method بتاخد عنوان الـ Object في السر: <code>this</code> = <code>&amp;clicks</code>، ومع other = <code>&amp;other</code>.',
        'opt', 'شيلها: العداد شغال عادي، بس مش هتشوف السر.'))
    return ''.join(S)


def build_texture():
    S = []
    S.append(step(1, 'GL_TEXTURE_MIN_FILTER', ['glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);'],
        'القيمة الافتراضية بتطلب Mipmaps (نسخ أصغر) واحنا ماعملناهاش، فالـ Texture «ناقصة».',
        'req', 'شيلنا السطر: المربع طلع أسود، و <code>glGetError()</code> = 0. يعني مفيش أي رسالة: لازم تعرف القاعدة.',
        img('t_no_min_filter', 'من غير MIN_FILTER: أسود'), True))
    S.append(step(2, 'stbi_set_flip_vertically_on_load(1)', ['stbi_set_flip_vertically_on_load(1);'],
        'الصورة في الملف بتبدأ من فوق، و OpenGL بيبدأ من تحت.',
        'req', 'خلّيناها 0: السهم طلع لتحت، والمربع الأزرق راح تحت شمال.',
        two('t1_texture', 'الصح', 't_no_flip', 'من غير القلب: مقلوبة'), True))
    S.append(step(3, 'glEnable(GL_BLEND)', ['glEnable(GL_BLEND);', 'glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);'],
        'الأماكن الشفافة في الـ PNG لونها أسود وشفافيتها 0. من غير الخلط، الكارت بيرسم اللون ويتجاهل الشفافية.',
        'imp', 'شيلنا <code>glEnable(GL_BLEND)</code>: ظهر مربع أسود حوالين الدايرة.',
        img('t_no_blend', 'من غير Blending: الشفاف بقى أسود'), True))
    S.append(step(4, 'glUniform1i(location, 0) = نفس الخانة', ['texture.Bind(0);', 'glUniform1i(location, 0);'],
        'الـ Shader بيقرا من الخانة اللي بنقولهاله، مش من الـ Texture اللي عملناها.',
        'req', 'بعتنا 1 بدل 0: الخانة 1 فاضية، فالمربع أسود. ومن غير أي خطأ.',
        img('t_wrong_slot', 'الخانة غلط: أسود'), True))
    S.append(step(5, 'المدخل رقم 1 (texCoord)', ['glEnableVertexAttribArray(1);', 'glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 4, (const void*)(sizeof(float) * 2));'],
        'كل ركن لازم يقول يقرا من أنهي نقطة في الصورة.',
        'req', 'شيلنا التفعيل: كل الأركان قرت (0, 0)، وده بكسل شفاف في ركن الصورة، فالمربع كله اختفى.',
        img('t_no_texcoord', 'من غير texCoord: المربع اختفى'), True))
    S.append(step(6, 'if (!pixels)', ['if (!pixels)', 'std::cout << "could not load " << path << std::endl;'],
        'لو اسم الملف غلط أو الفولدر مش جنب البرنامج، stbi_load بترجّع nullptr.',
        'imp', 'غيّرنا الاسم لـ <code>logo2.png</code>: اتطبعت الرسالة وخرجنا. من غير الفحص كنا هنبعت nullptr للكارت.',
        term(out('t_bad_path')), True))
    return ''.join(S)


def build_settings():
    S = []
    S.append(step(1, 'NEAREST و LINEAR', ['MakeTexture(pixels, 4, GL_NEAREST, GL_REPEAT);', 'MakeTexture(pixels, 4, GL_LINEAR, GL_CLAMP_TO_EDGE);'],
        'الصورة 4 × 4 بس وبتتكبّر لمئات البكسلات. NEAREST = مربعات حادة، LINEAR = خلط ناعم بين الألوان.',
        'opt', 'دي اختيارات مش غلطات. الصورة فوق بتوريهم جنب بعض.'))
    S.append(step(2, 'REPEAT و CLAMP_TO_EDGE', ['"    v_TexCoord = texCoord * u_Repeat;\\n"'],
        'الإحداثيات لما توصل 2 بتبقى برّه الصورة. REPEAT بيكرر (4 × 4 مربعات بقت 8 × 8)، و CLAMP بيمد آخر صف وعمود.',
        'opt', 'تحت شمال وتحت يمين في نفس الصورة.'))
    return ''.join(S)


def build_matrix():
    S = []
    S.append(step(1, 'العمود مش الصف', ['col1 = [M[0][0], M[1][0]]', 'col2 = [M[0][1], M[1][1]]'],
        'العمود الأول = المكان اللي î بيروحله. Python بتكتب المصفوفة صف صف، فلازم ناخد أول رقم من كل صف.',
        'req', 'خدنا الصفوف بدل الأعمدة: مثال الفيديو طلع [‎-5, ‎-3] بدل [5, 2]، والدوران لف في الاتجاه العكسي.',
        term('\n'.join(out('m_rows').splitlines()[:2] + out('m_rows').splitlines()[3:4])), True))
    S.append(step(2, 'ترتيب الضرب بيفرق', ['print(rotate @ shear)'],
        'rotate @ shear = «اقص الأول وبعدين لف». العكس تحويل تاني خالص.',
        'imp', 'حسبنا الترتيبين: مصفوفتين مختلفتين.',
        term('\n'.join(out('m_order').splitlines()[7:13])), True))
    return ''.join(S)


def build_brep():
    S = []
    S.append(step(1, 'أويلر بيمسك الغلط في العدد', ['return (int)faces.size() - (int)edges.size() + (int)vertices.size();'],
        'لو الجسم مقفول ومن غير خروم، لازم F − E + V = 2. أي ركن أو وش زيادة أو ناقص بيبوظ المعادلة.',
        'imp', 'زوّدنا ركن ملوش أي ضلع (2, 2, 2): أويلر بقى 3.',
        term(out('b_extra_vertex').splitlines()[0]), True))
    S.append(step(2, 'OpenEdges بيمسك الغلط في التوصيل', ['if (count != 2)'],
        'أويلر بيعد بس. ممكن الأعداد تبقى صح والتوصيل غلط.',
        'imp', 'غيّرنا ضلع واحد في الوش الشمال (11 بقى 10): أويلر لسه 2، بس فيه ضلعين مكشوفين. يعني لازم الفحصين.',
        term(out('b_wrong_edge').splitlines()[0]), True))
    S.append(step(3, 'GL_LINES مش GL_LINE_STRIP', ['glDrawElements(GL_LINES, (int)lines.size(), GL_UNSIGNED_INT, nullptr);'],
        'قايمتنا كل رقمين فيها خط مستقل.',
        'req', 'استخدمنا <code>GL_LINE_STRIP</code>: كل ركن اتوصل باللي بعده في القايمة، وظهرت خطوط مايلة جوه المكعب.',
        two('c2_wireframe', 'GL_LINES', 'b_line_strip', 'GL_LINE_STRIP: خطوط زيادة'), True))
    return ''.join(S)
