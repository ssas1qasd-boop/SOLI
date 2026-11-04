import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

CLASS_WORDS = [
 W('class Player', [('class', 'كلمة بتعرّف نوع جديد بتاعنا'), ('Player', 'اسم النوع (بحرف كبير عادةً)'), ('{ … };', 'جوه الأقواس اللي جواه، وفي الآخر <code>;</code> إجباري')],
   'الكلاس قالب، زي «استمارة فاضية». مفيش رام اتحجز لحد ما نعمل Object منه (<code>Player player;</code>).'),
 W('Player player;', [('Player', 'النوع: الكلاس اللي عملناه'), ('player', 'اسم الـ Object (نسخة حقيقية)')],
   'نفس <code>int x;</code> بالظبط: نوع واسم. والـ Object بياخد مكان في الرام قد مجموع متغيراته (12 بايت هنا).'),
 W('void Move(int xa, int ya)', [('void', 'مش بترجّع حاجة'), ('Move', 'اسم الـ Method'), ('int xa, int ya', 'الاتجاه: يمين/شمال وفوق/تحت')],
   'الـ Method = دالة جوه الكلاس. بتشوف متغيرات الكلاس على طول (x و y و speed) من غير ما نبعتهم.'),
 W('x += xa * speed;', [('x', 'x بتاع الـ Object اللي اتنادت عليه الدالة'), ('+=', 'زوّد على القيمة القديمة'), ('xa * speed', 'الاتجاه × السرعة')],
   'لو ندهنا <code>enemy.Move(…)</code>، نفس السطر بيغيّر x بتاع enemy. الـ compiler بيعرف مين من <code>this</code>.'),
 W('player.Move(1, -1);', [('player', 'الـ Object'), ('.', 'جوه'), ('Move', 'الـ Method'), ('(1, -1)', 'يمين 1، وتحت 1')],
   'بالظبط زي <code>Move(player, 1, -1)</code> اللي برّه، بس الكلاس بيبعت player لوحده في السر.'),
 W('void Move(Player& player, int xa, int ya)', [('Player&', 'Reference لـ Player: الأصل مش نسخة'), ('player', 'اسمه جوه الدالة'), ('int xa, int ya', 'الاتجاه')],
   'من غير <code>&amp;</code> الدالة بتاخد نسخة، والتغيير بيضيع (جربناها تحت).'),
 W('if (n > 0)', [('n', 'الرقم اللي اتبعت لـ Add'), ('> 0', 'أكبر من صفر')],
   'ده سبب الـ <code>private</code>: الكلاس بيتحكم في بياناته. محدش يقدر يكتب <code>count = -100</code> من برّه.'),
 W('std::cout << "inside Where(): this = " << this << std::endl;', [('this', 'عنوان الـ Object اللي الدالة اتنادت عليه'), ('std::cout <<', 'اطبعه')],
   '<code>this</code> نوعه <code>Counter*</code>. و <code>count</code> جوه أي Method معناها <code>this-&gt;count</code>.'),
]

CLASS_TABLE = '''<table class="types"><tr><th>الكلمة</th><th>معناها</th><th>في البرنامج</th></tr>
<tr><td>Class</td><td>قالب (نوع جديد) بيجمع بيانات + دوال</td><td><code>class Player { … };</code></td></tr>
<tr><td>Object / Instance</td><td>نسخة حقيقية من الكلاس، ليها مكان في الرام</td><td><code>Player player;</code></td></tr>
<tr><td>Member</td><td>متغير جوه الكلاس</td><td><code>int x, y;</code></td></tr>
<tr><td>Method</td><td>دالة جوه الكلاس</td><td><code>void Move(int xa, int ya)</code></td></tr>
<tr><td><code>public</code></td><td>ينفع نوصله من برّه</td><td><code>player.x = 5;</code> شغال</td></tr>
<tr><td><code>private</code> (الافتراضي)</td><td>من جوه الكلاس بس</td><td><code>clicks.count = 3;</code> خطأ ترجمة</td></tr>
<tr><td><code>this</code></td><td>عنوان الـ Object جوه الـ Method</td><td>= <code>&amp;clicks</code></td></tr></table>'''

