import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

LIFE_WORDS = [
 W('Entity b("b");', [('{', 'Scope جديد = «كتاب» جديد فوق الكومة'), ('Entity b("b");', 'b مكتوب في الكتاب ده'), ('}', 'الكتاب اتشال: b مات')],
   'The Cherno شبّه الـ Stack بكومة كتب: كل Scope كتاب فوق الكومة، ولما يخلص يتشال بكل اللي فيه. الـ Scope ممكن يكون دالة أو if أو for أو أقواس فاضية.'),
 W('Entity* h = new Entity("heap");', [('Entity* h', 'الـ Pointer: على الـ Stack، بيموت عند القوس'), ('new Entity("heap")', 'الـ Entity: على الـ Heap، مابيموتش لوحده')],
   'في التشغيل: «Created Entity heap» اتطبع، و «Destroyed Entity heap» ماتطبعش خالص لحد آخر البرنامج. الذاكرة بترجع للنظام لما البرنامج يقفل بس.'),
 W('int* array = new int[50];', [('int array[50];', 'لو على الـ Stack: بيموت مع الدالة'), ('new int[50]', 'على الـ Heap: بيعيش')],
   'The Cherno حذّر: مترجّعش عنوان حاجة على الـ Stack من دالة. جربناها: الـ compiler حذّر، والبرنامج وقع.'),
 W('class ScopedPtr', [('ScopedPtr', 'Pointer بيموت مع الـ Scope'), ('~ScopedPtr()', 'جواه delete m_Ptr')],
   'نستغل إن الـ Stack بيمسح لوحده: نحط الـ Pointer جوه object على الـ Stack، والـ Destructor بتاعه يعمل delete. ده اللي <code>std::unique_ptr</code> بيعمله (اسمه RAII: الحجز في الـ Constructor والترجيع في الـ Destructor).'),
 W('ScopedPtr e = new Entity();', [('ScopedPtr e', 'object على الـ Stack'), ('=', 'هنا = نادي ScopedPtr(Entity*)'), ('new Entity()', 'الـ Entity على الـ Heap')],
   'The Cherno كتبها بالطريقتين: <code>ScopedPtr e = new Entity();</code> أو <code>ScopedPtr e(new Entity());</code>. الاتنين بينادوا نفس الـ Constructor.'),
]

LIFE_TABLE = '''<table class="types"><tr><th></th><th>على الـ Stack</th><th>بـ new على الـ Heap</th><th>ScopedPtr / unique_ptr</th></tr>
<tr><td>بيتولد</td><td>عند السطر</td><td>عند new</td><td>عند new</td></tr>
<tr><td>بيموت</td><td>عند <code>}</code> لوحده</td><td>عند delete بس</td><td>عند <code>}</code> لوحده</td></tr>
<tr><td>من التشغيل</td><td>Destroyed b قبل الكلام اللي بعد القوس</td><td>Destroyed heap ماظهرش</td><td>Destroyed Entity قبل after the scope</td></tr>
<tr><td>ترجّعه من دالة؟</td><td>لأ (البرنامج وقع)</td><td>أيوه</td><td>unique_ptr أيوه</td></tr></table>'''

TEX_WORDS = [
 W('stbi_set_flip_vertically_on_load(flip);', [('flip = 0', 'أول صف في الذاكرة = فوق الصورة'), ('flip = 1', 'أول صف = تحت الصورة')],
   'Luke: OpenGL بيعتبر (0, 0) تحت شمال، وأغلب الصور بتتخزن من فوق. في التشغيل: من غير قلب أول بكسل أبيض (فوق شمال في letter.png)، ومع القلب أحمر (تحت شمال). والشباك: الحرف F مقلوب في الشمال وسليم في اليمين.'),
 W('stbi_image_free(data);', [('data', 'نسخة الـ CPU'), ('stbi_image_free', 'رجّعها (زي free)')],
   'Luke: بعد <code>glTexImage2D</code> الكارت معاه نسخته، فنمسح نسختنا. قرينا الصورة من الكارت بعد المسح بـ <code>glGetTexImage</code>: الـ 192 بايت لسه هناك.'),
 W('u0 = (float)col / CELLS;', [('col', 'العمود (0 لـ 3)'), ('(float)', 'حوّل لـ float'), ('/ CELLS', 'قسمة على 4: 0 و 0.25 و 0.5 و 0.75')],
   'الـ Texture Atlas = صور كتير صغيرة في صورة واحدة. كل مستطيل بياخد ربع × ربع من الإحداثيات. من غير <code>(float)</code>: 1 / 4 = 0 في الـ int، وكل المستطيلات بتاخد الخانة 0 (جربناها).'),
]

