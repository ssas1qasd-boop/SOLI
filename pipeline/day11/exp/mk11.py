import subprocess as sp, os, sys
sys.path.insert(0, '/home/claude/day11')
from glrun import run
os.chdir('/home/claude/day11/exp')
SRC = '/home/claude/day11/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day11/img/'
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

# ---- stack vs heap
variant('p1_stack_heap.cpp', 'x_no_delete_arr', [('    delete[] harray;\n', '')], valgrind=True)
variant('p1_stack_heap.cpp', 'x_delete_not_arr', [('    delete[] harray;\n', '    delete harray;\n')], valgrind=True)
variant('p1_stack_heap.cpp', 'x_ok_valgrind', [], valgrind=True)
variant('p2_speed_size.cpp', 's_million', [('const int N = 100;', 'const int N = 1000000;')])
variant('p2_speed_size.cpp', 's_no_delete_loop', [('        delete v;\n', '')], valgrind=True)
variant('p2_speed_size.cpp', 's_stack_texture', [('    unsigned char* pixels = new unsigned char[width * height * 4];\n', '    unsigned char pixels[2048 * 2048 * 4];\n')])
# ---- textures
variant('t1_wrap_by_hand.cpp', 'w_int_floor', [('"        return uv - floor(uv);\\n"', '"        return uv - vec2(ivec2(uv));\\n"')], gl=True, title='Wrap by hand')
variant('t1_wrap_by_hand.cpp', 'w_mirror_no_one', [('"        return 1.0 - abs(mod(uv, 2.0) - 1.0);\\n"', '"        return abs(mod(uv, 2.0) - 1.0);\\n"')], gl=True, title='Wrap by hand')
variant('t1_wrap_by_hand.cpp', 'w_repeat_sampler', [('                letter.SetWrap(GL_CLAMP_TO_EDGE);\n', '                letter.SetWrap(GL_REPEAT);\n')], gl=True, title='Wrap by hand')
variant('t2_procedural.cpp', 'p_no_unpack', [('    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);\n', '')], gl=True, title='Procedural')
variant('t2_procedural.cpp', 'p_linear', [('glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);', 'glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);')], gl=True, title='Procedural')
# ---- matrices
variant('m1_add_subtract.py', 'm_broadcast', [('F = np.array([[5, 7], [-1, 0]])', 'F = np.array([[5, 7]])')], py=True)
variant('m2_move_shape.py', 'm_flat_move', [('move = np.array([[3, 1]] * 6, dtype=float)', 'move = np.array([3, 1] * 6, dtype=float)')], py=True)
# ---- CAD
variant('c1_obj_cube.cpp', 'o_flip_bottom', [('f 1 4 3 2\\n', 'f 1 2 3 4\\n')])
variant('c1_obj_cube.cpp', 'o_one_based', [('                f.push_back(index - 1);\n', '                f.push_back(index);\n')], flags=('-D_GLIBCXX_ASSERTIONS',))
variant('c2_mesh_vs_brep.cpp', 'b_no_modulo', [('        int j = (i + 1) % n;\n', '        int j = i + 1;\n')])
