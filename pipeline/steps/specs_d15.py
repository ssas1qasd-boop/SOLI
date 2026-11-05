import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d5 import rest, rng
F = '/home/claude/day15/src/'


def U(p, d): return rest(p, set().union(*[rng(v) for v in d.values()]))


def programs():
    P = {}
    p1 = F + 'p1_print_template.cpp'
    a = {2: '27-28', 3: '10-14,30-32', 4: '16-20,33'}
    P[p1] = Program('d15_p1', {'print_template.cpp': p1}, [
        S('Template واحد لـ Print', 'int و float و const char*.', {'print_template.cpp': U(p1, a)}),
        S('النوع بإيدنا', 'std::string، و 7.9 بقت 7.', {'print_template.cpp': a[2]}),
        S('Biggest', '9 و 2.5 و banana.', {'print_template.cpp': a[3]}),
        S('Template فيه غلطة', 'اترجم عادي لأن محدش ناداه.', {'print_template.cpp': a[4]})])
    p2 = F + 'p2_array_template.cpp'
    b = {2: '30-32', 3: '34-37', 4: '39-40'}
    P[p2] = Program('d15_p2', {'array_template.cpp': p2}, [
        S('Array<int, 5>', 'size 5، و 20 بايت، و numbers[4] = 40.', {'array_template.cpp': U(p2, b)}),
        S('Array<float, 3>', '12 بايت.', {'array_template.cpp': b[2]}),
        S('Array<std::string, 2>', '64 بايت، و Cem.', {'array_template.cpp': b[3]}),
        S('std::array', 'نفس الـ 20 بايت.', {'array_template.cpp': b[4]})])
    t1 = F + 't1_transform2d.cpp'
    c = {2: '127-133'}
    P[t1] = Program('d15_t1', {'transform2d.cpp': t1}, [
        S('4 بيوت بـ 4 مصفوفات', 'رمادي وأزرق وبرتقاني وأخضر، ومفيش طباعة.', {'transform2d.cpp': U(t1, c)}),
        S('اطبع المصفوفات', 'العمود التالت = التحريك، والركن حوالين المركز (0.65, 0.55).', {'transform2d.cpp': c[2]})],
        kind='gl', window='Transform 2D')
    t2 = F + 't2_homogeneous.cpp'
    d = {2: '65-70', 3: '72-73', 4: '75-79'}
    P[t2] = Program('d15_t2', {'homogeneous.cpp': t2}, [
        S('M = T R', '[0, ‎-1, 3] [1, 0, 2] [0, 0, 1].', {'homogeneous.cpp': U(t2, d)}),
        S('نقطة واتجاه', '(3, 3) و (0, 1).', {'homogeneous.cpp': d[2]}),
        S('R Rᵀ = I', 'Identity، و Rᵀ = R(‎-30).', {'homogeneous.cpp': d[3]}),
        S('Skew', '(1, 1) ← (2, 2).', {'homogeneous.cpp': d[4]})])
    m1 = F + 'm1_composition.py'
    P[m1] = Program('d15_m1', {'composition.py': m1}, [
        S('دوران ثم Shear', '[[1, ‎-1], [1, 0]].', {'composition.py': '1-13'}),
        S('مثال M1 و M2', '[[2, 0], [1, ‎-2]].', {'composition.py': '15-24'}),
        S('الترتيب', 'same? False.', {'composition.py': '26-30'}),
        S('التجميع', 'نفس النتيجة.', {'composition.py': '32-35'})], kind='py')
    m2 = F + 'm2_grid_plot.py'
    P[m2] = Program('d15_m2', {'grid_plot.py': m2}, [
        S('الشبكة', 'مفيش طباعة.', {'grid_plot.py': '1-14'}),
        S('الرسمتين', 'î و ĵ للترتيبين، و composition.png.', {'grid_plot.py': '16-31'})], kind='py')
    c1 = F + 'c1_translate4x4.cpp'
    e = {2: '40-42', 3: '44-49', 4: '51-56'}
    P[c1] = Program('d15_c1', {'translate4x4.cpp': c1}, [
        S('مصفوفة 4 × 4', 'العمود الرابع 7 و 3 و 5.', {'translate4x4.cpp': U(c1, e)}),
        S('ركن', '(8, 2, 7).', {'translate4x4.cpp': e[2]}),
        S('Normal', 'w = 0 مابيتحركش، و w = 1 باظ.', {'translate4x4.cpp': e[3]}),
        S('Animation', '5 فريمات لحد (8, 2, 7).', {'translate4x4.cpp': e[4]})])
    c2 = F + 'c2_order.cpp'
    g = {2: '45', 3: '46'}
    P[c2] = Program('d15_c2', {'order.cpp': c2}, [
        S('اللفات', 'angle 0 و 90 و 180 و 270 بس.', {'order.cpp': U(c2, g)}),
        S('T * R', 'المركز ثابت (7, 0).', {'order.cpp': g[2]}),
        S('R * T', 'المركز بيلف حوالين 0.', {'order.cpp': g[3]})])
    return P
