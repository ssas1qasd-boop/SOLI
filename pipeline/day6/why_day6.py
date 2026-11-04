import sys, re
sys.path.insert(0, '/home/claude/day1')
from why import step, term, img

X = '/home/claude/day6/exp/'
def rd(p): return open(p).read()
def out(n): return rd(X + n + '.out').split('\nexit=')[0].rstrip('\n')
def code(n): return rd(X + n + '.out').rsplit('exit=', 1)[1].strip()
def pyerr(n): return rd(X + n + '.out').split('\nexit=')[0].strip().splitlines()[-1]
def two(a, ca, b, cb): return f'<div class="exrow">{img(a, ca)}{img(b, cb)}</div>'
def three(a, ca, b, cb, c, cc): return f'<div class="exrow">{img(a, ca)}{img(b, cb)}{img(c, cc)}</div>'
def part(n, a, b):
    L = out(n).splitlines(); return '\n'.join(L[a:b])


def build_compiler():
    S = []
    S.append(step(1, 'الجمع بينده الضرب (مش العكس)', ['Node* left = Multiplication();', 'while (Match(TokenType::Plus))'],
        'ده اللي بيخلّي <code>2 * 3</code> يتحسب الأول: الضرب بيتقفل في فرع لوحده تحت الـ <code>+</code>.',
        'req', 'بدّلنا المستويين (الضرب بينده الجمع): الشجرة اتقلبت، و 1 + 2 * 3 طلعت 9 بدل 7، والنتيجة 18 بدل 14. البرنامج اشتغل عادي ومن غير أي رسالة.',
        term(part('k_swap_levels', 2, 8)) + term(out('k_swap_levels').splitlines()[-1]), True))
    S.append(step(2, 'i++ في آخر لوب الـ Scanner', ['i++;'],
        'بعد ما نتعامل مع علامة زي <code>=</code> لازم نمشي للحرف اللي بعدها.',
        'req', 'شيلناها: الـ Scanner فضل واقف عند <code>=</code> ويلف عليها للأبد. البرنامج علّق، فقفلناه بعد 5 ثواني.',
        term(out('k_no_skip')), True))
    S.append(step(3, 'Token النهاية', ['tokens.push_back({ TokenType::End, "end" });'],
        'الـ Parser بيلف لحد ما يلاقي <code>End</code>. من غيره مش هيعرف إن الكود خلص.',
        'req', 'شيلناه: الـ Parser كمّل يقرا بعد آخر Token في ذاكرة مش بتاعته، والبرنامج وقع (exit = ‎-6).',
        term(out('k_no_end')), True))
    S.append(step(4, 'VariableIndex بتدوّر قبل ما تضيف', ['for (size_t i = 0; i < variables.size(); i++)', 'if (variables[i] == name)', 'return (int)i;'],
        'نفس الاسم لازم ياخد نفس الرقم في كل مرة، عشان <code>LOAD_VAR</code> يقرا الخانة اللي <code>STORE_VAR</code> كتب فيها.',
        'req', 'شيلنا الدوران: <code>x</code> اتخزن في الخانة 0 واتقرا من الخانة 1 (فاضية)، فالنتيجة طلعت 0 بدل 14.',
        term('\n'.join(L for L in out('k_no_lookup').splitlines() if 'VAR' in L or 'result' in L)), True))
    return ''.join(S)


