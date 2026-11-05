import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY12_CARDS = [
 card('#2563eb', 'البرمجة: new و delete', [
   '<code>new</code> = حجز (بتنادي malloc) + نداء الـ Constructor. و <code>malloc</code> حجز بس.',
   'إحنا ممكن نكتب <code>operator new</code> بنفسنا: عرفنا الأحجام 4 و 200 و 32 و 104.',
   '<code>new Entity[3]</code> = 104 بايت: 96 + 8 بيشيلوا العدد عشان <code>delete[]</code>.',
   'Placement new <code>new (b) T(...)</code>: Constructor بس على ذاكرة موجودة، ويترجع بـ <code>v->~T()</code>.'],
   ['Entity* e = new Entity();   // malloc + Entity()', 'Vector3* v = new (b) Vector3(1, 2, 3);'],
   '<code>delete</code> لحاجة اتعملت بـ <code>new[]</code>: البرنامج وقع (munmap_chunk: invalid pointer).', '<code>new_operator.cpp</code> و <code>placement_new.cpp</code>.'),
 card('#0d9488', 'الرسم: Mipmaps و Anisotropic Filtering', [
   'الـ Mipmaps = نسخ أصغر من الصورة (256 لـ 1)، بتزوّد الثلث بس (1.333 ×).',
   'من غيرها الأرضية البعيدة بتعمل Moiré (تموّج).',
   'الـ Mipmap للتصغير (MIN) بس. التكبير (MAG) NEAREST أو LINEAR.',
   'الـ Anisotropy (لحد 16) بيصلّح الرمادي اللي بيظهر في الزوايا الحادة.'],
   ['glGenerateMipmap(GL_TEXTURE_2D);', 'glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY, 16.0f);'],
   'فلتر MIPMAP من غير مستويات كاملة: الـ Texture أسود، ومن غير رسالة.', '<code>mipmaps.cpp</code> و <code>mip_levels.cpp</code>.'),
 card('#c2410c', 'الرياضيات: NumPy (مراجعة)', [
   '<code>shape</code> و <code>dtype</code> و <code>itemsize</code> و <code>nbytes</code>.',
   '<code>m[صف, عمود]</code> و <code>:</code> و <code>بداية:نهاية:خطوة</code>.',
   '<code>y = x</code> نفس المصفوفة، و <code>x.copy()</code> نسخة.',
   '<code>np.matmul</code> ضرب مصفوفات، و <code>*</code> خانة × خانة.'],
   ['m[0, 1:6:2]          # [2 4 6]', 'data[data > 50]      # [75 88 51]'],
   'تحط 2.7 في مصفوفة int: بتتخزن 2 من غير تحذير.', '<code>numpy_arrays.py</code> و <code>numpy_math.py</code>.'),
 card('#7c3aed', 'الـ CAD: Wireframe و Surface و Solid', [
   'Parametric: x = R sinθ، و y = R cosθ، و z = H.',
   'عدد البارامترات الحرة: 0 نقطة، 1 منحنى، 2 سطح، 3 جسم.',
   'الـ Wireframe = خطوط (طول بس)، والـ Surface = وشوش (مساحة)، والـ Solid = جوه وبرّه (حجم).',
   'الـ Solid بس يقدر يقول النقطة جوه ولا برّه.'],
   ['Shape("cylinder", {10, 10}, {-PI, PI}, {0, 25});   // surface', 'Inside(solid, {0, 0, 0})   // 1'],
   'Normal مقلوب في Solid: الجسم بيتفتح والحجم بيطلع غلط (12 بدل 8).', '<code>parametric.cpp</code> و <code>three_models.cpp</code>.'),
]

DAY12_QA = [
 ('البرمجة: new', [
   ('إيه الفرق بين <code>new Entity()</code> و <code>malloc(sizeof(Entity))</code>؟', '<code>new</code> بتنادي الـ Constructor، و malloc لأ.'),
   ('<code>new int[50]</code> طلب كام بايت؟', '200 = 50 × 4.'),
   ('ليه <code>new Entity[3]</code> طلب 104 مش 96؟', '8 بايت زيادة بيشيلوا العدد 3 عشان <code>delete[]</code> تنادي 3 Destructors.'),
   ('بعد Placement new بتعمل إيه؟', 'تنادي الـ Destructor بإيدك (<code>v->~Vector3()</code>)، وماتعملش <code>delete v</code>.')]),
 ('الرسم: Mipmaps', [
   ('صورة 512 × 512 فيها كام مستوى؟', '10: من 512 لـ 1.'),
   ('الـ Mipmaps بتزوّد الذاكرة قد إيه؟', 'حوالي الثلث (1.333 × الأصل).'),
   ('ينفع MAG_FILTER = LINEAR_MIPMAP_LINEAR؟', 'لأ: GL_INVALID_ENUM. التكبير مش محتاج نسخ أصغر.'),
   ('ليه الأرضية البعيدة بتبقى رمادي مع الـ Mipmap؟', 'البكسل بيغطي حتة طويلة رفيعة، والكارت بيختار مستوى صغير على قد الضلع الطويل. الحل Anisotropy.'),
   ('شيلنا glGenerateMipmap. إيه اللي باظ؟', 'المربعات اللي فلترها MIPMAP بس: بقت سودا.')]),
 ('الرياضيات: NumPy', [
   ('<code>m[1, -2]</code> لـ m (2 × 7) = ؟', 'الصف 1، التاني من الآخر: 13.'),
   ('<code>np.ones((2, 3)) @ np.full((3, 2), 2)</code> = ؟', '2 × 2 كلها 6.'),
   ('<code>reshape((2, 3))</code> لمصفوفة 8 أرقام؟', 'ValueError: 6 ≠ 8.'),
   ('<code>y = x; y[0] = 100</code>. x اتغيّرت؟', 'أيوه. لو عايز نسخة: <code>x.copy()</code>.')]),
 ('الـ CAD: التمثيل', [
   ('R ثابت و θ و H بيتغيروا: الشكل إيه؟', 'سطح أسطوانة (2 بارامتر حر).'),
   ('مكعب ضلعه 2 Wireframe: نعرف حجمه؟', 'لأ. الطول بس (24).'),
   ('ليه الـ Solid بيقدر يحسب الحجم؟', 'بيعرف أي نقطة جوه ولا برّه.'),
   ('R من 5 لـ 10: الشكل إيه؟', 'أسطوانة مجوّفة (جسم): ط (10² - 5²) H.')]),
]