TEX_WORDS = [
 W('#define STB_IMAGE_IMPLEMENTATION', [('#define', 'عرّف اسم للـ Preprocessor (قبل الترجمة)'), ('STB_IMAGE_IMPLEMENTATION', 'الاسم اللي stb_image.h بيدوّر عليه')],
   'الملف <code>stb_image.h</code> لو الاسم ده متعرّف قبله، بيحط كود الدوال كله. ولو مش متعرّف، بيحط التعريفات بس. لو حطيته في ملفين هيطلع خطأ «multiple definition».'),
 W('float positions[16] = {', [('float', 'أرقام عشرية'), ('positions', 'الاسم'), ('[16]', '4 أركان × 4 أرقام')],
   'كل ركن دلوقتي فيه حاجتين: مكانه على الشاشة (x, y)، والنقطة اللي يقرا منها في الصورة (u, v) من 0 لـ 1.'),
 W('stbi_set_flip_vertically_on_load(1);', [('stbi_', 'دوال مكتبة stb_image'), ('set_flip_vertically', 'اقلب الصورة فوق-تحت'), ('on_load', 'وإنت بتقراها'), ('1', 'أيوه')],
   'الصورة في الملف أول صف فيها = فوق. لكن إحداثيات الـ Texture في OpenGL (0, 0) = تحت شمال. من غير القلب السهم بيطلع مقلوب (جربناها).'),
 W('unsigned char* pixels = stbi_load(path.c_str(), &width, &height, &channels, 4);', [('unsigned char*', 'عنوان بايتات (كل بايت من 0 لـ 255)'), ('path.c_str()', 'اسم الملف كنص C'), ('&width, &height', 'عناوين: الدالة هتكتب فيهم المقاس'), ('&channels', 'هتكتب فيه قنوات الملف'), ('4', 'رجّعهالي RGBA دايماً')],
   'زي Pointers الأسبوع اللي فات: الدالة عايزة ترجّع 4 حاجات، فبترجّع واحدة وبتكتب التلاتة التانيين من خلال عناوينهم.'),
 W('glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);', [('glTexParameteri', 'اضبط إعداد في الـ Texture المربوطة (i = رقم صحيح)'), ('GL_TEXTURE_2D', 'الـ Texture المربوطة كصورة 2D'), ('GL_TEXTURE_MIN_FILTER', 'الإعداد: لما الصورة تتصغّر'), ('GL_LINEAR', 'القيمة: اخلط أقرب 4 بكسلات')],
   'القيمة الافتراضية للتصغير بتستخدم Mipmaps (نسخ أصغر من الصورة) واحنا ماعملناهاش، فالـ Texture بتعتبر ناقصة وبتطلع سودا. عشان كده The Cherno بيقول الـ 4 إعدادات إجبارية.'),
 W('glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels);', [('GL_TEXTURE_2D', 'الـ Texture المربوطة'), ('0', 'المستوى 0 (الصورة الأصلية، مش Mipmap)'), ('GL_RGBA8', 'إزاي تتخزن في الكارت: 4 قنوات × 8 bit'), ('width, height', 'المقاس'), ('0', 'لازم صفر (border)'), ('GL_RGBA, GL_UNSIGNED_BYTE', 'شكل البايتات اللي باعتينها'), ('pixels', 'العنوان في الرام')],
   'زي <code>glBufferData</code>: الكارت بياخد نسخة. بعدها نقدر نمسح البكسلات من الرام.'),
 W('glActiveTexture(GL_TEXTURE0 + slot);', [('glActiveTexture', 'اختار الخانة الشغالة'), ('GL_TEXTURE0', 'الخانة 0'), ('+ slot', 'زوّد رقم الخانة')],
   'أي <code>glBindTexture</code> بعده بيحط الـ Texture في الخانة دي. على الكمبيوتر غالباً 32 خانة، وعلى الموبايل 8.'),
 W('glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 4, (const void*)(sizeof(float) * 2));', [('1', 'المدخل رقم 1 (texCoord)'), ('2', 'رقمين (u, v)'), ('sizeof(float) * 4', 'الركن كله 16 بايت (stride)'), ('(const void*)(sizeof(float) * 2)', 'المدخل ده بيبدأ بعد 8 بايت من أول الركن (offset)')],
   'الـ offset لازم يتكتب كعنوان (<code>const void*</code>) عشان الدالة قديمة. بس هو رقم بايتات عادي.'),
 W('"out vec2 v_TexCoord;\\n"', [('out', 'طالع من الـ Vertex Shader'), ('vec2', 'رقمين'), ('v_TexCoord', 'الاسم (v_ = varying، يعني بيتغير من بكسل لبكسل)')],
   'الكارت بيحسب قيمة لكل بكسل بين الأركان (Interpolation): بكسل في نص المربع بياخد (0.5, 0.5).'),
 W('"uniform sampler2D u_Texture;\\n"', [('uniform', 'قيمة جاية من الـ CPU'), ('sampler2D', 'نوع: «قارئ صورة 2D»'), ('u_Texture', 'الاسم')],
   'الـ CPU بيبعتله <b>رقم الخانة</b> بـ <code>glUniform1i</code>، مش رقم الـ Texture.'),
 W('"    color = texture(u_Texture, v_TexCoord);\\n"', [('texture( , )', 'دالة GLSL: هات اللون من الصورة'), ('u_Texture', 'من أنهي خانة'), ('v_TexCoord', 'عند أنهي إحداثيات')],
   'الإعدادات (LINEAR أو NEAREST، و REPEAT أو CLAMP) بتأثر هنا: هي اللي بتقرر اللون لو الإحداثي بين بكسلين أو برّه 0..1.'),
 W('glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);', [('GL_SRC_ALPHA', 'لون الصورة × شفافيتها'), ('GL_ONE_MINUS_SRC_ALPHA', 'اللي ورا × (1 − شفافيتها)')],
   'بكسل شفافيته 0: يفضل اللي ورا. بكسل 1: يغطي. من غير <code>glEnable(GL_BLEND)</code> الشفاف بيطلع بلونه الحقيقي (أسود).'),
 W('glUniform1i(location, 0);', [('glUniform1i', 'ابعت رقم صحيح واحد'), ('location', 'خانة u_Texture'), ('0', 'رقم الخانة (Slot)')],
   'لازم يساوي الرقم في <code>texture.Bind(0)</code>. لو بعتنا 1 والخانة 1 فاضية: أسود (جربناها).'),
 W('unsigned int sharp = MakeTexture(pixels, 4, GL_NEAREST, GL_REPEAT);', [('GL_NEAREST', 'خد أقرب بكسل: مربعات حادة'), ('GL_REPEAT', 'برّه 0..1: كرر الصورة'), ('4', 'المقاس 4 × 4')],
   'عكسها: <code>GL_LINEAR</code> (خلط ناعم) و <code>GL_CLAMP_TO_EDGE</code> (مد آخر بكسل). الصورة تحت بتوري الأربعة.'),
]

