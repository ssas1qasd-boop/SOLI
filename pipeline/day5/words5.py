import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

SWAP_WORDS = [
 W('void swap(int* p, int* q);', [('void', 'مش بترجّع حاجة'), ('swap', 'اسم الدالة'), ('int* p', 'عنوان لرقم صحيح'), ('int* q', 'عنوان تاني'), (';', 'من غير جسم: ده تعريف بس')],
   'السطر ده جوه <code>main</code> لأن جسم الدالة مكتوب تحت. من غيره الـ compiler مش هيعرف <code>swap</code> دي بتاخد إيه.'),
 W('swap(&x, &y);', [('swap', 'نادي الدالة'), ('&x', 'عنوان x (مش قيمته)'), ('&y', 'عنوان y')],
   'الـ <code>&amp;</code> هنا معناها «عنوان». الدالة هتستلم رقمين زي <code>0x7ffe...90</code>، مش 10 و 20.'),
 W('temp = *a;', [('temp', 'الصندوق المؤقت'), ('=', 'خليه يساوي'), ('*a', 'اللي جوه العنوان a = قيمة x')],
   'النجمة قبل اسم Pointer = «روح للعنوان ده وهات اللي جواه» (Dereference).'),
 W('*a = *b;', [('*a', 'الصندوق اللي a بيشاور عليه (x نفسه)'), ('=', 'خليه يساوي'), ('*b', 'اللي جوه y')],
   'التغيير بيحصل في <code>x</code> الحقيقي اللي في <code>main</code>، مش في نسخة.'),
]

SWAP_TABLE = '''<table class="types"><tr><th>الرمز</th><th>فين</th><th>معناه</th><th>مثال من البرنامج</th></tr>
<tr><td><code>&amp;x</code></td><td>قبل اسم متغير</td><td>عنوان x في الذاكرة</td><td><code>swap(&amp;x, &amp;y);</code></td></tr>
<tr><td><code>int* a</code></td><td>في التعريف</td><td>a = Pointer: بيشيل عنوان int</td><td><code>void swap(int* a, int* b)</code></td></tr>
<tr><td><code>*a</code></td><td>في الكود</td><td>القيمة اللي في العنوان a</td><td><code>temp = *a;</code></td></tr>
<tr><td><code>int&amp; a</code></td><td>في التعريف</td><td>Reference: اسم تاني لنفس الصندوق</td><td><code>void SwapReference(int&amp; a, int&amp; b)</code></td></tr></table>'''

SHADER_WORDS = [
 W('"layout(location = 0) in vec4 position;\\n"', [('layout(location = 0)', 'الخانة رقم 0 (نفس رقم glVertexAttribPointer)'), ('in', 'داخل للـ Shader'), ('vec4', '4 أرقام: x, y, z, w'), ('position', 'اسمه جوه الـ Shader'), ('\\n', 'سطر جديد في النص')],
   'إحنا باعتين رقمين بس لكل ركن، والكارت بيكمّل z = 0 و w = 1 لوحده.'),
 W('"layout(location = 0) out vec4 color;\\n"', [('out', 'خارج من الـ Shader'), ('vec4', 'R, G, B, A'), ('color', 'لون البكسل')],
   'الـ Fragment Shader لازم يطلّع لون. كل رقم من 0.0 لـ 1.0.'),
 W('char* message = new char[length];', [('char*', 'عنوان لحروف'), ('message', 'اسمه'), ('new char[length]', 'احجز length حرف على الـ Heap')],
   'The Cherno استخدم <code>alloca</code> بيحجز على الـ Stack، بس دي مش جزء من C++ الرسمي واسمها بيختلف على Windows، فإحنا استخدمنا <code>new</code> و <code>delete[]</code>.'),
 W('"out vec4 v_Position;\\n"', [('out', 'خارج من الـ Vertex'), ('vec4', 'نوعه'), ('v_Position', 'اسمه (v_ = varying: بيتنقل من مرحلة للتانية)')],
   'لازم يقابله في الـ Fragment سطر <code>in vec4 v_Position;</code> بنفس الاسم والنوع بالظبط.'),
 W('"    gl_Position = vec4(position.x * 1.5, position.y * 1.5, 0.0, 1.0);\\n"', [('gl_Position', 'مكان الركن النهائي (لازم يتكتب)'), ('vec4(...)', 'اعمل 4 أرقام'), ('position.x * 1.5', 'x الركن × 1.5'), ('0.0, 1.0', 'z و w')],
   'ده «تعديل الـ Shader»: غيّرنا شكل الرسمة من غير ما نلمس الأرقام اللي في الكارت.'),
 W('"    color = vec4(v_Position.x + 0.5, v_Position.y + 0.5, 0.2, 1.0);\\n"', [('v_Position.x + 0.5', 'من ‎-0.5..0.5 لـ 0..1 = أحمر'), ('v_Position.y + 0.5', 'أخضر'), ('0.2', 'أزرق ثابت'), ('1.0', 'مش شفاف')],
   'كل بكسل بياخد <code>v_Position</code> متخلطة من الـ 3 أركان، فاللون بيتدرج.'),
]

