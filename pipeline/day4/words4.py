import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

STATIC_WORDS = [
 W('static int s_Variable = 5;', [('static', 'للملف ده بس (Internal Linkage)'), ('int', 'رقم صحيح'), ('s_Variable', 'الاسم (s_ = static، عادة The Cherno)'), ('= 5;', 'قيمته')],
   'برا أي كلاس، <code>static</code> معناها: الـ Linker مش هيشوف الاسم ده من ملفات تانية. كأنه <code>private</code> للملف.'),
 W('extern int s_Variable;', [('extern', 'مش هنا: دوّر عليه في ملف تاني (External Linkage)'), ('int', 'نوعه'), ('s_Variable', 'اسمه'), (';', 'من غير قيمة: ده تعريف بس')],
   'السطر ده مابيعملش صندوق. بيقول للـ compiler «صدّقني، موجود»، والـ Linker هو اللي هيدوّر عليه بعدين.'),
]

LINK_TABLE = '''<table class="types"><tr><th>الكلمة</th><th>اسمها</th><th>الـ Linker</th></tr>
<tr><td>(ولا حاجة)</td><td>External Linkage</td><td>بيشوفه من كل الملفات</td></tr>
<tr><td><code>static</code></td><td>Internal Linkage</td><td>بيشوفه في الملف ده بس</td></tr>
<tr><td><code>extern</code></td><td>تعريف بس</td><td>«دوّر عليه في ملف تاني»</td></tr></table>'''

CONST_WORDS = [
 W('const int* b = a;', [('const int', 'الـ int اللي هناك ثابت'), ('*', 'عنوان'), ('b', 'اسمه'), ('= a;', 'يشاور على نفس اللي a بيشاور عليه')],
   'اقراها من اليمين للشمال: «b عنوان لـ int ثابت». يعني المحتوى ممنوع يتغيّر من خلال <code>b</code>، بس <code>b</code> نفسه يتحرك عادي.'),
 W('int* const c = new int(5);', [('int*', 'عنوان لـ int'), ('const', 'الـ Pointer نفسه ثابت'), ('c', 'اسمه'), ('= new int(5);', 'رقم جديد جواه 5')],
   'من اليمين للشمال: «c ثابت، وهو عنوان لـ int». يعني <code>c</code> مايتحركش، بس المحتوى يتغيّر.'),
 W('int GetX() const', [('int', 'بترجّع رقم'), ('GetX', 'اسمها'), ('()', 'مفيش مدخلات'), ('const', 'وعد: مش هغيّر حاجة في الكلاس')],
   'الدالة دي بس هي اللي ينفع تتنادي على Entity جاي بـ <code>const&amp;</code>.'),
 W('void PrintEntity(const Entity& e)', [('const', 'مش هغيّره'), ('Entity&', 'Reference (من غير نسخ)'), ('e', 'اسمه جوه الدالة')],
   'ده Reference امبارح + <code>const</code> النهارده: أسرع طريقة تبعت بيها حاجة كبيرة لدالة بتقرا بس.'),
]

CONST_TABLE = '''<table class="types"><tr><th>الشكل</th><th>اقراه (من اليمين)</th><th>تغيّر المحتوى (<code>*p = 2</code>)؟</th><th>تحرّك الـ Pointer (<code>p = …</code>)؟</th></tr>
<tr><td><code>int* p</code></td><td>عنوان لـ int</td><td>✓</td><td>✓</td></tr>
<tr><td><code>const int* p</code></td><td>عنوان لـ int ثابت</td><td>✗</td><td>✓</td></tr>
<tr><td><code>int* const p</code></td><td>ثابت، عنوان لـ int</td><td>✓</td><td>✗</td></tr>
<tr><td><code>const int* const p</code></td><td>ثابت، عنوان لـ int ثابت</td><td>✗</td><td>✗</td></tr></table>
<div class="ok"><b>قاعدة The Cherno:</b> <code>const</code> <b>قبل</b> النجمة = المحتوى ثابت. <code>const</code> <b>بعد</b> النجمة = الـ Pointer ثابت. (و <code>int const*</code> = <code>const int*</code> بالظبط.)</div>'''

EBO_WORDS = [
 W('unsigned int indices[6] = {', [('unsigned', 'موجب بس (من غير سالب)'), ('int', 'رقم صحيح (4 بايت)'), ('indices', 'جمع index: أرقام الأركان'), ('[6]', '6 أرقام = مثلثين')],
   'كل رقم هنا مش مكان، ده <b>رقم ركن</b> من مصفوفة <code>positions</code>.'),
 W('glBufferData(GL_ELEMENT_ARRAY_BUFFER, 6 * sizeof(unsigned int), indices, GL_STATIC_DRAW);', [
   ('GL_ELEMENT_ARRAY_BUFFER', 'نوع الـ buffer: أرقام ترتيب (Index Buffer)'), ('6 * sizeof(unsigned int)', '6 × 4 = 24 بايت'),
   ('indices', 'عنوان المصفوفة'), ('GL_STATIC_DRAW', 'مش هتتغير')]),
 W('glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);', [
   ('glDrawElements', 'ارسم بالترتيب (Elements = indices)'), ('GL_TRIANGLES', 'كل 3 = مثلث'), ('6', 'عدد الـ indices (مش الأركان)'),
   ('GL_UNSIGNED_INT', 'نوع أرقام الترتيب'), ('nullptr', 'من أول الـ IBO المربوط')],
   'الـ <code>GL_UNSIGNED_INT</code> لازم يطابق نوع المصفوفة (<code>unsigned int</code>). The Cherno حذّر: <code>GL_INT</code> = شاشة سودا من غير رسالة.'),
]

VAO_WORDS = [
 W('glBindVertexArray(houseVao);', [('glBindVertexArray', 'شغّل «دفتر» إعدادات'), ('houseVao', 'دفتر البيت')],
   'وقت التجهيز: أي <code>glVertexAttribPointer</code> بعده بيتسجل في الدفتر ده، ومعاه الـ buffer المربوط ساعتها. وقت الرسم: سطر واحد بيرجّع كل الإعدادات دي.'),
 W('glDrawArrays(GL_LINE_STRIP, line.first, line.count);', [('GL_LINE_STRIP', 'خط متصل: كل نقطة بتتوصل باللي بعدها'), ('line.first', 'ابدأ من النقطة رقم كذا'), ('line.count', 'وارسم العدد ده')],
   'الخط المتصل بـ n نقطة = n − 1 قطعة. وكل الخطوط المتصلة في نفس الـ buffer، بس كل واحد ليه بداية وعدد.'),
]

MODES_TABLE = '''<table class="types"><tr><th>النوع</th><th>5 نقط بتتحوّل لـ</th></tr>
<tr><td><code>GL_POINTS</code></td><td>5 نقط</td></tr><tr><td><code>GL_LINES</code></td><td>خطين (0-1، 2-3)، والنقطة 4 لوحدها</td></tr>
<tr><td><code>GL_LINE_STRIP</code></td><td>4 خطوط متصلة (0-1-2-3-4)</td></tr><tr><td><code>GL_LINE_LOOP</code></td><td>5 خطوط: زي الـ strip + خط من الآخر للأول</td></tr></table>'''
