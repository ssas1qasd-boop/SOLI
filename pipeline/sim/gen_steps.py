# Builds the step-by-step trace of day3/src/s1_shader_file.cpp as JSON.
# Every value here comes from the real program: the shader file is parsed by the same rules as ParseShader,
# GL ids / pixel count / colour were read back from a real run (Mesa llvmpipe, OpenGL 4.5 core).
import json, copy, struct

CPP = open('/home/claude/day3/src/s1_shader_file.cpp').read().rstrip('\n').split('\n')
SH = open('/home/claude/day3/src/res/shaders/Basic.shader').read().rstrip('\n').split('\n')
TERM_REAL = open('/home/claude/day3/src/s1_shader_file.txt').read().rstrip('\n').split('\n')

S = {
    'stack': [],            # [{fn, vars:[[name,type,value]]}]
    'file': {'open': False, 'cursor': 0, 'eof': False},
    'ss': ['', ''],
    'win': False,
    'gpu': {'ctx': '', 'vsync': '', 'glad': False,
            'vao': None, 'buf': None, 'shaders': {}, 'prog': None},
    'back': 'none', 'front': 'none',
    'term': [],
}
steps = []

def snap(line, unit, title, text, anim=None, changed=(), sline=None):
    st = copy.deepcopy(S)
    steps.append({'line': line, 'sline': sline, 'unit': unit, 'title': title, 'text': text,
                  'anim': anim, 'changed': list(changed), 'state': st})

def frame(): return S['stack'][-1]
def setv(name, typ, val):
    for v in frame()['vars']:
        if v[0] == name: v[1], v[2] = typ, val; return
    frame()['vars'].append([name, typ, val])

def fbytes(fs):
    return [' '.join(f'{b:02X}' for b in struct.pack('<f', f)) for f in fs]

POS = [-0.5, -0.5, 0.0, 0.5, 0.5, -0.5]

# ------------------------------------------------------------------ main
S['stack'].append({'fn': 'main()', 'vars': []})
snap(87, 'CPU', 'البرنامج بدأ', 'نظام التشغيل حمّل البرنامج في الذاكرة، والـ CPU بدأ ينفذ <code>main</code>. اتعمل لها «إطار» (Stack frame) فاضي: ده المكان اللي هتتحط فيه متغيراتها.')
snap(89, 'CPU', 'تشغيل GLFW', '<code>glfwInit()</code>: مكتبة GLFW بتجهز نفسها وبتتكلم مع نظام التشغيل (الشاشة والكيبورد والماوس). رجّعت 1 (نجحت)، فـ <code>!1</code> = false ومش هنعمل <code>return -1</code>.')
snap(91, 'CPU', 'طلب نسخة 3', 'لسه مفيش شباك. ده مجرد «طلب» بنسجّله عند GLFW: عاوزين OpenGL رقمه الكبير 3.')
snap(92, 'CPU', 'طلب نسخة 3.3', 'والرقم الصغير 3 → يعني 3.3 على الأقل.')
snap(93, 'CPU', 'Core Profile', 'عاوزين النسخة الحديثة بس (Core): من غير الدوال القديمة. ده اللي بيخلي الـ VAO إجباري.')
S['win'] = True
setv('window', 'GLFWwindow*', 'عنوان الشباك')
snap(95, 'CPU', 'الشباك اتعمل', 'نظام التشغيل عمل شباك 640×480 اسمه «Shader File». المتغير <code>window</code> شايل عنوانه. لسه مفيش رسم: المحتوى فاضي.', changed=['win', 'stack'])
snap(96, 'CPU', 'اتأكد من الشباك', '<code>window</code> مش <code>nullptr</code>، فالشرط false ومش هندخل جوه الـ if.')
S['gpu']['ctx'] = 'OpenGL 4.5 Core'
snap(101, 'CPU→GPU', 'الـ Context', '<code>glfwMakeContextCurrent</code>: اتعمل «Context» = حالة كارت الشاشة الخاصة بالشباك ده. من هنا أي أمر <code>gl…</code> رايح للكارت ده. في التشغيل الحقيقي طلع <b>OpenGL 4.5 Core</b> (أكبر من 3.3 اللي طلبناها، فتمام).', changed=['ctx'])
S['gpu']['vsync'] = '1 (60 مرة في الثانية)'
snap(102, 'GPU', 'VSync', 'كل تبديل للشاشة يستنى تحديث الشاشة الجاي: الرسم هيبقى 60 مرة في الثانية بدل ما يجري بأقصى سرعة.', changed=['ctx'])
S['gpu']['glad'] = True
snap(104, 'CPU', 'GLAD جاب عناوين الدوال', 'دوال زي <code>glGenBuffers</code> مش جوه البرنامج؛ جوه درايفر كارت الشاشة. GLAD سأل الدرايفر عن عنوان كل دالة وحفظه. لو فشل كنا هنخرج بـ -1. نجح.', changed=['ctx'])

