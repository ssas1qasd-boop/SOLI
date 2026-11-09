# Build one standalone bench HTML per week (data + maps embedded; opens offline from a file).
import json, re, sys
src = open('bench_days.html').read()
names_old = re.search(r"const names = (\[[^\]]*\]);", src).group(1)
SKEL = '<!doctype html><html lang="ar"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
SHIM = '''<script>(() => { const real = window.fetch ? window.fetch.bind(window) : null;
  window.fetch = (u, ...a) => { const n = String(u).split('/').pop().split('?')[0]; const el = document.getElementById('f-' + n);
    if (el) { const t = n.endsWith('.json') ? el.textContent : JSON.parse(el.textContent);
      return Promise.resolve(new Response(t, {status: 200, headers: {'Content-Type': n.endsWith('.json') ? 'application/json' : 'text/html'}})); }
    return real ? real(u, ...a) : Promise.reject(new Error(n)); }; })();</script>'''
for week, days in ((2, range(1, 8)), (3, range(8, 15)), (4, range(15, 21))):
    if not all(__import__('os').path.exists(f'out_days/data_day{d}.json') for d in days): continue
    blobs, names = [], []
    for d in days:
        nm = f'data_day{d}.json'; names.append(nm)
        blobs.append(f'<script type="application/json" id="f-{nm}">' + open('out_days/' + nm).read().replace('</', '<\\/') + '</script>')
        mp = f'maps_day{d}.html'
        blobs.append(f'<script type="application/json" id="f-{mp}">' + json.dumps(open('out_days/' + mp).read(), ensure_ascii=False).replace('</', '<\\/') + '</script>')
    body = src.replace(f'const names = {names_old};', f'const names = {json.dumps(names)};', 1)
    KICK = {2: 'الأسبوع 2 · محاضرات الرسم والـ CAD · كل الأيام', 3: 'الأسبوع 3 · محاضرات الرسم والـ CAD · كل الأيام', 4: 'الأسبوع 4 · Templates والتحويلات · كل الأيام'}
    body = body.replace('الأسبوع 2 و 3 · محاضرات الرسم والـ CAD · كل الأيام', KICK[week]).replace('<title>بنش كل الأيام</title>', f'<title>بنش الأسبوع {week}</title>')
    if body.lstrip().lower().startswith('<meta charset="utf-8">'): body = body.lstrip()[len('<meta charset="utf-8">'):]
    out = SKEL + SHIM + ''.join(blobs) + body
    fn = f'/home/claude/bench2/Bench_Week{week}.html'
    open(fn, 'w').write(out)
    print(fn, round(len(out.encode()) / 1e6, 1), 'MB')
