import sys
sys.path.insert(0, '/home/claude/steps')
from engine import Program
from specs_d1 import S
from specs_d5 import rest, rng
F = '/home/claude/day8/src/'
TEX = {'stb_image.h': F + 'stb_image.h', 'res/logo.png': F + 'res/logo.png'}


def U(p, d): return rest(p, set().union(*[rng(v) for v in d.values()]))


def programs():
    P = {}
    p1 = F + 'p1_player.cpp'
    a = {2: '9-13,30-31', 3: '16-20,33-34', 4: '36-42', 5: '44-48'}
    P[p1] = Program('d8_p1', {'player.cpp': p1}, [
        S('الكلاس والـ Object', 'Object واحد في الرام: x = 0 و y = 0.', {'player.cpp': U(p1, a)}),
        S('Method جوه الكلاس', '<code>player.Move(1, -1)</code>: x = 2 و y = ‎-2.', {'player.cpp': a[2]}),
        S('نفس الحركة بدالة برّه', 'بنبعت player بالـ Reference: 4 و ‎-4.', {'player.cpp': a[3]}),
        S('Object تاني', 'enemy اتحرك، و player زي ما هو.', {'player.cpp': a[4]}),
        S('الـ Object في الرام', '12 بايت، والمتغيرات جنب بعض.', {'player.cpp': a[5]})])
    p2 = F + 'p2_counter.cpp'
    b = {2: '14-18,35-37', 3: '25-28,40-41', 4: '43-48'}
    P[p2] = Program('d8_p2', {'counter.cpp': p2}, [
        S('عداد private', 'Reset و Get بس: العداد 0.', {'counter.cpp': U(p2, b)}),
        S('Add بشرط', '3 + 4 = 7، والسالب اترفض.', {'counter.cpp': b[2]}),
        S('this', '<code>this</code> = <code>&amp;clicks</code>.', {'counter.cpp': b[3]}),
        S('Object تاني', 'عداد لوحده، و this = <code>&amp;other</code>.', {'counter.cpp': b[4]})])
    t1 = F + 't1_texture.cpp'
    c = {2: '6-7,53-80,173-177,199', 3: '82-86,132-133,144,146,151,159-160,164,179-181', 4: '170-171,183'}
    P[t1] = Program('d8_t1', {'texture.cpp': t1}, [
        S('الشباك والمربع', 'الشاشة سودا: المربع اترسم، بس الـ Fragment لسه مش بيحط لون، فطلع أسود على أسود.', {'texture.cpp': U(t1, c)}),
        S('نحمّل الصورة للكارت', 'اتحمّلت 128 × 128، بس الـ Shader لسه مش بيقرا منها.', {'texture.cpp': c[2]}),
        S('الإحداثيات والخانة والـ Shader', 'الصورة على المربع. الأماكن الشفافة لسه بلونها (أسود)، ومش باينة لأن الخلفية كمان سودا.', {'texture.cpp': c[3]}),
        S('الشفافية (Blending)', 'خلفية زرقا: دلوقتي باين إن الأماكن الشفافة شفافة فعلاً.', {'texture.cpp': c[4]})], kind='gl', window='Texture', run_cwd_extra=TEX)
    t2 = F + 't2_settings.cpp'
    d = {2: '181-184', 3: '186-190', 4: '192-195'}
    P[t2] = Program('d8_t2', {'texture_settings.cpp': t2}, [
        S('الخانة 0: NEAREST', 'فوق شمال: مربعات حادة.', {'texture_settings.cpp': U(t2, d)}),
        S('الخانة 1: LINEAR', 'فوق يمين: ناعمة.', {'texture_settings.cpp': d[2]}),
        S('REPEAT من 0 لـ 2', 'تحت شمال: الصورة اتكررت.', {'texture_settings.cpp': d[3]}),
        S('CLAMP_TO_EDGE من 0 لـ 2', 'تحت يمين: الحافة اتمدت.', {'texture_settings.cpp': d[4]})], kind='gl', window='Texture Settings')
    m1 = F + 'm1_matrix_columns.py'
    P[m1] = Program('d8_m1', {'matrix_columns.py': m1}, [
        S('الأعمدة ومثال الفيديو', '[5, 2].', {'matrix_columns.py': '1-5,8-9,12-13,15-19'}),
        S('الدوران', '', {'matrix_columns.py': '21-24'}),
        S('القص', '', {'matrix_columns.py': '26-29'}),
        S('الكبس على خط', '', {'matrix_columns.py': '31-34'})], kind='py')
    m2 = F + 'm2_numpy_grid.py'
    P[m2] = Program('d8_m2', {'numpy_grid.py': m2}, [
        S('M @ v والأعمدة', '', {'numpy_grid.py': '1-4,6-10'}),
        S('مربع الوحدة', '', {'numpy_grid.py': '12-14'}),
        S('تحويلين في مصفوفة', '', {'numpy_grid.py': '16-21'}),
        S('نرسم الشبكة', 'اتحفظت grids.png.', {'numpy_grid.py': '23-35,38-45'})], kind='py')
    c1 = F + 'c1_brep.cpp'
    e = {2: '70-76', 3: '78-81', 4: '83-87'}
    P[c1] = Program('d8_c1', {'brep.cpp': c1}, [
        S('الكلاسات والمكعب', '6 − 12 + 8 = 2.', {'brep.cpp': U(c1, e)}),
        S('الهرم', '5 − 8 + 5 = 2.', {'brep.cpp': e[2]}),
        S('مكعب من غير غطا', 'أويلر 1 و 4 أضلاع مكشوفة.', {'brep.cpp': e[3]}),
        S('الـ Topology', 'أضلاع الوش القدام.', {'brep.cpp': e[4]})])
    c2 = F + 'c2_wireframe.cpp'
    g = {2: '81-93,121-134,179-181', 3: '171,182-183', 4: '95-101,136-144,185-187'}
    P[c2] = Program('d8_c2', {'wireframe.cpp': c2}, [
        S('الـ B-Rep والشباك', 'الشباك فاضي.', {'wireframe.cpp': U(c2, g)}),
        S('الأضلاع خطوط', '12 خط.', {'wireframe.cpp': g[2]}),
        S('الأركان نقط', '8 نقط زرقا.', {'wireframe.cpp': g[3]}),
        S('الوش القدام', '4 خطوط برتقاني.', {'wireframe.cpp': g[4]})], kind='gl', window='B-Rep Wireframe')
    return P
