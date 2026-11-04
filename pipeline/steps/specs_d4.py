import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S, MAIN
from specs_d3 import GL_WIN
F = '/home/claude/day4/src/'
SH = '5-10,12-18,20-27,29-31,33,36-46'
SH2 = '6-11,13-19,21-28,30-32,34,37-47'
WIN = '51-55,57-58,60-61,63-64,66-67'
POLY_CLICKS = [(80, 400), (200, 300), (320, 380), (440, 260), (0, 0, 3), (120, 120), (300, 60), (480, 120), (0, 0, 3), (560, 420)]

def programs():
    P = {}
    P[F + 'st1/main.cpp'] = Program('d4_st1', {'static.cpp': F + 'st1/static.cpp', 'main.cpp': F + 'st1/main.cpp'}, [
        S('main.cpp: الهيكل', 'ابدأ بملف <code>main.cpp</code> بس.', {'main.cpp': '1,12,17'}),
        S('main.cpp: متغير ودالة عامين', '', {'main.cpp': '3,5,7,14-15'}),
        S('static.cpp: نفس الأسماء بـ static', 'ضيف ملف تاني للمشروع، فيه نفس الاسمين بس <code>static</code>. الـ Build اشتغل من غير خناقة، والنتيجة ماتغيرتش لأن محدش بينادي حاجة من الملف التاني لسه.',
          {'static.cpp': '1,3,5,7'}, note='الـ compiler هيحذّر إن <code>s_Variable</code> و <code>Function</code> في static.cpp مش مستخدمين. ده طبيعي هنا: هيتستخدموا في الخطوة الجاية.'),
        S('دالة عادية في static.cpp تطبع نسختها', 'دالة من غير <code>static</code>، فـ <code>main.cpp</code> يقدر يناديها بسطر تعريف بس.', {'static.cpp': '10,12-13', 'main.cpp': '10,16'})])
    P[F + 'st2/main.cpp'] = Program('d4_st2', {'static.cpp': F + 'st2/static.cpp', 'main.cpp': F + 'st2/main.cpp'}, [
        S('main.cpp: الهيكل', '', {'main.cpp': '1,5,8'}),
        S('المتغير في ملف، و extern في التاني', '', {'static.cpp': '1', 'main.cpp': '3,7'})])
    P[F + 'c1_const_pointers.cpp'] = Program('d4_c1', {'const_pointers.cpp': F + 'c1_const_pointers.cpp'}, [
        S('الهيكل', MAIN, {'const_pointers.cpp': '1,3,25'}),
        S('متغير const', '', {'const_pointers.cpp': '5-6'}),
        S('Pointer عادي', 'اللي بيتعمل بـ <code>new</code> لازم يترجع بـ <code>delete</code>.', {'const_pointers.cpp': '8-10,23'}),
        S('const قبل النجمة', 'بنحرّك الـ Pointer بس (مسموح).', {'const_pointers.cpp': '12-14'}),
        S('const بعد النجمة', 'بنغيّر المحتوى بس (مسموح).', {'const_pointers.cpp': '16-18,24'}),
        S('const في الحتتين', 'قراية بس.', {'const_pointers.cpp': '20-21'})])
    P[F + 'c2_const_method.cpp'] = Program('d4_c2', {'const_method.cpp': F + 'c2_const_method.cpp'}, [
        S('الهيكل', MAIN, {'const_method.cpp': '1,32,39'}),
        S('الكلاس بـ GetX و SetX', 'مفيش طباعة لسه.', {'const_method.cpp': '3,5-6,9-10,13,16,18,34-35'}),
        S('PrintEntity بـ const&amp;', 'بتشتغل لأن <code>GetX</code> عليها <code>const</code>.', {'const_method.cpp': '27,29,36-37'}),
        S('عدّاد mutable', '', {'const_method.cpp': '7,12,21,23,38'})])
    P[F + 'x1_cross_khan.cpp'] = Program('d4_x1', {'cross_khan.cpp': F + 'x1_cross_khan.cpp'}, [
        S('الهيكل', MAIN, {'cross_khan.cpp': '1,29,36'}),
        S('cross و dot و check + مثال الفيديو', '', {'cross_khan.cpp': '3,5,8,10-12,15,17,20,22-26,31'}),
        S('التمارين', '', {'cross_khan.cpp': '32-35'})])
    P[F + 'e1_rect_arrays.cpp'] = Program('d4_e1', {'rect_arrays.cpp': F + 'e1_rect_arrays.cpp'}, [
        S('المكتبات و main فاضية', '', {'rect_arrays.cpp': '1-3,49,105'}),
        S(*GL_WIN, {'rect_arrays.cpp': WIN + ',95,97,99-100,104'}),
        S('الـ 6 أركان في كارت الشاشة', 'لسه أسود.', {'rect_arrays.cpp': '69-76,78-80,82-85,87-88'}),
        S('الـ Shaders واللون والرسم', '', {'rect_arrays.cpp': SH + ',90-93,98,103'})], kind='gl', window='Rectangle Arrays')
    P[F + 'e2_rect_indices.cpp'] = Program('d4_e2', {'rect_indices.cpp': F + 'e2_rect_indices.cpp'}, [
        S('المكتبات و main فاضية', '', {'rect_indices.cpp': '1-3,49,113'}),
        S(*GL_WIN, {'rect_indices.cpp': WIN + ',103,105,107-108,112'}),
        S('الـ 4 أركان', 'لسه أسود.', {'rect_indices.cpp': '69-74,81-83,85-88,90-91'}),
        S('الترتيب في Index Buffer', 'لسه أسود: مفيش رسم.', {'rect_indices.cpp': '76-79,93-96'}),
        S('الـ Shaders والرسم بـ glDrawElements', '', {'rect_indices.cpp': SH + ',98-101,106,111'})], kind='gl', window='Rectangle Indices')
    P[F + 'v1_two_vaos.cpp'] = Program('d4_v1', {'two_vaos.cpp': F + 'v1_two_vaos.cpp'}, [
        S('المكتبات و main فاضية', '', {'two_vaos.cpp': '1-3,49,126'}),
        S(*GL_WIN, {'two_vaos.cpp': WIN + ',108,110,120-121,125'}),
        S('البيت: بياناته و VAO بتاعه والرسم', '', {'two_vaos.cpp': '69-76,83-90,' + SH + ',104-106,112-114,124'}),
        S('الشمس: VAO تاني', 'نفس الخطوات بأسماء تانية، وفي اللوب bind قبل الرسم.', {'two_vaos.cpp': '78-81,92-99,116-118'}),
        S('فك الـ VAO والـ buffer بعد التجهيز', 'النتيجة ماتغيرتش: ده دليل إن الرسم بيعتمد على الـ bind اللي في اللوب.', {'two_vaos.cpp': '101-102'})], kind='gl', window='Two VAOs')
    P[F + 'v2_polylines.cpp'] = Program('d4_v2', {'polylines.cpp': F + 'v2_polylines.cpp'}, [
        S('المكتبات و main فاضية', '', {'polylines.cpp': '1-3,85,140'}),
        S(*GL_WIN, {'polylines.cpp': '87-91,93-94,96-97,99-100,102-103,123,125,134-135,139'}),
        S('VAO و buffer فاضي والـ Shaders', 'لسه أسود.', {'polylines.cpp': '58,105-107,109-110,112-113,' + SH2 + ',115-117,138'}),
        S('قايمة الخطوط ورسمها', 'كل خط ليه بداية وعدد. القايمة فيها خط واحد فاضي، فمفيش حاجة باينة.', {'polylines.cpp': '4,50,52-53,56-57,120,127-129'}),
        S('دالة الماوس', 'شمال يضيف نقطة، ويمين يبدأ خط جديد. دوسنا فعلاً 4 شمال، يمين، 3 شمال، يمين، شمال.', {'polylines.cpp': '60,62-63,65,67-69,72-79,81-82,121'}),
        S('ارسم النقط', '', {'polylines.cpp': '118,131-132'})], kind='gl', window='Polylines', clicks={5: POLY_CLICKS, 6: POLY_CLICKS})
    return P
