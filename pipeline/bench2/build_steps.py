import re
"""Turn the real gdb traces into step data for the multi-program bench page.
Output: progs.json  {programs:[...]}  (frames embedded as PNG data URIs)."""
import json, re, io, base64, hashlib, html, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, '/home/claude/bench2')
import edicts
from fullex import FULL

WORK = '/home/claude/bench2/work'
E = edicts.load()

PROGS = [
  # id, day, kind, title, desc, sources
  ('d1_u1', 1, 'رسم', 'Uniform: لون ثابت', 'مستطيل من مثلثين بـ glDrawElements، ولونه جاي من uniform اسمه u_Color.',
   ['/home/claude/day1/full/u/u1.cpp']),
  ('d1_u2', 1, 'رسم', 'Uniform: لون بيتغير', 'نفس المستطيل، بس الأحمر r بيزيد كل لفة، فاللون بيتغير وانت بتتفرج.',
   ['/home/claude/day1/full/u/u2.cpp']),
  ('d1_cam', 1, 'CAD', 'الكاميرا (3 ملفات)', 'هرم ملوّن بكاميرا: main.cpp و shaderClass.cpp و Camera.cpp. الكود بينط بين الملفات.',
   ['/home/claude/day1/full/4_camera/main.cpp', '/home/claude/day1/full/4_camera/shaderClass.cpp', '/home/claude/day1/full/4_camera/Camera.cpp']),
  ('d1_p1', 1, 'برمجة', 'Pointers 1: nullptr', '3 Pointers فاضيين بـ 0 و NULL و nullptr: الـ 3 نفس القيمة (0).',
   ['/home/claude/day1/full/p/p1.cpp']),
  ('d1_p2', 1, 'برمجة', 'Pointers 2: عنوان متغير', 'void* ptr = &var: الـ Pointer شايل نفس عنوان var.',
   ['/home/claude/day1/full/p/p2.cpp']),
  ('d1_p3', 1, 'برمجة', 'Pointers 3: النوع', 'int* و double* على نفس العنوان: العنوان واحد، والنوع بيقول نقرا كام بايت.',
   ['/home/claude/day1/full/p/p3.cpp']),
  ('d1_p4', 1, 'برمجة', 'Pointers 4: الكتابة من خلال العنوان', '*ptr = 10 غيّر var نفسه من 8 لـ 10.',
   ['/home/claude/day1/full/p/p4.cpp']),
  ('d1_p5', 1, 'برمجة', 'Pointers 5: new و memset', 'حجز 8 بايت على الـ Heap بـ new، وتصفيرهم بـ memset، وطباعتهم، و delete[].',
   ['/home/claude/day1/full/p/p5.cpp']),
  ('d1_p6', 1, 'برمجة', 'Pointers 6: Pointer لـ Pointer', 'char** ptr = &buffer: عنوان متغير شايل عنوان.',
   ['/home/claude/day1/full/p/p6.cpp']),
  ('d1_dot', 1, 'رياضيات', 'الضرب النقطي (dot)', 'دالة dot بإيدنا على متجهات 2D و 4D، وبعدين glm::dot.',
   ['/home/claude/day1/full/3_dot/main.cpp']),
  ('d2_va1', 2, 'رسم', 'Vertex Attributes: مكان بس', 'مثلث برتقاني. كل ركن فيه رقمين (x, y) بس.',
   ['/home/claude/day2/src/va1_positions.cpp']),
  ('d2_va2', 2, 'رسم', 'Vertex Attributes: مكان + لون', 'مثلث ألوانه متدرجة. كل ركن فيه 5 أرقام: x, y ثم r, g, b.',
   ['/home/claude/day2/src/va2_colors.cpp']),
  ('d2_c1', 2, 'برمجة', 'C: أول برنامج', 'أول برنامج بلغة C: printf بدل cout.',
   ['/home/claude/day2/src/c1_hello.c']),
  ('d2_c2', 2, 'برمجة', 'C: malloc و free', 'حجز مصفوفة على الـ Heap بـ malloc وملاها وطباعتها و free.',
   ['/home/claude/day2/src/c2_malloc.c']),
  ('d2_c3', 2, 'برمجة', 'C: حساب العناوين', 'p + 1 بينط 4 بايت (حجم int): Pointer arithmetic.',
   ['/home/claude/day2/src/c3_ptr_arith.c']),
  ('d2_c4', 2, 'برمجة', 'doubleIt بالـ Pointer', 'دالة بتاخد عنوان score وتضاعفه: 21 بقت 42.',
   ['/home/claude/day2/src/c4_double_it.cpp']),
  ('d2_d1', 2, 'رياضيات', 'الضرب النقطي وطول المتجه', 'dot بإيدنا، والطول = جذر (v · v).',
   ['/home/claude/day2/src/d1_dot_length.cpp']),
  ('d2_v1', 2, 'CAD', 'vector: الأساسيات', 'vector من Vertex: push_back والحجم والوصول بالـ index.',
   ['/home/claude/day2/src/v1_basics.cpp']),
  ('d2_v2', 2, 'CAD', 'vector: اللوبات', 'اللف على الـ vector بالـ index وبـ for-each وبالـ Reference.',
   ['/home/claude/day2/src/v2_loops.cpp']),
  ('d2_v3', 2, 'CAD', 'vector: إضافة ومسح', 'push_back و erase وطباعة الـ vector كله.',
   ['/home/claude/day2/src/v3_full.cpp']),
  ('d2_v4', 2, 'CAD', 'نقط الـ CAD في vector', 'تخزين نقط رسمة CAD في vector وطباعتها.',
   ['/home/claude/day2/src/v4_cad_points.cpp']),
  ('d2_v5', 2, 'CAD', 'vector بيكبر إزاي', 'push_back 10 مرات: شوف size و capacity، وامتى الـ vector بيتنقل لمكان جديد.',
   ['/home/claude/day2/src/v5_growth.cpp']),
  ('d3_s1', 3, 'رسم', 'الـ Shader من ملف (بنش التلات)', 'المثلث الأزرق: الـ Shaders متكتبين في ملف Basic.shader، والبرنامج بيقراه سطر سطر بـ getline قبل ما يبعته للكارت.',
   ['/home/claude/day3/src/s1_shader_file.cpp', '/home/claude/day3/src/res/shaders/Basic.shader']),
  ('d3_l1', 3, 'CAD', 'خط واحد بنقطتين', 'أول أمر CAD: خط بين نقطتين، والنقطتين مرسومين كمربعات برتقاني.',
   ['/home/claude/day3/src/l1_line.cpp']),
  ('d3_l2', 3, 'CAD', 'خطوط بالضغط بالماوس', 'كل ضغطتين بالماوس = خط. هنا 5 ضغطات حقيقية اتبعتت للشباك وانت شايف الدالة بتتنده.',
   ['/home/claude/day3/src/l2_click_lines.cpp']),
  ('d3_r1', 3, 'برمجة', 'Reference: اسم تاني', 'int& ref = a: نفس العنوان، صندوق واحد باسمين.',
   ['/home/claude/day3/src/r1_reference.cpp']),
  ('d3_r2', 3, 'برمجة', 'Increment بـ 3 طرق', 'نسخة، و Pointer، و Reference: مين بيغيّر a فعلاً.',
   ['/home/claude/day3/src/r2_increment.cpp']),
  ('d3_r3', 3, 'برمجة', 'Reference مش بيتنقل', 'ref = b نسخ قيمة b جوه a، والـ Pointer بس اللي يقدر يشاور على حاجة تانية.',
   ['/home/claude/day3/src/r3_rebind.cpp']),
  ('d3_r4', 3, 'برمجة', 'References (كود The Cherno)', 'مثال The Cherno: Increment بالـ Pointer وبالـ Reference، و LOG.',
   ['/home/claude/day3/src/r4_cherno.cpp']),
  ('d3_h1', 3, 'برمجة', 'Hamming بـ strlen (C)', 'تمرين exercism: عدد الحروف المختلفة بين سلسلتين DNA، بالـ index.',
   ['/home/claude/day3/src/h1_hamming_strlen.c']),
  ('d3_h2', 3, 'برمجة', 'Hamming بالـ Pointers (C)', 'نفس التمرين، بس الـ Pointers هي اللي بتمشي على الحروف.',
   ['/home/claude/day3/src/h2_hamming_pointers.c']),
  ('d3_x1', 3, 'رياضيات', 'الضرب الاتجاهي (cross)', 'cross في 2D (رقم) و 3D (متجه) بإيدنا.',
   ['/home/claude/day3/src/x1_cross.cpp']),
  ('d4_e1', 4, 'رسم', 'مستطيل بـ 6 أركان', 'مستطيل من مثلثين بـ glDrawArrays: 6 أركان، فيهم ركنين متكررين.',
   ['/home/claude/day4/src/e1_rect_arrays.cpp']),
  ('d4_e2', 4, 'رسم', 'مستطيل بـ Index Buffer', 'نفس المستطيل بـ 4 أركان بس + جدول أرقام (EBO) و glDrawElements.',
   ['/home/claude/day4/src/e2_rect_indices.cpp']),
  ('d4_v1', 4, 'CAD', 'بيت وشمس: VAO اتنين', 'رسمتين كل واحدة ليها VAO و Buffer: البيت خطوط بيضا، والشمس صليب أصفر.',
   ['/home/claude/day4/src/v1_two_vaos.cpp']),
  ('d4_v2', 4, 'CAD', 'Polyline بالماوس', 'ضغطة شمال = نقطة في الخط الشغال، ضغطة يمين = اقفل الخط وابدأ واحد جديد. 10 ضغطات حقيقية.',
   ['/home/claude/day4/src/v2_polylines.cpp']),
  ('d4_st1', 4, 'برمجة', 'static: ملفين', 'نفس الأسماء في main.cpp و static.cpp، واللي في static.cpp مخفي بـ static.',
   ['/home/claude/day4/src/st1/main.cpp', '/home/claude/day4/src/st1/static.cpp']),
  ('d4_st2', 4, 'برمجة', 'extern: ملفين', 'main.cpp بيستخدم متغير متعرّف في static.cpp بـ extern.',
   ['/home/claude/day4/src/st2/main.cpp', '/home/claude/day4/src/st2/static.cpp']),
  ('d4_c1', 4, 'برمجة', 'const مع الـ Pointers', 'الأربع حالات: const قبل النجمة وبعدها وفي الحتتين.',
   ['/home/claude/day4/src/c1_const_pointers.cpp']),
  ('d4_c2', 4, 'برمجة', 'const مع الدوال و mutable', 'GetX const، و PrintEntity بـ const&، وعدّاد mutable.',
   ['/home/claude/day4/src/c2_const_method.cpp']),
  ('d4_x1', 4, 'رياضيات', 'Cross product (Khan)', 'مثال الفيديو [1,‎-7,1] × [5,2,4] و 4 تمارين، والتأكد إن الناتج عمودي.',
   ['/home/claude/day4/src/x1_cross_khan.cpp']),
  ('d5_p1', 5, 'برمجة', 'swap بالـ Pointers (كود الفيديو)', 'برنامج Terminal من غير شباك: دالة swap بتاخد عنوان x وعنوان y وتبدّلهم من خلالهم.',
   ['/home/claude/day5/src/p1_swap_pointers.cpp']),
  ('d5_p2', 5, 'برمجة', 'swap بـ 3 طرق والعناوين', 'برنامج Terminal: نفس التبديل بالقيمة وبالـ Pointer وبالـ Reference، وكل دالة بتطبع عناوين اللي استلمته.',
   ['/home/claude/day5/src/p2_swap_three.cpp']),
  ('d5_n1', 5, 'رياضيات', 'أساسيات NumPy (Python)', 'برنامج Python: مصفوفات NumPy وشكلها ونوعها وحجمها، والحساب على كل العناصر، وتحذير النسخ.',
   ['/home/claude/day5/src/n1_numpy_basics.py']),
  ('d5_n2', 5, 'رياضيات', 'dot و cross في NumPy (Python)', 'برنامج Python: الضرب النقطي والاتجاهي لمثال Khan Academy، والطول والزاوية، وكذا متجه مرة واحدة.',
   ['/home/claude/day5/src/n2_dot_cross.py']),
  ('d5_r1', 5, 'رسم', 'مثلث أحمر (كود The Cherno)', 'Shader مكتوب كنص std::string، ومعاه فحص أخطاء الترجمة. المثلث أحمر.',
   ['/home/claude/day5/src/r1_red_triangle.cpp']),
  ('d5_r2', 5, 'رسم', 'تعديل الـ Shader', 'نفس البرنامج، بس الـ Vertex بيكبّر المثلث مرة ونص، والـ Fragment بيلوّن كل بكسل حسب مكانه.',
   ['/home/claude/day5/src/r2_shader_edit.cpp']),
  ('d5_c1', 5, 'CAD', 'أسماء في vector لحد Q', 'برنامج Terminal (كود فيديو push_back و pop_back): اتكتب في الكيبورد Braden و Jeff و Katie و Q، وشوف الـ vector بيكبر في الرام.',
   ['/home/claude/day5/src/c1_names_vector.cpp']),
  ('d5_c2', 5, 'CAD', 'مسح آخر خط بـ Backspace', 'Polylines بالماوس، وزرار Backspace بيمسح آخر خط بـ pop_back. 11 حدث حقيقي (ماوس وكيبورد).',
   ['/home/claude/day5/src/c2_delete_last_line.cpp']),
  ('d6_p1', 6, 'برمجة', 'Compiler صغير من الصفر', 'برنامج Terminal (فكرة محاضرة Erik Schierboom): الكود var x = 1 + 2 * 3; x * 2; بيتحوّل لـ Tokens، وشجرة، و Bytecode، وبيتنفذ على Stack. النتيجة 14.',
   ['/home/claude/day6/src/p1_tiny_compiler.cpp']),
  ('d6_p2', 6, 'برمجة', 'exercism: Leap', 'برنامج Terminal: السنة كبيسة ولا لأ، و 6 اختبارات PASS أو FAIL.',
   ['/home/claude/day6/src/p2_leap.cpp']),
  ('d6_p3', 6, 'برمجة', 'exercism: Raindrops', 'برنامج Terminal: 3 = Pling و 5 = Plang و 7 = Plong، و 7 اختبارات.',
   ['/home/claude/day6/src/p3_raindrops.cpp']),
  ('d6_m1', 6, 'رياضيات', 'dot والطول بإيدنا (Python)', 'برنامج Python من غير مكتبات: دالة dot بلوب، والطول = جذر (a · a)، وأمثلة Khan.',
   ['/home/claude/day6/src/m1_dot_length.py']),
  ('d6_m2', 6, 'رياضيات', 'مراجعة بـ NumPy والخصائص', 'برنامج Python: نفس الأرقام بـ NumPy، والترتيب والتوزيع، ومتجه طوله 1.',
   ['/home/claude/day6/src/m2_numpy_review.py']),
  ('d6_r1', 6, 'رسم', 'ألوان متحركة (كود The Cherno)', 'مستطيل بـ Index Buffer، ولونه من uniform اسمه u_Color، والأحمر بيطلع وينزل كل فريم.',
   ['/home/claude/day6/src/r1_animated_color.cpp']),
  ('d6_r2', 6, 'رسم', 'ألوان بالوقت (u_Time)', 'الـ CPU بيبعت الوقت بس بـ glUniform1f، والـ Fragment بيحسب لون لكل بكسل بـ sin.',
   ['/home/claude/day6/src/r2_time_colors.cpp']),
  ('d6_c1', 6, 'CAD', 'Refactoring لبرنامج مسح آخر خط', 'نفس برنامج امبارح بنفس الدوسات (11 حدث حقيقي)، بس الكود مترتب: ثوابت، ودوال صغيرة بأسماء أفعال، و DrawScene.',
   ['/home/claude/day6/src/c1_refactored.cpp']),
  ('d7_p1', 7, 'برمجة', 'مراجعة الـ Pointers (أمثلة The Cherno)', 'برنامج Terminal: void* و int* والكتابة من خلال العنوان، وحجم الـ Pointer، و 8 بايت على الـ Heap، و Pointer لـ Pointer.',
   ['/home/claude/day7/src/p1_pointers_review.cpp']),
  ('d7_p2', 7, 'برمجة', 'اختبر نفسك: 4 دوال بالـ Pointers', 'برنامج Terminal: Swap و SetToZero و MakeText (char**) و Sum، وكل واحدة باختبار PASS أو FAIL.',
   ['/home/claude/day7/src/p2_pointer_quiz.cpp']),
  ('d7_m1', 7, 'رياضيات', 'اختبر نفسك: Cross product (Python)', 'برنامج Python من غير مكتبات: 7 أسئلة في الضرب الاتجاهي بتصحّح نفسها، ومثال Khan [1, ‎-7, 1] × [5, 2, 4].',
   ['/home/claude/day7/src/m1_cross_quiz.py']),
  ('d7_m2', 7, 'رياضيات', 'np.cross والـ Normal', 'برنامج Python: نفس المثال بـ NumPy، ومتجهين على خط واحد، والـ Normal بتاع مثلث.',
   ['/home/claude/day7/src/m2_numpy_cross.py']),
  ('d7_r1', 7, 'رسم', 'Vertex Array (كود The Cherno)', 'Core Profile: ربط من غير VAO بيترفض (1282). وبعدين نفك كل حاجة ونربط الـ Program والـ VAO في اللوب قبل الرسم.',
   ['/home/claude/day7/src/r1_vertex_array.cpp']),
  ('d7_r2', 7, 'رسم', 'تجربة حرة: الطريقتين جنب بعض', 'مربع ومثلث بـ Layout مختلف: الشمال بـ VAO لكل حاجة، واليمين بـ VAO واحد بيتعاد ربطه. نفس البكسلات.',
   ['/home/claude/day7/src/r2_two_methods.cpp']),
  ('d7_c1', 7, 'CAD', 'الـ ID بتاع الـ Commit (Python)', 'برنامج Python: بصمة SHA-1 للملف ثم الفولدر ثم الـ Commit، ويطلع نفس 84180e1 اللي Git طلّعه.',
   ['/home/claude/day7/src/c1_commit_id.py']),
  ('d8_p1', 8, 'برمجة', 'Classes: اللاعب (كود The Cherno)', 'كلاس Player فيه x و y و speed ودالة Move: نفس الحركة كـ Method وكدالة برّه، و Object تاني، والـ Object في الرام (12 بايت).',
   ['/home/claude/day8/src/p1_player.cpp']),
  ('d8_p2', 8, 'برمجة', 'عداد private و this', 'كلاس Counter بيحمي العداد: Add بترفض السالب، و this جوه الدالة = عنوان الـ Object.',
   ['/home/claude/day8/src/p2_counter.cpp']),
  ('d8_t1', 8, 'رسم', 'Texture: صورة على مربع', 'كود The Cherno في ملف واحد: stb_image بيقرا logo.png، و glTexImage2D بيبعتها للكارت، والـ Shader بيلوّن بيها المربع بشفافية.',
   ['/home/claude/day8/src/t1_texture.cpp']),
  ('d8_t2', 8, 'رسم', 'إعدادات الـ Texture الأربعة', 'صورة 4 × 4 في Textureين وخانتين: NEAREST و LINEAR، و REPEAT و CLAMP_TO_EDGE لما الإحداثيات توصل 2.',
   ['/home/claude/day8/src/t2_settings.cpp']),
  ('d8_m1', 8, 'رياضيات', 'المصفوفة عمود عمود (Python)', 'برنامج Python من غير مكتبات: الأعمدة = فين î و ĵ راحوا، ومثال 3Blue1Brown والدوران والقص والكبس على خط.',
   ['/home/claude/day8/src/m1_matrix_columns.py']),
  ('d8_m2', 8, 'رياضيات', 'NumPy والشبكة قبل وبعد', 'M @ v والأعمدة، ومربع الوحدة، وتحويلين في مصفوفة، ورسم الشبكة بعد كل تحويل في grids.png.',
   ['/home/claude/day8/src/m2_numpy_grid.py']),
  ('d8_c1', 8, 'CAD', 'B-Rep: المكعب والهرم', 'كلاسات Vertex و Edge و Face و Body: قانون أويلر (F − E + V = 2) وعد الأضلاع المكشوفة، ومكعب من غير غطا.',
   ['/home/claude/day8/src/c1_brep.cpp']),
  ('d8_c2', 8, 'CAD', 'من B-Rep لـ Wireframe', 'نفس المكعب: الأضلاع بقت ترتيب رسم GL_LINES، والأركان نقط، والوش القدام برتقاني بـ VAO تاني.',
   ['/home/claude/day8/src/c2_wireframe.cpp']),
  ('d9_p1', 9, 'برمجة', 'struct مقابل class (كود The Cherno)', 'نفس اللاعب مرة struct ومرة class: نفس الحركة ونفس الحجم (12 بايت). والفرق في public بس. و Vec2 مثال الـ struct البسيط.',
   ['/home/claude/day9/src/p1_struct_class.cpp']),
  ('d9_p2', 9, 'برمجة', 'الركن struct = الـ stride', 'struct Vertex فيه x و y و u و v: حجمه 16 = الـ stride، و offsetof(u) = 8 = الـ offset، ونفس البايتات كصف أرقام.',
   ['/home/claude/day9/src/p2_vertex_struct.cpp']),
  ('d9_t1', 9, 'رسم', 'قطة Pixel Art (Victor Gordan)', 'stbi_load بـ 0 قنوات، و glTexImage2D بـ GL_RGBA، و glGenerateMipmap، و NEAREST عشان المربعات تفضل حادة. الكود في ملفين: pixel_cat.cpp و stb.cpp.',
   ['/home/claude/day9/src/t1_pixel_cat.cpp', '/home/claude/day9/src/stb.cpp']),
  ('d9_t2', 9, 'رسم', 'الأنواع الأربعة للتكرار (WRAP)', 'صورة واحدة في 4 Textures: REPEAT و MIRRORED_REPEAT و CLAMP_TO_EDGE و CLAMP_TO_BORDER بلون أحمر، والإحداثيات من ‎-0.5 لـ 1.5.',
   ['/home/claude/day9/src/t2_wrap_modes.cpp', '/home/claude/day9/src/stb.cpp']),
  ('d9_m1', 9, 'رياضيات', 'التحويل T من ℝ³ لـ ℝ² (Python)', 'مثال Khan بالظبط: T(1, 1, 1) = (3, 3) و T(2, 4, 1) = (10, 3)، ونفس T كمصفوفة 2 × 3، وتحويل مش خطي للمقارنة.',
   ['/home/claude/day9/src/m1_transform.py']),
  ('d9_m2', 9, 'رياضيات', 'إسقاط المكعب مصفوفة (NumPy)', 'المعادلة بتاعة wireframe.cpp امبارح بقت مصفوفة P مقاسها 2 × 3: نفس الأرقام، وخاصية الخطي، والرسمة في projection.png.',
   ['/home/claude/day9/src/m2_projection.py']),
  ('d9_c1', 9, 'CAD', 'المكعب مثلثات و Barycentric', '12 مثلث: 240 بايت بالأرقام بدل 432، و E = 18 بـ std::set وأويلر 2، و α و β و γ لأربع نقط (جوه، ضلع، ركن، برّه).',
   ['/home/claude/day9/src/c1_mesh.cpp']),
  ('d9_c2', 9, 'CAD', 'الكارت بيلوّن بالـ Barycentric', 'مثلث أحمر وأخضر وأزرق: بنحسب لون بكسل بـ α و β و γ على الـ CPU ونقارنه بـ glReadPixels: نفس الأرقام.',
   ['/home/claude/day9/src/c2_barycentric.cpp']),
  ('d10_p1', 10, 'برمجة', 'Constructors (كود The Cherno)', 'Entity من غير Constructor بيطبع أرقام عجيبة، و Entity() بيحط أصفار، و Entity(float, float) بيتختار حسب القوسين، و Log() = delete.',
   ['/home/claude/day10/src/p1_constructor.cpp']),
  ('d10_p2', 10, 'برمجة', 'Destructors: إمتى الـ object بيموت؟', 'Created و Destroyed: على الـ Stack عند الـ }، وعلى الـ Heap عند delete، و Buffer بيحجز في الـ Constructor ويرجّع في الـ Destructor.',
   ['/home/claude/day10/src/p2_destructor.cpp']),
  ('d10_t1', 10, 'رسم', 'Texture class: صندوق على مستطيل', 'الـ Constructor بيحمّل crate.png (3 قنوات ← GL_RGB) ويرفعها للكارت، وكل ركن ليه لون بيتضرب في الصورة. والـ Destructor بيمسح الـ Texture. الكود في ملفين: crate.cpp و stb.cpp.',
   ['/home/claude/day10/src/t1_crate.cpp', '/home/claude/day10/src/stb.cpp']),
  ('d10_t2', 10, 'رسم', 'صورتين في خانتين (mix)', 'Texture crate في الخانة 0 و Texture face في الخانة 1، و mix بيحط الوش فوق الصندوق حسب الشفافية.',
   ['/home/claude/day10/src/t2_two_textures.cpp', '/home/claude/day10/src/stb.cpp']),
  ('d10_m1', 10, 'رياضيات', 'التحويل = مصفوفة أعمدتها T(e) (Python)', 'مثال Khan: مصفوفة الوحدة، و e₁ و e₂، و T(e₁) = (1, ‎-1, 4) و T(e₂) = (3, 5, 1) بقوا أعمدة A (3 × 2)، و A @ v = T(v).',
   ['/home/claude/day10/src/m1_matrix_columns.py']),
  ('d10_m2', 10, 'رياضيات', '4 مصفوفات على حرف F (NumPy)', 'تكبير ولف 90 وميل ومراية: كل مصفوفة من «e₁ راح فين و e₂ راح فين»، والرسمة في shapes.png.',
   ['/home/claude/day10/src/m2_shape_transforms.py']),
  ('d10_c1', 10, 'CAD', 'مخطط B-Rep للأسطوانة', 'structs للأركان والأضلاع والحلقات والوشوش زي Glen Gray: 2 و 3 و 3، وكل ضلع متلمس مرتين، و C(t) و S(u, v).',
   ['/home/claude/day10/src/c1_brep_cylinder.cpp']),
  ('d10_c2', 10, 'CAD', 'صندوق بخرم ومكعبين في ضلع', 'الخرم = حلقة تانية في الوش (Trim Loop): V - E + F - (loops - F) = 0. والمكعبين: الضلع 2-6 متلمس 4 مرات = مش Manifold.',
   ['/home/claude/day10/src/c2_brep_hole.cpp']),
  ('d11_p1', 11, 'برمجة', 'Stack و Heap (كود The Cherno)', 'int و int[5] و Vector3 على الـ Stack وبعدين بـ new على الـ Heap: الأحجام 4 و 20 و 12، والـ Stack لازق في بعض (12 بايت)، والـ Heap كل حتة بعد 32.',
   ['/home/claude/day11/src/p1_stack_heap.cpp']),
  ('d11_p2', 11, 'برمجة', 'السرعة وصورة 16 MB', 'عدد 100 Vector3 على الـ Stack وعدد 100 بـ new و delete، ودالة بتحجز صورة 2048 × 2048 × 4 على الـ Heap وترجّعها حية لـ main. الأوقات في البنش بالملي ثانية لأن البرنامج ماشي خطوة خطوة، ومن غير البنش: 16.37 ns للـ Stack و 33.29 ns للـ new + delete (وبمليون مرة: 3.18 و 16.41).',
   ['/home/claude/day11/src/p2_speed_size.cpp']),
  ('d11_t1', 11, 'رسم', 'التكرار بإيدنا (Wrap)', 'حرف F في 6 مستطيلات: فوق الكارت بيكرر (REPEAT و MIRRORED و CLAMP)، وتحت دالة Wrap في الـ Shader بتعمل نفس الحسبة. الكود في ملفين: wrap_by_hand.cpp و stb.cpp.',
   ['/home/claude/day11/src/t1_wrap_by_hand.cpp', '/home/claude/day11/src/stb.cpp']),
  ('d11_t2', 11, 'رسم', 'رقعة شطرنج من دالة ومن صورة 2 × 2', 'الكارت قال عدد الـ Texture Units (32)، والرقعة مرة من دالة Cem Yuksel ومرة من صورة 12 بايت بـ REPEAT و glPixelStorei.',
   ['/home/claude/day11/src/t2_procedural.cpp']),
  ('d11_m1', 11, 'رياضيات', 'جمع وطرح المصفوفات (أمثلة Khan)', 'A + B و B + A، و C - D = C + (‎-1) D، ودالة بتجمع خانة خانة، و 3 × 2 + 2 × 2 = undefined.',
   ['/home/claude/day11/src/m1_add_subtract.py']),
  ('d11_m2', 11, 'رياضيات', 'نحرّك بيت بجمع مصفوفة (NumPy)', 'البيت 6 × 2 + مصفوفة نقل كل صفوفها (3, 1)، والطرح بيرجّعه، وصف واحد بيكبس السقف، و 4 فريمات في moves.png.',
   ['/home/claude/day11/src/m2_move_shape.py']),
  ('d11_c1', 11, 'CAD', 'مكعب ProAnywhere في ملف OBJ', 'البرنامج بيكتب cube.obj (سطور v و f) ويقراه، ويحسب Normal كل وش من ترتيب الأركان: الستة outward، و V - E + F = 2.',
   ['/home/claude/day11/src/c1_obj_cube.cpp']),
  ('d11_c2', 11, 'CAD', 'الأسطوانة Mesh مقابل B-Rep', 'أسطوانة 8 حتت: 16 و 42 و 28 مقابل 2 و 3 و 3، وجدول الغلط R (1 - cos(ط/n))، و n = 256 لدقة 0.01 مم.',
   ['/home/claude/day11/src/c2_mesh_vs_brep.cpp']),
]

