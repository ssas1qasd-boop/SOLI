# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الثالث: الـ Classes والـ Textures</div>
  <h1>اليوم الثالث — التلات 3 نوفمبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> Constructors و Destructors — <span style="color:#5b6372">The Cherno (الحلقة 25 و 26)</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> Texture على مستطيل — <span style="color:#5b6372">learnopengl و Victor Gordan و Cem Yuksel (محاضرة 13)</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> التحويل الخطي = مصفوفة × متجه — <span style="color:#5b6372">Khan Academy (تمارين)</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> رسم مخطط B-Rep بإيدك — <span style="color:#5b6372">Glen Gray و Wikipedia</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:4mm;background:#fffbeb"><b>النهارده الأربعة مربوطين:</b> الـ Constructor والـ Destructor بقوا Texture class. وأي تحريك للمستطيل = مصفوفة. ووش الـ B-Rep سطح S(u, v) زي إحداثيات الـ Texture.</div>
</section>''')

# ================================================================== 1 · constructors & destructors
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'Constructors و Destructors', 'The Cherno · Constructors in C++ (الحلقة 25) · <span class="ltr">youtu.be/FXhALMsHwEY</span> · و Destructors in C++ (الحلقة 26)'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Constructor دالة بتشتغل لوحدها لما الـ object يتولد (عشان يحط قيم)، والـ Destructor بتشتغل لوحدها لما يموت (عشان يرجّع اللي حجزه).</div>
<p class="what">The Cherno بدأ بـ Entity فيه x و y من غير قيم، وطبع أرقام عجيبة. في C++ (عكس Java) الأرقام مش بتبقى صفر لوحدها. البرنامج 1 بيوري ده، وبعدين الـ Constructor الفاضي، والـ Constructor برقمين (Overloading)، و <code>Log() = delete</code>. والبرنامج 2 بيطبع «Created» و «Destroyed» عشان نشوف الـ object بيموت إمتى: على الـ Stack، وعلى الـ Heap، و class بيحجز ذاكرة ويرجّعها.</p>''')
P.append(D1.fig(D.p_choose(), 'كل سطر في main والـ Constructor اللي الـ compiler اختاره، واللي اتطبع (من التشغيل). و NoInit مالوش Constructor: اتطبع أرقام عجيبة.'))
P.append(CTOR_TABLE)
P.append('<h3 id="ctor-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CTOR_WORDS))
P.append('<h3>البرنامج 1: Entity بتاع The Cherno</h3><p class="what">قبل ما تشغّل: توقّع أول سطر هيطبع إيه.</p>'
         + prog(SRC + 'p1_constructor.cpp', 'constructor.cpp') + res(term(rd(SRC + 'p1_constructor.txt')) + '<p style="font-size:10pt">أول سطر أرقام عجيبة، وبتتغير كل مرة تشغّل (جرّبها مرتين). وبعده كل Constructor طبع اسمه قبل القيم.</p>'))
P.append(SB10.d10_ctor())
P.append(DTOR_TABLE)
P.append('<h3 id="dtor-words">كلمات الـ Destructor</h3>' + ''.join(DTOR_WORDS))
P.append('<h3>البرنامج 2: إمتى الـ object بيموت؟</h3><p class="what">توقّع ترتيب السطور قبل ما تشغّل.</p>'
         + prog(SRC + 'p2_destructor.cpp', 'destructor.cpp') + res(term(rd(SRC + 'p2_destructor.txt')) + '<p style="font-size:10pt">Destroyed بتاع Function قبل «back in main». وبتاع الـ Heap بعد <code>delete</code> بس. و ~Buffer قبل «after the { }».</p>'))
P.append(D1.fig(D.p_life(), 'نفس سطور التشغيل: كل عمود ملوّن = عمر object، من Created لحد Destroyed.'))
P.append(SB10.d10_dtor())
P.append('<h3 id="why-ctor">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_ctor() + '<h3>البرنامج 2</h3>' + WHY.build_dtor())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>الـ Constructor: نفس اسم الـ class، ومالوش نوع راجع، وبيشتغل لوحده.</li>
 <li>من غير Constructor: القيم «زبالة» (C++ مش بيحط أصفار).</li>
 <li>ممكن أكتر من Constructor (Overloading)، والـ compiler بيختار حسب القوسين.</li>
 <li><code>this-&gt;x</code> = x بتاع الـ object لما الاسم متكرر.</li>
 <li><code>= delete</code> أو <code>private</code> = ممنوع تعمل object.</li>
 <li>الـ Destructor (<code>~</code>): عند الـ <code>}</code> للـ Stack، وعند <code>delete</code> للـ Heap. واللي الـ Constructor يحجزه هو يرجّعه.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. زوّد في Entity Constructor بياخد رقم واحد ويحطه في x و y. 2. اعمل اتنين Entity جوه <code>{ }</code> وشوف مين يموت الأول. 3. شيل <code>delete e3;</code> وشغّل بـ <code>valgrind ./constructor</code>.</div></section>''')

# ================================================================== 2 · texture class on a rectangle
P.append(lec('l2', 'المحاضرة 2 · رسم', 'Texture على مستطيل (Texture class)', 'learnopengl · Getting started: Textures · Victor Gordan · OpenGL Tutorial 6 - Textures · <span class="ltr">youtu.be/u-00hjlfMKc</span> · Cem Yuksel · Intro to Graphics 13 - Textures · <span class="ltr">youtu.be/Yjv6hc4Zqjk</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> كل شغل الـ Texture بتاع امبارح بقى class: الـ Constructor بيحمّل ويرفع للكارت، والـ Destructor بيمسح. وصورتين في نفس الوقت = خانتين (Texture Units) و <code>mix</code>.</div>
<p class="what">Victor Gordan في آخر الفيديو: «نقدر نعمل Class خاص بالـ Texture عشان الكود يبقى منظم». البرنامج 1 بيرسم صندوق (64 × 64، 3 قنوات) على مستطيل، وكل ركن ليه لون بيتضرب في الصورة (طريقة learnopengl). والبرنامج 2 بيحط وش (32 × 32، 4 قنوات) فوق الصندوق بـ <code>mix</code>.</p>''')
P.append(D1.fig(D.t_class(), 'الـ class بيختار RGB أو RGBA من عدد القنوات. وكل object في خانة، والـ Shader بيعرف الخانة من <code>glUniform1i</code>. والأرقام من التشغيل.'))
P.append(TEX_TABLE)
P.append('<h3 id="tex-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(TEX_WORDS))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD)، و <code>stb_image.h</code> و <code>stb.cpp</code> بتوع امبارح جنب الكود، وفولدر <code>res</code> فيه الصورتين. الترجمة: <code>g++ crate.cpp stb.cpp</code> + مكتبات امبارح. والشباك بيتقفل بـ Esc.</div>' + '<div class="exrow">' + bigimg('crate_src', 'res/crate.png مكبّرة (64 × 64، 3 قنوات)', '30mm') + bigimg('face_src', 'res/face.png مكبّرة (32 × 32، الخلفية شفافة)', '30mm') + '</div>')
P.append('<h3>البرنامج 1: صندوق بـ Texture class</h3><p class="what">الأركان 7 أرقام: x و y، ولون (r, g, b)، و (u, v).</p>'
         + prog(SRC + 't1_crate.cpp', 'crate.cpp')
         + res(term(rd(SRC + 't1_crate.txt')) + bigimg('t1_crate', 'الصندوق × ألوان الأركان: تحت شمال مايل للأحمر، وتحت يمين للأخضر، وفوق يمين للأزرق، وفوق شمال أبيض.') + '<p style="font-size:10pt">السطور دي اتطبعت لما ضغطنا Esc: اللوب خلصت، وبعدين الـ <code>}</code> شغّلت الـ ~Texture، وبعدين <code>glfwTerminate</code>.</p>', '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append('<h3>البرنامج 2: صورتين في خانتين</h3><p class="what">نفس البرنامج + Texture تاني + <code>tex1</code> + <code>mix</code>.</p>'
         + prog(SRC + 't2_two_textures.cpp', 'two_textures.cpp')
         + res(term(rd(SRC + 't2_two_textures.txt')) + bigimg('t2_two_textures', 'الوش متكرر 2 × 2 (الإحداثيات × 2 و REPEAT)، والصندوق باين من الأماكن الشفافة.') + '<p style="font-size:10pt">لاحظ الترتيب: ID 2 اتمسح قبل ID 1. اللي اتعمل الأخير بيموت الأول.</p>', '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append('<h3 id="why-tex">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_crate() + '<h3>البرنامج 2</h3>' + WHY.build_two())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Texture class: الـ Constructor = <code>stbi_load</code> + <code>glGenTextures</code> + الإعدادات + <code>glTexImage2D</code> + Mipmaps + <code>stbi_image_free</code>.</li>
 <li>الـ Destructor = <code>glDeleteTextures</code>، ولازم قبل <code>glfwTerminate</code> (عشان كده الـ <code>{ }</code>).</li>
 <li>الـ format من عدد القنوات: 3 ← RGB و 4 ← RGBA.</li>
 <li>صورتين: <code>glActiveTexture(GL_TEXTURE0 + n)</code> + <code>glUniform1i(sampler, n)</code>.</li>
 <li><code>mix(a, b, t)</code> = a × (1 - t) + b × t.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. خلّي amount = 0.3. 2. خلّي الوش × 4 بدل × 2. 3. زوّد في الـ class دالة <code>void Unbind()</code> تعمل <code>glBindTexture(GL_TEXTURE_2D, 0)</code>.</div></section>''')

# ================================================================== 3 · matrix-vector products
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'التحويل الخطي = مصفوفة × متجه', 'Khan Academy · Linear transformations as matrix vector products · <span class="ltr">youtu.be/PErhLkQcpZ8</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> أي تحويل خطي T نكتبه مصفوفة: حط T(e₁) و T(e₂) كأعمدة. ليه؟ لأن x = x₁ e₁ + x₂ e₂، و T خطي، فـ T(x) = x₁ T(e₁) + x₂ T(e₂).</div>
<p class="what">Khan بدأ بمصفوفة الوحدة Iₙ (آحاد على القطر) والقاعدة المعيارية (أعمدتها e₁ و e₂ و e₃). البرنامج 1 بيعمل مثال الفيديو بالظبط: T(x₁, x₂) = (x₁ + 3x₂, 5x₂ - x₁, 4x₁ + x₂) من ℝ² لـ ℝ³، ويبني A من الأعمدة. والبرنامج 2 تمارين: 4 تحويلات على حرف F، كل مصفوفة مبنية من «e₁ راح فين و e₂ راح فين». (محتاجين <code>pip install numpy matplotlib</code>)</p>''')
P.append(D1.fig(D.m_columns(), 'من الفيديو: T(e₁) و T(e₂) بقوا عمودين، فـ A مقاسها 3 × 2. و A × (1, 1) = مجموع العمودين.'))
P.append(MAT_TABLE)
P.append('<h3 id="mat-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(MAT_WORDS))
P.append('<h3>البرنامج 1: مثال Khan بالظبط</h3><p class="what">احسب T(e₁) و T(e₂) في ورقة الأول.</p>'
         + prog(SRC + 'm1_matrix_columns.py', 'matrix_columns.py') + res(term(rd(SRC + 'm1_matrix_columns.txt')) + '<p style="font-size:10pt">نفس نتايج الفيديو: T(e₁) = (1, ‎-1, 4) و T(e₂) = (3, 5, 1). والدالة والمصفوفة طلعوا نفس الرقم في التلاتة.</p>'))
P.append('<h3>البرنامج 2: تمارين: 4 مصفوفات على حرف F</h3><p class="what">قبل التشغيل: لف 90 درجة، الركن (2, 3) هيروح فين؟</p>'
         + prog(SRC + 'm2_shape_transforms.py', 'shape_transforms.py') + res(term(rd(SRC + 'm2_shape_transforms.txt')) + bigimg('m2_shapes', 'shapes.png اللي البرنامج حفظها: الرمادي الأصل والبرتقاني بعد التحويل. السهم الأزرق = العمود الأول، والأخضر = التاني.', '160mm')))
P.append('<h3 id="why-mat">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_mat())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Iₙ: آحاد على القطر، و Iₙ x = x.</li>
 <li>القاعدة المعيارية: e₁ و e₂ و e₃ = أعمدة Iₙ.</li>
 <li>A = [T(e₁) | T(e₂)]: كل عمود = e راح فين.</li>
 <li>من ℝⁿ لـ ℝᵐ: m صف و n عمود.</li>
 <li>عشان تعمل مصفوفة لأي تحويل في الرسم: ارسم e₁ و e₂ بعد التحويل واكتبهم أعمدة.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. ابني مصفوفة لف 180 درجة (e₁ و e₂ يروحوا فين؟). 2. اضرب مصفوفة اللف 90 في نفسها وقارن بالـ 180. 3. زوّد في البرنامج 2 تحويل «تكبير × 0.5 في الاتجاهين».</div></section>''')

# ================================================================== 4 · B-Rep by hand
P.append(lec('l4', 'المحاضرة 4 · CAD', 'رسم مخطط B-Rep بإيدك', 'Glen Gray · Geometric Modeling - Boundary Representations (BREP) · <span class="ltr">youtu.be/sXbRT439vRI</span> · <span class="ltr">en.wikipedia.org/wiki/Boundary_representation</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ B-Rep بيخزّن الجسم بحدوده: Shell ← وشوش (سطوح S(u, v)) ← حلقات ← أضلاع (منحنيات C(t)) ← أركان. والخرم مش بيغيّر السطح: حلقة زيادة بتقول «المنطقة دي مش من الوش».</div>
<p class="what">Glen Gray شرح الأسطوانة: 3 وشوش (غطا وجنب وقاع)، و 3 أضلاع (دايرتين وخط لحام)، و 2 ركن. البرنامج 1 بيكتب المخطط ده كـ structs ويتأكد إن كل ضلع متلمس مرتين (Manifold). والبرنامج 2 صندوق فيه خرم (الحلقة التانية = Trim Loop) ومكعبين بيلمسوا بعض في ضلع (شكل مش Manifold زي اللي في الفيديو).</p>''')
P.append(D1.fig(D.c_cyl(), 'المخطط اللي تكتبه بإيدك للأسطوانة. وعلى اليمين الجنب مفرود: مستطيل في (u, v)، وحرفه الشمال واليمين نفس خط اللحام e1.'))
P.append(BREP_TABLE)
P.append('<h3 id="brep-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(BREP_WORDS))
P.append('<h3>البرنامج 1: مخطط الأسطوانة</h3><p class="what">ارسم المخطط في ورقة الأول (زي الرسمة)، وبعدين قارن بالمطبوع.</p>'
         + prog(SRC + 'c1_brep_cylinder.cpp', 'brep_cylinder.cpp') + res(term(rd(SRC + 'c1_brep_cylinder.txt')) + '<p style="font-size:10pt">‎-4.37114e-08 مكان الصفر: cos(ط/2) بـ float مش بيطلع صفر بالظبط. ده طبيعي في أي برنامج CAD، وعشان كده بنقارن بـ «قريب من» مش «يساوي».</p>'))
P.append(SB10.d10_brep())
P.append('<h3>البرنامج 2: صندوق بخرم، ومكعبين في ضلع</h3><p class="what">توقّع: V - E + F للصندوق بالخرم كام؟</p>'
         + prog(SRC + 'c2_brep_hole.cpp', 'brep_hole.cpp') + res(term(rd(SRC + 'c2_brep_hole.txt'))))
P.append(D1.fig(D.c_hole(), 'الغطا وش واحد بحلقتين. الحلقة البرتقاني (الخرم) عكس اتجاه الحلقة برّه.'))
P.append('<h3 id="why-brep">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_cyl() + '<h3>البرنامج 2</h3>' + WHY.build_hole())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>B-Rep: Shell ← Faces ← Loops ← Edges ← Vertices.</li>
 <li>الضلع = منحنى C(t) محدود بركنين، والوش = سطح S(u, v) محدود بحلقات.</li>
 <li>الحلقة الأولى حدود الوش، والباقي خروم (Trim Loops). الخرم مش بيغيّر السطح.</li>
 <li>Manifold = كل ضلع متلمس مرتين بالظبط. غير كده الشكل مايتصنعش.</li>
 <li>مع الخروم: V - E + F - (L - F) = 2(S - G).</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. ارسم مخطط المكعب بإيدك (8 و 12 و 6) واكتبه زي البرنامج 2. 2. ارسم مخطط كورة: وش واحد؟ كام ضلع؟ 3. في البرنامج 2 خلّي الخرم مش واصل لتحت (قاع للخرم من جوه) واحسب V و E و F.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>Constructors و Destructors:</b> بقوا Texture class: سطر واحد يحمّل الصورة، والـ <code>}</code> تمسحها.</td></tr>
 <tr><td class="n">2</td><td><b>Texture على مستطيل:</b> كل ركن ليه (u, v)، والكارت بيلزق الصورة على السطح. نفس فكرة S(u, v) في الـ B-Rep.</td></tr>
 <tr><td class="n">3</td><td><b>مصفوفة × متجه:</b> أي تحريك للمستطيل (لف، تكبير، ميل) = مصفوفة أعمدتها e راح فين. والخطوة الجاية نحطها في الـ Shader.</td></tr>
 <tr><td class="n">4</td><td><b>B-Rep:</b> الأسطوانة والصندوق بالخرم بقوا structs، وعرفنا نتأكد إن الشكل مقفول.</td></tr>
</table>
<h3>بكره (الأربع 4-11)</h3>
<ul><li>برمجة: Stack و Heap (The Cherno، الحلقة 54).</li><li>رسم: Texture wrapping (learnopengl، و Cem Yuksel محاضرة 14).</li>
<li>رياضيات: جمع وطرح المصفوفات (Khan Academy).</li><li>الـ CAD: مقارنة mesh و B-Rep (Wikipedia).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>Constructors in C++: <span class="ltr">youtube.com/watch?v=FXhALMsHwEY</span></li>
 <li>learnopengl Textures: <span class="ltr">learnopengl.com/Getting-started/Textures</span> · OpenGL Tutorial 6 - Textures: <span class="ltr">youtube.com/watch?v=u-00hjlfMKc</span> · Intro to Graphics 13 - Textures: <span class="ltr">youtube.com/watch?v=Yjv6hc4Zqjk</span></li>
 <li>Linear transformations as matrix vector products: <span class="ltr">youtube.com/watch?v=PErhLkQcpZ8</span> · <span class="ltr">khanacademy.org/math/linear-algebra/matrix-transformations</span></li>
 <li>Geometric Modeling - Boundary Representations (BREP): <span class="ltr">youtube.com/watch?v=sXbRT439vRI</span> · <span class="ltr">en.wikipedia.org/wiki/Boundary_representation</span></li></ul></section>''')

