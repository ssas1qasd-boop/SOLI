import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

NEW_WORDS = [
 W('void* operator new(size_t size)', [('void*', 'بترجّع عنوان من غير نوع'), ('operator new', 'اسم الدالة اللي ورا كلمة new'), ('size_t size', 'عدد البايتات اللي اتطلبت')],
   'The Cherno: <code>new</code> Operator، وتقدر تعمل له Overload زي أي Operator. لما كتبناها، كل <code>new</code> في البرنامج عدّى من عندنا، فعرفنا الحجم بالظبط: 4 و 200 و 32 و 104.'),
 W('Entity* e = new Entity();', [('new', '1. احجز sizeof(Entity) = 32 بايت'), ('Entity()', '2. نادي الـ Constructor على البايتات دي'), ('Entity* e', 'شيل العنوان')],
   'ده الفرق الوحيد بين <code>new</code> و <code>malloc</code>: الـ Constructor. سطر «Entity() ran» ظهر قبل الطباعة على طول.'),
 W('Entity* m = (Entity*)malloc(sizeof(Entity));', [('malloc(…)', 'احجز بايتات بس'), ('sizeof(Entity)', '32'), ('(Entity*)', 'حوّل void* لـ Entity* (في C++ لازم تكتبه)')],
   'The Cherno: الفرق إن <code>new</code> بتنادي الـ Constructor. هنا مفيش «Entity() ran»، و name ماتعملش. جربنا نطبعه تحت: طلع فاضي بدل Unknown، وده بالصدفة (Undefined Behavior).'),
 W('Vector3* v = new (b) Vector3(1.0f, 2.0f, 3.0f);', [('new (b)', 'Placement new: مفيش حجز، استخدم العنوان b'), ('Vector3(1, 2, 3)', 'نادي الـ Constructor هناك')],
   'The Cherno ذكره في آخر الفيديو: Placement new = إنت اللي بتقرر الذاكرة جاية منين. مفيد لما تكون حاجز حتة كبيرة مرة واحدة وعايز توزّع منها بنفسك.'),
 W('v->~Vector3();', [('v->', 'على الـ object اللي عند v'), ('~Vector3()', 'نادي الـ Destructor بإيدك')],
   'المرة الوحيدة اللي بننادي فيها Destructor بإيدنا. لو كتبنا <code>delete v;</code> بعدها: Destructor تاني و free لذاكرة مش بتاعته (جربناه: double free).'),
]

NEW_TABLE = '''<table class="types"><tr><th></th><th><code>new</code></th><th><code>malloc</code></th><th>Placement new</th></tr>
<tr><td>بيحجز؟</td><td>أيوه (بينادي malloc)</td><td>أيوه</td><td>لأ: بتديله العنوان</td></tr>
<tr><td>بينادي الـ Constructor؟</td><td>أيوه</td><td>لأ</td><td>أيوه</td></tr>
<tr><td>بيرجّع إيه</td><td><code>Entity*</code></td><td><code>void*</code> (لازم تحوّل)</td><td><code>Vector3*</code></td></tr>
<tr><td>بنرجّعه إزاي</td><td><code>delete</code> / <code>delete[]</code></td><td><code>free</code></td><td><code>v->~Vector3()</code> بس</td></tr>
<tr><td>من التشغيل</td><td>new Entity[3] = 104 بايت (96 + 8 للعدد)</td><td>مفيش «Entity() ran»</td><td>نفس عنوان b</td></tr></table>'''

