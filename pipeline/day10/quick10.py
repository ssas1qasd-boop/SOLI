import sys
sys.path.insert(0, '/home/claude/day2')
from quick import card

DAY10_CARDS = [
 card('#2563eb', 'البرمجة: Constructors و Destructors', [
   'الـ Constructor = دالة بنفس اسم الـ class ومالهاش نوع راجع. بتشتغل لوحدها لما الـ object يتعمل.',
   'من غير Constructor، C++ مش بيحط قيم: أرقام «زبالة».',
   'الـ Destructor = <code>~</code> + اسم الـ class. بيشتغل عند الـ <code>}</code> (Stack) أو <code>delete</code> (Heap).',
   'اللي الـ Constructor يحجزه، الـ Destructor يرجّعه.'],
   ['Entity(float x, float y) { this->x = x; this->y = y; }', '~Buffer() { delete[] data; }'],
   'تكتب <code>x = x;</code> بدل <code>this-&gt;x = x;</code>: بيترجم عادي والقيم بتفضل «زبالة».', '<code>constructor.cpp</code> و <code>destructor.cpp</code>.'),
 card('#0d9488', 'الرسم: Texture class على مستطيل', [
   'الـ Constructor: <code>stbi_load</code> + <code>glGenTextures</code> + الإعدادات + <code>glTexImage2D</code> + Mipmaps.',
   'الـ format من عدد القنوات: 3 ← <code>GL_RGB</code>، و 4 ← <code>GL_RGBA</code>.',
   'Texture Units: <code>glActiveTexture(GL_TEXTURE0 + unit)</code>، و <code>glUniform1i</code> لكل sampler.',
   'الـ Texture لازم يموت قبل <code>glfwTerminate</code>.'],
   ['Texture crate("res/crate.png");  crate.Bind(0);', 'FragColor = mix(texture(tex0, texCoord), face, face.a * amount);'],
   'تسيب الـ Texture يموت بعد <code>glfwTerminate</code>: البرنامج بيقع (Segmentation fault).', '<code>crate.cpp</code> و <code>two_textures.cpp</code>.'),
 card('#c2410c', 'الرياضيات: التحويل = مصفوفة × متجه', [
   'مصفوفة الوحدة Iₙ: آحاد على القطر. و Iₙ x = x.',
   'القاعدة المعيارية e₁ و e₂ = أعمدة Iₙ، وأي متجه = x₁ e₁ + x₂ e₂.',
   'A = [T(e₁) | T(e₂)]: كل عمود = e راح فين.',
   'من ℝⁿ لـ ℝᵐ: المصفوفة m × n.'],
   ['A = np.column_stack([T(e1), T(e2)])   # 3 x 2', 'A @ (1, 1) = (4, 4, 5) = T(1, 1)'],
   'تحط T(e₁) و T(e₂) صفوف بدل أعمدة: المقاس بيتقلب، أو النتيجة بتطلع غلط من غير أي خطأ.', '<code>matrix_columns.py</code> و <code>shape_transforms.py</code>.'),
 card('#7c3aed', 'الـ CAD: مخطط B-Rep', [
   'Shell ← Faces ← Loops ← Edges ← Vertices.',
   'الضلع = منحنى C(t) بين ركنين، والوش = سطح S(u, v) مقصوص بحلقات.',
   'الحلقة الأولى حدود الوش، والباقي خروم (Trim Loops).',
   'Manifold: كل ضلع بيتلمس مرتين بالظبط.'],
   ['cylinder: V = 2, E = 3, F = 3, V - E + F = 2', 'box with a hole: V - E + F - (loops - F) = 0'],
   'تعتمد على V - E + F بس: الصندوق بالخرم طلع 2 زي المكعب، والصح بالحلقات 0.', '<code>brep_cylinder.cpp</code> و <code>brep_hole.cpp</code>.'),
]

DAY10_QA = [
 ('البرمجة: Constructors و Destructors', [
   ('<code>class A { public: A(int n) { } };</code> وفي main <code>A a;</code>. يترجم؟', 'لأ: مفيش Constructor فاضي. لما كتبنا واحد بياخد رقم، C++ بطّل يعمل الفاضي.'),
   ('إيه الفرق بين <code>Log() = delete;</code> و <code>private: Log() { }</code>؟', 'الاتنين بيمنعوا <code>Log l;</code>. الأولى بتقول «الدالة دي مش موجودة خالص».'),
   ('<code>Entity* p = new Entity();</code> ونسيت <code>delete p;</code>. الـ Destructor هيشتغل؟', 'لأ، ولا مرة. والـ 8 بايت ضايعين (valgrind قالها).'),
   ('جوه <code>{ }</code>: <code>Entity a; Entity b;</code>. مين يموت الأول؟', 'b: الأخير يموت الأول (زي الـ Texture: ID 2 قبل ID 1).')]),
 ('الرسم: Texture class', [
   ('صورة JPG (3 قنوات). <code>format</code> = ؟', '<code>GL_RGB</code>.'),
   ('صورتين في الـ Shader (tex0 و tex1). إيه السطرين اللي لازم في C++؟', '<code>glUniform1i(glGetUniformLocation(shaderProgram, "tex1"), 1);</code> و <code>face.Bind(1);</code> (جواها <code>glActiveTexture(GL_TEXTURE1)</code>).'),
   ('<code>mix(a, b, 0.0)</code> = ؟ و <code>mix(a, b, 1.0)</code> = ؟', 'a، و b.'),
   ('ليه الـ Texture جوه <code>{ }</code> قبل اللوب؟', 'عشان الـ Destructor (glDeleteTextures) يشتغل والشباك لسه مفتوح.')]),
 ('الرياضيات: المصفوفات', [
   ('I₃ × (7, ‎-2, 5) = ؟', '(7, ‎-2, 5).'),
   ('T(e₁) = (2, 0) و T(e₂) = (0, 3). A = ؟', '[[2, 0], [0, 3]].'),
   ('A × (1, 1) لنفس A اللي فوق؟', '(2, 3) = العمود الأول + العمود التاني.'),
   ('تحويل من ℝ² لـ ℝ³: المصفوفة كام × كام؟', '3 × 2.'),
   ('لف 90 درجة: e₁ راح فين و e₂ راح فين؟', 'e₁ ← (0, 1) و e₂ ← (‎-1, 0).')]),
 ('الـ CAD: B-Rep', [
   ('الأسطوانة: V و E و F؟', '2 و 3 و 3.'),
   ('ليه خط اللحام بيتعد مرتين في حلقة الجنب؟', 'الجنب مستطيل ملفوف: حرفه الشمال والحرف اليمين هما نفس الخط.'),
   ('وش فيه خرم: كام حلقة؟', '2: الحدود برّه + حلقة الخرم.'),
   ('ضلع اتلمس 4 مرات. الشكل Manifold؟', 'لأ (زي المكعبين اللي بيلمسوا بعض في ضلع).')]),
]
