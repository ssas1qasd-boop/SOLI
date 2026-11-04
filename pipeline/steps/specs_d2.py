import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S, MAIN
F = '/home/claude/day2/src/'
MAINC = 'ابدأ بالهيكل: <code>stdio.h</code> و <code>main(void)</code> و <code>return 0</code>. اترجمه وشغّله: لازم يشتغل من غير أخطاء ومن غير ما يطبع حاجة.'

def programs():
    P = {}
    P[F + 'c1_hello.c'] = Program('d2_c1', {'hello.c': F + 'c1_hello.c'}, [
        S('الهيكل', MAINC, {'hello.c': '1,3,8'}),
        S('متغير وطباعته بـ %d', 'كل <code>%d</code> بتاخد قيمة من اللي بعد الفاصلة.', {'hello.c': '5-6'}),
        S('سطر تاني', '', {'hello.c': '7'})])
    P[F + 'c2_malloc.c'] = Program('d2_c2', {'malloc.c': F + 'c2_malloc.c'}, [
        S('الهيكل', MAINC, {'malloc.c': '1,4,18'}),
        S('احجز واتأكد', '<code>malloc</code> محتاجة <code>stdlib.h</code>. ولو رجّعت <code>NULL</code> يبقى الحجز فشل. لسه مفيش طباعة.', {'malloc.c': '2,6-9'}),
        S('املا الأرقام', 'لوب بيحط 0 و 10 و 20 … ولسه مفيش طباعة.', {'malloc.c': '11-12'}),
        S('اطبعهم', '', {'malloc.c': '14-15'}),
        S('رجّع الذاكرة', 'النتيجة نفسها، بس من غير تسريب ذاكرة.', {'malloc.c': '17'})])
    P[F + 'c3_ptr_arith.c'] = Program('d2_c3', {'pointer_arithmetic.c': F + 'c3_ptr_arith.c'}, [
        S('الهيكل', MAINC, {'pointer_arithmetic.c': '1,3,13'}),
        S('المصفوفة و Pointer على أولها', 'اسم المصفوفة لوحده = عنوان أول عنصر.', {'pointer_arithmetic.c': '5-6'}),
        S('اطبع وحرّك', 'كل لفة: اطبع العنوان والقيمة، وبعدين <code>p++</code>.', {'pointer_arithmetic.c': '8,10-11'})])
    P[F + 'c4_double_it.cpp'] = Program('d2_c4', {'double_it.cpp': F + 'c4_double_it.cpp'}, [
        S('الهيكل', MAIN, {'double_it.cpp': '1,8,14'}),
        S('المتغير وطباعته', '', {'double_it.cpp': '10-11'}),
        S('الدالة وندهتها', 'الدالة فوق <code>main</code>، وبتاخد العنوان. وابعتلها <code>&amp;score</code>.', {'double_it.cpp': '3,5,12-13'})])
    P[F + 'd1_dot_length.cpp'] = Program('d2_dot', {'dot_length.cpp': F + 'd1_dot_length.cpp'}, [
        S('الهيكل', MAIN, {'dot_length.cpp': '1,17,30'}),
        S('الضرب النقطي + مثال 2D', '', {'dot_length.cpp': '4,6-9,19-21'}),
        S('مثال 3D', '', {'dot_length.cpp': '23-25'}),
        S('الطول', 'دالة <code>length</code> = جذر الضرب النقطي في نفسه (محتاجة <code>cmath</code>).', {'dot_length.cpp': '2,12,14,27-29'})])
    P[F + 'v1_basics.cpp'] = Program('d2_v1', {'vector_basics.cpp': F + 'v1_basics.cpp'}, [
        S('الهيكل', MAIN, {'vector_basics.cpp': '1,9,22'}),
        S('الـ struct وقايمة فاضية', 'محتاج <code>#include &lt;vector&gt;</code>.', {'vector_basics.cpp': '2,4,6,11-12'}),
        S('ضيف 3 نقط', '', {'vector_basics.cpp': '14-17,19'}),
        S('اقرا منها', '', {'vector_basics.cpp': '20-21'})])
    P[F + 'v2_loops.cpp'] = Program('d2_v2', {'vector_loops.cpp': F + 'v2_loops.cpp'}, [
        S('الهيكل', MAIN, {'vector_loops.cpp': '1,9,23'}),
        S('قايمة فيها نقطتين', '', {'vector_loops.cpp': '2,4,6,11'}),
        S('لوب بالرقم', '', {'vector_loops.cpp': '13-14'}),
        S('لوب على كل عنصر', '', {'vector_loops.cpp': '16-17'}),
        S('لوب بيعدّل', 'من غير <code>&amp;</code> التعديل هيروح لنسخة.', {'vector_loops.cpp': '19-20,22'})])
    P[F + 'v3_full.cpp'] = Program('d2_v3', {'vector_full.cpp': F + 'v3_full.cpp'}, [
        S('الهيكل', MAIN, {'vector_full.cpp': '1,15,31'}),
        S('الـ struct وتعليم cout يطبعه', 'دالة <code>operator&lt;&lt;</code> فوق <code>main</code>.', {'vector_full.cpp': '2,4,6,9,11-12'}),
        S('ضيف واطبع', '', {'vector_full.cpp': '17-19,21-22'}),
        S('امسح التاني', '', {'vector_full.cpp': '24-27'}),
        S('امسح الكل', '', {'vector_full.cpp': '29-30'})])
    P[F + 'v4_cad_points.cpp'] = Program('d2_v4', {'cad_points.cpp': F + 'v4_cad_points.cpp'}, [
        S('الهيكل', MAIN, {'cad_points.cpp': '1,21,31'}),
        S('Point وقايمة', '', {'cad_points.cpp': '2,4,6,23'}),
        S('دالة الإضافة', 'بـ <code>&amp;</code> عشان تضيف للقايمة الأصلية. لسه مفيش طباعة.', {'cad_points.cpp': '9,11,24-26'}),
        S('دالة الطباعة', 'بـ <code>const&amp;</code>: من غير نسخ ومن غير تعديل.', {'cad_points.cpp': '14,16-18,27'}),
        S('امسح آخر نقطة', '', {'cad_points.cpp': '29-30'})])
    P[F + 'v5_growth.cpp'] = Program('d2_v5', {'vector_growth.cpp': F + 'v5_growth.cpp'}, [
        S('الهيكل', MAIN, {'vector_growth.cpp': '1,4,19'}),
        S('ضيف 9 أرقام واطبع size و capacity', '', {'vector_growth.cpp': '2,6,9,11,13,16'}),
        S('اكتشف النقل', 'قارن عنوان البيانات بالعنوان اللي فات.', {'vector_growth.cpp': '7,12,14-15,17'})])
    W = 'vertex_attributes'
    GL_WIN = ('الشباك واللوب', 'GLFW تفتح الشباك، و GLAD تحمّل دوال OpenGL، واللوب يمسح ويعرض كل فريم. لازم تشوف شباك أسود.')
    P[F + 'va1_positions.cpp'] = Program('d2_va1', {'triangle_positions.cpp': F + 'va1_positions.cpp'}, [
        S('المكتبات و main فاضية', 'اترجم بس عشان تتأكد من التركيب.', {'triangle_positions.cpp': '1-3,48,99'}),
        S(*GL_WIN, {'triangle_positions.cpp': '50-54,56-57,59-60,62-63,65-66,89,91,93-94,98'}),
        S('البيانات والمدخل 0', 'الأركان، والـ VAO والـ buffer، و <code>glVertexAttribPointer</code>. لسه أسود: مفيش Shader ولا رسم.', {'triangle_positions.cpp': '68-72,74-76,78-81,83-84'}),
        S('الـ Shaders وأمر الرسم', 'المثلث البرتقاني ظهر.', {'triangle_positions.cpp': '5-10,12-17,19-26,28-30,32,35-45,86-87,92,97'})], kind='gl', window='Vertex Attributes')
    P[F + 'va2_colors.cpp'] = Program('d2_va2', {'triangle_colors.cpp': F + 'va2_colors.cpp'}, [
        S('المكتبات و main فاضية', '', {'triangle_colors.cpp': '1-3,52,106'}),
        S(*GL_WIN, {'triangle_colors.cpp': '54-58,60-61,63-64,66-67,69-70,96,98,100-101,105'}),
        S('البيانات (5 أرقام لكل ركن) والمدخل 0', 'لاحظ الـ stride بقى <code>sizeof(float) * 5</code>. لسه أسود.', {'triangle_colors.cpp': '72-76,78-80,82-85,87-88'}),
        S('الـ Shaders وأمر الرسم', 'الشاشة لسه سودا! المثلث اترسم، بس المدخل 1 (اللون) لسه مش متفعّل، فـ <code>aColor</code> بياخد قيمته الافتراضية (0, 0, 0) = أسود.', {'triangle_colors.cpp': '5-13,15-21,23-30,32-34,36,39-49,93-94,99,104'}),
        S('فعّل المدخل 1 (اللون)', 'الـ offset بعد رقمين = 8 بايت. الألوان ظهرت واتمزجت.', {'triangle_colors.cpp': '90-91'})], kind='gl', window='Vertex Attributes')
    return P
