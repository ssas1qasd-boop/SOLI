import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY5_CARDS = [
 card('#2563eb', 'البرمجة: swap بالـ Pointers', [
   'الدالة لو استلمت <b>قيمة</b>، بتشتغل على نسخة، والأصل مايتغيرش.',
   'ابعت <b>العنوان</b> بـ <code>&amp;x</code>، واستلمه في <code>int* a</code>، واكتب فيه بـ <code>*a = ...</code>.',
   '<code>temp</code> لازم، وإلا القيمة الأولى تضيع.'],
   ['void swap(int* a, int* b) { int temp = *a; *a = *b; *b = temp; }', 'swap(&x, &y);'],
   'تنادي <code>swap(x, y)</code> من غير <code>&amp;</code>، أو تنسى سطر التعريف لما الدالة تحت <code>main</code>.', 'البرنامج 1 (<code>swap_pointers.cpp</code>).'),
 card('#0d9488', 'الرسم: تعديل الـ Shader', [
   'الـ Shader نص بيتترجم وقت التشغيل، فافحص الترجمة واطبع الرسالة.',
   'Vertex = مرة لكل ركن ولازم يكتب <code>gl_Position</code>. Fragment = مرة لكل بكسل ولازم يطلّع لون.',
   'تبعت من الـ Vertex للـ Fragment بـ <code>out</code> و <code>in</code> بنفس الاسم والنوع.',
   'الألوان من 0.0 لـ 1.0.'],
   ['"    gl_Position = vec4(position.x * 1.5, position.y * 1.5, 0.0, 1.0);\\n"', '"    color = vec4(v_Position.x + 0.5, v_Position.y + 0.5, 0.2, 1.0);\\n"'],
   'تنسى <code>;</code> جوه الـ Shader: البرنامج يشتغل عادي وتطلع ألوان غلط، والرسالة بس هي اللي بتقولك.', 'البرنامج 2 (<code>shader_edit.cpp</code>).'),
 card('#c2410c', 'الرياضيات: dot و cross في NumPy', [
   '<code>np.array</code> = أرقام جنب بعض في الذاكرة، والحساب على كلها مرة واحدة.',
   '<code>np.dot(a, b)</code> = رقم، و <code>np.cross(a, b)</code> = متجه عمودي (3D بس).',
   '<code>c = a</code> مش نسخة. استخدم <code>a.copy()</code>.'],
   ['np.dot([1, -7, 1], [5, 2, 4])     # -5', 'np.cross([1, -7, 1], [5, 2, 4])   # [-30, 1, 37]'],
   'تضرب List عادية في 2: بتتكرر بدل ما تتضرب.', '<code>dot_cross.py</code>.'),
 card('#7c3aed', 'الـ CAD: مسح آخر خط', [
   '<code>push_back</code> بيضيف في الآخر، و <code>pop_back</code> بيمسح الآخر.',
   'الـ Backspace بيمسح الخط من <code>polylines</code> ونقطه من <code>points</code> (عدد النقط × 2).',
   'بعد المسح ابدأ خط فاضي جديد، وابعت النقط للكارت.'],
   ['Polyline last = polylines.back(); polylines.pop_back();', 'for (int i = 0; i < last.count * 2; i++) points.pop_back();'],
   '<code>pop_back</code> على قايمة فاضية: البرنامج يقع.', 'البرنامج 2 (<code>delete_last_line.cpp</code>).'),
]

DAY5_QA = [
 ('البرمجة: swap بالـ Pointers', [
   ('لو الدالة <code>void swap(int a, int b)</code>، إيه اللي هيحصل لـ x و y؟', 'ولا حاجة: الدالة بدّلت نسخ.'),
   ('في <code>void swap(int* a, int* b)</code>، إيه الفرق بين <code>a</code> و <code>*a</code>؟', '<code>a</code> = العنوان، و <code>*a</code> = القيمة اللي في العنوان.'),
   ('ليه <code>temp</code>؟', 'لأن <code>*a = *b</code> بيمسح قيمة <code>x</code> القديمة، فلازم تتشال الأول.'),
   ('ليه SwapReference رجّعت x و y زي الأول في البرنامج 2؟', 'لأنهم كانوا اتبدلوا بالـ Pointer قبلها، فاتبدلوا تاني.')]),
 ('الرسم: تعديل الـ Shader', [
   ('الـ Vertex Shader بيشتغل كام مرة في المثلث؟ والـ Fragment؟', 'الـ Vertex 3 مرات، والـ Fragment مرة لكل بكسل جوه المثلث.'),
   ('إزاي الـ Fragment يعرف مكان البكسل؟', 'الـ Vertex يكتبه في <code>out vec4 v_Position</code>، والـ Fragment يقراه من <code>in vec4 v_Position</code>.'),
   ('عايز المثلث أخضر. تغيّر إيه؟', '<code>color = vec4(0.0, 1.0, 0.0, 1.0);</code>'),
   ('<code>GL_INFO_LOG_LENGTH</code> بتديك إيه؟', 'طول رسالة الخطأ، عشان تحجز مكان بالظبط.')]),
 ('الرياضيات: NumPy', [
   ('<code>np.dot([1, 2, 3], [4, 5, 6])</code> = ؟', '4 + 10 + 18 = 32.'),
   ('<code>np.cross([1, 0, 0], [0, 1, 0])</code> = ؟', '[0, 0, 1]، يعني z.'),
   ('<code>b.shape</code> لمصفوفة صفين و 3 أعمدة؟', '<code>(2, 3)</code>.'),
   ('إزاي تجيب العمود 1 كله من <code>b</code>؟', '<code>b[:, 1]</code>.')]),
 ('الـ CAD: مسح آخر خط', [
   ('القايمة [A, B, C]. بعد <code>push_back(D)</code> ثم <code>pop_back()</code> مرتين؟', '[A, B].'),
   ('خط فيه 4 نقط. كام مرة <code>points.pop_back()</code> عشان نمسحه؟', '8 مرات (كل نقطة x و y).'),
   ('ليه بنتخطى الخط اللي <code>count</code> بتاعه صفر؟', 'لأنه الخط الجديد الفاضي اللي اتعمل بعد الدوس يمين، والمستخدم عايز يمسح اللي قبله.')]),
]
