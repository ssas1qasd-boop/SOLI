import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

C_WORDS = [
 W('int main(void)', [('int', 'بترجّع رقم صحيح (0 = تمام)'), ('main', 'نقطة البداية'), ('(void)', 'في C: مش بتاخد مدخلات')],
   'في C++ بنكتب <code>()</code> بس. في C لازم <code>(void)</code> عشان تقول صراحةً «مفيش مدخلات».'),
 W('printf("C was born in %d\\n", year);', [
   ('printf', 'اطبع (print formatted)'), ('(', 'بداية المدخلات'), ('"C was born in ', 'نص هيتطبع زي ما هو'),
   ('%d', 'مكان فاضي لرقم صحيح (d = decimal)'), ('\\n', 'انزل سطر جديد'), ('"', 'نهاية النص'),
   (',', 'وبعد كده…'), ('year', 'القيمة اللي هتتحط مكان %d'), (');', 'نهاية الأمر')],
   'كل <code>%</code> في النص بتاخد قيمة من اللي بعد الفاصلة، بالترتيب. <code>%d</code> = رقم صحيح، و <code>%f</code> = عشري، و <code>%p</code> = عنوان. لو النوع غلط، الطباعة هتبوظ (هتشوفها في التجارب).'),
 W('int* numbers = malloc(count * sizeof(int));', [
   ('int*', 'Pointer لأرقام صحيحة'), ('numbers', 'اسمه'), ('=', 'يساوي'),
   ('malloc', 'memory allocate: احجز ذاكرة'), ('count', '5'), ('*', 'مضروبة في'),
   ('sizeof(int)', 'حجم الـ int بالبايت (4)'), (');', 'نهاية الأمر')],
   '<code>malloc</code> بتحسب بالبايت مش بعدد العناصر، فلازم تضرب العدد في الحجم: 5 × 4 = 20 بايت. (<code>new int[5]</code> في C++ بتحسبها لوحدها)'),
 W('free(numbers);', [('free', 'رجّع الذاكرة'), ('(numbers)', 'العنوان اللي جه من malloc'), (';', 'نهاية الأمر')]),
 W('printf("p = %p   *p = %d\\n", (void*)p, *p);', [
   ('%p', 'مكان لعنوان (pointer)'), ('%d', 'مكان لرقم صحيح'), ('(void*)p', 'العنوان، محوّل لـ void* زي ما %p عايزة'),
   ('*p', 'القيمة اللي على العنوان')]),
 W('p++;', [('p', 'الـ Pointer'), ('++', 'زوّد واحد… بس واحد «int» يعني 4 بايت'), (';', 'نهاية الأمر')],
   'ده «حساب الـ Pointers» اللي الفيديو قال إنه من مميزات C: <code>p + 1</code> = العنصر اللي بعده، مش البايت اللي بعده.'),
 W('void doubleIt(int* number)', [('void', 'مش بترجّع حاجة'), ('doubleIt', 'اسم الدالة'), ('int*', 'بتاخد عنوان رقم'), ('number', 'اسم المدخل')]),
 W('doubleIt(&score);', [('doubleIt', 'نادي الدالة'), ('&score', 'وابعتلها عنوان score مش قيمته'), (';', 'نهاية الأمر')]),
]

