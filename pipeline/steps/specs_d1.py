import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
F = '/home/claude/day1/full/'
S = lambda title, why, lines, note=None: dict(title=title, why=why, lines=lines, note=note)
MAIN = 'ابدأ دايماً بالهيكل: المكتبة، و <code>main</code> فاضية، و <code>std::cin.get()</code> عشان الشباك الأسود مايقفلش. اعمل Run: لازم يشتغل من غير أخطاء قبل ما تزوّد أي حاجة.'

def programs():
    P = {}
    P[F + 'p/p1.cpp'] = Program('d1_p1', {'p1.cpp': F + 'p/p1.cpp'}, [
        S('الهيكل', MAIN, {'p1.cpp': '1,4,12'}),
        S('Pointer فاضي بالرقم 0', 'أبسط طريقة: صفر. واطبعه على طول عشان تتأكد.', {'p1.cpp': '6,9'}),
        S('بـ NULL', 'محتاج مكتبة <code>cstddef</code> عشان <code>NULL</code> متعرّف فيها.', {'p1.cpp': '2,7,10'}),
        S('بـ nullptr', 'الطريقة الحديثة في C++، ومش محتاجة مكتبة.', {'p1.cpp': '8,11'})])
    P[F + 'p/p2.cpp'] = Program('d1_p2', {'p2.cpp': F + 'p/p2.cpp'}, [
        S('الهيكل', MAIN, {'p2.cpp': '1,3,10'}),
        S('متغير عادي', 'اعمل المتغير واطبع قيمته.', {'p2.cpp': '5,7'}),
        S('اطبع عنوانه', 'علامة <code>&amp;</code> قبل الاسم = العنوان.', {'p2.cpp': '8'}),
        S('خزّن العنوان في Pointer', 'نفس الرقم بالظبط، بس المرة دي متشال في متغير.', {'p2.cpp': '6,9'})])
    P[F + 'p/p3.cpp'] = Program('d1_p3', {'p3.cpp': F + 'p/p3.cpp'}, [
        S('الهيكل', MAIN, {'p3.cpp': '1,3,12'}),
        S('Pointer عادي من نوع int', '', {'p3.cpp': '5-6,8'}),
        S('نفس العنوان بنوع double', 'الـ cast <code>(double*)</code> لازم هنا، من غيرها الـ compiler يرفض (جربناها).', {'p3.cpp': '7,9'}),
        S('الفرق الحقيقي: الحجم', 'اطبع حجم كل نوع عشان تشوف ليه النوع مهم.', {'p3.cpp': '10-11'})])
    P[F + 'p/p4.cpp'] = Program('d1_p4', {'p4.cpp': F + 'p/p4.cpp'}, [
        S('الهيكل', MAIN, {'p4.cpp': '1,3,10'}),
        S('المتغير وقيمته', '', {'p4.cpp': '5,7'}),
        S('Pointer عليه', 'لسه مفيش تغيير في الشاشة: إحنا شايلين العنوان بس.', {'p4.cpp': '6'}),
        S('غيّر من خلال العنوان', 'النجمة قبل الاسم = روح هناك. واطبع <code>var</code> تاني عشان تشوف التغيير.', {'p4.cpp': '8-9'})])
    P[F + 'p/p5.cpp'] = Program('d1_p5', {'p5.cpp': F + 'p/p5.cpp'}, [
        S('الهيكل', MAIN, {'p5.cpp': '1,4,13'}),
        S('احجز 8 بايت', 'اطبع العنوان: هتلاحظ إنه مختلف عن عناوين الـ Stack (بيبدأ بـ 0x55 مش 0x7ff).', {'p5.cpp': '6,8'}),
        S('صفّرهم واطبعهم', '<code>memset</code> محتاجة مكتبة <code>cstring</code>.', {'p5.cpp': '2,7,9-11'}),
        S('رجّع الذاكرة', 'آخر سطر قبل الخروج: كل <code>new[]</code> ليها <code>delete[]</code>. النتيجة مش هتتغير، بس البرنامج بقى نضيف.', {'p5.cpp': '12'})])
    P[F + 'p/p6.cpp'] = Program('d1_p6', {'p6.cpp': F + 'p/p6.cpp'}, [
        S('الهيكل', MAIN, {'p6.cpp': '1,4,15'}),
        S('الـ buffer زي الكود اللي فات', 'مفيش طباعة لسه.', {'p6.cpp': '2,6-7,14'}),
        S('Pointer لـ Pointer', 'اطبع <code>ptr</code> و <code>&amp;buffer</code>: لازم يطلعوا زي بعض.', {'p6.cpp': '8-10'}),
        S('نجمة واحدة', '<code>*ptr</code> لازم = <code>buffer</code>.', {'p6.cpp': '11-12'}),
        S('نجمتين (بالأقواس)', 'وصلنا للبيانات نفسها.', {'p6.cpp': '13'})])
    P[F + '3_dot/main.cpp'] = Program('d1_dot', {'dot.cpp': F + '3_dot/main.cpp'}, [
        S('الهيكل', MAIN, {'dot.cpp': '1,12,27'}),
        S('دالة الضرب النقطي + أول مثال', 'اكتب الدالة فوق <code>main</code>، وجربها على مثال الفيديو الأول.', {'dot.cpp': '4,6-9,14-16'}),
        S('مثال 4 أبعاد', 'نفس الدالة، بس <code>n = 4</code>.', {'dot.cpp': '18-20'}),
        S('نفس الحساب بـ GLM', 'ضيف مكتبة GLM واستخدم <code>glm::dot</code> عشان تشوف الإشارات.', {'dot.cpp': '2,22-25'})])
    u1 = F + 'u/u1.cpp'
    GL_WIN = ('الشباك واللوب', 'GLFW تفتح الشباك، و GLAD تحمّل دوال OpenGL، واللوب يمسح ويعرض كل فريم. لازم تشوف شباك أسود. لو ماظهرش، المشكلة في التركيب مش في الكود.')
    GL_DATA = ('البيانات في كارت الشاشة', 'الأركان والترتيب، والـ VAO والـ VBO والـ IBO. الشاشة لسه سودا: البيانات وصلت، بس مفيش Shader ولا أمر رسم.')
    P[u1] = Program('d1_u1', {'uniform_fixed.cpp': u1}, [
        S('المكتبات و main فاضية', 'اترجم بس عشان تتأكد إن GLFW و GLAD متركبين صح. مفيش شباك لسه.', {'uniform_fixed.cpp': '1-3,49,118'}),
        S(*GL_WIN, {'uniform_fixed.cpp': '51-55,57-58,60-61,63-64,66-67,106,108,112-113,117'}),
        S(*GL_DATA, {'uniform_fixed.cpp': '69-78,80-82,84-87,89-90,92-95'}),
        S('الـ Shaders وأمر الرسم', 'الـ Shaderين ودوال تجهيزهم فوق <code>main</code>، و <code>glUseProgram</code>، و <code>glDrawElements</code> في اللوب. الشاشة لسه سودا! المربع اترسم فعلاً، بس <code>u_Color</code> لسه ماحدش ملاه، فقيمته صفر = أسود على أسود.', {'uniform_fixed.cpp': '5-10,12-18,20-27,29-31,33,36-46,97-98,110,116'}),
        S('املا الـ Uniform', 'هات رقم الخانة وابعت اللون كل فريم: المربع ظهر أزرق.', {'uniform_fixed.cpp': '100-101,109'}),
        S('جرّب اسم غلط', 'سطرين زيادة بيوروك إيه اللي يحصل لو كتبت الاسم غلط: الرقم ‎-1.', {'uniform_fixed.cpp': '103-104'})], kind='gl', window='Uniforms')
    u2 = F + 'u/u2.cpp'
    P[u2] = Program('d1_u2', {'uniform_animation.cpp': u2}, [
        S('المكتبات و main فاضية', 'نفس أول خطوة في البرنامج 1.', {'uniform_animation.cpp': '1-3,49,124'}),
        S(*GL_WIN, {'uniform_animation.cpp': '51-55,57-58,60-61,63-64,66-67,106,108,118-119,123'}),
        S(*GL_DATA, {'uniform_animation.cpp': '69-78,80-82,84-87,89-90,92-95'}),
        S('الـ Shaders وأمر الرسم', 'زي البرنامج 1: اترسم بس أسود، لأن <code>u_Color</code> لسه صفر.', {'uniform_animation.cpp': '5-10,12-18,20-27,29-31,33,36-46,97-98,110,122'}),
        S('الـ Uniform بمتغير r', 'بدل رقم ثابت للأحمر، متغير <code>r</code> بيبدأ بصفر. لسه مابيتحركش.', {'uniform_animation.cpp': '100-101,103,109'}),
        S('حرّك r كل فريم', 'زوّد <code>r</code> شوية كل فريم، ولما يوصل 1 ارجع. اللون بيتغير وإنت بتتفرج (الصورة لحظة واحدة منه).', {'uniform_animation.cpp': '104,112-116'})], kind='gl', window='Uniforms')
    C = F + '4_camera/'
    files = {f: C + f for f in ['shaderClass.h', 'shaderClass.cpp', 'Camera.h', 'Camera.cpp', 'main.cpp']}
    P[C + 'main.cpp'] = Program('d1_cam', files, [
        S('main.cpp: المكتبات والمقاس', 'ابدأ بملف <code>main.cpp</code> بس. الملفات التانية لسه مش موجودة.', {'main.cpp': '1-2,6-7,58,119'}),
        S('main.cpp: الشباك واللوب', 'شباك 800×800 بلون أزرق غامق. <code>gladLoadGL</code> و <code>glViewport</code> نفس فكرة كل يوم.', {'main.cpp': '60-63,65-66,68-69,71-73,97,99-100,109-110,117-118'}),
        S('كلاس الـ Shader (ملفين جداد)', 'اعمل <code>shaderClass.h</code> و <code>shaderClass.cpp</code>، وفي <code>main.cpp</code> اكتب نصوص الـ Shaders واعمل <code>Shader</code> وشغّله. الشباك لسه فاضي: مفيش أشكال.',
          {'shaderClass.h': '1-2,4,6,8-12,15', 'shaderClass.cpp': '1,3,5-7,9-11,13-16,18-19,22,24,27,29', 'main.cpp': '3,9-18,20-26,75,101,116'}),
        S('الهرم: البيانات والرسم', 'الأركان والألوان والترتيب، والـ buffers، وأمر الرسم. الشاشة لسه فاضية! لأن <code>camMatrix</code> لسه ماحدش ملاها، فكل الأركان بتتضرب في صفر وتقع في نقطة واحدة.',
          {'main.cpp': '28-46,48-56,77-80,82-86,88-91,106-107,113-115'}),
        S('الكاميرا: المكان والمصفوفة', 'اعمل <code>Camera.h</code> و <code>Camera.cpp</code> بالـ constructor و <code>Matrix</code> بس، ونادي <code>Matrix</code> كل فريم. الهرم ظهر! وشغّلنا <code>glEnable(GL_DEPTH_TEST)</code> عشان الوشوش اللي ورا ماتغطيش اللي قدام.',
          {'Camera.h': '1-8,13,15,17-20,22-23,25-26,30,32,36', 'Camera.cpp': '1,3,5-7,10,12-13,15-16,18', 'main.cpp': '4,93,95,104'}),
        S('الكاميرا: الكيبورد والماوس', 'ضيف <code>Inputs</code> (والمكتبات اللي محتاجاها للف)، ونادِيها كل فريم. الصورة هي هي لحد ما تدوس زرار: جرّب W و A و S و D والماوس.',
          {'Camera.h': '9-11,28,33', 'Camera.cpp': '21,23-38,40,42,44,46-47,50-52,54-55,57,59-60,62,64,66,68-69', 'main.cpp': '103'})], kind='gl', window='Camera')
    return P
