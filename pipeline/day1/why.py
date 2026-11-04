# "Why did we write this?" for every step of the Cherno Uniforms program, with real experiment results.
import html

BADGE = {'req': ('إجباري', 'b-req'), 'imp': ('مش إجباري، بس مهم جداً', 'b-imp'), 'opt': ('اختياري', 'b-opt')}

def term(t):
    return '<div class="run"><div class="bar">● ● ●  &nbsp;Terminal — output after Run</div>' + html.escape(t) + '</div>'

def img(name, cap, w='42mm'):
    return f'<div class="exshot"><img src="img/{name}.png" style="width:{w}"><div class="cap">{cap}</div></div>'

def step(num, title, code, why, badge, removed, evidence='', tested=False):
    b, cls = BADGE[badge]
    tag = '<span class="tested">✓ جربناها فعلاً</span>' if tested else ''
    code_html = ''.join(f'<div>{html.escape(c)}</div>' for c in code)
    return (f'<div class="why"><div class="whyhead"><span class="wnum">{num}</span><span class="wtitle">{title}</span>'
            f'<span class="badge {cls}">{b}</span></div>'
            f'<div class="whycode">{code_html}</div>'
            f'<div class="whyrow"><b>ليه كتبناه؟</b> {why}</div>'
            f'<div class="whyrow rm"><b>لو شيلته؟</b> {tag} {removed}</div>{evidence}</div>')

