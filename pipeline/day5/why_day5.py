import sys, re
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day5/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def code(n): return rd(X + n + '.out').rsplit('exit=', 1)[1].strip()
def err(n, k=('error',)):
    return '\n'.join(l.split('/')[-1] for l in rd(X + n + '.build').splitlines() if any(w in l for w in k) and re.search(r'\.cpp:\d+', l))
def pyerr(n):
    return rd(X + n + '.out').split('\nexit=')[0].strip().splitlines()[-1]
def two(a, ca, b, cb):
    return f'<div class="exrow">{img(a, ca)}{img(b, cb)}</div>'


def build_swap():
    S = []
    S.append(step(1, 'نبعت العناوين مش القيم', ['swap(&x, &y);', 'void swap(int* a, int* b)'],
        'عشان الدالة تقدر توصل لـ <code>x</code> و <code>y</code> الأصليين اللي في <code>main</code>.',
        'req', 'خلّينا الدالة تاخد <code>int a, int b</code> ونادينا <code>swap(x, y)</code>: البرنامج اشتغل عادي، بس ماحصلش تبديل. الدالة بدّلت نسخ واترمت.',
        term(out('s_value')), True))
    S.append(step(2, 'سطر التعريف جوه main', ['void swap(int* p, int* q);'],
        'الدالة مكتوبة <b>تحت</b> <code>main</code>، فلازم الـ compiler يعرف شكلها قبل النداء.',
        'req', 'شيلناه: الـ compiler راح يدوّر على <code>swap</code> تانية، ولقى <code>std::swap</code> (بسبب <code>using namespace std</code>)، ورفض لأنها مش بتاخد عناوين بالشكل ده.',
        term(err('s_no_decl')), True))
    S.append(step(3, 'الـ & في النداء', ['swap(&x, &y);'],
        'الدالة مستنية عنوان (<code>int*</code>)، و <code>x</code> لوحدها رقم.',
        'req', 'كتبنا <code>swap(x, y)</code>: رفض. مينفعش تحط رقم مكان عنوان.', term(err('s_no_amp')), True))
    S.append(step(4, 'النجمة في temp = *a', ['temp = *a;'],
        'عايزين القيمة اللي في العنوان، مش العنوان نفسه.',
        'req', 'كتبنا <code>temp = a;</code>: رفض. <code>temp</code> رقم و <code>a</code> عنوان.', term(err('s_no_star')), True))
    S.append(step(5, 'المتغير المؤقت temp', ['int temp;', 'temp = *a;', '*b = temp;'],
        'لما نكتب 20 جوه <code>x</code>، الـ 10 القديمة بتضيع لو مش متشالة في حتة.',
        'req', 'كتبنا <code>*a = *b; *b = *a;</code> من غير <code>temp</code>: الاتنين بقوا 20. الـ 10 ضاعت.', term(out('s_no_temp')), True))
    return ''.join(S)


