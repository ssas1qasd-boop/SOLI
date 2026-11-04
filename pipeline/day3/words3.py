import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

REF_WORDS = [
 W('int& ref = a;', [
   ('int&', 'نوعه: «اسم تاني لـ int»'), ('ref', 'الاسم الجديد'), ('=', 'خليه اسم تاني لـ…'), ('a', '…المتغير ده'), (';', 'نهاية الأمر')],
   'علامة <code>&amp;</code> لازقة في النوع (<code>int&amp;</code>)، فهي جزء من اسم النوع. مفيش صندوق جديد بيتعمل، ومفيش عنوان بيتنسخ.'),
 W('void IncrementReference(int& value)', [
   ('void', 'مش بترجّع حاجة'), ('IncrementReference', 'اسم الدالة'), ('int&', 'المدخل اسم تاني لـ int الأصلي'), ('value', 'اسمه جوه الدالة')],
   'لما تنادي <code>IncrementReference(a)</code>، الاسم <code>value</code> بيبقى اسم تاني لـ <code>a</code> طول ما الدالة شغالة.'),
 W('(*value)++;', [
   ('(', 'الأول…'), ('*value', 'روح للعنوان (اللي على العنوان)'), (')', '…خلّص ده'), ('++', 'وبعدين زوّد اللي هناك واحد'), (';', 'نهاية الأمر')],
   'من غير الأقواس، <code>++</code> بتشتغل الأول على العنوان نفسه (تحرّكه 4 بايت)، والنجمة بتقرا وخلاص. جربناها تحت.'),
 W('#define LOG(x) std::cout << x << std::endl', [
   ('#define', 'اعمل اختصار (قبل الترجمة)'), ('LOG', 'اسم الاختصار'), ('(x)', 'بياخد حاجة واحدة اسمها x'),
   ('std::cout << x << std::endl', 'اللي هيتكتب مكانه، و x بتتبدّل باللي بعته')],
   '<code>LOG(a)</code> بتتحول حرفياً لـ <code>std::cout &lt;&lt; a &lt;&lt; std::endl</code>. ده اسمه macro.'),
]

AMP_TABLE = '''<table class="types"><tr><th>الشكل</th><th>مكانه</th><th>اقراه</th><th>مثال</th></tr>
<tr><td><code>int&amp;</code></td><td>لازق في نوع</td><td>«اسم تاني لـ int»</td><td><code>int&amp; ref = a;</code></td></tr>
<tr><td><code>&amp;a</code></td><td>قبل اسم متغير</td><td>«عنوان a»</td><td><code>int* ptr = &amp;a;</code></td></tr>
<tr><td><code>int*</code></td><td>لازق في نوع</td><td>«عنوان لـ int»</td><td><code>int* ptr;</code></td></tr>
<tr><td><code>*ptr</code></td><td>قبل اسم متغير</td><td>«اللي على العنوان»</td><td><code>*ptr = 2;</code></td></tr></table>'''

HAM_WORDS = [
 W('int compute(const char* lhs, const char* rhs)', [
   ('int', 'بترجّع رقم'), ('compute', 'الاسم اللي Exercism طالبه'), ('const', 'وعد: مش هغيّر الحروف'),
   ('char*', 'عنوان أول حرف في نص'), ('lhs', 'left-hand side: النص الشمال'), ('rhs', 'right-hand side: النص اليمين')],
   'في C النص مش نوع لوحده: هو صف حروف ورا بعض، والدالة بتاخد عنوان أول حرف.'),
 W('size_t lhs_length = strlen(lhs);', [
   ('size_t', 'نوع للأحجام والأطوال (رقم موجب بس)'), ('lhs_length', 'اسم المتغير: «طول lhs»'), ('strlen', 'string length: عدّ الحروف'), ('(lhs)', 'النص اللي هتعده')],
   'أي نص زي <code>"AAA"</code> متخزن في C كده: <code>A A A \\0</code>. <code>strlen</code> بتعد لحد ما تقابل <code>\\0</code>، فبترجّع 3.'),
 W('if (!lhs || !rhs)', [('!lhs', 'lhs فاضي (NULL)؟'), ('||', 'أو'), ('!rhs', 'rhs فاضي؟')],
   'في C أي Pointer فاضي = صفر = false، فـ <code>!lhs</code> = «مفيش عنوان». ده من نصايح الفيديو: «ماتثقش في المدخلات».'),
 W('for (; *lhs && *rhs; lhs++, rhs++)', [
   ('for (', 'لوب'), (';', 'البداية فاضية: الـ Pointers جاهزة أصلاً'), ('*lhs', 'الحرف اللي lhs واقف عليه مش \\0'), ('&&', 'و'),
   ('*rhs', 'والحرف اللي rhs واقف عليه مش \\0'), (';', 'وبعد كل لفة…'), ('lhs++, rhs++', 'حرّك الاتنين حرف لقدام')],
   'ده حساب الـ Pointers اللي اتعلمناه امبارح (<code>p++</code>). <code>*lhs</code> لوحدها في شرط = «الحرف ده مش صفر»، لأن أي قيمة غير صفر = true.'),
 W('return (*lhs || *rhs) ? -1 : distance;', [
   ('(*lhs || *rhs)', 'لو واحد فيهم لسه ماوصلش لـ \\0'), ('?', 'يبقى…'), ('-1', '…رجّع ‎-1'), (':', 'غير كده…'), ('distance', '…رجّع العدد')],
   'علامة <code>? :</code> = if و else في سطر واحد (اسمها Ternary).'),
]

