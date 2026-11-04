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
# Hamming
variant('h1_hamming.c', 'h_no_end_check', [("while (lhs[i] != '\\0' && rhs[i] != '\\0')", "while (lhs[i] != '\\0')")], flags=A, c=True)
variant('h1_hamming.c', 'h_no_len_check', [("    if (lhs[i] != '\\0' || rhs[i] != '\\0')\n        return -1;\n\n", "")], c=True)
variant('h1_hamming.c', 'h_write_const', [("    int distance = 0;\n", "    int distance = 0;\n    lhs[0] = 'X';\n")], c=True)
# Cross
  ('Vec3 v = { 0, 0, 2 };', 'Vec3 v = { 1, 2, 3 };'), ('Vec3 w = { 0, 2, 0 };', 'Vec3 w = { 4, 5, 6 };')])
# Shader file
# CAD