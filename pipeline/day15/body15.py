# ================================================================== cover
P.append('''<section class="cover">
  <div class="kicker">خطة السنة الأولى · الأسبوع الرابع: Templates والتحويلات</div>
  <h1>اليوم الأول — الأحد 8 نوفمبر</h1>
  <div class="sub">كل كود هنا برنامج كامل: اكتبه زي ما هو، اعمله Run، هيشتغل</div>
  <table class="sched">
    <tr><td class="t"><span class="ltr">12:00 – 1:30</span></td><td><span class="dot" style="background:#2563eb"></span><b>البرمجة:</b> Templates — <span style="color:#5b6372">The Cherno</span></td></tr>
    <tr><td class="t"><span class="ltr">1:40 – 3:10</span></td><td><span class="dot" style="background:#0d9488"></span><b>الرسم:</b> تحويلات 2D والـ Homogeneous Coordinates — <span style="color:#5b6372">learnopengl و Cem Yuksel (محاضرة 5)</span></td></tr>
    <tr><td class="t"><span class="ltr">3:25 – 4:40</span></td><td><span class="dot" style="background:#c2410c"></span><b>الرياضيات:</b> ضرب المصفوفات = تركيب — <span style="color:#5b6372">3Blue1Brown (الفصل 4)</span></td></tr>
    <tr><td class="t"><span class="ltr">4:50 – 6:20</span></td><td><span class="dot" style="background:#7c3aed"></span><b>الـ CAD:</b> تحريك موديل 3D (Translate) — <span style="color:#5b6372">learnopengl و Code Imposter</span></td></tr>
  </table>
  <div class="howto"><b>كل كود فيه:</b> رسمة توضيحية، والبرنامج كامل وكل سطر جنبه شرحه، والكلمات الجديدة كلمة كلمة، ورسومات «خطوة بخطوة»، ومربع أخضر فيه اللي ظهر لما شغّلناه فعلاً. وفي آخر كل محاضرة قسم «ليه كتبنا كل ده؟» بالتجارب.</div>
  <div class="howto" style="margin-top:4mm;background:#fffbeb"><b>النهارده الأربعة مربوطين:</b> الـ Template بيخلي الـ compiler يكتب الكود (زي Array&lt;float, 3&gt; اللي هيبقى vec3 في GLM بكره). والتحويلات كلها مصفوفة واحدة بالـ Homogeneous، وضرب المصفوفات = تحويل ورا تحويل، والترتيب بيقرر الموديل يلف في مكانه ولا يدور في مدار.</div>
</section>''')