GLSL_TABLE = '''<table class="types"><tr><th></th><th>Vertex Shader</th><th>Fragment Shader</th></tr>
<tr><td>بيشتغل كام مرة؟</td><td>مرة لكل ركن (3)</td><td>مرة لكل بكسل جوه الشكل (آلاف)</td></tr>
<tr><td>لازم يكتب</td><td><code>gl_Position</code></td><td>اللون (<code>out vec4 color</code>)</td></tr>
<tr><td>يبعت للتاني</td><td><code>out vec4 v_Position;</code></td><td><code>in vec4 v_Position;</code> (نفس الاسم والنوع)</td></tr></table>'''

COLOR_TABLE = '''<table class="types"><tr><th>اللون</th><th><code>vec4(R, G, B, A)</code></th></tr>
<tr><td><span style="color:#dc2626">■</span> أحمر</td><td><code>vec4(1.0, 0.0, 0.0, 1.0)</code></td></tr>
<tr><td><span style="color:#16a34a">■</span> أخضر</td><td><code>vec4(0.0, 1.0, 0.0, 1.0)</code></td></tr>
<tr><td><span style="color:#2563eb">■</span> أزرق</td><td><code>vec4(0.0, 0.0, 1.0, 1.0)</code></td></tr>
<tr><td>□ أبيض</td><td><code>vec4(1.0, 1.0, 1.0, 1.0)</code></td></tr>
<tr><td>■ أسود</td><td><code>vec4(0.0, 0.0, 0.0, 1.0)</code></td></tr></table>'''

NUMPY_WORDS = [
 W('import numpy as np', [('import', 'هات مكتبة'), ('numpy', 'اسمها'), ('as np', 'وسمّيها np اختصاراً')],
   'لو ظهر <code>ModuleNotFoundError: No module named \'numpy\'</code> اكتب في الـ Terminal: <code>pip install numpy</code>.'),
 W('b = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])', [('np.array(...)', 'اعمل مصفوفة NumPy'), ('[[...], [...]]', 'List جواها Listين = صفين'), ('1.0', 'رقم عشري، فالنوع float64')]),
 W('print("row 0 =", b[0, :])', [('b[0, :]', 'الصف 0، وكل الأعمدة'), (':', '«كله» من الأول للآخر')]),
 W('d = np.dot(a, b)', [('np.dot', 'الضرب النقطي'), ('a, b', 'المتجهين'), ('d', 'الناتج: رقم واحد')]),
 W('c = np.cross(a, b)', [('np.cross', 'الضرب الاتجاهي'), ('a, b', 'متجهين 3D'), ('c', 'الناتج: متجه عمودي على الاتنين')]),
 W('print("3 dot products at once:", np.sum(P * Q, axis=1))', [('P * Q', 'ضرب عنصر في عنصر'), ('np.sum', 'اجمع'), ('axis=1', 'اجمع كل صف لوحده')]),
]

