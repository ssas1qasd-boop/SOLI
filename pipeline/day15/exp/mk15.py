import subprocess as sp, os, sys
sys.path.insert(0, '/home/claude/day15')
from glrun import run
os.chdir('/home/claude/day15/exp')
SRC = '/home/claude/day15/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day15/img/'
ONLY = sys.argv[1:]
def variant(base, name, reps, gl=False, title=None, py=False, timeout=5, flags=(), valgrind=False):
    if ONLY and name not in ONLY: return
    s = open(SRC + base).read()
    for a, b in reps:
        assert a in s, (name, a); s = s.replace(a, b, 1)
    ext = '.py' if py else '.cpp'
    fn = name + ext; open(fn, 'w').write(s)
    if py:
        r2 = sp.run(['python3', fn], capture_output=True, text=True, timeout=30)
        open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n'); print(name, 'ran', r2.returncode); return
    r = sp.run(['g++', '-Wall', *flags, fn, '-o', name] + (['stb.o'] if 'stb_image' in s else []) + (GL if gl else []), capture_output=True, text=True)
    open(name + '.build', 'w').write('\n'.join(l for l in (r.stdout + r.stderr).splitlines() if 'stb_image.h' not in l))
    if r.returncode == 0 and not gl:
        cmd = (['valgrind', '--leak-check=full', '--error-exitcode=0'] if valgrind else []) + ['./' + name]
        r2 = sp.run(cmd, capture_output=True, text=True, timeout=timeout * (6 if valgrind else 1))
        open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n')
    if r.returncode == 0 and gl:
        p = run('./' + name, title, name + '.out', name, I)
        if p is False: open(name + '.out', 'a').write('\n(window did not close on Escape)\n')
        st = sp.run(['true']); 
    print(name, 'built' if r.returncode == 0 else 'BUILD FAILED')

variant('p1_print_template.cpp', 'tp_call_broken', [('    std::cout << "NeverCalled has a mistake inside', '    NeverCalled(5);\n    std::cout << "NeverCalled has a mistake inside')])
variant('p1_print_template.cpp', 'tp_mixed_types', [('<< Biggest(2.5, 1.5) <<', '<< Biggest(3, 1.5) <<')])
variant('p2_array_template.cpp', 'ar_runtime_size', [('    Array<int, 5> numbers;\n', '    int n = 5;\n    Array<int, n> numbers;\n')])
variant('p2_array_template.cpp', 'ar_out_of_range', [('        numbers[i] = i * 10;\n', '        numbers[i] = i * 10;\n    numbers[5] = 99;\n')], flags=('-fsanitize=address', '-g'))
variant('t1_transform2d.cpp', 'tr_wrong_order', [('Multiply(Translate(0.45f, 0.4f), Multiply(Rotate(90), Translate(-0.45f, -0.4f)))', 'Multiply(Translate(-0.45f, -0.4f), Multiply(Rotate(90), Translate(0.45f, 0.4f)))')], gl=True, title='Transform 2D')
variant('t1_transform2d.cpp', 'tr_no_transpose', [('glUniformMatrix3fv(matLoc, 1, GL_TRUE, &shapes[i].m[0][0]);', 'glUniformMatrix3fv(matLoc, 1, GL_FALSE, &shapes[i].m[0][0]);')], gl=True, title='Transform 2D')
variant('t2_homogeneous.cpp', 'hm_direction_w1', [('    Vec3 direction = { 1, 0, 0 };', '    Vec3 direction = { 1, 0, 1 };')])
variant('m1_composition.py', 'm_star', [('composition = shear @ rotation', 'composition = shear * rotation')], py=True)
variant('c1_translate4x4.cpp', 'c_bottom_row', [('return { { { 1, 0, 0, tx }, { 0, 1, 0, ty }, { 0, 0, 1, tz }, { 0, 0, 0, 1 } } };', 'return { { { 1, 0, 0, 0 }, { 0, 1, 0, 0 }, { 0, 0, 1, 0 }, { tx, ty, tz, 1 } } };')])
