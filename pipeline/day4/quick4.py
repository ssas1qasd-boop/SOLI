import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY4_CARDS = [
 card('#2563eb', 'البرمجة: Static و Const', [
   '<code>static</code> برا الكلاس = الاسم ده للملف ده بس (الـ Linker مش شايفه).',
   '<code>extern</code> = «المتغير ده في ملف تاني».',
   '<code>const</code> قبل النجمة = المحتوى ثابت. بعد النجمة = الـ Pointer ثابت.',
   '<code>const</code> بعد اسم الدالة = مش هتغيّر حاجة في الكلاس، و <code>mutable</code> استثناء.'],
   ['static int s_Variable = 5;     // only this file', 'const int* p;   int* const q;', 'int GetX() const { return m_X; }'],
   'اسمين عامين زي بعض في ملفين = خطأ Linker (multiple definition).', 'البرنامج 3 (<code>const_pointers.cpp</code>).'),
 card('#0d9488', 'الرسم: Index Buffer (EBO)', [
   'اكتب كل ركن مرة واحدة، وقول بالأرقام مين بيعمل كل مثلث.',
   'نوع الـ buffer: <code>GL_ELEMENT_ARRAY_BUFFER</code>، والرسم: <code>glDrawElements</code>.',
   'العدد = عدد الـ indices، والنوع لازم unsigned.'],
   ['unsigned int indices[6] = { 0, 1, 2,  2, 3, 0 };', 'glBufferData(GL_ELEMENT_ARRAY_BUFFER, 6 * sizeof(unsigned int), indices, GL_STATIC_DRAW);', 'glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);'],
   '<code>GL_INT</code> بدل <code>GL_UNSIGNED_INT</code>: شاشة سودا من غير رسالة.', 'البرنامج 2 (<code>rect_indices.cpp</code>).'),
 card('#c2410c', 'الرياضيات: Cross product (Khan)', [
   'موجود في 3D بس، والناتج متجه.',
   'كل صف: اتجاهل رقمه واضرب الباقي على الصليب. الصف الأوسط معكوس.',
   'الناتج · a = 0 والناتج · b = 0 (طريقة تتأكد بيها).'],
   ['a x b = [ a2*b3 - a3*b2,  a3*b1 - a1*b3,  a1*b2 - a2*b1 ]', '[1,-7,1] x [5,2,4] = [-30, 1, 37]'],
   'تنسى تعكس الصف الأوسط.', '<code>cross_khan.cpp</code>.'),
 card('#7c3aed', 'الـ CAD: VAO وعدة خطوط', [
   'الـ VAO = دفتر بيفتكر الـ buffer وإعداداته. bind واحد قبل الرسم.',
   'في الـ Core Profile لازم VAO (من غيره: أسود و 1282).',
   '<code>GL_LINE_STRIP</code> = خط متصل، ولكل خط بداية وعدد.'],
   ['glBindVertexArray(houseVao);  glDrawArrays(GL_LINES, 0, 12);', 'glDrawArrays(GL_LINE_STRIP, line.first, line.count);'],
   'تنسى bind الـ VAO الصح قبل الرسمة: الشكل يترسم من بيانات شكل تاني.', 'البرنامج 4 (<code>polylines.cpp</code>).'),
]

DAY4_QA = [
 ('البرمجة: Static و Const', [
   ('ملفين فيهم <code>int x = 1;</code> برا أي دالة. هيحصل إيه؟', 'خطأ من الـ Linker: multiple definition. الحل: <code>static</code> في واحد منهم، أو <code>extern</code>.'),
   ('<code>extern int x;</code> بتعمل إيه؟', 'بتقول إن <code>x</code> موجود في ملف تاني، من غير ما تحجز مكان.'),
   ('في <code>const int* p</code>، ينفع <code>p = &amp;y</code>؟ وينفع <code>*p = 3</code>؟', 'الأولى أيوه (الـ Pointer يتحرك)، والتانية لأ (المحتوى ثابت).'),
   ('ليه <code>GetX</code> لازم تبقى <code>const</code> عشان <code>PrintEntity(const Entity&amp; e)</code> تشتغل؟', 'لأن <code>e</code> ثابت، فمسموح تنادي عليه الدوال اللي وعدت إنها مش هتغيّر بس.')]),
 ('الرسم: Index Buffer', [
   ('مستطيل بالـ Index Buffer: كام ركن وكام index؟', '4 أركان و 6 indices.'),
   ('الرقم 6 في <code>glDrawElements(GL_TRIANGLES, 6, …)</code> معناه إيه؟', 'عدد الـ indices اللي هتتقري (مش عدد الأركان).'),
   ('إيه اللي يحصل لو كتبت <code>GL_INT</code>؟', 'شاشة سودا من غير رسالة، و <code>glGetError</code> = 1280.')]),
 ('الرياضيات: Cross product', [
   ('[1, 0, 0] × [0, 1, 0] = ؟', '[0, 0, 1].'),
   ('[2, 3, 4] × [5, 6, 7] = ؟', '[3×7 − 4×6, 4×5 − 2×7, 2×6 − 3×5] = [‎-3, 6, ‎-3].'),
   ('إزاي تتأكد إن ناتجك صح من غير ما تعيد الحساب؟', 'اضربه نقطياً في a وفي b: لازم الاتنين = 0.')]),
 ('الـ CAD: VAO وعدة خطوط', [
   ('الـ VAO بيفتكر إيه؟', 'الـ buffer المربوط لكل خانة، وإعدادات <code>glVertexAttribPointer</code>، والخانات المفعّلة، والـ Index Buffer.'),
   ('5 نقط بـ <code>GL_LINE_STRIP</code> = كام خط؟', '4 خطوط متصلة.'),
   ('ليه البرنامج وقع لما شيلنا <code>polylines.push_back({ 0, 0 })</code>؟', 'لأن <code>back()</code> اتنادت على قايمة فاضية.')]),
]