def build_exercism():
    S = []
    S.append(step(1, 'شرط الـ 100 والـ 400', ['(year % 100 != 0 || year % 400 == 0)'],
        'السنة الكبيسة مش «كل 4 سنين» وخلاص: سنين القرن (1900، 2100) مش كبيسة إلا لو بتقبل على 400 (2000).',
        'req', 'خلّيناها <code>year % 4 == 0</code> بس: 2100 و 1900 طلعوا غلط. ومن غير جزء الـ 400: سنة 2000 طلعت غلط.',
        term(out('l_only4')) + term(out('l_no_400')), True))
    S.append(step(2, 'if لوحدها مش else if', ['if (drops % 5 == 0)', 'if (drops % 7 == 0)'],
        'الرقم ممكن يقبل على 3 و 5 و 7 مع بعض، فلازم نسأل الـ 3 أسئلة كلهم.',
        'req', 'خلّيناهم <code>else if</code>: 15 طلعت Pling بس، و 105 كمان.', term(out('d_else_if')), True))
    S.append(step(3, 'لو مفيش صوت: الرقم نفسه', ['if (sound.empty())', 'sound = std::to_string(drops);'],
        'التمرين بيقول: لو مش بيقبل على ولا واحد، رجّع الرقم كنص.',
        'req', 'شيلناهم: 1 و 34 رجعوا نص فاضي.', term(out('d_no_empty')), True))
    S.append(step(4, 'دالة check', ['void check(int year, bool expected)'],
        'دي فكرة exercism كلها: الاختبارات بتقولك PASS أو FAIL على طول. لما غيّرنا الكود في الخطوات اللي فوق، الـ FAIL ظهر في ثانية.',
        'imp', 'من غيرها هتقعد تقرا كل نتيجة بعينك وتقارن، وممكن غلطة تعدّي.', '', False))
    return ''.join(S)


def build_uniform():
    S = []
    S.append(step(1, 'glUseProgram قبل الـ uniform', ['glUseProgram(shader);'],
        '<code>glUniform4f</code> بيكتب في الـ Program <b>الشغال</b>. ومن غير Program شغال مفيش رسم أصلاً.',
        'req', 'شيلناه: الشاشة سودا، والأرقام في الـ Terminal بتتغير عادي. الـ CPU شغال والكارت مش بيرسم.',
        img('u_no_use_1', 'من غير glUseProgram: أسود'), True))
    S.append(step(2, 'الاسم لازم يطابق بالحرف', ['glGetUniformLocation(shader, "u_Color")'],
        'الاسم بيتدوّر عليه جوه الـ Shader حرف حرف، والكبير غير الصغير.',
        'req', 'كتبنا <code>"u_color"</code> (c صغيرة): رجع ‎-1، وفحصنا طبع التحذير، والمربع طلع أسود لأن الـ uniform فضل صفر.',
        term(out('u_wrong_name').splitlines()[0]) + img('u_wrong_name_1', 'u_color غلط: أسود'), True))
    S.append(step(3, 'الـ uniform لازم يتستخدم في الـ Shader', ['"    color = u_Color;\\n"'],
        'الكارت وقت الترجمة بيشيل أي uniform مش مستخدم، زي ما The Cherno حذّر.',
        'imp', 'خلّينا اللون ثابت في الـ Shader والـ uniform متعرّف بس: رجع ‎-1 مع إن الاسم صح، والمربع ثابت ومش بيتحرك.',
        term(out('u_unused').splitlines()[0]) + img('u_unused_1', 'uniform مش مستخدم: لون ثابت'), True))
    S.append(step(4, 'عكس الاتجاه عند 0 و 1', ['if (r > 1.0f)', 'increment = -0.05f;'],
        'الألوان من 0 لـ 1. من غير العكس الرقم بيكبر للأبد.',
        'req', 'شيلنا الـ if: <code>r</code> وصل 8.5، والكارت بيقص أي حاجة فوق 1، فالمربع وقف على لون واحد بعد ثلث ثانية.',
        term('\n'.join(out('u_no_flip').splitlines()[:6])) + two('u_no_flip_1', 'بعد ثانية تقريباً', 'u_no_flip_3', 'بعدها بشوية: نفس اللون'), True))
    return ''.join(S)


def build_time():
    S = []
    S.append(step(1, 'glfwGetTime كل فريم', ['float time = (float)glfwGetTime();'],
        'الوقت هو اللي بيحرّك الألوان. كل فريم وقت جديد = لون جديد.',
        'req', 'خلّيناه <code>0.0f</code>: الصورة ثابتة خالص.', term('\n'.join(out('t_fixed').splitlines()[:3])) + two('t_fixed_1', 'لقطة', 't_fixed_3', 'بعدها: نفس الصورة'), True))
    S.append(step(2, 'glUniform1f مش glUniform4f', ['glUniform1f(timeLocation, time);'],
        'الـ uniform في الـ Shader <code>float</code>، فلازم <code>1f</code>.',
        'req', 'كتبنا <code>glUniform4f</code>: الوقت في الـ Terminal بيزيد عادي، بس الكارت رفض الأمر من غير ما يقول، والصورة فضلت ثابتة على الوقت 0.',
        term('\n'.join(out('t_wrong_type').splitlines()[:3])) + two('t_wrong_type_1', 'لقطة', 't_wrong_type_3', 'بعدها: نفس الصورة'), True))
    S.append(step(3, 'glGetUniformLocation مرة واحدة قبل اللوب', ['int timeLocation = glGetUniformLocation(shader, "u_Time");'],
        'الدوران على الاسم بطيء نسبياً، والرقم مش بيتغير. The Cherno قال احفظه في متغير (Caching).',
        'opt', 'لو حطيناه جوه اللوب هيشتغل نفس الشكل، بس هيدوّر على الاسم 60 مرة في الثانية على الفاضي.', '', False))
    return ''.join(S)


