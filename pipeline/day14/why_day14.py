import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day14/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def code(n): return rd(X + n + '.out').split('\nexit=')[1].split('\n')[0] if '\nexit=' in rd(X + n + '.out') else ''
def errs(n, k=1): return '\n'.join([L.split('/')[-1] for L in rd(X + n + '.build').splitlines() if 'error' in L][:k])
def two(a, ca, b, cb, w='75mm'): return f'<div class="exrow">{img(a, ca, w)}{img(b, cb, w)}</div>'
def last(n, k): return '\n'.join(out(n).splitlines()[-k:])


def build_basics():
    return step(1, 'delete مرة واحدة بس', ['delete pa;'],
        'pa و pb نفس العنوان: object واحد.',
        'req', 'زوّدنا <code>delete pb;</code>: double free والبرنامج وقع (exit = ' + code('cp_delete_both') + '). نسخ الـ Pointer مابيعملش object تاني.',
        term(last('cp_delete_both', 1) + '\nexit=' + code('cp_delete_both')), True)


def build_string():
    S = []
    S.append(step(1, 'الـ Copy Constructor (Deep Copy)', ['String(const String& other)', 'm_Buffer = new char[m_Size + 1];', 'memcpy(m_Buffer, other.m_Buffer, m_Size + 1);'],
        'من غيره C++ بينسخ m_Buffer زي ما هو.',
        'req', 'شيلناه: «Charno / Charno» (الاتنين اتغيروا)، والعنوانين نفس الرقم، والطباعة التانية بالقيمة طلعت زبالة (النسخة الأولى ماتت ومسحت الـ Buffer)، وفي الآخر double free (exit = ' + code('s_shallow') + '). زي ما The Cherno قال بالظبط.',
        term(out('s_shallow') + '\nexit=' + code('s_shallow')), True))
    S.append(step(2, 'const String& في PrintByReference', ['void PrintByReference(const String& string)'],
        'عشان مفيش نسخ.',
        'imp', 'لو خلّيت كل الدوال بالقيمة: Copied! بتتطبع مع كل نداء (هنا 3 مرات مع إن واحدة بس مقصودة). ولو منعت النسخ (<code>= delete</code>) الـ compiler بيوقفك عند كل نسخة:',
        term(errs('s_copy_deleted', 3)), True))
    return ''.join(S)


def build_texcopy():
    S = []
    S.append(step(1, 'ماتبعتش الـ Texture بالقيمة', ['void Describe(Texture texture)'],
        'ده الغلط المقصود في البرنامج 1.',
        'req', 'سألنا الكارت بعد كل Bind: id 1 تمام، و id 2 = 1282 = GL_INVALID_OPERATION (الرقم مابقاش Texture). فالكارت فضل رابط الأحمر، والأزرق اترسم أحمر. ومفيش أي رسالة لو ماسألتش.',
        term('\n'.join(L for L in out('tc_bind_error').splitlines() if 'Bind' in L)), True))
    return ''.join(S)


def build_texref():
    return step(1, '= delete للنسخ', ['Texture(const Texture& other) = delete;'],
        'يمنع الغلطة دي من الأول.',
        'imp', 'جربنا نكتب <code>Texture copy = blue;</code>: البرنامج ماترجمش أصلاً. أحسن ما يترجم ويرسم غلط.',
        term(errs('tr_try_copy', 1)), True)


def build_mat():
    S = []
    S.append(step(1, 'الأركان بالترتيب', ['square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)'],
        'Shoelace محتاج الأركان ماشية حوالين الشكل.',
        'req', 'بدّلنا ركنين ((1, 1) قبل (1, 0)): الشكل بقى «فراشة» بتقطع نفسها، والمساحة 0 قبل وبعد. و det(A) لسه 2: الـ det مايعرفش الأركان.',
        term(out('m_corner_order').splitlines()[2]), True))
    S.append(step(2, 'det ≠ 0 قبل العكس', ['det = a * d - b * c'],
        'العكس بيقسم على det.',
        'req', 'خلّينا A = B (det = 0): الحساب بإيدنا طلّع inf و ‎-inf مع تحذير، و np.linalg.inv رمى LinAlgError. يعني افحص det الأول، أو امسك الغلط زي البرنامج.',
        term(out('m_inverse_singular').splitlines()[1] + '\n' + out('m_inverse_singular').splitlines()[-1]), True))
    return ''.join(S)


def build_git():
    S = []
    S.append(step(1, 'git add قبل أول commit', ['git("add", "site.css")'],
        'git مابيسجلش ملف مش متابعه.',
        'req', 'شيلناه: الملف فضل <code>??</code>، و <code>-a</code> ماضافهوش (بيضيف المتابَع بس)، والسجل فاضي، والرجوع للأصل مانفعش: الملف فضل orange.',
        term('\n'.join(out('g_no_add').splitlines()[2:4] + out('g_no_add').splitlines()[6:8])), True))
    S.append(step(2, 'الـ header قبل المحتوى', ['header = b"blob " + str(len(content)).encode() + b"\\0"'],
        'git بيحسب البصمة على «blob الحجم\\0» + المحتوى.',
        'req', 'حسبنا SHA-1 للمحتوى لوحده: بصمة تانية خالص، و git قال مش موجودة.',
        term('\n'.join(out('g_no_header').splitlines()[1:3]) + '\n' + out('g_no_header').splitlines()[-1]), True))
    return ''.join(S)