def build(rd):
    S = []
    S.append(step(1, 'المكتبات', ['#include <glad/glad.h>', '#include <GLFW/glfw3.h>', '#include <iostream>'],
        'GLAD فيها دوال OpenGL نفسها (كل حاجة بتبدأ بـ <code>gl</code>)، و GLFW بتعمل الشباك وبتقرا الكيبورد. أما <code>iostream</code> فعشان <code>std::cout</code> بس.',
        'req', 'من غير GLAD أو GLFW الكود مش هيترجم أصلاً. والترتيب كمان إجباري: GLAD <b>قبل</b> GLFW، وإلا يحصل تعارض بين الملفين. و <code>iostream</code> لو شيلتها لازم تشيل سطور الطباعة معاها.'))
    S.append(step(2, 'كود الـ Shader محطوط كنص', ['static const char* vertexShaderSrc = R"(...)";', 'static const char* fragmentShaderSrc = R"(...)";'],
        'كارت الشاشة مش بيفهم C++. بنديله برنامج صغير مكتوب بلغة GLSL كـ <b>نص</b>، وهو اللي بيترجمه ويشغّله. The Cherno بيحطه في ملف لوحده (<code>Basic.shader</code>) ويقراه؛ إحنا حطيناه جوه الكود عشان البرنامج يبقى ملف واحد. الطريقتين صح.',
        'req', 'لازم يبقى فيه Vertex Shader و Fragment Shader، وإلا مفيش رسم. وفي OpenGL الحديث مفيش رسم «افتراضي» من غيرهم.'))
    S.append(step(3, 'سطر #version', ['#version 330 core'],
        'بيقول لكارت الشاشة إحنا كاتبين بأنهي نسخة من اللغة. كلمة <code>layout(location = 0)</code> مثلاً مش موجودة في النسخ القديمة.',
        'req', 'شيلناه: البرنامج اشتغل بس الشاشة سودا. ودالة التحقق اللي عملناها (خطوة 6) طبعت سبب المشكلة، ورقم الـ Uniform بقى ‎-1 لأن البرنامج كله باظ.',
        term(rd('exp/no_version.out')) + img('exp_no_version', 'الشباك: أسود'), True))
    S.append(step(4, 'دالة main في الـ Vertex Shader و gl_Position', ['void main()', '{', '    gl_Position = position;', '}'],
        'قاعدة في لغة GLSL: كل Shader لازم يبقى فيه دالة اسمها <code>main</code>، وهي اللي كارت الشاشة بيبدأ منها. وشغلة الـ Vertex Shader الوحيدة إنه يقول كل ركن هيتحط فين، وده عن طريق <code>gl_Position</code>.',
        'req', 'شيلنا سطر <code>gl_Position</code> بس: الترجمة نجحت (مفيش ولا رسالة خطأ)، لكن الأركان ما اتحطتش في أي مكان، فالشاشة سودا.',
        img('exp_no_gl_position', 'الشباك: أسود، ومن غير أي رسالة خطأ'), True))
    S.append(step(5, 'الـ Fragment Shader والـ Uniform', ['layout(location = 0) out vec4 color;', 'uniform vec4 u_Color;', 'void main() { color = u_Color; }'],
        'الـ Fragment Shader بيقرر لون كل بكسل. والـ Uniform هو هدف المحاضرة كلها: نقدر نغيّر اللون من الـ C++ في أي وقت، من غير ما نعدّل الـ Shader ونترجمه تاني.',
        'req', 'الـ Fragment Shader نفسه إجباري. أما الـ Uniform فتقدر تكتب اللون ثابت جوه الـ Shader (<code>color = vec4(0.2, 0.3, 0.8, 1.0);</code>)، بس ساعتها مش هتقدر تغيّره من الـ C++، يعني مفيش Animation.'))
    S.append(step(6, 'دالة CompileShader', ['static unsigned int CompileShader(unsigned int type, const char* source)', '{ glCreateShader … glShaderSource … glCompileShader … }'],
        'الترجمة نفسها إجبارية: كارت الشاشة بيشغّل الـ Shader بعد ما يترجمه بس. وعملناها <b>دالة</b> عشان عندنا Shaderين، فبدل ما نكتب نفس الخمس سطور مرتين، بنكتبهم مرة وننده عليهم مرتين.',
        'imp', 'جزء التحقق (<code>if (result == GL_FALSE)</code>) مش إجباري، بس من غيره أي غلطة في الـ Shader هتديك شاشة سودا ومش هتعرف السبب. في تجربة خطوة 3 هو اللي طبع الرسالة اللي عرّفتنا الغلطة فين.'))
    S.append(step(7, 'دالة CreateShader (الربط)', ['glCreateProgram();', 'glAttachShader(...); glAttachShader(...);', 'glLinkProgram(program);', 'glDeleteShader(vs); glDeleteShader(fs);'],
        'كارت الشاشة بيشغّل «برنامج» واحد فيه الـ Shaderين مربوطين ببعض، فلازم نحطهم الاتنين فيه ونربطهم (link). وده اللي بيضمن إن اللي طالع من الأول بيوصل للتاني.',
        'req', 'من غير الربط مفيش برنامج تشغّله. أما سطرين <code>glDeleteShader</code> فاختياريين: بيمسحوا النسخ المنفصلة بعد ما بقت جوه البرنامج، عشان الذاكرة.'))
    S.append(step(8, 'دالة main في الـ C++', ['int main()'],
        'قاعدة في C++: أي برنامج لازم يبقى فيه <code>main</code> واحدة بس، والبرنامج بيبدأ منها. دي غير اللي في الـ Shaders: دي على المعالج (CPU) وبتشتغل مرة واحدة، واللي في الـ Shaders على كارت الشاشة (GPU) وبتشتغل آلاف المرات.',
        'req', 'من غيرها الـ Linker هيقول إنه مش لاقي نقطة البداية، والبرنامج مش هيتبني.'))
    S.append(step(9, 'تشغيل GLFW وطلب OpenGL 3.3', ['glfwInit();', 'glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);', 'glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);', 'glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);'],
        'لازم نشغّل GLFW قبل ما نستخدمه. والتلات سطور التانيين بيطلبوا OpenGL نسخة 3.3 الحديثة، عشان تطابق <code>#version 330 core</code> اللي في الـ Shader.',
        'req', '<code>glfwInit</code> إجباري. سطور الـ Hint إجبارية على الماك؛ على Windows غالباً هيشتغل من غيرها، بس ساعتها مش ضامن النسخة اللي هتاخدها.'))
    S.append(step(10, 'عمل الشباك', ['GLFWwindow* window = glfwCreateWindow(640, 480, "Uniforms", nullptr, nullptr);', 'if (!window) { glfwTerminate(); return -1; }'],
        'محتاجين مكان نرسم فيه. والـ <code>if</code> بتتأكد إن الشباك اتعمل فعلاً.',
        'req', 'الشباك إجباري. والـ <code>if</code> مهمة جداً: لو الشباك ما اتعملش (مثلاً الجهاز مش بيدعم 3.3)، البرنامج هيكمل ويقع من غير ما يقولك ليه.'))
    S.append(step(11, 'ربط OpenGL بالشباك', ['glfwMakeContextCurrent(window);'],
        'OpenGL محتاج «سياق» (context) متوصل بشباك معين قبل أي أمر رسم. السطر ده بيقول: «كل أوامر الرسم الجاية تروح للشباك ده».',
        'req', 'كل أوامر <code>gl…</code> بعد كده هتفشل، لأنها مش عارفة ترسم فين.'))
    S.append(step(12, 'سرعة الفريمات', ['glfwSwapInterval(1);'],
        'بيخلّي البرنامج يرسم فريم واحد مع كل تحديث للشاشة (غالباً 60 في الثانية).',
        'opt', 'البرنامج هيرسم أسرع ما يقدر (ممكن آلاف الفريمات في الثانية)، فالـ Animation هتبقى سريعة جداً، والجهاز هيسخن على الفاضي. شفنا ده بعينينا في الكاميرا: من غير تحديد السرعة، الكاميرا طارت بعيد.', '', True))
    S.append(step(13, 'تحميل دوال OpenGL', ['if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) return -1;'],
        'دوال OpenGL موجودة جوه تعريف كارت الشاشة (driver)، مش جوه برنامجك. GLAD بيروح يجيب عناوينها (Pointers لدوال، فاكر محاضرة 1؟). ولازم يتعمل <b>بعد</b> ما الشباك والـ context يتعملوا.',
        'req', 'شيلناه: البرنامج وقع فوراً عند أول أمر <code>gl…</code> من غير ما يظهر أي شباك. كود الخروج 139 = Segmentation fault، يعني حاول ينادي دالة عنوانها فاضي (nullptr)، بالظبط زي ما اتعلمنا إن قراءة Pointer فاضي = crash.',
        term('Segmentation fault (core dumped)\nexit code: 139'), True))
    S.append(step(14, 'بيانات المربع', ['float positions[] = { -0.5f,-0.5f,  0.5f,-0.5f,  0.5f,0.5f,  -0.5f,0.5f };', 'unsigned int indices[] = { 0,1,2,  2,3,0 };'],
        'كارت الشاشة بيرسم مثلثات بس. المربع = مثلثين. بنكتب الأربع أركان مرة واحدة، وبعدين نقول بالـ <code>indices</code> كل مثلث بياخد أنهي أركان.',
        'imp', 'الأماكن إجبارية (من غيرها مفيش حاجة ترسمها). الـ <code>indices</code> اختيارية: تقدر تكتب 6 أركان وترسم بـ <code>glDrawArrays</code>، بس هتكرر ركنين. في مربع مش فارقة، لكن في موديل فيه آلاف الأركان بتوفّر ذاكرة كتير.'))
    S.append(step(15, 'الـ VAO', ['glGenVertexArrays(1, &vao);', 'glBindVertexArray(vao);'],
        'الـ VAO «دفتر» بيفتكر إعدادات البيانات: أنهي buffer وإزاي يتقرا. في OpenGL الحديث (core) لازم يبقى فيه VAO شغال وإنت بترسم.',
        'req', 'شيلنا سطر <code>glBindVertexArray</code> بس: البرنامج اشتغل من غير ولا رسالة، بس الشاشة سودا. دي من أشهر الغلطات اللي بتحيّر المبتدئين.',
        img('exp_no_vao_bind', 'الشباك: أسود'), True))
    S.append(step(16, 'الـ VBO: نقل البيانات لكارت الشاشة', ['glGenBuffers(1, &vbo);', 'glBindBuffer(GL_ARRAY_BUFFER, vbo);', 'glBufferData(GL_ARRAY_BUFFER, sizeof(positions), positions, GL_STATIC_DRAW);'],
        'المصفوفة <code>positions</code> موجودة في ذاكرة الجهاز العادية، وكارت الشاشة ليه ذاكرة لوحده. السطور دي بتنسخ الأركان لذاكرته عشان يقدر يقراها بسرعة كل فريم.',
        'req', 'كارت الشاشة مش هيلاقي أي أركان يرسمها.'))
    S.append(step(17, 'شرح شكل البيانات', ['glEnableVertexAttribArray(0);', 'glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), 0);'],
        'الـ VBO مجرد bytes ورا بعض، وكارت الشاشة مش عارف معناها. هنا بنقول: «كل ركن = رقمين float، وحطهم في الخانة 0». والخانة 0 هي نفسها <code>layout(location = 0)</code> في الـ Shader.',
        'req', 'الـ Shader هيستلم أصفار، فكل الأركان هتبقى في نفس النقطة ومش هيظهر حاجة.'))
    S.append(step(18, 'الـ IBO (ترتيب الرسم)', ['glGenBuffers(1, &ibo);', 'glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);', 'glBufferData(GL_ELEMENT_ARRAY_BUFFER, ...);'],
        'نفس فكرة الـ VBO، بس للـ <code>indices</code>: بنبعتها لكارت الشاشة.',
        'imp', 'إجباري <b>طالما</b> بنرسم بـ <code>glDrawElements</code>. لو استخدمت <code>glDrawArrays</code> (من غير indices) مش هتحتاجه.'))
    S.append(step(19, 'تشغيل الـ Shader', ['unsigned int shader = CreateShader(...);', 'glUseProgram(shader);'],
        'بنعمل البرنامج وبنقول لكارت الشاشة: «ارسم بالبرنامج ده». ولازم ده يحصل قبل <code>glUniform</code> كمان، لأن الـ Uniform بيتبعت للبرنامج الشغال.',
        'req', 'شيلنا <code>glUseProgram</code>: الشاشة سودا. لاحظ إن رقم الـ Uniform لسه طالع 0، لأن <code>glGetUniformLocation</code> بتاخد البرنامج كمدخل، بس الرسم نفسه ما حصلش.',
        img('exp_no_useprogram', 'الشباك: أسود'), True))
    S.append(step(20, 'رقم الـ Uniform', ['int location = glGetUniformLocation(shader, "u_Color");', 'std::cout << ... << location;'],
        'في OpenGL 3.3 مينفعش تبعت قيمة للخانة باسمها؛ لازم تعرف رقمها الأول. والطباعة مجرد تأكيد إن الرقم مش ‎-1.',
        'req', 'السطر الأول إجباري (من غير الرقم مش هتعرف تبعت اللون). الطباعة اختيارية. ولو الاسم غلط هيرجع ‎-1، و <code>glUniform4f</code> هتتجاهل الأمر، وهيفضل اللون صفر (أسود).'))
    S.append(step(21, 'اللوب الرئيسي', ['while (!glfwWindowShouldClose(window)) { ... }'],
        'الشاشة محتاجة تترسم من جديد كل فريم. اللوب بيفضل يرسم لحد ما المستخدم يقفل الشباك.',
        'req', 'البرنامج هيخلص على طول والشباك هيقفل قبل ما تلحق تشوفه.'))
    S.append(step(22, 'مسح الشاشة', ['glClear(GL_COLOR_BUFFER_BIT);'],
        'بيمسح الفريم اللي فات قبل ما نرسم الجديد.',
        'req', 'في برنامج المربع مش هتلاحظ فرق، لأننا بنرسم نفس الحاجة في نفس المكان. بس جربناها في الكاميرا وإحنا بنتحرك بزرار D: كل فريم قديم فضل على الشاشة، والهرم ساب «ديل» وراه.',
        '<div class="exrow">' + img('exp_cam_ok', 'مع <code>glClear</code>', '38mm') + img('exp_cam_smear', 'من غير مسح الألوان', '38mm') + '</div>', True))
    S.append(step(23, 'إرسال اللون', ['glUniform4f(location, 0.2f, 0.3f, 0.8f, 1.0f);'],
        'بيحط اللون في خانة <code>u_Color</code>. في البرنامج 1 اللون ثابت، فممكن يتكتب مرة واحدة قبل اللوب؛ حطيناه جوه اللوب عشان البرنامج 2 بيغيّره كل فريم.',
        'req', 'الخانة هتفضل بقيمتها الافتراضية: صفر في الأربع أرقام = أسود وشفاف، فالمربع مش هيبان.'))
    S.append(step(24, 'أمر الرسم', ['glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);'],
        'ده الأمر اللي بيرسم فعلاً: «ارسم مثلثات باستخدام 6 أرقام من الـ IBO». كل اللي قبله تجهيز.',
        'req', 'مفيش رسم خالص.'))
    S.append(step(25, 'عرض الفريم', ['glfwSwapBuffers(window);'],
        'OpenGL بيرسم في صفحة مخفية ورا الشاشة (back buffer)، عشان المستخدم ما يشوفش الرسمة وهي بتترسم نص نص. السطر ده بيقلب الصفحة المخفية قدام.',
        'req', 'شيلناه: كل حاجة اترسمت في الصفحة المخفية، والشاشة فضلت سودا.',
        img('exp_no_swap', 'الشباك: أسود'), True))
    S.append(step(26, 'قراءة الأحداث', ['glfwPollEvents();'],
        'بيقرا اللي المستخدم عمله: كيبورد، ماوس، تحريك الشباك، زرار القفل.',
        'req', 'الشباك هيعلّق (Not Responding) وزرار القفل مش هيشتغل، لأن <code>glfwWindowShouldClose</code> مش هتعرف إنك دوست عليه. (دي من توثيق GLFW؛ ما جربناهاش هنا لأن الشاشة الوهمية ما فيهاش زرار قفل)'))
    S.append(step(27, 'كود الـ Animation (البرنامج 2 بس)', ['float r = 0.0f; float increment = 0.05f;', 'if (r > 1.0f) increment = -0.05f; else if (r < 0.0f) increment = 0.05f;', 'r += increment;'],
        'ده التطبيق العملي للمحاضرة: إثبات إن الـ Uniform بيتغير من الـ C++ كل فريم، والـ Shader نفسه ما اتغيرش.',
        'opt', 'اللون هيفضل ثابت، والبرنامج هيشتغل عادي.'))
    S.append(step(28, 'التنضيف في الآخر', ['glDeleteProgram(shader);', 'glfwTerminate();'],
        'بنرجّع الذاكرة اللي حجزناها في كارت الشاشة، ونقفل GLFW. نفس فكرة <code>delete</code> في محاضرة الـ Pointers.',
        'imp', 'في البرنامج ده مش هتلاحظ حاجة، لأن نظام التشغيل بيرجّع كل حاجة لما البرنامج يقفل. بس في برامج كبيرة بتعمل وتمسح حاجات كتير وهي شغالة، النسيان ده بيعمل تسريب ذاكرة.'))
    return ''.join(S)