# ------------------------------------------------------------------ helpers
def esc(t): return html.escape(str(t), quote=False)

def nicetype(t):
    if not t: return t
    t = t.replace('std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >', 'std::string')
    t = re.sub(r'std::vector<([^<>]+?), std::allocator<\1 ?> ?>', r'std::vector<\1>', t)
    return t

def short(v, n=48):
    if v is None: return 'null'
    v = str(v)
    mv = re.match(r'^std::vector of length (-?\d+), capacity (-?\d+)(?: = (\{.*\}))?$', v, re.S)
    if mv:
        v = f'{mv.group(3) or "{}"}  size {mv.group(1)}, capacity {mv.group(2)}'
        if len(v) <= 90: return v
    m = re.match(r'^(0x[0-9a-f]+) "(.*)$', v)  # char* : address + text
    if m: v = '"' + m.group(2)
    v = re.sub(r'\d+\.\d{5,}', lambda m: f'{round(float(m.group()), 4):.4f}', v)      # 0.400000006 -> 0.4000, 0.349999994 -> 0.3500 (rounded, not cut)
    v = re.sub(r'(\d+\.\d*?)0+\b', r'\1', v); v = re.sub(r'(\d)\.(?=[,}\s)]|$)', r'\1', v)
    return v if len(v) <= n else v[:n - 1] + '…'

