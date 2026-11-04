import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

STRUCT_WORDS = [
 W('struct PlayerS', [('struct', 'كلمة بتعرّف نوع جديد (زي class بالظبط)'), ('PlayerS', 'اسم النوع (S = struct عشان نفرّقه)')],
   'The Cherno: الفرق الوحيد إن الـ struct كل حاجة فيه <code>public</code> لوحدها، والـ class كل حاجة <code>private</code> لوحدها. غير كده نفس الحاجة.'),
 W('struct Vec2', [('struct', 'نوع جديد'), ('Vec2', 'متجه 2D (Vector 2)')],
   'The Cherno بيستخدم struct لما الحاجة «بيانات وبس» (POD = Plain Old Data): رقمين ومعاهم دالة صغيرة. ولو حاجة كبيرة فيها منطق (Player) يستخدم class.'),
 W('Vec2 position = { 1.0f, 2.0f };', [('Vec2', 'النوع'), ('position', 'الاسم'), ('{ 1.0f, 2.0f }', 'القيم بالترتيب: x ثم y')],
   'نفس طريقة المصفوفات <code>{ … }</code>. شغالة لأن الـ struct بسيط وكل حاجة فيه public. في class فيه <code>private</code> مش هتنفع كده.'),
 W('Vertex square[4] = {', [('Vertex', 'نوع الركن (struct)'), ('square', 'الاسم'), ('[4]', '4 أركان')],
   'بدل <code>float positions[16]</code> بتاع امبارح: نفس الـ 64 بايت بالظبط، بس كل ركن ليه أسماء (x و y و u و v).'),
 W('std::cout << "offsetof(Vertex, x) = " << offsetof(Vertex, x) << std::endl;', [('offsetof', 'ماكرو من <cstddef>'), ('Vertex', 'الـ struct'), ('x', 'المتغير')],
   'بيرجّع المتغير بيبدأ بعد كام بايت من أول الـ struct. ده بالظبط آخر رقم في <code>glVertexAttribPointer</code> (الـ offset).'),
 W('float* numbers = &square[0].x;', [('float*', 'Pointer لأرقام float'), ('&', 'عنوان'), ('square[0].x', 'أول رقم في أول ركن')],
   'كده بنقرا نفس البايتات كأنها 16 رقم ورا بعض. ده اللي الكارت بيشوفه بعد <code>glBufferData</code>: مفيش أسماء، أرقام بس.'),
]

STRUCT_TABLE = '''<table class="types"><tr><th></th><th><code>struct</code></th><th><code>class</code></th></tr>
<tr><td>من غير ما نكتب حاجة</td><td><code>public</code></td><td><code>private</code></td></tr>
<tr><td>Methods ومتغيرات</td><td>أيوه</td><td>أيوه</td></tr>
<tr><td>الحجم في الرام</td><td>نفس الحجم (12 بايت)</td><td>نفس الحجم (12 بايت)</td></tr>
<tr><td>The Cherno بيستخدمه لـ</td><td>بيانات بسيطة: Vec2، ركن، لون</td><td>حاجة فيها منطق: Player، Renderer</td></tr>
<tr><td>في برامج النهارده</td><td><code>Vec2</code> و <code>Vertex</code> و <code>Triangle</code> و <code>Corner</code></td><td><code>PlayerC</code></td></tr></table>'''