setv('positions', 'float[6]', ', '.join(f'{p:g}' for p in POS))
snap(107, 'CPU', '6 أرقام في الرام', 'مصفوفة 6 float في الـ Stack بتاع main = 6 × 4 = <b>24 بايت</b> في رام الكمبيوتر. كارت الشاشة لسه مايعرفش عنها حاجة. تحت: البايتات الحقيقية لكل رقم (float بيتخزن 4 بايت).', anim='bytes', changed=['stack'])
snap(108, 'CPU', 'الركن الأول', '(-0.5, -0.5) = تحت على الشمال. البايتات: <code>00 00 00 BF</code> و <code>00 00 00 BF</code>.', anim='bytes')
snap(109, 'CPU', 'الركن التاني', '(0, 0.5) = فوق في النص. <code>0.0</code> = <code>00 00 00 00</code> و <code>0.5</code> = <code>00 00 00 3F</code>.', anim='bytes')
snap(110, 'CPU', 'الركن التالت', '(0.5, -0.5) = تحت على اليمين.', anim='bytes')

setv('vao', 'unsigned int', '؟ (زبالة)')
snap(113, 'CPU', 'متغير للـ VAO', 'متغير فاضي في الرام. لسه ملوش قيمة مفهومة لحد ما الـ GPU يديله رقم.', changed=['stack'])
setv('vao', 'unsigned int', '1')
S['gpu']['vao'] = {'id': 1, 'bound': False, 'attr0': None}
snap(114, 'CPU→GPU', 'الـ GPU عمل VAO', 'الـ GPU عمل «VAO» (علبة بتحفظ إزاي نقرا النقط) وادّانا رقمه. الرقم الحقيقي اللي رجع: <b>1</b>. الـ CPU كتبه في <code>vao</code> (عشان بعتنا <code>&amp;vao</code> = عنوانه).', changed=['stack', 'vao'])
S['gpu']['vao']['bound'] = True
snap(115, 'GPU', 'VAO 1 بقى الشغال', 'أي إعداد للنقط من هنا لحد ما نغيّر هيتسجل جوه VAO رقم 1.', changed=['vao'])
setv('buffer', 'unsigned int', '؟ (زبالة)')
snap(117, 'CPU', 'متغير للـ Buffer', 'متغير تاني فاضي.', changed=['stack'])
setv('buffer', 'unsigned int', '1')
S['gpu']['buf'] = {'id': 1, 'bound': False, 'bytes': None}
snap(118, 'CPU→GPU', 'الـ GPU عمل Buffer', 'اتحجز «اسم» لـ Buffer في ذاكرة كارت الشاشة. الرقم الحقيقي: <b>1</b> (رقم الـ VAO ورقم الـ Buffer مستقلين، فالاتنين 1). لسه مفيش ولا بايت جواه.', changed=['stack', 'buf'])
S['gpu']['buf']['bound'] = True
snap(119, 'GPU', 'Buffer 1 على GL_ARRAY_BUFFER', 'ربطناه بخانة «بيانات النقط». أي أمر بيكلم <code>GL_ARRAY_BUFFER</code> هيروح لـ Buffer 1.', changed=['buf'])
S['gpu']['buf']['bytes'] = fbytes(POS)
snap(120, 'CPU→GPU', 'نسخ 24 بايت للكارت', '<code>6 * sizeof(float)</code> = 24. الـ 24 بايت اتنسخوا من الرام لذاكرة كارت الشاشة (VRAM). من دلوقتي الكارت عنده نسخته. <code>GL_STATIC_DRAW</code> = هنكتبهم مرة ونرسمهم كتير.', anim='upload', changed=['buf'])
S['gpu']['vao']['attr0'] = {'enabled': True, 'size': None}
snap(122, 'GPU', 'تشغيل الخانة 0', 'جوه VAO 1: الخانة رقم 0 بقت شغالة. لسه ما قلناش إزاي تتقري.', changed=['vao'])
S['gpu']['vao']['attr0'] = {'enabled': True, 'size': 2, 'type': 'GL_FLOAT', 'stride': 8, 'offset': 0, 'buffer': 1}
snap(123, 'GPU', 'إزاي تقرا النقطة', 'اتسجل جوه VAO 1: الخانة 0 = <b>2 float</b> لكل نقطة، المسافة بين نقطة والتانية <b>8 بايت</b>، وبتبدأ من بايت <b>0</b> في Buffer 1. يعني النقطة رقم i بايتاتها من 8×i لحد 8×i+7.', anim='stride', changed=['vao'])

