import subprocess as sp, os, sys
sys.path.insert(0, '/tmp/claude-0')
from gl3 import run
os.chdir('/home/claude/day7/exp')
SRC = '/home/claude/day7/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day7/img/'
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
# ---- pointers
variant('p1_pointers_review.cpp', 'x_void_deref', [('    int* intPtr = &var;\n    *intPtr = 10;', '    *ptr = 10;\n    int* intPtr = &var;')])
variant('p1_pointers_review.cpp', 'x_no_cast', [('std::cout << "buffer = " << (void*)buffer', 'std::cout << "buffer = " << buffer')])
variant('p1_pointers_review.cpp', 'x_double_delete', [('    delete[] buffer;\n    buffer = nullptr;', '    delete[] buffer;\n    delete[] buffer;')])
variant('p2_pointer_quiz.cpp', 'q_by_value', [('void Swap(int* a, int* b)\n{\n    int temp = *a;\n    *a = *b;\n    *b = temp;', 'void Swap(int a, int b)\n{\n    int temp = a;\n    a = b;\n    b = temp;'), ('Swap(&a, &b);', 'Swap(a, b);')])
variant('p2_pointer_quiz.cpp', 'q_single_ptr', [('void MakeText(char** out, int size)\n{\n    *out = new char[size];\n    memset(*out, \'x\', size - 1);\n    (*out)[size - 1] = 0;', 'void MakeText(char* out, int size)\n{\n    out = new char[size];\n    memset(out, \'x\', size - 1);\n    out[size - 1] = 0;'), ('MakeText(&text, 4);', 'MakeText(text, 4);')])
variant('p2_pointer_quiz.cpp', 'q_no_null', [('    if (p != nullptr)\n        *p = 0;', '    *p = 0;')])
variant('p2_pointer_quiz.cpp', 'q_no_deref', [('total += *(values + i);', 'total += values + i;')])
# ---- vertex arrays
variant('r1_vertex_array.cpp', 'v_no_rebind', [('        glBindVertexArray(vao);\n', '')], gl=True, title='Vertex Array', clicks=[F, F])
variant('r1_vertex_array.cpp', 'v_no_ibo', [('        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);\n', '')], gl=True, title='Vertex Array', clicks=[F, F])
variant('r1_vertex_array.cpp', 'v_ibo_first', [('    glBindVertexArray(0);\n    glBindBuffer(GL_ARRAY_BUFFER, 0);\n    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);', '    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);\n    glBindVertexArray(0);\n    glBindBuffer(GL_ARRAY_BUFFER, 0);'), ('        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);\n', '')], gl=True, title='Vertex Array', clicks=[F, F])
variant('r2_two_methods.cpp', 'w_no_pointer', [('        glBindBuffer(GL_ARRAY_BUFFER, triangleBuffer);\n        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, 0);\n', '        glBindBuffer(GL_ARRAY_BUFFER, triangleBuffer);\n')], gl=True, title='Two Methods', clicks=[F])
variant('r2_two_methods.cpp', 'w_order', [('        glBindBuffer(GL_ARRAY_BUFFER, triangleBuffer);\n        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, 0);\n', '        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, 0);\n        glBindBuffer(GL_ARRAY_BUFFER, triangleBuffer);\n')], gl=True, title='Two Methods', clicks=[F])
# ---- cross
variant('m1_cross_quiz.py', 'c_not_reversed', [('            a[2] * b[0] - a[0] * b[2],', '            a[0] * b[2] - a[2] * b[0],')], py=True)
variant('m1_cross_quiz.py', 'c_2d', [('a = [1, -7, 1]\nb = [5, 2, 4]\nc = cross(a, b)', 'print(cross([1, 2], [3, 4]))\na = [1, -7, 1]\nb = [5, 2, 4]\nc = cross(a, b)')], py=True)
# ---- git id
variant('c1_commit_id.py', 'g_one_second', [('1793458800 +0200"\ntext', '1793458801 +0200"\ntext')], py=True)