TEX_WORDS = [
 W('unsigned char* bytes = stbi_load("res/pixel_cat.png", &widthImg, &heightImg, &numColCh, 0);', [('bytes', 'اسم Victor Gordan للبكسلات'), ('&widthImg, &heightImg', 'الدالة هتكتب المقاس هنا'), ('&numColCh', 'عدد القنوات (Color Channels)'), ('0', 'هاتها زي ما هي في الملف')],
   'امبارح The Cherno كتب 4 (هاتها RGBA دايماً). Victor Gordan بيكتب 0، فلازم <code>glTexImage2D</code> يتكتب بعدد القنوات الصح (4 هنا). لو كتبنا RGB والملف 4 قنوات: الصورة بتبوظ (جربناها).'),
 W('glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST);', [('GL_TEXTURE_MIN_FILTER', 'لما الصورة تتصغّر'), ('NEAREST_MIPMAP', 'اختار أقرب نسخة مصغّرة'), ('_NEAREST', 'وجواها أقرب بكسل')],
   'القيم اللي فيها MIPMAP لازم معاها <code>glGenerateMipmap</code>. ودي القيمة اللي Victor Gordan اختارها.'),
 W('glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, widthImg, heightImg, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes);', [('0', 'المستوى 0 = الصورة الأصلية'), ('GL_RGBA', 'إزاي تتخزن في الكارت'), ('GL_RGBA', 'شكل البايتات اللي باعتينها: 4 لكل بكسل'), ('bytes', 'العنوان في الرام')],
   'التانية لازم تطابق الملف. الصورة 16 × 16 × 4 = 1024 بايت.'),
 W('glGenerateMipmap(GL_TEXTURE_2D);', [('glGenerateMipmap', 'اعمل نسخ مصغّرة'), ('GL_TEXTURE_2D', 'للـ Texture المربوطة')],
   'كل نسخة نص اللي قبلها: 16 و 8 و 4 و 2 و 1. لما المربع يبقى صغير على الشاشة، الكارت بيقرا من نسخة صغيرة بدل ما يتنطط في الأصل.'),
 W('"    texCoord = aTex * 2.0 - 0.5;\\n"', [('aTex', 'من 0 لـ 1'), ('* 2.0', 'من 0 لـ 2'), ('- 0.5', 'من ‎-0.5 لـ 1.5')],
   'كده المربع بيقرا الصورة في النص ونص صورة برّه من كل ناحية. الإعداد WRAP هو اللي بيقرر الجزء اللي برّه.'),
 W('GLint modes[4] = { GL_REPEAT, GL_MIRRORED_REPEAT, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER };', [('GL_REPEAT', 'كرر'), ('GL_MIRRORED_REPEAT', 'كرر معكوس (زي المراية)'), ('GL_CLAMP_TO_EDGE', 'مد آخر بكسل'), ('GL_CLAMP_TO_BORDER', 'لون ثابت إحنا بنختاره')],
   'دول الأربعة اللي Victor Gordan شرحهم. هما أرقام (GLint)، فينفع نحطهم في مصفوفة ونلف عليهم.'),
 W('glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border);', [('fv', 'f = float و v = vector (مصفوفة)'), ('GL_TEXTURE_BORDER_COLOR', 'لون الحدود'), ('border', '4 أرقام: أحمر')],
   'الـ <code>i</code> في <code>glTexParameteri</code> = رقم صحيح واحد. هنا محتاجين 4 أرقام عشرية، فالدالة اسمها <code>fv</code>.'),
 W('glGenTextures(4, textures);', [('4', 'عدد 4 Textures'), ('textures', 'المصفوفة (اسمها = عنوان أولها)')],
   'زي <code>glGenBuffers(1, &amp;vbo)</code> بس بالجملة. الكارت هيكتب 1 و 2 و 3 و 4.'),
]

TEX_TABLE = '''<table class="types"><tr><th>الإعداد</th><th>The Cherno (امبارح)</th><th>Victor Gordan (النهارده)</th></tr>
<tr><td>آخر رقم في <code>stbi_load</code></td><td>4 (دايماً RGBA)</td><td>0 (زي الملف)</td></tr>
<tr><td>التصغير (MIN)</td><td><code>GL_LINEAR</code></td><td><code>GL_NEAREST_MIPMAP_NEAREST</code> + <code>glGenerateMipmap</code></td></tr>
<tr><td>التكبير (MAG)</td><td><code>GL_LINEAR</code></td><td><code>GL_NEAREST</code> (مربعات حادة)</td></tr>
<tr><td>التكرار (WRAP)</td><td><code>GL_CLAMP_TO_EDGE</code></td><td><code>GL_REPEAT</code></td></tr>
<tr><td>أسماء الـ Shader</td><td><code>u_Texture</code> و <code>v_TexCoord</code></td><td><code>tex0</code> و <code>texCoord</code></td></tr>
<tr><td>الأركان</td><td><code>float positions[16]</code> (x, y, u, v)</td><td><code>GLfloat vertices[]</code> (x, y, z, u, v)</td></tr></table>'''

