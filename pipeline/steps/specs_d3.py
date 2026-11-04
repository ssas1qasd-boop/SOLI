import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S, MAIN
from specs_d2 import MAINC
F = '/home/claude/day3/src/'
GL_WIN = ('الشباك واللوب', 'GLFW تفتح الشباك، و GLAD تحمّل دوال OpenGL، واللوب يمسح ويعرض كل فريم. لازم تشوف شباك أسود.')
CLICKS = [(100, 380), (300, 120), (380, 400), (560, 300), (520, 80)]

def programs():
    P = {}
    P[F + 'r1_reference.cpp'] = Program('d3_r1', {'reference.cpp': F + 'r1_reference.cpp'}, [
        S('الهيكل', MAIN, {'reference.cpp': '1,3,12'}),
        S('متغير و Reference عليه', 'لسه مفيش طباعة.', {'reference.cpp': '5-6'}),
        S('غيّر من خلال الـ Reference', '', {'reference.cpp': '8-9'}),
        S('قارن العناوين', '', {'reference.cpp': '10-11'})])
    P[F + 'r2_increment.cpp'] = Program('d3_r2', {'increment.cpp': F + 'r2_increment.cpp'}, [
        S('الهيكل', MAIN, {'increment.cpp': '1,18,30'}),
        S('بالنسخة (مش هتشتغل)', 'الدالة فوق <code>main</code>.', {'increment.cpp': '3,5,20,22-23'}),
        S('بالعنوان', '', {'increment.cpp': '8,10,25-26'}),
        S('بالـ Reference', '', {'increment.cpp': '13,15,28-29'})])
    P[F + 'r3_rebind.cpp'] = Program('d3_r3', {'rebind.cpp': F + 'r3_rebind.cpp'}, [
        S('الهيكل', MAIN, {'rebind.cpp': '1,3,17'}),
        S('متغيرين و Reference', '', {'rebind.cpp': '5-6,8'}),
        S('ref = b', 'شوف: <code>a</code> بقى 8.', {'rebind.cpp': '9-10'}),
        S('نفس الفكرة بـ Pointer', 'الـ Pointer يقدر يتنقل لـ <code>b</code>.', {'rebind.cpp': '12-16'})])
    P[F + 'r4_cherno.cpp'] = Program('d3_r4', {'references_cherno.cpp': F + 'r4_cherno.cpp'}, [
        S('الهيكل + LOG', 'الاختصار فوق <code>main</code> عشان كل سطر تحت يستخدمه.', {'references_cherno.cpp': '1,3,10,30'}),
        S('Reference بسيط', '', {'references_cherno.cpp': '12,15-17'}),
        S('دالة بـ Reference', '', {'references_cherno.cpp': '5,7,19-20'}),
        S('الفرق مع Pointer', '', {'references_cherno.cpp': '13,22-24,26-28'})])
    P[F + 'h1_hamming_strlen.c'] = Program('d3_h1', {'hamming_strlen.c': F + 'h1_hamming_strlen.c'}, [
        S('الهيكل', MAINC, {'hamming_strlen.c': '1,21,26'}),
        S('الدالة: ارجع 0 مؤقتاً، وجرّب المثال', 'دالة فاضية بترجّع العدّاد بس، عشان تتأكد إن الندهة شغالة.', {'hamming_strlen.c': '4,11,18,23'}),
        S('اللوب اللي بيعد', 'دلوقتي بيطلّع 7 زي الفيديو.', {'hamming_strlen.c': '2,6,12,14-15,24'}),
        S('التأكد من الطولين', 'من غيرها كان المثال التالت هيقرا برا النص (جربناها في قسم «ليه»).', {'hamming_strlen.c': '7-9,25'})])
    P[F + 'h2_hamming_pointers.c'] = Program('d3_h2', {'hamming_pointers.c': F + 'h2_hamming_pointers.c'}, [
        S('الهيكل', MAINC, {'hamming_pointers.c': '1,18,24'}),
        S('الدالة بالـ Pointers', 'اللوب بيحرّك الـ Pointerين، والسطر الأخير بيكشف الطولين المختلفين بالـ <code>? :</code>.', {'hamming_pointers.c': '3,8-9,11-12,15,20-22'}),
        S('الحماية من NULL', 'من غيرها، المثال الرابع كان هيوقّع البرنامج (جربناها في قسم «ليه»).', {'hamming_pointers.c': '5-6,23'})])
    P[F + 'x1_cross.cpp'] = Program('d3_x1', {'cross.cpp': F + 'x1_cross.cpp'}, [
        S('الهيكل', MAIN, {'cross.cpp': '1,25,36'}),
        S('الضرب الاتجاهي في 2D', '', {'cross.cpp': '8,10,27-29'}),
        S('في 3D', '', {'cross.cpp': '3,5,13,15-17,31-34'}),
        S('التأكيد بالضرب النقطي', '', {'cross.cpp': '20,22,35'})])
    sh = F + 's1_shader_file.cpp'
    P[sh] = Program('d3_s1', {'shader_file.cpp': sh, 'res/shaders/Basic.shader': F + 'res/shaders/Basic.shader'}, [
        S('المكتبات و main فاضية', '', {'shader_file.cpp': '1-3,87,144'}),
        S(*GL_WIN, {'shader_file.cpp': '89-93,95-96,98-99,101-102,104-105,134,136,138-139,143'}),
        S('البيانات', 'لسه أسود.', {'shader_file.cpp': '107-111,113-115,117-120,122-123'}),
        S('ملف الـ Shader و ParseShader', 'اعمل ملف <code>res/shaders/Basic.shader</code>، واكتب <code>ParseShader</code> وجربها بالطباعة بس. الـ Terminal لازم يطلّع النصين متقسمين صح. الشباك لسه أسود.',
          {'shader_file.cpp': '4-6,8,10-11,14,16-18,21,23-26,28,30,32-35,37,39,43,125-129', 'res/shaders/Basic.shader': '1-2,4,6,8,11-12,14,16,18'}),
        S('تجهيز الـ Shaders والرسم', '<code>CompileShader</code> و <code>CreateShader</code> بـ <code>std::string</code>، و <code>glUseProgram</code>، وأمر الرسم. المثلث الأزرق ظهر.',
          {'shader_file.cpp': '46,48-51,53-55,57-64,67,70,72-74,76-79,81-82,84,131-132,137'}),
        S('امسح البرنامج في الآخر', 'بـ <code>glDeleteProgram</code> (التصحيح اللي The Cherno قاله).', {'shader_file.cpp': '142'})], kind='gl', window='Shader File')
    l1 = F + 'l1_line.cpp'
    SH = '5-10,12-18,20-27,29-31,33,36-46'
    P[l1] = Program('d3_l1', {'line.cpp': l1}, [
        S('المكتبات و main فاضية', '', {'line.cpp': '1-3,49,107'}),
        S(*GL_WIN, {'line.cpp': '51-55,57-58,60-61,63-64,66-67,91,93,101-102,106'}),
        S('النقطتين في كارت الشاشة', 'لسه أسود.', {'line.cpp': '69-72,74-76,78-81,83-84'}),
        S('الـ Shaders وارسم الخط', 'لون أبيض من <code>u_Color</code>، و <code>GL_LINES</code>.', {'line.cpp': SH + ',86-88,95-96,105'}),
        S('ارسم النقطتين كمان', 'نفس البيانات، بلون برتقاني و <code>GL_POINTS</code>.', {'line.cpp': '89,98-99'})], kind='gl', window='Line')
    l2 = F + 'l2_click_lines.cpp'
    P[l2] = Program('d3_l2', {'click_lines.cpp': l2}, [
        S('المكتبات و main فاضية', '', {'click_lines.cpp': '1-3,73,127'}),
        S(*GL_WIN, {'click_lines.cpp': '75-79,81-82,84-85,87-88,90-91,109,111,121-122,126'}),
        S('VAO و buffer فاضي', 'الـ buffer برا <code>main</code> عشان دالة الماوس تشوفه بعدين. لسه مفيش بيانات.', {'click_lines.cpp': '51,93-95,97-98,100-101'}),
        S('القايمة والـ Shaders والرسم', 'القايمة <code>points</code> فاضية، فـ <code>count</code> = 0 ومفيش حاجة بتترسم.', {'click_lines.cpp': '4,6-11,13-19,21-28,30-32,34,37-47,50,103-105,113,115-116,125'}),
        S('دالة الماوس', 'كل دوسة: حوّل البكسل، وضيف للقايمة، وابعتها لكارت الشاشة. دوسنا 5 مرات فعلاً: خطين، والنقطة الخامسة لسه لوحدها (مش باينة).', {'click_lines.cpp': '53,55-56,58-61,63-67,69-70,107'}),
        S('ارسم النقط', 'دلوقتي النقطة الخامسة باينة.', {'click_lines.cpp': '106,118-119'})], kind='gl', window='Click Lines', clicks={5: CLICKS, 6: CLICKS})
    return P
