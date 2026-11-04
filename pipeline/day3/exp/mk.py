import subprocess as sp, sys, os
os.chdir('/home/claude/day3/exp')
SRC = '/home/claude/day3/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
def variant(base, name, reps, ext=None, flags=(), gl=False, c=False):
    s = open(SRC + base).read()
    for a, b in reps:
        assert a in s, (name, a); s = s.replace(a, b, 1)
    ext = ext or os.path.splitext(base)[1]
    fn = name + ext
    open(fn, 'w').write(s)
    cmd = (['gcc', '-Wall'] if c else ['g++', '-Wall']) + list(flags) + [fn, '-o', name] + (GL if gl else [])
    r = sp.run(cmd, capture_output=True, text=True)
    open(name + '.build', 'w').write(r.stdout + r.stderr)
    ok = r.returncode == 0
    if ok and not gl:
        r2 = sp.run(['./' + name], input='\n', capture_output=True, text=True, timeout=20)
        open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n')
    print(name, 'built' if ok else 'BUILD FAILED')
A = ['-fsanitize=address', '-g']
# References
variant('r1_reference.cpp', 'r_no_init', [('int& ref = a;', 'int& ref;')])
variant('r2_increment.cpp', 'r_star_pp', [('(*value)++;', '*value++;')])
variant('r2_increment.cpp', 'r_literal', [('IncrementReference(a);', 'IncrementReference(5);')])
variant('r2_increment.cpp', 'r_const_literal', [('void IncrementReference(int& value)', 'void IncrementReference(const int& value)')])
variant('r2_increment.cpp', 'r_nullptr', [('IncrementPointer(&a);', 'IncrementPointer(nullptr);')])
variant('r4_cherno.cpp', 'r_no_define', [('#define LOG(x) std::cout << x << std::endl\n', '')])
variant('r4_cherno.cpp', 'r_no_amp', [('void Increment(int& value)', 'void Increment(int value)')])
# Hamming
variant('h1_hamming.c', 'h_no_end_check', [("while (lhs[i] != '\\0' && rhs[i] != '\\0')", "while (lhs[i] != '\\0')")], flags=A, c=True)
variant('h1_hamming.c', 'h_no_len_check', [("    if (lhs[i] != rhs[i])\n        return -1;\n\n", "")], c=True)
variant('h1_hamming.c', 'h_write_const', [("    int distance = 0;\n", "    int distance = 0;\n    lhs[0] = 'X';\n")], c=True)
# Cross
variant('x1_cross.cpp', 'x_wrong_sign', [('v.z * w.x - v.x * w.z', 'v.x * w.z - v.z * w.x'),
  ('Vec3 v = { 0, 0, 2 };', 'Vec3 v = { 1, 2, 3 };'), ('Vec3 w = { 0, 2, 0 };', 'Vec3 w = { 4, 5, 6 };')])
variant('x1_cross.cpp', 'x_right_123', [('Vec3 v = { 0, 0, 2 };', 'Vec3 v = { 1, 2, 3 };'), ('Vec3 w = { 0, 2, 0 };', 'Vec3 w = { 4, 5, 6 };')])
variant('x1_cross.cpp', 'x_parallel', [('Vec3 w = { 0, 2, 0 };', 'Vec3 w = { 0, 0, 5 };')])
# Shader file
variant('s1_shader_file.cpp', 's_wrong_path', [('"res/shaders/Basic.shader"', '"res/shader/Basic.shader"')], gl=True)
variant('s1_shader_file.cpp', 's_no_newline', [("ss[(int)type] << line << '\\n';", "ss[(int)type] << line;")], gl=True)
variant('s1_shader_file.cpp', 's_no_cast', [("ss[(int)type] << line << '\\n';", "ss[type] << line << '\\n';")], gl=True)
variant('s1_shader_file.cpp', 's_no_header_asan', [('"res/shaders/Basic.shader"', '"res/shaders/NoHeader.shader"')], gl=True, flags=A)
variant('s1_shader_file.cpp', 's_typo', [('"res/shaders/Basic.shader"', '"res/shaders/Typo.shader"')], gl=True)
variant('s1_shader_file.cpp', 's_delete_shader', [('    glDeleteProgram(shader);\n', '    glDeleteShader(shader);\n    std::cout << "glGetError = " << glGetError() << std::endl;\n')], gl=True)
# CAD
variant('l2_click_lines.cpp', 'l_no_flip', [('float y = (float)(1.0 - 2.0 * py / height);', 'float y = (float)(2.0 * py / height - 1.0);')], gl=True)
variant('l2_click_lines.cpp', 'l_static', [('GL_DYNAMIC_DRAW', 'GL_STATIC_DRAW')], gl=True)
variant('l2_click_lines.cpp', 'l_no_sizeof', [('points.size() * sizeof(float)', 'points.size()')], gl=True)
variant('l1_line.cpp', 'l_width', [('    glPointSize(12.0f);\n', '    glPointSize(12.0f);\n    glLineWidth(5.0f);\n    std::cout << "glGetError = " << glGetError() << std::endl;\n')], gl=True)
variant('l1_line.cpp', 'l_no_pointsize', [('    glPointSize(12.0f);\n', '')], gl=True)
