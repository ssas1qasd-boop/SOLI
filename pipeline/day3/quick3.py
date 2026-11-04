import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY3_CARDS = [
 card('#2563eb', 'البرمجة: References + Hamming', [
   'الـ Reference = اسم تاني لمتغير موجود. مش صندوق جديد ومش عنوان.',
   'علامة <code>&amp;</code> لازقة في نوع (<code>int&amp;</code>) = اسم تاني. وقبل متغير (<code>&amp;a</code>) = عنوان.',
   'لازم يتربط بحاجة وهو بيتعمل، ومابيتنقلش لحاجة تانية بعد كده.',
   'في C النص بيخلص بحرف خفي اسمه <code>\'\\0\'</code>، وأي متغير لازم تبدأه بقيمة.'],
   ['void Increment(int& value) { value++; }', 'Increment(a);          // a changes, no & and no *'],
   'تنسى <code>&amp;</code> في الدالة: البرنامج يشتغل والأصل مايتغيرش.', 'البرنامج 2 (<code>increment.cpp</code>).'),
 card('#0d9488', 'الرسم: الـ Shaders في ملف', [
   'الـ Vertex والـ Fragment في ملف واحد، وعلامة <code>#shader</code> بتفصلهم.',
   '<code>ParseShader</code> بتقرا سطر سطر وتحط كل سطر في النص بتاعه.',
   'المسار نسبي للمكان اللي البرنامج شغال منه، ولو غلط مفيش رسالة.',
   'امسح الـ Program بـ <code>glDeleteProgram</code>.'],
   ['ShaderProgramSource source = ParseShader("res/shaders/Basic.shader");', 'unsigned int shader = CreateShader(source.VertexSource, source.FragmentSource);'],
   'المسار غلط: شاشة سودا من غير أي رسالة إن الملف مش موجود.', 'البرنامج 1 (<code>shader_file.cpp</code> + <code>Basic.shader</code>).'),
 card('#c2410c', 'الرياضيات: Cross product', [
   'في 2D: رقم = المساحة بإشارتها = v₁w₂ − v₂w₁.',
   'في 3D: متجه، طوله = المساحة، واتجاهه عمودي على الاتنين (قاعدة الإيد اليمين).',
   'الترتيب بيقلب الإشارة: v × w = −(w × v).'],
   ['cross(v, w) = ( v.y*w.z - v.z*w.y,  v.z*w.x - v.x*w.z,  v.x*w.y - v.y*w.x )'],
   'تنسى السالب في الرقم التاني (اكشفها: الناتج · v لازم = 0).', '<code>cross.cpp</code>.'),
 card('#7c3aed', 'الـ CAD: خط بين نقطتين', [
   'الخطوات: buffer ← bind ← <code>glBufferData</code> ← <code>glDrawArrays</code>.',
   '<code>GL_LINES</code>: كل نقطتين ورا بعض = خط.',
   'الماوس بالبكسل (من فوق)، و OpenGL من ‎-1 لـ +1 (من تحت): حوّل واقلب y.'],
   ['float x = 2.0 * px / width - 1.0;', 'float y = 1.0 - 2.0 * py / height;', 'glDrawArrays(GL_LINES, 0, count);'],
   'تنسى <code>sizeof(float)</code> في <code>glBufferData</code>.', 'البرنامج 2 (<code>click_lines.cpp</code>).'),
]

DAY3_QA = [
 ('البرمجة: References + Hamming', [
   ('بعد <code>int&amp; ref = a; ref = 2;</code> قيمة <code>a</code> كام؟', '2. لأن <code>ref</code> هو <code>a</code> باسم تاني.'),
   ('بعد <code>int&amp; ref = a; ref = b;</code> هل <code>ref</code> بقى بيشاور على <code>b</code>؟', 'لأ. اللي حصل إن قيمة <code>b</code> اتنسخت في <code>a</code>.'),
   ('إيه الفرق بين <code>int&amp; x</code> و <code>&amp;x</code>؟', 'الأولى لازقة في نوع = Reference (اسم تاني). التانية قبل متغير = عنوان.'),
   ('<code>compute("AATG", "AAA")</code> بترجّع كام؟ وليه؟', '‎-1، لأن الطولين مختلفين.'),
   ('في C لو كتبت <code>int distance;</code> من غير <code>= 0</code>، يبدأ بكام؟', 'بأي رقم كان في الذاكرة قبله (garbage). في تجربتنا الإجابة التانية طلعت 7 بدل 0.'),
   ('في الحل التاني، <code>lhs++</code> بتعمل إيه؟', 'بتحرّك الـ Pointer للحرف اللي بعده (زي <code>p++</code> امبارح).')]),
 ('الرسم: الـ Shaders في ملف', [
   ('ليه <code>ss[(int)type]</code> فيها <code>(int)</code>؟', 'لأن <code>enum class</code> مابتتحولش لرقم لوحدها.'),
   ('لو المسار غلط، إيه اللي هيحصل؟', 'مفيش رسالة إن الملف مش موجود. النصين فاضيين، والـ Shaders تفشل، والشاشة سودا.'),
   ('ليه بنضيف <code>\'\\n\'</code> بعد كل سطر؟', 'لأن <code>getline</code> بتشيله، ومن غيره الـ Shader كله يبقى سطر واحد ويفشل.')]),
 ('الرياضيات: Cross product', [
   ('(‎-3, 1) × (2, 1) = ؟', '(‎-3)(1) − (1)(2) = ‎-5.'),
   ('(2, 1) × (‎-3, 1) = ؟', '+5. الترتيب اتعكس فالإشارة اتقلبت.'),
   ('لو v و w في نفس الاتجاه، الضرب الاتجاهي كام؟', 'صفر، لأن مفيش مساحة.')]),
 ('الـ CAD: خط بين نقطتين', [
   ('<code>glDrawArrays(GL_LINES, 0, 5)</code> هترسم كام خط؟', 'خطين. النقطة الخامسة مالهاش شريك.'),
   ('الماوس عند x = 320 في شباك عرضه 640. قيمة x في OpenGL كام؟', '2 × 320 ÷ 640 − 1 = 0 (نص الشاشة).'),
   ('ليه <code>GL_DYNAMIC_DRAW</code> في برنامج الماوس؟', 'لأن النقط بتتغير مع كل دوسة. وهي مجرد تلميح: <code>GL_STATIC_DRAW</code> اشتغلت نفس الشكل.')]),
]
