import sys, re
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d3 import GL_WIN
from specs_d5 import rest, rng
F = '/home/claude/day6/src/'
K = ('key', 'BackSpace')
CL = [(80, 400), (200, 300), (320, 380), (440, 260), (0, 0, 3), (120, 120), (300, 60), (480, 120), (0, 0, 3), K, (150, 200), (400, 200), (500, 330), K, K, (300, 300), (500, 100)]


def programs():
    P = {}
    p1 = F + 'p1_tiny_compiler.cpp'
    s2 = '7,9-13,15-53,195-202'
    s3 = '55-121,204-214,217-223,226-227'
    s4 = '123-154,215-216,224-225,229-231'
    s5 = '156-191,233-234'
    P[p1] = Program('d6_p1', {'tiny_compiler.cpp': p1}, [
        S('الهيكل', 'المكتبات و <code>main</code> فاضية.', {'tiny_compiler.cpp': rest(p1, rng(s2) | rng(s3) | rng(s4) | rng(s5))}),
        S('المرحلة 1: الـ Scanner', 'النص اتحوّل لـ 14 Token. لسه مفيش حساب.', {'tiny_compiler.cpp': s2}),
        S('المرحلة 2: الـ Parser والشجرة', 'الضرب طلع تحت الجمع في الشجرة.', {'tiny_compiler.cpp': s3}),
        S('المرحلة 3: الـ Compiler', 'الشجرة بقت 10 أوامر. لسه محدش نفّذها.', {'tiny_compiler.cpp': s4}),
        S('المرحلة 4: الـ VM', 'الأوامر اتنفذت على الـ Stack، والنتيجة 14.', {'tiny_compiler.cpp': s5})])
    p2 = F + 'p2_leap.cpp'
    P[p2] = Program('d6_p2', {'leap.cpp': p2}, [
        S('الدالة', 'الدالة جاهزة ومحدش بيناديها لسه.', {'leap.cpp': '1-2,4-10,19-20,27-28'}),
        S('الاختبارات', '6 سنين، والـ 6 PASS.', {'leap.cpp': '12-17,21-26'})])
    p3 = F + 'p3_raindrops.cpp'
    P[p3] = Program('d6_p3', {'raindrops.cpp': p3}, [
        S('الدالة', '', {'raindrops.cpp': '1-3,5-20,29-30,38-39'}),
        S('الاختبارات', '7 أرقام، والـ 7 PASS.', {'raindrops.cpp': '22-27,31-37'})])
    m1 = F + 'm1_dot_length.py'
    P[m1] = Program('d6_m1', {'dot_length.py': m1}, [
        S('الدالتين', 'مفيش طباعة لسه.', {'dot_length.py': '1-2,5-9,12-13'}),
        S('أمثلة Khan', '', {'dot_length.py': '16-18,20-22'}),
        S('الطول والعلاقة بالـ dot', '', {'dot_length.py': '24-26,28-29'})], kind='py')
    m2 = F + 'm2_numpy_review.py'
    P[m2] = Program('d6_m2', {'numpy_review.py': m2}, [
        S('نفس الأرقام بـ NumPy', '', {'numpy_review.py': '1-2,4-7'}),
        S('خصائص الضرب النقطي', '', {'numpy_review.py': '9-14'}),
        S('متجه طوله 1', '', {'numpy_review.py': '16-17'})], kind='py')
    r1 = F + 'r1_animated_color.cpp'
    a2, a3, a4 = '128,136', '129,139-143', '125-126,130,145-147'
    P[r1] = Program('d6_r1', {'animated_color.cpp': r1}, [
        S('المستطيل والـ uniform من غير قيمة', 'الـ uniform متعرّف في الـ Shader، ومحدش بعتله قيمة: الافتراضي صفر، فالمستطيل أسود على أسود.', {'animated_color.cpp': rest(r1, rng(a2) | rng(a3) | rng(a4))}),
        S('نبعت لون ثابت', '<code>r</code> = 0: أزرق ثابت.', {'animated_color.cpp': a2}),
        S('نحرّك الأحمر', 'كل فريم <code>r</code> بيتغير 0.05، ويرجع عند 0 و 1. اللقطة دي في لحظة واحدة.', {'animated_color.cpp': a3}),
        S('فحص الاسم وطباعة الأرقام', '', {'animated_color.cpp': a4})], kind='gl', window='Animated Color')
    r2 = F + 'r2_time_colors.cpp'
    b2, b3 = '130,140-141', '131-132,134,144-146'
    P[r2] = Program('d6_r2', {'time_colors.cpp': r2}, [
        S('المستطيل والألوان حسب المكان', 'الـ uniform <code>u_Time</code> لسه صفر، فالألوان حسب المكان بس وثابتة.', {'time_colors.cpp': rest(r2, rng(b2) | rng(b3))}),
        S('نبعت الوقت كل فريم', 'الألوان بقت بتتحرك.', {'time_colors.cpp': b2}),
        S('فحص الاسم وطباعة الوقت', '', {'time_colors.cpp': b3})], kind='gl', window='Time Colors')
    c1 = F + 'c1_refactored.cpp'
    c2, c3 = '66-70,72-73,76-158,213-215', '160-176,211,219'
    P[c1] = Program('d6_c1', {'refactored.cpp': c1}, [
        S('الإعدادات والـ Shaders والشباك', 'الثوابت فوق، والشباك فاضي.', {'refactored.cpp': rest(c1, rng(c2) | rng(c3))}),
        S('البيانات والـ 3 أفعال والـ Callbacks', 'دوسنا نفس الـ 17 دوسة: الرسايل في الـ Terminal زي امبارح بالحرف، بس لسه مفيش رسم.', {'refactored.cpp': c2}),
        S('DrawScene', 'الرسم رجع: نفس صورة امبارح بالظبط.', {'refactored.cpp': c3})],
        kind='gl', window='Refactored', clicks={2: CL, 3: CL})
    return P
