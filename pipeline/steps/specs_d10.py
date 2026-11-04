import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d5 import rest, rng
F = '/home/claude/day10/src/'


def U(p, d): return rest(p, set().union(*[rng(v) for v in d.values()]))


def programs():
    P = {}
    p1 = F + 'p1_constructor.cpp'
    a = {2: '8-18,27-31,55-56', 3: '20-25,58-63', 4: '33-42,65'}
    P[p1] = Program('d10_p1', {'constructor.cpp': p1}, [
        S('struct من غير Constructor', 'أرقام عجيبة: مفيش حد حط قيم.', {'constructor.cpp': U(p1, a)}),
        S('Entity() الفاضي', '«Entity() ran» و 0, 0.', {'constructor.cpp': a[2]}),
        S('Constructor برقمين', 'اتختار حسب القوسين: 10, 5 و 3, 4.', {'constructor.cpp': a[3]}),
        S('Log() = delete', '[Log] Hello من غير object.', {'constructor.cpp': a[4]})])
    p2 = F + 'p2_destructor.cpp'
    b = {2: '15-18', 3: '53-55', 4: '21-39,57-62'}
    P[p2] = Program('d10_p2', {'destructor.cpp': p2}, [
        S('Entity على الـ Stack', 'Created من غير Destroyed: لسه مفيش Destructor.', {'destructor.cpp': U(p2, b)}),
        S('~Entity()', 'Destroyed اتطبعت بعد Function end.', {'destructor.cpp': b[2]}),
        S('على الـ Heap', 'Destroyed التانية بعد <code>delete</code> بس.', {'destructor.cpp': b[3]}),
        S('Buffer بيحجز ويرجّع', '~Buffer اشتغل عند الـ } قبل after.', {'destructor.cpp': b[4]})])
    t1 = F + 't1_crate.cpp'
    c = {2: '110-135,137-160,162-163,176,178-179,187', 3: '5,51-75,83-88,164,168,177', 4: '77-81,184,189'}
    P[t1] = Program('d10_t1', {'crate.cpp': t1, 'stb.cpp': F + 'stb.cpp'}, [
        S('الشباك و Esc', 'شباك كحلي، و Esc بيقفله.', {'crate.cpp': U(t1, c)}),
        S('المستطيل والـ Shaders', 'مستطيل أسود: الـ Shader بيقرا من خانة مفيهاش صورة.', {'crate.cpp': c[2]}),
        S('Texture class (Constructor)', 'اعمل <code>stb.cpp</code>. الصندوق ظهر بألوان الأركان.', {'crate.cpp': c[3], 'stb.cpp': '1-2'}),
        S('الـ Destructor', 'نفس الصورة. لما تضغط Esc هيطبع loop ended ثم ~Texture ثم glfwTerminate (زي النتيجة فوق).', {'crate.cpp': c[4]})],
        kind='gl', window='Crate', run_cwd_extra={'stb_image.h': F + 'stb_image.h', 'res/crate.png': F + 'res/crate.png'})
    t2 = F + 't2_two_textures.cpp'
    d = {2: '169', 3: '174,184', 4: '168'}
    P[t2] = Program('d10_t2', {'two_textures.cpp': t2, 'stb.cpp': F + 'stb.cpp'}, [
        S('نفس البرنامج بـ mix', 'الصندوق لوحده: amount لسه 0.', {'two_textures.cpp': U(t2, d), 'stb.cpp': '1-2'}),
        S('amount = 0.8', 'tex1 بيقرا الخانة 0 (الصندوق نفسه) 2 × 2.', {'two_textures.cpp': d[2]}),
        S('Texture face + Bind(1)', 'لسه نفس الصورة: tex1 لسه بيقرا من 0.', {'two_textures.cpp': d[3]}),
        S('tex1 = الخانة 1', 'الوشوش ظهرت.', {'two_textures.cpp': d[4]})],
        kind='gl', window='Two Textures', run_cwd_extra={'stb_image.h': F + 'stb_image.h', 'res/crate.png': F + 'res/crate.png', 'res/face.png': F + 'res/face.png'})
    m1 = F + 'm1_matrix_columns.py'
    P[m1] = Program('d10_m1', {'matrix_columns.py': m1}, [
        S('مصفوفة الوحدة', 'I₃ × x = x.', {'matrix_columns.py': '1-8'}),
        S('القاعدة المعيارية', '3 e₁ + 5 e₂ = (3, 5).', {'matrix_columns.py': '10-12'}),
        S('T(e₁) و T(e₂)', '(1, ‎-1, 4) و (3, 5, 1).', {'matrix_columns.py': '15-17,20-21'}),
        S('A = أعمدة', 'A @ v = T(v) في التلاتة.', {'matrix_columns.py': '23-29'})], kind='py')
    m2 = F + 'm2_shape_transforms.py'
    P[m2] = Program('d10_m2', {'shape_transforms.py': m2}, [
        S('حرف F و 4 مصفوفات', '', {'shape_transforms.py': '1-4,6,9-10,13-18'}),
        S('نحوّل الركن (2, 3)', '(4, 3) و (‎-3, 2) و (5, 3) و (‎-2, 3).', {'shape_transforms.py': '20-23,34-36'}),
        S('نرسم الشكلين', 'اتحفظت shapes.png.', {'shape_transforms.py': '24-25'}),
        S('سهم لكل عمود', '', {'shape_transforms.py': '26-32'})], kind='py')
    c1 = F + 'c1_brep_cylinder.cpp'
    e = {2: '17-32,58-68,70,74-81', 3: '83-88', 4: '34,38-46,90-96'}
    P[c1] = Program('d10_c1', {'brep_cylinder.cpp': c1}, [
        S('الأركان والأضلاع', '3 أضلاع.', {'brep_cylinder.cpp': U(c1, e)}),
        S('الحلقات والوشوش', 'الجنب: e0- e1+ e2+ e1-.', {'brep_cylinder.cpp': e[2]}),
        S('كل ضلع اتلمس كام مرة', 'التلاتة 2: Manifold.', {'brep_cylinder.cpp': e[3]}),
        S('أويلر و C(t) و S(u, v)', 'V - E + F = 2.', {'brep_cylinder.cpp': e[4]})])
    c2 = F + 'c2_brep_hole.cpp'
    g = {2: '42-49', 3: '70-86'}
    P[c2] = Program('d10_c2', {'brep_hole.cpp': c2}, [
        S('صندوق بخرم', '16 و 24 و 10 و 12 حلقة، و 0.', {'brep_hole.cpp': U(c2, g)}),
        S('نتأكد إن كل ضلع 2', 'manifold: yes.', {'brep_hole.cpp': g[2]}),
        S('مكعبين في ضلع', 'الضلع 2-6 أربع مرات: no.', {'brep_hole.cpp': g[3]})])
    return P