TRANS_WORDS = [
 W('def T(v):', [('def', 'دالة في Python'), ('T', 'Transformation'), ('v', 'المتجه الداخل')],
   'Khan: «التحويل» هو نفس كلمة «دالة»، بس على متجهات. داخل متجه، طالع متجه.'),
 W('return (x1 + 2 * x2, 3 * x3)', [('x1 + 2 * x2', 'الرقم الأول الطالع'), ('3 * x3', 'الرقم التاني الطالع'), ('( , )', 'رقمين = متجه في ℝ²')],
   'بالرموز اللي في الفيديو: <bdi dir="ltr">T: ℝ³ → ℝ²</bdi>. عدد الداخل 3، وعدد الطالع 2.'),
 W('screen = (P @ centered.T).T', [('P', 'المصفوفة 2 × 3'), ('centered.T', 'الأركان عمود عمود (3 × 8)'), ('@', 'ضرب مصفوفات'), ('.T', 'رجّعها صف لكل ركن (8 × 2)')],
   '<code>.T</code> في NumPy = قلب الصفوف لأعمدة (Transpose)، مش T بتاع التحويل. المصفوفة 2 × 3 لازم تتضرب في حاجة عدد صفوفها 3.'),
]

TRANS_TABLE = '''<table class="types"><tr><th>الداخل (ℝ³)</th><th>بالدالة T</th><th>بالمصفوفة A</th></tr>
<tr><td>(1, 1, 1)</td><td>(3, 3)</td><td>(3, 3)</td></tr>
<tr><td>(2, 4, 1)</td><td>(10, 3)</td><td>(10, 3)</td></tr>
<tr><td>(0, 0, 0)</td><td>(0, 0)</td><td>(0, 0)</td></tr></table>'''

MESH_WORDS = [
 W('struct Triangle', [('struct', 'بيانات بسيطة'), ('Triangle', 'مثلث')],
   'المثلث مش شايل أماكن، شايل <b>أرقام</b> أركان من قايمة الأركان. ده الـ Indexed Face List بتاع Cem Yuksel، وهو نفس فكرة الـ EBO.'),
 W('float alpha = Area2(px, py, x1, y1, x2, y2) / A;', [('Area2(…)', 'مساحة المثلث اللي بين P والركنين التانيين'), ('/ A', 'على مساحة المثلث كله')],
   'α = A₀ / A. لو P على P₀ بالظبط، المثلث ده هو المثلث الأصلي، فـ α = 1. ولو P على الضلع اللي قصاد P₀، المساحة صفر.'),
 W('std::set<std::pair<unsigned int, unsigned int>> edges;', [('std::set', 'قايمة مرتبة ومفيهاش تكرار'), ('std::pair', 'حاجتين مع بعض'), ('unsigned int, unsigned int', 'رقمين الركنين')],
   'كل ضلع داخلي في المكعب موجود في مثلثين. الـ set بيشيله مرة واحدة. بـ vector كان هيتعد مرتين (جربناها).'),
 W('float x = (px + 0.5f) / 640.0f * 2.0f - 1.0f;', [('px + 0.5f', 'نص البكسل'), ('/ 640.0f', 'من 0 لـ 1'), ('* 2.0f - 1.0f', 'من ‎-1 لـ 1 (NDC)')],
   'الكارت بيحسب اللون في نص كل بكسل. لو نسينا 0.5 الأرقام بتختلف بواحد في الآخر.'),
 W('glReadPixels(px, py, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, gpu);', [('px, py', 'البكسل (من تحت شمال)'), ('1, 1', 'بكسل واحد'), ('GL_RGBA, GL_UNSIGNED_BYTE', '4 بايت'), ('gpu', 'اكتب هنا')],
   'عكس <code>glTexImage2D</code>: بدل ما نبعت بكسلات للكارت، بنقرا بكسل منه. كده نتأكد إن حسابنا = حساب الكارت.'),
]

MESH_TABLE = '''<table class="types"><tr><th>α و β و γ</th><th>النقطة فين</th><th>من برنامجنا</th></tr>
<tr><td>كلهم من 0 لـ 1</td><td>جوه المثلث</td><td>(1, 1): ‏0.5 و 0.25 و 0.25</td></tr>
<tr><td>واحدة = 0</td><td>على ضلع</td><td>(2, 2): ‏0 و 0.5 و 0.5</td></tr>
<tr><td>اتنين = 0 والتالتة = 1</td><td>على ركن</td><td>(4, 0): ‏0 و 1 و 0</td></tr>
<tr><td>واحدة سالبة</td><td>برّه</td><td>(3, 3): ‏‎-0.5 و 0.75 و 0.75</td></tr></table>'''
