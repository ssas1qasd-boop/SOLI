import subprocess as sp, time, os
os.environ['DISPLAY'] = ':84'
def run(exe, name, out, shot, img, wait=2.0, cwd=None):
    env = dict(os.environ, LD_PRELOAD='/tmp/claude-0/vsync.so')
    f = open(out, 'w')
    p = sp.Popen([exe], stdout=f, stderr=sp.STDOUT, env=env, cwd=cwd)
    time.sleep(wait)
    w = sp.run(['xdotool', 'search', '--name', name], capture_output=True, text=True, timeout=5).stdout.split()
    if not w or p.poll() is not None:
        print(exe, 'no window / exited', p.poll()); p.kill(); f.close(); return False
    w = w[0]
    sp.run(['import', '-window', w, img + shot + '.png'], timeout=10)
    sp.run(['xdotool', 'windowfocus', '--sync', w], timeout=5)
    sp.run(['xdotool', 'keydown', '--window', w, 'Escape'], timeout=5); time.sleep(0.5); sp.run(['xdotool', 'keyup', '--window', w, 'Escape'], timeout=5)
    try: p.wait(timeout=5); ok = True
    except sp.TimeoutExpired: p.kill(); ok = False; print(exe, 'did not exit on Escape')
    f.close()
    if ok: open(out, 'a').write(f'\nexit={p.returncode}\n')
    return ok