MIP_WORDS = [
 W('1.0f,  6.0f, 0.0f, 6.0f,    2.0f, 12.0f,', [('1.0f, 6.0f', 'x و y قبل القسمة'), ('0.0f', 'z'), ('6.0f', 'w: الكارت بيقسم x و y عليه'), ('2.0f, 12.0f', 'u و v')],
   'لسه ماعملناش مصفوفة Perspective. فبنكتب w بإيدنا: الركن البعيد w = 6 فبيبقى (1/6، 1): ضيّق وفوق. والكارت بيقسم الـ Texture كمان على w، فالمربعات بتصغر مع البعد زي أرضية حقيقية.'),
 W('GLint minFilters[] = { GL_NEAREST, GL_LINEAR, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR_MIPMAP_LINEAR };',
   [('GL_NEAREST', 'أقرب بكسل من الأصل'), ('GL_LINEAR', '4 بكسلات من الأصل وخلط'), ('GL_LINEAR_MIPMAP_LINEAR', 'LINEAR في مستويين وخلط بينهم = Trilinear')],
   'الفيديو (0:19): الـ Min Filters كلهم. لما مربع الشاشة يغطي بكسلات كتير من الصورة، NEAREST و LINEAR بيقروا من الأصل فبيطلع Moiré (تموّج). الـ Mipmap بيقرا من نسخة أصغر متحضّرة.'),
 W('glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY, &maxAniso);', [('GL_MAX_TEXTURE_MAX_ANISOTROPY', 'أكبر قيمة الكارت بيقبلها'), ('&maxAniso', 'حط الجواب هنا')],
   'الفيديو (0:47): الـ Mipmap لوحده بيبوّظ الزوايا الحادة: بيبقى رمادي. لأن البكسل بعيد بيغطي حتة طويلة رفيعة، والـ Mipmap بيختار المستوى على قد الضلع الطويل. الـ Anisotropy بياخد لحد 16 عينة على طول الحتة. وفي الفيديو (1:20) الفرق بيبان لحد ما الصورة 1024 أو 2048.'),
 W('glTexImage2D(GL_TEXTURE_2D, level, GL_RGB, w, w, 0, GL_RGB, GL_UNSIGNED_BYTE, pixels.data());', [('level', 'رقم المستوى: 0 الأصلي'), ('w, w', 'المقاس: نص اللي قبله')],
   'glGenerateMipmap بيعمل ده لوحده (كل مستوى متوسط 4 بكسلات من اللي قبله). إحنا رفعنا كل مستوى بلون عشان نشوف الكارت بيقرا من أنهي مستوى في كل حتة.'),
]

MIP_TABLE = '''<table class="types"><tr><th>المربع</th><th>MIN_FILTER</th><th>Anisotropy</th><th>البعيد شكله إيه (من الشباك)</th></tr>
<tr><td>فوق شمال</td><td>NEAREST</td><td>1</td><td>Moiré: تموّج ونقط عشوائية</td></tr>
<tr><td>فوق يمين</td><td>LINEAR</td><td>1</td><td>نفس التموّج (4 بكسلات بس من 16 أو أكتر)</td></tr>
<tr><td>تحت شمال</td><td>LINEAR_MIPMAP_LINEAR</td><td>1</td><td>هادي، بس بيبقى رمادي بدري</td></tr>
<tr><td>تحت يمين</td><td>LINEAR_MIPMAP_LINEAR</td><td>16</td><td>المربعات واضحة لمسافة أبعد</td></tr></table>'''

NP_WORDS = [
 W('print("a.dtype =", a.dtype, " itemsize =", a.itemsize, " nbytes =", a.nbytes)', [('dtype', 'نوع الخانة'), ('itemsize', 'بايتات الخانة'), ('nbytes', 'بايتات المصفوفة كلها')],
   'الـ int الافتراضي بيختلف من جهاز لجهاز: عندنا على لينكس int64. عشان كده حطينا <code>dtype="int16"</code> صريح لما الحجم يهمنا. زي <code>sizeof</code> في C++.'),
 W('print("m[0, 1:6:2] =", m[0, 1:6:2])', [('m[0, …]', 'الصف 0'), ('1', 'ابدأ من العمود 1'), (':6', 'لحد قبل 6'), (':2', 'بخطوة 2')],
   'نفس <code>range(1, 6, 2)</code> في Python: 1 و 3 و 5.'),
 W('y = x', [('y = x', 'اسم تاني لنفس المصفوفة'), ('y = x.copy()', 'مصفوفة جديدة')],
   'Keith حذّر منها: لو ماعملتش copy هتغيّر الأصل. زي Pointer في C++: y بيشاور على نفس الذاكرة.'),
 W('print(np.matmul(ones, twos))', [('np.matmul', 'ضرب مصفوفات'), ('ones (2 × 3)', 'الداخلي 3'), ('twos (3 × 2)', 'الداخلي 3 = يتضربوا، والنتيجة 2 × 2')],
   'الشرط: عدد أعمدة الأولى = عدد صفوف التانية. لو ضربنا 2 × 3 في 2 × 3: ValueError (جربناه تحت). و <code>*</code> حاجة تانية: خانة × خانة.'),
 W('print("min per row (axis=1) =", np.min(stats, axis=1), " max per column (axis=0) =", np.max(stats, axis=0))', [('axis=0', 'على طول الأعمدة: نتيجة لكل عمود'), ('axis=1', 'على طول الصفوف: نتيجة لكل صف')],
   '[[1, 2, 3], [4, 5, 6]]: أصغر كل صف [1 4]، وأكبر كل عمود [4 5 6].'),
 W('print("data[data > 50] =", data[data > 50])', [('data > 50', 'مصفوفة True/False'), ('data[…]', 'هات اللي قصاد True بس')],
   'اسمها Boolean Masking. النتيجة صف واحد فيه القيم اللي عدّت الشرط.'),
]

