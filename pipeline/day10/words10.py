import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

CTOR_WORDS = [
 W('Entity()', [('Entity', 'نفس اسم الـ class بالظبط'), ('()', 'مش بياخد حاجة'), ('(مفيش نوع قبله)', 'ولا int ولا void: ده اللي بيقول للـ compiler إنه Constructor')],
   'The Cherno: الـ Constructor «method خاص بيشتغل كل ما نعمل object». لو ماكتبناش واحد، C++ بيعمل واحد فاضي (Default Constructor) مابيحطش أي قيم.'),
 W('Entity(float x, float y)', [('Entity', 'نفس الاسم'), ('float x, float y', 'رقمين جايين من برّه')],
   'ممكن أكتر من Constructor بنفس الاسم لو القوسين مختلفين (Overloading). <code>Entity e1;</code> بينادي اللي من غير حاجة، و <code>Entity e2(10.0f, 5.0f);</code> بينادي ده.'),
 W('this->x = x;', [('this', 'Pointer للـ object اللي الدالة شغالة عليه دلوقتي'), ('->x', 'x بتاع الـ object'), ('= x', 'x اللي جاي في القوسين')],
   'الاسمين واحد، فالأقرب (اللي في القوسين) بيغطي على بتاع الـ class. لو كتبنا <code>x = x;</code> بيحط الرقم في نفسه، والـ object يفضل «زبالة» (جربناها تحت).'),
 W('Log() = delete;', [('Log()', 'الـ Constructor الافتراضي'), ('= delete', 'امسحه: ممنوع يتنادى')],
   'طريقة The Cherno التانية (الأولى: نحطه <code>private</code>). كده <code>Log l;</code> = خطأ ترجمة، و <code>Log::Write</code> شغالة عادي.'),
]

CTOR_TABLE = '''<table class="types"><tr><th>اللي كتبناه</th><th>الـ Constructor اللي اشتغل</th><th>اللي اتطبع (من التشغيل)</th></tr>
<tr><td><code>new NoInit</code> (مفيش Constructor)</td><td>ولا حاجة</td><td>أرقام عجيبة بتتغير كل مرة</td></tr>
<tr><td><code>Entity e1;</code></td><td><code>Entity()</code></td><td>0, 0</td></tr>
<tr><td><code>Entity e2(10.0f, 5.0f);</code></td><td><code>Entity(float, float)</code></td><td>10, 5</td></tr>
<tr><td><code>new Entity(3.0f, 4.0f)</code></td><td><code>Entity(float, float)</code></td><td>3, 4</td></tr>
<tr><td><code>Log l;</code></td><td>ممسوح بـ <code>= delete</code></td><td>خطأ ترجمة</td></tr></table>'''

DTOR_WORDS = [
 W('~Entity()', [('~', 'علامة «تيلدا»: معناها Destructor'), ('Entity', 'نفس اسم الـ class'), ('()', 'دايماً فاضي: مابياخدش حاجة')],
   'The Cherno: الـ Destructor «عكس» الـ Constructor. بيشتغل لما الـ object يتمسح: على الـ Stack لما نخرج من الـ <code>{ }</code>، وعلى الـ Heap لما نكتب <code>delete</code>.'),
 W('~Buffer()', [('~Buffer', 'Destructor الـ Buffer'), ('delete[] data;', 'اللي جواه: رجّع اللي الـ Constructor حجزه')],
   'القاعدة: اللي الـ Constructor يحجزه، الـ Destructor يرجّعه. كده مستحيل ننسى <code>delete[]</code>.'),
 W('Buffer b(16);', [('Buffer', 'النوع'), ('b', 'الاسم'), ('(16)', 'الرقم اللي رايح للـ Constructor')],
   'جوه <code>{ }</code> لوحدها: أول ما نوصل للـ <code>}</code>، الـ <code>~Buffer</code> بيشتغل لوحده.'),
]

DTOR_TABLE = '''<table class="types"><tr><th>الـ object</th><th>بيتولد</th><th>بيموت (الـ Destructor)</th></tr>
<tr><td><code>Entity e;</code> جوه Function</td><td>عند السطر ده</td><td>عند الـ <code>}</code> بتاعة Function</td></tr>
<tr><td><code>new Entity()</code></td><td>عند <code>new</code></td><td>عند <code>delete heap;</code> بس</td></tr>
<tr><td><code>Buffer b(16);</code> جوه <code>{ }</code></td><td>عند السطر ده</td><td>عند الـ <code>}</code>، قبل «after the { }»</td></tr></table>'''

