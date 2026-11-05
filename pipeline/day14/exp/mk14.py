import subprocess as sp, os, sys
sys.path.insert(0, '/home/claude/day14')
from glrun import run
os.chdir('/home/claude/day14/exp')
SRC = '/home/claude/day14/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day14/img/'
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

# ---- copying
variant('p1_copy_basics.cpp', 'cp_delete_both', [('    delete pa;\n', '    delete pa;\n    delete pb;\n')])
variant('p2_string.cpp', 's_shallow', [('''    String(const String& other)
        : m_Size(other.m_Size)
    {
        std::cout << "Copied!" << std::endl;
        m_Buffer = new char[m_Size + 1];
        memcpy(m_Buffer, other.m_Buffer, m_Size + 1);
    }

''', '')])
variant('p2_string.cpp', 's_copy_deleted', [('''    String(const String& other)
        : m_Size(other.m_Size)
    {
        std::cout << "Copied!" << std::endl;
        m_Buffer = new char[m_Size + 1];
        memcpy(m_Buffer, other.m_Buffer, m_Size + 1);
    }
''', '''    String(const String& other) = delete;
''')])
# ---- textures
variant('t1_texture_copy.cpp', 'tc_bind_error', [('            textures[i]->Bind();\n', '            textures[i]->Bind();\n            static int shown = 0;\n            GLenum error = glGetError();\n            if (shown++ < 2)\n                std::cout << "Bind id " << textures[i]->id << ": glGetError = " << error << (error == GL_INVALID_OPERATION ? " (GL_INVALID_OPERATION)" : "") << std::endl;\n')], gl=True, title='Texture copy')
variant('t2_texture_ref.cpp', 'tr_try_copy', [('    Describe(blue);\n', '    Describe(blue);\n    Texture copy = blue;\n')], gl=True, title='Texture reference')
# ---- math
variant('m1_image_area.py', 'm_corner_order', [('square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)', 'square = np.array([[0, 0], [1, 1], [1, 0], [0, 1]], dtype=float)')], py=True)
variant('m2_inverse.py', 'm_inverse_singular', [('A = np.array([[2.0, 1.0], [0.0, 1.0]])', 'A = np.array([[1.0, 2.0], [2.0, 4.0]])')], py=True)
# ---- git
variant('c1_git_record.py', 'g_no_add', [('git("add", "site.css")\n', '')], py=True)
variant('c2_git_store.py', 'g_no_header', [('by_hand = hashlib.sha1(header + content).hexdigest()', 'by_hand = hashlib.sha1(content).hexdigest()')], py=True)
