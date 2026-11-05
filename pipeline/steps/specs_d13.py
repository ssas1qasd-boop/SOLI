import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d5 import rest, rng
F = '/home/claude/day13/src/'


def U(p, d): return rest(p, set().union(*[rng(v) for v in d.values()]))


def programs():
    P = {}
    p1 = F + 'p1_lifetime.cpp'
    a = {2: '37-48', 3: '49-52', 4: '21-31,53-58'}
    P[p1] = Program('d13_p1', {'lifetime.cpp': p1}, [
        S('Entity a في main', 'Created a، و main ends، وبعدين Destroyed a.', {'lifetime.cpp': U(p1, a)}),
        S('3 أنواع Scope', 'b و c و d0 و d1: كل واحد بيموت عند قوسه.', {'lifetime.cpp': a[2]}),
        S('new جوه Scope', 'Created heap، ومفيش Destroyed heap خالص.', {'lifetime.cpp': a[3]}),
        S('مصفوفة من دالة', 'CreateArray = 7، و FillArray = 9.', {'lifetime.cpp': a[4]})])
    p2 = F + 'p2_scoped_ptr.cpp'
    b = {2: '19-34,58-62,75', 3: '63-67', 4: '36-54,68-74'}
    P[p2] = Program('d13_p2', {'scoped_ptr.cpp': p2}, [
        S('Entity بيطبع', 'مفيش طباعة لسه: main فاضية.', {'scoped_ptr.cpp': U(p2, b)}),
        S('ScopedPtr', 'Destroyed Entity قبل after the scope، و sizeof = 8.', {'scoped_ptr.cpp': b[2]}),
        S('std::unique_ptr', 'نفس الترتيب بالمكتبة.', {'scoped_ptr.cpp': b[3]}),
        S('Timer', 'sum = 4950، و Timer loop عند القوس.', {'scoped_ptr.cpp': b[4]})])
    t1 = F + 't1_gpu_copy.cpp'
    c = {2: '101', 3: '112,114-118'}
    P[t1] = Program('d13_t1', {'gpu_copy.cpp': t1, 'stb.cpp': F + 'stb.cpp'}, [
        S('الصورة مرتين من غير قلب', 'الاتنين F مقلوب، وأول بكسل أبيض. اعمل <code>stb.cpp</code> جنبه.', {'gpu_copy.cpp': U(t1, c), 'stb.cpp': '1-2'}),
        S('stbi_set_flip_vertically_on_load', 'اليمين اتعدل، وأول بكسل بقى أحمر.', {'gpu_copy.cpp': c[2]}),
        S('امسح نسخة الـ CPU واقرا من الكارت', 'CPU copy freed و 192 بايت بنفس أول بكسل.', {'gpu_copy.cpp': c[3]})],
        kind='gl', window='GPU copy', run_cwd_extra={'stb_image.h': F + 'stb_image.h', 'res/letter.png': F + 'res/letter.png'})
    t2 = F + 't2_atlas.cpp'
    d = {2: '92-100'}
    P[t2] = Program('d13_t2', {'atlas.cpp': t2}, [
        S('5 مستطيلات والـ Atlas كله', 'الخمسة فيهم الـ 16 خانة.', {'atlas.cpp': U(t2, d)}),
        S('كل مستطيل خانة', 'الخانات 0 و 5 و 10 و 15، والخامس الـ Atlas كله.', {'atlas.cpp': d[2]})],
        kind='gl', window='Atlas')
    m1 = F + 'm1_rotate_compose.py'
    P[m1] = Program('d13_m1', {'rotate_compose.py': m1}, [
        S('مصفوفة الدوران', '(0, 1) و (0.866, 0.5).', {'rotate_compose.py': '1-13'}),
        S('دوران + دوران', 'True.', {'rotate_compose.py': '15'}),
        S('الترتيب', '(‎-1, 2) مقابل (‎-2, 1).', {'rotate_compose.py': '17-25'}),
        S('العكس والطول', '(1, 1) رجعت، والطول 1.414.', {'rotate_compose.py': '27-30'})], kind='py')
    m2 = F + 'm2_rotate3d_project.py'
    P[m2] = Program('d13_m2', {'rotate3d_project.py': m2}, [
        S('دوران حوالين x', '(2, 0, 1).', {'rotate3d_project.py': '1-11'}),
        S('الإسقاط بالـ Dot Product', '(2.8, 1.4)، والباقي عمودي.', {'rotate3d_project.py': '13-18'}),
        S('الإسقاط كمصفوفة', 'P، و P @ P = P، و (‎-1, 2) ← 0.', {'rotate3d_project.py': '20-25'})], kind='py')
    c1 = F + 'c1_csg.cpp'
    e = {2: '14-17,49', 3: '19-32,50-52', 4: '53-54'}
    P[c1] = Program('d13_c1', {'csg.cpp': c1}, [
        S('الكرة على محور x', 'سطر sphere A: من ‎-1 لـ 1.', {'csg.cpp': U(c1, e)}),
        S('الصندوق', 'سطر box B: من 0 لـ 2.', {'csg.cpp': e[2]}),
        S('العمليات التلاتة', 'Union و Intersect و Difference.', {'csg.cpp': e[3]}),
        S('نقطة فوق الصندوق', 'A 1، B 0، A minus B 1.', {'csg.cpp': e[4]})])
    c2 = F + 'c2_regularized.cpp'
    g = {2: '23-30,51', 3: '52-54'}
    P[c2] = Program('d13_c2', {'regularized.cpp': c2}, [
        S('تقاطع الحتت', '[1, 2] و [2, 2] (طول 0).', {'regularized.cpp': U(c2, g)}),
        S('Regularize', '0 pieces.', {'regularized.cpp': g[2]}),
        S('لوح فيه خرم', 'حتتين وطول 8.', {'regularized.cpp': g[3]})])
    return P
