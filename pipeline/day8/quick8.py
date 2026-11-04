import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY8_CARDS = [
 card('#2563eb', 'البرمجة: الـ Classes', [
   'الـ Class = نوع جديد بيجمع بيانات (Members) ودوال (Methods).',
   'الـ Object = نسخة حقيقية في الرام: <code>Player player;</code>. حجمها = مجموع متغيراتها (12 بايت).',
   'الافتراضي <code>private</code>. اكتب <code>public:</code> عشان توصل من برّه.',
   'الـ Method بتشتغل على الـ Object اللي اتنادت عليه: <code>this</code> = عنوانه.'],
   ['class Player { public: int x, y, speed; void Move(int xa, int ya) { … } };', 'player.Move(1, -1);'],
   'تنسى <code>public:</code>: الـ compiler يرفض «is private within this context».', 'البرنامج 1 (<code>player.cpp</code>) و 2 (<code>counter.cpp</code>).'),
 card('#0d9488', 'الرسم: الـ Textures', [
   'الـ Texture = صورة في ذاكرة الكارت، والـ Shader بيقرا منها لون كل بكسل.',
   'كل ركن ليه إحداثيات في الصورة (u, v) من 0 لـ 1. (0, 0) = تحت شمال.',
   'الإعدادات الأربعة: MIN و MAG و WRAP_S و WRAP_T. من غير MIN = أسود.',
   'الخانة (Slot): <code>Bind(0)</code> و <code>glUniform1i(location, 0)</code> لازم نفس الرقم.'],
   ['stbi_load(…) → glTexImage2D(…) → glActiveTexture(GL_TEXTURE0) → glUniform1i(location, 0)', 'color = texture(u_Texture, v_TexCoord);'],
   'تنسى <code>stbi_set_flip_vertically_on_load(1)</code>: الصورة مقلوبة.', 'البرنامج 1 (<code>texture.cpp</code>) و 2 (<code>texture_settings.cpp</code>).'),
 card('#c2410c', 'الرياضيات: المصفوفة = تحويل', [
   'التحويل الخطي: الخطوط تفضل خطوط، والأصل (0, 0) مايتحركش.',
   'العمود الأول = فين î راح، والتاني = فين ĵ راح.',
   'M v = x × العمود الأول + y × العمود التاني.',
   'أعمدة على نفس الخط = المستوى كله يتكبس على خط.'],
   ['[[1, 3], [-2, 0]] @ [-1, 2] = -1*[1, -2] + 2*[3, 0] = [5, 2]', 'rotate 90 = [[0, -1], [1, 0]]'],
   'تقرا الصف على إنه العمود: كل النتايج تطلع غلط.', '<code>matrix_columns.py</code> و <code>numpy_grid.py</code>.'),
 card('#7c3aed', 'الـ CAD: الـ B-Rep', [
   'الـ B-Rep = بنوصف الجسم بحدوده: وشوش (Faces) وأضلاع (Edges) وأركان (Vertices).',
   'Geometry = الأماكن، و Topology = مين متوصل بمين.',
   'أويلر للجسم المقفول من غير خروم: F − E + V = 2.',
   'في جسم مقفول كل ضلع بين وشين بالظبط.'],
   ['cube: 6 - 12 + 8 = 2', 'for (const Edge& e : edges) { lines.push_back(e.v0); lines.push_back(e.v1); }'],
   'تثق في أويلر لوحده: الأعداد ممكن تبقى صح والتوصيل غلط.', '<code>brep.cpp</code> و <code>wireframe.cpp</code>.'),
]

DAY8_QA = [
 ('البرمجة: Classes', [
   ('<code>class A { int x; };</code> وكتبت في main <code>a.x = 1;</code>. إيه اللي يحصل؟', 'خطأ ترجمة: x <code>private</code> (الافتراضي في class).'),
   ('<code>sizeof</code> لكلاس فيه 3 متغيرات int ودالتين؟', '12 بايت. الدوال مش بتاخد مكان جوه الـ Object.'),
   ('إيه الفرق بين <code>player.Move(1, -1)</code> و <code>Move(player, 1, -1)</code>؟', 'نفس الشغل. الأولى Method والـ Object بيتبعت في السر (<code>this</code>)، والتانية دالة برّه بتاخد Reference.'),
   ('جوه <code>clicks.Where()</code>، <code>this</code> بيساوي إيه؟', '<code>&amp;clicks</code>.'),
   ('ليه Add بترفض الأرقام السالبة؟', 'عشان العداد <code>private</code> والكلاس بيتحكم في قيمته: محدش ينقّصه.')]),
 ('الرسم: Textures', [
   ('شلت <code>GL_TEXTURE_MIN_FILTER</code>. إيه اللي يظهر؟', 'مربع أسود، و <code>glGetError()</code> = 0.'),
   ('إحداثيات الـ Texture للركن فوق يمين؟', '(1, 1).'),
   ('<code>texture.Bind(0)</code> و <code>glUniform1i(location, 1)</code>. النتيجة؟', 'أسود: الـ Shader بيقرا من الخانة 1 الفاضية.'),
   ('الإحداثيات من 0 لـ 2 مع <code>GL_REPEAT</code>؟', 'الصورة تتكرر مرتين في كل اتجاه.'),
   ('ليه الأماكن الشفافة طلعت سودا؟', 'ناقص <code>glEnable(GL_BLEND)</code>.')]),
 ('الرياضيات: المصفوفات', [
   ('M = [[1, 3], [‎-2, 0]]. î بيروح فين؟', '(1, ‎-2): العمود الأول.'),
   ('[[0, ‎-1], [1, 0]] × [2, 1] = ؟', '2 × [0, 1] + 1 × [‎-1, 0] = [‎-1, 2].'),
   ('[[1, 1], [0, 1]] × [2, 1] = ؟', '[3, 1].'),
   ('الأعمدة [2, 1] و [‎-2, ‎-1]. إيه اللي يحصل للمستوى؟', 'بيتكبس على خط واحد (كل النتايج مضاعفات [2, 1]).')]),
 ('الـ CAD: B-Rep', [
   ('هرم قاعدته مربع: V و E و F كام؟', 'V = 5، E = 8، F = 5، و 5 − 8 + 5 = 2.'),
   ('مكعب من غير غطا: F − E + V = ؟', '5 − 12 + 8 = 1.'),
   ('أويلر طلع 2. يبقى الجسم أكيد سليم؟', 'لأ. ممكن التوصيل غلط (جربنا: أويلر 2 وفيه ضلعين مكشوفين).'),
   ('ليه التحويل من B-Rep لـ Wireframe سهل؟', 'لأن قايمة الأضلاع = أزواج أركان = ترتيب رسم <code>GL_LINES</code> على طول.')]),
]
