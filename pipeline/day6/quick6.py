import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY6_CARDS = [
 card('#2563eb', 'البرمجة: Compiler صغير + تمرينين exercism', [
   'الـ Compiler = 3 مراحل: Scanner (حروف ← Tokens)، و Parser (Tokens ← شجرة)، و Compiler (شجرة ← Bytecode). والـ VM بتنفذ.',
   'الأولوية من ترتيب الدوال: الجمع بينده الضرب، فالضرب بيتعمل الأول.',
   'الـ Bytecode بيشتغل على Stack: الرقم يتحط فوق، والعملية تشيل اتنين وتحط واحد.',
   'exercism: اكتب الدالة، والاختبارات تقولك PASS أو FAIL.'],
   ['Node* left = Multiplication();', 'while (Match(TokenType::Plus)) left = new Node{ \'+\', 0, "", left, Multiplication() };'],
   'تبدّل مستويات الأولوية: البرنامج يشتغل عادي ويطلّع 9 بدل 7.', 'البرنامج 1 (<code>tiny_compiler.cpp</code>) و 2 و 3.'),
 card('#0d9488', 'الرسم: ألوان متحركة (Uniforms)', [
   'الـ uniform قيمة واحدة لكل الرسمة، جاية من الـ CPU. والـ attribute قيمة لكل ركن.',
   'الخطوات: <code>glUseProgram</code> ← <code>glGetUniformLocation</code> (مرة واحدة) ← <code>glUniform4f</code> (أو <code>1f</code>) كل فريم.',
   'النوع لازم يطابق: <code>float</code> ← <code>1f</code>، و <code>vec4</code> ← <code>4f</code>.',
   '‎-1 = الاسم غلط أو الـ uniform مش مستخدم.'],
   ['int location = glGetUniformLocation(shader, "u_Color");', 'glUniform4f(location, r, 0.3f, 0.8f, 1.0f);'],
   'uniform مش مستخدم في الـ Shader: الكارت بيشيله ويرجّع ‎-1 مع إن الاسم صح.', 'البرنامج 1 (<code>animated_color.cpp</code>) و 2 (<code>time_colors.cpp</code>).'),
 card('#c2410c', 'الرياضيات: مراجعة dot والطول', [
   'a · b = a₁b₁ + a₂b₂ + … : رقم واحد.',
   '‖a‖ = √(a · a)، يعني ‖a‖² = a · a.',
   'c · d = d · c، والتوزيع، والرقم يطلع برا.',
   'نقسم على الطول ← متجه طوله 1.'],
   ['def dot(a, b): total = sum of a[i] * b[i]', 'def length(a): return math.sqrt(dot(a, a))'],
   'تنسى الجذر: الطول يطلع مربعه. أو متجهين مختلفين في الطول.', '<code>dot_length.py</code> و <code>numpy_review.py</code>.'),
 card('#7c3aed', 'الـ CAD: تنظيف الكود (Refactoring)', [
   'Refactoring = تغيّر الكود من جوه، والبرنامج من برا يفضل زي ما هو بالظبط.',
   'أرقام سحرية ← ثوابت بأسماء. كود متكرر ← دالة واحدة (DRY).',
   'كل دالة تعمل حاجة واحدة واسمها فعل: <code>AddPoint</code> و <code>DeleteLastLine</code>.',
   'بعد كل تغيير: شغّل بنفس الدخل وقارن الكلام والصورة.'],
   ['const int kWindowWidth = 640;', 'static void StartNewLine() { polylines.push_back({ PointCount(), 0 }); }'],
   'غلطة صغيرة (زي نسيان <code>* 2</code>) تغيّر الصورة والكلام يفضل زي ما هو: قارن الاتنين.', 'البرنامج 1 (<code>refactored.cpp</code>).'),
]

DAY6_QA = [
 ('البرمجة: Compiler و exercism', [
   ('إيه الـ Tokens بتوع <code>y = 4 * x;</code> في لغتنا؟', '[y] [=] [4] [*] [x] [;]'),
   ('ليه الضرب بيتحسب قبل الجمع في الـ Parser بتاعنا؟', 'لأن <code>Addition</code> بتنده <code>Multiplication</code> لكل حتة، فالضرب بيتقفل في فرع لوحده تحت الـ <code>+</code>.'),
   ('الـ Bytecode لـ <code>2 + 3</code>؟', '<code>LOAD_INT 2</code> ثم <code>LOAD_INT 3</code> ثم <code>ADD</code>.'),
   ('2100 كبيسة؟ و 2000؟', '2100 لأ (بتقبل على 100 ومش على 400). 2000 أيوه (بتقبل على 400).'),
   ('Raindrops لـ 21؟', 'PlingPlong (3 و 7).')]),
 ('الرسم: Uniforms', [
   ('إيه الفرق بين uniform و attribute؟', 'الـ uniform قيمة واحدة للرسمة كلها من الـ CPU. الـ attribute قيمة لكل ركن من الصندوق.'),
   ('<code>glGetUniformLocation</code> رجّعت ‎-1. ليه؟', 'الاسم مكتوب غلط، أو الـ uniform مش مستخدم في الـ Shader فالكارت شاله.'),
   ('uniform اسمه <code>u_Size</code> نوعه <code>float</code>. تبعته بإيه؟', '<code>glUniform1f(location, 2.0f);</code>'),
   ('ليه بنجيب الـ location قبل اللوب؟', 'الرقم مش بيتغير، والدوران على الاسم كل فريم شغل على الفاضي.')]),
 ('الرياضيات: dot والطول', [
   ('[3, 4] · [1, 2] = ؟', '3 + 8 = 11.'),
   ('طول [3, 4]؟', '√(9 + 16) = 5.'),
   ('لو a · a = 49، الطول كام؟', '7.'),
   ('الـ Unit vector بتاع [0, 5]؟', '[0, 1].')]),
 ('الـ CAD: Refactoring', [
   ('إيه اللي مينفعش يتغير في الـ Refactoring؟', 'سلوك البرنامج من برا: اللي بيطبعه واللي بيرسمه.'),
   ('إيه «الرقم السحري»؟', 'رقم مكتوب في الكود من غير اسم، زي 640. بنحطه في ثابت باسم.'),
   ('إزاي نتأكد إن الـ Refactoring ما بوّظش حاجة؟', 'نشغّل القديم والجديد بنفس الدخل ونقارن الكلام <b>والصورة</b>.')]),
]
