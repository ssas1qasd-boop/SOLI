# "Why?" sections for the C++ Pointers lecture and the Camera lecture, with real experiment results.
from why import step, term, img

def rd(p): return open(p).read()
def err(p): return rd(p).strip()
def asan(p, keep):
    """keep the program's own output plus the few sanitizer lines that matter"""
    lines = rd(p).splitlines()
    out = [l for l in lines if any(k in l for k in keep)]
    return '\n'.join(out)

def build_cpp():
    S = []
    S.append(step(1, 'سطر #include <iostream>', ['#include <iostream>'],
        'بيضم مكتبة الطباعة. هي اللي فيها <code>std::cout</code> (اطبع) و <code>std::cin</code> (اقرا) و <code>std::endl</code> (انزل سطر). من غيرها الـ compiler ما يعرفش الكلمات دي.',
        'req', 'شيلناه: الـ compiler رفض يترجم وقال إن <code>cout</code> مش موجودة في <code>std</code>.',
        term(err('expc/no_iostream.err')), True))
    S.append(step(2, 'سطر #include <cstring> و #include <cstddef>', ['#include <cstring>   // memset', '#include <cstddef>   // NULL'],
        'كل مكتبة فيها حاجات معينة: <code>cstring</code> فيها <code>memset</code>، و <code>cstddef</code> فيها <code>NULL</code>. القاعدة: ضم المكتبة اللي فيها الحاجة اللي بتستخدمها.',
        'imp', 'من غير <code>cstring</code> الترجمة فشلت. أما من غير <code>cstddef</code> فاشتغل عندنا عادي، لأن <code>iostream</code> بتضمها بالصدفة في الـ compiler ده؛ بس ده مش مضمون في كل compiler، فالأأمن تكتبها.',
        term(err('expc/no_cstring.err') + '\n\n(no #include <cstddef>):  compiled and ran: a = 0, b = 0, c = 0'), True))
    S.append(step(3, 'دالة int main()', ['int main()', '{', '    ...', '}'],
        'قاعدة في C++: البرنامج بيبدأ من دالة اسمها <code>main</code> بالظبط، ولازم تبقى واحدة بس. القوسين <code>{ }</code> بيحددوا جسمها: كل اللي بينهم هو اللي بيتنفذ بالترتيب.',
        'req', 'غيّرنا اسمها لـ <code>start</code>: الترجمة نجحت، لكن الخطوة الأخيرة (الربط، Linker) فشلت لأنها مش لاقية نقطة البداية.',
        term("undefined reference to `main'\ncollect2: error: ld returned 1 exit status"), True))
    S.append(step(4, 'سطر std::cin.get()', ['std::cin.get();'],
        'بيستنى لحد ما تدوس Enter. The Cherno بيحطه عشان في Visual Studio لما تشغّل البرنامج، الشاشة السودا ممكن تقفل أول ما البرنامج يخلص، قبل ما تلحق تقرا النتيجة.',
        'opt', 'البرنامج هيشتغل عادي. بس ممكن الشباك يقفل بسرعة على حسب طريقة التشغيل (Ctrl+F5 بيسيبه مفتوح، و F5 أحياناً لأ).'))
    S.append(step(5, 'nullptr بدل 0 أو NULL', ['void* c = nullptr;'],
        'التلاتة معناهم «مش بيشاور على حاجة». بس <code>0</code> و <code>NULL</code> في الأصل رقم صحيح، فممكن الـ compiler يلخبطهم مع رقم عادي. <code>nullptr</code> نوعه «Pointer فاضي» بس، فمفيش لخبطة.',
        'imp', 'هيشتغل نفس الشغل في أمثلتنا. الفرق بيظهر في برامج أكبر، فخلّي العادة إنك تكتب <code>nullptr</code>.'))
    S.append(step(6, 'علامة & (هات العنوان)', ['void* ptr = &var;'],
        'من غيرها مش هتعرف المتغير ساكن فين. الـ Pointer لازم يتملى بعنوان حقيقي عشان يبقى ليه فايدة.',
        'req', 'لو كتبت <code>ptr = var</code> من غير <code>&amp;</code>، الـ compiler هيرفض لأنك بتحط رقم (8) في مكان عنوان.'))
    S.append(step(7, 'Pointer بنوع (int*) بدل void*', ['int* ptr = &var;', '*ptr = 10;'],
        'عشان تقدر تروح للعنوان وتقرا أو تكتب، لازم الـ compiler يعرف هناك كام بايت. <code>int*</code> بتقوله «4 بايت».',
        'req', 'خليناه <code>void*</code> وجربنا <code>*ptr = 10</code>: الترجمة فشلت، لأن <code>void*</code> مش بيشاور على «نوع» معروف.',
        term(err('expc/void_deref.err')), True))
    S.append(step(8, 'التحويل (double*)', ['double* ptr2 = (double*)&var;'],
        'عنوان <code>int</code> مش من نفس نوع عنوان <code>double</code>. الـ C++ مش بتحوّل لوحدها؛ لازم تكتب التحويل صريح عشان تقول «أنا عارف أنا بعمل إيه».',
        'req', 'شيلنا <code>(double*)</code>: الترجمة فشلت. ⚠️ وخلي بالك: القراءة من الـ <code>double*</code> ده غلط (هيقرا 8 بايت ومتغيرنا 4 بس)؛ إحنا بنطبع العنوان بس عشان نثبت إنه هو هو.',
        term(err('expc/no_cast.err')), True))
    S.append(step(9, 'النجمة: روح للعنوان', ['*ptr = 10;'],
        'ده هدف المحاضرة: تغيّر قيمة متغير وإنت معاك عنوانه بس. هتستخدمه كتير لما دالة محتاجة تغيّر متغير مش بتاعها (زي <code>glfwGetCursorPos</code> في الكاميرا).',
        'req', 'وجربنا الغلطة الأشهر: نروح لعنوان <code>nullptr</code>. البرنامج طبع السطر الأول، ووقع عند سطر النجمة على طول.',
        term(asan('expc/null_deref.out', ['before', 'SEGV', 'WRITE memory', 'zero page'])), True))
    S.append(step(10, 'new: احجز في الـ Heap', ['char* buffer = new char[8];'],
        'بنحجز ذاكرة بنفسنا لما الحجم يتعرف وإحنا شغالين (مثلاً عدد النقط اللي المستخدم هيرسمها)، أو لما عايزين البيانات تفضل موجودة بعد ما الدالة تخلص. المتغيرات العادية بتتمسح لوحدها أول ما الدالة تخلص.',
        'imp', 'في المثال ده كان ممكن تكتب <code>char buffer[8];</code> عادي. الـ <code>new</code> هنا عشان نتعلمها؛ في الشغل الحقيقي هتستخدم <code>std::vector</code> و smart pointers (الأسبوع 5) بدلها.'))
    S.append(step(11, 'memset: تصفير', ['memset(buffer, 0, 8);'],
        'الذاكرة اللي بتحجزها بـ <code>new</code> مش مضمون تكون أصفار؛ ممكن يبقى فيها بواقي قديمة. <code>memset</code> بتملاها بالرقم اللي إنت عايزه.',
        'opt', 'ممكن تطلع أصفار بالصدفة (زي عندنا) وممكن لأ. ماتعتمدش عليها.'))
    S.append(step(12, 'التحويل (void*) و (int) في الطباعة', ['std::cout << (void*)buffer;', 'std::cout << (int)buffer[i];'],
        '<code>cout</code> بتتعامل مع <code>char*</code> على إنه <b>نص</b> مش عنوان، ومع <code>char</code> على إنه <b>حرف</b> مش رقم. التحويل بيقولها: اطبعه كعنوان، أو اطبعه كرقم.',
        'req', 'شيلنا التحويلين: مكان العنوان اتطبع فاضي (حاولت تطبعه كنص، وأول حرف صفر = نهاية النص). ومكان الأرقام اتطبعت مسافات (الحرف رقم 0 مالوش شكل).',
        term('buffer = \n                '), True))
    S.append(step(13, 'delete[]: رجّع الذاكرة', ['delete[] buffer;'],
        'كل <code>new</code> بتحجز ذاكرة لحد ما إنت ترجّعها. لو نسيت، البرنامج هيفضل ماسكها على الفاضي.',
        'imp', 'شغّلناه بأداة كشف أخطاء الذاكرة (AddressSanitizer). أول ما شيلنا <code>delete[]</code> قالت: «8 بايت ضاعوا (leak)». في برنامج صغير مش فارقة، بس في CAD بيحجز كل ما ترسم خط، الذاكرة هتخلص.',
        term(asan('expc/no_delete.out', ['LeakSanitizer', 'Direct leak', 'SUMMARY'])), True))
    S.append(step(14, 'الأقواس [] في delete', ['delete[] buffer;   // not: delete buffer;'],
        'اللي اتحجز بـ <code>new[]</code> (مصفوفة) لازم يترجع بـ <code>delete[]</code>. ومن غير القوسين، الـ C++ هتعتبره عنصر واحد.',
        'req', 'كتبنا <code>delete</code> من غير قوسين: الأداة مسكتها فوراً وقالت «new[] مع delete مش متطابقين». والنتيجة الرسمية في C++ «سلوك غير محدد»: ممكن يشتغل عادي، وممكن يوقع بعدين في حتة ملهاش علاقة.',
        term(asan('expc/delete_no_brackets.out', ['alloc-dealloc-mismatch'])), True))
    S.append(step(15, 'ماتلمسش الذاكرة بعد delete', ['delete[] buffer;', '// buffer[0]  <- forbidden now'],
        'بعد <code>delete[]</code> الـ Pointer لسه شايل العنوان، بس المكان مبقاش بتاعك. ودي غلطة شهيرة اسمها «use after free».',
        'req', 'جربنا نقرا <code>buffer[0]</code> بعد الـ delete: الأداة وقفت البرنامج وقالت «استخدام بعد الإرجاع». من غير الأداة ممكن يطبع رقم عادي، فتفتكره شغال.',
        term(asan('expc/use_after_delete.out', ['heap-use-after-free', 'READ of size'])), True))
    S.append(step(16, 'ليه Pointer لـ Pointer أصلاً؟', ['char** ptr = &buffer;'],
        'لما دالة محتاجة تغيّر Pointer نفسه أو تستلم قايمة نصوص. وإنت استخدمتها فعلاً من غير ما تاخد بالك: <code>glShaderSource(id, 1, &amp;source, nullptr)</code> في محاضرة الـ Uniforms، الـ <code>&amp;source</code> ده نوعه <code>const char**</code>.',
        'opt', 'في المثال ده مجرد توضيح. بس هتقابله في كل مكتبة مكتوبة بأسلوب C، زي OpenGL و GLFW.'))
    return ''.join(S)