# ------------------------------------------------------------------ ParseShader
S['stack'].append({'fn': 'ParseShader("res/shaders/Basic.shader")', 'vars': [['filepath', 'const std::string&', '"res/shaders/Basic.shader" (نفس النص اللي في main، من غير نسخة)']]})
snap(125, 'CPU', 'ندهنا ParseShader', 'الـ CPU ساب <code>main</code> مستنية، وعمل إطار جديد فوقها للدالة. <code>filepath</code> هو Reference: اسم تاني للنص، مش نسخة.', changed=['stack'])
S['file']['open'] = True
setv('stream', 'std::ifstream', 'مفتوح على Basic.shader (السطر 1)')
snap(23, 'CPU', 'فتح الملف', 'نظام التشغيل فتح الملف من الهارد. <code>stream</code> واقف على أول الملف.', changed=['stack', 'file'])
setv('line', 'std::string', '""')
snap(24, 'CPU', 'متغير للسطر', 'نص فاضي هيشيل كل سطر نقراه.', changed=['stack'])
setv('ss[0]', 'stringstream', '""'); setv('ss[1]', 'stringstream', '""')
snap(25, 'CPU', 'علبتين للنصوص', '<code>ss[0]</code> هتتجمع فيها شفرة الـ Vertex، و <code>ss[1]</code> شفرة الـ Fragment.', changed=['stack', 'ss'])
setv('type', 'ShaderType', 'NONE (-1)')
snap(26, 'CPU', 'لسه مش عارفين', '<code>type</code> = NONE (-1): لسه ما قريناش ولا علامة <code>#shader</code>.', changed=['stack'])

TY = {-1: 'NONE (-1)', 0: 'VERTEX (0)', 1: 'FRAGMENT (1)'}
typ = -1
for i, l in enumerate(SH, 1):
    S['file']['cursor'] = i
    setv('line', 'std::string', json.dumps(l, ensure_ascii=False))
    setv('stream', 'std::ifstream', f'مفتوح · اتقرا لحد السطر {i}')
    snap(28, 'CPU', f'getline: السطر {i}', f'<code>getline</code> قرا السطر {i} من الملف وحطه في <code>line</code> = <code>{json.dumps(l, ensure_ascii=False) if l else "&quot;&quot; (سطر فاضي)"}</code>. نجح، فالـ while هتكمل.', sline=i, changed=['file', 'stack'])
    has = '#shader' in l
    snap(30, 'CPU', 'فيه #shader؟', ('أيوه، السطر فيه <code>#shader</code>' if has else 'لأ، <code>find</code> رجعت <code>npos</code> (مش لاقية)') + ('.' if has else '، فهنروح للـ else.'), sline=i)
    if has:
        if 'vertex' in l:
            snap(32, 'CPU', 'فيه vertex؟', 'أيوه.', sline=i)
            typ = 0; setv('type', 'ShaderType', TY[typ])
            snap(33, 'CPU', 'type = VERTEX', 'من هنا كل سطر هيروح لـ <code>ss[0]</code>. والسطر ده نفسه (العلامة) مش هيتكتب في أي علبة.', sline=i, changed=['stack'])
        else:
            snap(32, 'CPU', 'فيه vertex؟', 'لأ.', sline=i)
            snap(34, 'CPU', 'فيه fragment؟', 'أيوه.', sline=i)
            typ = 1; setv('type', 'ShaderType', TY[typ])
            snap(35, 'CPU', 'type = FRAGMENT', 'من هنا كل سطر هيروح لـ <code>ss[1]</code>.', sline=i, changed=['stack'])
    else:
        S['ss'][typ] += l + '\n'
        setv(f'ss[{typ}]', 'stringstream', f'{S["ss"][typ].count(chr(10))} سطر')
        snap(39, 'CPU', f'أضيفه لـ ss[{typ}]', f'<code>(int)type</code> = {typ}، فالسطر اتضاف لـ <code>ss[{typ}]</code> ومعاه <code>\'\\n\'</code> (سطر جديد).', sline=i, changed=['ss'])
