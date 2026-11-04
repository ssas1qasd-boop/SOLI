import sys
sys.path.insert(0, '/home/claude/day1')
from words import W

COMPILER_WORDS = [
 W('enum class TokenType { Var, Identifier, Number, Equal, Plus, Star, Semicolon, End };', [('enum class', 'نوع جديد ليه قيم بأسماء بس'), ('TokenType', 'اسمه'), ('Var, Identifier, Number, Equal, Plus, Star, Semicolon', 'القيم المسموحة'), ('End', 'علامة إن الكود خلص')],
   'بدل ما نقول «النوع 3» بنقول <code>TokenType::Plus</code>، والـ compiler بيمنعك تكتب قيمة مش في القايمة.'),
 W('tokens.push_back({ TokenType::Number, source.substr(start, i - start) });', [('tokens.push_back', 'ضيف في آخر القايمة'), ('{ }', 'اعمل Token جديد من النوع والنص'), ('TokenType::Number', 'نوعه رقم'), ('source.substr(start, i - start)', 'قص من النص: من start، بطول i - start')],
   'لو النص <code>"var x = 12"</code> والرقم بدأ عند 8 وخلص عند 10، القص = <code>"12"</code>.'),
 W('Node* left;', [('Node*', 'Pointer لعقدة'), ('left', 'الفرع الشمال')],
   'الشجرة كلها Pointers: كل عقدة عملية بتشاور على عقدتين تحتها. ده نفس الـ Pointer بتاع الأسبوع ده، بس بيشاور على struct.'),
 W("left = new Node{ '*', 0, \"\", left, Primary() };", [('new Node{ }', 'اعمل عقدة على الـ Heap'), ("'*'", 'نوعها ضرب'), ('0, ""', 'مالهاش رقم ولا اسم'), ('left', 'شمالها = اللي اتبنى لحد دلوقتي'), ('Primary()', 'يمينها = الرقم الجاي'), ('left =', 'وبقت هي الشجرة')],
   'كده <code>2 * 3 * 4</code> بتبقى ((2 × 3) × 4): كل ضرب جديد بيركب فوق اللي قبله.'),
 W('Node* left = Multiplication();', [('Node* left', 'Pointer لأول حتة في الجمع'), ('Multiplication()', 'نده مستوى الضرب كامل الأول')],
   'ده سر الأولوية (Recursive Descent): المستوى الأقوى (الضرب) بيتنده من جوه المستوى الأضعف (الجمع)، فبيتقفل في فرع لوحده قبل ما الجمع يشوفه.'),
 W('stack.push_back(in.op == "ADD" ? a + b : a * b);', [('in.op == "ADD"', 'الأمر جمع؟'), ('? a + b', 'لو أيوه: اجمع'), (': a * b', 'لو لأ: اضرب'), ('stack.push_back', 'حط النتيجة فوق')],
   'كل عملية بتشيل رقمين من فوق وتحط رقم واحد. فبعد كل الأوامر بيفضل رقم واحد: النتيجة.'),
]

COMPILER_TABLE = '''<table class="types"><tr><th>المرحلة</th><th>الدخل</th><th>الخرج</th><th>في البرنامج</th></tr>
<tr><td>1. Scanner (Lexer)</td><td>حروف: <code>var x = 1 + 2 * 3;</code></td><td>Tokens: <code>[var] [x] [=] [1] [+] [2] [*] [3] [;]</code></td><td><code>Scan</code></td></tr>
<tr><td>2. Parser</td><td>Tokens</td><td>شجرة (AST): الضرب تحت الجمع</td><td><code>Parser</code> و <code>PrintTree</code></td></tr>
<tr><td>3. Compiler</td><td>الشجرة</td><td>Bytecode: <code>LOAD_INT 1</code> و <code>LOAD_INT 2</code> و <code>LOAD_INT 3</code> و <code>MULTIPLY</code> و <code>ADD</code></td><td><code>Compile</code></td></tr>
<tr><td>4. VM</td><td>Bytecode</td><td>النتيجة على الـ Stack</td><td><code>Run</code></td></tr></table>'''

BYTECODE_TABLE = '''<table class="types"><tr><th>الأمر</th><th>بيعمل إيه</th><th>الـ Stack</th></tr>
<tr><td><code>LOAD_INT n</code></td><td>حط الرقم n فوق</td><td>+1</td></tr>
<tr><td><code>LOAD_VAR i</code></td><td>حط قيمة المتغير رقم i فوق</td><td>+1</td></tr>
<tr><td><code>STORE_VAR i</code></td><td>شيل اللي فوق وخزّنه في المتغير رقم i</td><td>‎-1</td></tr>
<tr><td><code>ADD</code> / <code>MULTIPLY</code></td><td>شيل رقمين، وحط ناتجهم</td><td>‎-1</td></tr>
<tr><td><code>PRINT</code></td><td>اطبع اللي فوق وشيله</td><td>‎-1</td></tr></table>'''

