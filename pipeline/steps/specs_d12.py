import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d5 import rest, rng
F = '/home/claude/day12/src/'


def U(p, d): return rest(p, set().union(*[rng(v) for v in d.values()]))


def programs():
    P = {}
    p1 = F + 'p1_new.cpp'
    a = {2: '29-39,48-49,58', 3: '50-51,59', 4: '53-54,60'}
    P[p1] = Program('d12_p1', {'new_operator.cpp': p1}, [
        S('operator new بتاعتنا، و new int', 'new int: 4 bytes، و new int[50]: 200 bytes.', {'new_operator.cpp': U(p1, a)}),
        S('new Entity()', 'Entity() ran، و 32 bytes، و name = Unknown.', {'new_operator.cpp': a[2]}),
        S('new Entity[3]', 'Entity() ran عدد 3 مرات، و 104 bytes.', {'new_operator.cpp': a[3]}),
        S('malloc من غير Constructor', 'سطر malloc من غير «Entity() ran» قبله.', {'new_operator.cpp': a[4]})])
    p2 = F + 'p2_placement.cpp'
    b = {2: '25-27,29', 3: '32-33'}
    P[p2] = Program('d12_p2', {'placement_new.cpp': p2}, [
        S('200 بايت على الـ Heap', 'عنوان الـ 200 بايت بس.', {'placement_new.cpp': U(p2, b)}),
        S('Placement new جوه الـ 200 بايت', 'Vector3(1, 2, 3) عند نفس عنوان b، و b[0] = 1، و ~Vector3 بإيدنا.', {'placement_new.cpp': b[2]}),
        S('new العادي للمقارنة', 'Vector3(4, 5, 6) في عنوان جديد، و delete نادت الـ Destructor.', {'placement_new.cpp': b[3]})])
    t1 = F + 't1_mipmaps.cpp'
    c = {2: '114,116-125', 3: '126-128,155,170'}
    P[t1] = Program('d12_t1', {'mipmaps.cpp': t1}, [
        S('الأرضية بـ 4 فلاتر من غير Mipmaps', 'فوق: Moiré. تحت: أسود (فلتر MIPMAP ومفيش مستويات).', {'mipmaps.cpp': U(t1, c)}),
        S('glGenerateMipmap', 'mip level 0 لـ 8 اتطبعوا، واللي تحت ظهر هادي ورمادي بعيد.', {'mipmaps.cpp': c[2]}),
        S('Anisotropy = 16 للمربع الأخير', 'levels: 9 و 16، وتحت يمين أوضح لبعيد.', {'mipmaps.cpp': c[3]})],
        kind='gl', window='Mipmaps')
    t2 = F + 't2_mip_levels.cpp'
    d = {2: '124-125,151,165'}
    P[t2] = Program('d12_t2', {'mip_levels.cpp': t2}, [
        S('9 مستويات بـ 9 ألوان', 'الأحجام لحد 1 × 1، و 1.33333، والأرضية شرايط ألوان (الاتنين زي بعض).', {'mip_levels.cpp': U(t2, d)}),
        S('Anisotropy في اليمين', 'يمين: الأحمر والبرتقاني بقوا أطول (المستويات الصغيرة اتأخرت).', {'mip_levels.cpp': d[2]})],
        kind='gl', window='Mip levels')
    m1 = F + 'm1_numpy_arrays.py'
    P[m1] = Program('d12_m1', {'numpy_arrays.py': m1}, [
        S('الأبعاد والنوع والحجم', 'ndim و shape و int64 = 8 بايت، و int16 = 2.', {'numpy_arrays.py': '1-8'}),
        S('الوصول لخانة وصف وعمود', 'm[1, 5] = 13، و [2 4 6]، والعمود 2 اتغيّر.', {'numpy_arrays.py': '10-17'}),
        S('تمرين Keith 5 × 5', 'إطار 1 وجوه أصفار و 9 في النص.', {'numpy_arrays.py': '19-24'}),
        S('y = x مقابل copy', 'x اتغيّرت في الأولى، وماتغيّرتش في التانية.', {'numpy_arrays.py': '26-33'})], kind='py')
    m2 = F + 'm2_numpy_math.py'
    P[m2] = Program('d12_m2', {'numpy_math.py': m2}, [
        S('عمليات على كل خانة', '[3 4 5 6] و [2 4 6 8] و [1 4 9 16].', {'numpy_math.py': '1-5'}),
        S('matmul و * و det', '2 × 2 كلها 6، و 2 × 3 كلها 1، و 1.0.', {'numpy_math.py': '7-13'}),
        S('الإحصاء و reshape', 'min 1 و max 6 و sum 21، و (4, 2)، و ValueError.', {'numpy_math.py': '15-25'}),
        S('stack والفلترة', 'vstack و (2, 6) و [75 88 51].', {'numpy_math.py': '27-37'})], kind='py')
    c1 = F + 'c1_parametric.cpp'
    e = {2: '6-9,21-44,50-51', 3: '52-55', 4: '56-57'}
    P[c1] = Program('d12_c1', {'parametric.cpp': c1}, [
        S('معادلة Dr. Patil لنقطة', '(0, ‎-10, 25) تقريباً.', {'parametric.cpp': U(c1, e)}),
        S('Range ودالة Shape', 'point بـ 0، و circle بـ 1 (curve).', {'parametric.cpp': e[2]}),
        S('باقي الأشكال', 'cylinder و disk = surface، و solid و hollow = solid.', {'parametric.cpp': e[3]}),
        S('المساحات والأحجام', '1570.8 و 314.159 و 7853.98 و 5890.49.', {'parametric.cpp': e[4]})])
    c2 = F + 'c2_three_models.cpp'
    g = {2: '39-43', 3: '10-14,21-27,45-56'}
    P[c2] = Program('d12_c2', {'three_models.cpp': c2}, [
        S('Wireframe: 12 خط', 'الطول 24، والمساحة والحجم ؟', {'three_models.cpp': U(c2, g)}),
        S('Surface: 6 وشوش', 'المساحة 24، والحجم ؟', {'three_models.cpp': g[2]}),
        S('Solid: 6 أنصاف فراغ', 'المركز جوه، و (1.5, 0, 0) برّه، والحجم 8.', {'three_models.cpp': g[3]})])
    return P