S['file']['eof'] = True
setv('stream', 'std::ifstream', 'وصل لآخر الملف (EOF)')
setv('line', 'std::string', json.dumps(SH[-1], ensure_ascii=False))
snap(28, 'CPU', 'getline فشلت: الملف خلص', f'مفيش سطر {len(SH) + 1}. <code>getline</code> رجّعت false، فالـ while وقفت.', sline=len(SH), changed=['file'])
snap(43, 'CPU', 'رجّع النصين', f'اتعمل <code>ShaderProgramSource</code> فيه النصين: Vertex = {S["ss"][0].count(chr(10))} سطور، Fragment = {S["ss"][1].count(chr(10))} سطور. وبعدين إطار الدالة اتمسح كله (stream اتقفل، و line و ss اتمسحوا).', changed=['ss'])
S['stack'].pop(); S['file']['open'] = False
setv('source', 'ShaderProgramSource', f'VertexSource ({len(S["ss"][0])} حرف)، FragmentSource ({len(S["ss"][1])} حرف)')
snap(125, 'CPU', 'رجعنا لـ main', 'النصين بقوا جوه <code>source</code> في main. لحد دلوقتي ده كله شغل CPU بس: كارت الشاشة ما شافش الشفرة لسه.', changed=['stack', 'file'])

# terminal output lines 126-129 (real output)
vi = TERM_REAL.index('FRAGMENT')
S['term'] += ['VERTEX']; snap(126, 'CPU', 'طباعة', 'كلمة VERTEX طلعت في الـ Terminal.', changed=['term'])
S['term'] += TERM_REAL[1:vi]; snap(127, 'CPU', 'طباعة شفرة الـ Vertex', 'النص كله اتطبع. بعده سطرين فاضيين: واحد من آخر <code>\'\\n\'</code> في النص، وواحد من <code>std::endl</code>.', changed=['term'])
S['term'] += ['FRAGMENT']; snap(128, 'CPU', 'طباعة', 'كلمة FRAGMENT.', changed=['term'])
S['term'] += TERM_REAL[vi + 1:]; snap(129, 'CPU', 'طباعة شفرة الـ Fragment', 'دي نفس النتيجة الحقيقية اللي ظهرت لما شغّلنا البرنامج.', changed=['term'])

# ------------------------------------------------------------------ CreateShader
S['stack'].append({'fn': 'CreateShader(vertexShader, fragmentShader)', 'vars': [['vertexShader', 'const std::string&', 'source.VertexSource'], ['fragmentShader', 'const std::string&', 'source.FragmentSource']]})
snap(131, 'CPU', 'ندهنا CreateShader', 'إطار جديد. الاتنين Reference للنصوص اللي في main.', changed=['stack'])
setv('program', 'unsigned int', '1'); S['gpu']['prog'] = {'id': 1, 'attached': [], 'linked': False, 'validated': False, 'inuse': False}
snap(72, 'CPU→GPU', 'برنامج فاضي على الكارت', 'الكارت عمل Program فاضي. الرقم الحقيقي: <b>1</b> (على كارت تاني ممكن يطلع رقم مختلف، زي 3 على NVIDIA. المهم إنه مش 0).', changed=['stack', 'prog'])

