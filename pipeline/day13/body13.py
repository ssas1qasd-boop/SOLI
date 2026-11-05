# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثالث: الـ Classes والـ Textures</div>
  <h1>اليوم السادس — الجمعة 6 نوفمبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> عمر الـ Object (Stack/Scope Lifetimes) — <span style="color:#5b6372">cppreference و The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> Textures خطوة خطوة، والـ Atlas — <span style="color:#5b6372">learnopengl و Luke (DevMindscape)</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> تحويلات بالمصفوفات: الدوران والتركيب والإسقاط — <span style="color:#5b6372">Khan Academy</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> Solid modeling و CSG — <span style="color:#5b6372">Wikipedia و NERDfirst (Friday Minis 142)</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:4mm;background:#fffbeb"><b>النهارده الأربعة مربوطين:</b> الـ Object بيموت عند القوس، ونسخة الصورة على الـ CPU بنموّتها بإيدنا بعد ما الكارت ياخدها. والتحويلات بتتركب بالضرب والترتيب مهم، والـ CSG بيركب الأجسام بالعمليات والترتيب مهم برضه (A - B ≠ B - A).</div>
</section>''')

# ================================================================== 1 · object lifetime
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'عمر الـ Object على الـ Stack', '<span class="ltr">en.cppreference.com/w/cpp/memory</span> · The Cherno · Object Lifetime in C++ (Stack/Scope Lifetimes) · <span class="ltr">youtu.be/iNuTwvD6ciI</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> أي حاجة على الـ Stack بتموت لوحدها عند قوس الـ Scope بتاعها. واللي بـ <code>new</code> لأ. وبنستغل الموت الأوتوماتيك ده: Class على الـ Stack يعمل delete لما يموت (ScopedPtr).</div>
<p class="what">The Cherno شبّه الـ Stack بكومة كتب، وعمل Entity بيطبع «Created» و «Destroyed»، وورّى الفرق بين Stack و new، وحذّر من دالة بترجّع مصفوفة على الـ Stack، وبنى ScopedPtr، وذكر Timer و Scoped Lock. البرنامج 1 بيجرب كل أنواع الـ Scope. والبرنامج 2 بيعمل ScopedPtr و Timer ويقارنهم بـ <code>std::unique_ptr</code>.</p>''')
P.append(D1.fig(D.p_books(), 'كومة الكتب: كل Scope كتاب فوق اللي قبله، والـ Entity اللي على الـ Heap برّه الكومة خالص.'))
P.append(LIFE_TABLE)
P.append('<h3 id="life-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(LIFE_WORDS))
P.append('<h3>البرنامج 1: كل Scope بيموّت اللي فيه</h3><p class="what">قبل ما تشغّل: اكتب في ورقة ترتيب سطور Created و Destroyed.</p>'
         + prog(SRC + 'p1_lifetime.cpp', 'lifetime.cpp') + res(term(rd(SRC + 'p1_lifetime.txt')) + '<p style="font-size:10pt">«Destroyed Entity heap» مش موجودة في أي حتة، و «Destroyed Entity a» بعد «main ends»: a مات عند قوس main.</p>'))
P.append(SB13.d13_life())
P.append('<h3>البرنامج 2: ScopedPtr و unique_ptr و Timer</h3><p class="what">توقّع: «Destroyed Entity» قبل «after the scope» ولا بعدها؟</p>'
         + prog(SRC + 'p2_scoped_ptr.cpp', 'scoped_ptr.cpp') + res(term(rd(SRC + 'p2_scoped_ptr.txt'))))
P.append(D1.fig(D.p_scoped(), 'الـ ScopedPtr على الـ Stack ماسك عنوان الـ Entity اللي على الـ Heap.'))
P.append(SB13.d13_scoped())
P.append('<h3 id="why-life">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_life() + '<h3>البرنامج 2</h3>' + WHY.build_scoped())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ Scope = أي <code>{ }</code>: دالة، if، for، while، أو أقواس فاضية.</li>
 <li>اللي على الـ Stack بيموت عند <code>}</code>، والـ Destructor بيشتغل لوحده.</li>
 <li>اللي بـ <code>new</code> مابيموتش غير بـ delete.</li>
 <li>ماترجّعش عنوان متغير على الـ Stack. يا تحجز بـ new، يا تعمل المصفوفة برّه وتبعتها.</li>
 <li>ScopedPtr = <code>std::unique_ptr</code>: الـ Heap بيتمسح مع الـ Scope (RAII)، ومن غير ذاكرة زيادة (8 بايت).</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. زوّد في البرنامج 1 <code>while</code> بيعمل Entity مرتين. 2. اعمل Timer حوالين لوب مليون لفة واطبع الوقت الحقيقي بالـ ns. 3. حاول تنسخ <code>unique_ptr</code>: <code>auto v = u;</code> واقرا رسالة الـ compiler.</div></section>''')

# ================================================================== 2 · textures (Luke)
P.append(lec('l2', 'المحاضرة 2 · رسم', 'Textures خطوة خطوة، والـ Atlas', 'learnopengl · Getting started: Textures · Luke (DevMindscape) · Basic OpenGL Textures Explained (easy) · <span class="ltr">youtu.be/bvWQZq0NUv0</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Texture 3 خطوات: حمّل الصورة، واربط كل ركن بإحداثي فيها، وارسم بـ sampler في الـ Fragment Shader. والصورة بتتنسخ للكارت، فنسختنا على الـ CPU نقدر نمسحها.</div>
<p class="what">Luke بيبدأ من مربع ملوّن ويوصل لمربع عليه صورة: STB Image مع القلب، و stride 4 floats، و sampler = الخانة 0، و glDeleteTextures في الآخر. عملنا ده كذا مرة قبل كده. النهارده البرنامج 1 بيثبت كلامه بالأرقام: يحمّل نفس الصورة مرة من غير قلب ومرة مقلوبة، ويمسح نسخة الـ CPU، ويقرا الصورة من الكارت تاني. والبرنامج 2 بيكمّل خطوة «اربط الإحداثيات»: Atlas فيه 16 خانة، وكل مستطيل بياخد خانة واحدة.</p>''')
P.append(D1.fig(D.t_flip(), 'letter.png في الذاكرة: أول صف هو اللي بيترسم عند v = 0 (تحت). والأحمر في الملف تحت شمال.'))
P.append(D1.fig(D.t_atlas(), 'الـ Atlas: الخانات الصفرا هي اللي اخترناها. وأرقام u و v من التشغيل.'))
P.append(TEX_TABLE)
P.append('<h3 id="tex-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(TEX_WORDS))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD)، و <code>stb_image.h</code> و <code>stb.cpp</code> جنب الكود، وفولدر <code>res</code> فيه <code>letter.png</code> بتاع يوم 4. الترجمة: <code>g++ gpu_copy.cpp stb.cpp</code> + المكتبات. والبرنامج 2 مش محتاج صور. والشباك بيتقفل بـ Esc.</div>')
P.append('<h3>البرنامج 1: من الملف للكارت</h3><p class="what">شمال: من غير قلب. يمين: مقلوبة.</p>'
         + prog(SRC + 't1_gpu_copy.cpp', 'gpu_copy.cpp')
         + res(term(rd(SRC + 't1_gpu_copy.txt')) + bigimg('t1_gpu_copy', 'الشباك الحقيقي: شمال الحرف F مقلوب (الأحمر فوق)، ويمين سليم (الأحمر تحت شمال زي الملف).', '140mm'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append('<h3>البرنامج 2: Atlas فيه 16 خانة</h3><p class="what">توقّع: الخانة 10 u بتاعها من كام لكام؟</p>'
         + prog(SRC + 't2_atlas.cpp', 'atlas.cpp')
         + res(term(rd(SRC + 't2_atlas.txt')) + bigimg('t2_atlas', 'الشباك الحقيقي: الخانات 0 و 5 و 10 و 15، والأخير الـ Atlas كله. المربع الأبيض في ركن كل خانة تحت شمال.', '150mm'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append('<h3 id="why-tex">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_gpu() + '<h3>البرنامج 2</h3>' + WHY.build_atlas())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Luke: حمّل ← اربط بالأركان ← ارسم بـ sampler.</li>
 <li>اقلب الصورة: <code>stbi_set_flip_vertically_on_load(1)</code>.</li>
 <li><code>glTexImage2D</code> بينسخ للكارت، وبعده <code>stbi_image_free</code>.</li>
 <li>الـ sampler بياخد رقم الخانة (Texture Unit)، والخانة بتتربط بـ glActiveTexture و glBindTexture.</li>
 <li>Atlas: الخانة (col, row) = u من col/n لـ (col + 1)/n، و v من row/n لـ (row + 1)/n. رسمة واحدة لكل المستطيلات.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اختار الخانات 3 و 6 و 9 و 12 (القطر التاني). 2. خلّي مستطيل ياخد خانتين جنب بعض (u من 0 لـ 0.5). 3. في البرنامج 1 اطبع آخر بكسل في الذاكرة مع القلب ومن غيره.</div></section>''')

# ================================================================== 3 · matrix transformations
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'تحويلات بالمصفوفات: الدوران والتركيب والإسقاط', 'Khan Academy · Linear algebra: Matrix transformations · <span class="ltr">khanacademy.org/math/linear-algebra/matrix-transformations</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> أي تحويل خطي = مصفوفة أعمدتها T(e1) و T(e2). من كده نطلع مصفوفة الدوران، ولما نعمل تحويلين ورا بعض نضرب المصفوفتين، والترتيب مهم.</div>
<p class="what">في الأيام اللي فاتت عملنا التحويل كدالة، والمصفوفة من T(e1) و T(e2)، وتحويلات بسيطة على شكل (تكبير ودوران 90 وميل ومراية). النهارده الجزء اللي بعده من وحدة Khan: الدوران بأي زاوية، والتركيب (Composition)، والعكس، والدوران في 3D حوالين محور x، والإسقاط على خط (Projection).</p>''')
P.append(D1.fig(D.m_compose(), 'نفس النقطة ونفس التحويلين بترتيب مختلف: نتيجتين مختلفتين (من التشغيل).'))
P.append(D1.fig(D.m_proj(), 'الإسقاط: البرتقاني على الخط، والأحمر المتقطع عمودي عليه.'))
P.append(MAT_TABLE)
P.append('<h3 id="mat-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(MAT_WORDS))
P.append('<h3>البرنامج 1: الدوران والتركيب</h3><p class="what">احسب في ورقة: (1, 1) بعد S وبعدين R.</p>'
         + prog(SRC + 'm1_rotate_compose.py', 'rotate_compose.py') + res(term(rd(SRC + 'm1_rotate_compose.txt'))))
P.append('<h3>البرنامج 2: 3D والإسقاط</h3><p class="what">احسب: (2, 3) · (2, 1) = ؟</p>'
         + prog(SRC + 'm2_rotate3d_project.py', 'rotate3d_project.py') + res(term(rd(SRC + 'm2_rotate3d_project.txt'))))
P.append('<h3 id="why-mat">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_mat())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الدوران بزاوية θ: [[cos θ، ‎-sin θ]، [sin θ، cos θ]]، والزاوية بالـ Radians.</li>
 <li>تحويلين ورا بعض = ضرب المصفوفتين، وبيتقرا من اليمين: R @ S = S الأول.</li>
 <li>الترتيب مهم: R @ S ≠ S @ R.</li>
 <li>عكس الدوران = الدوران بالسالب = الـ Transpose، والدوران مابيغيرش الطول.</li>
 <li>الإسقاط على خط: P = u uᵀ ÷ (u · u)، و P @ P = P.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. لف (1, 0) بـ 45 درجة: النتيجة (0.707، 0.707)؟ 2. اعمل rotate_y و rotate_z. 3. اسقط (2, 3) على محور y: P = ؟</div></section>''')

# ================================================================== 4 · solid modeling & CSG
P.append(lec('l4', 'المحاضرة 4 · CAD', 'Solid modeling و CSG', '<span class="ltr">en.wikipedia.org/wiki/Solid_modeling</span> · 0612 TV w/ NERDfirst · Constructive Solid Geometry - Friday Minis 142 · <span class="ltr">youtu.be/az8nvcEM2bM</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ CSG بيبني الجسم من أجسام بسيطة (كرة وصندوق وأسطوانة) بـ 3 عمليات: Union و Intersect و Difference. ولو الجسم دالة «النقطة جوه؟»، العمليات بتبقى || و && و && !.</div>
<p class="what">NERDfirst شرح العمليات التلاتة اللي في Blender، وقال إن اسمها الأدق Set Operations مش Boolean. و Wikipedia بتقول إن برامج الـ Solid modeling بتستخدم نسخة «Regularized» منهم عشان النتيجة تفضل جسم سليم. البرنامج 1 بيعمل كرة وصندوق ويطبع العمليات التلاتة على محور x. والبرنامج 2 بيوري الـ Regularized على خط (بعد واحد) عشان تبان.</p>''')
P.append(D1.fig(D.c_csg(), 'العمليات التلاتة على مقطع z = 0 بنفس الكرة والصندوق اللي في البرنامج 1.'))
P.append(D1.fig(D.c_reg(), 'A و C لامسين بعض عند 2 بس: التقاطع العادي نقطة طولها صفر، والـ Regularized بيشيلها.'))
P.append(CSG_TABLE)
P.append('<h3 id="csg-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CSG_WORDS))
P.append('<h3>البرنامج 1: كرة وصندوق</h3><p class="what">توقّع سطر «A minus B».</p>'
         + prog(SRC + 'c1_csg.cpp', 'csg.cpp') + res(term(rd(SRC + 'c1_csg.txt')) + '<p style="font-size:10pt">عند x = 0 الكرة والصندوق الاتنين فيهم النقطة (حدود الصندوق ≥ 0)، فالـ Difference شالها.</p>'))
P.append('<h3>البرنامج 2: Regularized على خط</h3><p class="what">توقّع: A ∩ C كام حتة؟</p>'
         + prog(SRC + 'c2_regularized.cpp', 'regularized.cpp') + res(term(rd(SRC + 'c2_regularized.txt'))))
P.append('<h3 id="why-csg">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_csg())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>CSG = Primitives (أجسام بسيطة) + Union و Intersect و Difference، وكتير ورا بعض = شكل معقد (شجرة CSG).</li>
 <li>اسمها Boolean، والأدق Set Operations.</li>
 <li>Union = ||، و Intersect = &&، و Difference = && ! (والترتيب مهم: A - B ≠ B - A).</li>
 <li>الـ Regularized: بتشيل الحتت اللي مالهاش حجم (وش أو خط لوحده).</li>
 <li>الـ CSG بيوصف «إزاي اتبنى»، والـ B-Rep بيوصف «الأسطح النهائية»، وبرامج CAD بتشيل الاتنين.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اعمل B - A وقارن بـ A - B. 2. زوّد أسطوانة C وطلّع (A ∪ B) - C. 3. في Blender: Add ← Cube و Sphere، وبعدين Modifier ← Boolean وجرّب التلاتة.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>عمر الـ Object:</b> الـ Texture class ممكن يعمل glDeleteTextures في الـ Destructor (زي ScopedPtr)، فالـ Texture يتمسح لوحده.</td></tr>
 <tr><td class="n">2</td><td><b>Textures:</b> نسخة الـ CPU عمرها قصير (لحد glTexImage2D)، ونسخة الكارت بتعيش لحد glDeleteTextures.</td></tr>
 <tr><td class="n">3</td><td><b>التحويلات:</b> الدوران والتركيب هما اللي هنحطهم في الـ Vertex Shader لما نحرك الأشكال.</td></tr>
 <tr><td class="n">4</td><td><b>CSG:</b> بيركب الأجسام بالعمليات، وزي ضرب المصفوفات: الترتيب مهم.</td></tr>
</table>
<h3>بكره (السبت 7-11)</h3>
<ul><li>برمجة: النسخ و Copy Constructors (The Cherno: Copying and Copy Constructors in C++).</li><li>رسم: مراجعة learnopengl.</li>
<li>رياضيات: Matrix transformations (Khan Academy).</li><li>الـ CAD: Git (Recording Changes و Why Use Git).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>cppreference Memory: <span class="ltr">en.cppreference.com/w/cpp/memory</span> · Object Lifetime in C++: <span class="ltr">youtube.com/watch?v=iNuTwvD6ciI</span></li>
 <li>learnopengl Textures: <span class="ltr">learnopengl.com/Getting-started/Textures</span> · Basic OpenGL Textures Explained: <span class="ltr">youtube.com/watch?v=bvWQZq0NUv0</span></li>
 <li>Khan Matrix transformations: <span class="ltr">khanacademy.org/math/linear-algebra/matrix-transformations</span></li>
 <li>Solid modeling: <span class="ltr">en.wikipedia.org/wiki/Solid_modeling</span> · Constructive Solid Geometry - Friday Minis 142: <span class="ltr">youtube.com/watch?v=az8nvcEM2bM</span></li></ul></section>''')