# ================================================================== 1 · templates
P.append(lec('l1', 'المحاضرة 1 · برمجة', 'Templates', 'The Cherno · Templates in C++ · <span class="ltr">youtu.be/I-hZkUa9mIs</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> الـ Template قالب: بتكتب الكود مرة بـ T، والـ compiler بيكتب نسخة حقيقية لكل نوع بتستخدمه. والقالب نفسه مش كود لحد ما تناديه.</div>
<p class="what">The Cherno بدأ بـ Print متكررة لـ int و string و float، وخلّاها Template واحد، ووضّح إن النوع بيتعرف لوحده أو بإيدك، وإن Template فيه غلطة بيترجم لو محدش ناداه. وبعدين عمل Array&lt;T, N&gt; على الـ Stack وقال إنه شبه std::array. البرنامج 1 بيطبع النسخة اللي الـ compiler عملها فعلاً. والبرنامج 2 بيعمل Array بأنواع وأحجام مختلفة.</p>''')
P.append(D1.fig(D.p_tpl(), 'من Template واحد طلعت 4 دوال حقيقية (الأنواع من التشغيل).'))
P.append(TPL_TABLE)
P.append('<h3 id="tpl-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(TPL_WORDS))
P.append('<h3>البرنامج 1: Print و Biggest</h3><p class="what">توقّع: Print("Hello") هيبقى T إيه؟</p>'
         + prog(SRC + 'p1_print_template.cpp', 'print_template.cpp') + res(term(rd(SRC + 'p1_print_template.txt'))))
P.append('<h3>البرنامج 2: Array&lt;T, N&gt;</h3><p class="what">توقّع sizeof لكل واحدة.</p>'
         + prog(SRC + 'p2_array_template.cpp', 'array_template.cpp') + res(term(rd(SRC + 'p2_array_template.txt'))))
P.append('<h3 id="why-tpl">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_tpl() + '<h3>البرنامج 2</h3>' + WHY.build_arr())
P.append('''<div class="sum"><b>الملخص:</b><ul><li><code>template&lt;typename T&gt;</code> قبل الدالة أو الـ class (و class زي typename).</li>
 <li>النوع بيتعرف من القيم، أو بإيدك <code>Print&lt;int&gt;(…)</code>.</li>
 <li>الـ compiler بيعمل نسخة لكل نوع، والقالب اللي محدش ناداه مابيتعملش.</li>
 <li>البارامتر ممكن يبقى رقم ثابت: <code>template&lt;typename T, int N&gt;</code>، وده Metaprogramming.</li>
 <li>The Cherno: استخدمها (Logging و Materials)، بس لو بقت محدش فاهمها يبقى زودتها.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. اعمل <code>template&lt;typename T&gt; T Smallest(T a, T b)</code>. 2. زوّد في Array دالة <code>Fill(T value)</code>. 3. نادي <code>Biggest&lt;double&gt;(3, 1.5)</code>: اشتغلت؟</div></section>''')

# ================================================================== 2 · 2D transforms
P.append(lec('l2', 'المحاضرة 2 · رسم', 'تحويلات 2D والـ Homogeneous Coordinates', '<span class="ltr">learnopengl.com/Getting-started/Transformations</span> · Cem Yuksel · Intro to Graphics 05 - 2D Transformations · <span class="ltr">youtu.be/EKN7dTJ4ep8</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> التحريك والدوران والتكبير (Affine) بيبنوا المشهد: نحط الكراسي حوالين الترابيزة. الدوران والتكبير ضرب في مصفوفة، والتحريك جمع. فبنزوّد رقم تالت (Homogeneous) فيبقى كله ضرب، وكل التحويلات ورا بعض = مصفوفة 3 × 3 واحدة.</div>
<p class="what">Cem Yuksel شرح التحريك (p + t)، والتكبير (sx و sy على القطر)، والدوران (cos و sin)، وإن مصفوفة الدوران Orthogonal فعكسها الـ Transpose، وإن الـ Skew = دوران وتكبير ودوران. وبعدين: إزاي تلف حوالين المركز (تحريك، لف، تحريك عكسي)، والـ Homogeneous Coordinates، والصف 0 0 1، و w = 1 للنقطة و w = 0 للاتجاه. البرنامج 1 بيرسم بيت بـ 4 مصفوفات بنكتبها بإيدنا في الـ Shader (من غير GLM لسه). والبرنامج 2 بيطبع الأرقام.</p>''')
P.append(D1.fig(D.t_steps(), 'اللف حوالين المركز، وشكل المصفوفة 3 × 3، والنقطة مقابل الاتجاه.'))
P.append(TR_TABLE)
P.append('<h3 id="tr-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(TR_WORDS))
P.append('<div class="setup"><b>قبل ما تشغّل:</b> نفس إعداد كل يوم (GLFW و GLAD). مفيش صور. الترجمة: <code>g++ transform2d.cpp</code> + المكتبات. والبرنامج 2 Terminal بس: <code>g++ homogeneous.cpp</code>. والشباك بيتقفل بـ Esc.</div>')
P.append('<h3>البرنامج 1: بيت بـ 4 مصفوفات</h3><p class="what">رمادي = الأصل، أزرق = لف حوالين (0, 0)، برتقاني = لف حوالين المركز، أخضر = تكبير وتحريك.</p>'
         + prog(SRC + 't1_transform2d.cpp', 'transform2d.cpp')
         + res(term(rd(SRC + 't1_transform2d.txt')) + bigimg('t1_transform2d', 'الشباك الحقيقي: الأزرق طار شمال (لف حوالين الأصل)، والبرتقاني لف في مكانه فوق الرمادي.', '110mm'), '▶ النتيجة لما نعمل Run (الشباك الحقيقي، وبعدين Esc)'))
P.append('<h3>البرنامج 2: Homogeneous بالأرقام</h3><p class="what">توقّع: الاتجاه (1, 0) هيتحرك؟</p>'
         + prog(SRC + 't2_homogeneous.cpp', 'homogeneous.cpp') + res(term(rd(SRC + 't2_homogeneous.txt'))))
P.append(SB15.d15_hom())
P.append('<h3 id="why-tr">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + '<h3>البرنامج 1</h3>' + WHY.build_tr() + '<h3>البرنامج 2</h3>' + WHY.build_hom())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Affine = تحريك ودوران وتكبير: الخطوط بتفضل خطوط والمتوازي متوازي.</li>
 <li>الدوران Orthogonal: R⁻¹ = Rᵀ. وأي 2 × 2 = دوران × تكبير × دوران (SVD).</li>
 <li>Homogeneous: (x, y, 1) ومصفوفة 3 × 3 آخر صف فيها 0 0 1، فالتحريك يبقى ضرب.</li>
 <li>حوالين المركز: T(c) R T(‎-c)، ويتقرا من اليمين.</li>
 <li>w = 1 نقطة، و w = 0 اتجاه. ونبعت المصفوفة بـ GL_TRUE لو مكتوبة صف صف.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. خلّي البرتقاني يلف 45 بدل 90. 2. اعمل بيت خامس متكبر حوالين مركزه (T S T⁻¹). 3. في البرنامج 2 اطبع R(45) S R(‎-45) × (1, ‎-1).</div></section>''')

# ================================================================== 3 · composition
P.append(lec('l3', 'المحاضرة 3 · رياضيات', 'ضرب المصفوفات = تركيب', '3Blue1Brown · Matrix multiplication as composition | Chapter 4, Essence of linear algebra · <span class="ltr">youtu.be/XkY2DOUCWMU</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> لما تعمل تحويل وبعده تحويل، النتيجة تحويل واحد، ومصفوفته = حاصل ضرب المصفوفتين. وبنقرا من اليمين: اللي على اليمين بيحصل الأول.</div>
<p class="what">3Blue1Brown عمل دوران 90 وبعده Shear، وتابع î و ĵ: (1, 1) و (‎-1, 0). وحسب M2 M1 عمود عمود، ووضّح إن الترتيب بيفرق، وإن التجميع (Associativity) بديهي. البرنامج 1 نفس أمثلته بالظبط. والبرنامج 2 بيرسم الشبكة بعد الترتيبين.</p>''')
P.append(D1.fig(D.m_cols(), 'M2 @ M1 عمود عمود (من التشغيل).'))
P.append(MAT_TABLE)
P.append('<h3 id="mat-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(MAT_WORDS))
P.append('<h3>البرنامج 1: أمثلة 3Blue1Brown</h3><p class="what">احسب M2 @ M1 في ورقة الأول.</p>'
         + prog(SRC + 'm1_composition.py', 'composition.py') + res(term(rd(SRC + 'm1_composition.txt'))))
P.append('<h3>البرنامج 2: الشبكة بالترتيبين</h3><p class="what">توقّع: الأخضر (î) هيروح فين في كل رسمة؟</p>'
         + prog(SRC + 'm2_grid_plot.py', 'grid_plot.py') + res(term(rd(SRC + 'm2_grid_plot.txt')) + bigimg('m2_composition', 'composition.png اللي البرنامج حفظها: نفس التحويلين، ترتيب مختلف، شبكة مختلفة.', '130mm')))
P.append('<h3 id="why-mat">ليه كتبنا كل ده؟</h3>' + LEGEND + WHY.build_mat())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>التحويل الخطي بيتحدد بـ î و ĵ راحوا فين (أعمدة المصفوفة).</li>
 <li>A @ B = B الأول وبعدين A (من اليمين للشمال).</li>
 <li>العمود k في A @ B = A × العمود k من B.</li>
 <li>A @ B ≠ B @ A غالباً، و (A @ B) @ C = A @ (B @ C) دايماً.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. احسب rotation @ rotation: ده دوران كام؟ 2. اعمل Shear تاني [[1, 0], [1, 1]] وقارن الترتيبين. 3. ارسم الشبكة بعد 3 تحويلات.</div></section>''')

# ================================================================== 4 · translate 3D
P.append(lec('l4', 'المحاضرة 4 · CAD', 'تحريك موديل 3D (Translate)', '<span class="ltr">learnopengl.com/Getting-started/Transformations</span> · Code Imposter · How to Translate (Move) 3D Models in OpenGL · <span class="ltr">youtu.be/k38jO_x8W0c</span>'))
P.append('''<div class="idea"><b>الفكرة في سطر:</b> في 3D المصفوفة 4 × 4: Identity وعمود رابع فيه التحريك. الركن (x, y, z, 1) بيتحرك والـ Normal (w = 0) لأ. ولما تجمع تحريك ودوران: T * R = لف في المكان، و R * T = مدار.</div>
<p class="what">Code Imposter شرح مصفوفة التحريك و glm::translate، والـ Animation بنسبة بتزيد، وإن الـ Normals ماتتحركش، وإن ترتيب T و R بيفرق: الموديل يلف على نفسه أو يدور حوالين المركز. البرنامج 1 بيضرب مصفوفة 4 × 4 بإيدنا (بكره GLM هتعملها). والبرنامج 2 بيقارن الترتيبين في 4 زوايا.</p>''')
P.append(D1.fig(D.c_orbit(), 'الترتيبين: الأزرق ثابت بيلف، والبرتقاني بيدور (المراكز من التشغيل).'))
P.append(CAD_TABLE)
P.append('<h3 id="cad-words">الكلمات الجديدة كلمة كلمة</h3>' + ''.join(CAD_WORDS))
P.append('<h3>البرنامج 1: مصفوفة التحريك 4 × 4</h3><p class="what">احسب T × (1, ‎-1, 2, 1).</p>'
         + prog(SRC + 'c1_translate4x4.cpp', 'translate4x4.cpp') + res(term(rd(SRC + 'c1_translate4x4.txt'))))
P.append('<h3>البرنامج 2: T * R مقابل R * T</h3><p class="what">توقّع المركز عند 180 في الاتنين.</p>'
         + prog(SRC + 'c2_order.cpp', 'order.cpp') + res(term(rd(SRC + 'c2_order.txt'))))
P.append('<h3 id="why-cad">ليه كتبنا كل ده؟ وإيه اللي يحصل لو غلطت؟</h3>' + LEGEND + WHY.build_cad())
P.append('''<div class="sum"><b>الملخص:</b><ul><li>Translate في 3D: [1 0 0 tx] [0 1 0 ty] [0 0 1 tz] [0 0 0 1].</li>
 <li>في الـ Shader: <code>gl_Position = matrix * aPos;</code> و glm::translate بتعمل المصفوفة.</li>
 <li>الـ Normal ماتتحركش: w = 0.</li>
 <li>T * R = لف في المكان، و R * T = مدار حوالين المركز.</li></ul></div>
<div class="try"><b>جرّب بإيدك:</b> 1. خلّي الـ Animation رايح جاي (النسبة من 0 لـ 1 وترجع). 2. في البرنامج 2 جرّب 45 درجة. 3. اعمل RotateX وقارن.</div></section>''')

# ================================================================== links
P.append('''<section class="final"><h2>إزاي الأربعة مرتبطين؟</h2>
<table class="flow">
 <tr><td class="n">1</td><td><b>Templates:</b> مكتبة GLM بكره كلها Templates (vec3 و mat4 لأي نوع).</td></tr>
 <tr><td class="n">2</td><td><b>Homogeneous:</b> التحريك بقى ضرب، فكل التحويلات مصفوفة واحدة نبعتها للـ Shader.</td></tr>
 <tr><td class="n">3</td><td><b>التركيب:</b> الضرب = تحويل ورا تحويل، ومن اليمين.</td></tr>
 <tr><td class="n">4</td><td><b>3D:</b> نفس الكلام 4 × 4، والترتيب = لف في المكان أو مدار.</td></tr>
</table>
<h3>بكره (الاثنين 9-11)</h3>
<ul><li>برمجة: Function Templates (cppreference و The Cherno).</li><li>رسم: مكتبة GLM.</li>
<li>رياضيات: أمثلة ضرب المصفوفات (Khan Academy).</li><li>الـ CAD: Translation Transformation (OpenGL Tutorial 6).</li></ul>
<h3>المصادر</h3><ul style="font-size:10pt">
 <li>Templates in C++: <span class="ltr">youtube.com/watch?v=I-hZkUa9mIs</span></li>
 <li>learnopengl Transformations: <span class="ltr">learnopengl.com/Getting-started/Transformations</span> · Intro to Graphics 05 - 2D Transformations: <span class="ltr">youtube.com/watch?v=EKN7dTJ4ep8</span></li>
 <li>Matrix multiplication as composition: <span class="ltr">youtube.com/watch?v=XkY2DOUCWMU</span></li>
 <li>How to Translate (Move) 3D Models in OpenGL: <span class="ltr">youtube.com/watch?v=k38jO_x8W0c</span></li></ul></section>''')