SHADER_WORDS = [
 W('enum class ShaderType', [('enum', 'قايمة أسماء ثابتة'), ('class', 'محمية: لازم تكتب ShaderType:: قبلها'), ('ShaderType', 'اسم القايمة')],
   '<code>enum class</code> مابتتحولش لرقم لوحدها، عشان كده محتاجين <code>(int)type</code> (جربنا من غيرها: خطأ).'),
 W('static ShaderProgramSource ParseShader(const std::string& filepath)', [
   ('static', 'تخص الملف ده بس'), ('ShaderProgramSource', 'بترجّع العلبة (النصين)'), ('ParseShader', 'اسمها: «قسّم الـ Shader»'),
   ('const', 'مش هتغيّره'), ('std::string&', 'Reference لنص (من غير نسخ)'), ('filepath', 'مسار الملف')],
   'هنا الـ Reference اللي اتعلمناه في محاضرة البرمجة النهارده! <code>const std::string&amp;</code> = «هات النص الأصلي من غير ما تنسخه، ومش هغيّره».'),
 W('if (line.find("#shader") != std::string::npos)', [
   ('line.find("#shader")', 'دوّر على #shader جوه السطر، ورجّع مكانها'), ('!=', 'مش بيساوي'),
   ('std::string::npos', 'رقم خاص معناه «مش لاقيها»')],
   'يعني الجملة كلها: «لو لقيت <code>#shader</code> في السطر ده».'),
 W("ss[(int)type] << line << '\\n';", [
   ('ss', 'مصفوفة النصين'), ('[(int)type]', 'الخانة رقم: VERTEX ← 0 أو FRAGMENT ← 1'), ('<<', 'اكتب فيه (زي cout)'),
   ('line', 'السطر'), ("'\\n'", 'وانزل سطر (getline بتشيله، فلازم نرجّعه)')],
   'بدل <code>if</code> للـ Vertex و <code>if</code> للـ Fragment، بنستخدم النوع نفسه كرقم خانة.'),
]

CROSS_WORDS = [
 W('return v1 * w2 - v2 * w1;', [('v1 * w2', 'الأول من v × التاني من w'), ('-', 'ناقص'), ('v2 * w1', 'التاني من v × الأول من w')],
   'ده محدد المصفوفة [v₁ w₁ ; v₂ w₂]: اضرب على القطر الرئيسي، واطرح القطر التاني.'),
]

CAD_WORDS = [
 W('float x = (float)(2.0 * px / width - 1.0);', [
   ('px / width', 'مكان الماوس كنسبة من العرض (0 لـ 1)'), ('2.0 *', 'كبّرها (0 لـ 2)'), ('- 1.0', 'وزحزحها (‎-1 لـ +1)'),
   ('(float)', 'اعتبر الناتج float')],
   'مثال: الماوس عند x = 160 من 640 ← 160 ÷ 640 = 0.25 ← × 2 = 0.5 ← − 1 = ‎-0.5.'),
 W('float y = (float)(1.0 - 2.0 * py / height);', [
   ('py / height', 'مكان الماوس كنسبة من الطول (0 فوق، 1 تحت)'), ('1.0 - 2.0 * …', 'اقلب: فوق = +1 وتحت = ‎-1')],
   'البكسل بيتعد من فوق لتحت، لكن OpenGL بيعد من تحت لفوق. عشان كده القلب.'),
 W('static void MouseButtonCallback(GLFWwindow* window, int button, int action, int mods)', [
   ('static void', 'دالة مش بترجّع حاجة'), ('MouseButtonCallback', 'اسم اخترناه'), ('GLFWwindow* window', 'الشباك اللي حصل فيه الضغط'),
   ('int button', 'أنهي زرار'), ('int action', 'داس ولا ساب'), ('int mods', 'Shift أو Ctrl كانوا مدوسين؟')],
   'الشكل ده (المدخلات وترتيبها) GLFW هي اللي فارضاه، عشان هي اللي هتنادي الدالة.'),
]
