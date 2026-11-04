import json
tpl=open('tpl.html').read(); css=open('base.css').read()
js=open('app.js').read().replace('(() => {\n', '(() => {\n' + open('why.js').read() + '\nwindow.__bench = {role: (v, j) => useRole(v, j), uses: k => allUses(k), progs: () => PROGS, load: id => loadProgram(id), st: () => ST, why: k => whyHtml(k), text: k => stepText(ST[k]), go: k => go(k), agent: t => window.__agent && window.__agent.ask(t), dyn: () => [Object.keys(crates), Object.keys(tags)], scale: () => Object.fromEntries(Object.entries(crates).map(([k, c]) => [k, +c.scale.x.toFixed(2)]))};\n', 1).replace('%%GLOSS%%', open('gloss.js').read()).replace('\nsyncPause();\nrequestAnimationFrame(frame);\n})();', '\nconst AG_SEM = ' + open('sem/sem.json').read() + ';\nconst AG_MODEL = ' + open('model/learned.json').read() + ';\nconst AG_KB = ' + __import__('json').dumps([dict(e, pid=__import__('os').path.basename(f)[:-5]) for f in sorted(__import__('glob').glob('kb/*.json')) for e in __import__('json').load(open(f))], ensure_ascii=False) + ';\n' + open('agent.js').read() + '\nsyncPause();\nrequestAnimationFrame(frame);\n})();')
allp=json.load(open('progs.json'))['programs']
import base64, os
def _fm(ps):
    for p in ps:
        for ext, mt in (('.q.png', 'image/png'), ('.webp', 'image/webp')):
            fp = f'fmap/{p["id"]}{ext}'
            if os.path.exists(fp): p['fmap'] = f'data:{mt};base64,' + base64.b64encode(open(fp, 'rb').read()).decode()
_fm(allp)
W3 = {8: 1, 9: 2}
for d in [1,2,3,4,5,6,7,8,9]:
    ps=[p for p in allp if p['day']==d]
    data=json.dumps({'programs':ps},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    kinds=sorted(set(p['kind'] for p in ps))
    DN = f'الأسبوع 3 · اليوم {W3[d]}' if d in W3 else f'اليوم {d}'
    t=(tpl.replace('<title>بنش كل الأيام</title>', f'<title>بنش {DN}</title>' if d in W3 else f'<title>بنش اليوم {d}</title>')
          .replace('<div class="numeral">6</div>', f'<div class="numeral">{W3.get(d, d)}</div>')
          .replace('الأسبوع 2 و 3 · محاضرات الرسم والـ CAD · كل الأيام', ('' if d in W3 else 'الأسبوع 2 · ') + f'{DN} · ' + ' و '.join('محاضرة '+k if k=='رسم' else k for k in kinds) + f' · {len(ps)} برامج'))
    j=js.replace("'bench06'", f"'bench06_d{d}'")
    j = 'window.CMD_TABLE = true;\n' + j
    out=t.replace('%%BASECSS%%',css).replace('%%JS%%',j).replace('%%DATA%%',data).replace('%%BYTES%%', open(f'sizes/frag_day{d}.html').read())
    open(f'bench_day{d}.html','w').write(out); print(d, len(ps), len(out))
open('app_full.js','w').write(js)
