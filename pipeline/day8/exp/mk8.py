import subprocess as sp, os, sys
sys.path.insert(0, '/tmp/claude-0')
from gl3 import run
os.chdir('/home/claude/day8/exp')
SRC = '/home/claude/day8/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day8/img/'
ONLY = sys.argv[1:]
def variant(base, name, reps, gl=False, title=None, py=False, timeout=5):
    if ONLY and name not in ONLY: return
    s = open(SRC + base).read()
    for a, b in reps:
        assert a in s, (name, a); s = s.replace(a, b, 1)
    ext = '.py' if py else '.cpp'
    fn = name + ext; open(fn, 'w').write(s)
    if py:
        r2 = sp.run(['python3', fn], capture_output=True, text=True, timeout=30)
        open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n'); print(name, 'ran', r2.returncode); return
    r = sp.run(['g++', '-Wall', fn, '-o', name] + (GL if gl else []), capture_output=True, text=True)
    open(name + '.build', 'w').write('\n'.join(l for l in (r.stdout + r.stderr).splitlines() if 'stb_image.h' not in l))
    if r.returncode == 0 and not gl:
        r2 = sp.run(['./' + name], capture_output=True, text=True, timeout=timeout)
        open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n')
    if r.returncode == 0 and gl:
        run('./' + name, title, name + '.out', name, img=I, wait=3)
    print(name, 'built' if r.returncode == 0 else 'BUILD FAILED')

# ---- classes
variant('p1_player.cpp', 'x_no_public', [('class Player\n{\npublic:\n', 'class Player\n{\n')])
variant('p1_player.cpp', 'x_by_value', [('void Move(Player& player, int xa, int ya)', 'void Move(Player player, int xa, int ya)')])
variant('p1_player.cpp', 'x_no_speed', [('    player.speed = 2;\n', '')])
variant('p2_counter.cpp', 'x_touch_private', [('    clicks.Add(3);\n', '    clicks.count = 3;\n')])
variant('p2_counter.cpp', 'x_no_reset', [('    clicks.Reset();\n', '')])
# ---- textures
variant('t1_texture.cpp', 't_no_min_filter', [('        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);\n', '')], gl=True, title='Texture')
variant('t1_texture.cpp', 't_no_flip', [('stbi_set_flip_vertically_on_load(1);', 'stbi_set_flip_vertically_on_load(0);')], gl=True, title='Texture')
variant('t1_texture.cpp', 't_no_blend', [('    glEnable(GL_BLEND);\n', '')], gl=True, title='Texture')
variant('t1_texture.cpp', 't_wrong_slot', [('    glUniform1i(location, 0);', '    glUniform1i(location, 1);')], gl=True, title='Texture')
variant('t1_texture.cpp', 't_no_texcoord', [('    glEnableVertexAttribArray(1);\n', '')], gl=True, title='Texture')
variant('t1_texture.cpp', 't_bad_path', [('texture.Load("res/logo.png")', 'texture.Load("res/logo2.png")')], gl=True, title='Texture')
variant('t1_texture.cpp', 't_no_unbind_free', [('        stbi_image_free(pixels);\n', '        stbi_image_free(pixels);\n        std::cout << "pixels after free: " << (void*)pixels << std::endl;\n')], gl=True, title='Texture')
# ---- matrices
variant('m1_matrix_columns.py', 'm_rows', [('    col1 = [M[0][0], M[1][0]]\n    col2 = [M[0][1], M[1][1]]', '    col1 = [M[0][0], M[0][1]]\n    col2 = [M[1][0], M[1][1]]')], py=True)
variant('m2_numpy_grid.py', 'm_order', [('print("shear then rotate (one matrix):")\nprint(rotate @ shear)', 'print("shear then rotate (one matrix):")\nprint(rotate @ shear)\nprint("rotate then shear (other order):")\nprint(shear @ rotate)')], py=True)
# ---- b-rep
variant('c1_brep.cpp', 'b_extra_vertex', [('{0, 1, 1} };\n    cube.edges', '{0, 1, 1}, {2, 2, 2} };\n    cube.edges')])
variant('c1_brep.cpp', 'b_wrong_edge', [('{{3, 8, 7, 11}} };\n    cube.Report();', '{{3, 8, 7, 10}} };\n    cube.Report();')])
variant('c2_wireframe.cpp', 'b_line_strip', [('glDrawElements(GL_LINES, (int)lines.size(), GL_UNSIGNED_INT, nullptr);', 'glDrawElements(GL_LINE_STRIP, (int)lines.size(), GL_UNSIGNED_INT, nullptr);')], gl=True, title='B-Rep Wireframe')
