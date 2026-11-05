import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day12/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def code(n): return rd(X + n + '.out').split('\nexit=')[1].split('\n')[0] if '\nexit=' in rd(X + n + '.out') else ''
def vg(n, k):
    return '\n'.join(L.split('== ', 1)[-1] for L in rd(X + n + '.out').splitlines() if k in L)
def two(a, ca, b, cb, w='75mm'): return f'<div class="exrow">{img(a, ca, w)}{img(b, cb, w)}</div>'
def last(n, k): return '\n'.join(out(n).splitlines()[-k:])


def build_new():
    S = []
    S.append(step(1, 'delete[] entities (مش delete بس)', ['delete[] entities;'],
        '<code>new Entity[3]</code> حجزت 104 بايت: 8 للعدد و 96 للـ 3. العنوان اللي رجع لينا بعد الـ 8 دول.',
        'req', 'كتبنا <code>delete entities;</code>: البرنامج طبع كل حاجة ووقع في الآخر (exit = ' + code('n_delete_no_arr') + '). <code>delete</code> العادية ادّت free العنوان اللي بعد الـ 8، وده مش أول الحتة اللي malloc ادّتها.',
        term(last('n_delete_no_arr', 2) + '\nexit=' + code('n_delete_no_arr')), True))
    S.append(step(2, 'malloc مابتعملش Constructor', ['Entity* m = (Entity*)malloc(sizeof(Entity));'],
        'لو عايز object حقيقي (name = Unknown) لازم <code>new</code>.',
        'imp', 'طبعنا <code>m->name</code>: طلع فاضي بدل Unknown، والبرنامج ماوقعش. ده بالصدفة: الذاكرة كانت أصفار. ده اسمه Undefined Behavior: على جهاز تاني ممكن يقع.',
        term(last('n_malloc_name', 1)), True))
    S.append(step(3, 'delete e', ['delete e;'],
        'كل <code>new</code> = <code>delete</code>.',
        'req', 'شيلناه: valgrind لقى 32 بايت ضايعين = حجم Entity بالظبط. (وملحوظة: تحت valgrind سطور «bytes» طبعت 0، لأن valgrind بيحط <code>new</code> بتاعته مكان بتاعتنا عشان يراقب.)',
        term(out('n_no_delete').splitlines()[0] + '\n' + vg('n_no_delete', 'definitely lost:')), True))
    return ''.join(S)


def build_place():
    S = []
    S.append(step(1, 'v->~Vector3() بإيدك', ['v->~Vector3();'],
        'Placement new ماحجزش، فمفيش delete. بس الـ Destructor لازم يشتغل (لو الـ class شايل حاجات زي string أو ملف).',
        'req', 'شيلناه: «~Vector3() at ' + out('pl_no_dtor').splitlines()[1].split(' at ')[1] + '» ماظهرش خالص. ظهر بس بتاع h. البرنامج ماوقعش، بس الـ Destructor ماشتغلش.',
        term(last('pl_no_dtor', 2)), True))
    S.append(step(2, 'مفيش delete v', ['delete[] b;'],
        'الذاكرة بتاعة b، و b اتحجزت بـ <code>new int[50]</code>، فهي اللي تترجع بـ <code>delete[] b</code>.',
        'req', 'زوّدنا <code>delete v;</code>: الـ Destructor اشتغل مرتين، و free اتنادت مرتين على نفس العنوان: «double free» والبرنامج وقع (exit = ' + code('pl_delete_v') + ').',
        term(last('pl_delete_v', 3) + '\nexit=' + code('pl_delete_v')), True))
    return ''.join(S)


def build_mip():
    S = []
    S.append(step(1, 'glGenerateMipmap', ['glGenerateMipmap(GL_TEXTURE_2D);'],
        'بيعمل المستويات 1 لـ 8 من المستوى 0 (كل مستوى نص اللي قبله).',
        'req', 'شيلناه: الكارت لقى مستوى واحد بس (levels: 1). المربعين اللي فوق (NEAREST و LINEAR) فضلوا زي ما هما لأنهم مش محتاجين Mipmaps. لكن اللي تحت بقوا <b>سود</b>: Texture «ناقص» (Incomplete) = أسود، ومن غير أي رسالة خطأ.',
        term(out('mm_no_generate')) + two('t1_mipmaps', 'الصح', 'mm_no_generate', 'من غير glGenerateMipmap'), True))
    S.append(step(2, 'الـ Mipmap للتصغير بس', ['glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilters[i]);'],
        'الفيديو (2:13): للتكبير (MAG) فيه NEAREST و LINEAR بس. الـ Mipmap معناه نسخ أصغر، والتكبير مش محتاجها.',
        'req', 'جربنا <code>GL_TEXTURE_MAG_FILTER</code> = <code>GL_LINEAR_MIPMAP_LINEAR</code>: الكارت رفض (GL_INVALID_ENUM) وسابه LINEAR. الصورة زي الأصل بالظبط.',
        term(last('mm_mag_mipmap', 1)) + two('t1_mipmaps', 'الصح', 'mm_mag_mipmap', 'MAG = MIPMAP: اترفض'), True))
    S.append(step(3, 'Anisotropy = 16 في المربع الأخير', ['glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY, aniso[i]);'],
        'ده الفرق الوحيد بين المربعين اللي تحت.',
        'imp', 'قارن الصورتين اللي تحت في الشباك الأصلي: من غيره البعيد رمادي، ومعاه المربعات باينة لمسافة أبعد. نفس الكلام في البرنامج 2: الألوان اتزقت لورا.',
        '', True))
    return ''.join(S)


