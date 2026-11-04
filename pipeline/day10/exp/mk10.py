import subprocess as sp, os, sys
sys.path.insert(0, '/home/claude/day10')
from glrun import run
os.chdir('/home/claude/day10/exp')
SRC = '/home/claude/day10/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day10/img/'
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

# ---- constructors
variant('p1_constructor.cpp', 'x_no_default', [('''    Entity()
    {
        x = 0.0f;
        y = 0.0f;
        std::cout << "Entity() ran" << std::endl;
    }

''', '')])
variant('p1_constructor.cpp', 'x_log_object', [('    Log::Write("Hello");\n', '    Log::Write("Hello");\n    Log l;\n')])
variant('p1_constructor.cpp', 'x_no_this', [('        this->x = x;\n        this->y = y;\n', '        x = x;\n        y = y;\n')])
# ---- destructors
variant('p2_destructor.cpp', 'd_no_delete', [('    delete heap;\n', '')], valgrind=True)
variant('p2_destructor.cpp', 'd_no_delete_arr', [('        delete[] data;\n', '')], valgrind=True)
variant('p2_destructor.cpp', 'd_ok_valgrind', [], valgrind=True)
# ---- textures
variant('t1_crate.cpp', 't_rgba_for_rgb', [('GLenum format = (channels == 4) ? GL_RGBA : GL_RGB;', 'GLenum format = GL_RGBA;')], gl=True, title='Crate')
variant('t1_crate.cpp', 't_no_tint', [('"    FragColor = texture(tex0, texCoord) * vec4(color, 1.0);\\n"', '"    FragColor = texture(tex0, texCoord);\\n"')], gl=True, title='Crate')
variant('t1_crate.cpp', 't_no_scope', [('    {\n        Texture crate("res/crate.png");\n', '        Texture crate("res/crate.png");\n'), ('        std::cout << "loop ended (Escape)" << std::endl;\n    }\n', '        std::cout << "loop ended (Escape)" << std::endl;\n')], gl=True, title='Crate')
variant('t2_two_textures.cpp', 't_no_unit1', [('    glUniform1i(glGetUniformLocation(shaderProgram, "tex1"), 1);\n', '')], gl=True, title='Two Textures')
variant('t2_two_textures.cpp', 't_amount1', [('"amount"), 0.8f);', '"amount"), 1.0f);'), ('"    FragColor = mix(texture(tex0, texCoord), face, face.a * amount);\\n"', '"    FragColor = mix(texture(tex0, texCoord), face, amount);\\n"')], gl=True, title='Two Textures')
# ---- matrices
variant('m1_matrix_columns.py', 'm_rows', [('A = np.column_stack([T(e1), T(e2)])', 'A = np.vstack([T(e1), T(e2)])')], py=True)
variant('m2_shape_transforms.py', 'm_transposed', [('    moved = (A @ F.T).T', '    moved = (A.T @ F.T).T'), ('plt.savefig("shapes.png", dpi=110)', 'plt.savefig("/home/claude/day10/img/m_transposed.png", dpi=110)')], py=True)
# ---- B-Rep
variant('c1_brep_cylinder.cpp', 'b_no_seam_back', [('{ 2, false }, { 1, true } }', '{ 2, false } }')])
variant('c2_brep_hole.cpp', 'h_no_inner', [('{ { { 0, 3, 2, 1 }, { 8, 9, 10, 11 } } },', '{ { { 0, 3, 2, 1 } } },'), ('{ { { 4, 5, 6, 7 }, { 12, 15, 14, 13 } } },', '{ { { 4, 5, 6, 7 } } },')])
