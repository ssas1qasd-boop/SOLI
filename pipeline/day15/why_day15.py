import sys
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day15/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def code(n): return rd(X + n + '.out').split('\nexit=')[1].split('\n')[0] if '\nexit=' in rd(X + n + '.out') else ''
def errs(n, k=1): return '\n'.join([L.split('/')[-1] for L in rd(X + n + '.build').splitlines() if 'error' in L][:k])
def two(a, ca, b, cb, w='75mm'): return f'<div class="exrow">{img(a, ca, w)}{img(b, cb, w)}</div>'


def build_tpl():
    S = []
    S.append(step(1, 'NeverCalled مش متنادية', ['value.ThisDoesNotExist();'],
        'الغلطة دي موجودة عن قصد عشان نشوف إن الـ Template مش كود.',
        'opt', 'ناديناها <code>NeverCalled(5);</code>: الـ compiler عمل نسخة بـ int، ولقى إن int مالوش دوال: error.',
        term(errs('tp_call_broken')), True))
    S.append(step(2, 'نفس النوع للبارامترين', ['T Biggest(T a, T b)'],
        'a و b الاتنين T: لازم نفس النوع.',
        'req', 'نادينا <code>Biggest(3, 1.5)</code> (int و double): الـ compiler مايعرفش يختار T. الحل: <code>Biggest&lt;double&gt;(3, 1.5)</code>.',
        term(errs('tp_mixed_types')), True))
    return ''.join(S)


def build_arr():
    S = []
    S.append(step(1, 'N رقم ثابت', ['Array<int, 5> numbers;'],
        'N لازم معروف وقت الترجمة: الـ compiler بيكتب الـ class بيه.',
        'req', 'كتبنا <code>int n = 5; Array&lt;int, n&gt;</code>: error. لو الحجم بيتعرف وقت التشغيل استخدم new أو std::vector.',
        term(errs('ar_runtime_size')), True))
    S.append(step(2, 'مفيش فحص للحدود', ['return m_Data[index];'],
        'operator[] بتاعنا بيرجّع الخانة من غير ما يتأكد.',
        'imp', 'كتبنا <code>numbers[5] = 99;</code> (الخانات 0 لـ 4): من غير أدوات البرنامج بيكمل عادي. شغّلناه بـ <code>-fsanitize=address</code>: stack-buffer-overflow.',
        term('\n'.join(out('ar_out_of_range').splitlines()[1:3])), True))
    return ''.join(S)


def build_tr():
    S = []
    S.append(step(1, 'ترتيب T(c) R T(‎-c)', ['Mat3 aroundCenter = Multiply(Translate(0.45f, 0.4f), Multiply(Rotate(90), Translate(-0.45f, -0.4f)));'],
        'اليمين بيحصل الأول: ودّي المركز للأصل الأول.',
        'req', 'بدّلنا الإشارتين (T(‎-c) R T(c)): البرتقاني طار برّه الشباك (الركن بقى (‎-1.05, 0.65)).',
        term(out('tr_wrong_order').splitlines()[-1]) + two('t1_transform2d', 'الصح', 'tr_wrong_order', 'الترتيب غلط: البرتقاني اختفى'), True))
    S.append(step(2, 'GL_TRUE في glUniformMatrix3fv', ['glUniformMatrix3fv(matLoc, 1, GL_TRUE, &shapes[i].m[0][0]);'],
        'OpenGL بيقرا عمود عمود.',
        'req', 'خلّيناها GL_FALSE: الكارت قرا المصفوفة مقلوبة: الدوران بقى بالعكس، والتحريك اتحط في الصف الأخير فماعملش حاجة. الأزرق والبرتقاني بقوا لفة ‎-90 من غير تحريك، فاترسموا فوق بعض تحت يمين، والأخضر فضل متكبر بس مارحش تحت.',
        two('t1_transform2d', 'الصح', 'tr_no_transpose', 'GL_FALSE'), True))
    return ''.join(S)


def build_hom():
    return step(1, 'w = 0 للاتجاه', ['Vec3 direction = { 1, 0, 0 };'],
        'الاتجاه مالوش مكان: لازم يلف بس.',
        'req', 'خلّيناه w = 1: الاتجاه اتحرك زي النقطة (3, 3). يعني Normal أو سرعة هتبوظ لو اتعاملت كنقطة.',
        term(out('hm_direction_w1').splitlines()[2]), True)


def build_mat():
    return step(1, '@ مش *', ['composition = shear @ rotation'],
        '<code>@</code> = ضرب مصفوفات (تركيب).',
        'req', 'كتبنا <code>*</code>: خانة × خانة: [[0, ‎-1], [0, 0]]، وده مش التركيب خالص (والعمود التاني بقى صفر).',
        term('\n'.join(out('m_star').splitlines()[3:6])), True)


def build_cad():
    return step(1, 'التحريك في العمود الرابع', ['return { { { 1, 0, 0, tx }, { 0, 1, 0, ty }, { 0, 0, 1, tz }, { 0, 0, 0, 1 } } };'],
        'إحنا بنضرب M × (x, y, z, 1): التحريك لازم في آخر عمود.',
        'req', 'حطيناه في الصف الأخير (طريقة الكتب اللي بتضرب الركن من الشمال): الركن ماتحركش، و w بقى 15. لازم تعرف المكتبة بتاعتك بتكتب إزاي.',
        term('\n'.join(out('c_bottom_row').splitlines()[5:7])), True)