def build_shader():
    S = []
    S.append(step(1, 'فحص الترجمة ورسالة الخطأ', ['glGetShaderiv(id, GL_COMPILE_STATUS, &result);', 'glGetShaderInfoLog(id, length, &length, message);'],
        'الـ Shader بيتترجم وقت التشغيل جوه الكارت، مش لما تعمل Build. لو فيه غلطة، مش هتعرف غير من هنا.',
        'imp', 'شيلنا <code>;</code> من آخر سطر اللون: البرنامج طبع رسالة فيها رقم السطر جوه الـ Shader والسبب. ولاحظ إن المثلث طلع <b>أبيض</b> مش أحمر: الـ Fragment Shader اتمسح، وكارت الشاشة رسم بلون من عنده. على كارت تاني ممكن يطلع أسود. من غير الفحص ده كنت هتشوف أبيض ومتعرفش ليه.',
        term(out('r_syntax')) + img('r_syntax', 'المثلث أبيض: الـ Fragment Shader فشل'), True))
    S.append(step(2, 'vec4 مع إن البيانات رقمين', ['"layout(location = 0) in vec4 position;\\n"'],
        'الكارت بيكمّل z = 0 و w = 1 لوحده، و <code>gl_Position</code> لازم يبقى <code>vec4</code>.',
        'imp', 'خلّيناها <code>vec2</code>: الـ Vertex Shader ماترجمش (مينفعش تحط vec2 في vec4)، والشاشة سودا خالص.',
        term(out('r_vec2')) + img('r_vec2', 'شاشة سودا: مفيش Vertex Shader'), True))
    S.append(step(3, 'الألوان من 0.0 لـ 1.0', ['"    color = vec4(1.0, 0.0, 0.0, 1.0);\\n"'],
        'OpenGL بيقيس الألوان من 0 لـ 1، مش من 0 لـ 255 زي برامج الرسم.',
        'opt', 'كتبنا 255.0 بدل 1.0: نفس الأحمر بالظبط، لأن أي حاجة فوق 1 بتتقص لـ 1. وبتغيير رقمين بس (<code>0.0, 1.0, 0.0</code>) المثلث بقى أخضر من غير ما نلمس C++.',
        two('r_255', '255.0: نفس الأحمر', 'r_green', '0, 1, 0: أخضر'), True))
    S.append(step(4, 'out و in بنفس الاسم', ['"out vec4 v_Position;\\n"', '"in vec4 v_Position;\\n"'],
        'دي الطريقة الوحيدة الـ Vertex يبعت بيها حاجة للـ Fragment.',
        'req', 'شيلنا <code>out</code> وسطر <code>v_Position = position;</code> من الـ Vertex: مفيش ولا رسالة (لأن برنامجنا مش بيفحص الـ Link)، والمثلث طلع كحلي غامق في كل حتة: الـ Fragment قرا قيمة محدش كتبها.',
        img('r_no_out', 'من غير out: لون واحد غلط ومفيش رسالة'), True))
    S.append(step(5, 'الضرب في 1.5 جوه الـ Vertex', ['"    gl_Position = vec4(position.x * 1.5, position.y * 1.5, 0.0, 1.0);\\n"'],
        'ده «التعديل»: الشكل بيتغير في الكارت من غير ما نغيّر <code>positions</code>.',
        'opt', 'جربنا 0.5 بدل 1.5: المثلث صغر. وجربنا <code>-position.y</code>: اتقلب على راسه.',
        two('r_small', '× 0.5: صغير', 'r_flip', '‎-y: مقلوب'), True))
    return ''.join(S)


def build_numpy():
    S = []
    S.append(step(1, 'np.array بدل List', ['a = np.array([1, 2, 3])'],
        'الـ List العادية مش بتفهم الحساب على كل العناصر.',
        'req', 'خلّينا <code>a = [1, 2, 3]</code> List عادية: <code>a * 2</code> كررت القايمة بدل ما تضرب، و <code>a + 2</code> وقّفت البرنامج بخطأ.',
        term(out('n_list').replace('Traceback (most recent call last):\n', '').split('\n    ')[0] + '\n' + pyerr('n_list')), True))
    S.append(step(2, 'copy() بدل =', ['d = a.copy()'],
        '<code>c = a</code> مابتعملش نسخة: الاسمين بيشاوروا على نفس البيانات.',
        'imp', 'في البرنامج 1 نفسه: لما غيّرنا <code>c[0]</code> اتغيرت <code>a</code> كمان. ومع <code>copy()</code> فضلت زي ما هي.',
        term('after c = a and c[0] = 100: a = [100   2   3]\nafter d = a.copy() and d[0] = 100: a = [1 2 3] d = [100   2   3]'), True))
    S.append(step(3, 'np.dot لازم نفس الطول', ['d = np.dot(a, b)'],
        'الضرب النقطي بيضرب الأماكن المتقابلة، فلازم المتجهين نفس العدد.',
        'req', 'جربنا متجه 3 مع متجه 2: خطأ.', term(pyerr('n_dot_mismatch')), True))
    S.append(step(4, 'np.cross لـ 3D', ['c = np.cross(a, b)'],
        'الضرب الاتجاهي موجود في 3D بس (زي ما Khan قال امبارح).',
        'req', 'جربنا متجهين 2D: NumPy 2 رفضت.', term(pyerr('n_cross2d')), True))
    return ''.join(S)


