import sys, importlib
sys.path.insert(0, '/home/claude/steps')
mods = sys.argv[1:]
for m in mods:
    P = importlib.import_module(m).programs()
    for path, p in P.items():
        rs = p.build_and_run()
        bad = [r['step'] for r in rs if not r['build_ok']]
        print(p.pid, len(rs), 'steps', 'BAD ' + str(bad) if bad else 'ok', [str(r.get('code')) for r in rs])
        for r in rs:
            if not r['build_ok']: print('   step', r['step'], r['build'][:400])
