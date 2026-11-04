# "Write it yourself, step by step": every program is rebuilt from an empty main in small steps.
# Each step = the lines added at that step. Every step is compiled and really run; its output/screenshot is stored.
import os, re, subprocess as sp, html, json, time, shutil, sys
sys.path.insert(0, '/tmp/claude-0')
ROOT = '/home/claude/steps/work'
GLFLAGS = "/home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl".split()

def parse_ranges(r):
    out = set()
    for part in str(r).replace(' ', '').split(','):
        if not part: continue
        if '-' in part:
            a, b = part.split('-'); out |= set(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return out

PURE_OPEN = re.compile(r'^\s*\{\s*$')
PURE_CLOSE = re.compile(r'^\s*\}\s*;?\s*$')

def assign(lines, step_of):
    """step_of: {lineno: step} for explicit lines. Fill braces/blank lines automatically."""
    n = len(lines)
    # brace matching by raw char counting
    stack, match = [], {}
    for i, l in enumerate(lines, 1):
        for ch in l:
            if ch == '{': stack.append(i)
            elif ch == '}':
                if stack: match.setdefault(i, stack.pop())
    res = dict(step_of)
    for i, l in enumerate(lines, 1):
        if i in res: continue
        if PURE_OPEN.match(l):
            j = i - 1
            while j > 0 and not lines[j - 1].strip(): j -= 1
            if j in res: res[i] = res[j]
    for i, l in enumerate(lines, 1):
        if i in res: continue
        if PURE_CLOSE.match(l) and i in match and match[i] in res:
            res[i] = res[match[i]]
    for i, l in enumerate(lines, 1):
        if i in res: continue
        if not l.strip():
            res[i] = None  # blank: shown if next included
            continue
        raise ValueError(f'line {i} has no step: {l!r}')
    return res

def ensure_x():
    if sp.run(['pgrep', '-x', 'Xvfb'], capture_output=True).returncode != 0:
        sp.Popen(['Xvfb', ':84', '-screen', '0', '1024x900x24'], stdout=sp.DEVNULL, stderr=sp.DEVNULL, start_new_session=True)
        time.sleep(1.5)

class Program:
    def __init__(self, pid, files, steps, kind='cli', window=None, clicks=None, cmd_files=None, run_cwd_extra=None, cc='g++', stdin='\n'):
        self.pid, self.files, self.steps, self.kind, self.window = pid, files, steps, kind, window
        self.clicks = clicks or {}          # {step: [(x,y[,btn]), ...]}
        self.extra = run_cwd_extra or {}     # {relpath: srcpath} copied next to the binary (e.g. shader files)
        self.cc = cc
        self.stdin = stdin
        self.src = {f: open(p).read().split('\n') for f, p in files.items()}
        for f in self.src:
            if self.src[f] and self.src[f][-1] == '': self.src[f].pop()
        self.map = {}
        for f, lines in self.src.items():
            explicit = {}
            for k, st in enumerate(steps, 1):
                for ln in parse_ranges(st['lines'].get(f, '')):
                    if ln in explicit: raise ValueError(f'{pid}:{f}:{ln} assigned twice')
                    explicit[ln] = k
            self.map[f] = assign(lines, explicit)

    def code_at(self, f, k):
        lines, m = self.src[f], self.map[f]
        out = []
        for i, l in enumerate(lines, 1):
            s = m[i]
            if s is None:
                # keep blank line only if neighbours on both sides are included
                prev = next((m[j] for j in range(i - 1, 0, -1) if m[j] is not None), None)
                nxt = next((m[j] for j in range(i + 1, len(lines) + 1) if m[j] is not None), None)
                if prev is not None and nxt is not None and prev <= k and nxt <= k: out.append((i, l, None))
            elif s <= k:
                out.append((i, l, s))
        return out

    def files_at(self, k):
        return [f for f in self.src if any(s is not None and s <= k for s in self.map[f].values())]

    def build_and_run(self, force=False):
        base = f'{ROOT}/{self.pid}'
        results = []
        for k in range(1, len(self.steps) + 1):
            d = f'{base}/s{k}'
            done = f'{d}/result.json'
            if os.path.exists(done) and not force:
                results.append(json.load(open(done))); continue
            if os.path.exists(d): shutil.rmtree(d)
            os.makedirs(d)
            for f in self.files_at(k):
                p = f'{d}/{f}'; os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, 'w').write('\n'.join(l for _, l, _ in self.code_at(f, k)) + '\n')
            for rel, srcp in self.extra.items():
                p = f'{d}/{rel}'; os.makedirs(os.path.dirname(p), exist_ok=True); shutil.copy(srcp, p)
            cfiles = [f for f in self.files_at(k) if f.endswith(('.cpp', '.c'))]
            cc = 'gcc' if all(f.endswith('.c') for f in cfiles) else 'g++'
            cmd = [cc, '-Wall', *cfiles, '-o', 'prog'] + (GLFLAGS if self.kind == 'gl' else [])
            if self.kind == 'py':
                pyf = [f for f in self.files_at(k) if f.endswith('.py')][0]
                cmd = ['python3', '-m', 'py_compile', pyf]
            r = sp.run(cmd, cwd=d, capture_output=True, text=True)
            res = {'step': k, 'build_ok': r.returncode == 0, 'build': r.stderr[-3000:]}
            if r.returncode == 0:
                if self.kind in ('cli', 'py'):
                    try:
                        runcmd = ['python3', [f for f in self.files_at(k) if f.endswith('.py')][0]] if self.kind == 'py' else ['./prog']
                        r2 = sp.run(runcmd, cwd=d, input=self.stdin, capture_output=True, text=True, timeout=20)
                        res.update(out=r2.stdout + r2.stderr, code=r2.returncode)
                    except sp.TimeoutExpired:
                        res.update(out='', code='timeout')
                else:
                    res.update(self._run_gl(d, k))
            json.dump(res, open(done, 'w'), ensure_ascii=False)
            results.append(res)
        self.results = results
        return results

    def _run_gl(self, d, k):
        ensure_x()
        env = dict(os.environ, DISPLAY=':84', LD_PRELOAD='/tmp/claude-0/vsync.so')
        out = open(f'{d}/out.txt', 'w')
        p = sp.Popen(['./prog'], cwd=d, stdout=out, stderr=sp.STDOUT, env=env)
        time.sleep(1.5)
        shot = None
        if p.poll() is None:
            w = sp.run(['xdotool', 'search', '--name', self.window], capture_output=True, text=True, env=env, timeout=5).stdout.split()
            if w:
                w = w[0]
                for c in self.clicks.get(k, []):
                    if c[0] == 'key':
                        sp.run(['xdotool', 'windowfocus', '--sync', w], env=env, timeout=5)
                        sp.run(['xdotool', 'key', '--window', w, c[1]], env=env, timeout=5); time.sleep(0.35); continue
                    btn = str(c[2]) if len(c) > 2 else '1'
                    sp.run(['xdotool', 'mousemove', '--window', w, str(c[0]), str(c[1]), 'click', btn], env=env, timeout=5); time.sleep(0.35)
                time.sleep(0.2)
                sp.run(['import', '-window', w, f'{d}/shot.png'], env=env, timeout=10)
                shot = f'{d}/shot.png'
            p.terminate()
            try: p.wait(timeout=5)
            except sp.TimeoutExpired: p.kill()
            code = 'running'
        else:
            code = p.returncode
        out.close()
        return {'out': open(f'{d}/out.txt').read(), 'code': code, 'shot': shot}

    def check(self):
        bad = [r for r in self.results if not r['build_ok']]
        return bad
