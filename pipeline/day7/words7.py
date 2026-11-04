import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

POINTER_WORDS = [
 W('*intPtr = 10;', [('*', 'روح للعنوان (Dereference)'), ('intPtr', 'الـ Pointer اللي فيه عنوان var'), ('= 10', 'اكتب 10 هناك')],
   'النجمة ليها معنيين حسب مكانها: في التعريف (<code>int* intPtr</code>) معناها «النوع ده Pointer»، وقدام اسم متغير (<code>*intPtr</code>) معناها «روح للعنوان».'),
 W("*(buffer + 1) = 'i';", [('buffer', 'عنوان أول بايت'), ('+ 1', 'العنوان اللي بعده بخطوة (بايت واحد لأن النوع char)'), ('*( )', 'روح للعنوان ده'), ("= 'i'", 'اكتب الحرف')],
   'لو النوع <code>int*</code> كانت <code>+ 1</code> هتنط 4 بايت مرة واحدة. عشان كده النوع مهم.'),
 W('std::cout << "buffer = " << (void*)buffer << "   text = " << buffer << std::endl;', [('(void*)buffer', 'اعتبره عنوان وبس: اطبع الرقم'), ('buffer', 'من غير تحويل: الـ cout بيعتبر char* نص ويطبع الحروف')],
   'دي حالة خاصة في <code>std::cout</code> مع <code>char*</code> بس. أي Pointer تاني بيتطبع كعنوان على طول.'),
 W('char** ptrToBuffer = &buffer;', [('char**', 'Pointer لـ (Pointer لـ char)'), ('ptrToBuffer', 'الاسم'), ('&buffer', 'عنوان المتغير buffer نفسه، مش عنوان الحروف')],
   'نجمة واحدة (<code>*ptrToBuffer</code>) = اللي جوه buffer = عنوان الحروف. نجمتين (<code>**ptrToBuffer</code>) = أول حرف.'),
 W('void MakeText(char** out, int size)', [('char** out', 'عنوان متغير من نوع char* في main'), ('int size', 'عدد البايتات')],
   'لو كانت <code>char* out</code> بس، الدالة هتاخد نسخة من العنوان، والتغيير هيضيع لما ترجع. جربناها تحت.'),
]

POINTER_TABLE = '''<table class="types"><tr><th>الكتابة</th><th>معناها</th><th>في البرنامج</th><th>النتيجة</th></tr>
<tr><td><code>&amp;var</code></td><td>عنوان var</td><td><code>void* ptr = &amp;var;</code></td><td>رقم زي <code>0x7ffe9daad634</code></td></tr>
<tr><td><code>*intPtr</code></td><td>اللي جوه العنوان</td><td><code>*intPtr = 10;</code></td><td>var بقى 10</td></tr>
<tr><td><code>int*</code> / <code>void*</code></td><td>نوع الـ Pointer</td><td><code>sizeof(int*)</code></td><td>8 بايت للكل</td></tr>
<tr><td><code>new char[8]</code></td><td>احجز على الـ Heap</td><td><code>char* buffer = new char[8];</code></td><td>عنوان أول بايت</td></tr>
<tr><td><code>delete[]</code></td><td>رجّع اللي اتحجز</td><td><code>delete[] buffer;</code></td><td>العنوان مبقاش بتاعنا</td></tr>
<tr><td><code>char**</code></td><td>عنوان Pointer</td><td><code>char** ptrToBuffer = &amp;buffer;</code></td><td>سلسلة عناوين</td></tr>
<tr><td><code>nullptr</code></td><td>Pointer مش بيشاور على حاجة</td><td><code>buffer = nullptr;</code></td><td>0</td></tr></table>'''