def build_math():
    S = []
    S.append(step(1, 'المتجهين نفس الطول', ['for i in range(len(a)):'],
        'الضرب النقطي بيضرب الأماكن المتقابلة، فلازم كل عنصر يلاقي اللي قصاده.',
        'req', 'جربنا [2, 5] مع [7, 1, 3]: دالتنا طلعت 19 من غير ما تشتكي (اتجاهلت الـ 3). ولما عكسنا الترتيب وقعت. NumPy رفضت على طول.',
        term('\n'.join(out('m_len_mismatch').splitlines()[1:2]) + '\n' + pyerr('m_len_mismatch')) + term(pyerr('m_star')), True))
    S.append(step(2, 'الجذر في length', ['return math.sqrt(dot(a, a))'],
        'a · a = مربع الطول، مش الطول.',
        'req', 'شيلنا <code>sqrt</code>: الطول طلع 29 بدل 5.39، و 50 بدل 7.07.', term('\n'.join(L for L in out('m_no_sqrt').splitlines() if 'length' in L or '|[2, 5]|' in L)), True))
    S.append(step(3, 'np.dot مش a * b', ['np.dot(a, b)'],
        'في NumPy <code>*</code> بتضرب عنصر في عنصر وبس، والضرب النقطي = الضرب ده + الجمع.',
        'imp', '<code>a * b</code> طلعت [14 5] (متجه)، ومجموعها 19 = <code>np.dot</code>.', term(out('m_star').splitlines()[0]), True))
    return ''.join(S)


def build_refactor():
    S = []
    S.append(step(1, 'نفس الرسايل بالحرف', ['std::cout << "left click: polyline " << FinishedLineCount() << " has " << polylines.back().count << " points" << std::endl;'],
        'Refactoring = من برا مفيش حاجة تتغير. عشان نتأكد، شغّلنا البرنامجين بنفس الدوسات (17 دوسة بالماوس والكيبورد) وقارنا.',
        'req', 'النتيجة: الـ Terminal نفس الكلام بالحرف، والـ 17 صورة نفس البكسلات بالظبط (قارناهم بالكمبيوتر بكسل بكسل).', '', True))
    S.append(step(2, 'غلطة Refactoring: الصورة بتكشفها', ['points.resize(points.size() - last.count * 2);'],
        'وإحنا بنحوّل اللوب لـ <code>resize</code> سهل ننسى الـ <code>* 2</code>.',
        'req', 'نسيناها: الـ Terminal نفس الكلام بالحرف (يعني لو قارنت الكلام بس هتقول تمام)، بس الصور من الدوسة 10 اختلفت: نص النقط القديمة فضلت.',
        two('c1_14', 'الصح (بعد Backspace مرتين)', 'f_half_14', 'الغلط: نقط قديمة فضلت'), True))
    S.append(step(3, 'غلطة Refactoring: الكلام بيكشفها', ['StartNewLine();', 'std::cout << "backspace: deleted a line of " << last.count << " points, "'],
        'الترتيب جزء من «السلوك»: الرسالة بتعد الخطوط بعد ما نبدأ الخط الجديد.',
        'req', 'نقلنا <code>StartNewLine()</code> بعد الطباعة: الرسم زي ما هو، بس الرسالة بقت «0 lines left» بدل «1»، وفي الآخر «‎-1».',
        term('\n'.join(L for L in out('f_order').splitlines() if 'backspace' in L)), True))
    return ''.join(S)
