import subprocess as sp, os, sys
sys.path.insert(0, '/tmp/claude-0')
from gl3 import run
os.chdir('/home/claude/day6/exp')
SRC = '/home/claude/day6/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day6/img/'
def variant(base, name, reps, gl=False, stdin='\n', title=None, clicks=(), py=False, timeout=5):
    s = open(SRC + base).read()
    for a, b in reps:
        assert a in s, (name, a); s = s.replace(a, b, 1)
    ext = '.py' if py else '.cpp'
    fn = name + ext; open(fn, 'w').write(s)
    if py:
        r2 = sp.run(['python3', fn], capture_output=True, text=True, timeout=20)
        open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n'); print(name, 'ran', r2.returncode); return
    r = sp.run(['g++', '-Wall', fn, '-o', name] + (GL if gl else []), capture_output=True, text=True)
    open(name + '.build', 'w').write(r.stdout + r.stderr)
    if r.returncode == 0 and not gl:
        try:
            r2 = sp.run(['./' + name], input=stdin, capture_output=True, text=True, timeout=timeout)
            open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n')
        except sp.TimeoutExpired as e:
            out = (e.stdout or b'')
            out = out.decode() if isinstance(out, bytes) else out
            open(name + '.out', 'w').write(out[:3000] + '\n(timeout: still running after 5 seconds)\nexit=timeout\n')
    if r.returncode == 0 and gl:
        run('./' + name, title, name + '.out', name, clicks=clicks, img=I)
    print(name, 'built' if r.returncode == 0 else 'BUILD FAILED')
K = ('key', 'BackSpace'); F = ('key', 'F12')
CL = [(80, 400), (200, 300), (320, 380), (440, 260), (0, 0, 3), (120, 120), (300, 60), (480, 120), (0, 0, 3), K, (150, 200), (400, 200), (500, 330), K, K, (300, 300), (500, 100)]
# ---- compiler
variant('p1_tiny_compiler.cpp', 'k_swap_levels', [('while (Match(TokenType::Star))', 'while (Match(TokenType::Plus))'), ("left = new Node{ '*', 0, \"\", left, Primary() };", "left = new Node{ '+', 0, \"\", left, Primary() };"),
    ('while (Match(TokenType::Plus))\n            left = new Node{ \'+\', 0, "", left, Multiplication() };', 'while (Match(TokenType::Star))\n            left = new Node{ \'*\', 0, "", left, Multiplication() };')])
variant('p1_tiny_compiler.cpp', 'k_no_skip', [('        if (c == \';\') tokens.push_back({ TokenType::Semicolon, ";" });\n        i++;', '        if (c == \';\') tokens.push_back({ TokenType::Semicolon, ";" });')])
variant('p1_tiny_compiler.cpp', 'k_no_end', [('    tokens.push_back({ TokenType::End, "end" });\n', '')])
variant('p1_tiny_compiler.cpp', 'k_no_lookup', [('    for (size_t i = 0; i < variables.size(); i++)\n        if (variables[i] == name)\n            return (int)i;\n', '')])
# ---- leap / raindrops
variant('p2_leap.cpp', 'l_only4', [('return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);', 'return year % 4 == 0;')])
variant('p2_leap.cpp', 'l_no_400', [('return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);', 'return year % 4 == 0 && year % 100 != 0;')])
variant('p3_raindrops.cpp', 'd_else_if', [('        if (drops % 5 == 0)', '        else if (drops % 5 == 0)'), ('        if (drops % 7 == 0)', '        else if (drops % 7 == 0)')])
variant('p3_raindrops.cpp', 'd_no_empty', [('        if (sound.empty())\n            sound = std::to_string(drops);\n', '')])
# ---- uniforms
variant('r1_animated_color.cpp', 'u_wrong_name', [('glGetUniformLocation(shader, "u_Color")', 'glGetUniformLocation(shader, "u_color")')], gl=True, title='Animated Color', clicks=[F, F])
variant('r1_animated_color.cpp', 'u_unused', [('"    color = u_Color;\\n"', '"    color = vec4(0.2, 0.3, 0.8, 1.0);\\n"')], gl=True, title='Animated Color', clicks=[F, F])
variant('r1_animated_color.cpp', 'u_no_flip', [('        if (r > 1.0f)\n            increment = -0.05f;\n        else if (r < 0.0f)\n            increment = 0.05f;\n', '')], gl=True, title='Animated Color', clicks=[F, F, F])
variant('r1_animated_color.cpp', 'u_no_use', [('    glUseProgram(shader);\n', '')], gl=True, title='Animated Color', clicks=[F, F])
variant('r2_time_colors.cpp', 't_fixed', [('float time = (float)glfwGetTime();', 'float time = 0.0f;')], gl=True, title='Time Colors', clicks=[F, F, F])
variant('r2_time_colors.cpp', 't_wrong_type', [('glUniform1f(timeLocation, time);', 'glUniform4f(timeLocation, time, 0.0f, 0.0f, 0.0f);')], gl=True, title='Time Colors', clicks=[F, F, F])
# ---- math
variant('m1_dot_length.py', 'm_len_mismatch', [('print("[2, 5] . [7, 1] =", dot(a, b))', 'print("[2, 5] . [7, 1] =", dot(a, b))\nprint("[2, 5] . [7, 1, 3] =", dot(a, [7, 1, 3]))\nprint("[7, 1, 3] . [2, 5] =", dot([7, 1, 3], a))')], py=True)
variant('m1_dot_length.py', 'm_no_sqrt', [('    return math.sqrt(dot(a, a))', '    return dot(a, a)')], py=True)
variant('m2_numpy_review.py', 'm_star', [('print("a . b =", np.dot(a, b), "  |a| =", np.linalg.norm(a))', 'print("a * b =", a * b, "  sum =", np.sum(a * b), "  a . b =", np.dot(a, b))\nprint("a . [7, 1, 3] =", np.dot(a, np.array([7, 1, 3])))')], py=True)
# ---- refactoring mistakes (caught by comparing with yesterday's program)
variant('c1_refactored.cpp', 'f_half', [('points.resize(points.size() - last.count * 2);', 'points.resize(points.size() - last.count);')], gl=True, title='Refactored', clicks=CL)
variant('c1_refactored.cpp', 'f_order', [('''    StartNewLine();
    std::cout << "backspace: deleted''', '''    std::cout << "backspace: deleted'''), ('''              << FinishedLineCount() << " lines left" << std::endl;
    UploadPoints();''', '''              << FinishedLineCount() << " lines left" << std::endl;
    StartNewLine();
    UploadPoints();''')], gl=True, title='Refactored', clicks=CL)
