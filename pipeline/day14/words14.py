import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

COPY_WORDS = [
 W('Vector2* pb = pa;', [('Vector2* pb', 'Pointer جديد'), ('= pa', 'انسخ العنوان (8 بايت) بس')],
   'The Cherno: «= بينسخ دايماً». مع int و struct بينسخ القيمة، ومع Pointer بينسخ العنوان، فالاتنين بيشاوروا على نفس المكان (pa == pb: yes).'),
 W('String(const String& other)', [('String(', 'Constructor'), ('const String& other', 'الـ String اللي بنتنسخ منه (Reference عشان مايتنسخش هو كمان)')],
   'لو ماكتبناهوش، C++ بيكتب واحد لوحده بينسخ كل Member زي ما هو (Shallow Copy): m_Buffer نفس العنوان. جربناه: Cherno بقت Charno هي كمان، والبرنامج وقع بـ double free.'),
 W('memcpy(m_Buffer, other.m_Buffer, m_Size + 1);', [('m_Buffer', 'الـ Buffer الجديد بتاعنا (اتحجز في السطر اللي قبله)'), ('other.m_Buffer', 'بتاع الأصل'), ('m_Size + 1', 'الحروف + الصفر')],
   'ده الـ Deep Copy: نسخة من المحتوى نفسه في مكان جديد. وكل String بيمسح الـ Buffer بتاعه بس.'),
 W('void PrintByReference(const String& string)', [('const', 'مش هغيّره'), ('String&', 'Reference: نفس الـ object من غير نسخ')],
   'The Cherno: «دايماً ابعت الـ objects بـ const reference إلا لو محتاج نسخة». في التشغيل: Copied! عدد 3 مرات (نسخة مقصودة + 2 بالقيمة)، وبالـ Reference صفر.'),
]

COPY_TABLE = '''<table class="types"><tr><th>نسخ</th><th>بيتنسخ إيه</th><th>من التشغيل</th></tr>
<tr><td><code>int b = a;</code></td><td>الرقم</td><td>a لسه 2</td></tr>
<tr><td><code>Vector2 vb = va;</code></td><td>الـ 8 بايت كلهم</td><td>va.x لسه 2، وعنوان تاني</td></tr>
<tr><td><code>Vector2* pb = pa;</code></td><td>العنوان بس</td><td>pa->x بقى 5 (pa == pb)</td></tr>
<tr><td>String من غير Copy Constructor</td><td>m_Buffer (العنوان)</td><td>Charno / Charno، و double free</td></tr>
<tr><td>String مع Deep Copy</td><td>الحروف في Buffer جديد</td><td>Cherno / Charno</td></tr>
<tr><td><code>const String&amp;</code></td><td>ولا حاجة</td><td>مفيش Copied!</td></tr></table>'''

TEX_WORDS = [
 W('void Describe(Texture texture)', [('Texture texture', 'نسخة (الـ Copy Constructor الافتراضي: id نفسه)'), ('}', 'النسخة بتموت: ~Texture يمسح id 2')],
   'نفس مشكلة الـ String، بس على الكارت: النسخة ماسكة نفس الرقم، ولما ماتت مسحت الـ Texture الأصلي. glIsTexture بقت 0، والأزرق اترسم أحمر.'),
 W('Texture(const Texture& other) = delete;', [('= delete', 'الدالة دي ممنوعة')],
   'لو حد كتب <code>Texture copy = blue;</code> أو بعت Texture بالقيمة: خطأ في الترجمة بدل باظ وقت التشغيل. ده اللي learnopengl وكتب كتير بيعملوه في class بيمسك حاجة على الكارت.'),
]

TEX_TABLE = '''<table class="types"><tr><th></th><th>texture_copy.cpp</th><th>texture_ref.cpp</th></tr>
<tr><td>Describe بتاخد</td><td><code>Texture</code> (نسخة)</td><td><code>const Texture&amp;</code></td></tr>
<tr><td>~Texture اشتغل كام مرة لـ id 2</td><td>2 (النسخة + الأصل)</td><td>1</td></tr>
<tr><td>glIsTexture(blue.id) بعد Describe</td><td>0</td><td>1</td></tr>
<tr><td>Bind id 2</td><td>GL_INVALID_OPERATION (1282)</td><td>تمام</td></tr>
<tr><td>الشباك</td><td>أحمر وأحمر</td><td>أحمر وأزرق</td></tr></table>'''