TEX_TABLE = '''<table class="types"><tr><th>الخطوة</th><th>الأمر</th><th>زي إيه من اللي فات</th></tr>
<tr><td>1. اقرا الصورة للرام</td><td><code>stbi_load</code></td><td>المصفوفة <code>positions</code> في الرام</td></tr>
<tr><td>2. اعمل Texture واربطها</td><td><code>glGenTextures</code> + <code>glBindTexture</code></td><td><code>glGenBuffers</code> + <code>glBindBuffer</code></td></tr>
<tr><td>3. الإعدادات الأربعة</td><td><code>glTexParameteri</code> × 4</td><td>جديد</td></tr>
<tr><td>4. ابعت البكسلات للكارت</td><td><code>glTexImage2D</code></td><td><code>glBufferData</code></td></tr>
<tr><td>5. حطها في خانة</td><td><code>glActiveTexture</code> + <code>glBindTexture</code></td><td>جديد (الخانات)</td></tr>
<tr><td>6. قول للـ Shader الخانة</td><td><code>glUniform1i</code></td><td><code>glUniform4f</code> بتاع اللون</td></tr>
<tr><td>7. إحداثيات لكل ركن</td><td>مدخل رقم 1 (texCoord)</td><td>مدخل اللون في اليوم 2</td></tr></table>'''

MAT_WORDS = [
 W('col1 = [M[0][0], M[1][0]]', [('M[0][0]', 'الصف 0، العمود 0'), ('M[1][0]', 'الصف 1، العمود 0'), ('col1', 'العمود الأول = فين î راح')],
   'المصفوفة مكتوبة صف صف في Python، لكن 3Blue1Brown بيقرأها عمود عمود. لو أخدنا الصف بدل العمود، كل النتايج تطلع غلط (جربناها).'),
 W('return [x * col1[0] + y * col2[0], x * col1[1] + y * col2[1]]', [('x * col1', 'x مرة من î الجديد'), ('y * col2', 'y مرة من ĵ الجديد'), ('+', 'اجمعهم')],
   'ده تعريف ضرب المصفوفة في متجه: v = x î + y ĵ، فبعد التحويل v′ = x î′ + y ĵ′.'),
 W('print("M @ v =", M @ v)', [('@', 'ضرب مصفوفات في NumPy'), ('M @ v', 'المصفوفة × المتجه')],
   '<code>M * v</code> (نجمة) في NumPy حاجة تانية: بتضرب كل رقم في اللي قصاده. للتحويل لازم <code>@</code>.'),
 W('print("columns of M:", M[:, 0], M[:, 1])', [(':', 'كل الصفوف'), ('0', 'العمود 0')],
   'كده بنطلّع î′ و ĵ′ من المصفوفة مباشرة.'),
]