NUMPY_TABLE = '''<table class="types"><tr><th>عايز</th><th>بإيدك (C++ امبارح)</th><th>NumPy</th></tr>
<tr><td>ضرب نقطي</td><td><code>a.x*b.x + a.y*b.y + a.z*b.z</code></td><td><code>np.dot(a, b)</code></td></tr>
<tr><td>ضرب اتجاهي</td><td>3 سطور بالصليب</td><td><code>np.cross(a, b)</code></td></tr>
<tr><td>الطول</td><td><code>sqrt(dot(a, a))</code></td><td><code>np.linalg.norm(a)</code></td></tr>
<tr><td>الزاوية</td><td><code>acos(dot / (|a| |b|))</code></td><td><code>np.degrees(np.arccos(...))</code></td></tr>
<tr><td>100 متجه</td><td>لوب</td><td>نفس السطر، والمصفوفة فيها 100 صف</td></tr></table>'''

VECTOR_WORDS = [
 W('vector<string> list;', [('vector', 'قايمة بتكبر لوحدها'), ('<string>', 'كل عنصر نص'), ('list', 'اسمها')],
   'في الأول فاضية (<code>size() = 0</code>). من غير <code>using namespace std;</code> كانت هتتكتب <code>std::vector&lt;std::string&gt;</code>.'),
 W('while (name != "Q")', [('while', 'لف طول ما'), ('name != "Q"', 'آخر اسم مش Q')],
   'القيمة اللي بتوقّف اللوب اسمها <b>Sentinel</b> (حارس). الشرط بيتشاف في <b>أول</b> اللفة بس.'),
 W('list.push_back(name);', [('list', 'القايمة'), ('.push_back', 'ضيف في الآخر'), ('(name)', 'العنصر الجديد')]),
 W('list.pop_back();', [('list', 'القايمة'), ('.pop_back', 'امسح آخر عنصر'), ('()', 'مش بتاخد حاجة')],
   'خلي بالك: <code>pop_back</code> على قايمة فاضية = كارثة (جربناها تحت).'),
 W('static void KeyCallback(GLFWwindow* window, int key, int scancode, int action, int mods)', [
   ('KeyCallback', 'اسم اخترناه'), ('window', 'الشباك'), ('key', 'أنهي زرار (GLFW_KEY_...)'), ('scancode', 'رقم الزرار عند الجهاز (مش محتاجينه)'),
   ('action', 'اتداس / اتساب / متساب مداسة'), ('mods', 'Shift أو Ctrl معاه؟')],
   'الشكل ده لازم يبقى كده بالظبط عشان GLFW تقبلها، حتى لو مش هنستخدم كل المدخلات.'),
 W('Polyline last = polylines.back();', [('Polyline', 'نوعه: بداية وعدد'), ('last', 'نسخة'), ('polylines.back()', 'آخر عنصر في القايمة (من غير ما يتمسح)')]),
]

VECTOR_TABLE = '''<table class="types"><tr><th>الدالة</th><th>بتعمل إيه</th><th>الحجم</th></tr>
<tr><td><code>push_back(x)</code></td><td>تضيف x في <b>الآخر</b></td><td>+1</td></tr>
<tr><td><code>pop_back()</code></td><td>تمسح <b>آخر</b> عنصر</td><td>‎-1</td></tr>
<tr><td><code>back()</code></td><td>ترجّع آخر عنصر من غير ما تمسحه</td><td>نفسه</td></tr>
<tr><td><code>size()</code></td><td>عدد العناصر دلوقتي</td><td>نفسه</td></tr>
<tr><td><code>list[i]</code></td><td>العنصر رقم i (من صفر)</td><td>نفسه</td></tr></table>'''