VAO_WORDS = [
 W('glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, 0);', [('0', 'المدخل رقم 0 في الـ Shader'), ('2', 'رقمين لكل ركن'), ('GL_FLOAT', 'نوعهم float'), ('GL_FALSE', 'من غير تحويل'), ('sizeof(float) * 2', 'الركن طوله 8 بايت (stride)'), ('0', 'المدخل بيبدأ من أول الركن (offset)')],
   'السطر ده هو اللي بيعمل الربط: بياخد <b>الصندوق المربوط دلوقتي</b> على <code>GL_ARRAY_BUFFER</code> ويسجّله مع الـ Layout ده جوه <b>الـ VAO المربوط دلوقتي</b>.'),
 W('std::cout << "no VAO bound: glGetError() = " << glGetError() << std::endl;', [('glGetError()', 'هات آخر غلطة واحفظ صفر مكانها'), ('0', 'مفيش غلطة'), ('1282', 'GL_INVALID_OPERATION: أمر في وقت غلط')],
   'الكارت مش بيوقف البرنامج لما يرفض أمر: بيسجل رقم الغلطة بس. لو ماسألتش بـ <code>glGetError</code> مش هتعرف.'),
 W('glBindVertexArray(vao);', [('glBindVertexArray', 'خلّي الـ VAO ده هو الشغال'), ('vao', 'رقمه')],
   'في اللوب: سطر واحد بيرجّع الصندوق والـ Layout وصندوق الترتيب مرة واحدة.'),
 W('glUseProgram(0);', [('glUseProgram', 'اختار Shader'), ('0', 'ولا واحد')],
   'نفس فكرة <code>glBindVertexArray(0)</code>: الصفر = «فك». The Cherno بيفك كل حاجة عشان يثبت إن اللوب بيربط اللي محتاجه بنفسه.'),
]

VAO_TABLE = '''<table class="types"><tr><th>الـ VAO بيفتكر</th><th>الـ VAO مش بيفتكر</th></tr>
<tr><td><code>glEnableVertexAttribArray(0)</code> (المدخلات المفعّلة)</td><td><code>glUseProgram</code> (الـ Shader)</td></tr>
<tr><td><code>glVertexAttribPointer</code> + الصندوق اللي كان مربوط وقتها</td><td><code>glUniform4f</code> (الـ uniforms جوه الـ Program)</td></tr>
<tr><td><code>glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)</code> (صندوق الترتيب)</td><td><code>glBindBuffer(GL_ARRAY_BUFFER, buffer)</code> لوحده من غير Pointer</td></tr></table>'''

METHOD_TABLE = '''<table class="types"><tr><th></th><th>الطريقة 1: VAO واحد</th><th>الطريقة 2: VAO لكل حاجة</th></tr>
<tr><td>الإعداد</td><td>VAO واحد ومدخل واحد مفعّل</td><td>VAO لكل رسمة، والـ Layout بتاعها جواه</td></tr>
<tr><td>قبل كل رسمة</td><td><code>glBindBuffer</code> + <code>glVertexAttribPointer</code> (+ الترتيب)</td><td><code>glBindVertexArray</code> بس</td></tr>
<tr><td>في برنامجنا (المربع والمثلث)</td><td>6 أوامر ربط في الفريم</td><td>2 أمر ربط في الفريم</td></tr>
<tr><td>الصورة</td><td colspan="2" style="text-align:center">نفس البكسلات بالظبط (قارناهم بالكمبيوتر)</td></tr>
<tr><td>The Cherno</td><td>زي الـ Compatibility Profile. NVIDIA كانت بتقول أسرع زمان</td><td><b>بينصح بيها</b>. ولو السرعة مهمة: قيس على جهازك</td></tr></table>'''

CROSS_WORDS = [
 W('return [a[1] * b[2] - a[2] * b[1],', [('a[1] * b[2]', 'a₂ × b₃'), ('- a[2] * b[1]', 'ناقص a₃ × b₂'), ('[ ,', 'أول عنصر في الناتج')],
   'Python بتعد من 0، فـ <code>a[0]</code> = a₁ و <code>a[1]</code> = a₂ و <code>a[2]</code> = a₃. أسهل غلطة هنا إن الرقم يتزحلق.'),
 W('n = np.cross(p1 - p0, p2 - p0)', [('p1 - p0', 'ضلع من الركن 0 للركن 1'), ('p2 - p0', 'ضلع من الركن 0 للركن 2'), ('np.cross', 'الضرب الاتجاهي'), ('n', 'Normal: عمودي على المثلث')],
   'كده بنجيب «وش» المثلث بيبص فين. الإضاءة بعدين = dot بين الـ Normal (طوله 1) واتجاه الضوء.'),
]

CROSS_TABLE = '''<table class="types"><tr><th>السؤال</th><th>الإجابة</th><th>ليه</th></tr>
<tr><td>[1, ‎-7, 1] × [5, 2, 4]</td><td>[‎-30, 1, 37]</td><td>(‎-7)(4) − (1)(2) و (1)(5) − (1)(4) و (1)(2) − (‎-7)(5)</td></tr>
<tr><td>(a × b) · a و (a × b) · b</td><td>0 و 0</td><td>الناتج عمودي على الاتنين</td></tr>
<tr><td>i × j</td><td>k = [0, 0, 1]</td><td>قاعدة الإيد اليمين</td></tr>
<tr><td>j × i</td><td>‎-k = [0, 0, ‎-1]</td><td>الترتيب بيفرق: الإشارة بتتعكس</td></tr>
<tr><td>a × a</td><td>[0, 0, 0]</td><td>متجهين على نفس الخط ← صفر</td></tr></table>'''

