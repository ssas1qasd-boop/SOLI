import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY11_CARDS = [
 card('#2563eb', 'البرمجة: Stack و Heap', [
   'الاتنين في الرام. الـ Stack صغير (8 MB هنا) والحجز فيه = تحريك الـ Stack Pointer.',
   'الـ Heap كبير، والحجز فيه بـ <code>new</code> = malloc بتدوّر وتسجّل (أبطأ حوالي 5 مرات في التجربة).',
   'الـ Stack بيترجع لوحده عند الـ <code>}</code>. والـ Heap بإيدك: <code>delete</code> و <code>delete[]</code>.',
   'استخدم الـ Heap لما الحاجة كبيرة (صورة 16 MB) أو لازم تعيش بعد الدالة.'],
   ['int value = 5;            // stack', 'int* hvalue = new int;  ...  delete hvalue;   // heap'],
   'تنسى <code>delete</code> في لوب: البرنامج شغال عادي وبيسرّب ذاكرة (valgrind: 1,200 بايت).', '<code>stack_heap.cpp</code> و <code>speed_size.cpp</code>.'),
 card('#0d9488', 'الرسم: Texture wrapping والـ Texture Units', [
   'REPEAT = <code>u - floor(u)</code>، و MIRRORED = <code>1 - |mod(u, 2) - 1|</code>، و CLAMP = <code>clamp(u, 0, 1)</code>.',
   'الـ Texture Unit هاردوير بيعمل ده لوحده، وعددها محدود (<code>GL_MAX_TEXTURE_IMAGE_UNITS</code> = 32 هنا).',
   'Procedural Texture = دالة بدل صورة: 0 بايت ومتكررة للأبد.',
   'صورة من مصفوفة صفها مش مضاعف 4 بايت: <code>glPixelStorei(GL_UNPACK_ALIGNMENT, 1)</code>.'],
   ['letter.SetWrap(GL_MIRRORED_REPEAT);', 'return 1.0 - abs(mod(uv, 2.0) - 1.0);'],
   'تستخدم <code>int()</code> بدل <code>floor</code>: الإحداثيات السالبة بتبوظ.', '<code>wrap_by_hand.cpp</code> و <code>procedural.cpp</code>.'),
 card('#c2410c', 'الرياضيات: جمع وطرح المصفوفات', [
   'نفس المقاس بس، وكل خانة + اللي قصادها.',
   'A + B = B + A، لكن A - B ≠ B - A.',
   'A - B = A + (‎-1) B.',
   'في الرسم: مصفوفة نقل بنفس مقاس الأركان = كل الأركان تتحرك.'],
   ['A + B   # [[6, -7, 8], [11, 2, -3]]', 'moved = house + move   # 6 x 2 + 6 x 2'],
   'تفتكر إن NumPy بيرفض أي مقاسين مختلفين: صف واحد (1 × 2) بيتجمع (Broadcasting).', '<code>add_subtract.py</code> و <code>move_shape.py</code>.'),
 card('#7c3aed', 'الـ CAD: Mesh مقابل B-Rep', [
   'الـ Mesh = أركان + وشوش (OBJ: سطور v و f، والعد من 1).',
   'ترتيب أركان الوش بيحدد الـ Normal: عكس عقارب الساعة = ناحيتك.',
   'الـ Mesh تقريب: الدايرة مضلع، والغلط R (1 - cos(ط/n)).',
   'الـ B-Rep شايل المعادلة نفسها: 3 وشوش للأسطوانة بدل مئات المثلثات.'],
   ['f 1 4 3 2      # OBJ bottom face', 'n = 256 for R = 50 mm at 0.01 mm'],
   'تنسى <code>index - 1</code> وانت بتقرا OBJ: البرنامج بيقرا ركن مش موجود.', '<code>obj_cube.cpp</code> و <code>mesh_vs_brep.cpp</code>.'),
]

DAY11_QA = [
 ('البرمجة: Stack و Heap', [
   ('<code>int* p = new int[10];</code>. ترجّعه إزاي؟', '<code>delete[] p;</code> (مع الأقواس).'),
   ('ليه الصورة 16 MB ماتنفعش على الـ Stack؟', 'الـ Stack هنا 8 MB بس. جربناها: Segmentation fault.'),
   ('دالة لازم ترجّع حاجة تعيش بعدها: Stack ولا Heap؟', 'Heap (زي LoadTexture). اللي على الـ Stack بيموت عند الـ <code>}</code>.'),
   ('ليه الـ int على الـ Heap خد 32 بايت مكان؟', 'malloc بتحجز حتة أكبر عشان دفاترها (Bookkeeping) والتقريب.')]),
 ('الرسم: Texture wrapping', [
   ('u = 2.7 مع REPEAT = ؟', '0.7.'),
   ('u = 1.25 مع MIRRORED = ؟', '0.75.'),
   ('u = ‎-0.5 مع CLAMP = ؟', '0.'),
   ('صورة 3 × 3 بـ RGB من مصفوفة. محتاج glPixelStorei؟', 'أيوه: الصف 9 بايت مش مضاعف 4.'),
   ('إيه ميزة الـ Procedural Texture؟', 'مالهاش حجم في الذاكرة، وبتتكرر من غير حد، ومفيش ضبابية لما تتكبر.')]),
 ('الرياضيات: الجمع والطرح', [
   ('[[1, 2], [3, 4]] + [[4, 3], [2, 1]] = ؟', '[[5, 5], [5, 5]].'),
   ('2 × 3 + 3 × 2 = ؟', 'مش متعرّف (Undefined).'),
   ('A - B = [[1, 0], [0, 1]]. يبقى B - A = ؟', '[[‎-1, 0], [0, ‎-1]].'),
   ('عايز تحرّك 4 أركان (4 × 2) خطوة (2, 0). مصفوفة النقل؟', '4 صفوف كلهم [2, 0].')]),
 ('الـ CAD: Mesh و B-Rep', [
   ('في OBJ: <code>f 1 2 3</code>. أول ركن في C++ رقمه كام؟', '0.'),
   ('قلبنا ترتيب أركان وش. إيه اللي اتغيّر؟', 'الـ Normal بقى للناحية التانية (العدد وأويلر زي ما هما).'),
   ('أسطوانة n = 8: كام مثلث؟', '28 = 4 × 8 - 4.'),
   ('ليه برامج CAD بتشيل B-Rep مش Mesh؟', 'الـ B-Rep مظبوط (معادلة الدايرة)، والـ Mesh تقريب بيكبر غلطه لو الحتت قليلة.')]),
]
