import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

TPL_WORDS = [
 W('template<typename T>', [('template', 'اللي جاي قالب مش كود'), ('<typename T>', 'بارامتر: T نوع (ممكن class بدل typename)')],
   'The Cherno: «الـ Template بيخلي الـ compiler يكتبلك كود بقواعد انت بتحددها». كل نوع بتستخدمه بيطلع له نسخة: Print(int) و Print(float) و Print(const char*)، وده باين في <code>__PRETTY_FUNCTION__</code>.'),
 W('value.ThisDoesNotExist();', [('value', 'من النوع T'), ('ThisDoesNotExist', 'دالة مش موجودة')],
   'The Cherno قال إن ده بيترجم في MSVC لو محدش نادى الدالة. g++ برضه عدّاها (مش عارف T لسه). أول ما ناديناها بـ int: error.'),
 W('template<typename T, int N>', [('typename T', 'نوع'), ('int N', 'رقم ثابت وقت الترجمة')],
   'The Cherno عمل Array كده وقال إنه تقريباً std::array. الرقم بيبقى جزء من النوع: Array&lt;int, 5&gt; و Array&lt;int, 6&gt; نوعين مختلفين. وده Metaprogramming: بنبرمج الـ compiler.'),
]

TPL_TABLE = '''<table class="types"><tr><th>النداء</th><th>T طلع إيه (من التشغيل)</th></tr>
<tr><td><code>Print(5)</code></td><td>int</td></tr>
<tr><td><code>Print(5.5f)</code></td><td>float</td></tr>
<tr><td><code>Print("Hello")</code></td><td>const char*</td></tr>
<tr><td><code>Print&lt;std::string&gt;("Hello")</code></td><td>std::string</td></tr>
<tr><td><code>Print&lt;int&gt;(7.9)</code></td><td>int (طبع 7)</td></tr>
<tr><td><code>Array&lt;int, 5&gt;</code></td><td>20 بايت، زي <code>std::array&lt;int, 5&gt;</code></td></tr></table>'''

TR_WORDS = [
 W('return { { { 1, 0, tx }, { 0, 1, ty }, { 0, 0, 1 } } };', [('1, 0 / 0, 1', 'Identity: x و y زي ما هما'), ('tx, ty', 'بتتضرب في الـ 1 وتتجمع'), ('0, 0, 1', 'الصف الأخير ثابت')],
   'Cem: «مفيش مصفوفة 2 × 2 تعمل جمع». الحل Homogeneous Coordinates: نزوّد رقم تالت = 1 للنقطة، فالتحريك يبقى ضرب زي الدوران والتكبير.'),
 W('Mat3 aroundCenter = Multiply(Translate(0.45f, 0.4f), Multiply(Rotate(90), Translate(-0.45f, -0.4f)));', [('Translate(-c)', '1. ودّي المركز للأصل'), ('Rotate(90)', '2. لف'), ('Translate(c)', '3. رجّعه')],
   'Cem: الدوران دايماً حوالين الأصل. عشان تلف حوالين نقطة تانية: تحريك، لف، تحريك عكسي. والكل مصفوفة واحدة.'),
 W('Vec3 direction = { 1, 0, 0 };', [('w = 1', 'نقطة: بتتحرك'), ('w = 0', 'اتجاه: بيلف بس')],
   'Cem: نفس المصفوفة للنقط والاتجاهات. التحريك بيتضرب في w، فلو w = 0 التحريك بيختفي.'),
 W('glUniformMatrix3fv(matLoc, 1, GL_TRUE, &shapes[i].m[0][0]);', [('glUniformMatrix3fv', 'ابعت mat3'), ('GL_TRUE', 'اقلبها (Transpose)'), ('&m[0][0]', 'عنوان أول رقم')],
   'إحنا كاتبين المصفوفة صف صف (زي الورق)، و OpenGL بيقرا عمود عمود (Column-major). جربنا GL_FALSE: الدوران اتعكس والتحريك راح.'),
]

