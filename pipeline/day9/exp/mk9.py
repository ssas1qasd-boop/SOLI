import subprocess as sp, os, sys
sys.path.insert(0, '/tmp/claude-0')
from gl3 import run
os.chdir('/home/claude/day9/exp')
SRC = '/home/claude/day9/src/'
GL = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()
I = '/home/claude/day9/img/'
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
    r = sp.run(['g++', '-Wall', fn, '-o', name] + (['stb.o'] if 'stb_image' in s else []) + (GL if gl else []), capture_output=True, text=True)
    open(name + '.build', 'w').write('\n'.join(l for l in (r.stdout + r.stderr).splitlines() if 'stb_image.h' not in l))
    if r.returncode == 0 and not gl:
        r2 = sp.run(['./' + name], capture_output=True, text=True, timeout=timeout)
        open(name + '.out', 'w').write(r2.stdout + r2.stderr + f'\nexit={r2.returncode}\n')
    if r.returncode == 0 and gl:
        run('./' + name, title, name + '.out', name, img=I, wait=3)
    print(name, 'built' if r.returncode == 0 else 'BUILD FAILED')


# ---- struct vs class
variant('p1_struct_class.cpp', 'x_class_no_public', [('class PlayerC\n{\npublic:\n', 'class PlayerC\n{\n')])
variant('p1_struct_class.cpp', 'x_struct_private', [('struct PlayerS\n{\n', 'struct PlayerS\n{\nprivate:\n')])
variant('p2_vertex_struct.cpp', 'x_vertex_double', [('    float x, y;\n    float u, v;', '    double x, y;\n    double u, v;')])
variant('p2_vertex_struct.cpp', 'x_vertex_extra', [('    float u, v;\n};', '    float u, v;\n    int id;\n};'), ('{ -0.5f, -0.5f, 0.0f, 0.0f },', '{ -0.5f, -0.5f, 0.0f, 0.0f, 7 },')])
# ---- textures
variant('t1_pixel_cat.cpp', 't_no_mipmap', [('    glGenerateMipmap(GL_TEXTURE_2D);\n', '')], gl=True, title='Pixel Cat')
variant('t1_pixel_cat.cpp', 't_rgb', [('glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, widthImg, heightImg, 0, GL_RGBA,', 'glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, widthImg, heightImg, 0, GL_RGB,')], gl=True, title='Pixel Cat')
variant('t1_pixel_cat.cpp', 't_no_flip', [('stbi_set_flip_vertically_on_load(true);', 'stbi_set_flip_vertically_on_load(false);')], gl=True, title='Pixel Cat')
variant('t1_pixel_cat.cpp', 't_linear', [('glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);', 'glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);')], gl=True, title='Pixel Cat')
variant('t2_wrap_modes.cpp', 'w_no_border', [('        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border);\n', '')], gl=True, title='Wrap Modes')
# ---- transformations
variant('m1_transform.py', 'm_wrong_matrix', [('A = [[1, 2, 0],\n     [0, 0, 3]]', 'A = [[1, 0, 2],\n     [0, 3, 0]]')], py=True)
variant('m2_projection.py', 'm_shape', [('screen = (P @ centered.T).T', 'screen = (P.T @ centered.T).T')], py=True)
# ---- mesh
variant('c1_mesh.cpp', 'b_no_set', [('std::set<std::pair<unsigned int, unsigned int>> edges;', 'std::vector<std::pair<unsigned int, unsigned int>> edges;'), ('edges.insert({ std::min(p, q), std::max(p, q) });', 'edges.push_back({ std::min(p, q), std::max(p, q) });')])
variant('c2_barycentric.cpp', 'b_flat', [('"out vec3 color;\\n"', '"flat out vec3 color;\\n"'), ('"in vec3 color;\\n"', '"flat in vec3 color;\\n"')], gl=True, title='Barycentric')