VA_WORDS = [
 W('glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 5, (void*)(sizeof(float) * 2));', [
   ('glVertexAttribPointer', 'اشرح لكارت الشاشة إزاي يقرا مدخل'),
   ('1', 'index: رقم المدخل = layout(location = 1)'),
   ('3', 'size: كام رقم (r, g, b) مش كام بايت'),
   ('GL_FLOAT', 'type: كل رقم float (4 بايت)'),
   ('GL_FALSE', 'normalized: ماتحوّلش الأرقام'),
   ('sizeof(float) * 5', 'stride: طول الركن كله = 20 بايت'),
   ('(void*)(sizeof(float) * 2)', 'offset: اللون بيبدأ بعد 8 بايت من أول الركن'),
 ], '<b>الـ stride</b> = تنط قد إيه عشان توصل للركن اللي بعده. <b>الـ offset</b> = جوه الركن الواحد، المدخل ده بيبدأ فين. والـ <code>(void*)</code> لأن آخر مدخل نوعه عنوان؛ رقم عادي زي <code>8</code> مش هيترجم (جربناها).'),
 W('glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 5, 0);', [
   ('0', 'index: المدخل 0 = المكان'), ('2', 'size: رقمين (x, y)'), ('GL_FLOAT', 'type'), ('GL_FALSE', 'normalized'),
   ('sizeof(float) * 5', 'stride: نفس الـ 20 بايت'), ('0', 'offset: المكان في أول الركن')]),
 W('glEnableVertexAttribArray(1);', [('glEnableVertexAttribArray', 'فعّل المدخل'), ('(1)', 'رقم 1')],
   'التفعيل والشرح خطوتين منفصلين، والاتنين لازم. ولو نسيت التفعيل، كارت الشاشة بيستخدم قيمة افتراضية (0, 0, 0) = أسود.'),
 W('layout(location = 0) in vec2 aPosition;', [('layout(location = 0)', 'المدخل رقم 0'), ('in', 'داخل'), ('vec2', 'رقمين'), ('aPosition', 'اسم: a = attribute')]),
 W('gl_Position = vec4(aPosition, 0.0, 1.0);', [('gl_Position', 'مكان الركن على الشاشة'), ('vec4(', 'اعمل 4 أرقام من…'), ('aPosition,', 'الرقمين (x, y)…'), ('0.0,', '…و z = 0…'), ('1.0)', '…و w = 1'), (';', 'نهاية السطر')]),
 W('layout(location = 1) in vec3 aColor;', [('layout(location = 1)', 'المدخل رقم 1'), ('in', 'داخل'), ('vec3', '3 أرقام'), ('aColor', 'لون الركن')]),
 W('out vec3 vertexColor;', [('out', 'طالع للـ Fragment Shader'), ('vec3', '3 أرقام'), ('vertexColor', 'الاسم، ولازم يتكتب بالظبط كده في الناحية التانية')]),
 W('in vec3 vertexColor;', [('in', 'داخل من الـ Vertex Shader'), ('vec3 vertexColor', 'نفس النوع ونفس الاسم بالحرف')],
   'كارت الشاشة مش بيدّي كل بكسل لون ركن واحد؛ بيخلط ألوان الـ 3 أركان حسب قرب البكسل من كل ركن. ده اسمه interpolation، وهو سبب التدرّج.'),
 W('glDrawArrays(GL_TRIANGLES, 0, 3);', [('glDrawArrays', 'ارسم من الـ buffer بالترتيب'), ('GL_TRIANGLES', 'كل 3 أركان = مثلث'), ('0', 'ابدأ من الركن 0'), ('3', 'خد 3 أركان')]),
]

VEC_WORDS = [
 W('std::vector<Vertex> vertices;', [('std::', 'من المكتبة القياسية'), ('vector', 'قايمة بتكبر لوحدها'), ('<Vertex>', 'نوع اللي جواها'), ('vertices', 'اسم القايمة'), (';', 'نهاية السطر')],
   'اللي بين <code>&lt; &gt;</code> بيحدد نوع العناصر: <code>std::vector&lt;int&gt;</code> قايمة أرقام، و <code>std::vector&lt;Point&gt;</code> قايمة نقط.'),
 W('vertices.push_back({ 1, 2, 3 });', [('vertices', 'القايمة'), ('.', 'استخدم حاجة جواها'), ('push_back', 'ضيف في الآخر'), ('{ 1, 2, 3 }', 'نقطة جديدة: x=1, y=2, z=3')]),
 W('for (const Vertex& v : vertices)', [('for (', 'لف'), ('const', 'للقراية بس'), ('Vertex', 'نوع العنصر'), ('&', 'من غير نسخ (Reference)'), ('v', 'اسم العنصر الحالي'), (':', '«في»'), ('vertices)', 'القايمة')],
   'اقراها: «لكل نقطة v في vertices». أسهل وأأمن من اللف بالأرقام.'),
 W('vertices.erase(vertices.begin() + 1);', [('vertices.erase', 'امسح من القايمة'), ('vertices.begin()', 'مكان أول عنصر'), ('+ 1', 'خطوة لقدام = التاني')],
   '<code>erase</code> عايزة «مكان» (iterator) مش رقم. وبعد المسح، العناصر اللي بعده بتتزق مكانه.'),
 W('std::ostream& operator<<(std::ostream& stream, const Vertex& vertex)', [
   ('std::ostream&', 'بترجّع الـ stream نفسه'), ('operator<<', 'إحنا بنعرّف معنى << لنوعنا'),
   ('std::ostream& stream', 'المكان اللي هنكتب فيه (cout)'), ('const Vertex& vertex', 'النقطة اللي هتتطبع')]),
]