CSS = '''
.why { border:1px solid #e2e6ee; border-radius:2.5mm; margin:0 0 3.5mm; page-break-inside:avoid; background:#fff; }
.whyhead { display:flex; align-items:center; gap:2.5mm; padding:2mm 3mm; background:#f5f7fb; border-bottom:1px solid #e2e6ee; border-radius:2.5mm 2.5mm 0 0; }
.wnum { font-weight:bold; color:#fff; background:#0d9488; border-radius:50%; width:6.5mm; height:6.5mm; display:inline-flex; align-items:center; justify-content:center; font-size:9pt; flex:none; }
.wtitle { font-weight:bold; font-size:11pt; flex:1; }
.badge { font-size:8.8pt; font-weight:bold; padding:0.6mm 2.5mm; border-radius:10mm; white-space:nowrap; }
.b-req { background:#fee2e2; color:#b91c1c; }
.b-imp { background:#fef3c7; color:#92400e; }
.b-opt { background:#e5e7eb; color:#374151; }
.whycode { direction:ltr; text-align:left; background:#141a26; color:#e6e9ef; font-family:"DejaVu Sans Mono",monospace; font-size:8.3pt; padding:2mm 3mm; line-height:1.5; white-space:pre-wrap; word-break:break-word; }
.whyrow { padding:2mm 3.5mm 1mm; font-size:10pt; line-height:1.65; }
.whyrow.rm { padding-bottom:2.5mm; }
.whyrow b { color:#0f766e; }
.whyrow.rm b { color:#b91c1c; }
.tested { font-size:8.8pt; font-weight:bold; color:#15803d; background:#dcfce7; padding:0.3mm 2mm; border-radius:10mm; }
.why .run { margin:0 3.5mm 2.5mm; }
.exshot { display:inline-block; text-align:center; margin:0 3.5mm 2.5mm; vertical-align:top; }
.exshot img { border-radius:1.5mm; display:block; }
.exshot .cap { font-size:9pt; color:#5b6372; margin-top:1mm; }
.exrow { display:flex; gap:2mm; }
.legend { display:flex; flex-wrap:wrap; gap:2mm; margin:0 0 4mm; font-size:10pt; }
'''