def build_cam():
    S = []
    S.append(step(1, 'حماية الملف #ifndef … #endif', ['#ifndef SHADER_CLASS_H', '#define SHADER_CLASS_H', '...', '#endif'],
        'الملف <code>shaderClass.h</code> بيتضم مرتين: مرة في <code>main.cpp</code> ومرة جوه <code>Camera.h</code>. الحماية بتقول: «لو اتضم قبل كده، اتخطاه».',
        'req', 'شيلنا الحماية: الترجمة فشلت لأن كلاس <code>Shader</code> اتعرّف مرتين.',
        term(err('expcam/no_guard/build.txt').splitlines()[0].split('/')[-1] if False else 'shaderClass.h:4:7: error: redefinition of \'class Shader\''), True))
    S.append(step(2, 'ليه كلاس Shader أصلاً؟', ['class Shader { GLuint ID; Shader(...); void Activate(); void Delete(); };'],
        'نفس شغل <code>CompileShader</code> و <code>CreateShader</code> في محاضرة The Cherno، بس متجمعين في «حاجة» واحدة. بدل ما تشيل رقم البرنامج في متغير وتفتكر تنده <code>glUseProgram</code>، بتكتب <code>shaderProgram.Activate()</code>.',
        'opt', 'تقدر تكتبه دوال عادية زي The Cherno. الكلاس بيرتّب الكود، وده بيفرق لما المشروع يكبر ويبقى فيه Shaders كتير.'))
    S.append(step(3, 'مفيش تحقق من الأخطاء في الكلاس', ['glCompileShader(vertexShader);   // no error check', 'glLinkProgram(ID);              // no error check'],
        'كلاس Victor Gordan (وبالتالي نسختنا) ما فيهوش التحقق اللي عمله The Cherno. ده عيب حقيقي لازم تعرفه.',
        'imp', 'غيّرنا اسم متغير في الـ Fragment Shader بس (<code>colour</code> بدل <code>color</code>)، فالـ Shaderين بقوا مش متطابقين والربط فشل. الهرم ظهر <b>أسود</b> ومن غير ولا رسالة تقولك ليه. لو كان فيه تحقق كان قالك الغلطة فين.',
        '<div class="exrow">' + img('cx_ok', 'الطبيعي', '36mm') + img('cx_name', 'اسم مش متطابق', '36mm') + '</div>', True))
    S.append(step(4, 'GLM_ENABLE_EXPERIMENTAL', ['#define GLM_ENABLE_EXPERIMENTAL'],
        'دوال <code>rotate</code> و <code>angle</code> في ملفات <code>gtx</code>، ودي «تجريبية» في GLM. السطر ده بتقول بيه: «أنا عارف وموافق».',
        'req', 'شيلناه هنا: اشتغل، لأن GLM المتركبة عندنا قديمة (0.9.9) وبتطلّع تحذير بس. أما في GLM 1.0 وأحدث، واللي vcpkg هيركبهالك في الأسبوع 6، نفس الحالة خطأ والكود مش هيترجم. فاكتبه دايماً.', '', True))
    S.append(step(5, 'الـ 3 متجهات: Position و Orientation و Up', ['glm::vec3 Position;', 'glm::vec3 Orientation = glm::vec3(0.0f, 0.0f, -1.0f);', 'glm::vec3 Up = glm::vec3(0.0f, 1.0f, 0.0f);'],
        'دي أقل حاجة تحتاجها عشان توصف كاميرا: واقف فين، باصص فين، وراسك لفوق ولا مايلة. ومنهم بنحسب كل حاجة تانية (اليمين، مصفوفة الـ View).',
        'req', 'من غير أي واحد فيهم <code>lookAt</code> مش هتعرف تبني المصفوفة.'))
    S.append(step(6, 'Camera:: في الـ Constructor', ['Camera::width = width;', 'Camera::height = height;'],
        'المدخل اسمه <code>width</code> والمتغير اللي جوه الكلاس اسمه <code>width</code> برضه. <code>Camera::width</code> معناها «بتاع الكلاس»، فبنحط قيمة المدخل فيه.',
        'req', 'كتبنا <code>width = width;</code> من غير <code>Camera::</code>: الترجمة نجحت، بس المدخل اتحط في نفسه، ومتغيرات الكلاس فضلت فاضية. البرنامج وقع أول ما اشتغل، لأن نسبة الشاشة طلعت غلط.',
        term('Assertion `abs(aspect - epsilon) > 0\' failed.\nAborted (core dumped)'), True))
    S.append(step(7, 'مصفوفة الـ View بـ lookAt', ['view = glm::lookAt(Position, Position + Orientation, Up);'],
        'بتحوّل العالم كله بحيث الكاميرا تبقى في النص وباصة لقدام. ليه <code>Position + Orientation</code>؟ لأن <code>lookAt</code> عايزة «نقطة» تبصلها، مش اتجاه؛ فبناخد نقطة قدامك بخطوة.',
        'req', 'من غيرها هتشوف العالم من نقطة الأصل دايماً، والكيبورد والماوس مش هيأثروا.'))
    S.append(step(8, 'glm::radians في perspective', ['glm::perspective(glm::radians(FOVdeg), ...)'],
        'دالة <code>perspective</code> عايزة الزاوية بالـ radians، وإحنا بنكتبها بالدرجات (45) عشان أسهل. <code>radians</code> بتحوّل.',
        'req', 'شيلناها: الـ 45 اتقرت على إنها 45 radian (يعني حوالي 2578 درجة!). المشهد اتعرض بزاوية غلط والهرم صغر.',
        '<div class="exrow">' + img('cx_ok', 'الطبيعي', '36mm') + img('cx_no_radians', 'من غير radians', '36mm') + '</div>', True))
    S.append(step(9, 'التحويل (float) في نسبة الشاشة', ['(float)width / height'],
        'قسمة رقمين صحيحين في C++ بترمي الكسر. شاشتنا 800×800 فالنسبة 1 والحمد لله، بس لو 800×600 هتفرق.',
        'imp', 'جربناها بالأرقام: 800 / 600 من غير تحويل طلعت 1 بدل 1.333، يعني الصورة هتتمط.',
        term('width / height        = 1     (int division: fraction lost)\n(float)width / height = 1.33333'), True))
    S.append(step(10, 'ترتيب الضرب projection * view', ['glm::value_ptr(projection * view)'],
        'في ضرب المصفوفات الترتيب مهم (فاكر 3Blue1Brown؟). اللي على اليمين بيتطبق الأول: الـ view الأول (حرّك العالم حوالين الكاميرا)، وبعدين الـ projection (اعمل المنظور).',
        'req', 'عكسنا الترتيب (<code>view * projection</code>): الشاشة فضيت خالص.',
        '<div class="exrow">' + img('cx_ok', 'الترتيب الصح', '36mm') + img('cx_swap', 'معكوس', '36mm') + '</div>', True))
    S.append(step(11, 'glm::value_ptr', ['glm::value_ptr(projection * view)'],
        'OpenGL مكتوب بأسلوب C ومش يعرف يعني إيه <code>glm::mat4</code>. هو عايز <b>عنوان</b> أول رقم من الـ 16 (محاضرة 1 تاني!). <code>value_ptr</code> بتديله العنوان ده.',
        'req', 'بعتنا المصفوفة على طول: الترجمة فشلت لأن النوع مش متطابق.',
        term("error: cannot convert 'glm::mat<4, 4, float>' to 'const GLfloat*'"), True))
    S.append(step(12, 'if منفصلة لكل زرار (مش else if)', ['if (W) ...', 'if (A) ...', 'if (S) ...', 'if (D) ...'],
        'كل زرار بيتسأل عنه لوحده، فلو دايس على اتنين مع بعض الاتنين يشتغلوا.',
        'req', 'غيّرناها لـ <code>else if</code> ودوسنا W و D مع بعض: الكاميرا مشيت لقدام بس، لأن أول ما W اتحقق الباقي اتخطى.',
        '<div class="exrow">' + img('cx_ok_wd', 'if: قدام + يمين', '36mm') + img('cx_elseif_wd', 'else if: قدام بس', '36mm') + '</div>', True))
    S.append(step(13, 'normalize في الحركة يمين وشمال', ['glm::normalize(glm::cross(Orientation, Up))'],
        'الـ cross بيدّي اتجاه اليمين، بس طوله بيقل لما تبص لتحت أو لفوق. <code>normalize</code> بيخلي طوله 1 دايماً، فسرعتك يمين وشمال تفضل ثابتة.',
        'imp', 'حسبناها وإنت باصص 60° لتحت: من غير <code>normalize</code> الطول 0.5، يعني هتمشي يمين بنص السرعة.',
        term('length of cross(Orientation, Up)            = 0.5\nlength of normalize(cross(Orientation, Up)) = 1'), True))
    S.append(step(14, 'firstClick', ['if (firstClick) { glfwSetCursorPos(center); firstClick = false; }'],
        'الكاميرا بتحسب اللفة من بُعد الماوس عن نص الشاشة. أول ضغطة الماوس ممكن يبقى في أي حتة، فبنرجّعه للنص الأول.',
        'imp', 'حسبناها: لو أول ضغطة والماوس عند (700, 100)، الكاميرا هتلف 37.5° لفوق و 37.5° يمين في فريم واحد. ده «النطة» اللي في الفيديو.',
        term('jump up/down    = -37.5 deg\njump left/right = 37.5 deg   (in ONE frame)'), True))
    S.append(step(15, 'شرط الـ 5°', ['if (!(glm::angle(newOrientation, Up) <= glm::radians(5.0f) || ...))'],
        'لو بصيت لفوق بالظبط، اتجاه النظر هيبقى نفس اتجاه <code>Up</code>. ساعتها <code>cross</code> هيطلع صفر (مفيش «يمين»)، و <code>lookAt</code> هتطلّع أرقام بايظة.',
        'req', 'حسبناها: <code>lookAt</code> وإنت باصص لفوق بالظبط طلّعت <code>nan</code> (مش رقم)، يعني مفيش حاجة هتترسم.',
        term("view[0][0] = -nan   (nan = not a number -> nothing can be drawn)\ncross(Up, Up) = (0, 0, 0)  -> no 'right' direction"), True))
    S.append(step(16, 'رجّع الماوس للنص كل فريم', ['glfwSetCursorPos(window, (width / 2), (height / 2));'],
        'اللفة = بُعد الماوس عن النص. بعد ما نلف، بنرجّعه للنص عشان الفريم الجاي يقيس الحركة الجديدة بس.',
        'req', 'شيلناه، وحركنا الماوس 4 بكسل يمين مرة واحدة وسبناه: الكاميرا فضلت تلف لوحدها كل فريم، لأن الماوس فاضل «بعيد عن النص».',
        '<div class="exrow">' + img('cx_ncr1', 'بعد 0.05 ث', '30mm') + img('cx_ncr2', 'بعد 0.2 ث', '30mm') + img('cx_ncr3', 'بعد 0.35 ث', '30mm') + '</div>', True))
    S.append(step(17, 'glEnable(GL_DEPTH_TEST)', ['glEnable(GL_DEPTH_TEST);'],
        'من غيره OpenGL بيرسم الوشوش بترتيب الكود: اللي اترسم في الآخر يبقى فوق، حتى لو هو ورا.',
        'req', 'شيلناه: الوش الورّاني الأخضر (اترسم بعد الوش القدامي في الكود) ظهر فوقه.',
        '<div class="exrow">' + img('cx_ok', 'مع Depth Test', '36mm') + img('cx_no_depth', 'من غيره', '36mm') + '</div>', True))
    S.append(step(18, 'مسح العمق في glClear', ['glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);'],
        'الـ Depth Test بيقارن بـ «أقرب حاجة اترسمت قبل كده». لازم نصفّر الذاكرة دي كل فريم.',
        'req', 'شيلنا <code>glClear</code> كله: الشاشة بقت سودا خالص، لأن العمق القديم منع أي حاجة جديدة. ولما مسحنا العمق بس من غير الألوان، الهرم ساب «ديل» وإحنا ماشيين (شوف خطوة 22 في الـ Uniforms).', '', True))
    S.append(step(19, 'الـ 1.0 في vec4(aPos, 1.0)', ['gl_Position = camMatrix * vec4(aPos, 1.0);'],
        'الرقم الرابع (w) معناه «ده مكان». لما يبقى 1، المصفوفة بتحرّك النقطة. لو 0، المصفوفة بتعاملها كـ «اتجاه» ومش بتحركها.',
        'req', 'خليناه 0.0: الهرم اختفى خالص.',
        '<div class="exrow">' + img('cx_ok', 'w = 1.0', '36mm') + img('cx_w0', 'w = 0.0', '36mm') + '</div>', True))
    S.append(step(20, 'camera.Inputs و camera.Matrix جوه اللوب', ['camera.Inputs(window);', 'camera.Matrix(45.0f, 0.1f, 100.0f, shaderProgram, "camMatrix");'],
        'الكاميرا بتتغير كل فريم، فلازم نقرا الأزرار ونبني المصفوفة من جديد كل مرة. و <code>Inputs</code> قبل <code>Matrix</code> عشان المصفوفة تاخد آخر مكان.',
        'req', 'من غير <code>Inputs</code> الكاميرا متجمدة. ومن غير <code>Matrix</code> الـ Uniform هيفضل صفر والهرم مش هيظهر.'))
    S.append(step(21, 'sizeof(indices) / sizeof(int)', ['glDrawElements(GL_TRIANGLES, sizeof(indices) / sizeof(int), ...);'],
        'بيحسب عدد الأرقام في المصفوفة لوحده: الحجم الكلي ÷ حجم الرقم الواحد = 72 ÷ 4 = 18. فلو زودت مثلث، مش محتاج تعدّل الرقم بإيدك.',
        'opt', 'تقدر تكتب <code>18</code> على طول، بس هتنسى تغيّره لما تعدّل الشكل.'))
    return ''.join(S)
