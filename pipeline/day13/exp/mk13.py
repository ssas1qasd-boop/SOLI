import subprocess as sp, os, sys
sys.path.insert(0, '/home/claude/day13')
from glrun import run
os.chdir('/home/claude/day13/exp')
SRC = '/home/claude/day13/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day13/img/'
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

# ---- lifetime
variant('p1_lifetime.cpp', 'lf_return_stack', [('    int* array = new int[50];\n', '    int array[50];\n'), ('    delete[] fromHeap;\n', '')])
variant('p1_lifetime.cpp', 'lf_delete_heap', [('        std::cout << "end of the scope with new: " << h->name << " is still alive" << std::endl;\n', '        std::cout << "end of the scope with new: " << h->name << " is still alive" << std::endl;\n        delete h;\n')])
variant('p2_scoped_ptr.cpp', 'sp_copy', [('        ScopedPtr e = new Entity();\n', '        ScopedPtr e = new Entity();\n        ScopedPtr e2 = e;\n')])
variant('p2_scoped_ptr.cpp', 'sp_no_delete', [('        delete m_Ptr;\n', '')], valgrind=True)
# ---- textures
variant('t1_gpu_copy.cpp', 'g_free_before', [('        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);\n        stbi_image_free(data);\n', '        stbi_image_free(data);\n        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);\n')], gl=True, title='GPU copy')
variant('t1_gpu_copy.cpp', 'g_no_unpack', [('        glPixelStorei(GL_UNPACK_ALIGNMENT, 1);\n', '')], gl=True, title='GPU copy')
variant('t2_atlas.cpp', 'a_int_divide', [('            u0 = (float)col / CELLS;\n            v0 = (float)row / CELLS;\n', '            u0 = col / CELLS;\n            v0 = row / CELLS;\n')], gl=True, title='Atlas')
variant('t2_atlas.cpp', 'a_swap_rowcol', [('            v0 = (float)row / CELLS;\n', '            v0 = (float)col / CELLS;\n'), ('int pick[4] = { 0, 5, 10, 15 };', 'int pick[4] = { 1, 6, 11, 12 };')], gl=True, title='Atlas')
# ---- math
variant('m1_rotate_compose.py', 'm_no_radians', [('    t = np.radians(degrees)\n', '    t = degrees\n')], py=True)
variant('m2_rotate3d_project.py', 'm_no_divide', [('P = np.outer(u, u) / (u @ u)', 'P = np.outer(u, u)')], py=True)
# ---- CAD
variant('c1_csg.cpp', 'c_or_not', [('    return InSphere(p) && !InBox(p);\n', '    return InSphere(p) || !InBox(p);\n')])
variant('c2_regularized.cpp', 'c_keep_zero', [('        if (p.b > p.a)\n', '        if (p.b >= p.a)\n')])
