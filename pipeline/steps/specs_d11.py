import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d5 import rest, rng
F = '/home/claude/day11/src/'


def U(p, d): return rest(p, set().union(*[rng(v) for v in d.values()]))


def programs():
    P = {}
    p1 = F + 'p1_stack_heap.cpp'
    a = {2: '26-31,35,40-42', 3: '13-16,36-37', 4: '38'}
    P[p1] = Program('d11_p1', {'stack_heap.cpp': p1}, [
        S('على الـ Stack', 'الأحجام 4 و 20 و 12، وعناوين الـ Stack (0x7ff…).', {'stack_heap.cpp': U(p1, a)}),
        S('نفس الحاجات بـ new', 'عناوين الـ Heap مختلفة خالص (0x5…)، و delete لكل واحد.', {'stack_heap.cpp': a[2]}),
        S('المسافات بالبايت', 'array - &vector = 12 (لازقين في بعض)، وعلى الـ Heap كل واحد بعد 32.', {'stack_heap.cpp': a[3]}),
        S('نفس القيم في الاتنين', '5 = 5، 2 = 2، 12 = 12.', {'stack_heap.cpp': a[4]})])
    p2 = F + 'p2_speed_size.cpp'
    b = {2: '40-46,49-50', 3: '21-27,53-56'}
    P[p2] = Program('d11_p2', {'speed_size.cpp': p2}, [
        S('عدد 100 Vector3 على الـ Stack', 'كام ns لكل واحد (الرقم بيتغير كل تشغيلة).', {'speed_size.cpp': U(p2, b)}),
        S('نفس العدد بـ new و delete', 'رقم الـ Heap، و heap / stack.', {'speed_size.cpp': b[2]}),
        S('صورة 16 MB على الـ Heap', 'LoadTexture: 16 MB، والصورة لسه عايشة في main لحد delete[].', {'speed_size.cpp': b[3]})])
    t1 = F + 't1_wrap_by_hand.cpp'
    c = {2: '188,190,193', 3: '85-89,173,191', 4: '172,192,195-198'}
    P[t1] = Program('d11_t1', {'wrap_by_hand.cpp': t1, 'stb.cpp': F + 'stb.cpp'}, [
        S('الشباك والمستطيل والصورة', 'شباك كحلي فاضي: لسه مفيش رسم. اعمل <code>stb.cpp</code> بتاع امبارح جنبه.', {'wrap_by_hand.cpp': U(t1, c), 'stb.cpp': '1-2'}),
        S('3 مستطيلات فوق', 'نفس الصورة 3 مرات: الإعداد الافتراضي REPEAT.', {'wrap_by_hand.cpp': c[2]}),
        S('SetWrap: الكارت يعمل التكرار', 'فوق: REPEAT ثم MIRRORED_REPEAT ثم CLAMP_TO_EDGE.', {'wrap_by_hand.cpp': c[3]}),
        S('تحت: إحنا نعمل التكرار بإيدنا', 'الصف اللي تحت نسخة من اللي فوق بالظبط.', {'wrap_by_hand.cpp': c[4]})],
        kind='gl', window='Wrap by hand', run_cwd_extra={'stb_image.h': F + 'stb_image.h', 'res/letter.png': F + 'res/letter.png'})
    t2 = F + 't2_procedural.cpp'
    d = {2: '156,168-170', 3: '104-115,117-118,172-174,180', 4: '116'}
    P[t2] = Program('d11_t2', {'procedural.cpp': t2}, [
        S('الشباك وحدود الكارت', 'اتطبع الكارت وعدد الخانات (32) وأكبر مقاس، والشباك فاضي.', {'procedural.cpp': U(t2, d)}),
        S('رقعة شطرنج من دالة', 'شمال: أحمر وأزرق 8 × 8 من غير أي صورة.', {'procedural.cpp': d[2]}),
        S('نفس الرقعة من صورة 2 × 2', 'يمين: الألوان باظت (أصفر وكحلي ومايلة).', {'procedural.cpp': d[3]}),
        S('glPixelStorei(GL_UNPACK_ALIGNMENT, 1)', 'يمين بقى زي الشمال بالظبط.', {'procedural.cpp': d[4]})],
        kind='gl', window='Procedural')
    m1 = F + 'm1_add_subtract.py'
    P[m1] = Program('d11_m1', {'add_subtract.py': m1}, [
        S('A + B (مثال Khan)', '[[6, ‎-7, 8], [11, 2, ‎-3]]، و B + A نفس الحاجة.', {'add_subtract.py': '1-7'}),
        S('الطرح', 'C - D = C + (‎-1) × D، و D - C بالسالب.', {'add_subtract.py': '9-16'}),
        S('الجمع بإيدنا عنصر عنصر', 'نفس نتيجة A + B.', {'add_subtract.py': '19-30'}),
        S('مقاسين مختلفين', 'undefined، و NumPy رفض بـ ValueError.', {'add_subtract.py': '31-37'})], kind='py')
    m2 = F + 'm2_move_shape.py'
    P[m2] = Program('d11_m2', {'move_shape.py': m2}, [
        S('بيت + مصفوفة نقل', 'السقف (1, 3) راح (4, 4)، والطرح رجّعه.', {'move_shape.py': '1-12'}),
        S('صف واحد بس', 'السقف بس نزل لـ 1.5.', {'move_shape.py': '14-17'}),
        S('4 فريمات', 'الركن 0 ماشي من (0, 0) لـ (3, 1).', {'move_shape.py': '19-21'}),
        S('الرسمة', 'اتحفظت moves.png.', {'move_shape.py': '23-30'})], kind='py')
    c1 = F + 'c1_obj_cube.cpp'
    e = {2: '9-12,38-62', 3: '14-27,64-78', 4: '80-85'}
    P[c1] = Program('d11_c1', {'obj_cube.cpp': c1}, [
        S('نكتب cube.obj', 'مفيش طباعة: بس اتعمل ملف cube.obj جنب البرنامج (افتحه بالـ Notepad).', {'obj_cube.cpp': U(c1, e)}),
        S('نقرا الملف سطر سطر', 'read cube.obj: 8 vertices, 6 faces.', {'obj_cube.cpp': e[2]}),
        S('الـ Normal من ترتيب الأركان', 'الستة outward.', {'obj_cube.cpp': e[3]}),
        S('الأضلاع وأويلر', 'V = 8، E = 12، F = 6، و V - E + F = 2.', {'obj_cube.cpp': e[4]})])
    c2 = F + 'c2_mesh_vs_brep.cpp'
    g = {2: '42-50', 3: '53-60', 4: '62-67'}
    P[c2] = Program('d11_c2', {'mesh_vs_brep.cpp': c2}, [
        S('نبني الأسطوانة مثلثات', 'اتطبع سطر الـ B-Rep بس: الـ Mesh اتبنى في الرام.', {'mesh_vs_brep.cpp': U(c2, g)}),
        S('نعد الـ Mesh', 'V = 16، E = 42، F = 28، و V - E + F = 2.', {'mesh_vs_brep.cpp': g[2]}),
        S('جدول n', 'كل ما n تكبر: مثلثات أكتر وغلط أقل.', {'mesh_vs_brep.cpp': g[3]}),
        S('كام n لدقة 0.01 مم؟', 'n = 256 و 1020 مثلث.', {'mesh_vs_brep.cpp': g[4]})])
    return P