TEX_TABLE = '''<table class="types"><tr><th>خطوة Luke</th><th>في الكود</th><th>من التشغيل</th></tr>
<tr><td>1. حمّل الصورة</td><td><code>stbi_load</code> (مع القلب)</td><td>8 × 8، و 3 قنوات</td></tr>
<tr><td>2. اربطها بالأركان</td><td>(x, y, u, v) لكل ركن، و stride 4 floats</td><td>الـ Atlas: u من 0.25 لـ 0.5 = الخانة 5</td></tr>
<tr><td>3. ارسمها في الـ Shader</td><td><code>texture(tex0, texCoord)</code>، و tex0 = الخانة 0</td><td>الحرف F</td></tr>
<tr><td>انقل وامسح نسخة الـ CPU</td><td><code>glTexImage2D</code> ثم <code>stbi_image_free</code></td><td>قريناها من الكارت: 192 بايت</td></tr>
<tr><td>التنضيف</td><td><code>glDeleteTextures</code></td><td></td></tr></table>'''

MAT_WORDS = [
 W('return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])', [('[cos, sin] (العمود 1)', 'e1 = (1, 0) بعد الدوران'), ('[-sin, cos] (العمود 2)', 'e2 = (0, 1) بعد الدوران')],
   'نفس طريقة Khan: المصفوفة = [T(e1) | T(e2)]. e1 بيلف لـ (cos θ، sin θ)، و e2 بيلف لـ (‎-sin θ، cos θ).'),
 W('print(np.round(R @ S, 6))', [('S', 'بيحصل الأول (أقرب للنقطة)'), ('R @', 'بيحصل بعده')],
   'Composition (تركيب): <code>(R @ S) @ p = R @ (S @ p)</code>. اقرا من اليمين للشمال. و R @ S ≠ S @ R: النقطة (1, 1) راحت (‎-1, 2) مرة و (‎-2, 1) مرة.'),
 W('proj = (x @ u) / (u @ u) * u', [('x @ u', 'Dot Product: 2×2 + 3×1 = 7'), ('u @ u', 'الطول تربيع: 5'), ('* u', 'اضرب في الاتجاه')],
   'Khan: الإسقاط على خط = النقطة اللي على الخط وأقرب حاجة لـ x. والباقي (x - proj) عمودي على الخط.'),
]

MAT_TABLE = '''<table class="types"><tr><th>التحويل</th><th>المصفوفة</th><th>من التشغيل</th></tr>
<tr><td>دوران θ</td><td>[[cos, ‎-sin], [sin, cos]]</td><td>(1, 0) بـ 30 ← (0.866، 0.5)</td></tr>
<tr><td>تركيب</td><td>R @ S = S الأول</td><td>R @ S ≠ S @ R</td></tr>
<tr><td>العكس</td><td>rotation(‎-θ) = rotation(θ).T</td><td>(1, 1) رجعت (1, 1)</td></tr>
<tr><td>دوران حوالين x في 3D</td><td>[[1, 0, 0], [0, cos, ‎-sin], [0, sin, cos]]</td><td>(2, 1, 0) ← (2, 0, 1)</td></tr>
<tr><td>إسقاط على خط</td><td>u uᵀ ÷ (u · u)</td><td>(2, 3) ← (2.8، 1.4)، و P @ P = P</td></tr></table>'''

CSG_WORDS = [
 W('return InSphere(p) || InBox(p);', [('||', 'أو = Union'), ('&&', 'و = Intersect'), ('&& !', 'و مش = Difference')],
   'NERDfirst: بيسموها Boolean، والأدق Set Operations (عمليات مجموعات): الجسم = مجموعة نقط، والعمليات على المجموعات. ولو الجسم دالة «جوه؟»، العمليات بتبقى || و && و ! بالظبط.'),
 W('void Row(const char* name, bool (*inside)(Vec3))', [('bool (*inside)(Vec3)', 'Pointer لدالة بتاخد Vec3 وترجّع bool'), ('Row(…, Union)', 'ابعت اسم الدالة من غير أقواس')],
   'عشان نطبع كل العمليات بنفس الدالة. ده اسمه Function Pointer: هنشرحه بالتفصيل يوم ما ييجي في خطة The Cherno.'),
 W('std::vector<Interval> Regularize(const std::vector<Interval>& A)', [('Regularize', 'شيل الحتت اللي طولها صفر'), ('p.b > p.a', 'طول أكبر من صفر')],
   'Wikipedia (Solid modeling): العمليات العادية ممكن تطلّع وش أو خط لوحده من غير حجم (لما جسمين بيلمسوا بعض). الـ Regularized بتشيلهم، فالنتيجة دايماً Solid سليم.'),
]

CSG_TABLE = '''<table class="types"><tr><th>العملية</th><th>في Blender</th><th>في الكود</th><th>على x (من التشغيل)</th></tr>
<tr><td>Union</td><td>Union</td><td><code>A || B</code></td><td>من ‎-1 لـ 2</td></tr>
<tr><td>Intersect</td><td>Intersect</td><td><code>A &amp;&amp; B</code></td><td>من 0 لـ 1</td></tr>
<tr><td>Difference</td><td>Difference</td><td><code>A &amp;&amp; !B</code></td><td>‎-1 و ‎-0.5</td></tr>
<tr><td>Regularized</td><td>(لوحده)</td><td><code>Regularize</code></td><td>[2, 2] ← مفيش</td></tr></table>'''
