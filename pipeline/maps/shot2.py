import re, sys
day, pid, scheme = sys.argv[1], sys.argv[2], sys.argv[3]
h = open(f'/home/claude/maps/out/day{day}.html').read()
css = re.search(r'<style>(.*?)</style>', h, re.S).group(1)
sec = h[h.index(f'id="{pid}"'):]
svg = re.search(r'<svg.*?</svg>', sec, re.S).group(0)
open('/tmp/claude-0/svgtest.html','w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css} body{{margin:0;padding:0}} svg{{width:800px;display:block}}</style></head><body>{svg}</body></html>')