def parse_nums(v):
    if not v or not v.startswith('{'): return None
    try: return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:e[-+]?\d+)?', v)]
    except Exception: return None

def find_regions(lines):
    """function bodies: [startLine, endLine, name] by brace matching."""
    regs = []; k = 0; n = len(lines)
    sig = re.compile(r'^(?:static\s+|inline\s+)?[\w:<>\*&\s]+?\b([~\w]+(?:::[~\w]+)?)\s*\([^;]*\)\s*(?:const\s*)?(?:\{.*)?$')
    while k < n:
        L = lines[k]
        m = sig.match(L) if not L.startswith((' ', '\t', '#', '/', '}')) else None
        if m and m.group(1) not in ('if', 'while', 'for', 'return'):
            # find opening brace on this or next line
            j = k; depth = 0; opened = False
            while j < n:
                depth += lines[j].count('{') - lines[j].count('}')
                if '{' in lines[j]: opened = True
                if opened and depth <= 0: break
                if not opened and j > k + 1: break
                j += 1
            if opened: regs.append([k + 1, j + 1, m.group(1).split('::')[-1] + '()']); k = j + 1; continue
        k += 1
    return regs

def shader_ranges(lines):
    out = {'vs': [], 'fs': []}; cur = None
    for k, L in enumerate(lines):
        if 'R"(' in L:
            nm = L.lower(); cur = 'fs' if 'frag' in nm else 'vs'
        if cur: out[cur].append(k + 1)
        if cur and ')"' in L: cur = None
    return out