TEX_WORDS = [
 W('Texture(const char* path)', [('Texture', 'الـ Constructor'), ('const char* path', 'مسار الصورة (نص بأسلوب C)')],
   'زي Victor Gordan في آخر الفيديو: «عمل Texture Class». كل الخطوات العشرة بتاعة امبارح بقت جوه الـ Constructor، فعمل Texture = سطر واحد.'),
 W('GLenum format = (channels == 4) ? GL_RGBA : GL_RGB;', [('GLenum', 'نوع أرقام OpenGL الخاصة'), ('channels == 4', 'الملف فيه شفافية؟'), ('? GL_RGBA', 'لو آه'), (': GL_RGB', 'لو لأ')],
   'الصندوق 3 قنوات والوش 4. لو كتبنا RGBA للاتنين، الصندوق بيبوظ (جربناها). ده نفس غلطة امبارح بالعكس.'),
 W('~Texture()', [('~Texture', 'الـ Destructor'), ('glDeleteTextures', 'امسح من الكارت')],
   'لما الـ object يموت، الـ Texture يتمسح من الكارت لوحده. بس لازم يموت <b>قبل</b> <code>glfwTerminate</code>، وإلا البرنامج بيقع (جربناها).'),
 W('glActiveTexture(GL_TEXTURE0 + unit);', [('GL_TEXTURE0', 'الخانة 0'), ('+ unit', 'الخانات ورا بعض: + 1 = GL_TEXTURE1')],
   'Victor Gordan: «الـ Texture Units زي slots للصور». فيه 16 خانة على الأقل في نفس الوقت.'),
 W('Texture crate("res/crate.png");', [('Texture', 'النوع (الـ class)'), ('crate', 'الاسم'), ('("res/crate.png")', 'رايح للـ Constructor')],
   'وهو جوه <code>{ }</code> قبل اللوب: بيموت بعد اللوب وقبل <code>glfwTerminate</code>.'),
 W('"    FragColor = mix(texture(tex0, texCoord), face, face.a * amount);\\n"', [('mix(a, b, t)', 'a × (1 - t) + b × t'), ('texture(tex0, texCoord)', 'لون الصندوق'), ('face', 'لون الوش'), ('face.a * amount', 'الشفافية × 0.8')],
   'learnopengl بيخلط صورتين بـ <code>mix</code>. إحنا ضربنا في <code>face.a</code> عشان الأماكن الشفافة في الوش يبان فيها الصندوق كامل.'),
]

TEX_TABLE = '''<table class="types"><tr><th></th><th>امبارح (من غير class)</th><th>النهارده (Texture class)</th></tr>
<tr><td>عمل Texture</td><td>16 سطر في main</td><td><code>Texture crate("res/crate.png");</code></td></tr>
<tr><td>عدد القنوات</td><td>مكتوب بإيدنا (RGBA)</td><td>الـ class بيختار (3 ← RGB، 4 ← RGBA)</td></tr>
<tr><td>المسح</td><td><code>glDeleteTextures</code> بإيدنا</td><td>الـ Destructor لوحده</td></tr>
<tr><td>صورتين</td><td>مرتين كل الكود</td><td><code>Texture face("res/face.png");</code> + <code>face.Bind(1);</code></td></tr></table>'''

MAT_WORDS = [
 W('I2 = np.identity(2)', [('np.identity', 'دالة NumPy لمصفوفة الوحدة'), ('2', 'المقاس 2 × 2')],
   'Khan بيكتبها Iₙ: آحاد على القطر الرئيسي وأصفار في الباقي. و Iₙ × x = x لأي متجه.'),
 W('e1 = np.array([1.0, 0.0])', [('e1', 'e₁: أول متجه في القاعدة المعيارية (Standard Basis)'), ('[1.0, 0.0]', '1 في المكان الأول بس')],
   'أعمدة مصفوفة الوحدة هي e₁ و e₂. وأي متجه = x₁ e₁ + x₂ e₂.'),
 W('A = np.column_stack([T(e1), T(e2)])', [('np.column_stack', 'حط الحاجات دي أعمدة جنب بعض'), ('T(e1)', 'العمود الأول'), ('T(e2)', 'العمود التاني')],
   'الفكرة الأساسية في الفيديو: T(x) = x₁ T(e₁) + x₂ T(e₂)، فلو حطينا T(e₁) و T(e₂) أعمدة، T(x) = A x. من ℝ² لـ ℝ³ = مصفوفة 3 × 2.'),
 W('moved = (A @ F.T).T', [('F.T', 'النقط أعمدة (2 × 11)'), ('A @', 'اضرب A في كل الأعمدة مرة واحدة'), ('.T', 'رجّعها صفوف عشان الرسم')],
   'A × (11 نقطة) = 11 نقطة جديدة في سطر واحد. ده بالظبط اللي الـ Vertex Shader هيعمله لكل ركن.'),
]

