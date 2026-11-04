import json, sys
d = int(sys.argv[1]); ids = sys.argv[2:]
for p in json.load(open(f'/home/claude/bench2/out_days/data_day{d}.json'))['programs']:
    if ids and p['id'] not in ids: continue
    print(f"===== {p['id']} | {p['title']} | frames={len(p['frames'] or [])} W={p['W']} H={p['H']}")
    print('TERM:', (p['term'] or [])[:10], '(+%d)' % max(0, len(p['term'] or []) - 10))
    for f, fl in enumerate(p['files']):
        print(f'--- f{f} {fl["name"]}')
        for n, t in enumerate(fl['lines'], 1):
            if t.strip(): print(f'{n:4} {t.rstrip()}')
    last = {}
    for s in p['steps']:
        for fr in s.get('st') or []:
            for v in fr.get('v') or []:
                last[(fr['fn'], v[0])] = v[1]
    print('VALS:', '; '.join(f'{fn}.{k}={str(v)[:40]}' for (fn, k), v in list(last.items())[:40]))