EXERCISM_WORDS = [
 W('return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);', [('year % 4 == 0', 'بيقبل القسمة على 4'), ('&&', 'و (لازم الاتنين)'), ('year % 100 != 0', 'مش بيقبل على 100'), ('||', 'أو (واحد يكفي)'), ('year % 400 == 0', 'بيقبل على 400')],
   'الأقواس هنا مش إجبارية للـ compiler (الـ <code>&amp;&amp;</code> أقوى من <code>||</code>)، بس من غيرها اللي بيقرا هيتلخبط. جربناها تحت.'),
 W('namespace leap', [('namespace', 'عيلة أسماء'), ('leap', 'اسم العيلة')],
   'ننده الدالة كده: <code>leap::is_leap_year(2000)</code>، زي <code>std::cout</code> بالظبط.'),
 W('sound = std::to_string(drops);', [('std::to_string', 'حوّل رقم لنص'), ('(drops)', 'الرقم'), ('sound =', 'حطه في sound')],
   'مينفعش <code>sound = drops</code> لأن <code>sound</code> نص و <code>drops</code> رقم.'),
]

UNIFORM_WORDS = [
 W('"uniform vec4 u_Color;\\n"', [('uniform', 'جاي من برا (الـ CPU)'), ('vec4', '4 أرقام: R, G, B, A'), ('u_Color', 'اسمه (u_ = uniform، عادة)')],
   'الـ uniform قيمة <b>واحدة</b> لكل الأركان وكل البكسلات في الرسمة الواحدة. عكس الـ attribute اللي بيختلف من ركن لركن.'),
 W('int location = glGetUniformLocation(shader, "u_Color");', [('glGetUniformLocation', 'دوّر على uniform بالاسم'), ('shader', 'جوه الـ Program ده'), ('"u_Color"', 'الاسم بالحرف'), ('location', 'رقم خانته')],
   'لو رجع ‎-1: الاسم غلط، أو الـ uniform مش مستخدم فالكارت شاله وقت الترجمة. الاتنين جربناهم تحت.'),
 W('glUniform4f(location, r, 0.3f, 0.8f, 1.0f);', [('glUniform', 'ابعت لـ uniform'), ('4f', '4 أرقام float'), ('location', 'في الخانة دي'), ('r, 0.3f, 0.8f, 1.0f', 'R, G, B, A')],
   'لازم يتنده بعد <code>glUseProgram</code>، لأنه بيكتب في الـ Program الشغال.'),
 W('glUniform1f(timeLocation, time);', [('1f', 'رقم واحد float'), ('timeLocation', 'خانة u_Time'), ('time', 'الثواني')],
   'النوع لازم يطابق الـ Shader: <code>float</code> ← <code>1f</code>، و <code>vec4</code> ← <code>4f</code>. لو غلطت، الكارت بيرفض ومش بيقولك.'),
 W('"    float r = 0.5 + 0.5 * sin(u_Time + v_Position.x * 3.0);\\n"', [('sin( )', 'بين ‎-1 و 1، وبيلف'), ('0.5 + 0.5 *', 'حوّله لبين 0 و 1'), ('u_Time', 'الوقت: كل فريم أكبر شوية'), ('v_Position.x * 3.0', 'كل بكسل متأخر حسب مكانه')],
   'الوقت واحد لكل البكسلات (uniform)، بس المكان مختلف (جاي من الـ Vertex)، فكل بكسل بيطلع لون مختلف.'),
]

UNIFORM_TABLE = '''<table class="types"><tr><th></th><th>Attribute</th><th>Uniform</th></tr>
<tr><td>قيمته</td><td>مختلفة لكل ركن</td><td>واحدة لكل الرسمة</td></tr>
<tr><td>جاي منين</td><td>الصندوق (Buffer) + <code>glVertexAttribPointer</code></td><td><code>glUniform4f</code> أو <code>glUniform1f</code> من الـ CPU</td></tr>
<tr><td>في الـ Shader</td><td><code>layout(location = 0) in vec4 position;</code></td><td><code>uniform vec4 u_Color;</code></td></tr>
<tr><td>أمثلة</td><td>المكان، اللون لكل ركن</td><td>لون الرسمة، الوقت، مصفوفة الكاميرا</td></tr></table>'''

GLUNIFORM_TABLE = '''<table class="types"><tr><th>في الـ Shader</th><th>من C++</th></tr>
<tr><td><code>uniform float u_Time;</code></td><td><code>glUniform1f(loc, t);</code></td></tr>
<tr><td><code>uniform vec2 u_Pos;</code></td><td><code>glUniform2f(loc, x, y);</code></td></tr>
<tr><td><code>uniform vec3 u_Rgb;</code></td><td><code>glUniform3f(loc, r, g, b);</code></td></tr>
<tr><td><code>uniform vec4 u_Color;</code></td><td><code>glUniform4f(loc, r, g, b, a);</code></td></tr>
<tr><td><code>uniform int u_Mode;</code></td><td><code>glUniform1i(loc, 5);</code></td></tr>
<tr><td><code>uniform mat4 u_MVP;</code></td><td><code>glUniformMatrix4fv(loc, 1, GL_FALSE, ptr);</code></td></tr></table>'''