MAT_TABLE = '''<table class="types"><tr><th>المتجه x</th><th>T(x) بالمعادلة</th><th>A @ x</th></tr>
<tr><td>e₁ = (1, 0)</td><td>(1, ‎-1, 4)</td><td>العمود الأول</td></tr>
<tr><td>e₂ = (0, 1)</td><td>(3, 5, 1)</td><td>العمود التاني</td></tr>
<tr><td>(1, 1)</td><td>(4, 4, 5)</td><td>(4, 4, 5)</td></tr>
<tr><td>(2, ‎-1)</td><td>(‎-1, ‎-7, 7)</td><td>(‎-1, ‎-7, 7)</td></tr></table>'''

BREP_WORDS = [
 W('struct Use', [('Use', 'استخدام ضلع جوه حلقة'), ('edge', 'رقم الضلع'), ('reversed', 'ماشيين عكسه؟')],
   'الضلع الواحد بين وشين، وكل وش بيمشي عليه في اتجاه. عشان كده الحلقة بتشيل «استخدام» مش الضلع نفسه (Glen Gray سماها PreEdge).'),
 W('Vertex Side(float u, float v)', [('Side', 'السطح الجانبي'), ('u', 'متغير أول: اللفة'), ('v', 'متغير تاني: الارتفاع')],
   'Glen Gray: الضلع منحنى C(t) بمتغير واحد، والوش سطح S(u, v) بمتغيرين. فضاء (u, v) مستطيل بيتلف ويبقى الأسطوانة.'),
 W('{ { { 0, true }, { 1, false }, { 2, false }, { 1, true } } },', [('{ 0, true }', 'الدايرة اللي فوق، عكس'), ('{ 1, false }', 'اللحام لتحت'), ('{ 2, false }', 'الدايرة اللي تحت'), ('{ 1, true }', 'اللحام لفوق')],
   'لو فردنا الجنب يبقى مستطيل: فوق وتحت الدايرتين، وشمال ويمين نفس خط اللحام. عشان كده اللحام بيتعد مرتين وكل ضلع «مستخدم مرتين».'),
 W('std::vector<std::vector<int>> loops;', [('std::vector<int>', 'حلقة = أرقام أركان'), ('std::vector<std::vector<int>>', 'قايمة حلقات')],
   'الحلقة الأولى حدود الوش برّه، وأي حلقة بعدها خرم (Trim Loop): «المنطقة دي ماتعرضهاش» من غير ما نغيّر السطح (Glen Gray).'),
 W('std::map<std::pair<int, int>, int> CountEdges(const Shape& s)', [('std::map', 'قاموس'), ('std::pair<int, int>', 'المفتاح: الركنين'), ('int', 'القيمة: العدد')],
   'نفس فكرة std::set امبارح، بس بنعد كمان: كل ضلع لازم يطلع 2.'),
 W('std::cout << "  V - E + F = " << V - E + F << ",  V - E + F - (loops - F) = " << V - E + F - (L - F) << std::endl;', [('V - E + F', 'أويلر العادي'), ('loops - F', 'عدد الخروم في الوشوش'), ('= 2(S - G)', 'S = عدد الأجسام، G = عدد الخروم اللي بتعدي الجسم')],
   'ده اسمه أويلر-بوانكاريه (Euler–Poincaré). للصندوق بالخرم: 16 - 24 + 10 - 2 = 0 = 2(1 - 1): جسم واحد وخرم واحد بيعديه.'),
]

BREP_TABLE = '''<table class="types"><tr><th>الشكل</th><th>V</th><th>E</th><th>F</th><th>الحلقات</th><th>V - E + F</th><th>كل ضلع مرتين؟</th></tr>
<tr><td>الأسطوانة</td><td>2</td><td>3</td><td>3</td><td>3</td><td>2</td><td>أيوه</td></tr>
<tr><td>صندوق بخرم</td><td>16</td><td>24</td><td>10</td><td>12</td><td>2 (والصح: 0)</td><td>أيوه</td></tr>
<tr><td>مكعبين في ضلع</td><td>14</td><td>23</td><td>12</td><td>12</td><td>3</td><td>لأ: 2-6 أربع مرات</td></tr></table>'''
