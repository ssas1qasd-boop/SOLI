import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d5 import rest, rng
F = '/home/claude/day14/src/'


def U(p, d): return rest(p, set().union(*[rng(v) for v in d.values()]))


def programs():
    P = {}
    p1 = F + 'p1_copy_basics.cpp'
    a = {2: '15-18', 3: '20-24', 4: '26-29'}
    P[p1] = Program('d14_p1', {'copy_basics.cpp': p1}, [
        S('نسخ int', 'a = 2، b = 3.', {'copy_basics.cpp': U(p1, a)}),
        S('نسخ struct', 'va.x لسه 2، وعنوانين مختلفين.', {'copy_basics.cpp': a[2]}),
        S('نسخ Pointer', 'الاتنين 5، و pa == pb: yes.', {'copy_basics.cpp': a[3]}),
        S('Reference', 'va.y = 9، و sizeof 8 و 8.', {'copy_basics.cpp': a[4]})])
    p2 = F + 'p2_string.cpp'
    b = {2: '19-25,37-40,64-67', 3: '51-54,69-70', 4: '56-59,71-72'}
    P[p2] = Program('d14_p2', {'string.cpp': p2}, [
        S('String بإيدنا', 'مفيش طباعة: String واحد اتعمل.', {'string.cpp': U(p2, b)}),
        S('Copy Constructor', 'Copied!، و Cherno / Charno، وعنوانين مختلفين.', {'string.cpp': b[2]}),
        S('بالقيمة', 'Copied! قبل كل by value.', {'string.cpp': b[3]}),
        S('بالـ const reference', 'by const reference من غير Copied!.', {'string.cpp': b[4]})])
    t1 = F + 't1_texture_copy.cpp'
    c = {2: '80-83,133-134'}
    P[t1] = Program('d14_t1', {'texture_copy.cpp': t1}, [
        S('Texture class: أحمر وأزرق', 'id 1 و id 2، والشباك أحمر وأزرق.', {'texture_copy.cpp': U(t1, c)}),
        S('Describe بالقيمة', '~Texture deletes id 2 بدري، و glIsTexture = 0، والاتنين أحمر.', {'texture_copy.cpp': c[2]})],
        kind='gl', window='Texture copy')
    t2 = F + 't2_texture_ref.cpp'
    d = {2: '68,82-85,135-136'}
    P[t2] = Program('d14_t2', {'texture_ref.cpp': t2}, [
        S('نفس الـ Texture class', 'أحمر وأزرق.', {'texture_ref.cpp': U(t2, d)}),
        S('= delete و const Texture&', 'glIsTexture = 1 للاتنين، والأزرق فضل أزرق.', {'texture_ref.cpp': d[2]})],
        kind='gl', window='Texture reference')
    m1 = F + 'm1_image_area.py'
    P[m1] = Program('d14_m1', {'image_area.py': m1}, [
        S('صورة المربع تحت A', 'الأركان (0, 0) و (2, 0) و (3, 1) و (1, 1).', {'image_area.py': '1-10'}),
        S('المساحة و det', '1 ← 2، و det = 2.', {'image_area.py': '13-18'}),
        S('B بتكبس المربع', 'المساحة 0 و det 0.', {'image_area.py': '20-23'}),
        S('الرسمة', 'اتحفظت image_area.png.', {'image_area.py': '25-37'})], kind='py')
    m2 = F + 'm2_inverse.py'
    P[m2] = Program('d14_m2', {'inverse.py': m2}, [
        S('العكس بإيدنا', 'det 2، و [[0.5, ‎-0.5], [0, 1]]، و A @ inverse = I.', {'inverse.py': '1-10'}),
        S('روح وارجع', '(4, 2) ← (1, 2).', {'inverse.py': '12-14'}),
        S('حل A x = b', 'x = (1, 3).', {'inverse.py': '16-19'}),
        S('مصفوفة مالهاش عكس', 'Singular matrix.', {'inverse.py': '21-27'})], kind='py')
    c1 = F + 'c1_git_record.py'
    P[c1] = Program('d14_c1', {'git_record.py': c1}, [
        S('git init', 'empty repository made.', {'git_record.py': '1-22'}),
        S('add و commit', '?? ثم A.', {'git_record.py': '24-28'}),
        S('3 تعديلات', 'M و diff (من غير طباعة باقي اللفات).', {'git_record.py': '30-35'}),
        S('log والرجوع للأصل', '4 commits، و site.css رجع blue.', {'git_record.py': '37-42'})], kind='py')
    c2 = F + 'c2_git_store.py'
    P[c2] = Program('d14_c2', {'git_store.py': c2}, [
        S('البصمة بإيدنا', '7614dc7c…', {'git_store.py': '1-16'}),
        S('git hash-object', 'نفس البصمة.', {'git_store.py': '18-23'}),
        S('3 ملفات و 2 objects', 'a.css و copy_v2.css نفس البصمة.', {'git_store.py': '25-36'})], kind='py')
    return P
