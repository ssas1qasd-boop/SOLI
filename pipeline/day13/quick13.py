import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY13_CARDS = [
 card('#2563eb', 'البرمجة: عمر الـ Object', [
   'كل Scope (دالة، if، for، أقواس فاضية) = كتاب على الـ Stack. يخلص = كل اللي فيه يموت.',
   'اللي بـ <code>new</code> مابيموتش عند القوس: لازم delete.',
   'ماترجّعش عنوان متغير على الـ Stack من دالة.',
   'ScopedPtr و <code>std::unique_ptr</code>: object على الـ Stack بيعمل delete في الـ Destructor.'],
   ['{ Entity b("b"); }          // Destroyed b here', '{ ScopedPtr e = new Entity(); }   // deleted here'],
   'نسخ ScopedPtr: الاتنين بيعملوا delete (double free).', '<code>lifetime.cpp</code> و <code>scoped_ptr.cpp</code>.'),
 card('#0d9488', 'الرسم: Textures من الأول (Luke)', [
   '3 خطوات: حمّل، واربط الإحداثيات بالأركان، وارسم بـ sampler.',
   '<code>stbi_set_flip_vertically_on_load(1)</code> لأن (0, 0) في OpenGL تحت شمال.',
   'بعد <code>glTexImage2D</code>: <code>stbi_image_free</code> (الكارت معاه نسخته).',
   'Atlas: صور كتير في Texture واحد، وكل مستطيل بياخد جزء من u و v.'],
   ['glTexImage2D(...); stbi_image_free(data);', 'u0 = (float)col / CELLS;'],
   'تمسح قبل النسخ: ألوان عشوائية من غير أي رسالة.', '<code>gpu_copy.cpp</code> و <code>atlas.cpp</code>.'),
 card('#c2410c', 'الرياضيات: تحويلات بالمصفوفات', [
   'الدوران: [[cos, ‎-sin], [sin, cos]]، والزاوية بالـ Radians.',
   'R @ S = S الأول وبعدين R، و R @ S ≠ S @ R.',
   'عكس الدوران = rotation(‎-θ) = الـ Transpose.',
   'الإسقاط على خط: (x · u) ÷ (u · u) × u، و P @ P = P.'],
   ['rotation(30) @ rotation(60)   # = rotation(90)', 'P = np.outer(u, u) / (u @ u)'],
   'تنسى np.radians: الأرقام كلها غلط بس الشكل «مقنع».', '<code>rotate_compose.py</code> و <code>rotate3d_project.py</code>.'),
 card('#7c3aed', 'الـ CAD: Solid modeling و CSG', [
   'CSG = أجسام بسيطة + Union و Intersect و Difference.',
   'بيسموها Boolean، والأدق Set Operations.',
   'لو الجسم دالة «جوه؟»: || و && و && !.',
   'Regularized: بتشيل الوشوش والخطوط اللي مالهاش حجم.'],
   ['return InSphere(p) && !InBox(p);   // A minus B', 'Regularize(Intersect(A, C))   // 0 pieces'],
   '|| بدل && في الـ Difference: النتيجة الفراغ كله تقريباً.', '<code>csg.cpp</code> و <code>regularized.cpp</code>.'),
]

DAY13_QA = [
 ('البرمجة: عمر الـ Object', [
   ('<code>{ Entity b("b"); }</code>: b بيموت إمتى؟', 'عند الـ <code>}</code> بالظبط.'),
   ('<code>{ Entity* h = new Entity(); }</code>: الـ Entity بيموت إمتى؟', 'مش بيموت لوحده: لازم delete (أو النظام لما البرنامج يقفل).'),
   ('دالة بترجّع <code>int array[50]</code> على الـ Stack. إيه المشكلة؟', 'المصفوفة ماتت مع الدالة، والعنوان بقى بيشاور على ذاكرة مش بتاعتنا (البرنامج وقع).'),
   ('ScopedPtr حجمه كام؟', '8 بايت: زي الـ Pointer بالظبط.')]),
 ('الرسم: Textures', [
   ('ليه بنقلب الصورة؟', '(0, 0) في OpenGL تحت شمال، والصورة في الملف بتبدأ من فوق.'),
   ('إمتى نعمل stbi_image_free؟', 'بعد glTexImage2D.'),
   ('Atlas 4 × 4، الخانة 6. u من كام لكام؟', 'العمود 2: من 0.5 لـ 0.75. والصف 1: v من 0.25 لـ 0.5.'),
   ('صورة RGB عرضها 8. محتاجين UNPACK_ALIGNMENT؟', 'لأ: الصف 24 بايت = مضاعف 4. بس حطه دايماً عشان الصور التانية.')]),
 ('الرياضيات: التحويلات', [
   ('rotation(90) @ (1, 0) = ؟', '(0, 1).'),
   ('R @ S: مين بيحصل الأول؟', 'S (الأقرب للنقطة).'),
   ('عكس rotation(40)؟', 'rotation(‎-40) = rotation(40).T.'),
   ('إسقاط (3, 4) على محور x؟', '(3, 0): u = (1, 0)، و (x · u) ÷ 1 = 3.')]),
 ('الـ CAD: CSG', [
   ('مكعب فيه خرم أسطواني: أنهي عملية؟', 'Difference: المكعب - الأسطوانة.'),
   ('Intersect لكرتين مش لامسين بعض؟', 'فاضي.'),
   ('ليه Set Operations أدق من Boolean؟', 'الجسم مجموعة نقط، والعمليات اتحاد وتقاطع وفرق مجموعات.'),
   ('مكعبين لامسين بعض في وش: Intersect العادي = ؟', 'الوش ده لوحده (مالوش حجم). والـ Regularized = فاضي.')]),
]
