import subprocess as sp, os
os.chdir('/home/claude/day4/exp')
SRC = '/home/claude/day4/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
ONCE = '\n        static bool once = true;\n        if (once) { std::cout << "glGetError = " << glGetError() << std::endl; once = false; }'
def variant(base, name, reps, gl=False, extra_files=()):
    s = open(SRC + base).read()
    for a, b in reps:
        assert a in s, (name, a); s = s.replace(a, b, 1)
    fn = name + '.cpp'; open(fn, 'w').write(s)
    r = sp.run(['g++', '-Wall', fn, *extra_files, '-o', name] + (GL if gl else []), capture_output=True, text=True)
    open(name + '.build', 'w').write(r.stdout + r.stderr)
    if r.returncode == 0 and not gl:
        r2 = sp.run(['./' + name], input='\n', capture_output=True, text=True, timeout=20)
        open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n')
    print(name, 'built' if r.returncode == 0 else 'BUILD FAILED')
def multi(name, files):
    d = name; os.makedirs(d, exist_ok=True)
    for fn, txt in files.items(): open(f'{d}/{fn}', 'w').write(txt)
    cpps = [f'{d}/{f}' for f in files if f.endswith('.cpp')]
    r = sp.run(['g++', '-Wall', *cpps, '-o', f'{d}/prog'], capture_output=True, text=True)
    open(name + '.build', 'w').write(r.stdout + r.stderr)
    if r.returncode == 0:
        r2 = sp.run([f'./{d}/prog'], input='\n', capture_output=True, text=True)
        open(name + '.out', 'w').write(r2.stdout)
    print(name, 'built' if r.returncode == 0 else 'LINK/BUILD FAILED')
S1 = SRC + 'st1/'; S2 = SRC + 'st2/'
rd = lambda p: open(p).read()
# ---- static
multi('st_conflict', {'main.cpp': rd(S1 + 'main.cpp'), 'static.cpp': rd(S1 + 'static.cpp').replace('static int s_Variable', 'int s_Variable')})
multi('st_func_conflict', {'main.cpp': rd(S1 + 'main.cpp'), 'static.cpp': rd(S1 + 'static.cpp').replace('static void Function', 'void Function')})
multi('st_extern_static', {'main.cpp': rd(S2 + 'main.cpp'), 'static.cpp': 'static int s_Variable = 5;\n'})
multi('st_header', {'counter.h': 'static int s_Counter = 0;\n',
   'other.cpp': '#include <iostream>\n#include "counter.h"\n\nvoid AddFromOther()\n{\n    s_Counter++;\n    std::cout << "other.cpp: s_Counter = " << s_Counter << std::endl;\n}\n',
   'main.cpp': '#include <iostream>\n#include "counter.h"\n\nvoid AddFromOther();\n\nint main()\n{\n    s_Counter++;\n    std::cout << "main.cpp:  s_Counter = " << s_Counter << std::endl;\n    AddFromOther();\n}\n'})
# ---- const
variant('c1_const_pointers.cpp', 'c_max_age', [('    std::cout << "MAX_AGE = "', '    MAX_AGE = 100;\n    std::cout << "MAX_AGE = "')])
variant('c1_const_pointers.cpp', 'c_b_content', [('    b = &MAX_AGE;\n', '    b = &MAX_AGE;\n    *b = 2;\n')])
variant('c1_const_pointers.cpp', 'c_c_pointer', [('    *c = 2;\n', '    *c = 2;\n    c = nullptr;\n')])
variant('c1_const_pointers.cpp', 'c_d_both', [('    const int* const d = &MAX_AGE;\n', '    const int* const d = &MAX_AGE;\n    *d = 2;\n    d = nullptr;\n')])
variant('c2_const_method.cpp', 'c_no_const_method', [('    int GetX() const\n', '    int GetX()\n')])
variant('c2_const_method.cpp', 'c_no_mutable', [('    mutable int m_DebugCount = 0;', '    int m_DebugCount = 0;')])
# ---- cross
variant('x1_cross_khan.cpp', 'x_middle_not_reversed', [('a.z * b.x - a.x * b.z', 'a.x * b.z - a.z * b.x')])
# ---- EBO (GL)
variant('e2_rect_indices.cpp', 'e_gl_int', [('GL_UNSIGNED_INT, nullptr);', 'GL_INT, nullptr);' + ONCE)], gl=True)
variant('e2_rect_indices.cpp', 'e_count3', [('glDrawElements(GL_TRIANGLES, 6,', 'glDrawElements(GL_TRIANGLES, 3,')], gl=True)
variant('e2_rect_indices.cpp', 'e_wrong_indices', [('        2, 3, 0\n', '        2, 3, 1\n')], gl=True)
variant('e2_rect_indices.cpp', 'e_unbind_ibo', [('    unsigned int shader = CreateShader', '    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);\n\n    unsigned int shader = CreateShader'),
                                               ('GL_UNSIGNED_INT, nullptr);', 'GL_UNSIGNED_INT, nullptr);' + ONCE)], gl=True)
variant('e2_rect_indices.cpp', 'e_unbind_vbo', [('    unsigned int ibo;\n', '    glBindBuffer(GL_ARRAY_BUFFER, 0);\n\n    unsigned int ibo;\n')], gl=True)
# ---- VAO
NOVAO = [('    unsigned int vao;\n    glGenVertexArrays(1, &vao);\n    glBindVertexArray(vao);\n\n', '')]
variant('e2_rect_indices.cpp', 'v_no_vao_core', NOVAO + [('GL_UNSIGNED_INT, nullptr);', 'GL_UNSIGNED_INT, nullptr);' + ONCE)], gl=True)
variant('e2_rect_indices.cpp', 'v_no_vao_compat', NOVAO + [('    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);\n    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);\n    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);\n', ''),
    ('GL_UNSIGNED_INT, nullptr);', 'GL_UNSIGNED_INT, nullptr);' + ONCE)], gl=True)
variant('v1_two_vaos.cpp', 'v_no_sun_bind', [('        glBindVertexArray(sunVao);\n', '')], gl=True)
variant('v2_polylines.cpp', 'p_lines_not_strip', [('glDrawArrays(GL_LINE_STRIP, line.first, line.count);', 'glDrawArrays(GL_LINES, line.first, line.count);')], gl=True)
variant('v2_polylines.cpp', 'p_no_first_polyline', [('    polylines.push_back({ 0, 0 });\n', '')], gl=True)