def compile_shader(kind, gltype, idn, src, ret_line):
    S['stack'].append({'fn': f'CompileShader({gltype}, source)', 'vars': [['type', 'unsigned int', gltype], ['source', 'const std::string&', f'{kind}Shader']]})
    snap(ret_line, 'CPU', f'ندهنا CompileShader للـ {kind}', 'إطار تالت فوق main و CreateShader.', changed=['stack'])
    setv('id', 'unsigned int', str(idn))
    S['gpu']['shaders'][idn] = {'type': kind, 'src': '', 'compiled': False, 'status': None, 'del': False}
    snap(48, 'CPU→GPU', f'Shader فاضي رقم {idn}', f'الكارت عمل Shader من نوع {kind} ورجّع رقمه الحقيقي: <b>{idn}</b>.', changed=['stack', 'shaders'])
    setv('src', 'const char*', f'عنوان أول حرف في النص ({len(src)} حرف)')
    snap(49, 'CPU', 'Pointer للنص', '<code>c_str()</code> بيدينا عنوان أول حرف. OpenGL مكتوبة بـ C ومش فاهمة <code>std::string</code>.', changed=['stack'])
    S['gpu']['shaders'][idn]['src'] = src
    snap(50, 'CPU→GPU', 'النص اتبعت للكارت', f'الدرايفر نسخ الـ {len(src)} حرف لـ Shader {idn}. لسه نص عادي، مش برنامج.', anim='src', changed=['shaders'])
    S['gpu']['shaders'][idn]['compiled'] = True
    snap(51, 'GPU', 'ترجمة GLSL', 'الدرايفر ترجم الـ GLSL لأوامر يفهمها الكارت (زي ما g++ بيترجم C++). ده بيحصل وإنت شغال، كل مرة تشغّل البرنامج.', anim='compile', changed=['shaders'])
    setv('result', 'int', '؟ (زبالة)')
    snap(53, 'CPU', 'متغير للنتيجة', '', changed=['stack'])
    setv('result', 'int', '1 (GL_TRUE)'); S['gpu']['shaders'][idn]['status'] = 1
    snap(54, 'GPU→CPU', 'الترجمة نجحت؟', 'سألنا الكارت. الرد الحقيقي: <b>1</b> = GL_TRUE = اتترجم من غير أخطاء.', changed=['stack', 'shaders'])
    snap(55, 'CPU', 'فشلت؟', '<code>1 == GL_FALSE</code>؟ لأ، فهننط على كل الـ if ومش هنطبع رسالة خطأ.')
    snap(67, 'CPU', f'رجّع {idn}', 'إطار CompileShader اتمسح.')
    S['stack'].pop()

compile_shader('Vertex', 'GL_VERTEX_SHADER', 2, S['ss'][0], 73)
setv('vs', 'unsigned int', '2')
snap(73, 'CPU', 'vs = 2', 'رجعنا لـ CreateShader ومعانا رقم الـ Vertex Shader.', changed=['stack'])
compile_shader('Fragment', 'GL_FRAGMENT_SHADER', 3, S['ss'][1], 74)
setv('fs', 'unsigned int', '3')
snap(74, 'CPU', 'fs = 3', 'ومعانا رقم الـ Fragment Shader.', changed=['stack'])
S['gpu']['prog']['attached'].append(2)
snap(76, 'GPU', 'ركّب الـ Vertex', 'Shader 2 اتركب في Program 1.', changed=['prog'])
S['gpu']['prog']['attached'].append(3)
snap(77, 'GPU', 'ركّب الـ Fragment', 'Shader 3 اتركب كمان.', changed=['prog'])
S['gpu']['prog']['linked'] = True
snap(78, 'GPU', 'Link', 'الكارت وصّل الاتنين ببعض في برنامج واحد: الـ Vertex بيطلع <code>gl_Position</code> للمرحلة اللي بعده، والـ Fragment بيطلع <code>color</code> على الخانة 0 = الشاشة. الحالة الحقيقية: LINK_STATUS = <b>1</b>.', changed=['prog'])
S['gpu']['prog']['validated'] = True
snap(79, 'GPU', 'Validate', 'اتأكد إن البرنامج ينفع يشتغل مع الحالة الحالية.', changed=['prog'])
S['gpu']['shaders'][2]['del'] = True
snap(81, 'GPU', 'امسح Shader 2؟', 'مش هيتمسح دلوقتي: هو متركب في Program 1، فالكارت بيعلّم عليه «يتمسح أول ما يتفك». البرنامج المترجم شغال عادي.', changed=['shaders'])
S['gpu']['shaders'][3]['del'] = True
snap(82, 'GPU', 'امسح Shader 3؟', 'نفس الحكاية: متعلّم عليه للمسح.', changed=['shaders'])
snap(84, 'CPU', 'رجّع 1', 'إطار CreateShader اتمسح (program و vs و fs).')
S['stack'].pop()
setv('shader', 'unsigned int', '1')
snap(131, 'CPU', 'shader = 1', '', changed=['stack'])
S['gpu']['prog']['inuse'] = True
snap(132, 'GPU', 'استخدم Program 1', 'أي رسم من دلوقتي هيعدّي على الـ Vertex والـ Fragment اللي في Program 1.', changed=['prog'])