MAT_WORDS = [
 W('return 0.5 * abs(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))', [('np.roll(y, -1)', 'y للركن اللي بعده'), ('x * … - … * y', 'xᵢ yᵢ₊₁ - xᵢ₊₁ yᵢ'), ('0.5 * abs(np.sum(…))', 'نص القيمة المطلقة للمجموع')],
   'اسمها Shoelace (رباط الجزمة). الأركان لازم تبقى بالترتيب حوالين الشكل. جربنا ترتيب غلط: المساحة طلعت 0.'),
 W('inverse = np.array([[d, -b], [-c, a]]) / det + 0.0', [('[[d, -b], [-c, a]]', 'بدّل وقلب الإشارة'), ('/ det', 'اقسم على ad - bc')],
   'Khan: التحويل له عكس لو كل نتيجة جاية من نقطة واحدة. ده بيحصل لما det ≠ 0. مع det = 0 الحساب بيقسم على صفر (جربناه: inf).'),
]

MAT_TABLE = '''<table class="types"><tr><th></th><th>A = [[2, 1], [0, 1]]</th><th>B = [[1, 2], [2, 4]]</th></tr>
<tr><td>صورة المربع</td><td>متوازي أضلاع</td><td>خط</td></tr>
<tr><td>المساحة (من التشغيل)</td><td>2</td><td>0</td></tr>
<tr><td>det</td><td>2</td><td>0</td></tr>
<tr><td>العكس</td><td>[[0.5, ‎-0.5], [0, 1]]</td><td>Singular matrix</td></tr>
<tr><td>A x = (5, 3)</td><td>x = (1, 3)</td><td>(2, 0) و (0, 1) بيروحوا لنفس المكان</td></tr></table>'''

GIT_WORDS = [
 W('git("add", "site.css")', [('git add', 'جهّز الملف للـ Commit (Staging)'), ('git commit', 'سجّل لقطة'), ('git status', 'إيه اللي اتغيّر')],
   'git-scm (Recording Changes): كل ملف يا Untracked (??)، يا Modified (M)، يا Staged (A)، يا Committed. الـ Commit بياخد اللي في الـ Staging بس: جربنا من غير add: «does not have any commits yet».'),
 W('print(git("init", "-q", "-b", "main") or "git init: empty repository made")', [('git init', 'اعمل .git'), ('-b main', 'اسم الفرع')],
   'Net Ninja: بدل فولدرات V1 و V2 و V3، فولدر واحد فيه .git شايل كل النسخ (Revision History).'),
 W('by_hand = hashlib.sha1(header + content).hexdigest()', [('header', '"blob 22" + صفر'), ('sha1', 'بصمة 40 حرف'), ('hexdigest', 'بالـ Hex')],
   'git بيسمّي كل محتوى ببصمته. نفس المحتوى = نفس البصمة = يتخزن مرة واحدة. عشان كده 25 تعديل مابيملوش الهارد زي قصة Net Ninja.'),
]

GIT_TABLE = '''<table class="types"><tr><th>الأمر</th><th>بيعمل إيه</th><th>من التشغيل</th></tr>
<tr><td><code>git init</code></td><td>Repository جديد</td><td>empty repository</td></tr>
<tr><td><code>git status --short</code></td><td>حالة الملفات</td><td>?? ثم A ثم M</td></tr>
<tr><td><code>git add</code></td><td>للـ Staging</td><td>A  site.css</td></tr>
<tr><td><code>git commit -m</code></td><td>لقطة برسالة</td><td>4 commits</td></tr>
<tr><td><code>git diff</code></td><td>الفرق</td><td>‎-blue +pink</td></tr>
<tr><td><code>git log --oneline</code></td><td>السجل</td><td>c03766c v4 … 372ae88 v1</td></tr>
<tr><td><code>git checkout &lt;commit&gt; -- file</code></td><td>رجّع ملف لنسخة قديمة</td><td>رجع أزرق</td></tr></table>'''
