# usage: python3 check.py N   -> checks d{N}.py against todo_d{N}.json
import sys, json, re, runpy
d = sys.argv[1]
base = '/home/claude/steps/wordsdata/'
todo = json.load(open(f'{base}todo_d{d}.json'))
L = runpy.run_path(f'{base}d{d}.py')['L']
ns = lambda s: re.sub(r'\s+', '', s)
BAD = ['زي اللي فوق', 'زي ما قلنا', 'نفس اللي فوق', 'راجع', 'شوف فوق', 'زي قبل', 'نفس الشرح', 'اللي فات']
errs = 0
for t in todo:
    if t not in L:
        print('MISSING:', t); errs += 1; continue
for t, (chips, note) in L.items():
    if ns(''.join(tok for tok, _ in chips)) != ns(t):
        print('COVERAGE:', t, '\n   tokens:', ''.join(tok for tok, _ in chips)); errs += 1
    for tok, m in chips:
        if not m.strip(): print('EMPTY MEANING:', t, tok); errs += 1
        for b in BAD:
            if b in m: print(f'SHORTCUT "{b}":', t, '|', tok, '|', m); errs += 1
print('errors:', errs, '| lines:', len(L), '/', len(todo))