MAT_TABLE = '''<table class="types"><tr><th>التحويل</th><th>î بيروح</th><th>ĵ بيروح</th><th>المصفوفة (صف صف)</th></tr>
<tr><td>مثال الفيديو</td><td>(1, ‎-2)</td><td>(3, 0)</td><td>[[1, 3], [‎-2, 0]]</td></tr>
<tr><td>دوران 90° عكس عقارب الساعة</td><td>(0, 1)</td><td>(‎-1, 0)</td><td>[[0, ‎-1], [1, 0]]</td></tr>
<tr><td>قص (Shear)</td><td>(1, 0)</td><td>(1, 1)</td><td>[[1, 1], [0, 1]]</td></tr>
<tr><td>كبس على خط (أعمدة على خط واحد)</td><td>(2, 1)</td><td>(‎-2, ‎-1)</td><td>[[2, ‎-2], [1, ‎-1]]</td></tr></table>'''

BREP_WORDS = [
 W('class Body', [('class', 'نوع جديد'), ('Body', 'الجسم: أركان + أضلاع + وشوش')],
   'الـ B-Rep = بنوصف الجسم بحدوده: الوشوش، واللي حوالين كل وش من أضلاع، واللي في طرف كل ضلع من أركان.'),
 W('return (int)faces.size() - (int)edges.size() + (int)vertices.size();', [('faces.size()', 'F: عدد الوشوش'), ('edges.size()', 'E: عدد الأضلاع'), ('vertices.size()', 'V: عدد الأركان'), ('(int)', 'حوّل لرقم بإشارة عشان الطرح')],
   'size() بترجّع رقم من غير إشارة؛ لو طرحنا رقم أكبر من غير التحويل النتيجة تبقى رقم عملاق.'),
 W('cube.faces = { {{0, 1, 2, 3}}, {{4, 5, 6, 7}}, {{0, 9, 4, 8}},', [('{{0, 1, 2, 3}}', 'وش: قوس للـ Face وجواه قوس للـ vector'), ('0, 1, 2, 3', 'أرقام الأضلاع (مش الأركان)')],
   'الوش التالت {0, 9, 4, 8} = الضلع 0 (من ركن 0 لـ 1) والضلع 9 (1-5) والضلع 4 (4-5) والضلع 8 (0-4): الوش القدام. ده الـ Topology.'),
 W('lines.push_back(e.v1);', [('lines', 'ترتيب رسم الخطوط'), ('push_back', 'زوّد في الآخر'), ('e.v1', 'الركن التاني للضلع')],
   'قايمة الأضلاع في الـ B-Rep هي نفسها ترتيب رسم <code>GL_LINES</code>. عشان كده Ekeeda بيقول التحويل لـ Wireframe سهل.'),
 W('screen.push_back((v.x - 0.5f) * 0.9f + (v.y - 0.5f) * 0.45f);', [('v.x - 0.5f', 'خلّي نص المكعب في النص'), ('* 0.9f', 'كبّر/صغّر'), ('+ (v.y - 0.5f) * 0.45f', 'العمق بيزق يمين (إسقاط مايل)')],
   'ده إسقاط بسيط بالحساب على الـ CPU. قريب هنعمله بمصفوفة (المحاضرة 3 النهارده) جوه الـ Shader.'),
 W('glDrawElements(GL_LINES, (int)lines.size(), GL_UNSIGNED_INT, nullptr);', [('GL_LINES', 'كل رقمين = خط مستقل'), ('lines.size()', '24 رقم = 12 خط')],
   '<code>GL_LINE_STRIP</code> بدلها كان هيوصل كل ركن باللي بعده في القايمة، فتطلع خطوط زيادة (جربناها).'),
]

BREP_TABLE = '''<table class="types"><tr><th>الجسم</th><th>V (أركان)</th><th>E (أضلاع)</th><th>F (وشوش)</th><th>F − E + V</th></tr>
<tr><td>مكعب</td><td>8</td><td>12</td><td>6</td><td>2 ✓</td></tr>
<tr><td>هرم قاعدته مربع</td><td>5</td><td>8</td><td>5</td><td>2 ✓</td></tr>
<tr><td>مكعب من غير غطا</td><td>8</td><td>12</td><td>5</td><td>1 ✗ (مش مقفول)</td></tr></table>'''
