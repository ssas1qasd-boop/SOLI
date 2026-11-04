import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d5 import rest, rng
F = '/home/claude/day7/src/'
FK = ('key', 'F12')


def programs():
    P = {}
    p1 = F + 'p1_pointers_review.cpp'
    a = {2: '10-12', 3: '14-15', 4: '17-21,27-29', 5: '23-25'}
    P[p1] = Program('d7_p1', {'pointers_review.cpp': p1}, [
        S('العنوان و void*', 'الـ Pointer = رقم فيه عنوان. <code>&amp;var</code> و <code>ptr</code> نفس الرقم.', {'pointers_review.cpp': rest(p1, set().union(*[rng(v) for v in a.values()]))}),
        S('نكتب من خلال int*', '<code>var</code> بقى 10 من غير ما نكتب اسمه.', {'pointers_review.cpp': a[2]}),
        S('حجم الـ Pointer', 'كلهم 8 بايت على جهاز 64-bit.', {'pointers_review.cpp': a[3]}),
        S('8 بايت على الـ Heap', 'حجزنا، وكتبنا حرفين، ومسحنا.', {'pointers_review.cpp': a[4]}),
        S('Pointer لـ Pointer', 'سلسلة عناوين: <code>ptrToBuffer</code> ← <code>buffer</code> ← الحروف.', {'pointers_review.cpp': a[5]})])
    p2 = F + 'p2_pointer_quiz.cpp'
    b = {2: '11-15,43-46', 3: '17-22,48-51', 4: '24-30,53-54'}
    P[p2] = Program('d7_p2', {'pointer_quiz.cpp': p2}, [
        S('Swap و check', '', {'pointer_quiz.cpp': rest(p2, set().union(*[rng(v) for v in b.values()]))}),
        S('SetToZero', '', {'pointer_quiz.cpp': b[2]}),
        S('MakeText (Pointer لـ Pointer)', '', {'pointer_quiz.cpp': b[3]}),
        S('Sum', 'الـ 4 PASS.', {'pointer_quiz.cpp': b[4]})])
    r1 = F + 'r1_vertex_array.cpp'
    c = {2: '82-83', 3: '131-134,144,147-148', 4: '138,157-159'}
    P[r1] = Program('d7_r1', {'vertex_array.cpp': r1}, [
        S('المستطيل بالـ VAO (زي امبارح)', 'كل حاجة متربطة من وقت الإعداد، فالرسم شغال.', {'vertex_array.cpp': rest(r1, set().union(*[rng(v) for v in c.values()]))}),
        S('تجربة: من غير VAO', 'قبل ما نعمل الـ VAO: الأمر اترفض بخطأ 1282. والرسم لسه شغال عادي.', {'vertex_array.cpp': c[2]}),
        S('نفك كل حاجة ونربط قبل الرسم', 'فكّينا الـ 4 روابط، وفي اللوب ربطنا الـ Program والـ VAO بس: نفس الصورة.', {'vertex_array.cpp': c[3]}),
        S('نطبع glGetError', 'كل 10 فريمات: الخطأ 0.', {'vertex_array.cpp': c[4]})], kind='gl', window='Vertex Array', clicks={1: [FK], 2: [FK], 3: [FK], 4: [FK]})
    r2 = F + 'r2_two_methods.cpp'
    d = {2: '93-110,153-160', 3: '112-117,162-173', 4: '147,175-177'}
    P[r2] = Program('d7_r2', {'two_methods.cpp': r2}, [
        S('البيانات والـ Shader', 'الأرقام في الرام ولسه مفيش رسم.', {'two_methods.cpp': rest(r2, set().union(*[rng(v) for v in d.values()]))}),
        S('الطريقة 2: VAO لكل حاجة (شمال)', 'المربع والمثلث في النص الشمال.', {'two_methods.cpp': d[2]}),
        S('الطريقة 1: VAO واحد (يمين)', 'نفس الرسمة يمين، بنفس البكسلات بالظبط.', {'two_methods.cpp': d[3]}),
        S('نطبع glGetError', '', {'two_methods.cpp': d[4]})], kind='gl', window='Two Methods', clicks={1: [FK], 2: [FK], 3: [FK], 4: [FK]})
    m1 = F + 'm1_cross_quiz.py'
    P[m1] = Program('d7_m1', {'cross_quiz.py': m1}, [
        S('cross و check ومثال Khan', '', {'cross_quiz.py': '1-5,15-16,19-22'}),
        S('dot: النتيجة عمودية', '', {'cross_quiz.py': '8-12,23-24'}),
        S('i و j و k والترتيب', '', {'cross_quiz.py': '26-32'})], kind='py')
    m2 = F + 'm2_numpy_cross.py'
    P[m2] = Program('d7_m2', {'numpy_cross.py': m2}, [
        S('np.cross', '', {'numpy_cross.py': '1-2,4-8'}),
        S('متجهين على خط واحد', '', {'numpy_cross.py': '10-11'}),
        S('الـ Normal بتاع مثلث', '', {'numpy_cross.py': '13-17'})], kind='py')
    c1 = F + 'c1_commit_id.py'
    P[c1] = Program('d7_c1', {'commit_id.py': c1}, [
        S('الـ ID بتاع الملف (blob)', 'نفس <code>d088e29</code> اللي ظهر في <code>git diff</code>.', {'commit_id.py': '1-2,5-7,10-12'}),
        S('الـ ID بتاع الفولدر (tree)', 'نفس <code>c298df0</code> اللي في <code>git cat-file</code>.', {'commit_id.py': '14-16'}),
        S('الـ ID بتاع الـ Commit', 'نفس <code>84180e1</code> اللي في <code>git log --oneline</code>.', {'commit_id.py': '18-22'}),
        S('حرف واحد اتغير', 'ID جديد خالص للملف.', {'commit_id.py': '24-25'})], kind='py', run_cwd_extra={'refactored.cpp': F + 'refactored.cpp'})
    return P