def build_vector():
    S = []
    S.append(step(1, 'pop_back بعد اللوب', ['list.pop_back();'],
        'الـ Q بيتضاف قبل ما الشرط يتشاف، فلازم نشيله.',
        'req', 'شيلناه: البرنامج قال 4 أسماء، وطبع Q كأنها اسم.', term(out('v_no_pop')), True))
    S.append(step(2, 'القيمة الأولى "x"', ['string name = "x";'],
        'أي حاجة غير "Q"، عشان اللوب يدخل أول مرة.',
        'req', 'خلّيناها "Q": اللوب مادخلش خالص، فالقايمة فضلت فاضية، و <code>pop_back</code> على قايمة فاضية وقّعت البرنامج (exit = ‎-11 يعني Segmentation fault). ماطبعش حتى عدد الأسماء.',
        term(out('v_start_q') + f'\n(exit = {code("v_start_q")})'), True))
    S.append(step(3, '(int) قبل size()', ['for (int i = 0; i < (int)list.size(); i++)'],
        '<code>size()</code> نوعها موجب بس، و <code>i</code> نوعه <code>int</code>.',
        'opt', 'شيلناها زي الفيديو: اشتغل عادي، بس الـ compiler حذّر.', term(err('v_no_cast', ('warning',))), True))
    return ''.join(S)


def build_delete():
    S = []
    S.append(step(1, 'نتخطى الخط الفاضي', ['if (polylines.back().count == 0)', 'polylines.pop_back();'],
        'بعد الدوس يمين بيبقى فيه خط جديد فاضي في الآخر. لو مسحنا آخر خط على طول هنمسح الفاضي ده.',
        'imp', 'شيلنا الـ <code>if</code> كلها: أول Backspace مسح «خط من 0 نقط» ومفيش حاجة اتغيرت على الشاشة. لازم تدوس مرتين.',
        term('\n'.join(out('d_no_empty_check').splitlines()[8:10])) + img('d_no_empty_check_10', 'بعد Backspace: الخطين لسه موجودين'), True))
    S.append(step(2, 'count × 2 في اللوب', ['for (int i = 0; i < last.count * 2; i++)'],
        'كل نقطة رقمين (x و y) في <code>points</code>.',
        'req', 'خلّيناها <code>last.count</code> بس: اتمسح نص الأرقام. الخط الجديد بدأ في نص بيانات قديمة، فطلعت خطوط ونقط في أماكن غلط.',
        img('d_half_points_12', 'بعد Backspace ونقطتين جداد: خط غلط'), True))
    S.append(step(3, 'خط جديد فاضي بعد المسح', ['polylines.push_back({ (int)points.size() / 2, 0 });'],
        'عشان الدوسة الجاية تبدأ خط جديد لوحدها.',
        'req', 'شيلناه: النقط الجديدة اتضافت على الخط الأول (بقى فيه 5 و 6 نقط) واتوصلت بيه.',
        term('\n'.join(out('d_no_new_line').splitlines()[9:12])) + img('d_no_new_line_12', 'النقط الجديدة اتوصلت بالخط الأول'), True))
    S.append(step(4, 'UploadPoints() بعد المسح', ['UploadPoints();'],
        'عشان الكارت يبقى عنده نفس النقط اللي في الرام.',
        'opt', 'شيلناه: الشاشة طلعت <b>زي ما هي بالظبط</b>. الكارت لسه شايل النقط القديمة، بس إحنا مش بنقوله يرسمها (العدد اتغيّر). وأول دوسة بعدها بتبعت كله من جديد. يعني هنا مش لازم، بس هو اللي بيخلّي الرام والكارت شبه بعض.',
        two('c2_10', 'البرنامج الأصلي', 'd_no_upload_10', 'من غير UploadPoints'), True))
    return ''.join(S)