GLTITLE = {
 'glfwInit': 'تشغيل GLFW', 'glfwWindowHint': 'إعداد قبل فتح الشباك', 'glfwCreateWindow': 'فتح الشباك',
 'glfwMakeContextCurrent': 'توصيل الكارت بالشباك (Context)', 'glfwSwapInterval': 'تشغيل VSync', 'gladLoadGLLoader': 'GLAD بيجيب دوال الكارت',
 'gladLoadGL': 'GLAD بيجيب دوال الكارت', 'glViewport': 'مساحة الرسم (Viewport)', 'glGenVertexArrays': 'حجز VAO جديد', 'glBindVertexArray': 'ربط VAO',
 'glGenBuffers': 'حجز Buffer جديد', 'glBindBuffer': 'ربط Buffer', 'glBufferData': 'نسخ البايتات للكارت', 'glEnableVertexAttribArray': 'تفعيل خانة (Attribute)',
 'glVertexAttribPointer': 'وصف شكل الركن للكارت', 'glCreateShader': 'عمل Shader فاضي', 'glShaderSource': 'بعت نص الـ Shader', 'glCompileShader': 'ترجمة الـ Shader',
 'glGetShaderiv': 'سؤال: الترجمة نجحت؟', 'glCreateProgram': 'عمل Program فاضي', 'glAttachShader': 'تركيب Shader في الـ Program', 'glLinkProgram': 'ربط الـ Program (Link)',
 'glValidateProgram': 'التأكد من الـ Program', 'glDeleteShader': 'مسح الـ Shader', 'glUseProgram': 'استخدم الـ Program ده', 'glGetUniformLocation': 'هات رقم الـ uniform',
 'glUniform4f': 'بعت قيمة uniform', 'glUniform1f': 'بعت قيمة uniform (رقم واحد)', 'glUniform2f': 'بعت قيمة uniform (رقمين)', 'glGetError': 'سؤال: الكارت رفض أمر؟', 'glUniformMatrix4fv': 'بعت مصفوفة الكاميرا', 'glClearColor': 'اختيار لون المسح', 'glClear': 'مسح اللوحة اللي ورا',
 'glDrawArrays': 'أمر رسم (Draw call)', 'glDrawElements': 'أمر رسم بالـ Indices', 'glfwSwapBuffers': 'تبديل اللوحتين (Swap)', 'glfwPollEvents': 'شوف الماوس والكيبورد',
 'glfwWindowShouldClose': 'الشباك لسه مفتوح؟', 'glfwTerminate': 'قفل GLFW', 'glDeleteVertexArrays': 'مسح الـ VAO', 'glDeleteBuffers': 'مسح الـ Buffer',
 'glDeleteProgram': 'مسح الـ Program', 'glPointSize': 'حجم النقطة', 'glLineWidth': 'تخانة الخط', 'glfwSetMouseButtonCallback': 'تسجيل دالة الماوس', 'glfwSetKeyCallback': 'تسجيل دالة الكيبورد',
 'glfwGetCursorPos': 'مكان الماوس بالبكسل', 'glfwGetWindowSize': 'مقاس الشباك', 'glEnable': 'تشغيل خاصية', 'glfwGetKey': 'زرار متداس؟', 'glfwGetMouseButton': 'زرار الماوس متداس؟',
 'glfwSetInputMode': 'شكل الماوس', 'glGenTextures': 'حجز Texture جديدة', 'glBindTexture': 'ربط Texture', 'glTexParameteri': 'إعداد للـ Texture', 'glTexImage2D': 'نسخ الصورة للكارت',
 'glActiveTexture': 'اختيار خانة (Texture Slot)', 'glUniform1i': 'بعت قيمة uniform (رقم صحيح)', 'glBlendFunc': 'معادلة الشفافية (Blending)', 'glDeleteTextures': 'مسح الـ Texture', 'glGenerateMipmap': 'عمل النسخ المصغّرة (Mipmaps)', 'glTexParameterfv': 'إعداد للـ Texture (كذا رقم)', 'glReadPixels': 'قراية بكسل من الكارت', 'glfwGetTime': 'الوقت', 'glfwDestroyWindow': 'قفل الشباك', 'glGetShaderInfoLog': 'رسالة الخطأ',
}
GPU_ONLY = {'glClear', 'glDrawArrays', 'glDrawElements', 'glfwSwapBuffers'}

def unit_of(g, text):
    if g:
        f = g['fn']
        if f in GPU_ONLY: return 'GPU'
        if f.startswith('gl') and not f.startswith('glfw') and not f.startswith('glad'): return 'CPU→GPU'
    if re.search(r'\bgl[A-Z]\w*\s*\(', text) and not re.search(r'\bglfw\w*\(', text): return 'CPU→GPU'
    return 'CPU'

