# Full bench: shell from bench_days.html (current app.js/tpl) + data for every day.
# Days without local progs (1-14) come from the published repo's bench/ folder.
import json, os, re, shutil
REPO = '/home/claude/SOLI/bench'
for d in range(1, 21):
    for nm in (f'data_day{d}.json', f'maps_day{d}.html'):
        if not os.path.exists('out_days/' + nm) and os.path.exists(f'{REPO}/{nm}'):
            shutil.copyfile(f'{REPO}/{nm}', 'out_days/' + nm)
days = sorted(int(m.group(1)) for f in os.listdir('out_days') if (m := re.fullmatch(r'data_day(\d+)\.json', f)))
names = [f'data_day{d}.json' for d in days]
src = open('bench_days.html').read()
old = re.search(r'const names = (\["data_day[^\]]*\]);', src).group(0)
src = src.replace(old, f'const names = {json.dumps(names)};', 1)
src = src.replace('الأسبوع 2 و 3 · محاضرات الرسم والـ CAD · كل الأيام', 'الأسابيع 2 و 3 و 4 · محاضرات الرسم والـ CAD والـ Templates · كل الأيام')
open('bench_full.html', 'w').write(src)
print('days', days, len(src))