def build_levels():
    S = []
    S.append(step(1, 'كل المستويات لحد 1 × 1', ['for (int level = 0, w = SIZE; w >= 1; level++, w /= 2)'],
        'لو الفلتر MIPMAP، الكارت عايز كل المستويات من 256 لـ 1 (9 مستويات).',
        'req', 'خلّيناها <code>w &gt;= 2</code>: نقص المستوى الأبيض 1 × 1 بس (3 بايت من 262,143). النتيجة: الشباك كله أسود. ناقص مستوى = Texture ناقص.',
        term(last('lv_missing_last', 2)) + two('t2_mip_levels', 'الصح: 9 مستويات', 'lv_missing_last', 'من غير 1 × 1'), True))
    S.append(step(2, 'LINEAR_MIPMAP_NEAREST', ['glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST);'],
        'NEAREST بين المستويات = الحدود بين الألوان حادة، فنشوف كل مستوى بيبدأ فين.',
        'opt', 'مع <code>LINEAR_MIPMAP_LINEAR</code> الألوان كانت هتتخلط (أحمر ← برتقاني تدريجي). ده الأحسن في لعبة، بس هنا عايزين نشوف الحدود.'))
    return ''.join(S)


def build_np():
    S = []
    S.append(step(1, 'الطول لازم يطابق', ['m[:, 2] = [1, 2]'],
        'العمود فيه خانتين (عدد الصفوف = 2).',
        'req', 'كتبنا <code>[1, 2, 3]</code>: ValueError.',
        term(last('m_wrong_len', 1)), True))
    S.append(step(2, 'النوع int بيقص الكسور', ['m = np.array([[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14]])'],
        'المصفوفة int64: كل خانة رقم صحيح.',
        'imp', 'حطينا <code>m[0, 0] = 2.7</code>: اتخزن 2 من غير أي تحذير. لو عايز كسور اعمل المصفوفة float من الأول.',
        term([L for L in out('m_int_float').splitlines() if '2.7' in L][0]), True))
    S.append(step(3, 'matmul: الداخلي لازم يتساوى', ['print(np.matmul(ones, twos))'],
        '2 × 3 في 3 × 2: الـ 3 = الـ 3.',
        'req', 'ضربنا ones في ones (2 × 3 في 2 × 3): ValueError (size 2 is different from 3). خانة × خانة (<code>*</code>) كانت هتشتغل، بس دي عملية تانية.',
        term(last('m_matmul_shape', 1)), True))
    return ''.join(S)


def build_cad():
    S = []
    S.append(step(1, 'الـ 12 خط كلهم', ['int edges[12][2] = { { 0, 1 }, { 1, 2 }, { 2, 3 }, { 3, 0 }, { 4, 5 }, { 5, 6 }, { 6, 7 }, { 7, 4 }, { 0, 4 }, { 1, 5 }, { 2, 6 }, { 3, 7 } };'],
        'الـ Wireframe هو الخطوط دي وبس.',
        'req', 'لفّينا على 11 بس: الطول 22، والبرنامج مقالش أي حاجة. الـ Wireframe مالوش طريقة يعرف إن ناقصه خط: مفيش وشوش ولا جوه يتحقق منهم.',
        term(out('c_eleven_edges').splitlines()[0]), True))
    S.append(step(2, 'اتجاه كل Normal لبرّه', ['std::vector<Plane> solid = { { { 1, 0, 0 }, 1 }, { { -1, 0, 0 }, 1 }, { { 0, 1, 0 }, 1 }, { { 0, -1, 0 }, 1 }, { { 0, 0, 1 }, 1 }, { { 0, 0, -1 }, 1 } };'],
        'كل مستوى بيقفل ناحية: لو اتنين قافلين نفس الناحية، الناحية التانية مفتوحة.',
        'req', 'غيّرنا <code>-1, 0, 0</code> لـ <code>1, 0, 0</code>: الجسم بقى مفتوح ناحية x السالب، وعدد 12 خلية بقوا «جوه» بدل 8، والحجم 12 غلط.',
        term(out('c_wrong_sign').splitlines()[-1]), True))
    return ''.join(S)