def png_uri(a):
    b = io.BytesIO(); Image.fromarray(a).save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

GLENUM = {'34962': 'GL_ARRAY_BUFFER', '34963': 'GL_ELEMENT_ARRAY_BUFFER', '35633': 'GL_VERTEX_SHADER', '35632': 'GL_FRAGMENT_SHADER'}
MODE_AR = {'GL_TRIANGLES': 'مثلثات مليانة', 'GL_LINES': 'خطوط (كل ركنين = خط)', 'GL_POINTS': 'نقط', 'GL_LINE_STRIP': 'خط متصل (Polyline)', 'GL_LINE_LOOP': 'خط مقفول'}


TYPES = [('unsigned int', 'رقم صحيح موجب (unsigned int)، 4 بايت'), ('int', 'رقم صحيح (int)، 4 بايت'), ('float', 'رقم عشري (float)، 4 بايت'),
         ('double', 'رقم عشري بدقة أكبر (double)، 8 بايت'), ('bool', 'صح أو غلط (bool)'), ('char', 'حرف (char)، بايت واحد'),
         ('GLuint', 'رقم صحيح موجب بتاع OpenGL (GLuint)، 4 بايت'), ('GLint', 'رقم صحيح بتاع OpenGL (GLint)'), ('GLFWwindow', 'الشباك اللي GLFW فتحه')]
def type_desc(tx, pl):
    m = re.match(r'^(?:static\s+|const\s+)*([\w:<>]+(?:\s+[\w:<>]+)?)\s*(\*|&)?\s+(\w+)\s*(\[(\d*)\])?', tx)
    if not m: return None
    ty, ptr, name, arr, n = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
    if ty in ('return', 'else', 'delete'): return None
    base = next((d for t, d in TYPES if ty == t), None)
    vec = re.match(r'std::vector<(.+)>', ty)
    if vec: d = f'std::vector: قايمة بتكبر لوحدها، كل عنصر فيها نوعه <code>{esc(vec.group(1))}</code>'
    elif ty.startswith('glm::mat4'): d = 'مصفوفة 4×4 أرقام (glm::mat4): 16 float = 64 بايت'
    elif ty.startswith('glm::vec3'): d = 'متجه 3 أرقام (glm::vec3): x و y و z'
    elif ty == 'std::string': d = 'نص (std::string)'
    elif ptr == '*': d = f'Pointer: مش هو الحاجة نفسها، ده <b>عنوانها</b> في الرام{(" (" + base + ")") if base else f" (<code>{esc(ty)}*</code>)"}'
    elif arr is not None:
        cnt = None
        if pl and name in pl:
            v = pl[name][2] or ''; nums = re.findall(r'-?\d+(?:\.\d+)?(?:e[-+]?\d+)?', v) if v.startswith('{') else []
            cnt = len(nums) if nums and '...' not in v else None
        cnt = cnt or (int(n) if n else None)
        unit = base.split('،')[0] if base else f'<code>{esc(ty)}</code>'
        size = (4 if ty in ('float', 'int', 'unsigned int', 'GLuint', 'GLint') else 8 if ty == 'double' else None)
        d = f'مصفوفة (array): صف من {(str(cnt) + (" عناصر" if 3 <= cnt <= 10 else " عنصر")) if cnt else "كذا عنصر"} ورا بعض، كل عنصر {unit}' + (f'. الحجم: <span dir="ltr">{cnt} × {size} = {cnt * size}</span> بايت' if cnt and size else '')
    elif base: d = base
    else: d = f'نوع <code>{esc(ty)}</code>'
    return (name, d)

