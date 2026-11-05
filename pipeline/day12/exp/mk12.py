import subprocess as sp, os, sys
sys.path.insert(0, '/home/claude/day12')
from glrun import run
os.chdir('/home/claude/day12/exp')
SRC = '/home/claude/day12/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day12/img/'
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

# ---- new
variant('p1_new.cpp', 'n_delete_no_arr', [('    delete[] entities;\n', '    delete entities;\n')])
variant('p1_new.cpp', 'n_malloc_name', [('    std::cout << "malloc(sizeof(Entity)): no \\"Entity() ran\\" above this line" << std::endl;\n', '    std::cout << "m->name = " << m->name << std::endl;\n')])
variant('p1_new.cpp', 'n_no_delete', [('    delete e;\n', '')], valgrind=True)
variant('p2_placement.cpp', 'pl_no_dtor', [('    v->~Vector3();\n', '')])
variant('p2_placement.cpp', 'pl_delete_v', [('    v->~Vector3();\n    delete[] b;\n', '    v->~Vector3();\n    delete v;\n    delete[] b;\n')])
# ---- mipmaps
variant('t1_mipmaps.cpp', 'mm_no_generate', [('    glGenerateMipmap(GL_TEXTURE_2D);\n', '')], gl=True, title='Mipmaps')
variant('t1_mipmaps.cpp', 'mm_mag_mipmap', [('glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilters[i]);', 'glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilters[i]);\n            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR_MIPMAP_LINEAR);\n            static bool once = true; if (glGetError() != GL_NO_ERROR && once) { once = false; std::cout << "MAG_FILTER = LINEAR_MIPMAP_LINEAR: GL_INVALID_ENUM" << std::endl; }')], gl=True, title='Mipmaps')
variant('t2_mip_levels.cpp', 'lv_missing_last', [('for (int level = 0, w = SIZE; w >= 1; level++, w /= 2)', 'for (int level = 0, w = SIZE; w >= 2; level++, w /= 2)')], gl=True, title='Mip levels')
# ---- numpy
variant('m1_numpy_arrays.py', 'm_wrong_len', [('m[:, 2] = [1, 2]', 'm[:, 2] = [1, 2, 3]')], py=True)
variant('m1_numpy_arrays.py', 'm_int_float', [('z[1, 1] = 9', 'z[1, 1] = 9\nm[0, 0] = 2.7\nprint("m[0, 0] = 2.7 -> m[0, 0] =", m[0, 0])')], py=True)
variant('m2_numpy_math.py', 'm_matmul_shape', [('print(np.matmul(ones, twos))', 'print(np.matmul(ones, ones))')], py=True)
# ---- CAD
variant('c2_three_models.cpp', 'c_wrong_sign', [('{ { -1, 0, 0 }, 1 }', '{ { 1, 0, 0 }, 1 }')])
variant('c2_three_models.cpp', 'c_eleven_edges', [('    for (auto& e : edges)\n', '    for (int i = 0; i < 11; i++)\n    {\n        auto& e = edges[i];\n'), ('        wire += Length(v[e[0]], v[e[1]]);\n', '        wire += Length(v[e[0]], v[e[1]]);\n    }\n')])
