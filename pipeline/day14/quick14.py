import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY14_CARDS = [
 card('#2563eb', 'البرمجة: النسخ و Copy Constructor', [
   '<code>=</code> بينسخ دايماً: القيمة مع int و struct، والعنوان مع Pointer.',
   'الافتراضي Shallow Copy: الـ Pointers جوه الـ class بتتنسخ عناوين.',
   'Copy Constructor <code>T(const T&amp; other)</code> يعمل Deep Copy.',
   'ابعت الـ objects بـ <code>const T&amp;</code>، أو امنع النسخ بـ <code>= delete</code>.'],
   ['String(const String& other) { ... new char[...]; memcpy(...); }', 'void Print(const String& string);'],
   'class فيه new من غير Copy Constructor: نسختين بيمسحوا نفس الـ Buffer (double free).', '<code>copy_basics.cpp</code> و <code>string.cpp</code>.'),
 card('#0d9488', 'الرسم: Texture class والنسخ', [
   'الـ Texture class بيعمل glDeleteTextures في الـ Destructor.',
   'نسخه بالقيمة = نسخة بنفس id، ولما تموت تمسح الأصلي.',
   'glIsTexture بتقولك الرقم لسه موجود ولا لأ.',
   'الحل: <code>const Texture&amp;</code> و <code>Texture(const Texture&amp;) = delete;</code>.'],
   ['void Describe(const Texture& texture);', 'Texture(const Texture& other) = delete;'],
   'Bind لـ id اتمسح: GL_INVALID_OPERATION من غير رسالة، والقديم بيفضل مربوط.', '<code>texture_copy.cpp</code> و <code>texture_ref.cpp</code>.'),
 card('#c2410c', 'الرياضيات: الصورة والعكس', [
   'الـ Image = الشكل بعد التحويل. المربع الوحدة بيبقى متوازي أضلاع.',
   'المساحة بتتضرب في |det|.',
   'العكس لـ 2 × 2: [[d, ‎-b], [‎-c, a]] ÷ (ad - bc).',
   'det = 0: الشكل بيتكبس، ومفيش عكس (Singular).'],
   ['np.linalg.inv(A)      # [[0.5, -0.5], [0, 1]]', 'np.linalg.solve(A, [5, 3])   # [1, 3]'],
   'تعكس مصفوفة det بتاعها 0: inf أو LinAlgError.', '<code>image_area.py</code> و <code>inverse.py</code>.'),
 card('#7c3aed', 'الـ CAD: Git', [
   'Git = نظام بيسجل التغييرات وترجع لأي نسخة (Version Control).',
   'add (Staging) ثم commit (لقطة).',
   'status و diff و log عشان تشوف.',
   'كل محتوى باسمه (SHA-1): المتشابه بيتخزن مرة.'],
   ['git add site.css && git commit -m "v1: blue"', 'git checkout 372ae88 -- site.css'],
   'تنسى git add لملف جديد: الـ commit فاضي، ومفيش حاجة ترجعلها.', '<code>git_record.py</code> و <code>git_store.py</code>.'),
]

DAY14_QA = [
 ('البرمجة: النسخ', [
   ('<code>Vector2* pb = pa; pb->x = 5;</code>. pa->x = ؟', '5: نفس الـ object.'),
   ('إمتى الـ Copy Constructor بيتنادى؟', '<code>T b = a;</code>، أو لما تبعت T بالقيمة لدالة (أو ترجّعه بالقيمة).'),
   ('ليه البرنامج وقع من غير Copy Constructor؟', 'الاتنين مسكوا نفس m_Buffer، والـ Destructor اتنادى مرتين: double free.'),
   ('إزاي تمنع النسخ؟', '<code>T(const T&amp;) = delete;</code>')]),
 ('الرسم: Texture class', [
   ('Describe(Texture t): إيه اللي حصل لـ id 2؟', 'النسخة ماتت ومسحته: glIsTexture = 0.'),
   ('ليه الأزرق اترسم أحمر؟', 'Bind(2) فشل (GL_INVALID_OPERATION)، فالأحمر فضل مربوط.'),
   ('الحل الأسهل؟', '<code>const Texture&amp;</code>.')]),
 ('الرياضيات: الصورة والعكس', [
   ('A = [[3, 0], [0, 2]]: مساحة المربع الوحدة بعدها؟', '6 = det.'),
   ('عكس [[2, 0], [0, 4]]؟', '[[0.5, 0], [0, 0.25]].'),
   ('[[1, 2], [2, 4]] ليها عكس؟', 'لأ: det = 0.'),
   ('A x = b. إزاي تحل في NumPy؟', '<code>np.linalg.solve(A, b)</code>.')]),
 ('الـ CAD: Git', [
   ('ملف جديد. status بيقول إيه؟', '<code>??</code> (Untracked).'),
   ('الفرق بين add و commit؟', 'add بيحط في الـ Staging، و commit بيسجل اللقطة.'),
   ('ترجع ملف لأول نسخة إزاي؟', '<code>git checkout &lt;أول commit&gt; -- الملف</code>.'),
   ('ملفين بنفس المحتوى: git بيخزنهم كام مرة؟', 'مرة واحدة: نفس البصمة.')]),
]
