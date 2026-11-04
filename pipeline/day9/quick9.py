import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY9_CARDS = [
 card('#2563eb', 'البرمجة: struct مقابل class', [
   'الفرق الوحيد: الـ struct كل حاجة فيه <code>public</code> لوحدها، والـ class <code>private</code>.',
   'الاتنين فيهم متغيرات ودوال، ونفس الحجم في الرام.',
   'The Cherno: struct للبيانات البسيطة (Vec2، ركن، لون)، و class للحاجات اللي فيها منطق.',
   'الـ struct الركن = الـ stride، و <code>offsetof</code> = الـ offset.'],
   ['struct Vec2 { float x, y; void Add(const Vec2& other) { … } };', 'struct Vertex { float x, y; float u, v; };   // sizeof = 16'],
   'تكتب <code>private:</code> في struct أو تنسى <code>public:</code> في class: «is private within this context».', '<code>struct_class.cpp</code> و <code>vertex_struct.cpp</code>.'),
 card('#0d9488', 'الرسم: Textures (Victor Gordan)', [
   '<code>stbi_load(…, 0)</code> = هات الصورة بعدد قنواتها، و <code>glTexImage2D</code> لازم يطابق (RGBA = 4).',
   'MIN = <code>GL_NEAREST_MIPMAP_NEAREST</code> محتاج <code>glGenerateMipmap</code>.',
   'MAG = <code>GL_NEAREST</code>: مربعات حادة للـ Pixel Art.',
   'WRAP: REPEAT و MIRRORED_REPEAT و CLAMP_TO_EDGE و CLAMP_TO_BORDER (+ لون الحدود).'],
   ['glTexImage2D(…, GL_RGBA, …, GL_RGBA, GL_UNSIGNED_BYTE, bytes); glGenerateMipmap(GL_TEXTURE_2D);', 'glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border);'],
   'تنسى <code>glGenerateMipmap</code>: أسود من غير أي خطأ.', '<code>pixel_cat.cpp</code> و <code>wrap_modes.cpp</code>.'),
 card('#c2410c', 'الرياضيات: تحويلات المتجهات', [
   'التحويل = دالة على المتجهات: <bdi dir="ltr">T: ℝⁿ → ℝᵐ</bdi>.',
   'مثال Khan: T(x₁, x₂, x₃) = (x₁ + 2x₂, 3x₃) من ℝ³ لـ ℝ².',
   'نفس T = مصفوفة 2 × 3: صفوف = عدد الخارج، أعمدة = عدد الداخل.',
   'الخطي: الأصل مايتحركش، و T(a + b) = T(a) + T(b).'],
   ['T(1, 1, 1) = (3, 3)   T(2, 4, 1) = (10, 3)', 'screen = (P @ centered.T).T   # P is 2 x 3'],
   'تجرّب مثال واحد وتصدّق: المصفوفة الغلط ممكن تطلّع نفس النتيجة بالصدفة.', '<code>transform.py</code> و <code>projection.py</code>.'),
 card('#7c3aed', 'الـ CAD: الشبكات المثلثية', [
   '3 نقط = مستوى واحد: المثلث دايماً مسطح.',
   'Indexed Face List: الأركان مرة واحدة، والمثلثات أرقام (= الـ EBO).',
   'Barycentric: P = αP₀ + βP₁ + γP₂، و α + β + γ = 1.',
   'سالبة = برّه. صفر = على ضلع. اتنين صفر = على ركن. والكارت بيلوّن بيها.'],
   ['cube: 12 triangles, E = 18, 8 - 18 + 12 = 2', 'color = alpha * red + beta * green + gamma * blue'],
   'تعد الأضلاع من غير ما تشيل التكرار: كل ضلع بيتعد مرتين.', '<code>mesh.cpp</code> و <code>barycentric.cpp</code>.'),
]

DAY9_QA = [
 ('البرمجة: struct و class', [
   ('<code>struct A { int x; };</code> وفي main <code>a.x = 1;</code>. شغال؟', 'أيوه: الـ struct كله public لوحده.'),
   ('<code>class A { int x; };</code> ونفس السطر؟', 'خطأ ترجمة: x <code>private</code>.'),
   ('struct فيه رقمين float ودالة: <code>sizeof</code> كام؟', '8 بايت. الدالة مش بتاخد مكان.'),
   ('<code>struct Vertex { float x, y, z; float u, v; };</code>: الـ stride والـ offset بتاع u؟', 'الـ stride = 20، والـ offset = 12.'),
   ('زوّدت <code>int id;</code> في Vertex. إيه اللي لازم يتغير في OpenGL؟', 'الـ stride في <code>glVertexAttribPointer</code> (بقى 20).')]),
 ('الرسم: Textures', [
   ('<code>stbi_load(…, 0)</code> والملف PNG فيه شفافية. أكتب إيه في <code>glTexImage2D</code>؟', '<code>GL_RGBA</code> (4 قنوات).'),
   ('MIN_FILTER = <code>GL_NEAREST_MIPMAP_NEAREST</code> ونسيت <code>glGenerateMipmap</code>؟', 'مربع أسود، و <code>glGetError()</code> = 0.'),
   ('صورة 16 × 16: النسخ المصغّرة كام وأحجامها؟', 'عدد 4: ‏8 و 4 و 2 و 1.'),
   ('الإحداثيات 1.3 مع <code>GL_CLAMP_TO_EDGE</code>؟', 'لون آخر بكسل في الحافة.'),
   ('إيه الفرق بين REPEAT و MIRRORED_REPEAT؟', 'التاني بيقلب كل نسخة زي المراية.')]),
 ('الرياضيات: التحويلات', [
   ('T(x₁, x₂, x₃) = (x₁ + 2x₂, 3x₃). T(0, 1, 2) = ؟', '(2, 6).'),
   ('مصفوفة التحويل من ℝ³ لـ ℝ² مقاسها كام؟', '2 × 3.'),
   ('S(v) = (x₁², x₂ + 1). خطي؟', 'لأ: S(0, 0, 0) = (0, 1)، الأصل اتحرك.'),
   ('A = [[1, 2, 0], [0, 0, 3]]. A × (1, 0, 1) = ؟', '(1, 3).')]),
 ('الـ CAD: الشبكات المثلثية', [
   ('ليه المثلث أحسن من المربع في الرسم؟', '3 نقط دايماً على مستوى واحد. الركن الرابع ممكن يطلع برّه المستوى.'),
   ('مكعب بمثلثات: V و E و F؟', 'V = 8، E = 18، F = 12، و 8 − 18 + 12 = 2.'),
   ('α = 0 و β = 0.5 و γ = 0.5. النقطة فين؟', 'على الضلع اللي قصاد P₀.'),
   ('α = ‎-0.5. النقطة فين؟', 'برّه المثلث.'),
   ('بكسل α = 0.25 و β = 0.25 و γ = 0.5 والأركان أحمر وأخضر وأزرق. لونه؟', '(0.25, 0.25, 0.5) يعني تقريباً 64 64 128 (برنامجنا طلع 63 64 128).')]),
]
