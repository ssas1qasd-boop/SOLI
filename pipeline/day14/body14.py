# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثالث: الـ Classes والـ Textures</div>
  <h1>اليوم السابع — السبت 7 نوفمبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> النسخ و Copy Constructors — <span style="color:#5b6372">The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> مراجعة: Texture class والنسخ — <span style="color:#5b6372">learnopengl</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> صورة الشكل بعد التحويل، والعكس — <span style="color:#5b6372">Khan Academy</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> Git: تسجيل التغييرات — <span style="color:#5b6372">git-scm و Net Ninja</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:4mm;background:#fffbeb"><b>النهارده الأربعة عن «النسخة»:</b> نسخة الـ object (Shallow ولا Deep)، ونسخة الـ Texture اللي بتمسح الأصل، والتحويل اللي ليه عكس يرجّعك للأصل ولا لأ، و Git اللي بيحفظ كل نسخ الملف ويرجّعك لأي واحدة.</div>
</section>''')

# ================================================================== 1 · copying
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'النسخ و Copy Constructors', 'The Cherno · Copying and Copy Constructors in C++ · <span class="ltr">youtu.be/BvR1Pgzzr38</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> <code>=</code> بينسخ دايماً. مع Pointer بينسخ العنوان بس، فالـ class اللي جواه Pointer محتاج Copy Constructor يعمل نسخة حقيقية (Deep Copy). وأحسن حاجة إنك ماتنسخش أصلاً: ابعت <code>const T&amp;</code>.</div>
<p class="what">The Cherno بدأ بـ int و struct و Pointer، وبعدين بنى String «old school» بـ char* و new و memcpy، ونسخه: الاتنين اتغيروا والبرنامج وقع. وبعدين كتب Copy Constructor، وعد «Copied!» مع الدوال بالقيمة، وصلّحها بـ const reference. البرنامج 1 أنواع النسخ الأربعة. والبرنامج 2 الـ String بتاعه بالظبط.</p>''')
P.append(D1.fig(D.p_shallow(), 'Shallow: Buffer واحد لاتنين (اللي حصل من غير Copy Constructor). Deep: كل واحد Buffer.'))
P.append(COPY_TABLE)
P.append('<h3 id="copy-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(COPY_WORDS))
P.append('<h3>البرنامج 1: int و struct و Pointer و Reference</h3><p class="what">توقّع قيمة pa->x.</p>'
         + prog(SRC + 'p1_copy_basics.cpp', 'copy_basics.cpp') + res(term(rd(SRC + 'p1_copy_basics.txt')) + '<p style="font-size:10pt">&amp;va و &amp;vb بينهم 8 بايت = sizeof(Vector2): نسختين جنب بعض على الـ Stack.</p>'))
P.append('<h3>البرنامج 2: String بتاع The Cherno</h3><p class="what">عد: Copied! هتتطبع كام مرة؟</p>'
         + prog(SRC + 'p2_string.cpp', 'string.cpp') + res(term(rd(SRC + 'p2_string.txt')) + '<p style="font-size:10pt">Copied! عدد 3 مرات: واحدة لـ second، واتنين لـ PrintByValue. وزي The Cherno بالظبط.</p>'))
P.append(SB14.d14_string())
P.append('<h3 id="why-copy">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_basics() + '<h3>البرنامج 2</h3>' + WHY.build_string())
P.append('''<div class="sum"><b>الملخص:</b><ul><li><code>=</code> بينسخ القيمة، ومع Pointer القيمة هي العنوان.</li>
 <li>الـ Copy Constructor الافتراضي = Shallow Copy (كل Member زي ما هو).</li>
 <li>class بيعمل new في الـ Constructor و delete في الـ Destructor: لازم Copy Constructor بـ Deep Copy (أو تمنع النسخ).</li>
 <li><code>T(const T&amp; other) = delete;</code> = ممنوع النسخ (زي unique_ptr).</li>
 <li>ابعت الـ objects بـ <code>const T&amp;</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. زوّد <code>String third = second; third[0] = \'K\';</code> واطبع التلاتة. 2. خلّي PrintByValue بـ <code>String&amp;</code> (من غير const) وغيّر حرف جواها: الأصل اتغير؟ 3. اكتب <code>operator=</code> كمان: ده اللي بيشتغل في <code>second = string;</code> لما الاتنين يكونوا متعملين قبل كده.</div></section>''')

# ================================================================== 2 · texture class & copies
P.append(lec('l2', 'المحاضرة 2 · رسم', 'مراجعة: Texture class والنسخ', '<span class="ltr">learnopengl.com</span> · Getting started (Textures و Shaders)'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Texture class بيمسك رقم على الكارت ويمسحه في الـ Destructor (زي ScopedPtr امبارح). لو اتنسخ بالقيمة، النسخة بتمسح الـ Texture الأصلي. نفس مشكلة الـ String بالظبط، بس الكارت مش هيقولك.</div>
<p class="what">مراجعة الأسبوع: Texture class من Constructor و Destructor (يوم 3)، و Bind، والخانة 0. البرنامج 1 بيبعت الـ Texture الأزرق لدالة بالقيمة ويسأل الكارت قبل وبعد. والبرنامج 2 نفس البرنامج بعد التصليح: <code>const Texture&amp;</code> ومنع النسخ.</p>''')
P.append(D1.fig(D.t_copy(), 'اللي حصل في البرنامج 1 خطوة خطوة (من التشغيل).'))
P.append(TEX_TABLE)
P.append('<h3 id="tex-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(TEX_WORDS))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD). مفيش صور: الرقعة 2 × 2 في الكود. الترجمة: <code>g++ texture_copy.cpp</code> + المكتبات. والشباك بيتقفل بـ Esc. كل حاجة جوه أقواس <code>{ }</code> في main عشان الـ Textures تموت قبل glfwTerminate.</div>')
P.append('<h3>البرنامج 1: Texture بالقيمة</h3><p class="what">توقّع: اليمين هيبقى أزرق؟</p>'
         + prog(SRC + 't1_texture_copy.cpp', 'texture_copy.cpp')
         + res(term(rd(SRC + 't1_texture_copy.txt')) + bigimg('t1_texture_copy', 'الشباك الحقيقي: الاتنين أحمر. الأزرق اتمسح من الكارت جوه Describe.', '140mm'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append('<h3>البرنامج 2: const Texture& و = delete</h3><p class="what">نفس البرنامج، سطرين اتغيروا.</p>'
         + prog(SRC + 't2_texture_ref.cpp', 'texture_ref.cpp')
         + res(term(rd(SRC + 't2_texture_ref.txt')) + bigimg('t2_texture_ref', 'الشباك الحقيقي: أحمر وأزرق. و ~Texture اشتغل مرة واحدة لكل id.', '140mm'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append('<h3 id="why-tex">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_texcopy() + '<h3>البرنامج 2</h3>' + WHY.build_texref())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>class بيمسك حاجة على الكارت (Texture، Buffer، Shader) = نفس قواعد الـ String.</li>
 <li>نسخه بالقيمة = id نفسه، والنسخة بتمسح الأصل.</li>
 <li>الكارت مابيقولش: استخدم glIsTexture و glGetError عشان تعرف.</li>
 <li>الحل: <code>const Texture&amp;</code> في الدوال، و <code>Texture(const Texture&amp;) = delete;</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. في البرنامج 1 خلّي Describe تاخد <code>Texture&amp;</code> (من غير const): اشتغل؟ 2. اعمل Texture تالت أخضر في البرنامج 2 وارسم 3 مربعات. 3. اطبع glGetError بعد كل Bind في البرنامج 2.</div></section>''')

# ================================================================== 3 · image & inverse
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'صورة الشكل بعد التحويل، والعكس', 'Khan Academy · Linear algebra: Matrix transformations · <span class="ltr">khanacademy.org/math/linear-algebra/matrix-transformations</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> التحويل بيودّي المربع الوحدة لمتوازي أضلاع، ومساحته = |det|. ولو det = 0 المربع بيتكبس لخط، ومفيش طريقة نرجع (مفيش عكس). غير كده العكس بيرجّعك للأصل بالظبط.</div>
<p class="what">كمّلنا وحدة Khan: الـ Image of a subset (صورة شكل كامل)، وإمتى التحويل ليه عكس (Invertible). البرنامج 1 بيحسب صورة المربع تحت A و B ومساحتها ويقارنها بالـ det، ويرسمهم. والبرنامج 2 بيحسب العكس بإيدنا ويحل A x = b.</p>''')
P.append(D1.fig(D.m_det(), 'المربع الوحدة (رمادي) وصورته: A مساحتها 2، و B خط (من التشغيل).'))
P.append(MAT_TABLE)
P.append('<h3 id="mat-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(MAT_WORDS))
P.append('<h3>البرنامج 1: صورة المربع ومساحتها</h3><p class="what">احسب: (1, 1) بعد A = ؟</p>'
         + prog(SRC + 'm1_image_area.py', 'image_area.py') + res(term(rd(SRC + 'm1_image_area.txt')) + bigimg('m1_image_area', 'image_area.png اللي البرنامج حفظها.', '120mm')))
P.append('<h3>البرنامج 2: العكس وحل المعادلة</h3><p class="what">احسب العكس في ورقة الأول.</p>'
         + prog(SRC + 'm2_inverse.py', 'inverse.py') + res(term(rd(SRC + 'm2_inverse.txt'))))
P.append('<h3 id="why-mat">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_mat())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ Image = كل نقط الشكل بعد التحويل: <code>(A @ corners.T).T</code>.</li>
 <li>المساحة الجديدة = |det(A)| × القديمة.</li>
 <li>عكس 2 × 2 = [[d, ‎-b], [‎-c, a]] ÷ (ad - bc)، و A @ A⁻¹ = I.</li>
 <li>det = 0: مفيش عكس (Singular)، لأن نقط كتير بتروح لنفس المكان.</li>
 <li>A x = b: <code>np.linalg.solve(A, b)</code>.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. جرّب A = rotation(30) بتاعة امبارح: المساحة اتغيرت؟ 2. اعكس [[3, 1], [2, 1]] في ورقة وقارن. 3. ارسم صورة مثلث (0, 0) و (1, 0) و (0, 1) تحت A.</div></section>''')

# ================================================================== 4 · git
P.append(lec('l4', 'المحاضرة 4 · CAD', 'Git: تسجيل التغييرات', '<span class="ltr">git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository</span> · Net Ninja · Git &amp; GitHub Tutorial for Beginners #1 - Why Use Git? · <span class="ltr">youtu.be/3RjQznt-8kE</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> Git بيسجل لقطات (Commits) من ملفاتك في فولدر واحد، وترجع لأي لقطة. الملف بيعدي من «اتغير» لـ «جاهز» (add) لـ «اتسجل» (commit).</div>
<p class="what">Net Ninja حكى قصة العميل اللي غيّر اللون 3 مرات وفي الآخر عايز الأصلي، وإزاي كان بيعمل فولدرات V1 و V2 و V3 لحد ما الهارد اتملى. و git-scm بيشرح الأوامر: status و add و commit و diff و log. ملفات الـ CAD كمان بتتغير كتير، فبنستخدم Git ليها هي والكود. البرنامج 1 بيعمل قصة Net Ninja بـ Git حقيقي من Python. والبرنامج 2 بيوري إزاي Git بيخزن: كل محتوى ببصمته، والمتشابه مرة واحدة. (محتاجين git متسطّب: <code>git --version</code>.)</p>''')
P.append(D1.fig(D.c_git(), 'الملف بيعدي على 3 أماكن، والـ 4 Commits بأرقامهم من التشغيل.'))
P.append(GIT_TABLE)
P.append('<h3 id="git-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(GIT_WORDS))
P.append('<h3>البرنامج 1: قصة Net Ninja بـ Git</h3><p class="what">توقّع: هيفضل في الفولدر كام ملف؟</p>'
         + prog(SRC + 'c1_git_record.py', 'git_record.py') + res(term(rd(SRC + 'c1_git_record.txt')) + '<p style="font-size:10pt">أرقام الـ Commits ثابتة كل تشغيلة لأننا ثبّتنا الاسم والتاريخ. لو شيلت ENV الأرقام هتتغير.</p>'))
P.append(SB14.d14_git())
P.append('<h3>البرنامج 2: Git بيخزن إزاي</h3><p class="what">توقّع: 3 ملفات = كام object؟</p>'
         + prog(SRC + 'c2_git_store.py', 'git_store.py') + res(term(rd(SRC + 'c2_git_store.txt'))))
P.append('<h3 id="why-git">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_git())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Git = Version Control موزّع: بيسجل التغييرات وترجع لأي نسخة، وكل واحد معاه نسخة كاملة.</li>
 <li>الحالات: Untracked (??) ← Staged (A) ← Committed، والمتغير Modified (M).</li>
 <li><code>git add</code> ثم <code>git commit -m</code>، و <code>-a</code> للملفات المتابعة.</li>
 <li><code>status</code> و <code>diff</code> و <code>log</code> عشان تشوف، و <code>checkout &lt;commit&gt; -- file</code> عشان ترجع.</li>
 <li>كل محتوى بيتسمى ببصمة SHA-1، فالمتشابه بيتخزن مرة. و GitHub = مكان على النت للـ Repository.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اعمل Repository لفولدر الكود بتاع الأسبوع ده، و commit لكل يوم. 2. غيّر ملف واعمل <code>git diff</code>. 3. اعمل ملف <code>.gitignore</code> فيه <code>*.o</code> وشوف status.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>Copy Constructor:</b> الـ class اللي بيمسك ذاكرة لازم يقرر النسخ معناه إيه: Deep Copy أو ممنوع.</td></tr>
 <tr><td class="n">2</td><td><b>Texture class:</b> نفس القاعدة لحاجة على الكارت: نسخة غلط = Texture اتمسح.</td></tr>
 <tr><td class="n">3</td><td><b>العكس:</b> التحويل اللي det بتاعه مش صفر ليه طريق رجوع. زي Git: بيحتفظ باللي يرجّعك.</td></tr>
 <tr><td class="n">4</td><td><b>Git:</b> بيحفظ كل نسخة من غير ما ينسخ المتشابه، وده نفس فكرة «ماتنسخش من غير لازمة».</td></tr>
</table>
<h3>بكره (الأحد 8-11، الأسبوع 4)</h3>
<ul><li>برمجة: Templates (The Cherno: Templates in C++).</li><li>رسم: Transformations (learnopengl).</li>
<li>رياضيات: ضرب المصفوفات = تركيب (3Blue1Brown: Essence of linear algebra 4).</li><li>الـ CAD: تحريك الأشكال 3D في OpenGL (Translate).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>Copying and Copy Constructors in C++: <span class="ltr">youtube.com/watch?v=BvR1Pgzzr38</span></li>
 <li>learnopengl: <span class="ltr">learnopengl.com</span></li>
 <li>Khan Matrix transformations: <span class="ltr">khanacademy.org/math/linear-algebra/matrix-transformations</span></li>
 <li>Git Basics - Recording Changes: <span class="ltr">git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository</span> · Why Use Git?: <span class="ltr">youtube.com/watch?v=3RjQznt-8kE</span></li></ul></section>''')
