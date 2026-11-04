import subprocess as sp, os, shutil
def sess(name, cmds, cfg=True):
    W = '/tmp/gx_' + name; shutil.rmtree(W, ignore_errors=True); os.makedirs(W + '/home'); os.makedirs(W + '/cad')
    shutil.copy('/home/claude/day7/src/refactored.cpp', W + '/cad/')
    open(W + '/home/.gitconfig', 'w').write('[init]\n\tdefaultBranch = master\n[core]\n\tpager = cat\n' + ('[user]\n\tname = Student\n\temail = student@example.com\n' if cfg else ''))
    env = dict(os.environ, HOME=W + '/home', GIT_CONFIG_NOSYSTEM='1', GIT_AUTHOR_DATE='1793458800 +0200', GIT_COMMITTER_DATE='1793458800 +0200', EMAIL='', GIT_AUTHOR_EMAIL='', GIT_COMMITTER_EMAIL='') if not cfg else dict(os.environ, HOME=W + '/home', GIT_CONFIG_NOSYSTEM='1', GIT_AUTHOR_DATE='1793458800 +0200', GIT_COMMITTER_DATE='1793458800 +0200')
    if not cfg:
        for k in ('EMAIL', 'GIT_AUTHOR_EMAIL', 'GIT_COMMITTER_EMAIL'): env.pop(k, None)
    out = []
    for c in cmds:
        r = sp.run(c, shell=True, cwd=W + '/cad', env=env, capture_output=True, text=True)
        out.append('$ ' + c); t = (r.stdout + r.stderr).rstrip('\n').replace(W + '/cad', 'C:/Users/Student/cad').replace(W, '')
        if t: out.append(t)
        out.append('')
    open(f'/home/claude/day7/exp/{name}.out', 'w').write('\n'.join(out).rstrip() + '\n')
    print(open(f'/home/claude/day7/exp/{name}.out').read())
sess('g_no_add', ['git init -q', 'git commit -m "add refactored polyline tool"'])
sess('g_no_name', ['git init -q', 'git add .', 'git commit -m "add refactored polyline tool"'], cfg=False)
sess('g_bad_msg', ['git init -q', 'git add .', 'git commit -q -m "stuff"', "sed -i 's/kPointSize = 10.0f/kPointSize = 12.0f/' refactored.cpp", 'git commit -q -a -m "fixed things"', 'git log --oneline'])
