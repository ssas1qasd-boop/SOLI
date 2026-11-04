import sys, re
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d3 import GL_WIN
F = '/home/claude/day5/src/'
NAMES = 'Braden\nJeff\nKatie\nQ\n'
K = ('key', 'BackSpace')
CLICKS = [(80, 400), (200, 300), (320, 380), (440, 260), (0, 0, 3), (120, 120), (300, 60), (480, 120), (0, 0, 3)]
CLICKS_BS = CLICKS + [K, (150, 200), (400, 200), (500, 330), K]

def rest(path, exclude):
    """every non-blank, non-brace line of the file that is not in `exclude` (a set of line numbers)."""
    out = []
    for i, l in enumerate(open(path), 1):
        t = l.strip()
        if not t or re.match(r'^[{}];?$', t) or i in exclude: continue
        out.append(i)
    return ','.join(map(str, out))

def rng(r):
    s = set()
    for p in r.split(','):
        if '-' in p: a, b = p.split('-'); s |= set(range(int(a), int(b) + 1))
        elif p: s.add(int(p))
    return s

def programs():
    P = {}
    P[F + 'p1_swap_pointers.cpp'] = Program('d5_p1', {'swap_pointers.cpp': F + 'p1_swap_pointers.cpp'}, [
        S('الهيكل', 'المكتبة و <code>main</code> فاضية. اعمل Run: لازم يشتغل من غير أخطاء قبل ما تزوّد أي حاجة.', {'swap_pointers.cpp': '1,3-4,6'}),
        S('المتغيرين والطباعة', 'لسه مفيش تبديل: بنطبع القيم مرتين.', {'swap_pointers.cpp': '8,12-13,17-18'}),
        S('دالة swap بالـ Pointers', 'سطر التعريف جوه <code>main</code>، والنداء بالعناوين، والدالة تحت.', {'swap_pointers.cpp': '10,15,21,23-26'})])
    P[F + 'p2_swap_three.cpp'] = Program('d5_p2', {'swap_three.cpp': F + 'p2_swap_three.cpp'}, [
        S('الهيكل والعناوين', 'بنطبع مكان <code>x</code> و <code>y</code> في الذاكرة. الأرقام دي بتتغير كل مرة تشغّل فيها البرنامج.', {'swap_three.cpp': '1,27,29-30'}),
        S('SwapValue: نسخ', 'الدالة استلمت نسخ في أماكن تانية، فـ <code>x</code> و <code>y</code> ماتغيروش.', {'swap_three.cpp': '3,5-8,32-33'}),
        S('SwapPointer: عناوين', 'الدالة استلمت نفس عناوين <code>x</code> و <code>y</code>، فبدّلتهم فعلاً.', {'swap_three.cpp': '11,13-16,35-36'}),
        S('SwapReference: أسماء تانية لنفس الصناديق', 'نفس العناوين بالظبط، فبدّلتهم تاني ورجعوا زي الأول.', {'swap_three.cpp': '19,21-24,38-39'})])
    P[F + 'n1_numpy_basics.py'] = Program('d5_n1', {'numpy_basics.py': F + 'n1_numpy_basics.py'}, [
        S('import و مصفوفتين', 'لو ظهر <code>ModuleNotFoundError</code> يبقى NumPy مش متسطبة: اكتب في الـ Terminal <code>pip install numpy</code>.', {'numpy_basics.py': '1,3-6'}),
        S('الأبعاد والشكل والنوع والحجم', '', {'numpy_basics.py': '8-11'}),
        S('الوصول لعنصر وصف وعمود', '', {'numpy_basics.py': '13-15'}),
        S('الحساب على كل العناصر مرة واحدة', '', {'numpy_basics.py': '17-19'}),
        S('تحذير النسخ: c = a', '', {'numpy_basics.py': '21-23'}),
        S('الحل: copy()', '', {'numpy_basics.py': '25-28'})], kind='py')
    P[F + 'n2_dot_cross.py'] = Program('d5_n2', {'dot_cross.py': F + 'n2_dot_cross.py'}, [
        S('import والمتجهين', '', {'dot_cross.py': '1,3-5'}),
        S('الضرب النقطي بـ 3 طرق', '', {'dot_cross.py': '7-10'}),
        S('الضرب الاتجاهي والتأكد منه', '', {'dot_cross.py': '12-15'}),
        S('الطول والزاوية', '', {'dot_cross.py': '17-22'}),
        S('x × y = z', '', {'dot_cross.py': '24-26'}),
        S('كذا متجه مرة واحدة', '', {'dot_cross.py': '28-32'})], kind='py')
    P[F + 'c1_names_vector.cpp'] = Program('d5_c1', {'names_vector.cpp': F + 'c1_names_vector.cpp'}, [
        S('الهيكل', 'المكتبات و <code>main</code> فاضية.', {'names_vector.cpp': '1-3,5,7,30'}),
        S('الـ vector واللوب', 'كتبنا في الـ Terminal: Braden و Jeff و Katie و Q. لسه مفيش طباعة للأسماء.', {'names_vector.cpp': '9,11,13,15,17-18'}),
        S('pop_back والطباعة', '', {'names_vector.cpp': '21,23,25,27'})], stdin=NAMES)
    c2 = F + 'c2_delete_last_line.cpp'
    s2 = '90,92-93,105-108,110-113,153'
    s3 = '95,97,99-100,102'
    P[c2] = Program('d5_c2', {'delete_last_line.cpp': c2}, [
        S('برنامج الـ Polylines بتاع امبارح', 'نفس برنامج امبارح، بس رفع النقط للكارت بقى في دالة لوحدها <code>UploadPoints</code> عشان هنستخدمها مرتين. دوسنا: 4 شمال، يمين، 3 شمال، يمين.', {'delete_last_line.cpp': rest(c2, rng(s2) | rng(s3))}),
        S('Backspace يمسح آخر خط', 'دوسنا نفس الدوسات وبعدها Backspace. اتفرج على الـ Terminal: «deleted a line of 0 points». الدوس يمين كان بدأ خط جديد فاضي، فـ Backspace مسح الفاضي ده، والخط التاني فضل مكانه. وبعدين رسمنا خط بـ 3 نقط، و Backspace التاني مسحه.', {'delete_last_line.cpp': s2}),
        S('لو الخط الحالي فاضي', 'نفس الدوسات بالظبط. المرة دي أول Backspace مسح الخط التاني فعلاً («deleted a line of 3 points»)، لأنه اتخطى الخط الفاضي.', {'delete_last_line.cpp': s3})],
        kind='gl', window='Delete Last Line', clicks={1: CLICKS, 2: CLICKS_BS, 3: CLICKS_BS})
    r1 = F + 'r1_red_triangle.cpp'
    P[r1] = Program('d5_r1', {'red_triangle.cpp': r1}, [
        S('المكتبات و main فاضية', '', {'red_triangle.cpp': '1-4,50,121'}),
        S(*GL_WIN, {'red_triangle.cpp': '52-56,58-59,61-62,64-65,67-68,111,113,115-116,120'}),
        S('الـ 3 أركان في كارت الشاشة', 'لسه أسود: مفيش Shader ومفيش رسم.', {'red_triangle.cpp': '70-73,76-78,80-83,85-86'}),
        S('الـ Shaders كنص، والترجمة، والرسم', 'من غير أي فحص للأخطاء لسه.', {'red_triangle.cpp': '6,8-11,30,33,35-37,39-41,44-45,47,88-96,98-106,108-109,114,119'}),
        S('فحص الأخطاء زي The Cherno', 'النتيجة نفسها، لأن الـ Shader سليم. الفايدة بتبان لما تغلط (شوف قسم «ليه»).', {'red_triangle.cpp': '13-15,17-27,42'})],
        kind='gl', window='Red Triangle')
    r2 = F + 'r2_shader_edit.cpp'
    P[r2] = Program('d5_r2', {'shader_edit.cpp': r2}, [
        S('المكتبات و main فاضية', '', {'shader_edit.cpp': '1-4,50,124'}),
        S(*GL_WIN, {'shader_edit.cpp': '52-56,58-59,61-62,64-65,67-68,114,116,118-119,123'}),
        S('الأركان زي البرنامج 1', 'لسه أسود.', {'shader_edit.cpp': '70-73,76-78,80-83,85-86'}),
        S('الدوال، والـ Shaders المعدّلة، والرسم', 'الدالتين زي البرنامج 1 بالظبط. الـ Vertex كبّر المثلث وبعت مكانه، والـ Fragment لوّن كل بكسل حسب مكانه.', {'shader_edit.cpp': '6,8-11,13-15,17-27,30,33,35-37,39-42,44-45,47,88-98,100-109,111-112,117,122'})],
        kind='gl', window='Shader Edit')
    return P
