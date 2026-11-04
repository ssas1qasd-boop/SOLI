import json
tpl=open('tpl.html').read()
css=open('base.css').read()
js=open('app.js').read().replace('(() => {\n', '(() => {\n' + open('why.js').read() + '\nwindow.__bench = {role: (v, j) => useRole(v, j), uses: k => allUses(k), progs: () => PROGS, load: id => loadProgram(id), st: () => ST, why: k => whyHtml(k), text: k => stepText(ST[k]), go: k => go(k), agent: t => window.__agent && window.__agent.ask(t), dyn: () => [Object.keys(crates), Object.keys(tags)], scale: () => Object.fromEntries(Object.entries(crates).map(([k, c]) => [k, +c.scale.x.toFixed(2)]))};\n', 1).replace('%%GLOSS%%', open('gloss.js').read()).replace('\nsyncPause();\nrequestAnimationFrame(frame);\n})();', '\nconst AG_SEM = ' + open('sem/sem.json').read() + ';\nconst AG_MODEL = ' + open('model/learned.json').read() + ';\nconst AG_KB = ' + __import__('json').dumps([dict(e, pid=__import__('os').path.basename(f)[:-5]) for f in sorted(__import__('glob').glob('kb/*.json')) for e in __import__('json').load(open(f))], ensure_ascii=False) + ';\n' + open('agent.js').read() + '\nsyncPause();\nrequestAnimationFrame(frame);\n})();')
import base64, os
def _fm(ps):
    for p in ps:
        for ext, mt in (('.q.png', 'image/png'), ('.webp', 'image/webp')):
            fp = f'fmap/{p["id"]}{ext}'
            if os.path.exists(fp): p['fmap'] = f'data:{mt};base64,' + base64.b64encode(open(fp, 'rb').read()).decode()
_d=json.load(open('progs.json')); _fm(_d['programs'])
data=json.dumps(_d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
os.makedirs('out_days', exist_ok=True)
for f in os.listdir('out_days'): os.remove('out_days/' + f)
_days = sorted(set(p['day'] for p in _d['programs'])); _names = []
for dd in _days:
    nm = f'data_day{dd}.json'; _names.append(nm)
    open('out_days/' + nm, 'w').write(json.dumps({'programs': [p for p in _d['programs'] if p['day'] == dd]}, ensure_ascii=False, separators=(',', ':')))
import shutil as _sh
for _d2 in range(1, 12):
    if os.path.exists(f'/home/claude/maps/out/day{_d2}.html'): _sh.copyfile(f'/home/claude/maps/out/day{_d2}.html', f'out_days/maps_day{_d2}.html')
bootjs = js.replace('(() => {\n', 'window.__benchBoot = () => {\n', 1)
assert bootjs.rstrip().endswith('})();'); bootjs = bootjs.rstrip()[:-len('})();')] + '};\n'
loader = '''(async () => { const st = document.getElementById('bootMsg'); const names = %s;
  try { const parts = await Promise.all(names.map(n => fetch(n).then(r => { if (!r.ok) throw new Error(n); return r.json(); })));
    window.__BENCH_DATA = {programs: parts.flatMap(p => p.programs)}; if (st) st.remove(); window.__benchBoot(); }
  catch (e){ if (st) st.textContent = 'مقدرتش أحمّل داتا البنش. افتح الصفحة تاني.'; } })();''' % json.dumps(_names)
out=tpl.replace('%%BASECSS%%',css).replace('%%JS%%','window.CMD_TABLE = true;\n'+bootjs+'\n'+loader).replace('%%DATA%%','{"programs":[]}').replace('%%BYTES%%', open('sizes/frag_all.html').read())
out=out.replace('<canvas id="gl"', '<div id="bootMsg" style="position:fixed;inset:auto 0 50% 0;text-align:center;z-index:70;font:600 16px sans-serif;color:#888">بيحمّل البنش…</div><canvas id="gl"', 1)
import re as _re, base64 as _b64, io as _io
from PIL import Image as _Im
_cache = {}
def _webp(m):
    b = m.group(1)
    if b in _cache: return _cache[b]
    raw = _b64.b64decode(b); im = _Im.open(_io.BytesIO(raw)); bio = _io.BytesIO()
    im.save(bio, 'WEBP', lossless=True, method=4); w = bio.getvalue()
    r = ('data:image/webp;base64,' + _b64.b64encode(w).decode()) if len(w) < len(raw) else m.group(0)
    _cache[b] = r; return r
out = _re.sub(r'data:image/png;base64,([A-Za-z0-9+/=]+)', _webp, out)  # lossless: same pixels, smaller page (16 MB limit)
for nm in _names:
    t_ = open('out_days/' + nm).read(); open('out_days/' + nm, 'w').write(_re.sub(r'data:image/png;base64,([A-Za-z0-9+/=]+)', _webp, t_))
out = '<meta charset="utf-8">\n' + out if not out.lstrip().lower().startswith('<meta charset') else out
open('bench_days.html','w').write(out)
open('app_full.js','w').write(js)
print(len(out))
