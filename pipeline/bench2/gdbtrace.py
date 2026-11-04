# Run inside gdb:  TRACE_CFG=cfg.json gdb -q -batch -x gdbtrace.py --args ./prog
# Steps through the real program line by line (only our own source files), records for every step:
# file, line, function, call depth, locals (with declaration line), evaluated gl* call arguments,
# stdout produced by the step, and the real back-buffer pixels after glClear / glDraw* (glReadPixels).
import gdb, json, os, re, subprocess, time
CFG = json.load(open(os.environ['TRACE_CFG']))
OUT = CFG['out']; os.makedirs(OUT + '/frames', exist_ok=True)
SRCS = set(CFG['srcs'])
for c in ['set pagination off', 'set confirm off', 'set print pretty off', 'set print elements 400', 'set print repeats 64',
          'set step-mode off', 'set width 0', 'skip -gfi /usr/include/*', 'skip -gfi /usr/include/*/*', 'skip -gfi /usr/include/*/*/*',
          'skip -gfi /usr/include/*/*/*/*', 'skip -gfi /usr/lib/*', 'set environment DISPLAY=:84']:
    try: gdb.execute(c, to_string=True)
    except gdb.error: pass
gdb.execute('break main', to_string=True)
stdout_path = OUT + '/stdout.txt'
gdb.execute(f'run < {CFG["stdin"]} > {stdout_path} 2>&1' if CFG.get('stdin') else f'run > {stdout_path} 2>&1', to_string=True)
try: gdb.execute('call (int)setvbuf(stdout, 0, 2, 0)', to_string=True)
except gdb.error: pass

def our_frames():
    n, f = 0, gdb.newest_frame()
    while f is not None:
        sal = f.find_sal()
        if sal.symtab and sal.symtab.fullname() in SRCS: n += 1
        f = f.older()
    return n

def val_str(v):
    try:
        s = v.format_string(max_elements=int(os.environ.get('MAXEL', '24')), repeat_threshold=64, styling=False)
    except Exception:
        try: s = str(v)
        except Exception: s = '?'
    return s if len(s) < 4000 else s[:3997] + '…'

def locals_of(frame):
    out = []
    try: block = frame.block()
    except RuntimeError: return out
    seen = set()
    while block is not None:
        for sym in block:
            if not (sym.is_variable or sym.is_argument) or sym.name in seen: continue
            seen.add(sym.name)
            try: v = sym.value(frame); vs = val_str(v); ty = str(sym.type)
            except Exception: vs, ty = '?', str(sym.type)
            out.append([sym.name, ty, vs, sym.line, bool(sym.is_argument)])
        if block.function is not None: break
        block = block.superblock
    return out

def split_args(s):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch in '([{': depth += 1
        if ch in ')]}': depth -= 1
        if ch == ',' and depth == 0: out.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): out.append(cur.strip())
    return out

def gl_call(text):
    m = re.search(r'\b(gl[A-Z]\w*|glfw\w+)\s*\(', text)
    if not m: return None
    i, depth, j = m.end(), 1, m.end()
    while j < len(text) and depth:
        if text[j] == '(': depth += 1
        elif text[j] == ')': depth -= 1
        j += 1
    fn, args = m.group(1), split_args(text[i:j-1])
    ev = []
    for a in args:
        try: ev.append([a, val_str(gdb.parse_and_eval(a))])
        except Exception: ev.append([a, None])
    return {'fn': fn, 'args': ev}

LINES = {p: open(p).read().split('\n') for p in SRCS}
steps, laps, frame_no = [], 0, 0
buf = None; W = H = 0
swap_line = None
clicks = CFG.get('clicks', [])  # [{lap, x, y, btn}]
closed = False
wid = None