NP_TABLE = '''<table class="types"><tr><th>عايز</th><th>NumPy</th><th>من التشغيل</th></tr>
<tr><td>المقاس</td><td><code>a.shape</code> و <code>a.ndim</code></td><td>(2, 3) و 2</td></tr>
<tr><td>الحجم بالبايت</td><td><code>a.itemsize</code> و <code>a.nbytes</code></td><td>8 و 24</td></tr>
<tr><td>صف / عمود</td><td><code>m[0, :]</code> و <code>m[:, 2]</code></td><td>[3 10]</td></tr>
<tr><td>ضرب مصفوفات</td><td><code>np.matmul(a, b)</code></td><td>2 × 2 كلها 6</td></tr>
<tr><td>خانة × خانة</td><td><code>a * b</code></td><td>2 × 3 كلها 1</td></tr>
<tr><td>تغيير الشكل</td><td><code>a.reshape((4, 2))</code></td><td>(2, 3) = ValueError</td></tr>
<tr><td>فلترة</td><td><code>a[a > 50]</code></td><td>[75 88 51]</td></tr></table>'''

CAD_WORDS = [
 W('return { r * std::sin(t), r * std::cos(t), h };', [('r * std::sin(t)', 'x = R sinθ'), ('r * std::cos(t)', 'y = R cosθ'), ('h', 'z = H')],
   'Dr. Patil: Parametric Representation = كل إحداثي دالة في بارامترات. الأسطوانة 3 بارامترات: R و θ و H.'),
 W('int params = (R.to > R.from) + (T.to > T.from) + (H.to > H.from);', [('R.to > R.from', 'R بيتغير؟ (true = 1)'), ('+', 'اجمع')],
   'Dr. Patil: لو ثبّت التلاتة = نقطة، ولو سبت θ = دايرة، و θ و H = سطح أسطوانة، والتلاتة = جسم. نفس المعادلة، والفرق في عدد اللي بيتغير.'),
 W('bool Inside(const std::vector<Plane>& solid, Vec3 p)', [('Plane', 'n · p ≤ d = الناحية الجوانية'), ('Inside', 'جوه كل المستويات؟')],
   'Dr. Patil: الـ Solid بس يقدر يقول النقطة جوه ولا برّه، وبالتالي الحجم والكتلة ومركز الثقل. الـ Wireframe خطوط بس، والـ Surface قشرة.'),
]

CAD_TABLE = '''<table class="types"><tr><th></th><th>Wireframe</th><th>Surface</th><th>Solid</th></tr>
<tr><td>شايل إيه</td><td>12 خط (أركان + أضلاع)</td><td>6 وشوش</td><td>6 أنصاف فراغ (أو B-Rep مقفول)</td></tr>
<tr><td>الطول (من التشغيل)</td><td>24</td><td>24</td><td>24</td></tr>
<tr><td>المساحة</td><td>؟</td><td>24</td><td>24</td></tr>
<tr><td>الحجم</td><td>؟</td><td>؟</td><td>8</td></tr>
<tr><td>نقطة جوه ولا برّه</td><td>؟</td><td>؟</td><td>(0, 0, 0) جوه، (1.5, 0, 0) برّه</td></tr>
<tr><td>مشاكله</td><td>غامض: نفس الخطوط ممكن تبقى أكتر من شكل</td><td>مايعرفش الجوه</td><td>أتقل في الحساب</td></tr></table>'''
