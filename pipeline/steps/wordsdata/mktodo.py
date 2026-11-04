import sys, re, json, importlib, html as H
sys.path.insert(0,'/home/claude/steps')
for p in ['/home/claude/day1','/home/claude/day2','/home/claude/day3','/home/claude/day4']: sys.path.insert(0,p)
def norm(t): return re.sub(r'\s+',' ',t).strip()
cur=set()
for f in ['/home/claude/day1/week2_day1_web.html','/home/claude/day2/week2_day2_web.html','/home/claude/day3/week2_day3_web.html','/home/claude/day4/week2_day4_web.html']:
    for m in re.finditer(r'<div class="wline"[^>]*>.*?<span class="ltr">(.*?)</span>', open(f).read(), re.S):
        cur.add(norm(H.unescape(re.sub('<[^>]+>','',m.group(1)))))
json.dump(sorted(cur),open('/home/claude/steps/wordsdata/curated.json','w'),ensure_ascii=False)
Es={1:importlib.import_module('full_data2').E,2:importlib.import_module('data2').E,3:importlib.import_module('data3').E,4:importlib.import_module('data4').E}
for d in range(1,5):
    E=Es[d]; En={norm(k):v for k,v in E.items()}
    P=importlib.import_module(f'specs_d{d}').programs()
    seen=set(); out=[]; todo=[]
    for key,pr in P.items():
        for fn,path in pr.files.items():
            out.append(f'\n===== program {pr.pid} · file {fn}  ({path})')
            for i,l in enumerate(open(path),1):
                t=norm(l)
                mark=' '
                if t and t not in cur and t not in seen:
                    mark='*'; seen.add(t); todo.append(t)
                out.append(f'{mark}{i:4}| {l.rstrip()}')
                if mark=='*' and t in En: out.append(f'      ↳ الشرح الموجود: {re.sub("<[^>]+>","",En[t])}')
    open(f'/home/claude/steps/wordsdata/todo_d{d}.txt','w').write(f'Day {d}: {len(todo)} lines marked * need a word-by-word breakdown\n'+'\n'.join(out))
    json.dump(todo,open(f'/home/claude/steps/wordsdata/todo_d{d}.json','w'),ensure_ascii=False)
    print(d,len(todo))
