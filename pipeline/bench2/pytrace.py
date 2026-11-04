"""Python twin of gdbtrace.py: runs a .py program line by line with sys.settrace and writes the same trace.json
(file, line, fn, depth, locals [name, type, value, first-assignment line, is_arg], text, out)."""
import sys, os, io, json, re, runpy

src, out_dir = os.path.abspath(sys.argv[1]), sys.argv[2]
os.makedirs(out_dir + '/frames', exist_ok=True)
lines = open(src).read().split('\n')
first = {}
for k, l in enumerate(lines, 1):
    m = re.match(r'^\s*([A-Za-z_]\w*)\s*=(?!=)', l)
    if m: first.setdefault(m.group(1), k)

def tname(v):
    t = type(v)
    if t.__module__ == 'numpy' and t.__name__ == 'ndarray':
        return f'numpy.ndarray {v.dtype} shape {v.shape}'
    if t.__module__ == 'numpy': return f'numpy.{t.__name__}'
    return t.__name__

def vstr(v):
    try:
        import numpy as np
        if isinstance(v, np.ndarray):
            return np.array2string(v, separator=', ', max_line_width=400).replace('\n', ' ')
        if isinstance(v, np.generic): return str(v)
    except Exception: pass
    s = repr(v)
    return s if len(s) < 4000 else s[:3997] + '…'

steps, buf = [], io.StringIO()
real_out = sys.stdout
last = [0]

def snap(frame):
    return [[n, tname(v), vstr(v), first.get(n, frame.f_lineno), False]
            for n, v in frame.f_locals.items() if not n.startswith('__') and type(v).__name__ != 'module' and n in first]

def flush_out():
    s = buf.getvalue()
    if len(s) > last[0] and steps:
        steps[-1]['out'] = steps[-1].get('out', '') + s[last[0]:]
        last[0] = len(s)

def tracer(frame, event, arg):
    if frame.f_code.co_filename != src: return None
    if event == 'line':
        flush_out()
        ln = frame.f_lineno
        steps.append({'file': os.path.basename(src), 'line': ln, 'fn': 'main', 'depth': 1, 'locals': snap(frame), 'text': lines[ln - 1].strip()})
    return tracer

sys.stdout = buf
sys.settrace(tracer)
try:
    runpy.run_path(src, run_name='__main__')
finally:
    sys.settrace(None)
    flush_out()
    sys.stdout = real_out
open(out_dir + '/stdout.txt', 'w').write(buf.getvalue())
json.dump({'steps': steps, 'laps': 0, 'W': 0, 'H': 0}, open(out_dir + '/trace.json', 'w'), ensure_ascii=False)
json.dump({'out': out_dir, 'srcs': [src], 'laps': 0, 'title': 'x', 'callbacks': [], 'clicks': [], 'lang': 'python'}, open(out_dir + '/cfg.json', 'w'), ensure_ascii=False)
print('TRACED', len(steps), 'steps')