MATH_WORDS = [
 W('def dot(a, b):', [('def', 'عرّف دالة'), ('dot', 'اسمها'), ('(a, b)', 'بتاخد متجهين'), (':', 'الجسم جاي تحت، داخل لجوه')],
   'Python مافيهاش أقواس <code>{ }</code>: السطور اللي داخلة لجوه بمسافات هي جسم الدالة.'),
 W('total += a[i] * b[i]', [('a[i] * b[i]', 'العنصرين المتقابلين مضروبين'), ('total +=', 'ضيفهم للمجموع')],
   'ده تعريف Khan بالظبط: a₁b₁ + a₂b₂ + … + aₙbₙ.'),
 W('return math.sqrt(dot(a, a))', [('dot(a, a)', 'a · a = مجموع المربعات'), ('math.sqrt', 'الجذر')],
   '‖a‖ = √(a · a). الدالة بتستخدم <code>dot</code> اللي فوقها بدل ما نكتب المربعات تاني.'),
 W('u / np.linalg.norm(u)', [('u', 'المتجه'), ('/', 'اقسم كل عنصر'), ('np.linalg.norm(u)', 'على الطول')],
   'الناتج متجه طوله 1 في نفس الاتجاه (Unit vector).'),
]

MATH_TABLE = '''<table class="types"><tr><th>الخاصية</th><th>بالرموز</th><th>جربناها بـ</th><th>النتيجة</th></tr>
<tr><td>الترتيب مش بيفرق</td><td>c · d = d · c</td><td><code>np.dot(c, d)</code> و <code>np.dot(d, c)</code></td><td>13 و 13</td></tr>
<tr><td>التوزيع</td><td>c · (d + e) = c · d + c · e</td><td>e = [4, ‎-1, 2]</td><td>21 و 21</td></tr>
<tr><td>الرقم يطلع برا</td><td>(3c) · d = 3 (c · d)</td><td>3 × 13</td><td>39 و 39</td></tr>
<tr><td>الطول</td><td>‖a‖² = a · a</td><td>[2, 5]</td><td>29 و 29</td></tr></table>'''

REFACTOR_TABLE = '''<table class="types"><tr><th>قبل (امبارح)</th><th>بعد (النهارده)</th><th>ليه</th></tr>
<tr><td><code>glfwCreateWindow(640, 480, "Delete Last Line", nullptr, nullptr)</code> و <code>glPointSize(10.0f)</code></td><td><code>kWindowWidth</code> و <code>kPointSize</code> فوق</td><td>الرقم السحري: مش واضح معناه، ولو اتكرر هتنسى تغيّره في حتة</td></tr>
<tr><td><code>glUniform4f(location, 1.0f, 0.5f, 0.1f, 1.0f)</code></td><td><code>SetColor(location, kPointColor)</code></td><td>الاسم بيقول ده لون إيه</td></tr>
<tr><td><code>polylines.push_back({ (int)points.size() / 2, 0 })</code> في 3 أماكن</td><td><code>StartNewLine()</code></td><td>DRY: ماتكررش نفسك. التعديل في مكان واحد</td></tr>
<tr><td><code>points.size() / 2</code> و <code>polylines.size() - 1</code></td><td><code>PointCount()</code> و <code>FinishedLineCount()</code></td><td>الاسم بيشرح الحساب</td></tr>
<tr><td>كل الشغل جوه <code>MouseButtonCallback</code> و <code>KeyCallback</code></td><td><code>AddPoint</code> و <code>FinishLine</code> و <code>DeleteLastLine</code></td><td>كل دالة بتعمل حاجة واحدة، والـ Callback بقى يترجم الضغطة بس</td></tr>
<tr><td>لوب فيه <code>points.pop_back()</code></td><td><code>points.resize(points.size() - last.count * 2)</code></td><td>سطر واحد بنفس النتيجة</td></tr>
<tr><td>الرسم جوه اللوب</td><td><code>DrawScene(location)</code></td><td>اللوب بقى 3 سطور تتقري في ثانية</td></tr></table>'''

REFACTOR_WORDS = [
 W('const int kWindowWidth = 640;', [('const', 'مايتغيرش'), ('int', 'رقم صحيح'), ('kWindowWidth', 'k = Constant + الاسم'), ('640', 'القيمة في مكان واحد')],
   'لو عايز الشباك أكبر، بتغيّر سطر واحد فوق بدل ما تدوّر على 640 في الكود.'),
 W('static void StartNewLine()', [('static', 'الدالة دي للملف ده بس'), ('void', 'مش بترجّع حاجة'), ('StartNewLine', 'اسم فعل بيقول بتعمل إيه')],
   'اسم الدالة فعل (Start, Add, Delete). اللي بيقرا <code>StartNewLine();</code> بيفهم من غير ما يفتح الدالة.'),
 W('points.resize(points.size() - last.count * 2);', [('points.resize', 'خلّي الحجم'), ('points.size()', 'الحجم الحالي'), ('- last.count * 2', 'ناقص أرقام الخط (رقمين لكل نقطة)')],
   'بتشيل من الآخر زي <code>pop_back</code> بالظبط، بس مرة واحدة.'),
]