# ------------------------------------------------------------------ render loop
def frame_iter(n):
    snap(134, 'CPU', f'اللفة {n}: الشباك اتقفل؟', 'لأ، فندخل جوه الـ while.')
    S['back'] = 'black'
    snap(136, 'GPU', 'امسح الـ Back buffer', 'فيه صورتين: <b>Front</b> (اللي إنت شايفها) و <b>Back</b> (اللي بنرسم فيها في الخفا). <code>glClear</code> ملا الـ Back بالأسود (0,0,0). الشاشة لسه زي ما هي.', changed=['back'])
    snap(137, 'GPU', 'Vertex Shader × 3', 'الكارت قرا 3 نقط من Buffer 1 بالطريقة اللي في VAO 1، وشغّل الـ Vertex Shader <b>3 مرات</b> (مرة لكل ركن). <code>in vec4 position</code> = (x, y, 0, 1): z و w اتملوا لوحدهم لأننا بعتنا رقمين بس. وبعدين حوّل كل ركن لبكسل في الشباك 640×480.', anim='vs')
    snap(137, 'GPU', 'Rasterizer: مين جوه المثلث؟', 'الكارت شاف كل بكسل في الشباك: مركزه جوه المثلث ولا لأ؟ الحسبة طلعت <b>38,400 بكسل</b> = نص (320 × 240). والرقم ده نفس اللي عدّيناه فعلاً من الصورة الحقيقية.', anim='raster')
    S['back'] = 'tri'
    snap(137, 'GPU', 'Fragment Shader × 38,400', 'الـ Fragment Shader اشتغل <b>38,400 مرة</b> (مرة لكل بكسل)، وفي الآلاف بالتوازي. كل مرة بيطلع <code>vec4(0.2, 0.3, 0.8, 1.0)</code> ← بايتات (51, 76, 204, 255). قريناه من الشاشة الحقيقية: نص الشباك = 51, 76, 204, 255 بالظبط.', anim='fs', changed=['back'])
    snap(138, 'GPU', 'استنى تحديث الشاشة (VSync)', 'قبل ما <code>glfwSwapBuffers</code> تبدّل، بتستنى الشاشة تخلص عرض الصورة الحالية وتبدأ واحدة جديدة (60 مرة في الثانية). ده بسبب <code>glfwSwapInterval(1)</code> في سطر 102. لو بدّلت في نص العرض كنت هتشوف نص صورة قديمة ونص جديدة.')
    S['front'], S['back'] = S['back'], S['front']
    snap(138, 'GPU', 'بدّل الصورتين', 'الـ Back بقى Front: المثلث ظهر على الشاشة. والـ Front القديم بقى Back عشان نرسم فيه اللفة الجاية. (VSync: التبديل بيستنى تحديث الشاشة.)', anim='swap', changed=['front', 'back'])
    snap(139, 'CPU', 'الأحداث', 'GLFW شاف لو فيه ماوس أو كيبورد أو حد داس X. مفيش، فنكمل.')

frame_iter(1)
frame_iter(2)
frame_iter(3)
frame_iter(4)
snap(134, 'CPU', 'وهكذا… 60 مرة في الثانية', 'نفس الـ 6 خطوات بتتكرر لحد ما تقفل الشباك. الـ CPU كل لفة بيبعت 4 أوامر بس؛ الشغل التقيل كله (3 + 38,400 تشغيلة) على الـ GPU.')
snap(134, 'CPU', 'دوست X', 'لما تقفل الشباك <code>glfwWindowShouldClose</code> بترجع true، فالـ while بتخلص.')
S['gpu']['prog'] = None; S['gpu']['shaders'] = {}
snap(142, 'GPU', 'امسح Program 1', 'Program 1 اتمسح، ومعاه Shaders 2 و 3 اللي كانوا متعلّم عليهم.', changed=['prog', 'shaders'])
S['win'] = False; S['gpu'] = {'ctx': '', 'vsync': '', 'glad': False, 'vao': None, 'buf': None, 'shaders': {}, 'prog': None}; S['front'] = S['back'] = 'none'
snap(143, 'CPU', 'قفل GLFW', 'الشباك والـ Context وكل اللي على الكارت (VAO 1 و Buffer 1) اترجعوا.', changed=['win', 'ctx'])
S['stack'] = []
snap(144, 'CPU', 'return 0', 'البرنامج خلص بنجاح، ونظام التشغيل رجّع الرام.', changed=['stack'])

json.dump({'cpp': CPP, 'shader': SH, 'steps': steps}, open('/home/claude/sim/steps.json', 'w'), ensure_ascii=False)
print(len(steps), 'steps')
