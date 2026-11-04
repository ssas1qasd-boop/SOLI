import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d5 import rest, rng
F = '/home/claude/day9/src/'


def U(p, d): return rest(p, set().union(*[rng(v) for v in d.values()]))


def programs():
    P = {}
    p1 = F + 'p1_struct_class.cpp'
    a = {2: '15-26,45-47,50', 3: '28-37,52-57'}
    P[p1] = Program('d9_p1', {'struct_class.cpp': p1}, [
        S('struct من غير public', 'x = 2 و y = ‎-2، والحجم 12 بايت.', {'struct_class.cpp': U(p1, a)}),
        S('نفس اللاعب بـ class', 'لازم <code>public:</code>. نفس الأرقام ونفس الحجم.', {'struct_class.cpp': a[2]}),
        S('Vec2 (بيانات بسيطة)', '(2, 0) و 8 بايت.', {'struct_class.cpp': a[3]})])
    p2 = F + 'p2_vertex_struct.cpp'
    b = {2: '20-22', 3: '24-28', 4: '30-31'}
    P[p2] = Program('d9_p2', {'vertex_struct.cpp': p2}, [
        S('الركن struct', 'الركن 16 بايت = الـ stride.', {'vertex_struct.cpp': U(p2, b)}),
        S('offsetof والحجم كله', 'x عند 0، و u عند 8، والكل 64 بايت.', {'vertex_struct.cpp': b[2]}),
        S('نفس البايتات كأرقام', '16 رقم ورا بعض.', {'vertex_struct.cpp': b[3]}),
        S('نغيّر بالاسم', 'الرقم رقم 10 بقى 2.', {'vertex_struct.cpp': b[4]})])
    t1 = F + 't1_pixel_cat.cpp'
    c = {2: '5,119-122,137', 3: '124-127,129-132,134,138,140-142,153,165', 4: '135', 5: '144-145'}
    P[t1] = Program('d9_t1', {'pixel_cat.cpp': t1, 'stb.cpp': F + 'stb.cpp'}, [
        S('الشباك والمربع', 'مربع أسود على خلفية كحلي: الـ Shader بيقرا من خانة فاضية.', {'pixel_cat.cpp': U(t1, c)}),
        S('نحمّل الصورة للرام', 'اعمل <code>stb.cpp</code>. اتطبع 16 × 16 و 4 قنوات. المربع لسه أسود.', {'pixel_cat.cpp': c[2], 'stb.cpp': '1-2'}),
        S('الـ Texture والإعدادات', 'لسه أسود: MIN_FILTER بيطلب Mipmaps ومفيش.', {'pixel_cat.cpp': c[3]}),
        S('glGenerateMipmap', 'القطة ظهرت، بس الأماكن الشفافة سودا.', {'pixel_cat.cpp': c[4]}),
        S('الشفافية (Blending)', 'الخلفية الكحلي بانت من الأماكن الشفافة.', {'pixel_cat.cpp': c[5]})],
        kind='gl', window='Pixel Cat', run_cwd_extra={'stb_image.h': F + 'stb_image.h', 'res/pixel_cat.png': F + 'res/pixel_cat.png'})
    t2 = F + 't2_wrap_modes.cpp'
    d = {2: '5,121-123,125,128-136,138-141,166', 3: '126,151-154,156', 4: '127,137'}
    P[t2] = Program('d9_t2', {'wrap_modes.cpp': t2, 'stb.cpp': F + 'stb.cpp'}, [
        S('الشباك والمربع', 'مربع أسود في النص.', {'wrap_modes.cpp': U(t2, d)}),
        S('الصورة في 4 Textures', 'اعمل <code>stb.cpp</code>. اتعملوا الأربعة، بس الرسم لسه مرة واحدة في النص بآخر واحدة اتربطت (CLAMP_TO_BORDER).', {'wrap_modes.cpp': d[2], 'stb.cpp': '1-2'}),
        S('لوب الرسم', '4 مربعات، كل واحد بنوع. CLAMP_TO_BORDER حدوده شفافة (لون الحدود الافتراضي 0 0 0 0).', {'wrap_modes.cpp': d[3]}),
        S('لون الحدود', 'الحدود بقت حمرا.', {'wrap_modes.cpp': d[4]})],
        kind='gl', window='Wrap Modes', run_cwd_extra={'stb_image.h': F + 'stb_image.h', 'res/logo.png': F + 'res/logo.png'})
    m1 = F + 'm1_transform.py'
    P[m1] = Program('d9_m1', {'transform.py': m1}, [
        S('T من ℝ³ لـ ℝ²', '(3, 3) و (10, 3).', {'transform.py': '1-3,6-8'}),
        S('نفس T بمصفوفة', 'نفس الأرقام.', {'transform.py': '10-11,14-15,18-19'}),
        S('تحويل مش خطي', 'الأصل اتحرك.', {'transform.py': '22-24,27-28'})], kind='py')
    m2 = F + 'm2_projection.py'
    P[m2] = Program('d9_m2', {'projection.py': m2}, [
        S('P مصفوفة 2 × 3', '', {'projection.py': '1,6-8'}),
        S('نحوّل الـ 8 أركان', 'نفس أرقام امبارح.', {'projection.py': '10-14,16-18'}),
        S('خاصية الخطي', '', {'projection.py': '20-21'}),
        S('نرسم', 'اتحفظت projection.png.', {'projection.py': '2-4,23-34'})], kind='py')
    c1 = F + 'c1_mesh.cpp'
    e = {2: '3-4,54-65', 3: '16-38,67-70'}
    P[c1] = Program('d9_c1', {'mesh.cpp': c1}, [
        S('المكعب مثلثات', '432 بايت مقابل 240.', {'mesh.cpp': U(c1, e)}),
        S('نعد الأضلاع (std::set)', 'E = 18، وأويلر 2.', {'mesh.cpp': e[2]}),
        S('Barycentric', 'جوه، على ضلع، على ركن، برّه.', {'mesh.cpp': e[3]})])
    c2 = F + 'c2_barycentric.cpp'
    g = {2: '50-54,98-102,104-113,142', 3: '115-133,135-136,157', 4: '56-76,144-150'}
    P[c2] = Program('d9_c2', {'barycentric.cpp': c2}, [
        S('الشباك', 'أسود.', {'barycentric.cpp': U(c2, g)}),
        S('المثلث في الكارت', 'لسه مفيش Shader، فمفيش رسم.', {'barycentric.cpp': g[2]}),
        S('الـ Shaders', 'المثلث الملون ظهر.', {'barycentric.cpp': g[3]}),
        S('نقارن بحسابنا', 'لون الكارت = لوننا.', {'barycentric.cpp': g[4]})], kind='gl', window='Barycentric')
    return P