GIT_WORDS = [
 W('git commit -m "add refactored polyline tool"', [('git commit', 'اعمل نقطة حفظ من اللي في الـ Staging'), ('-m', 'وده الكلام اللي بعده الرسالة (message)'), ('"add refactored polyline tool"', 'الرسالة بين علامتين تنصيص')],
   'من غير <code>-m</code> Git بيفتح محرر نصوص تكتب فيه الرسالة.'),
 W('[master (root-commit) 84180e1] add refactored polyline tool', [('master', 'الـ branch اللي اتعمل فيه'), ('(root-commit)', 'أول Commit في المشروع'), ('84180e1', 'أول 7 حروف من الـ ID'), ('add refactored', 'الرسالة')]),
 W(' 1 file changed, 1 insertion(+), 1 deletion(-)', [('1 file changed', 'ملف واحد اتغير'), ('1 insertion(+)', 'سطر جديد'), ('1 deletion(-)', 'سطر اتشال')],
   'إحنا غيّرنا سطر واحد بس، و Git بيعتبره: القديم اتشال، والجديد اتضاف.'),
 W('git log --oneline', [('git log', 'تاريخ الـ Commits'), ('--oneline', 'كل Commit في سطر: ID مختصر + الرسالة')]),
]

GIT_TABLE = '''<table class="types"><tr><th>الأمر</th><th>بيعمل إيه</th><th>إمتى</th></tr>
<tr><td><code>git config --global user.name "Student"</code> و <code>user.email</code></td><td>اسمك وإيميلك على كل Commit</td><td>مرة واحدة على الجهاز</td></tr>
<tr><td><code>git init</code></td><td>اعمل مستودع (فولدر <code>.git</code>) في الفولدر ده</td><td>مرة لكل مشروع</td></tr>
<tr><td><code>git status</code></td><td>إيه اللي اتغير وإيه اللي في الـ Staging</td><td>قبل أي حاجة</td></tr>
<tr><td><code>git add .</code></td><td>حط كل التغييرات في الـ Staging</td><td>قبل كل Commit</td></tr>
<tr><td><code>git commit -m "msg"</code></td><td>اعمل نقطة حفظ</td><td>بعد كل خطوة صغيرة شغالة</td></tr>
<tr><td><code>git diff</code></td><td>وريني السطور اللي اتغيرت</td><td>قبل الـ add</td></tr>
<tr><td><code>git log</code> / <code>git log --oneline</code></td><td>التاريخ كامل / مختصر</td><td>أي وقت</td></tr></table>'''

# words for lines that come from earlier days (so every "(شرحه كلمة كلمة فوق)" in today's file has a target)
import importlib, html as _h
def _pick(mod, var, line):
    sys.path.insert(0, '/home/claude/' + mod.split('/')[0])
    M = importlib.import_module(mod.split('/')[1]); sys.path.pop(0)
    return next(w for w in getattr(M, var) if f'<span class="ltr">{_h.escape(line)}</span>' in w)
REVIEW_WORDS = [
 W('std::string vertexShader =', [('std::string', 'نص C++ (بيكبر لوحده)'), ('vertexShader', 'اسمه: كود الـ Vertex Shader'), ('=', 'وقيمته السطور اللي تحت')],
   'كل سطر تحت بين علامتين تنصيص، و C++ بتلزقهم في نص واحد. النص ده مش C++، ده كود GLSL هيتبعت للكارت.'),
 _pick('day5/words5', 'SHADER_WORDS', '"layout(location = 0) in vec4 position;\\n"'),
 _pick('day6/words6', 'UNIFORM_WORDS', '"uniform vec4 u_Color;\\n"'),
 _pick('day4/words4', 'EBO_WORDS', 'unsigned int indices[6] = {'),
 _pick('day5/words5', 'SHADER_WORDS', 'char* message = new char[length];'),
]
GIT_WORDS.append(W('header = (kind + " " + str(len(data)) + "\\0").encode()', [('kind', 'blob أو tree أو commit'), ('" "', 'مسافة'), ('str(len(data))', 'الحجم بالبايت كنص'), ('"\\0"', 'بايت صفر: آخر الرأس'), ('.encode()', 'حوّل النص لبايتات')],
   'مثلاً لملف 5722 بايت الرأس = <code>blob 5722</code> وبعده بايت صفر. وبعده بايتات الملف نفسها.'))
