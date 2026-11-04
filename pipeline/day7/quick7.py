import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY7_CARDS = [
 card('#2563eb', 'البرمجة: مراجعة الـ Pointers', [
   'الـ Pointer = رقم فيه عنوان. <code>&amp;var</code> = هات العنوان، و <code>*ptr</code> = روح للعنوان.',
   'النوع (<code>int*</code> أو <code>char*</code>) بيقول للـ compiler هيقرا كام بايت. الحجم نفسه 8 بايت للكل.',
   '<code>new</code> بيحجز على الـ Heap ويرجّع عنوان، و <code>delete[]</code> بيرجّعه مرة واحدة بس.',
   '<code>char**</code> = عنوان Pointer: الدالة تقدر تغيّر الـ Pointer نفسه.'],
   ['int* intPtr = &var;   *intPtr = 10;', 'void MakeText(char** out, int size)'],
   'تبعت قيمة بدل عنوان (<code>Swap(a, b)</code>): الدالة بتغيّر نسخة، والأصل مايتغيرش.', 'البرنامج 1 (<code>pointers_review.cpp</code>) و 2 (<code>pointer_quiz.cpp</code>).'),
 card('#0d9488', 'الرسم: تجربة حرة بالـ Vertex Arrays', [
   'الـ VAO بيفتكر: المدخلات المفعّلة، والـ Layout مع الصندوق، وصندوق الترتيب.',
   'في الـ Core Profile لازم VAO. من غيره الكارت بيرفض (خطأ 1282).',
   '<code>glVertexAttribPointer</code> بيربط الصندوق المربوط <b>دلوقتي</b> بالـ VAO المربوط <b>دلوقتي</b>.',
   'الطريقة 2 (VAO لكل حاجة) = سطر ربط واحد قبل كل رسمة. نفس الصورة بالظبط زي الطريقة 1.'],
   ['glBindVertexArray(vao);', 'glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);'],
   'تفك صندوق الترتيب والـ VAO لسه مربوط: الـ VAO ينساه.', 'البرنامج 1 (<code>vertex_array.cpp</code>) و 2 (<code>two_methods.cpp</code>).'),
 card('#c2410c', 'الرياضيات: اختبر نفسك في الضرب الاتجاهي', [
   'a × b = [a₂b₃ − a₃b₂, a₃b₁ − a₁b₃, a₁b₂ − a₂b₁]: متجه، وفي 3 أبعاد بس.',
   'الناتج عمودي على الاتنين: (a × b) · a = 0.',
   'b × a = ‎−(a × b). ومتجهين على خط واحد ← صفر.',
   'Normal المثلث = (p1 − p0) × (p2 − p0).'],
   ['def cross(a, b): return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]', 'n = np.cross(p1 - p0, p2 - p0)'],
   'تنسى تعكس الصف الأوسط: العنصر التاني يطلع بإشارة غلط.', '<code>cross_quiz.py</code> و <code>numpy_cross.py</code>.'),
 card('#7c3aed', 'الـ CAD: Commit في Git', [
   'Commit = نقطة حفظ (Snapshot) للمشروع كله.',
   'الترتيب: عدّل ← <code>git add .</code> ← <code>git commit -m "رسالة"</code> ← <code>git log --oneline</code>.',
   'سطر اتغير = 1 deletion + 1 insertion.',
   'الـ ID بصمة SHA-1 للمحتوى والاسم والوقت والرسالة: مش عشوائي.'],
   ['git commit -m "make points bigger: 10 -> 12 px"', 'git log --oneline'],
   'تعمل commit من غير add: Git بيقول «nothing added to commit».', 'جلسة Git و <code>commit_id.py</code>.'),
]

DAY7_QA = [
 ('البرمجة: Pointers', [
   ('<code>int var = 8; int* p = &amp;var; *p = 3;</code> قيمة var كام؟', '3.'),
   ('ليه <code>*ptr = 10;</code> مينفعش لو <code>ptr</code> نوعه <code>void*</code>؟', 'الـ compiler مش عارف يكتب كام بايت. لازم نوع زي <code>int*</code>.'),
   ('حجم <code>double*</code> على برنامج 64-bit؟', '8 بايت، زي أي Pointer.'),
   ('دالة عايزة تحجز ذاكرة وترجّع عنوانها في متغير بتاعك. تاخد إيه؟', 'عنوان الـ Pointer: <code>char**</code>، وتنادي <code>MakeText(&amp;text, 4)</code>.'),
   ('إيه اللي يحصل لو عملت <code>delete[]</code> مرتين لنفس العنوان؟', 'البرنامج بيقع (double free).')]),
 ('الرسم: Vertex Arrays', [
   ('الـ VAO بيفتكر الـ Shader؟', 'لأ. بيفتكر المدخلات والـ Layout والصندوق وصندوق الترتيب. الـ Shader بـ <code>glUseProgram</code>.'),
   ('<code>glGetError()</code> رجع 1282. يعني إيه؟', 'GL_INVALID_OPERATION: أمر في وقت غلط، زي ربط Layout من غير VAO في الـ Core Profile.'),
   ('في الطريقة 1 نسيت <code>glVertexAttribPointer</code> قبل رسمة. إيه اللي يترسم؟', 'الرسمة بتقرا بالـ Layout والصندوق القديم: شكل غلط.'),
   ('أنهي طريقة The Cherno بينصح بيها؟', 'VAO لكل حاجة. ولو السرعة مهمة: قيس على جهازك.')]),
 ('الرياضيات: Cross product', [
   ('[1, 0, 0] × [0, 1, 0] = ؟', '[0, 0, 1].'),
   ('[0, 1, 0] × [1, 0, 0] = ؟', '[0, 0, ‎-1].'),
   ('[2, 0, 0] × [0, 0, 3] = ؟', '[0·3 − 0·0, 0·0 − 2·3, 2·0 − 0·0] = [0, ‎-6, 0].'),
   ('[1, 2, 3] × [3, 6, 9] = ؟', '[0, 0, 0] (نفس الخط).')]),
 ('الـ CAD: Git', [
   ('إيه الفرق بين <code>git add</code> و <code>git commit</code>؟', 'add بيحط التغيير في الـ Staging. commit بيعمل نقطة حفظ من اللي في الـ Staging.'),
   ('غيّرت سطر واحد. الـ commit هيقول إيه؟', '1 insertion(+)، 1 deletion(-).'),
   ('ليه الـ ID بتاعك مختلف عن اللي في الملف؟', 'الـ ID بصمة فيها الاسم والوقت، وده مختلف عندك.'),
   ('إزاي تشوف التاريخ في سطر لكل Commit؟', '<code>git log --oneline</code>.')]),
]