# ------------------------------------------------------------------ main
def corner_groups(files, fname, line, name, vv):
    """Split a flat float array into corners, using how the source writes one corner per line."""
    f = next((x for x in files if x['name'] == fname), None)
    if not f or not any('glVertexAttribPointer' in l for x in files for l in x['lines']): return None
    L = f['lines']
    if not re.match(r'\s*float\s+' + re.escape(name) + r'\s*\[[^\]]*\]\s*=\s*\{\s*$', L[line - 1]): return None
    rows = []
    for l in L[line:]:
        if l.strip().startswith('}'): break
        nums = re.findall(r'-?\d+(?:\.\d+)?f?', l.split('//')[0])
        if nums: rows.append(len(nums))
    vals = [x.strip() for x in vv.strip('{}').split(',')]
    if not rows or len(set(rows)) != 1 or rows[0] < 2 or rows[0] * len(rows) != len(vals) or len(rows) > 12: return None
    S = set()
    for x in files:
        for l in x['lines']:
            m = re.search(r'glVertexAttribPointer\([^;]*?(?:sizeof\(float\)\s*\*\s*(\d+)|(\d+)\s*\*\s*sizeof\(float\))', l)
            if m: S.add(int(m.group(1) or m.group(2)))
    ks = [q for q in sorted(S, reverse=True) if rows[0] % q == 0]
    if not ks: return None
    k = rows[0] if rows[0] in ks else ks[0]; nc = len(vals) // k
    if k < 2 or nc > 12: return None
    names = {2: ' (x, y)', 3: ' (x, y, z)', 5: ': مكانه (x, y) ولونه (r, g, b)', 6: ': مكانه (x, y, z) ولونه (r, g, b)'}.get(k, '')
    cnt = {2: 'كل رقمين', 3: 'كل 3 أرقام', 5: 'كل 5 أرقام', 6: 'كل 6 أرقام'}.get(k, f'كل {k} أرقام')
    how = 'زي ما هي مكتوبة سطر لكل ركن في الكود' if k == rows[0] else ('في الكود كل سطر فيه ركنين' if rows[0] // k == 2 else f'في الكود كل سطر فيه {rows[0] // k} أركان')
    parts = [f'ركن {i} = <b dir="ltr">({", ".join(vals[i * k:(i + 1) * k])})</b>' for i in range(nc)]
    return (f'نفس الأرقام مقسومة على الأركان ({cnt} ورا بعض = ركن{names}، {how}): ' + '، '.join(parts)
            + f'. في الرام مفيش سطور: {len(vals)} {"أرقام" if len(vals) <= 10 else "رقم"} ورا بعض، والكارت هيعرف التقسيم ده بس من <code>glVertexAttribPointer</code>.')

def build(pid, day, kind, title, desc, srcs):
    build._gl = 0
    t = json.load(open(f'{WORK}/{pid}/trace.json')); W, H = t['W'], t['H']; T = t['steps']
    _cfg0 = json.load(open(f'{WORK}/{pid}/cfg.json'))
    if _cfg0.get('stdin'):   # what was typed on the keyboard: shown in the Terminal at the cin step that read it
        toks = open(_cfg0['stdin']).read().split()
        for st in T:
            if 'cin >>' in st['text'] and toks: st['typed'] = toks.pop(0)
    files = []; off = {}; v0 = 0
    for p in srcs:
        L = open(p).read().split('\n')
        if L and L[-1] == '': L = L[:-1]
        nm = os.path.basename(p); files.append({'name': nm, 'lines': L, 'off': v0}); off[nm] = v0; v0 += len(L)
    NV = v0
    PAL = ['#e0561c', '#3a8fbf', '#7d5cc4', '#c78512', '#0f766e', '#b0406a', '#5a7d2a', '#8a6a3a']
    regions = []; ci = 0; shl_extra = {'vs': [], 'fs': []}
    for fi, f in enumerate(files):
        if f['name'].endswith('.shader'):
            sl = f['lines']; cur = None
            for k, L in enumerate(sl):
                if '#shader' in L: cur = 'fs' if 'fragment' in L else 'vs'
                elif cur: shl_extra[cur].append(f['off'] + k + 1)
            continue
        shr = shader_ranges(f['lines']); inside = set(shr['vs'] + shr['fs'])
        regs = [r for r in find_regions(f['lines']) if r[0] not in inside]
        for a, b, n in regs:
            col = '#e0561c' if n == 'main()' else PAL[1 + ci % (len(PAL) - 1)]
            if n != 'main()': ci += 1
            regions.append([f['off'] + a, f['off'] + b, n, col, fi])
    shl = {'vs': list(shl_extra['vs']), 'fs': list(shl_extra['fs'])}
    for f in files:
        r = shader_ranges(f['lines']); shl['vs'] += [f['off'] + x for x in r['vs']]; shl['fs'] += [f['off'] + x for x in r['fs']]
    dE = E[f'day{day}']; over = E.get(f'day{day}_over', {})
    allE = {}
    for d in ['day4', 'day3', 'day2', 'day1']:
        for k, v in E[d].items(): allE.setdefault(k, v)
    def expl(fname, text):
        o = over.get(fname, {})
        return o.get(text) or dE.get(text) or allE.get(text) or ''
    for f in files: f['lx'] = [re.sub(r'\s*\(شرحه كلمة كلمة فوق\)', '', re.sub(r'<[^>]+>', '', expl(f['name'], l.strip()))) if l.strip() and l.strip() not in ('{', '}', '};') else '' for l in f['lines']]  # line notes for the offline helper
    cfg = json.load(open(f'{WORK}/{pid}/cfg.json')); clicks = cfg.get('clicks', [])

    # ---- frames
    frames = []; fidx = {}; rawcache = {}
    def load_raw(fn):
        if fn not in rawcache:
            a = np.fromfile(f'{WORK}/{pid}/frames/{fn}', dtype=np.uint8).reshape(H, W, 4)[::-1, :, :3].copy(); rawcache[fn] = a
        return rawcache[fn]
    def add_frame(a):
        h = hashlib.md5(a.tobytes()).hexdigest()
        if h not in fidx: fidx[h] = len(frames); frames.append(png_uri(a))
        return fidx[h]
    blank = np.zeros((H, W, 3), np.uint8)

    # ---- laps
    lap = None; laps_first = {}; exit_seen = False
    lapof = []
    for k, s in enumerate(T):
        if s.get('loopcheck'):
            lap = s['loopcheck']
            if s.get('closing'): exit_seen = True
        if exit_seen and not s.get('loopcheck') and s['depth'] == 1 and k > 0 and T[k-1].get('closing'): lap = None
        lapof.append(lap)
    # steps after the closing check are outside the loop
    seen_close = False
    for k, s in enumerate(T):
        if s.get('closing'): seen_close = True
        if seen_close: lapof[k] = None

    # ---- GPU model
    gpu = {'win': False, 'ctx': False, 'glad': False, 'vaos': {}, 'bufs': {}, 'sh': {}, 'pr': {}, 'uni': {}, 'bvao': 0, 'bbuf': {'A': 0, 'E': 0},
           'clear': [0, 0, 0, 1], 'ps': 1, 'depth': False, 'cb': None, 'vsync': None}
    nextVao = [1]; nextBuf = [1]; nextName = [1]; loc2name = {}
    back = None; front = None; termAll = []
    stack = []  # list of {fn, vars:{name:[val, uninit]}}
    out = []; cbcount = 0; prevFront = None
    lastMouse = [0, 0]

    def post_locals(k):
        """locals right after step k (same function frame): from the next step at the same depth & fn"""
        s = T[k]
        for j in range(k + 1, min(len(T), k + 400)):
            q = T[j]
            if q['depth'] == s['depth'] and q['fn'] == s['fn']: return {l[0]: l for l in q['locals']}
            if q['depth'] < s['depth']: return None
        return None

    for k, s in enumerate(T):
        fname = s['file']; v = off[fname] + s['line']; text = s['text']; g = s.get('gl'); fn = s['fn']
        d = s['depth']
        # stack
        prevdepth = len(stack)
        while len(stack) > d: stack.pop()
        while len(stack) < d: stack.append({'fn': fn, 'vars': {}})
        stack[-1]['fn'] = fn
        cur = {}
        for l in s['locals']:
            name, typ, val, decl, isarg = (l + [None] * 5)[:5]
            typ = nicetype(typ)
            uninit = (not isarg) and decl is not None and s['line'] <= decl and s['file'] == fname
            cur[name] = [short(val), bool(uninit), typ]
        stack[-1]['vars'] = cur
        ev = None
        entered = d > prevdepth and k > 0
        # callback entry
        if entered and fn in cfg.get('callbacks', []):
            # read the real callback arguments (GLFW: action 1 = press, 0 = release; button 0 = left, 1 = right)
            a_act = (cur.get('action') or ['1'])[0]; a_btn = (cur.get('button') or [None])[0]
            act = 'release' if a_act == '0' else 'press'
            if act == 'press': cbcount += 1
            idx = cbcount - 1
            c = clicks[idx] if 0 <= idx < len(clicks) else None
            if c and not c.get('key') and a_btn is not None: c = dict(c, btn=3 if a_btn == '1' else 1)
            if c and c.get('key'):
                ev = {'x': lastMouse[0], 'y': lastMouse[1], 'btn': 'key', 'key': c['key'], 'act': act}
            elif c:
                if c.get('x') or c.get('y'): lastMouse = [c['x'], c['y']]
                ev = {'x': lastMouse[0], 'y': lastMouse[1], 'btn': 'right' if c.get('btn') == 3 else 'left', 'act': act}
        pl = post_locals(k)
        before = {kk: vv[0] for kk, vv in cur.items() if not vv[1]}
        changes = []
        if pl is not None:
            for name, l in pl.items():
                nv = short(l[2], 3000); ov = cur.get(name)
                decl = l[3] if len(l) > 3 else None
                if decl is not None and s['line'] < decl: continue
                if '<incomplete' in nv: continue
                if ov is None or ov[1] or short(l[2]) != ov[0]:
                    if decl is not None and s['line'] != decl and ov is not None and ov[1]: continue
                    changes.append([name, nv])
        # ---- gpu effects + texts
        anim = None; live = []; dyn = []; unit = unit_of(g, text); fr = None; pix = None; mask = None
        gfn = g['fn'] if g else None
        args = g['args'] if g else []
        av = [a[1] for a in args]
        def A(i, default=None):
            return av[i] if i < len(av) and av[i] is not None else default
        assign = re.match(r'^(?:[\w:<>\*\s]+?\s+)?(\w+)\s*=\s*gl\w+\(', text)
        post = (lambda name: (pl or {}).get(name, [None, None, None])[2]) if True else None
        if gfn == 'glfwCreateWindow':
            gpu['win'] = True; anim = 'win'; live.append(['mon', 'الشباك', f'اتفتح شباك {A(0, W)} × {A(1, H)} بكسل'])
        elif gfn == 'glfwMakeContextCurrent':
            gpu['ctx'] = True; live.append(['ctx', 'Context', 'الكارت بقى شغال للشباك ده: أي أمر gl بعد كده يروحله'])
        elif gfn in ('gladLoadGLLoader', 'gladLoadGL') or 'gladLoad' in text:
            gpu['glad'] = True; live.append(['ctx', 'GLAD', 'عناوين دوال OpenGL اتجابت من الدرايفر'])
        elif gfn == 'glfwSwapInterval':
            gpu['vsync'] = A(0); live.append(['mon', 'VSync', f'التبديل هيستنى الشاشة ({A(0)} = استنى إطار واحد)'])
        elif gfn == 'glGenVertexArrays':
            vid = nextVao[0]; nextVao[0] += 1; gpu['vaos'][vid] = {'at': {}, 'ebo': 0}; anim = 'new'
            live.append(['vao', f'VAO {vid}', f'اتحجز VAO رقم {vid} (لسه فاضي)']); dyn.append(f'الكارت رجّع الرقم <b>{vid}</b>')
        elif gfn == 'glBindVertexArray':
            vid = int(A(0, '0') or 0); gpu['bvao'] = vid
            live.append(['vao', 'VAO', f'VAO {vid} بقى المربوط' if vid else 'فكّينا ربط الـ VAO (0 = ولا حاجة)'])
        elif gfn == 'glGenBuffers':
            bid = nextBuf[0]; nextBuf[0] += 1; gpu['bufs'][bid] = {'t': '', 'bytes': 0, 'vals': []}; anim = 'new'
            live.append(['buf', f'Buffer {bid}', f'اتحجز Buffer رقم {bid} على الكارت، لسه فاضي']); dyn.append(f'الكارت رجّع الرقم <b>{bid}</b>')
        elif gfn == 'glBindBuffer':
            tg = GLENUM.get(A(0), A(0)); bid = int(A(1, '0') or 0); key = 'E' if 'ELEMENT' in tg else 'A'
            gpu['bbuf'][key] = bid
            if key == 'E' and gpu['bvao']: gpu['vaos'][gpu['bvao']]['ebo'] = bid
            if bid and bid in gpu['bufs']: gpu['bufs'][bid]['t'] = 'EBO' if key == 'E' else 'VBO'
            live.append(['buf', f'Buffer {bid}' if bid else 'Buffer', (f'Buffer {bid} مربوط على {tg}' if bid else f'فكّينا ربط {tg}')])
        elif gfn == 'glBufferData':
            tg = GLENUM.get(A(0), A(0)); key = 'E' if 'ELEMENT' in tg else 'A'; bid = gpu['bbuf'][key]; nb = int(float(A(1, '0') or 0))
            nums = parse_nums(A(2) or '') or []
            if bid in gpu['bufs']: gpu['bufs'][bid].update({'bytes': nb, 'vals': [round(x, 3) for x in nums[:24]], 't': 'EBO' if key == 'E' else 'VBO'})
            anim = 'upload'; live.append(['buf', f'Buffer {bid}', f'اتنسخ {nb} بايت من الرام لـ Buffer {bid}'])
            dyn.append(f'الحجم الحقيقي: <b>{nb} بايت</b>' + (f' = {nb // 4} رقم × 4 بايت' if nb % 4 == 0 else ''))
        elif gfn == 'glEnableVertexAttribArray':
            loc = A(0, '0'); vv = gpu['vaos'].get(gpu['bvao'])
            if vv is not None: vv['at'].setdefault(loc, {})['on'] = True
            live.append(['vao', f'VAO {gpu["bvao"]}', f'الخانة {loc} اتفعّلت'])
        elif gfn == 'glVertexAttribPointer':
            loc, size, stride, offv = A(0, '0'), A(1, '?'), A(4, '0'), A(5, '0')
            offn = re.sub(r'^\(void ?\*\) ?', '', str(offv)); offn = str(int(offn, 16)) if str(offn).startswith('0x') else offn
            vv = gpu['vaos'].get(gpu['bvao'])
            if vv is not None: vv['at'].setdefault(loc, {}).update({'size': size, 'stride': stride, 'off': offn, 'buf': gpu['bbuf']['A']})
            anim = 'attr'; live.append(['vao', f'VAO {gpu["bvao"]}', f'خانة {loc}: {size} رقم، كل {stride} بايت، من بايت {offn}، من Buffer {gpu["bbuf"]["A"]}'])
        elif gfn == 'glCreateShader':
            sid = nextName[0]; nextName[0] += 1; ty = 'Fragment' if A(0) == '35632' or 'FRAG' in text else 'Vertex'
            gpu['sh'][sid] = {'ty': ty, 'st': 'new'}; anim = 'new'; live.append(['vs' if ty == 'Vertex' else 'fs', f'Shader {sid}', f'اتعمل {ty} Shader فاضي رقم {sid}'])
            dyn.append(f'النوع الحقيقي: <b>{GLENUM.get(A(0), A(0))}</b> = {A(0)}، والكارت رجّع <b>{sid}</b>')
        elif gfn == 'glShaderSource':
            sid = int(A(0, '0') or 0); sh = gpu['sh'].get(sid)
            if sh: sh['st'] = 'src'; live.append(['vs' if sh['ty'] == 'Vertex' else 'fs', f'Shader {sid}', 'النص بتاعه اتبعت للكارت (لسه مش مترجم)'])
            anim = 'src'
        elif gfn == 'glCompileShader':
            sid = int(A(0, '0') or 0); sh = gpu['sh'].get(sid)
            if sh: sh['st'] = 'ok'; live.append(['vs' if sh['ty'] == 'Vertex' else 'fs', f'Shader {sid}', 'اتترجم لأوامر الكارت'])
            anim = 'compile'
        elif gfn == 'glCreateProgram':
            pidn = nextName[0]; nextName[0] += 1; gpu['pr'][pidn] = {'att': [], 'linked': False, 'use': False}; anim = 'new'
            live.append(['prog', f'Program {pidn}', f'اتعمل Program فاضي رقم {pidn}']); dyn.append(f'الكارت رجّع <b>{pidn}</b>')
        elif gfn == 'glAttachShader':
            p_, sid = int(A(0, '0') or 0), int(A(1, '0') or 0)
            if p_ in gpu['pr']: gpu['pr'][p_]['att'].append(sid)
            live.append(['prog', f'Program {p_}', f'Shader {sid} اتركّب فيه'])
        elif gfn == 'glLinkProgram':
            p_ = int(A(0, '0') or 0)
            if p_ in gpu['pr']: gpu['pr'][p_]['linked'] = True
            anim = 'link'; live.append(['prog', f'Program {p_}', 'الـ Vertex والـ Fragment اتربطوا في برنامج واحد'])
        elif gfn == 'glDeleteShader':
            sid = int(A(0, '0') or 0)
            if sid in gpu['sh']: gpu['sh'][sid]['st'] = 'del'
            live.append(['vs' if gpu['sh'].get(sid, {}).get('ty') == 'Vertex' else 'fs', f'Shader {sid}', 'متعلّم عليه للمسح (نسخته جوه الـ Program فاضلة)'])
        elif gfn == 'glUseProgram':
            p_ = int(A(0, '0') or 0)
            for q in gpu['pr'].values(): q['use'] = False
            if p_ in gpu['pr']: gpu['pr'][p_]['use'] = True
            live.append(['prog', f'Program {p_}', 'بقى هو اللي هيترسم بيه'])
        elif gfn == 'glGetUniformLocation':
            nm = (A(1) or '').strip('"'); var = assign.group(1) if assign else None
            locv = post(var) if var else None
            if locv is not None: loc2name[str(locv)] = nm
            live.append(['prog', 'uniform', f'«{nm}» رقمه {locv}' if locv is not None else f'«{nm}»'])
            if locv is not None: dyn.append(f'الكارت رجّع رقم الخانة: <b>{locv}</b>')
        elif gfn and gfn.startswith('glUniform'):
            loc = A(0); nm = loc2name.get(str(loc), f'#{loc}')
            mq = re.search(r'glGetUniformLocation\([^,]+,\s*("?)([\w.]+)\1\s*\)', text)
            if mq:
                if mq.group(1): nm = mq.group(2)
                else:
                    vv_ = cur.get(mq.group(2)); mm = re.search(r'"([^"]*)', vv_[0]) if vv_ else None
                    nm = mm.group(1) if mm else mq.group(2)
            if 'Matrix' in gfn: val = 'مصفوفة 4×4'
            else: val = '(' + ', '.join(short(x, 8) for x in av[1:]) + ')'
            gpu['uni'][nm] = val; anim = 'uniform'; live.append(['prog', f'uniform {nm}', f'{nm} = {val}'])
            if 'Matrix' not in gfn and len(av) >= 5:
                try:
                    r, g_, b, _a = [float(x) for x in av[1:5]]; dyn.append(f'يعني اللون: أحمر {r:g}، أخضر {g_:g}، أزرق {b:g} → بالـ 0–255: <b>({round(r*255)}, {round(g_*255)}, {round(b*255)})</b>')
                except Exception: pass
        elif gfn == 'glClearColor':
            try: gpu['clear'] = [float(x) for x in av[:4]]
            except Exception: pass
            live.append(['car', 'لون المسح', 'اللون اللي glClear هتمسح بيه = (' + ', '.join(short(x, 6) for x in av[:4]) + ')'])
        elif gfn == 'glPointSize':
            gpu['ps'] = A(0); live.append(['ras', 'Rasterizer', f'كل نقطة هتترسم مربع {short(A(0), 6)} × {short(A(0), 6)} بكسل'])
        elif gfn == 'glEnable':
            if 'DEPTH' in text: gpu['depth'] = True
            live.append(['ras', 'Depth test', 'الكارت هيرسم القريب فوق البعيد'])
        elif gfn == 'glViewport':
            live.append(['ras', 'Viewport', f'الرسم في {A(2)} × {A(3)} بكسل'])
        elif gfn == 'glfwSetMouseButtonCallback':
            gpu['cb'] = 'MouseButtonCallback'; live.append(['mouse', 'الماوس', 'لما تدوس، GLFW هينده MouseButtonCallback لوحده'])
        elif gfn == 'glfwSetKeyCallback':
            live.append(['mouse', 'الكيبورد', 'لما تدوس زرار، GLFW هينده KeyCallback لوحده'])
        # frames from the real back buffer
        if s.get('fb'):
            fb = s['fb'][0] if isinstance(s['fb'], list) else s['fb']; a = load_raw(fb)
            prevA = rawcache.get('_back', blank)
            diff = np.any(a != prevA, axis=2); pix = int(diff.sum())
            cols = 32; rows = max(1, round(32 * H / W))
            bh, bw = H / rows, W / cols
            m = ''.join('1' if diff[int(r*bh):int((r+1)*bh), int(c*bw):int((c+1)*bw)].any() else '0' for r in range(rows) for c in range(cols))
            col = a[diff].mean(axis=0).astype(int).tolist() if pix else None
            mask = {'m': m, 'c': cols, 'r': rows, 'col': col, 'px': pix}
            fr = add_frame(a); rawcache['_back'] = a
            if gfn == 'glClear':
                anim = 'clear'; cc = a[H // 2, 2].tolist()
                live.append(['car', 'Back buffer', f'اللوحة اللي ورا اتمسحت كلها باللون ({cc[0]}, {cc[1]}, {cc[2]})'])
                dyn.append(f'اتمسح <b>{W*H:,}</b> بكسل ({W} × {H}) في ضربة واحدة على الكارت')
            else:
                anim = 'draw'; mode = next((x for x in MODE_AR if x in text), None)
                cnt = ''
                if gfn == 'glDrawArrays': cnt = f'ابدأ من ركن {A(1)} وخد {A(2)} ركن'
                elif gfn == 'glDrawElements': cnt = f'{A(1)} رقم من جدول الـ Indices (EBO)'
                live.append(['vs', 'Vertex Shader', f'اشتغل مرة لكل ركن: {cnt}' if cnt else 'اشتغل مرة لكل ركن'])
                live.append(['ras', 'Rasterizer', (f'{MODE_AR[mode]}: حدد البكسلات اللي جوه' if mode else 'حدد البكسلات اللي جوه')])
                live.append(['fs', 'Fragment Shader', f'لوّن {pix:,} بكسل' + (f' باللون ({col[0]}, {col[1]}, {col[2]})' if col else '') if pix else 'مفيش ولا بكسل اتغير (مفيش أركان كفاية)'])
                dyn.append(f'الكارت غيّر <b>{pix:,} بكسل</b> في اللوحة اللي ورا' + (f'، متوسط لونهم ({col[0]}, {col[1]}, {col[2]})' if col else '') + (f' · {cnt}' if cnt else ''))
            back = fr
        if gfn == 'glfwSwapBuffers':
            anim = 'swap'; prevFront = front; front = back; back = prevFront
            live.append(['car', 'Swap', 'اللوحتين اتبدلوا: اللي اترسم ورا بقى قدام']); live.append(['mon', 'الشاشة', 'بتعرض الصورة الجديدة دلوقتي'])
        if gfn == 'glfwPollEvents':
            anim = 'poll'; live.append(['mouse', 'Events', 'GLFW بيشوف: حد داس على حاجة؟'])
        if s.get('loopcheck'):
            anim = 'check'
            if s.get('closing'): dyn.append('الشباك اتطلب يتقفل (في التشغيل ده إحنا اللي طلبنا بعد آخر لفة)، فالشرط بقى false و<b>هنخرج من الـ while</b>.')
            else: dyn.append(f'الشباك لسه مفتوح → <b>ندخل اللفة رقم {s["loopcheck"]}</b>.')
        if ev and ev['btn'] == 'key':
            anim = 'click'
            act_ar = 'نزل (Press)' if ev['act'] == 'press' else 'اترفع (Release)'
            live.insert(0, ['mouse', 'زرار كيبورد', f'زرار {ev["key"]} {act_ar}'])
            dyn.append(f'محدش نده الدالة دي من الكود بتاعك: <b>GLFW ندهها لوحده جوه glfwPollEvents</b> لأن زرار {ev["key"]} في الكيبورد {act_ar}.')
        elif ev:
            anim = 'click'
            b_ar = 'الشمال' if ev['btn'] == 'left' else 'اليمين'
            act_ar = 'نزل (Press)' if ev['act'] == 'press' else 'اترفع (Release)'
            live.insert(0, ['mouse', 'ضغطة ماوس', f'زرار {b_ar} {act_ar} عند ({ev["x"]}, {ev["y"]})'])
            dyn.append(f'محدش نده الدالة دي من الكود بتاعك: <b>GLFW ندهها لوحده جوه glfwPollEvents</b> لأن زرار {b_ar} في الماوس {act_ar} عند البكسل ({ev["x"]}, {ev["y"]}).')
        # calls / returns of our own functions
        nxt = T[k + 1] if k + 1 < len(T) else None
        callee = None
        if nxt and nxt['depth'] > d and not (nxt['fn'] in cfg.get('callbacks', [])):
            callee = nxt['fn']; dyn.append(f'السطر ده بينده <b>{esc(callee)}()</b>: التنفيذ هينط لها، ولما تخلص يرجع هنا.')
            anim = anim or 'call'; live.append(['cpu', 'Stack', f'إطار جديد هيتعمل لـ {callee}()'])
        if nxt and nxt['depth'] < d:
            anim = anim or 'ret'; live.append(['cpu', 'Stack', f'{fn}() خلصت، وإطارها هيتمسح'])
        # stdout
        o = s.get('out') or ''
        o = '\n'.join(x for x in o.split('\n') if x and 'vblank' not in x and 'ATTENTION' not in x)
        if s.get('typed'):
            termAll.append('\u0001' + s['typed']); live.append(['prn', 'Terminal', 'اتكتب في الكيبورد: ' + s['typed']]); dyn.append('اتكتب في الكيبورد (في الـ Terminal): <code>' + esc(s['typed']) + '</code> وبعده Enter، و <code>cin</code> قراه.')
        if o:
            termAll += o.split('\n'); live.append(['prn', 'Terminal', 'اتطبع: ' + o.split('\n')[-1][:60]]); dyn.append('اتطبع في الـ Terminal: <code>' + esc(o) + '</code>')
        # values used on this line
        shown = []
        for ex_, val in args:
            if val is None or ex_ == val or ex_.strip('"') == str(val).strip('"'): continue
            if re.match(r'^&', ex_) or str(val).startswith('0x'):
                if ex_.startswith('&'): shown.append(f'<code>{esc(ex_)}</code> = عنوان {esc(ex_[1:])} في الرام')
                continue
            sv = short(val, 3000)
            nm = GLENUM.get(str(val))
            shown.append(f'<code>{esc(ex_)}</code> = <b dir="ltr">{esc(sv)}</b>')
        if shown: dyn.insert(0, 'القيم الحقيقية وقت التشغيل: ' + '، '.join(shown[:6]))
        if changes:
            ch = [c for c in changes if c[0] not in ('this',)][:5]
            if ch:
                dyn.append('بعد السطر ده في الرام: ' + '، '.join(f'<code>{esc(n)}</code> = <b dir="ltr">{esc(vv)}</b>' for n, vv in ch))
                for n, vv in ch:
                    cg = corner_groups(files, fname, s['line'], n, vv)
                    if cg: dyn.append(cg)
                live.append(['ram', 'الرام', '، '.join(f'{n} = {vv}' for n, vv in ch[:3])])
        # title
        ttl = GLTITLE.get(gfn) if gfn else None
        tx = text
        if ev: ttl = 'GLFW نده دالة الكيبورد' if ev['btn'] == 'key' else 'GLFW نده دالة الماوس'
        elif s.get('loopcheck'): ttl = 'خروج من الـ while' if s.get('closing') else f'أول الـ while · لفة {s["loopcheck"]}'
        elif not ttl:
            if tx == '{': ttl = f'دخلنا {fn}()'
            elif tx.startswith('}'): ttl = f'آخر {fn}()'
            elif tx.startswith('return'): ttl = 'return: رجّع النتيجة'
            elif tx.startswith(('if', 'else if')): ttl = 'شرط if'
            elif tx.startswith('else'): ttl = 'else'
            elif tx.startswith(('for', 'while')): ttl = 'لفة loop'
            elif callee: ttl = f'نداء {callee}()'
            elif 'std::cout' in tx: ttl = 'طباعة في الـ Terminal'
            elif re.match(r'^[\w:<>\*\s]+\s+\w+(\[\d*\])?\s*(=|;|\{|\()', tx):
                td = type_desc(tx, pl)
                if td: ttl = f'متغير جديد: {td[0]}'; dyn.insert(0, f'<b>النوع:</b> {td[1]}')
                else: ttl = 'متغير جديد في الرام'
            elif re.search(r'\w\s*(=|\+=|-=|\+\+)', tx): ttl = 'تغيير قيمة متغير'
            elif 'push_back' in tx: ttl = 'زوّد عنصر في الـ vector'
            else: ttl = 'سطر على الـ CPU'
        sv = None
        if 'getline' in text and len(files) > 1:
            gl_n = getattr(build, '_gl', 0); shf = next((x for x in files if x['name'].endswith('.shader')), None)
            if shf and gl_n < len(shf['lines']): sv = shf['off'] + gl_n + 1; dyn.append(f'getline قرا السطر رقم {gl_n + 1} من {shf["name"]}: <code>{esc(shf["lines"][gl_n])}</code>')
            elif shf: dyn.append('الملف خلص (EOF): getline رجّعت false فالـ while هتقف.')
            build._gl = gl_n + 1
        base = re.sub(r'\s*<span style="color:#2563eb">\(شرح[هـا]* كلمة كلمة فوق\)</span>', '', expl(fname, text))
        base = FULL.get(base, base)
        out.append({'v': v, 'f': files.index(next(x for x in files if x['name'] == fname)), 'ln': s['line'], 'fn': fn, 'd': d, 'u': unit,
                    'ti': ttl, 'ex': base, 'dy': dyn, 'lap': lapof[k], 'an': anim, 'lv': live[:4], 'fr': fr, 'bk': back, 'ft': front,
                    'mk': mask, 'ev': ev, 'sv': sv, 'cl': bool(s.get('closing')),
                    'st': [{'fn': q['fn'], 'v': [[n, x[0], x[1]] for n, x in list(q['vars'].items())[:12]]} for q in stack],
                    'gp': json.loads(json.dumps(gpu)), 'tm': len(termAll)})
    # cycle phases: distinct depth-1 lines of lap 1 in order
    ph = []
    l1 = [x for x in out if x['lap'] == 1 and x['d'] == 1]
    for x in l1:
        if x['v'] not in [p[0] for p in ph]: ph.append([x['v'], files[x['f']]['lines'][x['ln'] - 1].strip()])
    return {'id': pid, 'day': day, 'kind': kind, 'title': title, 'desc': desc, 'W': W, 'H': H, 'files': files, 'NV': NV,
            'regions': regions, 'shl': shl, 'frames': frames, 'steps': out, 'term': termAll, 'phases': ph,
            'laps': max([x['lap'] or 0 for x in out])}

if __name__ == '__main__':
    progs = [build(*p) for p in PROGS]
    # timing programs: under gdb every line is stepped, so the times are huge. Show the normal run (no bench) next to them, from the real output files.
    def _real(path):
        try: return [l for l in open(path).read().splitlines() if ' ns each' in l or 'heap / stack' in l]
        except OSError: return []
    REAL = {'d11_p2': (_real('/home/claude/day11/src/p2_speed_size.txt'), _real('/home/claude/day11/exp/s_million.out'))}
    for p in progs:
        if p['id'] not in REAL: continue
        n100, n1m = REAL[p['id']]
        for s_ in p['steps']:
            t = p['files'][s_['f']]['lines'][s_['ln'] - 1]
            k = 0 if 'stack Vector3' in t else 1 if 'new + delete' in t else 2 if 'heap / stack' in t else None
            if k is None or k >= len(n100): continue
            s_['dy'].append(f'⏱ <b>التشغيل العادي (من غير البنش):</b> <code>{n100[k]}</code>' + (f' · ولما خلّينا N = مليون: <code>{n1m[k]}</code>' if k < len(n1m) else '')
                            + '. الرقم اللي فوق كبير لأن البنش بيوقّف البرنامج عند كل سطر.')
            s_['lv'] = [['cpu', 'من غير البنش', n100[k][:60]]] + (s_.get('lv') or [])[:3]
    json.dump({'programs': progs}, open('/home/claude/bench2/progs.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    for p in progs:
        print(p['id'], len(p['steps']), 'steps', len(p['frames']), 'frames', 'laps', p['laps'], 'regions', [r[2] for r in p['regions']], 'phases', len(p['phases']))
    print('size', os.path.getsize('/home/claude/bench2/progs.json'))
