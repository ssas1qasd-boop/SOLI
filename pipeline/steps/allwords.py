import sys, importlib, re, html
def all_words():
    out = {}
    for d, mods in [('day1', ['words']), ('day2', ['words2']), ('day3', ['words3']), ('day4', ['words4']), ('day5', ['words5']), ('day6', ['words6']), ('day7', ['words7']), ('day8', ['words8']), ('day9', ['words9'])]:
        sys.path.insert(0, f'/home/claude/{d}')
        for m in mods:
            try: M = importlib.import_module(m)
            except Exception as e: print('skip', d, m, e); continue
            for k, v in vars(M).items():
                if isinstance(v, list):
                    for w in v:
                        if isinstance(w, str) and w.startswith('<div class="wline">'):
                            t = html.unescape(re.search(r'<span class="ltr">(.*?)</span>', w).group(1))
                            out.setdefault(re.sub(r'\s+', ' ', t.strip()), w)
        sys.path.pop(0)
    return out
if __name__ == '__main__':
    A = all_words(); print(len(A))
