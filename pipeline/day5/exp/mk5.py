import subprocess as sp, os, sys
sys.path.insert(0, '/tmp/claude-0')
from gl3 import run
os.chdir('/home/claude/day5/exp')
SRC = '/home/claude/day5/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day5/img/'
def variant(base, name, reps, gl=False, stdin='\n', title=None, clicks=(), py=False):
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
            r2 = sp.run(['./' + name], input=stdin, capture_output=True, text=True, timeout=10)
            open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n')
        except sp.TimeoutExpired:
            open(name + '.out', 'w').write('(timeout)\nexit=timeout\n')
    if r.returncode == 0 and gl:
        run('./' + name, title, name + '.out', name, clicks=clicks, img=I)
    print(name, 'built' if r.returncode == 0 else 'BUILD FAILED')
NAMES = 'Braden\nJeff\nKatie\nQ\n'
K = ('key', 'BackSpace')
# ---- swap
variant('p1_swap_pointers.cpp', 's_value', [('void swap(int* p, int* q);', 'void swap(int p, int q);'), ('swap(&x, &y);', 'swap(x, y);'),
    ('void swap(int* a, int* b)', 'void swap(int a, int b)'), ('    temp = *a;\n    *a = *b;\n    *b = temp;', '    temp = a;\n    a = b;\n    b = temp;')])
variant('p1_swap_pointers.cpp', 's_no_temp', [('    temp = *a;\n    *a = *b;\n    *b = temp;', '    *a = *b;\n    *b = *a;')])
variant('p1_swap_pointers.cpp', 's_no_star', [('    temp = *a;', '    temp = a;')])
variant('p1_swap_pointers.cpp', 's_no_amp', [('swap(&x, &y);', 'swap(x, y);')])
variant('p1_swap_pointers.cpp', 's_no_decl', [('    void swap(int* p, int* q);\n\n', '')])
# ---- shader
variant('r1_red_triangle.cpp', 'r_syntax', [('"    color = vec4(1.0, 0.0, 0.0, 1.0);\\n"', '"    color = vec4(1.0, 0.0, 0.0, 1.0)\\n"')], gl=True, title='Red Triangle')
variant('r1_red_triangle.cpp', 'r_255', [('"    color = vec4(1.0, 0.0, 0.0, 1.0);\\n"', '"    color = vec4(255.0, 0.0, 0.0, 1.0);\\n"')], gl=True, title='Red Triangle')
variant('r1_red_triangle.cpp', 'r_green', [('"    color = vec4(1.0, 0.0, 0.0, 1.0);\\n"', '"    color = vec4(0.0, 1.0, 0.0, 1.0);\\n"')], gl=True, title='Red Triangle')
variant('r1_red_triangle.cpp', 'r_vec2', [('in vec4 position;', 'in vec2 position;')], gl=True, title='Red Triangle')
variant('r2_shader_edit.cpp', 'r_no_out', [('        "out vec4 v_Position;\\n"\n', ''), ('        "    v_Position = position;\\n"\n', '')], gl=True, title='Shader Edit')
variant('r2_shader_edit.cpp', 'r_small', [('position.x * 1.5, position.y * 1.5', 'position.x * 0.5, position.y * 0.5')], gl=True, title='Shader Edit')
variant('r2_shader_edit.cpp', 'r_flip', [('position.x * 1.5, position.y * 1.5', 'position.x * 1.5, -position.y * 1.5')], gl=True, title='Shader Edit')
# ---- numpy
variant('n2_dot_cross.py', 'n_dot_mismatch', [('print("np.dot(a, b) =", d)', 'print("np.dot(a, b) =", d)\nprint(np.dot(np.array([1, 2, 3]), np.array([1, 2])))')], py=True)
variant('n1_numpy_basics.py', 'n_list', [('a = np.array([1, 2, 3])\n', 'a = [1, 2, 3]\nprint("list * 2 =", a * 2)\nprint("list + 2 =", a + 2)\n', )], py=True)
variant('n2_dot_cross.py', 'n_cross2d', [('print("np.cross(a, b) =", c)', 'print("np.cross(a, b) =", c)\nprint("2D:", np.cross(np.array([1, 2]), np.array([3, 4])))')], py=True)
# ---- names vector
variant('c1_names_vector.cpp', 'v_no_pop', [('    list.pop_back();\n\n', '')], stdin=NAMES)
variant('c1_names_vector.cpp', 'v_start_q', [('string name = "x";', 'string name = "Q";')], stdin=NAMES)
variant('c1_names_vector.cpp', 'v_no_cast', [('i < (int)list.size()', 'i < list.size()')], stdin=NAMES)
# ---- delete last line
CL = [(80, 400), (200, 300), (320, 380), (440, 260), (0, 0, 3), (120, 120), (300, 60), (480, 120), (0, 0, 3), K, (150, 200), (400, 200)]
variant('c2_delete_last_line.cpp', 'd_no_new_line', [('    polylines.push_back({ (int)points.size() / 2, 0 });\n    std::cout << "backspace', '    std::cout << "backspace')], gl=True, title='Delete Last Line', clicks=CL)
variant('c2_delete_last_line.cpp', 'd_no_empty_check', [('''    if (polylines.back().count == 0)
    {
        if (polylines.size() == 1)
        {
            std::cout << "backspace: nothing to delete" << std::endl;
            return;
        }
        polylines.pop_back();
    }

''', '')], gl=True, title='Delete Last Line', clicks=CL)
variant('c2_delete_last_line.cpp', 'd_half_points', [('i < last.count * 2;', 'i < last.count;')], gl=True, title='Delete Last Line', clicks=CL)
variant('c2_delete_last_line.cpp', 'd_no_upload', [('    UploadPoints();\n}\n\nint main()', '}\n\nint main()')], gl=True, title='Delete Last Line', clicks=CL)