TR_TABLE = '''<table class="types"><tr><th>التحويل</th><th>المصفوفة 3 × 3</th><th>من التشغيل</th></tr>
<tr><td>تحريك</td><td>[1 0 tx] [0 1 ty] [0 0 1]</td><td>(1, 0, w = 1) ← (3, 3)</td></tr>
<tr><td>دوران</td><td>[c ‎-s 0] [s c 0] [0 0 1]</td><td>(0.6, 0.2) ← (‎-0.2, 0.6)</td></tr>
<tr><td>تكبير</td><td>[sx 0 0] [0 sy 0] [0 0 1]</td><td>البيت الأخضر</td></tr>
<tr><td>حوالين المركز</td><td>T(c) R T(‎-c)</td><td>(0.6, 0.2) ← (0.65, 0.55)</td></tr>
<tr><td>Skew</td><td>R(45) S R(‎-45)</td><td>(1, 1) ← (2, 2)</td></tr>
<tr><td>اتجاه (w = 0)</td><td>نفس المصفوفة</td><td>(1, 0) ← (0, 1) بس</td></tr></table>'''

MAT_WORDS = [
 W('composition = shear @ rotation', [('rotation', 'بيحصل الأول (على اليمين)'), ('shear @', 'بعده'), ('composition', 'مصفوفة واحدة للاتنين')],
   '3Blue1Brown: ضرب المصفوفات = تحويل وبعده تحويل. وبنقرا من اليمين للشمال زي f(g(x)).'),
 W('first_column = M2 @ M1[:, 0]', [('M1[:, 0]', 'العمود الأول = فين î راح بعد M1'), ('M2 @', 'طبّق M2 عليه')],
   'القاعدة: العمود k في الناتج = الشمال × العمود k من اليمين. من غير ما تحفظ «صف في عمود».'),
]

MAT_TABLE = '''<table class="types"><tr><th></th><th>دوران ثم Shear</th><th>Shear ثم دوران</th></tr>
<tr><td>المصفوفة</td><td>shear @ rotation</td><td>rotation @ shear</td></tr>
<tr><td>î (من التشغيل)</td><td>(1, 1)</td><td>(0, 1)</td></tr>
<tr><td>ĵ</td><td>(‎-1, 0)</td><td>(‎-1, 1)</td></tr>
<tr><td>نفس الحاجة؟</td><td colspan="2">لأ (False). لكن (A B) C = A (B C)</td></tr></table>'''

CAD_WORDS = [
 W('return { { { 1, 0, 0, tx }, { 0, 1, 0, ty }, { 0, 0, 1, tz }, { 0, 0, 0, 1 } } };', [('العمود الرابع', 'tx, ty, tz'), ('الصف الرابع', '0 0 0 1')],
   'Code Imposter: الواحدات على القطر بتحافظ على x و y و z، والعمود الرابع بيتضرب في الـ 1 بتاع الركن ويتجمع. و glm::translate بتعمل نفس المصفوفة.'),
 W('Where("  R * T (orbit around 0)", Multiply(R, T));', [('T * R', 'T على الشمال: لف في المكان'), ('R * T', 'T على اليمين: Orbit حوالين المركز')],
   'Code Imposter: الترتيب بيفرق جداً. T * R = الموديل بيلف على نفسه في مكانه الجديد. R * T = التحريك نفسه بيلف، فالموديل بيدور في مدار.'),
]

CAD_TABLE = '''<table class="types"><tr><th>الزاوية</th><th>T * R: المركز</th><th>R * T: المركز</th></tr>
<tr><td>0</td><td>(7, 0)</td><td>(7, 0)</td></tr>
<tr><td>90</td><td>(7, 0)</td><td>(0, 7)</td></tr>
<tr><td>180</td><td>(7, 0)</td><td>(‎-7, 0)</td></tr>
<tr><td>270</td><td>(7, 0)</td><td>(0, ‎-7)</td></tr></table>'''
