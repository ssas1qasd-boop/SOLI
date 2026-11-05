import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY15_CARDS = [
 card('#2563eb', 'البرمجة: Templates', [
   '<code>template&lt;typename T&gt;</code>: الـ compiler بيكتب نسخة لكل نوع.',
   'النوع بيتعرف لوحده، أو بإيدك: <code>Print&lt;int&gt;(7.9)</code>.',
   'الـ Template مش كود لحد ما تستخدمه.',
   'بارامتر رقم: <code>template&lt;typename T, int N&gt;</code> = std::array.'],
   ['template<typename T> void Print(T value);', 'Array<int, 5> numbers;   // 20 bytes'],
   'Biggest(3, 1.5): نوعين مختلفين لـ T = error.', '<code>print_template.cpp</code> و <code>array_template.cpp</code>.'),
 card('#0d9488', 'الرسم: تحويلات 2D (Cem Yuksel)', [
   'تحريك وتكبير ودوران = Affine. والـ Skew = دوران وتكبير ودوران.',
   'Homogeneous: (x, y, 1) فالتحريك يبقى ضرب، و 3 × 3 لكل حاجة.',
   'حوالين المركز: T(c) R T(‎-c)، واليمين الأول.',
   'w = 1 نقطة بتتحرك، و w = 0 اتجاه بيلف بس.'],
   ['"    vec3 p = u_M * vec3(aPos, 1.0);\\n"', 'glUniformMatrix3fv(matLoc, 1, GL_TRUE, ...);'],
   'GL_FALSE والمصفوفة مكتوبة صف صف: التحريك بيختفي.', '<code>transform2d.cpp</code> و <code>homogeneous.cpp</code>.'),
 card('#c2410c', 'الرياضيات: الضرب = تركيب (3Blue1Brown)', [
   'A @ B = طبّق B الأول وبعدين A.',
   'العمود k في الناتج = A × العمود k من B.',
   'A @ B ≠ B @ A، بس (A B) C = A (B C).',
   'تابع î و ĵ بس.'],
   ['shear @ rotation    # [[1, -1], [1, 0]]', 'M2 @ M1            # [[2, 0], [1, -2]]'],
   '* بدل @: خانة × خانة، مش تركيب.', '<code>composition.py</code> و <code>grid_plot.py</code>.'),
 card('#7c3aed', 'الـ CAD: تحريك موديل 3D', [
   'مصفوفة 4 × 4: Identity + العمود الرابع (tx, ty, tz).',
   'الركن (x, y, z, 1) بيتحرك، والـ Normal (w = 0) لأ.',
   'T * R: لف في المكان. R * T: مدار حوالين المركز.',
   'Animation: التحريك × نسبة من 0 لـ 1.'],
   ['glm::translate(matrix, glm::vec3(7, 3, 5));', 'gl_Position = matrix * aPos;'],
   'التحريك في الصف الأخير بدل العمود: الموديل مابيتحركش.', '<code>translate4x4.cpp</code> و <code>order.cpp</code>.'),
]

DAY15_QA = [
 ('البرمجة: Templates', [
   ('Print("Hi") T طلع إيه؟', 'const char*.'),
   ('Array<int, 5> و Array<int, 6> نفس النوع؟', 'لأ: الرقم جزء من النوع.'),
   ('ليه NeverCalled ماعملتش error؟', 'محدش ناداها، فالـ compiler ماكتبش منها نسخة.')]),
 ('الرسم: 2D', [
   ('مصفوفة تحريك (4, ‎-1) في 3 × 3؟', '[1 0 4] [0 1 ‎-1] [0 0 1].'),
   ('عايز تلف حوالين (2, 3). الترتيب؟', 'T(2, 3) R T(‎-2, ‎-3).'),
   ('عكس R(30)؟', 'Rᵀ = R(‎-30).'),
   ('الاتجاه بياخد w كام؟', '0.')]),
 ('الرياضيات: التركيب', [
   ('A @ B: مين الأول؟', 'B.'),
   ('العمود الأول من A @ B؟', 'A × العمود الأول من B.'),
   ('shear @ rotation = rotation @ shear؟', 'لأ.')]),
 ('الـ CAD: Translate', [
   ('translate(7, 3, 5) × (1, ‎-1, 2, 1)؟', '(8, 2, 7, 1).'),
   ('ليه الـ Normal مايتحركش؟', 'w = 0، فالعمود الرابع بيتضرب في صفر.'),
   ('عايز الموديل يدور حوالين المركز: T * R ولا R * T؟', 'R * T.')]),
]
