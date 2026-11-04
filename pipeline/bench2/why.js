// «هيفيدنا بإيه»: why a line is there, and «هنستخدمه في إيه»: the next real line that uses what it made
const PURPOSE = [
  // ---- GLFW: the window
  [/glfwInit\s*\(/, 'من غيرها مفيش شباك ولا ماوس ولا كيبورد. بتجهّز مكتبة GLFW اللي بتكلم نظام التشغيل بالنيابة عننا.'],
  [/glfwWindowHint\s*\(/, 'بنقول لـ GLFW قبل ما يعمل الشباك: عايزين نسخة OpenGL كام (3.3) وأنهي نوع (Core). لو ماقلناش، ممكن ناخد نسخة قديمة مش بتفهم الـ VAO والـ Shaders بالشكل اللي بنكتبه.'],
  [/glfwCreateWindow\s*\(/, 'بيعمل الشباك اللي هنرسم فيه، وبيرجّع عنوانه في <code>window</code>. أي حاجة بعد كده عايزة الشباك (الرسم، الماوس، القفل) بتاخد <code>window</code> ده.'],
  [/glfwTerminate\s*\(/, 'بيقفل GLFW ويرجّع لنظام التشغيل كل حاجة خدناها (الشباك والوصلة بالكارت). آخر سطر قبل ما البرنامج يخلص.'],
  [/glfwMakeContextCurrent\s*\(/, 'بيوصّل الشباك ده بالكارت (الـ Context). من غير الوصلة دي أي أمر <code>gl...</code> مالوش مكان يروحله.'],
  [/gladLoadGL(Loader)?\s*\(/, 'بيجيب عناوين دوال OpenGL من الدرايفر. دوال زي <code>glGenBuffers</code> مش موجودة في البرنامج نفسه، والدرايفر هو اللي فيه الكود بتاعها. GLAD بيدوّر عليها ويحط عناوينها، فلما ننده <code>glGenBuffers</code> النداء يروح للدرايفر صح.'],
  [/glfwSwapInterval\s*\(/, 'بيربط تبديل اللوحتين بتحديث الشاشة (VSync). كده البرنامج مش هيرسم أسرع من الشاشة ويحرق المعالج على الفاضي، والصورة مش هتتقطع.'],
  [/glfwWindowShouldClose\s*\(/, 'بيسأل: المستخدم داس على زرار القفل؟ طول ما الإجابة لأ، اللوب تفضل تلف والشباك يفضل مفتوح.'],
  [/glfwSwapBuffers\s*\(/, 'بنرسم في لوحة مستخبية (Back) عشان المستخدم مايشوفش الرسمة وهي بتتعمل. السطر ده بيبدّل اللوحتين، فالرسمة الكاملة تظهر مرة واحدة.'],
  [/glfwPollEvents\s*\(/, 'بيسأل نظام التشغيل: حصل إيه من آخر لفة؟ ضغطة ماوس، زرار، تحريك شباك. لو فيه ضغطة، GLFW بينده الـ Callback بتاعنا من هنا.'],
  [/glfwSetMouseButtonCallback\s*\(/, 'بنسجّل دالتنا عند GLFW: «لما الماوس يتداس، ندهلي الدالة دي». إحنا مش بنناديها بنفسنا، GLFW هو اللي بيناديها جوه <code>glfwPollEvents</code>.'],
  [/glfwSetKeyCallback\s*\(/, 'بنسجّل دالتنا عند GLFW: «لما زرار في الكيبورد يتداس، ندهلي الدالة دي». GLFW بيناديها لوحده جوه <code>glfwPollEvents</code>.'],
  [/glfwGetCursorPos\s*\(/, 'بيجيب مكان الماوس بالبكسل جوه الشباك (من فوق شمال). هنحوّله بعد كده لأرقام من ‎-1 لـ 1 عشان الكارت يفهمها.'],
  [/glfwGetWindowSize\s*\(/, 'بيجيب عرض وطول الشباك بالبكسل. محتاجينهم عشان نحوّل مكان الماوس من بكسل لـ ‎-1..1 (نقسم على العرض والطول).'],
  [/glfwGetKey\s*\(/, 'بيسأل: الزرار ده متداس دلوقتي؟ بنستخدمه عشان نحرّك الكاميرا طول ما الزرار متداس.'],
  [/glfwGetMouseButton\s*\(/, 'بيسأل: زرار الماوس ده متداس دلوقتي؟'],
  [/glfwSetInputMode\s*\(/, 'بيخبّي مؤشر الماوس أو يظهّره (عشان الكاميرا تلف بالماوس من غير ما المؤشر يخرج برا الشباك).'],
  [/glfwDestroyWindow\s*\(/, 'بيقفل الشباك ويمسحه.'],
  [/glViewport\s*\(/, 'بيقول للكارت يرسم في أنهي جزء من الشباك (هنا الشباك كله). كده ‎-1..1 بتتمد على العرض والطول بالبكسل.'],
  // ---- buffers / VAO
  [/glGenVertexArrays\s*\(/, 'بيعمل «ورقة تعليمات» (VAO) فاضية ويدينا رقمها. الورقة دي هتشيل وصف الأركان: كل ركن فيه كام رقم ومن أنهي صندوق.'],
  [/glBindVertexArray\s*\(\s*0\s*\)/, 'بيشيل ورقة التعليمات من على الترابيزة. كده أي إعداد بعده مش هيتكتب بالغلط في الورقة اللي فاتت.'],
  [/glBindVertexArray\s*\(/, 'بيخلّي ورقة التعليمات دي هي الشغالة. أي <code>glVertexAttribPointer</code> بعده بيتكتب فيها، وأي رسم بعده بيقرا منها.'],
  [/glGenBuffers\s*\(/, 'بيعمل صندوق (Buffer) فاضي على الكارت ويدينا رقمه. لسه مافيهوش ولا بايت.'],
  [/glBindBuffer\s*\(/, 'بيخلّي الصندوق ده هو الشغال. الأوامر اللي بعده (زي <code>glBufferData</code>) مش بتاخد رقم الصندوق، بتشتغل على الصندوق الشغال.'],
  [/glBufferData\s*\(/, 'بينسخ الأرقام من الرام لذاكرة الكارت. الكارت مايقدرش يقرا الرام بتاعتنا، فلازم الأرقام تتنقل له قبل الرسم.'],
  [/glBufferSubData\s*\(/, 'بيكتب جزء من الأرقام في صندوق موجود من غير ما يعمله من الأول.'],
  [/glEnableVertexAttribArray\s*\(/, 'بيشغّل الخانة رقم N في ورقة التعليمات. الخانة المقفولة الـ Shader بياخد فيها رقم ثابت مش أرقام الصندوق.'],
  [/glVertexAttribPointer\s*\(/, 'بيوصف للكارت إزاي يقطّع البايتات اللي في الصندوق لأركان: كل ركن كام رقم، ونوعهم، وكل ركن بعد كام بايت (stride)، والخانة دي بتبدأ منين (offset). من غيره الكارت شايف بايتات ومش عارف مين x ومين y.'],
  [/glDeleteBuffers\s*\(/, 'بيفضّي الصندوق ويرجّع ذاكرته للكارت.'],
  [/glDeleteVertexArrays\s*\(/, 'بيمسح ورقة التعليمات من الكارت.'],
  // ---- shaders
  [/glCreateShader\s*\(/, 'بيعمل Shader فاضي على الكارت من النوع ده (Vertex أو Fragment) ويدينا رقمه. هنحط فيه النص ونترجمه بعد كده.'],
  [/glShaderSource\s*\(/, 'بيبعت نص الـ Shader للكارت. الدالة دي مكتوبة بأسلوب C، فبتاخد عنوان النص (<code>char*</code>) مش <code>std::string</code>، وعشان كده جهزنا <code>src</code> قبلها.'],
  [/glCompileShader\s*\(/, 'بيترجم النص لأوامر يفهمها الكارت. الترجمة بتحصل وقت التشغيل، فلو فيه غلطة في الـ Shader مش هتعرفها إلا من الرسالة.'],
  [/glGetShaderiv\s*\([^)]*COMPILE_STATUS/, 'بيسأل الكارت: الترجمة نجحت؟ الإجابة بتتكتب في <code>result</code>. لو 0 يبقى فيه غلطة وهنطبع رسالتها.'],
  [/glGetShaderiv\s*\([^)]*INFO_LOG_LENGTH/, 'بيسأل الكارت: رسالة الغلط طولها كام حرف؟ عشان نحجز لها مكان بالظبط.'],
  [/glGetShaderiv\s*\(/, 'بيسأل الكارت سؤال عن الـ Shader، والإجابة بتتكتب في المتغير اللي بعتنا عنوانه.'],
  [/glGetShaderInfoLog\s*\(/, 'بيجيب رسالة الغلط نفسها (فيها رقم السطر جوه الـ Shader والسبب) عشان نطبعها.'],
  [/glCreateProgram\s*\(/, 'بيعمل Program فاضي على الكارت. الـ Program هو اللي هيجمع الـ Vertex والـ Fragment Shader في حتة واحدة تشتغل مع بعض.'],
  [/glAttachShader\s*\(/, 'بيحط الـ Shader جوه الـ Program. لازم الاتنين (Vertex و Fragment) يتحطوا قبل الربط.'],
  [/glLinkProgram\s*\(/, 'بيربط الـ Shaders اللي جوه الـ Program ببعض: بيتأكد إن كل <code>out</code> في الـ Vertex ليه <code>in</code> بنفس الاسم في الـ Fragment، ويطلّع برنامج واحد جاهز يشتغل.'],
  [/glValidateProgram\s*\(/, 'بيسأل الكارت: الـ Program ده ينفع يشتغل بالإعدادات اللي دلوقتي؟ (فحص زيادة للأمان).'],
  [/glDeleteShader\s*\(/, 'بعد الربط، الـ Program بقى معاه نسخته. الـ Shader المنفصل مش محتاجينه، فبنمسحه عشان مايفضلش واخد مكان.'],
  [/glUseProgram\s*\(/, 'بيختار الـ Program اللي هيتشغّل في أي رسم بعده. ولازم يبقى شغال قبل <code>glUniform...</code> كمان.'],
  [/glDeleteProgram\s*\(/, 'بيمسح الـ Program من الكارت قبل ما البرنامج يقفل.'],
  [/glGetUniformLocation\s*\(/, 'بيدوّر على الـ uniform بالاسم جوه الـ Program ويرجّع رقم خانته. <code>glUniform4f</code> مش بتاخد اسم، بتاخد الرقم ده. لو رجع ‎-1 يبقى الاسم مش موجود.'],
  [/glUniform4f\s*\(/, 'بيبعت 4 أرقام (لون R, G, B, A) للـ uniform في الـ Shader. الـ uniform قيمة واحدة لكل الأركان وكل البكسلات في الرسمة دي.'],
  [/glUniformMatrix4fv\s*\(/, 'بيبعت مصفوفة 4×4 للـ Shader. الـ Vertex Shader بيضرب كل ركن فيها عشان يحرّكه حسب الكاميرا.'],
  // ---- draw
  [/glClearColor\s*\(/, 'بيحدد اللون اللي <code>glClear</code> هيمسح بيه.'],
  [/glClear\s*\(/, 'بيمسح اللوحة اللي ورا قبل الرسم. من غيره الرسمة الجديدة هتترسم فوق القديمة.'],
  [/glDrawArrays\s*\(/, 'ده الأمر اللي بيرسم فعلاً. كل اللي قبله كان تجهيز. الكارت بيقرا الأركان من الصندوق حسب ورقة التعليمات، ويشغّل الـ Vertex Shader لكل ركن، ويلوّن البكسلات بالـ Fragment Shader.'],
  [/glDrawElements\s*\(/, 'ده الأمر اللي بيرسم فعلاً، بس بيمشي على جدول الأرقام (EBO) بدل ما ياخد الأركان بالترتيب. كده الركن المتكرر بيتخزن مرة واحدة.'],
  [/glPointSize\s*\(/, 'بيحدد حجم كل نقطة بالبكسل لما نرسم <code>GL_POINTS</code>. من غيره النقطة بكسل واحد ومش هتبان.'],
  [/glLineWidth\s*\(/, 'بيحدد سُمك الخط.'],
  [/glEnable\s*\(\s*GL_DEPTH_TEST/, 'بيشغّل اختبار العمق: البكسل الأقرب للكاميرا هو اللي يكسب. من غيره الوش اللي ورا ممكن يترسم فوق اللي قدام.'],
  // ---- our own functions
  [/\bParseShader\s*\(/, 'بننده دالتنا اللي بتقرا ملف <code>Basic.shader</code> وتقسمه نصين: Vertex و Fragment.'],
  [/\bCreateShader\s*\(/, 'بننده دالتنا اللي بتترجم الـ Shaderين وتربطهم في Program واحد وترجّع رقمه. ده الرقم اللي هنديه لـ <code>glUseProgram</code>.'],
  [/\bCompileShader\s*\(/, 'بننده دالتنا اللي بتعمل Shader واحد وتترجمه وتفحص الترجمة. بننديها مرتين: مرة للـ Vertex ومرة للـ Fragment.'],
  [/\bUploadPoints\s*\(/, 'بننده دالتنا اللي بتبعت كل النقط اللي في الرام للكارت تاني، عشان الكارت يبقى عنده نفس النقط بعد التغيير.'],
  // ---- C / C++ library
  [/\.c_str\s*\(\s*\)/, 'الـ <code>std::string</code> نوع C++، ودوال OpenGL مكتوبة بأسلوب C ومش بتفهمه. <code>c_str()</code> بتدينا عنوان أول حرف في النص (<code>const char*</code>)، وده الشكل اللي <code>glShaderSource</code> مستنياه.'],
  [/std::ifstream|ifstream\s+\w+\(/, 'بيفتح الملف للقراية. من غيره مانقدرش نقرا <code>Basic.shader</code>.'],
  [/getline\s*\(/, 'بيقرا سطر واحد من الملف في كل لفة، ويرجّع false لما الملف يخلص فاللوب تقف.'],
  [/std::stringstream|stringstream\s+\w+/, 'صندوق نصوص بنضيف فيه سطر ورا سطر، وفي الآخر بناخد النص كله مرة واحدة بـ <code>.str()</code>.'],
  [/\.find\s*\(/, 'بيدوّر على كلمة جوه السطر. لو مالقاهاش بيرجّع <code>npos</code>.'],
  [/\.str\s*\(\s*\)/, 'بياخد كل اللي اتجمع في الـ stringstream كنص واحد (<code>std::string</code>).'],
  [/\.push_back\s*\(/, 'بيضيف عنصر في آخر الـ vector، والـ vector بيكبر لوحده.'],
  [/\.pop_back\s*\(/, 'بيمسح آخر عنصر في الـ vector.'],
  [/\.back\s*\(\s*\)/, 'بيرجّع آخر عنصر في الـ vector من غير ما يمسحه.'],
  [/\.size\s*\(\s*\)/, 'عدد العناصر اللي في الـ vector دلوقتي.'],
  [/\.data\s*\(\s*\)/, 'عنوان أول رقم في الـ vector. <code>glBufferData</code> محتاج عنوان مش vector.'],
  [/\.clear\s*\(\s*\)/, 'بيفضّي الـ vector (الحجم يبقى 0).'],
  [/\.erase\s*\(/, 'بيمسح عنصر من نص الـ vector، واللي بعده بيتزحزحوا مكانه.'],
  [/\.capacity\s*\(\s*\)/, 'المكان المحجوز فعلاً للـ vector. ممكن يبقى أكبر من الحجم عشان الإضافة الجاية تبقى أسرع.'],
  [/\bmalloc\s*\(/, 'بيحجز مكان في الذاكرة (الـ Heap) بعدد البايتات اللي طلبناه، ويرجّع عنوانه. لازم نرجّعه بعد كده بـ <code>free</code>.'],
  [/\bfree\s*\(/, 'بيرجّع المكان اللي حجزناه بـ <code>malloc</code>. من غيره الذاكرة بتفضل محجوزة (Memory leak).'],
  [/\bmemset\s*\(/, 'بيملا عدد من البايتات بقيمة واحدة (غالباً صفر) مرة واحدة.'],
  [/\bstrlen\s*\(/, 'بيعد حروف النص لحد أول حرف صفر (<code>\\0</code>).'],
  [/\bnew\s+char\s*\[/, 'بيحجز مكان للحروف على الـ Heap بالطول اللي عرفناه. لازم نرجّعه بعد كده بـ <code>delete[]</code>.'],
  [/\bdelete\s*\[\]/, 'بيرجّع المكان اللي حجزناه بـ <code>new[]</code>.'],
  [/std::cout|\bprintf\s*\(/, 'بيطبع في الـ Terminal. ده عشان إحنا نشوف القيم ونتأكد إن البرنامج ماشي صح.'],
  [/\bstd::cin\b|\bcin\s*>>/, 'بيستنى المستخدم يكتب حاجة في الـ Terminal ويحطها في المتغير.'],
  [/std::sqrt|\bsqrt\s*\(/, 'الجذر التربيعي. بنستخدمه في حساب الطول: ‎√(x² + y² + z²).'],
  // ---- glm
  [/glm::lookAt\s*\(/, 'بيعمل مصفوفة «الكاميرا بتبص منين ولفين».'],
  [/glm::perspective\s*\(/, 'بيعمل مصفوفة المنظور: الحاجة البعيدة تبان أصغر.'],
  [/glm::value_ptr\s*\(/, 'عنوان أول رقم في المصفوفة، عشان <code>glUniformMatrix4fv</code> محتاج عنوان.'],
  [/glm::dot\s*\(/, 'الضرب النقطي جاهز من مكتبة glm.'],
  // ---- python / numpy
  [/np\.array\s*\(/, 'بيعمل مصفوفة NumPy: الأرقام جنب بعض في الذاكرة، والحساب عليها كلها بيحصل مرة واحدة من غير لوب.'],
  [/np\.dot\s*\(/, 'الضرب النقطي: بيضرب الأماكن المتقابلة ويجمعهم. الناتج رقم واحد بيقول المتجهين في نفس الاتجاه ولا لأ.'],
  [/np\.cross\s*\(/, 'الضرب الاتجاهي: الناتج متجه عمودي على الاتنين (3D بس).'],
  [/np\.linalg\.norm\s*\(/, 'طول المتجه: ‎√(x² + y² + z²).'],
  [/np\.degrees\s*\(/, 'بيحوّل الزاوية من راديان لدرجات.'],
  [/np\.arccos\s*\(/, 'عكس الـ cos: من رقم الـ cos بيرجّع الزاوية.'],
  [/np\.sum\s*\(/, 'بيجمع الأرقام. ومع <code>axis=1</code> بيجمع كل صف لوحده.'],
  [/\.copy\s*\(\s*\)/, 'بيعمل نسخة جديدة منفصلة. من غيرها <code>c = a</code> بيخلّي الاسمين على نفس البيانات.'],
  [/\.tolist\s*\(\s*\)/, 'بيحوّل مصفوفة NumPy لـ List عادية في بايثون.'],
  [/^\s*import\s+numpy/, 'بيجيب مكتبة NumPy ويسمّيها <code>np</code> اختصاراً.'],
  [/^\s*print\s*\(/, 'بيطبع في الـ Terminal.'],
  // ---- control flow and the rest
  [/^if\s*\(\s*!window\s*\)|^if\s*\(\s*window\s*==\s*nullptr\s*\)/, 'لو الشباك ماتعملش (مثلاً الجهاز مش بيدعم OpenGL 3.3)، بنقفل GLFW ونخرج بدل ما نكمّل ونقع عند أول أمر رسم.'],
  [/^if\s*\(\s*result\s*==\s*GL_FALSE\s*\)/, 'لو الترجمة فشلت بندخل جوه عشان نطبع رسالة الغلط ونمسح الـ Shader. لو نجحت بنتخطى الجزء ده كله.'],
  [/^if\s*\(\s*\w+\s*==\s*NULL\s*\)|^if\s*\(\s*!\w+\s*\|\|/, 'بنتأكد إن الـ Pointer مش فاضي (NULL) قبل ما نستخدمه. لو فاضي واستخدمناه البرنامج هيقع.'],
  [/^return\s+0\s*;/, 'بيخلّص الدالة. لو دي <code>main</code> يبقى بيقول لنظام التشغيل إن البرنامج خلص من غير مشاكل (0 = تمام).'],
  [/^return\s*;/, 'بيخرج من الدالة على طول من غير ما يكمّل السطور اللي تحته. بنستخدمه عشان نتجاهل الحالة دي.'],
  [/^return\b/, 'بيرجّع النتيجة دي للسطر اللي نده الدالة، والتنفيذ يرجع هناك.'],
  [/^for\s*\([^;:]*:\s*[^)]*\)/, 'لوب بيمشي على كل عنصر في القايمة واحد واحد، من غير ما نكتب عداد.'],
  [/^for\s*\(/, 'لوب: بيكرر السطور اللي جواه. الشرط اللي في النص بيتشاف في أول كل لفة، ولما يبقى غلط اللوب تقف.'],
  [/^while\s*\(/, 'لوب: بيكرر السطور اللي جواه طول ما الشرط صح. الشرط بيتشاف في أول كل لفة بس.'],
  [/^else\s+if\s*\(/, 'شرط تاني: بيتشاف بس لو الشرط اللي قبله طلع غلط.'],
  [/^if\s*\(/, 'شرط: السطور اللي جواه بتتنفذ بس لو الشرط صح، ولو غلط بنتخطاها.'],
  [/^else\b/, 'ده اللي بيتنفذ لو الشرط اللي قبله طلع غلط.'],
  [/\bcout\b/, 'بيطبع في الـ Terminal. ده عشان إحنا نشوف القيم ونتأكد إن البرنامج ماشي صح.'],
  [/^\(?\*\s*\w+\)?\s*(?:[+\-*\/]?=|\+\+|--)/, 'النجمة قبل اسم الـ Pointer معناها «روح للعنوان اللي جواه واكتب هناك». كده بنغيّر المتغير الأصلي نفسه، مش نسخة منه.'],
  [/^"[^"]*"\s*;?$/, 'قطعة من نص الـ Shader. الـ C++ بيلزق القطع اللي ورا بعض في نص واحد، و <code>\\n</code> في آخر كل قطعة = سطر جديد جوه الـ Shader.'],
  [/^struct\s+\w+/, 'بيعرّف نوع جديد بيجمع كذا متغير تحت اسم واحد.'],
  [/^\w+::\w+\s*=/, 'بيحفظ القيمة جوه الـ object، عشان الدوال التانية بتاعته تقدر تستخدمها بعدين.'],
  [/^[A-Z]\w*\s+\w+\s*\(/, 'بيعمل object جديد من الكلاس ده، وبيشغّل الدالة اللي بتجهّزه (constructor) بالقيم اللي بين القوسين.'],
  [/^\w+::\w+\s*\(/, 'أول الدالة اللي بتجهّز الـ object (constructor): بتاخد القيم وتحطها جواه.'],
  [/^(<<|[-+*\/]|\w[\w.\s*+\-]*\}\s*;?$)/, 'تكملة السطر اللي قبله: الـ C++ بيعتبر السطرين جملة واحدة لحد <code>;</code>.'],
  [/^\w+\s*<<\s*/, 'بيضيف النص ده في الـ stream بالترتيب.'],
  [/^\w+\[[^\]]*\]\s*<</, 'بيضيف السطر اللي اتقرا في الـ stringstream بتاع النوع ده (Vertex أو Fragment)، ومعاه سطر جديد. كده كل نوع بيتجمع نصه لوحده.'],
  [/^const\s+\w+\s*\*\s*const\b/, 'Pointer ثابت لقيمة ثابتة: لا ينفع نغيّر العنوان اللي جواه، ولا ينفع نكتب في القيمة اللي بيشاور عليها.'],
  [/^\w+\s*\*\s*const\b/, 'Pointer ثابت: العنوان اللي جواه مايتغيرش أبداً، بس ينفع نكتب في القيمة اللي بيشاور عليها بـ <code>*c = ...</code>.'],
  [/^LOG\s*\(/, '<code>LOG</code> ماكرو إحنا عاملينه: بيطبع القيمة في الـ Terminal عشان نشوفها.'],
  [/^\w+\.\w+\s*=(?!=)/, 'بيغيّر خانة جوه العنصر نفسه (مش نسخة)، عشان الـ <code>&amp;</code> في اللوب.'],
  [/^\w+\.\w+\s*\(/, 'بننده دالة جوه الـ object ده (method). الدالة بتشتغل على البيانات اللي جوه الـ object نفسه.'],
  [/,\s*$/, 'تكملة السطر اللي قبله: الـ C++ بيعتبر السطور دي جملة واحدة لحد <code>;</code>.'],
];
function ownFn(t){ const m = /^(?:[\w:<>]+\s+)?(\w+)\s*\((.*)\)\s*;\s*$/.exec(t); if (!m) return null; const r = (P.regions || []).find(r => r[2] === m[1] + '()'); if (!r) return null;
  return `بننده الدالة <code>${esc(m[1])}</code> اللي إحنا كاتبينها (السطور ${r[0]}–${r[1]}). التنفيذ هينط لها${m[2].trim() ? ' ومعاه القيم اللي بين القوسين' : ''}، ولما تخلص يرجع للسطر اللي بعد ده.`; }
function purposeOf(t){ const out = []; const o = ownFn(t); if (o) out.push(o); for (const [re, x] of PURPOSE){ if (re.test(t) && !out.includes(x)){ out.push(x); if (out.length === 2) break; } } return out; }
// the variable this line makes or changes
function madeVar(t){
  let m = /^(?:const\s+|static\s+|unsigned\s+|signed\s+|struct\s+)*[\w:<>,]+(?:\s*[*&]+\s*|\s+)([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*(?:=(?!=)|;|\{|\(\s*[^)]*\)\s*;)/.exec(t);
  if (m && !/^(return|delete|else|case|goto)$/.test(m[1])) return m[1];
  m = /^([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*(?:[+\-*\/]?=(?!=)|\+\+|--)/.exec(t); if (m) return m[1];
  m = /^gl(?:Gen\w+|GetShaderiv|GetProgramiv)\s*\([^)]*&\s*([A-Za-z_]\w*)/.exec(t); if (m) return m[1];
  m = /^glfwGet(?:CursorPos|WindowSize)\s*\([^,]*,\s*&\s*(\w+)/.exec(t); if (m) return m[1];
  return null; }
function allUses(k){
  const s = ST[k], t = stepText(s), v = madeVar(t); if (!v) return null;
  const re = new RegExp('\\b' + v + '\\b'), out = [], seen = new Set([s.v]);
  const scan = scoped => { for (let j = k + 1; j < ST.length && out.length < 6; j++){ const q = ST[j];
      if (scoped){ if (q.d < s.d) break; if (q.d !== s.d || q.fn !== s.fn) continue; }
      if (seen.has(q.v)) continue; const tq = stepText(q); if (!re.test(tq.replace(/"(?:[^"\\]|\\.)*"/g, '""'))) continue;
      if (madeVar(tq) === v && !new RegExp('=.*\\b' + v + '\\b').test(tq) && !/^\w+\s*[+\-*\/]?=/.test(tq)) break;
      seen.add(q.v); out.push({j, t: tq, line: fileLine(q)}); } };
  scan(true); if (!out.length) scan(false);
  return {v, uses: out}; }

// «يعني إيه»: one plain sentence saying what a later line does WITH this variable
function useRole(v, j){
  const t = stepText(ST[j]).trim(), X = jx(), g = X.G[j] || {}, q = ST[j];
  const nx = ST[j + 1] ? stepText(ST[j + 1]).trim() : '', nfn = (/\b(gl\w+)\s*\(/.exec(nx) || [])[1];
  const fm = /\b(gl\w+|glfw\w+)\s*\((.*)\)\s*;?\s*$/.exec(t);
  const A = fm ? fm[2].split(/,(?![^()]*\))/).map(a => a.trim()) : [];
  const at = A.findIndex(a => new RegExp('(^|[^\\w])' + v + '($|[^\\w])').test(a));
  const inLoop = q.lap ? ` (ده جوه اللوب، فبيتنفذ كل لفة)` : '';
  const after = {glBufferData: 'عشان <code>glBufferData</code> اللي بعده يحط فيه الأرقام', glVertexAttribPointer: 'عشان <code>glVertexAttribPointer</code> اللي بعده يربط الـ Layout بيه',
    glEnableVertexAttribArray: 'عشان التفعيل اللي بعده يتسجل فيها', glDrawElements: 'عشان الرسمة اللي بعده تقرا منه', glDrawArrays: 'عشان الرسمة اللي بعده تقرا منه', glBindBuffer: 'عشان الربط اللي بعده يتسجل فيها',
    glUniform4f: 'وبعدها نبعت اللون ونرسم', glUniform2f: 'وبعدها نبعت المكان ونرسم'}[nfn];
  const tail = after && !(q.lap && /^glUniform/.test(nfn)) ? '، ' + after : '';
  if (fm){ const fn = fm[1];
    if (/^glGen/.test(fn)) return `الكارت يعمل حاجة جديدة ويكتب رقمها في <code>${esc(v)}</code>.`;
    if (fn === 'glBindBuffer'){ const el = /ELEMENT/.test(A[0]);
      return (el ? `نخلّي <code>${esc(v)}</code> هو صندوق الترتيب الحالي` + (g.bvao ? `، والـ VAO رقم ${g.bvao} المربوط وقتها بيسجّله عنده` : '') + (q.lap ? '، عشان الرسمة الجاية بـ <code>glDrawElements</code> تعرف ترتيب الأركان' : '') : `نخلّي <code>${esc(v)}</code> هو صندوق الأركان الحالي (GL_ARRAY_BUFFER)`) + tail + inLoop + '.'; }
    if (fn === 'glBindVertexArray') return `نشغّل ورقة التعليمات <code>${esc(v)}</code>` + (q.lap ? '، عشان الرسمة الجاية تقرا أركانها وترتيبها منها' : tail || '، عشان الأوامر اللي بعدها تتسجل فيها') + inLoop + '.';
    if (/^glBuffer(Sub)?Data$/.test(fn)) return `ننسخ أرقام <code>${esc(v)}</code> من الرام لصندوق الكارت المربوط دلوقتي` + ((g.bbuf || {})[/ELEMENT/.test(A[0]) ? 'E' : 'A'] ? ` (Buffer ${g.bbuf[/ELEMENT/.test(A[0]) ? 'E' : 'A']})` : '') + '. بعد كده الكارت مش محتاج الرام عشان يرسم.';
    if (fn === 'glUseProgram') return `نشغّل الـ Program ده، فأي رسمة بعده هتستخدم الـ Shaders اللي جواه` + inLoop + '.';
    if (fn === 'glGetUniformLocation') return `نسأل الـ Program عن مكان المتغير ${esc(A[1] || '')} جوه الـ Shader، عشان نعرف نبعتله قيم.`;
    if (/^glUniform/.test(fn)){ let un = ''; for (let i = 0; i < ST.length; i++){ const m = new RegExp('\\b' + v + '\\s*=\\s*glGetUniformLocation\\([^,]+,\\s*"(\\w+)"').exec(stepText(ST[i])); if (m){ un = m[1]; break; } }
      const vals = A.slice(1).join(', ');
      return at === 0 ? `نستخدم المكان ده عشان نبعت ${un ? `لـ <code>${esc(un)}</code> اللي في الـ Shader` : 'للـ Shader'} قيمة جديدة: <b dir="ltr">(${esc(vals)})</b>` + (ST[j + 1] && /^\s*glDraw/.test(stepText(ST[j + 1])) ? '، والرسمة اللي بعده هتستخدمها' : '') + inLoop + '.' : `نبعت قيمة <code>${esc(v)}</code> للـ Shader` + inLoop + '.'; }
    if (fn === 'glAttachShader') return at === 0 ? `نحط Shader جوه الـ Program ده.` : `نحط الـ Shader ده جوه الـ Program.`;
    if (fn === 'glLinkProgram') return `نجمّع الـ Shaders اللي جوه الـ Program في برنامج واحد يشتغل على الكارت.`;
    if (fn === 'glValidateProgram') return `نسأل الكارت: الـ Program ده ينفع يشتغل بالحالة اللي الكارت فيها دلوقتي؟`;
    if (fn === 'glShaderSource') return at === 0 ? `نحط كود الـ Shader (النص) جوه الـ Shader ده.` : `نبعت النص ده للكارت ككود Shader.`;
    if (fn === 'glCompileShader') return `الكارت يترجم كود الـ Shader ده.`;
    if (/^glDelete/.test(fn)) return `نمسحه من الكارت عشان مش محتاجينه تاني.`;
    if (/^glGet\w+iv$/.test(fn)) return at === 0 ? `نسأل الكارت عن حالته (اتترجم؟ اترابط؟).` : `الكارت يكتب الإجابة في <code>${esc(v)}</code>.`;
    if (/^glDraw/.test(fn)) return `الرسم نفسه بيستخدمه` + inLoop + '.';
    if (/^glVertexAttribPointer$/.test(fn)) return `بيستخدمه في وصف الـ Layout.`;
    if (/^glfw/.test(fn)) return at >= 0 ? `بنبعته لـ <code>${esc(fn)}</code> عشان يشتغل على الشباك ده` + inLoop + '.' : null; }
  if (/(std::)?cout\b|\bprintf\s*\(/.test(t)) return (new RegExp('\\b' + v + '\\s*\\[').test(t) ? `نطبع عنصر من عناصره في الـ Terminal` : new RegExp('\\*\\s*' + v + '\\b').test(t) ? `نطبع القيمة اللي هو بيشاور عليها في الـ Terminal` : `نطبع قيمته في الـ Terminal`) + inLoop + '.';
  if (new RegExp('^\\s*free\\s*\\(\\s*' + v + '\\s*\\)').test(t)) return `نرجّع الذاكرة اللي حجزناها بـ malloc، فـ <code>${esc(v)}</code> مايبقاش ينفع نستخدمه بعد كده.`;
  if (new RegExp('^\\s*\\*\\s*' + v + '\\s*=').test(t)) return `بنكتب قيمة جديدة في المكان اللي <code>${esc(v)}</code> بيشاور عليه، يعني المتغير الأصلي هو اللي بيتغير` + inLoop + '.';
  if (new RegExp('^\\s*' + v + '\\s*\\[[^\\]]*\\]\\s*=').test(t)) return `بنكتب قيمة في خانة من خاناته` + inLoop + '.';
  { const am = new RegExp('^(?:[\\w:<>\\*&\\s]+\\s)?\\**(\\w+)\\s*=\\s*&' + v + '\\s*;').exec(t); if (am) return `بناخد عنوانه في الرام ونحطه في <code>${esc(am[1])}</code>، فـ <code>${esc(am[1])}</code> يبقى بيشاور عليه.`; }
  if (new RegExp('^(delete(\\[\\])?)\\s+' + v + '\\b').test(t)) return `نرجّع الذاكرة اللي هو بيشاور عليها.`;
  if (/^(if|else if|while|for)\b/.test(t)) return `الشرط ده بيقرا قيمته عشان يقرر` + (/^(while|for)/.test(t) ? ' نكمّل اللوب ولا لأ' : ' يدخل ولا لأ') + '.';
  if (new RegExp('^\\s*\\**' + v + '\\s*(\\[[^\\]]*\\])?\\s*([+\\-*/]?=|\\+\\+|--)').test(t)) return `بنغيّر قيمته` + inLoop + '.';
  const asg = /^(?:[\w:<>\*&\s]+\s)?\**(\w+)\s*(?:\[[^\]]*\])?\s*=\s*(.+)$/.exec(t);
  if (asg && asg[1] !== v) return `بنستخدم قيمته عشان نحسب <code>${esc(asg[1])}</code>` + inLoop + '.';
  const call = /\b([A-Za-z_]\w*)\s*\(/.exec(t);
  if (call && !/^(if|while|for|return|sizeof)$/.test(call[1])) return `بنبعته للدالة <code>${esc(call[1])}()</code> تشتغل عليه` + inLoop + '.';
  if (/^return\b/.test(t)) return `الدالة بترجّع قيمته للي ناداها.`;
  const ex = (q.ex || '').replace(/<[^>]+>/g, '').trim();
  return ex ? ex : null; }
// ---------- the journey of the GPU thing a line made or changed
const OBJ_ARGS = {glShaderSource: [[0, 'sh']], glCompileShader: [[0, 'sh']], glGetShaderiv: [[0, 'sh']], glGetShaderInfoLog: [[0, 'sh']], glDeleteShader: [[0, 'sh']],
  glAttachShader: [[0, 'pr'], [1, 'sh']], glLinkProgram: [[0, 'pr']], glValidateProgram: [[0, 'pr']], glUseProgram: [[0, 'pr']], glGetUniformLocation: [[0, 'pr']], glDeleteProgram: [[0, 'pr']], glGetProgramiv: [[0, 'pr']],
  glBindBuffer: [[1, 'buf']], glBindVertexArray: [[0, 'vao']]};
const OBJ_NAME = {sh: n => `الـ Shader رقم ${n}`, pr: n => `الـ Program رقم ${n}`, buf: n => `الصندوق (Buffer ${n})`, vao: n => `ورقة التعليمات (VAO ${n})`};
let JX = null;
function jx(){
  if (JX && JX.id === P.id) return JX;
  const G = []; let g = {}; ST.forEach((s, k) => { if (s.gp) g = s.gp; G[k] = g; });
  const objs = [], draws = [];
  ST.forEach((s, k) => { const o = new Set(), t = stepText(s), gk = G[k] || {};
    for (const l of (s.lv || [])){ const m = /^(Shader|Buffer|VAO|Program) (\d+)/.exec(l[1] || ''); if (m) o.add({Shader: 'sh', Buffer: 'buf', VAO: 'vao', Program: 'pr'}[m[1]] + ':' + m[2]); }
    const fm = /\b(gl\w+)\s*\((.*)\)\s*;?\s*$/.exec(t);
    if (fm){ const fn = fm[1], A = fm[2].split(/,(?![^()]*\))/).map(a => a.trim()), dv = {};
      for (const d of (s.dy || [])){ const re = /<code>(.*?)<\/code> = <b dir="ltr">(.*?)<\/b>/g; let m; while ((m = re.exec(d))) dv[m[1].replace(/&amp;/g, '&')] = m[2]; }
      for (const [i, ty] of (OBJ_ARGS[fn] || [])){ const a = A[i]; const val = /^\d+$/.test(a || '') ? a : dv[a]; if (val && val !== '0') o.add(ty + ':' + val); }
      if (/^glBuffer(Sub)?Data$/.test(fn) && gk.bbuf){ const b = gk.bbuf[/ELEMENT/.test(A[0]) ? 'E' : 'A']; if (b) o.add('buf:' + b); }
      if (/^gl(VertexAttribPointer|EnableVertexAttribArray|DisableVertexAttribArray)$/.test(fn) && gk.bvao){ o.add('vao:' + gk.bvao); if (fn === 'glVertexAttribPointer' && gk.bbuf && gk.bbuf.A) o.add('buf:' + gk.bbuf.A); }
      if (/^glUniform/.test(fn)){ for (const [id, p] of Object.entries(gk.pr || {})) if (p.use) o.add('pr:' + id); o.add('uni:' + k); }
      if (/^glDraw/.test(fn)){ const d = new Set(); const va = (gk.vaos || {})[gk.bvao];
        if (gk.bvao) d.add('vao:' + gk.bvao);
        if (va){ for (const a of Object.values(va.at || {})) if (a.on) d.add('buf:' + a.buf); if (va.ebo) d.add('buf:' + va.ebo); }
        for (const [id, p] of Object.entries(gk.pr || {})) if (p.use){ d.add('pr:' + id); for (const sid of (p.att || [])) d.add('sh:' + sid); }
        draws[k] = d; } }
    objs[k] = o; });
  JX = {id: P.id, objs, draws, G}; return JX; }
function journey(k){
  const X = jx(), t = stepText(ST[k]); if (/^\s*gl(Draw|Clear)/.test(t) || /glfwSwapBuffers/.test(t)) return null;
  const O = [...(X.objs[k] || [])].filter(o => !o.startsWith('uni:')); const isUni = [...(X.objs[k] || [])].some(o => o.startsWith('uni:'));
  if (!O.length && !isUni) return null;
  const out = [], seen = new Set([ST[k].v]); let firstDraw = -1, nDraw = 0;
  for (let j = k + 1; j < ST.length; j++){
    if (X.draws[j]){ const hit = isUni ? true : O.some(o => X.draws[j].has(o) && !(o.startsWith('buf:') && +(((X.G[j] || {}).bufs || {})[o.slice(4)] || {}).bytes === 0)); if (hit){ if (firstDraw < 0) firstDraw = j; nDraw++; }
      if (isUni) break; continue; }
    if (isUni) continue;
    const oj = X.objs[j]; if (!oj || seen.has(ST[j].v)) continue;
    if ([...oj].some(o => O.includes(o))){ seen.add(ST[j].v); if (out.length < 7) out.push(j); } }
  if (!out.length && firstDraw < 0) return null;
  return {O, out, firstDraw, nDraw, isUni}; }
function journeyHtml(k){
  const J = journey(k); if (!J) return '';
  const who = J.isUni ? 'القيمة دي' : J.O.map(o => { const [ty, n] = o.split(':'); return OBJ_NAME[ty] ? OBJ_NAME[ty](n) : o; }).join(' و ');
  const item = (j, extra) => `<li><button type="button" class="ugo" data-go="${j}">خطوة ${j + 1} ▶</button> <span class="jt">${esc(ST[j].ti)}</span>${extra ? ` <b>${extra}</b>` : ''}<code class="uc">${esc(stepText(ST[j]))}</code></li>`;
  const times = n => n === 1 ? 'مرة كمان' : n === 2 ? 'مرتين كمان' : n <= 10 ? `${n} مرات كمان` : `${n} مرة كمان`;
  const list = J.out.map(j => [j, '']);
  if (J.firstDraw >= 0){ const ty = J.isUni ? 'uni' : J.O[0].split(':')[0];
    const deleted = ty === 'sh' && [k, ...J.out.filter(j => j < J.firstDraw)].some(j => /glDeleteShader/.test(stepText(ST[j])));
    const what = {sh: 'أول مرة الـ Shader ده يشتغل فعلاً على الكارت' + (deleted ? ' (النسخة اللي جوه الـ Program، لأن الـ Shader المنفصل اتمسح)' : ''), pr: 'أول رسم بيستخدم الـ Program ده', buf: 'أول مرة الكارت يقرا الأرقام دي وهو بيرسم', vao: 'أول رسم بيقرا ورقة التعليمات دي', uni: 'الرسم اللي بيستخدم القيمة دي'}[ty] || 'أول رسم بيستخدمه';
    list.push([J.firstDraw, '← ' + what + (J.nDraw > 1 && !J.isUni ? `، وبعدها ${times(J.nDraw - 1)} في اللفات اللي بعدها` : '')]); }
  list.sort((x, y) => x[0] - y[0]);
  return `<details class="jr2"><summary><b>🔗 رحلته بعد كده</b> — ${who}</summary><ol class="jl">` + list.map(([j, e]) => item(j, e)).join('') + '</ol></details>'; }
function whyHtml(k){
  const s = ST[k], t = stepText(s); if (t === '{' || t === '}' || t === '};') return '';
  const P2 = purposeOf(t), U = allUses(k);
  let h = P2.length ? `<details class="why2"><summary><b>🎯 هيفيدنا بإيه؟</b></summary>${P2.join(' ')}</details>` : '';
  if (U) h += U.uses.length ? `<details class="use2"><summary><b>📍 هنستخدم <code>${esc(U.v)}</code> في إيه؟</b> <span class="sm">(${U.uses.length === 1 ? 'في سطر واحد بعد كده' : `في عدد ${U.uses.length} سطور بعد كده، بالترتيب`})</span></summary><ol class="jl">${U.uses.map(u => `<li><button type="button" class="ugo" data-go="${u.j}">خطوة ${u.j + 1} ▶</button> سطر ${esc(u.line)}<code class="uc">${esc(u.t)}</code>${(r => r ? `<span class="ur"><b>يعني:</b> ${r}</span>` : '')(useRole(U.v, u.j))}</li>`).join('')}</ol></details>`
    : `<span class="use2"><b>📍 <code>${esc(U.v)}</code>:</b> مفيش سطر بعده بيقراه في التشغيل ده.</span>`;
  h += journeyHtml(k);
  return h; }