def readpixels(tag):
    global buf, W, H, frame_no
    try:
        if not W and CFG.get('size'):
            W, H = CFG['size']
            gdb.execute(f'set $pix = (unsigned char*)malloc({W*H*4})', to_string=True)
        if not W:
            wname = CFG.get('window_var', 'window')
            gdb.execute('set $fw = (int*)malloc(8)', to_string=True)
            gdb.execute(f'call ((void(*)(void*,int*,int*))glfwGetFramebufferSize)({wname}, $fw, $fw+1)', to_string=True)
            W = int(gdb.parse_and_eval('$fw[0]')); H = int(gdb.parse_and_eval('$fw[1]'))
            gdb.execute(f'set $pix = (unsigned char*)malloc({W*H*4})', to_string=True)
        gdb.execute('call ((void(*)(void))glad_glFinish)()', to_string=True)
        gdb.execute(f'call ((void(*)(int,int,int,int,unsigned,unsigned,void*))glad_glReadPixels)(0, 0, {W}, {H}, 0x1908, 0x1401, $pix)', to_string=True)
        frame_no += 1; fn = f'{OUT}/frames/f{frame_no:04d}.raw'
        gdb.execute(f'dump binary memory {fn} $pix $pix+{W*H*4}', to_string=True)
        return [os.path.basename(fn), W, H]
    except gdb.error as e:
        return ['ERR ' + str(e)[:80], 0, 0]

def send_click(c):
    global wid
    try:
        if wid is None:
            wid = subprocess.run(['xdotool', 'search', '--name', CFG['title']], capture_output=True, text=True, env={**os.environ, 'DISPLAY': ':84'}).stdout.split()[0]
        env = {**os.environ, 'DISPLAY': ':84'}
        if c.get('key'):
            subprocess.run(['xdotool', 'windowfocus', '--sync', wid], env=env)
            subprocess.run(['xdotool', 'key', '--window', wid, c['key']], env=env)
            time.sleep(.15); return
        if c.get('x') or c.get('y'):
            subprocess.run(['xdotool', 'mousemove', '--window', wid, str(c['x']), str(c['y'])], env=env); time.sleep(.05)
        subprocess.run(['xdotool', 'click', str(c.get('btn', 1))], env=env)
        time.sleep(.15)
    except Exception as e:
        print('click failed', e)

for cb in CFG.get('callbacks', []):
    gdb.execute(f'break {cb}', to_string=True)

last_out = 0
for guard in range(20000):
    try: f = gdb.selected_frame()
    except gdb.error: break
    sal = f.find_sal()
    if not sal.symtab or sal.symtab.fullname() not in SRCS:
        try: gdb.execute('finish', to_string=True); continue
        except gdb.error: break
    path, line = sal.symtab.fullname(), sal.line
    text = LINES[path][line - 1] if line - 1 < len(LINES[path]) else ''
    rec = {'file': os.path.basename(path), 'line': line, 'fn': f.name() or '?', 'depth': our_frames(), 'locals': locals_of(f), 'text': text.strip()}
    g = gl_call(text)
    if g: rec['gl'] = g
    # lap bookkeeping / clicks / close
    if 'glfwSwapBuffers' in text:
        laps += 1; rec['lap'] = laps
    if 'glfwWindowShouldClose' in text and 'while' in text:
        lapno = laps + 1; rec['loopcheck'] = lapno
        for c in clicks:
            if c['lap'] == lapno and not c.get('sent'): send_click(c); c['sent'] = True
        if lapno > CFG['laps'] and not closed:
            gdb.execute(f"call ((void(*)(void*,int))glfwSetWindowShouldClose)({CFG.get('window_var','window')}, 1)", to_string=True); closed = True; rec['closing'] = True
    steps.append(rec)
    try: gdb.execute('step', to_string=True)
    except gdb.error: break
    # stdout produced by this step
    try:
        sz = os.path.getsize(stdout_path)
        if sz > last_out:
            with open(stdout_path, 'rb') as fh: fh.seek(last_out); rec['out'] = fh.read(sz - last_out).decode('utf-8', 'replace')
            last_out = sz
    except OSError: pass
    # real pixels after anything that writes the back buffer
    if re.search(r'\bgl(Clear|DrawArrays|DrawElements)\b', text):
        try: gdb.selected_frame(); rec['fb'] = readpixels(rec['line'])
        except gdb.error: pass
    try:
        if not gdb.selected_inferior().pid: break
    except Exception: break

json.dump({'steps': steps, 'laps': laps, 'W': W, 'H': H}, open(OUT + '/trace.json', 'w'), ensure_ascii=False)
print('TRACED', len(steps), 'steps', laps, 'laps', W, H)
gdb.execute('kill', to_string=True) if gdb.selected_inferior().pid else None
