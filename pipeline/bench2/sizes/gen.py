import json, html
A = json.load(open('/home/claude/bench2/exe/all.json'))
E = lambda t: html.escape(str(t))
f = lambda n: f'{n:,}'
def L(t): return f'<bdi dir="ltr">{t}</bdi>'
DAYS = [(1, 'الأحد 25-10', ['d1_u1', 'd1_u2', 'd1_cam']), (2, 'الإتنين 26-10', ['d2_va1', 'd2_va2']), (3, 'التلات 27-10', ['d3_s1', 'd3_l1', 'd3_l2']), (4, 'الأربعاء 28-10', ['d4_e1', 'd4_e2', 'd4_v1', 'd4_v2']), (5, 'الخميس 29-10', ['d5_r1', 'd5_r2', 'd5_c2']), (6, 'الجمعة 30-10', ['d6_r1', 'd6_r2', 'd6_c1']), (7, 'السبت 31-10', ['d7_r1', 'd7_r2']), (8, 'الأحد 1-11 · الأسبوع 3', ['d8_t1', 'd8_t2', 'd8_c2']), (9, 'الإتنين 2-11 · الأسبوع 3', ['d9_t1', 'd9_t2', 'd9_c2'])]
SH = {'d1_u1': (100, 113), 'd1_u2': (100, 113), 'd1_cam': (214, 102), 'd2_va1': (118, 87), 'd2_va2': (203, 106), 'd3_s1': (104, 110)}
for k in ['d3_l1', 'd3_l2', 'd4_e1', 'd4_e2', 'd4_v1', 'd4_v2', 'd5_c2']: SH[k] = (118, 92)
SH['d5_r1'] = (103, 111); SH['d5_r2'] = (193, 161)
SH['d9_t1'] = (181, 137); SH['d9_t2'] = (228, 137); SH['d9_c2'] = (184, 103); SH['d8_t1'] = (191, 167); SH['d8_t2'] = (279, 167); SH['d8_c2'] = (103, 117); SH['d7_r1'] = (103, 117); SH['d7_r2'] = (156, 117); SH['d6_r1'] = (103, 117); SH['d6_r2'] = (154, 319); SH['d6_c1'] = (118, 92)
WH = {k: (640, 480) for k in A}; WH['d1_cam'] = (800, 800)
CODE = {'d9_t1': (169, 5267), 'd9_t2': (170, 5665), 'd9_c2': (160, 5119), 'd8_t1': (203, 5809), 'd8_t2': (210, 6615), 'd8_c2': (200, 6080), 'd7_r1': (168, 4523), 'd7_r2': (186, 5856), 'd1_u1': (119, 3215), 'd1_u2': (125, 3277), 'd1_cam': (221, 6748), 'd2_va1': (100, 2621), 'd2_va2': (107, 2920), 'd3_s1': (145, 4002), 'd3_l1': (108, 2817), 'd3_l2': (128, 3519), 'd4_e1': (106, 2804), 'd4_e2': (114, 3049), 'd4_v1': (127, 3585), 'd4_v2': (141, 3899), 'd5_r1': (122, 3217), 'd5_r2': (125, 3392), 'd5_c2': (173, 4759), 'd6_r1': (156, 4083), 'd6_r2': (155, 4265), 'd6_c1': (227, 5722)}
POS = '2 (x, y)'
P = {
 'd1_u1': dict(name='Uniform: لون ثابت', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('vbo', 1, 4, 'أركان المستطيل', 2, 'x, y', 32)], ebo=('ibo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('u_Color', 4, 16, '')),
 'd1_u2': dict(name='Uniform: لون بيتغير', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('vbo', 1, 4, 'أركان المستطيل', 2, 'x, y', 32)], ebo=('ibo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('u_Color', 4, 16, 'بيتبعت كل لفة')),
 'd1_cam': dict(name='الكاميرا (3 ملفات)', vao=[('VAO', 1, 'خانة 0: مكان، خانة 1: لون')], vbo=[('VBO', 1, 16, 'لون لكل وش: قاعدة 4 + جوانب 4 × 3', 6, 'x, y, z, r, g, b', 384)], ebo=('EBO', 2, 18, '6 مثلثات × 3: مثلثين للقاعدة + مثلث لكل جنب', 72), uni=('camMatrix', 16, 64, 'مصفوفة 4×4، بتتبعت كل لفة')),
 'd2_va1': dict(name='مكان بس', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 3, 'مثلث', 2, 'x, y', 24)], ebo=None, uni=None),
 'd2_va2': dict(name='مكان + لون', vao=[('vao', 1, 'خانة 0: مكان، خانة 1: لون')], vbo=[('buffer', 1, 3, 'مثلث', 5, 'x, y, r, g, b', 60)], ebo=None, uni=None),
 'd3_s1': dict(name='Shader من ملف (بنش التلات)', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 3, 'مثلث', 2, 'x, y', 24)], ebo=None, uni=None),
 'd3_l1': dict(name='خط بنقطتين', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 2, 'طرفين الخط', 2, 'x, y', 16)], ebo=None, uni=('u_Color', 4, 16, '')),
 'd3_l2': dict(name='خطوط بالماوس', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 5, 'ضغطات، في آخر التشغيل', 2, 'x, y', 40)], ebo=None, uni=('u_Color', 4, 16, '')),
 'd4_e1': dict(name='مستطيل بـ 6 أركان', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 6, 'مثلثين × 3', 2, 'x, y', 48)], ebo=None, uni=('u_Color', 4, 16, '')),
 'd4_e2': dict(name='مستطيل بـ Index Buffer', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 4, 'أركان المستطيل', 2, 'x, y', 32)], ebo=('ibo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('u_Color', 4, 16, '')),
 'd4_v1': dict(name='بيت وشمس', vao=[('houseVao', 1, 'البيت · خانة 0: مكان'), ('sunVao', 2, 'الشمس · خانة 0: مكان')], vbo=[('houseBuffer', 1, 12, 'البيت: 6 خطوط × 2', 2, 'x, y', 96), ('sunBuffer', 2, 4, 'الشمس: خطين × 2', 2, 'x, y', 32)], ebo=None, uni=('u_Color', 4, 16, '')),
 'd4_v2': dict(name='Polyline بالماوس', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 8, 'ضغطات شمال، في آخر التشغيل', 2, 'x, y', 64)], ebo=None, uni=('u_Color', 4, 16, '')),
 'd5_r1': dict(name='مثلث أحمر (The Cherno)', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 3, 'مثلث', 2, 'x, y', 24)], ebo=None, uni=None),
 'd5_r2': dict(name='تعديل الـ Shader', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 3, 'مثلث (التكبير جوه الـ Shader)', 2, 'x, y', 24)], ebo=None, uni=None),
 'd6_r1': dict(name='ألوان متحركة (The Cherno)', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 4, 'أركان المستطيل', 2, 'x, y', 32)], ebo=('ibo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('u_Color', 4, 16, 'بيتبعت كل لفة')),
 'd6_r2': dict(name='ألوان بالوقت', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 4, 'أركان المستطيل', 2, 'x, y', 32)], ebo=('ibo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('u_Time', 1, 4, 'رقم واحد، بيتبعت كل لفة')),
 'd6_c1': dict(name='Refactoring: مسح آخر خط', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 5, 'نقط فاضلة بعد المسح، في آخر التشغيل', 2, 'x, y', 40)], ebo=None, uni=('u_Color', 4, 16, '')),
 'd7_r1': dict(name='Vertex Array (The Cherno)', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 4, 'أركان المستطيل', 2, 'x, y', 32)], ebo=('ibo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('u_Color', 4, 16, 'بيتبعت كل لفة')),
 'd7_r2': dict(name='الطريقتين جنب بعض', vao=[('squareVao', 1, 'المربع · خانة 0: مكان'), ('triangleVao', 2, 'المثلث · خانة 0: مكان'), ('globalVao', 3, 'الطريقة 1 · خانة 0 بتتعاد')], vbo=[('squareBuffer', 1, 4, 'أركان المربع', 2, 'x, y', 32), ('triangleBuffer', 3, 3, 'أركان المثلث', 3, 'x, y, z', 36)], ebo=('squareIbo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('u_Color + u_Offset', 6, 24, '4 + 2 أرقام')),
 'd8_t1': dict(name='Texture: صورة على مربع', vao=[('vao', 1, 'خانة 0: مكان، خانة 1: إحداثيات الصورة')], vbo=[('buffer', 1, 4, 'أركان المربع', 4, 'x, y, u, v', 64)], ebo=('ibo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('u_Texture', 1, 4, 'رقم الخانة (int)'), tex=[('texture.id', 1, 128, 128, 'logo.png', 65536)]),
 'd8_t2': dict(name='إعدادات الـ Texture', vao=[('vao', 1, 'خانة 0: مكان، خانة 1: إحداثيات الصورة')], vbo=[('buffer', 1, 4, 'أركان المربع', 4, 'x, y, u, v', 64)], ebo=('ibo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('u_Texture + u_Offset + u_Repeat', 4, 16, '1 + 2 + 1 أرقام'), tex=[('sharp', 1, 4, 4, 'شطرنج 4 × 4', 64), ('smooth', 2, 4, 4, 'نفس البكسلات', 64)]),
 'd8_c2': dict(name='B-Rep Wireframe', vao=[('allVao', 1, 'كل الأضلاع · خانة 0: مكان'), ('frontVao', 2, 'الوش القدام · نفس الصندوق')], vbo=[('buffer', 1, 8, 'أركان المكعب بعد الإسقاط', 2, 'x, y', 64)], ebo=('allIbo + frontIbo', '2 + 3', 32, '12 خط × 2 + 4 خطوط × 2', 128), uni=('u_Color', 4, 16, '')),
 'd9_t1': dict(name='قطة Pixel Art (Victor Gordan)', vao=[('vao', 1, 'خانة 0: مكان، خانة 1: إحداثيات الصورة')], vbo=[('vbo', 1, 4, 'أركان المستطيل', 5, 'x, y, z, u, v', 80)], ebo=('ebo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('tex0', 1, 4, 'رقم الخانة (int)'), tex=[('texture', 1, 16, 16, 'pixel_cat.png: المستوى 0', 1024), ('texture', 1, 8, 8, 'Mipmap: المستوى 1', 256), ('texture', 1, 4, 4, 'Mipmap: المستوى 2', 64), ('texture', 1, 2, 2, 'Mipmap: المستوى 3', 16), ('texture', 1, 1, 1, 'Mipmap: المستوى 4', 4)]),
 'd9_t2': dict(name='الأنواع الأربعة للتكرار', vao=[('vao', 1, 'خانة 0: مكان، خانة 1: إحداثيات الصورة')], vbo=[('vbo', 1, 4, 'أركان المربع', 4, 'x, y, u, v', 64)], ebo=('ebo', 2, 6, 'مثلثين × 3 أركان', 24), uni=('tex0 + offset', 3, 12, '1 + 2 أرقام'), tex=[('textures[0]', 1, 128, 128, 'logo.png · REPEAT', 65536), ('textures[1]', 2, 128, 128, 'logo.png · MIRRORED_REPEAT', 65536), ('textures[2]', 3, 128, 128, 'logo.png · CLAMP_TO_EDGE', 65536), ('textures[3]', 4, 128, 128, 'logo.png · CLAMP_TO_BORDER', 65536)]),
 'd9_c2': dict(name='Barycentric (مثلث ملون)', vao=[('vao', 1, 'خانة 0: مكان، خانة 1: لون')], vbo=[('vbo', 1, 3, 'أركان المثلث (struct Corner)', 5, 'x, y, r, g, b', 60)], ebo=None, uni=None),
 'd5_c2': dict(name='مسح آخر خط', vao=[('vao', 1, 'خانة 0: مكان')], vbo=[('buffer', 1, 5, 'نقط فاضلة بعد المسح، في آخر التشغيل', 2, 'x, y', 40)], ebo=None, uni=('u_Color', 4, 16, '')),
}
EXK = ['كودك: أوامر (الدوال)', 'كودك: ثوابت (نصوص وأرقام)', 'كودك: بيانات', 'كودك: جداول الاستثناءات', 'GLAD', 'تشغيل C/C++ (crt)', 'ربط المكتبات (GLFW والدرايفر)', 'هيكل الملف', 'حشو (محاذاة)', 'فراغ بين الصفحات (4 كيلو)']
def fname(n):
    if n.startswith('std::basic_ostream'): return 'std::endl'
    if n.startswith('std::ctype'): return 'do_widen'
    if '_M_realloc_insert' in n: return 'vector&lt;' + ('Polyline' if 'Polyline' in n else 'float') + '&gt;: توسيع'
    if n.startswith('_GLOBAL__sub_I'): return 'تجهيز المتغيرات العامة'
    if '~vector' in n: return 'vector: مسح'
    if 'glm::rotate' in n: return 'glm::rotate'
    if 'glm::operator*' in n: return 'glm: ضرب مصفوفات'
    if n == '.data.rel.ro': return 'جدول عناوين'
    return E(n.split('(')[0])
# ---- columns: (key, group, header, source-note)
COLS = [
 ('prog', '', 'البرنامج', ''),
 ('vao_n', 'vao', 'الاسم · الرقم', ''), ('vao_a', 'vao', 'الخانات اللي بيوصفها', ''),
 ('vbo_n', 'vbo', 'الاسم · الرقم', ''), ('vbo_c', 'vbo', 'الأركان', 'جت منين'), ('vbo_p', 'vbo', 'أرقام في كل ركن', ''), ('vbo_b', 'vbo', 'بايت لكل رقم', ''), ('vbo_calc', 'vbo', 'الحساب', ''), ('vbo', 'vbo', 'بايتات الـ VBO', ''),
 ('ebo_n', 'ebo', 'الاسم · الرقم', ''), ('ebo_c', 'ebo', 'الأرقام', 'جت منين'), ('ebo_b', 'ebo', 'بايت لكل رقم', ''), ('ebo_calc', 'ebo', 'الحساب', ''), ('ebo', 'ebo', 'بايتات الـ EBO', ''),
 ('uni_n', 'uni', 'الاسم', ''), ('uni_calc', 'uni', 'الحساب', ''), ('uni', 'uni', 'البايتات', ''),
 ('tex_n', 'tex', 'الاسم · الرقم', ''), ('tex_calc', 'tex', 'الحساب', ''), ('tex', 'tex', 'البايتات', ''),
 ('sh_t', 'sh', 'النص (Vertex + Fragment)', ''), ('sh_p', 'sh', 'Program المترجم', 'من الدرايفر'),
 ('px', 'fb', 'البكسلات', 'العرض × الطول'), ('fb_calc', 'fb', 'الحساب لكل لوحة', ''), ('fb1', 'fb', 'Back', ''), ('fb2', 'fb', 'Front', ''), ('fb3', 'fb', 'Depth + Stencil', ''),
 ('g_fb1', 'gpu', 'Back', '← من لوحات الرسم'), ('g_fb2', 'gpu', 'Front', '← من لوحات الرسم'), ('g_fb3', 'gpu', 'Depth + Stencil', '← من لوحات الرسم'),
 ('g_vbo', 'gpu', 'VBO', '← من عمود الـ VBO'), ('g_ebo', 'gpu', 'EBO', '← من عمود الـ EBO'), ('g_vao', 'gpu', 'VAO', 'مش بيتقاس = 0'), ('g_uni', 'gpu', 'Uniforms', '← من عمود الـ Uniforms'), ('g_tex', 'gpu', 'Textures', '← من عمود الـ Textures'), ('g_prog', 'gpu', 'Program المترجم', '← من عمود الـ Shaders'),
 ('gpu_calc', 'gpu', 'الحساب', 'جمع الأعمدة اللي قبله'), ('gpu', 'gpu', 'على الكارت (الناتج)', ''),
 ('x0', 'exe', 'أوامر كودك', 'الدوال'), ('x_fn', 'exe', 'أوامر كودك بالتفصيل', 'كل دالة لوحدها'), ('x1', 'exe', 'ثوابت كودك', 'نصوص وأرقام'), ('x2', 'exe', 'بيانات كودك', 'متغيرات برا الدوال'), ('x3', 'exe', 'جداول استثناءات كودك', ''),
 ('x4', 'exe', 'GLAD', ''), ('x5', 'exe', 'تشغيل C/C++', 'قبل وبعد main'), ('x6', 'exe', 'ربط المكتبات', 'GLFW والدرايفر'), ('x7', 'exe', 'هيكل الملف', 'الرؤوس والفهارس'), ('x8', 'exe', 'حشو بين الأجزاء', ''), ('x9', 'exe', 'فراغ الصفحات', 'صفحات 4 كيلو'),
 ('exe_calc', 'exe', 'الحساب', 'جمع الأعمدة اللي قبله'), ('exe', 'exe', 'ملف الـ exe (الناتج)', ''),
 ('code', 'code', 'سطور · بايت', ''),
]
GNAME = {'': '', 'vao': 'الـ VAO', 'vbo': 'الـ VBO (الأركان)', 'ebo': 'الـ EBO (أرقام الأركان)', 'uni': 'الـ Uniforms', 'tex': 'الـ Textures (الصور)', 'sh': 'الـ Shaders', 'fb': 'لوحات الرسم', 'gpu': 'كل اللي على الكارت (كل جزء في عمود)', 'exe': 'ملف البرنامج exe (كل جزء في عمود)', 'code': 'الكود'}
SUM = ['vbo', 'ebo', 'uni', 'tex', 'g_tex', 'sh_p', 'fb1', 'fb2', 'fb3', 'g_fb1', 'g_fb2', 'g_fb3', 'g_vbo', 'g_ebo', 'g_vao', 'g_uni', 'g_prog', 'gpu', 'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'exe']
num = lambda v, big=False: f'<span class="n{" big" if big else ""}">{f(v) if v else "0"}</span>'
def row(k):
    p = P[k]; a = A[k]; W, H = WH[k]; px = W * H; c = {}; v = {}
    c['prog'] = f'<th scope="row">{E(p["name"])}</th>'
    c['vao_n'] = '<br>'.join(f'<code>{x[0]}</code> · {x[1]}' for x in p['vao']); c['vao_a'] = '<br>'.join(E(x[2]) for x in p['vao'])
    vb = p['vbo']
    c['vbo_n'] = '<br>'.join(f'<code>{x[0]}</code> · {x[1]}' for x in vb)
    c['vbo_c'] = '<br>'.join(f'{x[2]} <span class="why">({E(x[3])})</span>' for x in vb)
    c['vbo_p'] = '<br>'.join(L(f'{x[4]} <span class="why">({x[5]})</span>') for x in vb)
    c['vbo_b'] = '<br>'.join(L('4 <span class="why">(float)</span>') for x in vb)
    c['vbo_calc'] = '<br>'.join(f'{x[2]} ركن × {x[4]} رقم × 4 بايت = <b>{x[6]}</b>' for x in vb)
    v['vbo'] = sum(x[6] for x in vb); c['vbo'] = num(v['vbo']) + (f'<small class="f">{L(" + ".join(str(x[6]) for x in vb))}</small>' if len(vb) > 1 else '')
    e = p['ebo']
    if e: c.update(ebo_n=f'<code>{e[0]}</code> · {e[1]}', ebo_c=f'{e[2]} <span class="why">({E(e[3])})</span>', ebo_b=L('4 <span class="why">(unsigned int)</span>'), ebo_calc=f'{e[2]} رقم × 4 بايت = <b>{e[4]}</b>'); v['ebo'] = e[4]
    else: c.update(ebo_n='—', ebo_c='—', ebo_b='—', ebo_calc='—'); v['ebo'] = 0
    c['ebo'] = num(v['ebo'])
    u = p['uni']
    if u: c.update(uni_n=f'<code>{u[0]}</code>' + (f'<small> · {E(u[3])}</small>' if u[3] else ''), uni_calc=f'{u[1]} رقم × 4 بايت = <b>{u[2]}</b>'); v['uni'] = u[2]
    else: c.update(uni_n='—', uni_calc='—'); v['uni'] = 0
    c['uni'] = num(v['uni'])
    tx = p.get('tex') or []
    if tx:
        c['tex_n'] = '<br>'.join(f'<code>{x[0]}</code> · {x[1]}' for x in tx)
        c['tex_calc'] = '<br>'.join(f'{x[2]} × {x[3]} بكسل × 4 بايت = <b>{f(x[5])}</b> <span class="why">({E(x[4])})</span>' for x in tx)
    else: c['tex_n'] = c['tex_calc'] = '—'
    v['tex'] = sum(x[5] for x in tx); c['tex'] = num(v['tex'])
    vs, fs = SH[k]; c['sh_t'] = f'Vertex {vs} + Fragment {fs} = <b>{vs + fs}</b> بايت'; v['sh_t'] = vs + fs
    v['sh_p'] = a['gpu']['prog']; c['sh_p'] = num(v['sh_p'])
    c['px'] = f'{L(f"{W} × {H}")} = <b>{f(px)}</b>'; c['fb_calc'] = f'{f(px)} بكسل × 4 بايت = <b>{f(px * 4)}</b>'
    for j in (1, 2, 3): v[f'fb{j}'] = v[f'g_fb{j}'] = px * 4; c[f'fb{j}'] = c[f'g_fb{j}'] = num(px * 4)
    v['g_vbo'], v['g_ebo'], v['g_vao'], v['g_uni'], v['g_tex'], v['g_prog'] = v['vbo'], v['ebo'], 0, v['uni'], v['tex'], v['sh_p']
    for kk in ('g_vbo', 'g_ebo', 'g_vao', 'g_uni', 'g_tex', 'g_prog'): c[kk] = num(v[kk])
    parts = [v[x] for x in ('g_fb1', 'g_fb2', 'g_fb3', 'g_vbo', 'g_ebo', 'g_vao', 'g_uni', 'g_tex', 'g_prog')]
    v['gpu'] = a['gpu_total']; assert sum(parts) == v['gpu']
    c['gpu_calc'] = f'<span class="calc">{L(" + ".join(f(x) for x in parts))}</span>'; c['gpu'] = num(v['gpu'], True)
    ex = [a['exe'].get(x, 0) for x in EXK]; assert sum(ex) == a['size']
    for j, x in enumerate(ex): v[f'x{j}'] = x; c[f'x{j}'] = num(x)
    c['x_fn'] = '<br>'.join(f'{fname(n)} = <b>{vv}</b>' for n, vv in a['fns']) + f'<small class="f">المجموع = {ex[0]}</small>'
    c['exe_calc'] = f'<span class="calc">{L(" + ".join(f(x) for x in ex))}</span>'; v['exe'] = a['size']; c['exe'] = num(v['exe'], True)
    lc, bc = CODE[k]; c['code'] = f'{lc} · {f(bc)}' + (' <small>(+ Basic.shader)</small>' if k == 'd3_s1' else ''); v['lines'], v['bytes'] = lc, bc
    return c, v
ADD = {'gpu': ['g_fb1', 'g_fb2', 'g_fb3', 'g_vbo', 'g_ebo', 'g_vao', 'g_uni', 'g_tex', 'g_prog'], 'exe': ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9']}
ROLE = {}
for res, keys in ADD.items():
    for n, k in enumerate(keys, 1): ROLE[k] = ('add', res, n)
    ROLE[res] = ('res', res, len(keys))
def cls(k, g):
    r = ROLE.get(k)
    return g + (' wide' if k in ('gpu_calc', 'exe_calc') else '') + (f' add add-{r[1]}' if r and r[0] == 'add' else f' res res-{r[1]}' if r else '')
def render(c):
    return '<tr>' + ''.join(c[k] if k == 'prog' else f'<td class="{cls(k, g)}">{c[k]}</td>' for k, g, h, n in COLS) + '</tr>'
def total_row(label, vals, cls):
    c = {'prog': f'<th scope="row">{label}</th>'}
    for k, g, h, n in COLS[1:]:
        if k in SUM:
            xs = [x[k] for x in vals]; s = sum(xs); big = k in ('gpu', 'exe')
            c[k] = num(s, big) + (f'<small class="f">{L(" + ".join(f(x) for x in xs))}</small>' if len(xs) > 1 else '') + (f'<small class="f">≈ {s / 1048576:.2f} ميجا</small>' if big else '')
        elif k == 'sh_t': c[k] = f'<b>{f(sum(x["sh_t"] for x in vals))}</b> بايت نص'
        elif k == 'code': c[k] = f'{f(sum(x["lines"] for x in vals))} · {f(sum(x["bytes"] for x in vals))}'
        elif k == 'gpu_calc': c[k] = f'<span class="calc">{L(" + ".join(f(sum(x[q] for x in vals)) for q in ("g_fb1", "g_fb2", "g_fb3", "g_vbo", "g_ebo", "g_vao", "g_uni", "g_tex", "g_prog")))}</span>'
        elif k == 'exe_calc': c[k] = f'<span class="calc">{L(" + ".join(f(sum(x[f"x{j}"] for x in vals)) for j in range(10)))}</span>'
        else: c[k] = ''
    return render(c).replace('<tr>', f'<tr class="{cls}">', 1)
def build_body(days, grand):
    body = []; allv = []
    for d, dn, ids in days:
        body.append(f'<tr class="day"><th scope="rowgroup" colspan="{len(COLS)}"><span class="dl"><span>📅 اليوم {d}</span> · {dn}</span></th></tr>')
        vals = []
        for k in ids:
            c, v = row(k); vals.append(v); body.append(render(c).replace('<tr>', f'<tr data-pid="{k}">', 1))
        body.append(total_row(f'إجمالي اليوم {d}', vals, 'total')); allv += vals
    if grand: body.append(total_row(f'الإجمالي الكلي · {len(allv)} برنامج', allv, 'total grand'))
    return body
body = build_body(DAYS, True)
groups = []; 
for k, g, h, n in COLS[1:]:
    if groups and groups[-1][0] == g: groups[-1][1] += 1
    else: groups.append([g, 1])
ghead = '<tr class="groups"><th rowspan="2" class="corner" scope="col">البرنامج</th>' + ''.join(f'<th colspan="{n}" class="{g}" scope="colgroup">{GNAME[g]}</th>' for g, n in groups) + '</tr>'
def badge(k):
    r = ROLE.get(k)
    if not r: return ''
    return f'<span class="bd bd-{r[1]}">➕ {r[2]}</span>' if r[0] == 'add' else f'<span class="bd bd-{r[1]} rs">مجموع ➕1 لـ ➕{r[2]}</span>'
chead = '<tr class="cols">' + ''.join(f'<th class="{cls(k, g)}" scope="col">{badge(k)}{E(h)}' + (f'<small class="src">{E(n)}</small>' if n else '') + '</th>' for k, g, h, n in COLS[1:]) + '</tr>'
tpl = open('/home/claude/bench2/sizes/tpl.html').read()
out = tpl.replace('%%HEAD%%', ghead + chead).replace('%%BODY%%', '\n'.join(body))
open('/home/claude/bench2/sizes/bytes.html', 'w').write(out)
print(len(out))

# ---- fragments for the bench pages (one per day + all)
import re as _re
css = _re.search(r'<style>(.*?)</style>', tpl, _re.S).group(1)
def scope(css, S='#bytesSheet'):
    out = []; i = 0; n = len(css)
    def sel_map(sel):
        sel = sel.strip()
        if sel.startswith('/*'): return sel
        if sel.startswith(':root:not'): return sel + ' ' + S
        if sel.startswith(':root['): return sel + ' ' + S
        if sel == ':root': return S
        if sel == 'body': return S
        if sel == '*': return S + ', ' + S + ' *'
        return S + ' ' + sel
    def parse(block):
        res = []; j = 0
        while j < len(block):
            if block[j].isspace(): j += 1; continue
            if block.startswith('/*', j):
                k = block.index('*/', j) + 2; j = k; continue
            br = block.index('{', j)
            head = block[j:br].strip()
            depth = 1; k = br + 1
            while depth:
                if block[k] == '{': depth += 1
                elif block[k] == '}': depth -= 1
                k += 1
            inner = block[br + 1:k - 1]
            if head.startswith('@media'): res.append(head + '{' + parse(inner) + '}')
            else: res.append(','.join(sel_map(x) for x in head.split(',')) + '{' + inner + '}')
            j = k
        return '\n'.join(res)
    return parse(css)
scss = scope(css)
legend = _re.search(r'(<div class="keys".*?</div>)', tpl, _re.S).group(1)
notes = _re.search(r'(<div class="notes">.*?</div>)\s*</div>\s*$', tpl, _re.S).group(1)
def frag(days, grand):
    b = build_body(days, grand)
    return (f'<style>{scss}</style>' + legend +
            f'<div class="scroller" tabindex="0" aria-label="جدول البايتات"><table><thead>{ghead + chead}</thead><tbody>' + '\n'.join(b) + '</tbody></table></div>' + notes)
for d, dn, ids in DAYS:
    open(f'/home/claude/bench2/sizes/frag_day{d}.html', 'w').write(frag([(d, dn, ids)], False))
open('/home/claude/bench2/sizes/frag_all.html', 'w').write(frag(DAYS, True))
print('frags ok')
